// Render thumbnail specs: node thumbs4/render.js specs.json [name ...]  -> out/thumbs/<name>.jpg (1280x720) + _full.png
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const dir = __dirname, specs = JSON.parse(fs.readFileSync(process.argv[2]));
  const only = process.argv.slice(3);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e)));
  await p.goto('file://' + dir + '/thumb.html');
  await p.evaluate(() => document.fonts.ready);
  for (const [name, spec] of Object.entries(specs)) {
    if (only.length && !only.includes(name)) continue;
    const sp = JSON.parse(JSON.stringify(spec).replace(/"thumbsrc\//g, '"file://' + path.resolve(dir, '../assets/thumbsrc') + '/'));
    await p.evaluate(s => window.render(s), sp);
    await p.waitForTimeout(300);
    const png = path.resolve(dir, '../out/thumbs', name + '_full.png');
    await p.screenshot({ path: png });
    console.log('rendered', name);
  }
  console.log('errors:', errs.length ? errs : 'none');
  await b.close();
})();
