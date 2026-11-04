'use strict';
// Offline license keys: "<base64url(payload JSON)>.<base64url(Ed25519 signature)>".
// The app only holds the PUBLIC key, so keys can't be forged from the app.
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const PUBLIC_KEY_FILE = path.join(__dirname, 'license-public.pem');

function b64url(buf) {
  return Buffer.from(buf).toString('base64url');
}

function sign(payload, privateKeyPem) {
  const body = b64url(JSON.stringify(payload));
  const sig = crypto.sign(null, Buffer.from(body), privateKeyPem);
  return `${body}.${b64url(sig)}`;
}

/** Returns { valid: true, payload } or { valid: false, reason }. */
function verify(key, publicKeyPem) {
  if (!publicKeyPem) return { valid: false, reason: 'not-configured' };
  const trimmed = String(key || '').trim();
  const parts = trimmed.split('.');
  if (parts.length !== 2 || !parts[0] || !parts[1]) return { valid: false, reason: 'malformed' };
  let ok = false;
  try {
    ok = crypto.verify(null, Buffer.from(parts[0]), publicKeyPem, Buffer.from(parts[1], 'base64url'));
  } catch {
    return { valid: false, reason: 'malformed' };
  }
  if (!ok) return { valid: false, reason: 'bad-signature' };
  try {
    const payload = JSON.parse(Buffer.from(parts[0], 'base64url').toString('utf8'));
    if (payload.plan !== 'pro') return { valid: false, reason: 'wrong-plan' };
    return { valid: true, payload };
  } catch {
    return { valid: false, reason: 'malformed' };
  }
}

function loadPublicKey(file = PUBLIC_KEY_FILE) {
  try {
    return fs.readFileSync(file, 'utf8');
  } catch {
    return null;
  }
}

module.exports = { sign, verify, loadPublicKey, PUBLIC_KEY_FILE };
