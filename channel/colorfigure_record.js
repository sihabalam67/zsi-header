const { chromium } = require('playwright');
(async () => {
  const dir = __dirname;
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1080, height: 1080 },
    recordVideo: { dir: dir + '/vid', size: { width: 1080, height: 1080 } } });
  const p = await ctx.newPage();
  await p.goto('file://' + dir + '/toaster_out.html?xr=1&labels=1');
  await p.waitForTimeout(1500);
  for (let i = 0; i < 40; i++) { await p.keyboard.press('ArrowRight'); await p.waitForTimeout(80); }
  await p.waitForTimeout(800);
  const btns = await p.$$('button');
  const names = [];
  for (const bt of btns) names.push((await bt.innerText()).trim());
  for (const bt of btns) {
    const t = (await bt.innerText()).trim();
    if (/lever|toast|press|down|start/i.test(t)) { await bt.click(); break; }
  }
  await p.waitForTimeout(4000);
  const errs = await p.evaluate(() => document.documentElement.getAttribute('data-errors'));
  const v = p.video();
  await ctx.close(); await b.close();
  console.log('buttons:', names.join(' | '), '| errors:', errs, '| video:', await v.path());
})();
