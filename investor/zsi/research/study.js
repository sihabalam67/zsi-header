const { chromium } = require('playwright');
const fs = require('fs');
const OUT = process.argv[2];
const pages = [
 ['calc_overview','https://moosa-proposal-calculator.vercel.app/#overview'],
 ['calc_saas','https://moosa-proposal-calculator.vercel.app/#saas'],
 ['calc_goldenmark','https://moosa-proposal-calculator.vercel.app/#goldenmark'],
 ['calc_zsipay','https://moosa-proposal-calculator.vercel.app/#zsipay'],
 ['calc_misc','https://moosa-proposal-calculator.vercel.app/#misc'],
 ['kababking','https://kk-express.vercel.app/'],
 ['goldenmarkstore','https://goldenmarkstore.com/'],
 ['usamarry','https://usamarry.com/'],
 ['dgprint24','https://dgprint24.com/'],
 ['rpclimo','https://rpclimo.com/'],
 ['goldenmarkmoney','https://goldenmark.money/'],
];
(async () => {
  const b = await chromium.launch();
  for (const [name, url] of pages) {
    const ctx = await b.newContext({ viewport: { width: 1440, height: 900 } });
    const p = await ctx.newPage();
    try {
      await p.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
    } catch (e) { console.log(name, 'goto:', String(e).slice(0, 120)); }
    await p.waitForTimeout(2500);
    // scroll through to trigger lazy content
    const h = await p.evaluate(() => document.body.scrollHeight).catch(() => 0);
    for (let y = 0; y < h; y += 700) { await p.evaluate(v => window.scrollTo(0, v), y); await p.waitForTimeout(150); }
    await p.evaluate(() => window.scrollTo(0, 0)); await p.waitForTimeout(800);
    const txt = await p.evaluate(() => document.body.innerText).catch(e => 'ERR ' + e);
    fs.writeFileSync(`${OUT}/text/${name}.txt`, `URL ${url}\nTITLE ${await p.title()}\nHEIGHT ${h}\n\n` + txt);
    await p.screenshot({ path: `${OUT}/shots/${name}.png`, fullPage: true }).catch(e => console.log(name, 'shot', String(e).slice(0, 80)));
    console.log(name, 'ok height', h, 'chars', txt.length);
    await ctx.close();
  }
  await b.close();
})();
