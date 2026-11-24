const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const dir = __dirname, mode = process.argv[2] || 'stills';
  const tl = JSON.parse(fs.readFileSync(dir + '/timeline.json'));
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e)));
  await p.goto('file://' + dir + '/short.html');
  await p.evaluate(t => window.setup(t), tl);
  await p.evaluate(() => document.fonts.ready);
  const times = mode === 'stills' ? (process.argv[3] || "1,3.9,6,7.5,10,12.4,17.5,20.6,23,27").split(',').map(Number)
    : Array.from({ length: Math.ceil(tl.total * 30) }, (_, i) => i / 30);
  const out = dir + (mode === 'stills' ? '/stills' : '/frames');
  fs.mkdirSync(out, { recursive: true });
  for (let i = 0; i < times.length; i++) {
    await p.evaluate(t => window.frame(t), times[i]);
    await p.screenshot({ path: `${out}/${mode === 'stills' ? 's_' + times[i] : String(i).padStart(5, '0')}.jpg`, type: 'jpeg', quality: 93 });
  }
  console.log('frames', times.length, 'errors', errs.length ? errs : 'none');
  await b.close();
})();
