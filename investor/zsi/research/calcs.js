const { chromium } = require('playwright'); const fs=require('fs'); const OUT=process.argv[2];
(async()=>{
 const b=await chromium.launch();
 for(const name of ['saas','goldenmark','zsipay','misc']){
   const p=await b.newPage({viewport:{width:1440,height:900}});
   await p.goto(`https://moosa-proposal-calculator.vercel.app/${name}/index.html`,{waitUntil:'networkidle'}); await p.waitForTimeout(2500);
   const t=await p.evaluate(()=>document.body.innerText); const h=await p.evaluate(()=>document.body.scrollHeight);
   fs.writeFileSync(`${OUT}/text/calc_${name}.txt`,t); await p.screenshot({path:`${OUT}/shots/calc_${name}.png`,fullPage:true});
   console.log(name,t.length,'h',h); await p.close();
 }
 // overview: expand the scroll section for a full screenshot
 const p=await b.newPage({viewport:{width:1440,height:900}});
 await p.goto('https://moosa-proposal-calculator.vercel.app/#overview',{waitUntil:'networkidle'}); await p.waitForTimeout(2500);
 const h=await p.evaluate(()=>document.querySelector('section.view').scrollHeight);
 await p.setViewportSize({width:1440,height:h+200}); await p.waitForTimeout(1200);
 await p.screenshot({path:`${OUT}/shots/calc_overview.png`,fullPage:true}); console.log('overview h',h);
 await b.close();})();
