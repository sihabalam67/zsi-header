#!/usr/bin/env node
'use strict';
// Blocks a release build that would ship with everything unlocked or with no way to pay.
const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');
const problems = [];

const pubFile = path.join(root, 'src', 'license-public.pem');
if (!fs.existsSync(pubFile)) {
  problems.push('src/license-public.pem is missing. Run `npm run license:init` once and commit the public key. Without it every copy is Pro for free.');
}

const config = JSON.parse(fs.readFileSync(path.join(root, 'src', 'config.json'), 'utf8'));
if (!/^https:\/\/(buy|checkout)\.stripe\.com\/[A-Za-z0-9_\-/]+$/.test(config.buyUrl) || /REPLACE/.test(config.buyUrl)) {
  problems.push('src/config.json "buyUrl" must be your real Stripe Payment Link (https://buy.stripe.com/...).');
}

if (!fs.existsSync(path.join(root, 'build', 'icon.png'))) problems.push('build/icon.png is missing.');

if (problems.length) {
  console.error('Release check failed:\n- ' + problems.join('\n- '));
  process.exit(1);
}
console.log('Release check passed.');
