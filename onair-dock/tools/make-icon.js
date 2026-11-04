#!/usr/bin/env node
'use strict';
// Renders the app icon (build/icon.png 512px, src/renderer/icon.png 64px) with headless Chromium.
// Only needed if you change the design; the PNGs are committed.
const path = require('path');
const { chromium } = require('playwright');

const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#8f6bff"/><stop offset="1" stop-color="#4b2fd6"/>
    </linearGradient>
  </defs>
  <rect x="16" y="16" width="480" height="480" rx="112" fill="#14141b"/>
  <rect x="72" y="196" width="368" height="120" rx="40" fill="url(#g)"/>
  <circle cx="142" cy="256" r="26" fill="#ff3b5c"/>
  <rect x="190" y="242" width="96" height="28" rx="14" fill="#ffffff" opacity=".9"/>
  <rect x="302" y="242" width="96" height="28" rx="14" fill="#ffffff" opacity=".45"/>
</svg>`;

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  for (const [size, out] of [[512, 'build/icon.png'], [64, 'src/renderer/icon.png']]) {
    await page.setViewportSize({ width: size, height: size });
    await page.setContent(`<html><body style="margin:0;background:transparent">${svg.replace('<svg ', `<svg width="${size}" height="${size}" `)}</body></html>`);
    await page.screenshot({ path: path.join(__dirname, '..', out), omitBackground: true });
  }
  await browser.close();
  console.log('Icons written.');
})();
