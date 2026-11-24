// node rec.js <timeline.json> stills "t1,t2,..." | full <outdir> [from] [to]
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const dir = __dirname, B = dir + '/../build/s01';
  const tl = JSON.parse(fs.readFileSync(process.argv[2])), dca = JSON.parse(fs.readFileSync(B + '/dca.json')), N = JSON.parse(fs.readFileSync(B + '/N.json'));
  const mode = process.argv[3];
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e)));
  await p.goto('file://' + dir + '/story.html'); await p.evaluate(() => document.fonts.ready);
  await p.evaluate(([a, c, n]) => window.setup(a, c, n), [tl, dca, N]);
  if (mode === 'stills') {
    const ts = process.argv[4].split(',').map(Number); fs.mkdirSync(B + '/stills', { recursive: true });
    for (const t of ts) { await p.evaluate(t => window.frame(t), t); await p.screenshot({ path: `${B}/stills/s_${t.toFixed(1)}.jpg`, type: 'jpeg', quality: 85 }); }
  } else {
    const out = process.argv[4], from = +(process.argv[5] || 0), to = +(process.argv[6] || Math.ceil(tl.total * 30)); fs.mkdirSync(out, { recursive: true });
    for (let i = from; i < to; i++) { await p.evaluate(t => window.frame(t), i / 30); await p.screenshot({ path: `${out}/${String(i).padStart(6, '0')}.jpg`, type: 'jpeg', quality: 92 }); }
  }
  console.log('errors', errs.length ? errs.slice(0, 5) : 'none'); await b.close();
})();
