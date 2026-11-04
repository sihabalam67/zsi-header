#!/usr/bin/env node
'use strict';
// npm run license:init            -> creates keys/private.pem (keep secret!) and src/license-public.pem
// npm run license:issue -- a@b.co -> prints a Pro license key for that buyer
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const { sign, verify, PUBLIC_KEY_FILE } = require('../src/license');

const ROOT = path.join(__dirname, '..');
const PRIVATE_KEY_FILE = path.join(ROOT, 'keys', 'private.pem');

function init() {
  if (fs.existsSync(PRIVATE_KEY_FILE)) {
    console.error(`Refusing to overwrite ${PRIVATE_KEY_FILE}. Every key you already sold depends on it.`);
    process.exit(1);
  }
  const { publicKey, privateKey } = crypto.generateKeyPairSync('ed25519');
  fs.mkdirSync(path.dirname(PRIVATE_KEY_FILE), { recursive: true });
  fs.writeFileSync(PRIVATE_KEY_FILE, privateKey.export({ type: 'pkcs8', format: 'pem' }), { mode: 0o600 });
  fs.writeFileSync(PUBLIC_KEY_FILE, publicKey.export({ type: 'spki', format: 'pem' }));
  console.log(`Private key: ${PRIVATE_KEY_FILE}`);
  console.log('  -> back it up somewhere safe (password manager). Never commit it; keys/ is in .gitignore.');
  console.log(`Public key:  ${PUBLIC_KEY_FILE}`);
  console.log('  -> commit this one. It ships inside the app.');
}

function issue(email) {
  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    console.error('Usage: npm run license:issue -- buyer@example.com');
    process.exit(1);
  }
  const priv = fs.readFileSync(PRIVATE_KEY_FILE, 'utf8');
  const key = sign({ plan: 'pro', email, issued: new Date().toISOString().slice(0, 10) }, priv);
  const pub = fs.readFileSync(PUBLIC_KEY_FILE, 'utf8');
  if (!verify(key, pub).valid) {
    console.error('Self-check failed: private and public keys do not match.');
    process.exit(1);
  }
  console.log(key);
}

const [cmd, arg] = process.argv.slice(2);
if (cmd === 'init') init();
else if (cmd === 'issue') issue(arg);
else {
  console.error('Usage: node tools/license.js init | issue <email>');
  process.exit(1);
}
