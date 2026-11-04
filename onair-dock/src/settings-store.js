'use strict';
const fs = require('fs');
const path = require('path');

const DEFAULTS = Object.freeze({
  position: 'top', // 'top' | 'bottom'
  height: 48,
  launchAtLogin: false,
  widgets: {
    obs: true,
    nowPlaying: true,
    runOfShow: true,
    streamTimer: true,
    breakTimer: true,
    system: true,
    clock: true,
  },
  obs: { host: '127.0.0.1', port: 4455, password: '' },
  runOfShow: ['Intro + hellos', 'Main segment', 'Q&A with chat', 'Raid someone'],
  breakMinutes: 5,
  license: '',
});

function merge(base, patch) {
  if (patch === null || typeof patch !== 'object' || Array.isArray(patch)) return patch;
  const out = { ...base };
  for (const [k, v] of Object.entries(patch)) {
    out[k] = base && typeof base[k] === 'object' && !Array.isArray(base[k]) && base[k] !== null
      ? merge(base[k], v)
      : v;
  }
  return out;
}

function sanitize(s) {
  const out = merge(DEFAULTS, s || {});
  out.position = out.position === 'bottom' ? 'bottom' : 'top';
  out.height = Math.min(72, Math.max(36, Number(out.height) || DEFAULTS.height));
  out.obs.port = Math.min(65535, Math.max(1, Number(out.obs.port) || 4455));
  out.obs.host = String(out.obs.host || '127.0.0.1').slice(0, 253);
  out.breakMinutes = Math.min(120, Math.max(1, Number(out.breakMinutes) || 5));
  out.runOfShow = (Array.isArray(out.runOfShow) ? out.runOfShow : [])
    .map((x) => String(x).trim().slice(0, 80)).filter(Boolean).slice(0, 30);
  out.license = String(out.license || '').trim();
  out.launchAtLogin = Boolean(out.launchAtLogin);
  return out;
}

class SettingsStore {
  constructor(dir) {
    this.file = path.join(dir, 'settings.json');
    this.data = sanitize(this.#read());
  }

  #read() {
    try {
      return JSON.parse(fs.readFileSync(this.file, 'utf8'));
    } catch {
      return {};
    }
  }

  get() {
    return structuredClone(this.data);
  }

  set(patch) {
    this.data = sanitize(merge(this.data, patch));
    fs.mkdirSync(path.dirname(this.file), { recursive: true });
    const tmp = this.file + '.tmp';
    fs.writeFileSync(tmp, JSON.stringify(this.data, null, 2));
    fs.renameSync(tmp, this.file);
    return this.get();
  }
}

module.exports = { SettingsStore, DEFAULTS, sanitize, merge };
