'use strict';
const test = require('node:test');
const assert = require('node:assert');
const crypto = require('crypto');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { sign, verify } = require('../src/license');
const { SettingsStore, sanitize } = require('../src/settings-store');
const { cpuPercent } = require('../src/stats');
const { parseLine } = require('../src/media-win');

const { publicKey, privateKey } = crypto.generateKeyPairSync('ed25519');
const pub = publicKey.export({ type: 'spki', format: 'pem' });
const priv = privateKey.export({ type: 'pkcs8', format: 'pem' });

test('license: valid key verifies and carries the email', () => {
  const key = sign({ plan: 'pro', email: 'a@b.co' }, priv);
  const r = verify(key, pub);
  assert.equal(r.valid, true);
  assert.equal(r.payload.email, 'a@b.co');
});

test('license: tampered payload, foreign key, garbage and wrong plan are rejected', () => {
  const key = sign({ plan: 'pro', email: 'a@b.co' }, priv);
  const [, sig] = key.split('.');
  const forged = Buffer.from(JSON.stringify({ plan: 'pro', email: 'x@y.z' })).toString('base64url') + '.' + sig;
  assert.equal(verify(forged, pub).reason, 'bad-signature');
  const other = crypto.generateKeyPairSync('ed25519').privateKey.export({ type: 'pkcs8', format: 'pem' });
  assert.equal(verify(sign({ plan: 'pro' }, other), pub).reason, 'bad-signature');
  assert.equal(verify('nonsense', pub).reason, 'malformed');
  assert.equal(verify('', pub).reason, 'malformed');
  assert.equal(verify(sign({ plan: 'free' }, priv), pub).reason, 'wrong-plan');
  assert.equal(verify(key, null).reason, 'not-configured');
});

test('settings: defaults, clamping, persistence, deep merge', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'onair-'));
  const s = new SettingsStore(dir);
  assert.equal(s.get().position, 'top');
  s.set({ position: 'bottom', height: 999, obs: { port: 4456 }, widgets: { clock: false } });
  const again = new SettingsStore(dir).get();
  assert.equal(again.position, 'bottom');
  assert.equal(again.height, 72);
  assert.equal(again.obs.port, 4456);
  assert.equal(again.obs.host, '127.0.0.1');
  assert.equal(again.widgets.clock, false);
  assert.equal(again.widgets.obs, true);
  assert.equal(sanitize({ position: 'left' }).position, 'top');
  assert.deepEqual(sanitize({ runOfShow: ['  a ', '', 'b'] }).runOfShow, ['a', 'b']);
});

test('settings: corrupt file falls back to defaults', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'onair-'));
  fs.writeFileSync(path.join(dir, 'settings.json'), '{not json');
  assert.equal(new SettingsStore(dir).get().height, 48);
});

test('stats: cpu percent from snapshots', () => {
  assert.equal(cpuPercent({ idle: 100, total: 200 }, { idle: 150, total: 300 }), 50);
  assert.equal(cpuPercent({ idle: 0, total: 0 }, { idle: 0, total: 0 }), 0);
});

test('media: parses PowerShell lines', () => {
  assert.deepEqual(parseLine('{"title":"Song","artist":"Band","status":"Playing","app":"Spotify"}'), { available: true, playing: true, title: 'Song', artist: 'Band' });
  assert.deepEqual(parseLine('{}'), { available: true, playing: false, title: '', artist: '' });
  assert.deepEqual(parseLine('{"error":"unavailable"}'), { available: false });
  assert.equal(parseLine('garbage'), null);
});
