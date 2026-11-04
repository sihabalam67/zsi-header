// Minimal obs-websocket v5 client (built into OBS Studio 28+).
// Works in the browser/Electron renderer and in Node 22 (global WebSocket + crypto.subtle).

const OP = { Hello: 0, Identify: 1, Identified: 2, Event: 5, Request: 6, RequestResponse: 7 };
// EventSubscription bits: General (1) | Scenes (4) | Outputs (64)
const EVENT_SUBS = 1 | 4 | 64;

async function sha256b64(text) {
  const bytes = new TextEncoder().encode(text);
  const hash = await crypto.subtle.digest('SHA-256', bytes);
  let bin = '';
  for (const b of new Uint8Array(hash)) bin += String.fromCharCode(b);
  return btoa(bin);
}

/** obs-websocket auth string: b64(sha256(b64(sha256(password + salt)) + challenge)) */
export async function authString(password, salt, challenge) {
  const secret = await sha256b64(password + salt);
  return sha256b64(secret + challenge);
}

export class ObsClient {
  constructor({ host = '127.0.0.1', port = 4455, password = '', WebSocketImpl = globalThis.WebSocket } = {}) {
    this.url = `ws://${host}:${port}`;
    this.password = password;
    this.WS = WebSocketImpl;
    this.ws = null;
    this.pending = new Map();
    this.nextId = 1;
    this.listeners = new Map();
    this.status = 'disconnected'; // disconnected | connecting | connected | auth-failed
    this.retryTimer = null;
    this.closedByUser = false;
    this.state = { scenes: [], currentScene: '', streaming: false, recording: false, streamStartedAt: 0, recordStartedAt: 0 };
  }

  on(event, fn) {
    if (!this.listeners.has(event)) this.listeners.set(event, new Set());
    this.listeners.get(event).add(fn);
    return () => this.listeners.get(event).delete(fn);
  }

  #emit(event, payload) {
    for (const fn of this.listeners.get(event) || []) fn(payload);
  }

  #setStatus(s) {
    this.status = s;
    this.#emit('status', s);
  }

  connect() {
    this.closedByUser = false;
    clearTimeout(this.retryTimer);
    this.#setStatus('connecting');
    let ws;
    try {
      ws = new this.WS(this.url);
    } catch {
      return this.#scheduleRetry();
    }
    this.ws = ws;
    ws.onmessage = (msg) => this.#onMessage(msg.data).catch(() => {});
    ws.onclose = (ev) => {
      this.ws = null;
      for (const { reject } of this.pending.values()) reject(new Error('disconnected'));
      this.pending.clear();
      if (ev && ev.code === 4009) {
        this.#setStatus('auth-failed'); // wrong password: don't hammer OBS
        return;
      }
      this.#setStatus('disconnected');
      if (!this.closedByUser) this.#scheduleRetry();
    };
    ws.onerror = () => {};
  }

  #scheduleRetry() {
    this.#setStatus('disconnected');
    clearTimeout(this.retryTimer);
    this.retryTimer = setTimeout(() => this.connect(), 5000);
  }

  close() {
    this.closedByUser = true;
    clearTimeout(this.retryTimer);
    if (this.ws) this.ws.close();
  }

  async #onMessage(raw) {
    const msg = JSON.parse(typeof raw === 'string' ? raw : raw.toString());
    const d = msg.d || {};
    switch (msg.op) {
      case OP.Hello: {
        const identify = { rpcVersion: 1, eventSubscriptions: EVENT_SUBS };
        if (d.authentication) identify.authentication = await authString(this.password, d.authentication.salt, d.authentication.challenge);
        this.ws.send(JSON.stringify({ op: OP.Identify, d: identify }));
        break;
      }
      case OP.Identified:
        this.#setStatus('connected');
        await this.refresh();
        break;
      case OP.RequestResponse: {
        const p = this.pending.get(d.requestId);
        if (!p) break;
        this.pending.delete(d.requestId);
        if (d.requestStatus && d.requestStatus.result) p.resolve(d.responseData || {});
        else p.reject(new Error((d.requestStatus && d.requestStatus.comment) || 'request failed'));
        break;
      }
      case OP.Event:
        this.#onEvent(d.eventType, d.eventData || {});
        break;
    }
  }

  request(requestType, requestData) {
    if (!this.ws || this.status !== 'connected') return Promise.reject(new Error('not connected'));
    const requestId = String(this.nextId++);
    return new Promise((resolve, reject) => {
      this.pending.set(requestId, { resolve, reject });
      this.ws.send(JSON.stringify({ op: OP.Request, d: { requestType, requestId, requestData } }));
      setTimeout(() => {
        if (this.pending.delete(requestId)) reject(new Error('timeout'));
      }, 5000);
    });
  }

  async refresh() {
    const [scenes, stream, record] = await Promise.all([
      this.request('GetSceneList'),
      this.request('GetStreamStatus'),
      this.request('GetRecordStatus'),
    ]);
    const now = Date.now();
    this.state = {
      // OBS lists scenes bottom-to-top; show them in the order the user sees in OBS.
      scenes: (scenes.scenes || []).slice().sort((a, b) => b.sceneIndex - a.sceneIndex).map((s) => s.sceneName),
      currentScene: scenes.currentProgramSceneName || '',
      streaming: Boolean(stream.outputActive),
      recording: Boolean(record.outputActive),
      streamStartedAt: stream.outputActive ? now - (stream.outputDuration || 0) : 0,
      recordStartedAt: record.outputActive ? now - (record.outputDuration || 0) : 0,
    };
    this.#emit('state', this.state);
  }

  #onEvent(type, data) {
    const s = this.state;
    switch (type) {
      case 'CurrentProgramSceneChanged':
        s.currentScene = data.sceneName;
        break;
      case 'SceneListChanged':
        s.scenes = (data.scenes || []).slice().sort((a, b) => b.sceneIndex - a.sceneIndex).map((x) => x.sceneName);
        break;
      case 'StreamStateChanged':
        s.streaming = Boolean(data.outputActive);
        s.streamStartedAt = s.streaming ? s.streamStartedAt || Date.now() : 0;
        break;
      case 'RecordStateChanged':
        s.recording = Boolean(data.outputActive);
        s.recordStartedAt = s.recording ? s.recordStartedAt || Date.now() : 0;
        break;
      default:
        return;
    }
    this.#emit('state', s);
  }

  setScene(sceneName) {
    return this.request('SetCurrentProgramScene', { sceneName });
  }
}
