// node rec.js stills "t1,t2" | node rec.js pipe out.mp4
const { chromium } = require('playwright'); const fs = require('fs'); const { spawn } = require('child_process');
(async () => {
  const dir = __dirname, mode = process.argv[2], tl = JSON.parse(fs.readFileSync(dir + '/timeline.json'));
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e)));
  await p.goto('file://' + dir + '/short.html'); await p.evaluate(() => document.fonts.ready); await p.evaluate(t => window.setup(t), tl);
  if (mode === 'stills') { fs.mkdirSync(dir + '/stills', { recursive: true });
    for (const t of process.argv[3].split(',').map(Number)) { await p.evaluate(t => window.frame(t), t); await p.screenshot({ path: `${dir}/stills/s_${t}.jpg`, type: 'jpeg', quality: 85 }); } }
  else { const out = process.argv[3], n = Math.ceil(tl.total * 30);
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', '30', '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', out], { stdio: ['pipe', 'inherit', 'inherit'] });
    for (let i = 0; i < n; i++) { await p.evaluate(t => window.frame(t), i / 30); const buf = await p.screenshot({ type: 'jpeg', quality: 92 }); if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r)); }
    ff.stdin.end(); await new Promise(r => ff.on('close', r)); }
  console.log('errors', errs.length ? errs.slice(0, 3) : 'none'); await b.close();
})();
