// node rec.js stills <out_dir> t1 t2 ...   |   node rec.js video <out.mp4> [fps]
const { chromium } = require('playwright'); const path=require('path'); const { spawn }=require('child_process');
(async()=>{
 const [mode,out,...rest]=process.argv.slice(2);
 const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1920,height:1080}});
 await p.goto('file://'+path.resolve(__dirname,'demo.html')); await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(800);
 // preload images
 await p.evaluate(async()=>{for(const t of [1,6,9]){window.frame(t);} await new Promise(r=>setTimeout(r,800));});
 if(mode==='stills'){ for(const t of rest){ await p.evaluate(t=>window.frame(t),+t); await p.waitForTimeout(60); await p.screenshot({path:`${out}/s_${t}.jpg`,type:'jpeg',quality:80}); } }
 else { const fps=+(rest[0]||30); const total=await p.evaluate(()=>window.TOTAL); const n=Math.round(total*fps);
   const ff=spawn('ffmpeg',['-y','-loglevel','error','-f','image2pipe','-framerate',String(fps),'-i','-','-c:v','libx264','-pix_fmt','yuv420p','-crf','18',out],{stdio:['pipe','inherit','inherit']});
   for(let i=0;i<n;i++){ await p.evaluate(t=>window.frame(t),i/fps); const buf=await p.screenshot({type:'jpeg',quality:90}); if(!ff.stdin.write(buf)) await new Promise(r=>ff.stdin.once('drain',r)); }
   ff.stdin.end(); await new Promise(r=>ff.on('close',r)); console.log('frames',n); }
 await b.close();})();
