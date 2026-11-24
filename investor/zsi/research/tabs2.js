const { chromium } = require('playwright'); const fs=require('fs'); const OUT=process.argv[2];
(async()=>{
 const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1440,height:900}});
 for(const name of ['saas','goldenmark','zsipay','misc']){
   await p.goto('https://moosa-proposal-calculator.vercel.app/#'+name,{waitUntil:'networkidle'}); await p.waitForTimeout(3000);
   const fr=p.frames(); let all='';
   for(const f of fr){ const t=await f.evaluate(()=>document.body?document.body.innerText:'').catch(()=>'' ); all+=`\n--- FRAME ${f.url()}\n`+t; }
   fs.writeFileSync(`${OUT}/text/calc_${name}.txt`,all); console.log(name,'frames',fr.length,'chars',all.length, fr.map(f=>f.url()).join(' '));
 }
 await b.close();})();
