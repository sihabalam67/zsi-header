// camera: push in on whoever is talking
let CAMPREV=null;
function camera(t){
  let line=null, prev=null; for(const sc of TL.scenes) for(const l of sc.lines){ if(t>=l.start-.15) { prev=line; line=l; } }
  const tgt=l=>(l&&l.who!=='P'&&POS[l.who]!==undefined)?[POS[l.who],1.12]:[960,1.0];
  if(!line) return [960,1];
  const [x1,z1]=tgt(line), [x0,z0]=tgt(prev), k=eio(seg(t,line.start-.15,line.start+.5));
  return [lerp(x0,x1,k), lerp(z0,z1,k)];
}
function frame(t){
  const s=scene(t), L=s.lines.map(l=>l.start); OV='';
  for(const k in POS) delete POS[k];
  let world=(SCN[s.id]||(()=>''))(t,s,L);
  const [cx,z]=camera(t), push=1+.03*seg(t,s.start,s.end);
  const zz=z*push, tx=960-(cx*zz-(cx-960)*0)-(960-cx)*0; // keep the speaker near center
  const ox=Math.max(Math.min(960-cx*zz+ (cx-960)*0, 0), W-W*zz), oy=(H-H*zz)*0.62;
  let g=`<g transform="translate(${f(Math.min(0,Math.max(W-W*zz, 960-cx*zz)))} ${f(oy)}) scale(${f(zz)})">${world}</g>`+OV;
  const k=seg(t,s.start,s.start+.4); if(k<1&&s.start>0) g+=`<rect width="${W}" height="${H}" fill="#1E293B" opacity="${f(1-k)}"/>`;
  g+=captions(t);
  document.getElementById('root').innerHTML=g;
}
window.setup=(tl,dca,N)=>{ TL=tl; TL.N=N; };
window.frame=frame;
</script></body></html>
