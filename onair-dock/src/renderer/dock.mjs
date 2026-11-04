import { ObsClient } from './obs-client.mjs';
import { fmtDuration, fmtClock, nextItem } from './format.mjs';

const $ = (id) => document.getElementById(id);
const api = window.dock;

let state = null;
let obs = null;
let obsKey = '';
let obsState = null;

// ---------- local, per-machine conveniences ----------
const local = {
  get(key, fallback) {
    try {
      const v = localStorage.getItem(key);
      return v === null ? fallback : JSON.parse(v);
    } catch {
      return fallback;
    }
  },
  set(key, value) {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch {
      /* storage unavailable: state just won't survive a restart */
    }
  },
};

// ---------- widget visibility + Pro gating ----------
function applyWidgets() {
  const { settings, isPro, proWidgets } = state;
  for (const el of document.querySelectorAll('[data-widget]')) {
    const name = el.dataset.widget;
    el.classList.toggle('hidden', !settings.widgets[name]);
    const locked = !isPro && proWidgets.includes(name);
    el.classList.toggle('locked', locked);
    el.title = locked ? 'Pro feature: click to unlock' : '';
  }
}

document.addEventListener('click', (e) => {
  const locked = e.target.closest('.widget.locked');
  if (locked) {
    e.stopPropagation();
    e.preventDefault();
    api.openSettings();
  }
}, true);

function proOn(name) {
  return state.settings.widgets[name] && (state.isPro || !state.proWidgets.includes(name));
}

// ---------- OBS ----------
function syncObs() {
  const { host, port, password } = state.settings.obs;
  const key = proOn('obs') ? `${host}:${port}:${password}` : '';
  if (key === obsKey) return;
  obsKey = key;
  if (obs) obs.close();
  obs = null;
  obsState = null;
  renderObs();
  if (!key) return;
  obs = new ObsClient({ host, port, password });
  obs.on('status', renderObs);
  obs.on('state', (s) => {
    obsState = s;
    renderObs();
  });
  obs.connect();
}

function renderObs() {
  const status = obs ? obs.status : 'disconnected';
  const live = $('obs-live');
  const rec = $('obs-rec');
  const scenesEl = $('obs-scenes');
  const statusEl = $('obs-status');
  const connected = status === 'connected' && obsState;

  statusEl.classList.toggle('hidden', connected);
  statusEl.textContent = status === 'auth-failed'
    ? 'OBS password wrong: check Settings'
    : status === 'connecting' ? 'Connecting to OBS…' : 'OBS not connected';

  if (!connected) {
    live.className = 'badge off';
    live.textContent = 'OFFLINE';
    rec.classList.add('hidden');
    scenesEl.replaceChildren();
    return;
  }

  live.className = obsState.streaming ? 'badge live' : 'badge off';
  rec.classList.toggle('hidden', !obsState.recording);

  const existing = [...scenesEl.children].map((b) => b.dataset.scene).join('\u0000');
  if (existing !== obsState.scenes.join('\u0000')) {
    scenesEl.replaceChildren(
      ...obsState.scenes.slice(0, 8).map((name) => {
        const b = document.createElement('button');
        b.className = 'scene';
        b.dataset.scene = name;
        b.textContent = name;
        b.title = `Switch to “${name}”`;
        b.addEventListener('click', () => obs.setScene(name).catch(() => {}));
        return b;
      })
    );
  }
  for (const b of scenesEl.children) b.classList.toggle('active', b.dataset.scene === obsState.currentScene);
}

// ---------- now playing ----------
let lastMedia = { available: false };
function renderMedia() {
  const m = lastMedia;
  $('np-title').textContent = !m.available ? 'Media info unavailable' : m.title || 'Nothing playing';
  $('np-artist').textContent = m.available && m.artist ? `· ${m.artist}` : '';
  $('np-toggle').textContent = m.playing ? '⏸' : '▶';
}
api.onMedia((m) => {
  lastMedia = m;
  renderMedia();
});
$('np-toggle').addEventListener('click', () => api.mediaCommand('toggle'));
$('np-next').addEventListener('click', () => api.mediaCommand('next'));
$('np-prev').addEventListener('click', () => api.mediaCommand('prev'));

// ---------- run of show ----------
function renderRunOfShow() {
  const items = state.settings.runOfShow;
  const done = Math.min(local.get('ros.done', 0), items.length);
  const idx = nextItem(items, done);
  const el = $('ros-item');
  el.textContent = items.length === 0 ? 'Add segments in Settings' : idx === -1 ? 'All done 🎉' : items[idx];
  el.classList.toggle('done', idx === -1 && items.length > 0);
  $('ros-progress').textContent = items.length ? `${done}/${items.length}` : '';
}
$('ros-done').addEventListener('click', () => {
  local.set('ros.done', Math.min(local.get('ros.done', 0) + 1, state.settings.runOfShow.length));
  renderRunOfShow();
});
$('ros-reset').addEventListener('click', () => {
  local.set('ros.done', 0);
  renderRunOfShow();
});

// ---------- stream timer (manual; shows OBS uptime when OBS is live) ----------
$('st-toggle').addEventListener('click', () => {
  const started = local.get('st.startedAt', 0);
  local.set('st.startedAt', started ? 0 : Date.now());
  tick();
});

// ---------- break timer ----------
$('brb-btn').addEventListener('click', () => {
  local.set('brb.endsAt', Date.now() + state.settings.breakMinutes * 60_000);
  tick();
});
$('brb-end').addEventListener('click', () => {
  local.set('brb.endsAt', 0);
  tick();
});

// ---------- system ----------
api.onStats((s) => {
  $('cpu').textContent = `${s.cpu}%`;
  $('ram').textContent = `${s.ram}%`;
});

// ---------- 1-second tick ----------
function tick() {
  const now = Date.now();
  $('clock').textContent = fmtClock(new Date(now));

  if (obsState && obsState.streaming && obsState.streamStartedAt) {
    $('obs-live').textContent = `LIVE ${fmtDuration(now - obsState.streamStartedAt)}`;
  } else if (obsState && obs && obs.status === 'connected') {
    $('obs-live').textContent = 'OFFLINE';
  }
  if (obsState && obsState.recording && obsState.recordStartedAt) {
    $('obs-rec').textContent = `REC ${fmtDuration(now - obsState.recordStartedAt)}`;
  }

  const started = local.get('st.startedAt', 0);
  $('st-time').textContent = started ? fmtDuration(now - started) : '0:00';
  $('st-toggle').textContent = started ? '■' : '▶';

  const endsAt = state && proOn('breakTimer') ? local.get('brb.endsAt', 0) : 0;
  const overlay = $('break-overlay');
  overlay.classList.toggle('hidden', !endsAt);
  if (endsAt) {
    const left = endsAt - now;
    $('brb-time').textContent = left > 0 ? fmtDuration(left) : 'Time’s up!';
    overlay.classList.toggle('flash', left <= 0);
  }
}

// ---------- boot ----------
$('open-settings').addEventListener('click', () => api.openSettings());

function onState(s) {
  state = s;
  applyWidgets();
  syncObs();
  renderRunOfShow();
  renderMedia();
  tick();
}

api.onState(onState);
api.getState().then(onState);
setInterval(tick, 1000);
