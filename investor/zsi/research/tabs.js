const { chromium } = require('playwright'); const fs=require('fs'); const OUT=process.argv[2];
(async()=>{
 const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1440,height:900}});
 await p.goto('https://moosa-proposal-calculator.vercel.app/#overview',{waitUntil:'networkidle'}); await p.waitForTimeout(2000);
 // find scroll container
 const sc=await p.evaluate(()=>{const els=[...document.querySelectorAll('*')].filter(e=>{const s=getComputedStyle(e);return /(auto|scroll)/.test(s.overflowY)&&e.scrollHeight>e.clientHeight+50});return els.map(e=>e.tagName+'.'+e.className.toString().slice(0,60)+' '+e.scrollHeight)});
 console.log('scrollers',sc);
 for(const [name,label] of [['saas','SaaS Platforms'],['goldenmark','GoldenMark Money'],['zsipay','ZSI PAY'],['misc','Miscellaneous']]){
   await p.getByText(label,{exact:true}).first().click(); await p.waitForTimeout(1500);
   const t=await p.evaluate(()=>document.body.innerText); fs.writeFileSync(`${OUT}/text/calc_${name}.txt`,t);
   console.log(name,t.length, 'hash',await p.evaluate(()=>location.hash));
 }
 await b.close();})();
