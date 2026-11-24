// ------------------------------------------------------------ story #2 scenes ---
let OV='';               // overlay layer (not affected by the camera)
const ov=s=>{OV+=s;};
const POS={};            // per-scene speaker x positions for the camera
function rain(t,k=1,n=70){ if(k<=0) return ''; let g=''; for(let i=0;i<n*k;i++){const x=((i*131+t*300)%2100)-90, y=((i*71+t*1500)%1200)-60; g+=`<line x1="${f(x)}" y1="${f(y)}" x2="${f(x-10)}" y2="${f(y+44)}" stroke="#BFDBFE" stroke-width="4" opacity=".55" stroke-linecap="round"/>`;} return g; }
function nightSky(){ return `<defs><linearGradient id="ng" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0B1026"/><stop offset="1" stop-color="#27304F"/></linearGradient></defs><rect width="${W}" height="${H}" fill="url(#ng)"/><circle cx="1650" cy="160" r="60" fill="#E2E8F0" opacity=".25"/>`; }
function street(){ return `<rect y="${GY}" width="${W}" height="${H-GY}" fill="#1E293B"/><rect y="${GY}" width="${W}" height="10" fill="#334155"/>`+Array.from({length:8},(_,i)=>`<ellipse cx="${i*260+80}" cy="${GY+90}" rx="90" ry="10" fill="#64748B" opacity=".35"/>`).join(''); }
function office(){ let g=`<rect width="${W}" height="${H}" fill="#E8EEF6"/><rect y="${GY}" width="${W}" height="${H-GY}" fill="#94A3B8"/><rect y="${GY}" width="${W}" height="12" fill="#64748B"/>`;
  g+=`<rect x="120" y="140" width="520" height="320" rx="12" fill="#BAE6FD" stroke="${INK}" stroke-width="6"/><path d="M380 140 L380 460 M120 300 L640 300" stroke="${INK}" stroke-width="5"/>`;
  g+=`<rect x="1300" y="160" width="360" height="200" rx="10" fill="#fff" stroke="${INK}" stroke-width="5"/><text x="1480" y="250" text-anchor="middle" font-size="40" fill="#2563EB">BLUEBIRD</text><text x="1480" y="300" text-anchor="middle" font-size="30" fill="#64748B" style="font-weight:700">LOGISTICS</text>`;
  return g; }
function desk(x){ return `<rect x="${x-260}" y="${GY-170}" width="520" height="40" rx="8" fill="#B45309" stroke="${INK}" stroke-width="6"/><rect x="${x-240}" y="${GY-130}" width="24" height="130" fill="#78350F"/><rect x="${x+216}" y="${GY-130}" width="24" height="130" fill="#78350F"/><rect x="${x-90}" y="${GY-300}" width="180" height="120" rx="10" fill="#1E293B" stroke="${INK}" stroke-width="5"/><rect x="${x-14}" y="${GY-180}" width="28" height="14" fill="#1E293B"/>`; }
function apartment(){ return `<rect width="${W}" height="${H}" fill="#FDE7C7"/><rect y="${GY}" width="${W}" height="${H-GY}" fill="#B98B5E"/><rect y="${GY}" width="${W}" height="12" fill="#8B6340"/><rect x="1500" y="180" width="300" height="260" rx="10" fill="#1E3A8A" stroke="${INK}" stroke-width="6"/><circle cx="1650" cy="300" r="40" fill="#E2E8F0" opacity=".5"/>`; }
function park(){ return sky(0)+`<rect y="${GY}" width="${W}" height="${H-GY}" fill="#475569"/>`+Array.from({length:6},(_,i)=>`<rect x="${i*340+60}" y="${GY+60}" width="160" height="12" fill="#F8FAFC"/>`).join(''); }
function bigReveal(x,y,text,size,col,k){ return bigNum(x,y,text,size,col,k); }
function heart(x,y,s,k=1){ if(k<=0) return ''; return `<g transform="translate(${f(x)} ${f(y)}) scale(${f(s*k)})"><path d="M0 30 C-60 -10 -40 -60 0 -30 C40 -60 60 -10 0 30Z" fill="#F43F5E" stroke="${INK}" stroke-width="4"/></g>`; }
function cloudOver(x,y,t){ return `<g transform="translate(${f(x)} ${f(y+Math.sin(t*3)*6)})"><circle cx="-50" cy="0" r="45" fill="#64748B"/><circle cx="10" cy="-20" r="55" fill="#64748B"/><circle cx="60" cy="0" r="42" fill="#64748B"/>${[0,1,2,3].map(i=>`<line x1="${-50+i*35}" y1="${45+((t*300+i*30)%60)}" x2="${-56+i*35}" y2="${70+((t*300+i*30)%60)}" stroke="#93C5FD" stroke-width="5"/>`).join('')}</g>`; }
function chart401(t,t0,pts,x0,y0,w,h,maxV,k,col='#16A34A'){ // pts: [[u 0..1, value]], drawn up to progress k
  const n=Math.max(2,Math.ceil(pts.length*k)), sub=pts.slice(0,n);
  let g=`<rect x="${x0-40}" y="${y0-h-60}" width="${w+80}" height="${h+110}" rx="24" fill="#fff" stroke="${INK}" stroke-width="6" filter="url(#sh)"/><line x1="${x0}" y1="${y0}" x2="${x0+w}" y2="${y0}" stroke="${INK}" stroke-width="5"/>`;
  g+=`<path d="M${sub.map(p=>f(x0+p[0]*w)+' '+f(y0-p[1]/maxV*h)).join(' L')}" stroke="${col}" stroke-width="12" fill="none" stroke-linejoin="round" stroke-linecap="round"/>`;
  const l=sub[sub.length-1]; g+=`<circle cx="${f(x0+l[0]*w)}" cy="${f(y0-l[1]/maxV*h)}" r="16" fill="${col}" stroke="#fff" stroke-width="5"/>`;
  return g; }
