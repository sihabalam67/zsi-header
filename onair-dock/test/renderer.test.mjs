import test from 'node:test';
import assert from 'node:assert';
import crypto from 'node:crypto';
import { createRequire } from 'node:module';
import { fmtDuration, nextItem } from '../src/renderer/format.mjs';
import { ObsClient, authString } from '../src/renderer/obs-client.mjs';

const require = createRequire(import.meta.url);
const { WebSocketServer } = require('ws');

test('format: durations and run-of-show', () => {
  assert.equal(fmtDuration(0), '0:00');
  assert.equal(fmtDuration(75_000), '1:15');
  assert.equal(fmtDuration(3_723_000), '1:02:03');
  assert.equal(fmtDuration(-5), '0:00');
  assert.equal(nextItem(['a', 'b'], 1), 1);
  assert.equal(nextItem(['a', 'b'], 2), -1);
});

test('obs auth string matches the obs-websocket v5 spec', async () => {
  const b64 = (s) => crypto.createHash('sha256').update(s).digest('base64');
  const expected = b64(b64('pw' + 'salt') + 'chal');
  assert.equal(await authString('pw', 'salt', 'chal'), expected);
});

function fakeObs({ password }) {
  const salt = 'S4lt', challenge = 'Ch4llenge';
  const b64 = (s) => crypto.createHash('sha256').update(s).digest('base64');
  const expected = b64(b64(password + salt) + challenge);
  const wss = new WebSocketServer({ port: 0 });
  const seen = [];
  let current = 'Starting Soon';
  wss.on('connection', (ws) => {
    ws.send(JSON.stringify({ op: 0, d: { rpcVersion: 1, authentication: { salt, challenge } } }));
    ws.on('message', (raw) => {
      const m = JSON.parse(raw);
      if (m.op === 1) {
        if (m.d.authentication !== expected) return ws.close(4009, 'auth failed');
        assert.equal(m.d.eventSubscriptions, 69);
        return ws.send(JSON.stringify({ op: 2, d: { negotiatedRpcVersion: 1 } }));
      }
      if (m.op === 6) {
        seen.push(m.d.requestType);
        const reply = (responseData) => ws.send(JSON.stringify({ op: 7, d: { requestType: m.d.requestType, requestId: m.d.requestId, requestStatus: { result: true, code: 100 }, responseData } }));
        if (m.d.requestType === 'GetSceneList') reply({ currentProgramSceneName: current, scenes: [{ sceneName: 'BRB', sceneIndex: 0 }, { sceneName: 'Gameplay', sceneIndex: 1 }, { sceneName: 'Starting Soon', sceneIndex: 2 }] });
        else if (m.d.requestType === 'GetStreamStatus') reply({ outputActive: true, outputDuration: 60_000 });
        else if (m.d.requestType === 'GetRecordStatus') reply({ outputActive: false, outputDuration: 0 });
        else if (m.d.requestType === 'SetCurrentProgramScene') {
          current = m.d.requestData.sceneName;
          reply({});
          ws.send(JSON.stringify({ op: 5, d: { eventType: 'CurrentProgramSceneChanged', eventData: { sceneName: current } } }));
        }
      }
    });
  });
  return new Promise((r) => wss.on('listening', () => r({ wss, port: wss.address().port, seen })));
}

const waitFor = (fn, ms = 3000) => new Promise((resolve, reject) => {
  const t0 = Date.now();
  const iv = setInterval(() => {
    if (fn()) { clearInterval(iv); resolve(); } else if (Date.now() - t0 > ms) { clearInterval(iv); reject(new Error('timeout')); }
  }, 20);
});

test('obs client: authenticates, loads state, switches scene, follows events', async () => {
  const { wss, port, seen } = await fakeObs({ password: 'secret' });
  const c = new ObsClient({ port, password: 'secret' });
  c.connect();
  await waitFor(() => c.status === 'connected' && c.state.scenes.length === 3);
  assert.deepEqual(c.state.scenes, ['Starting Soon', 'Gameplay', 'BRB']);
  assert.equal(c.state.currentScene, 'Starting Soon');
  assert.equal(c.state.streaming, true);
  assert.ok(Date.now() - c.state.streamStartedAt >= 60_000);
  await c.setScene('Gameplay');
  await waitFor(() => c.state.currentScene === 'Gameplay');
  assert.ok(seen.includes('SetCurrentProgramScene'));
  c.close();
  wss.close();
});

test('obs client: wrong password ends in auth-failed without retry loop', async () => {
  const { wss, port } = await fakeObs({ password: 'secret' });
  const c = new ObsClient({ port, password: 'nope' });
  c.connect();
  await waitFor(() => c.status === 'auth-failed');
  c.close();
  wss.close();
});
