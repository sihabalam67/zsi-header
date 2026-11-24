// ---------------------------------------------------------------- helpers ---
function scene(t){ let cur=TL.scenes[0]; for(const s of TL.scenes) if(t>=s.start) cur=s; return cur; }
function talkOf(t,who){ // mouth openness for a character if it's their line
  const fr=Math.min(TL.mouth.length-1,Math.round(t*TL.fps));
  for(const s of TL.scenes) for(const l of s.lines) if(l.who===who && t>=l.start && t<=l.start+l.dur) return TL.mouth[fr];
  return 0;
}
const blinkAt=(t,ph=0)=>((t+ph)%3.7)<.12;
function sky(t,stormK=0,night=0){
  const top=mixc('#9ED8FF','#4A5568',stormK), bot=mixc('#FFF1DC','#A0AEC0',stormK);
  let g=`<defs><linearGradient id="skyg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${top}"/><stop offset="1" stop-color="${bot}"/></linearGradient></defs><rect width="${W}" height="${H}" fill="url(#skyg)"/>`;
  if(stormK<.6) g+=`<circle cx="1640" cy="170" r="90" fill="#FFE58A" opacity="${f(1-stormK*1.6)}"/><circle cx="1640" cy="170" r="140" fill="#FFE58A" opacity="${f(.25*(1-stormK*1.6))}"/>`;
  for(let i=0;i<4;i++){const cx=((i*520+t*14)%(W+400))-200, cy=120+i*45; g+=`<g opacity="${f(.85*(1-stormK))}"><ellipse cx="${f(cx)}" cy="${cy}" rx="110" ry="38" fill="#fff"/><ellipse cx="${f(cx+60)}" cy="${cy-20}" rx="70" ry="34" fill="#fff"/></g>`;}
  return g;
}
function mixc(a,b,k){k=clamp(k);const p=s=>[1,3,5].map(i=>parseInt(s.slice(i,i+2),16));const A=p(a),B=p(b);return '#'+A.map((v,i)=>Math.round(v+(B[i]-v)*k).toString(16).padStart(2,'0')).join('');}
function ground(stormK=0){
  return `<rect y="${GY}" width="${W}" height="${H-GY}" fill="${mixc('#7CC46A','#5E7F57',stormK)}"/><rect y="${GY}" width="${W}" height="14" fill="${mixc('#5DA84B','#4A6A44',stormK)}"/>`+
    Array.from({length:14},(_,i)=>`<path d="M${i*140+30} ${GY+60+(i%3)*40} q8 -22 16 0 q8 -18 16 0" stroke="#4E9A3E" stroke-width="5" fill="none"/>`).join('');
}
function house(x,y,s=1){
  return `<g transform="translate(${x} ${y}) scale(${s})" filter="url(#sh)"><rect x="-200" y="-300" width="400" height="300" fill="#F9E3C3" stroke="${INK}" stroke-width="6"/><path d="M-240 -290 L0 -470 L240 -290Z" fill="#C2410C" stroke="${INK}" stroke-width="6" stroke-linejoin="round"/>`+
    `<rect x="-50" y="-170" width="100" height="170" rx="8" fill="#7C2D12" stroke="${INK}" stroke-width="6"/><circle cx="30" cy="-85" r="8" fill="#FDE047"/>`+
    `<rect x="-160" y="-240" width="90" height="80" fill="#BFE7FF" stroke="${INK}" stroke-width="6"/><rect x="70" y="-240" width="90" height="80" fill="#BFE7FF" stroke="${INK}" stroke-width="6"/></g>`;
}
function fence(){ let g=''; for(let x=0;x<W;x+=70) g+=`<rect x="${x+10}" y="${GY-110}" width="44" height="118" rx="6" fill="#FFF7ED" stroke="${INK}" stroke-width="4"/>`; return `<g opacity=".9">${g}<rect x="0" y="${GY-80}" width="${W}" height="16" fill="#FFF7ED" stroke="${INK}" stroke-width="4"/></g>`; }
// big year badge (springs in when the year changes)
function yearBadge(t,year,since){
  const k=pop(t,since,.5);
  return `<g transform="translate(160 120) scale(${f(k)}) rotate(-4)" filter="url(#sh)"><rect x="-130" y="-62" width="260" height="124" rx="22" fill="#1E293B" stroke="#FDE047" stroke-width="8"/><text x="0" y="32" text-anchor="middle" font-size="86" fill="#FDE047" font-family="A" style="font-family:A">${year}</text></g>`;
}
function hud(t,label,val,k=1,col='#16A34A'){
  if(k<=0) return '';
  return `<g transform="translate(1600 110) scale(${f(k)})" filter="url(#sh)"><rect x="-260" y="-70" width="520" height="140" rx="26" fill="#fff" stroke="${INK}" stroke-width="6"/>`+
    `<text x="0" y="-18" text-anchor="middle" font-size="34" fill="#475569" style="font-weight:700">${label}</text><text x="0" y="48" text-anchor="middle" font-size="68" fill="${col}">${val}</text></g>`;
}
function bigNum(x,y,text,size,col,k,rot=0){
  if(k<=0) return '';
  return `<g transform="translate(${f(x)} ${f(y)}) rotate(${rot}) scale(${f(k)})"><text text-anchor="middle" font-size="${size}" fill="${col}" class="cap" style="stroke-width:${size*.15}px">${text}</text></g>`;
}
function card(x,y,w,h,k){ return `<rect x="${f(x-w/2)}" y="${f(y-h/2)}" width="${w}" height="${h}" rx="30" fill="#fff" stroke="${INK}" stroke-width="6" filter="url(#sh)" transform="translate(${f(x*(1-k))} ${f(y*(1-k))}) scale(${f(k)})" />`; }
function label(x,y,text,size,col='#fff',bg='#1E293B',k=1,rot=0){
  if(k<=0) return ''; MC0.font=`900 ${size}px P`; const w=MC0.measureText(text).width+size*.9;
  return `<g transform="translate(${f(x)} ${f(y)}) rotate(${rot}) scale(${f(k)})" filter="url(#sh)"><rect x="${f(-w/2)}" y="${f(-size*.85)}" width="${f(w)}" height="${f(size*1.5)}" rx="${f(size*.4)}" fill="${bg}"/><text x="0" y="${f(size*.32)}" text-anchor="middle" font-size="${size}" fill="${col}">${text}</text></g>`;
}
function confetti(t,t0,n=60){ const k=t-t0; if(k<0||k>3.2) return ''; let g='';
  for(let i=0;i<n;i++){const x=W/2+(rand(i,1)-.5)*1600*Math.min(1,k*2), y=-40+k*380*(.6+rand(i,2))+Math.sin(k*5+i)*20, c=['#F43F5E','#FDE047','#22C55E','#3B82F6','#F97316'][i%5];
    g+=`<rect x="${f(x)}" y="${f(y)}" width="18" height="10" fill="${c}" transform="rotate(${f(k*300+i*40)} ${f(x)} ${f(y)})"/>`;} return g; }
function leavesFalling(t,t0,dur,x0,y0,n=24){ const k=t-t0; if(k<0||k>dur) return ''; let g='';
  for(let i=0;i<n;i++){const st=rand(i,7)*dur*.6, kk=k-st; if(kk<0) continue; const x=x0+(rand(i,3)-.3)*500+kk*260, y=y0+(rand(i,4)-.5)*200+kk*kk*120+kk*60;
    if(y>GY+40) continue; g+=`<ellipse cx="${f(x)}" cy="${f(y)}" rx="18" ry="10" fill="${i%3?'#2E9E4F':'#FFD23F'}" stroke="${INK}" stroke-width="3" transform="rotate(${f(kk*400+i*30)} ${f(x)} ${f(y)})"/>`;} return g; }
function captions(t){
  let line=null; for(const s of TL.scenes) for(const l of s.lines) if(t>=l.start-.05 && t<=l.start+l.dur+.25) line=l;
  if(!line||!line.words.length) return '';
  const ws=line.words; let i=0; for(let k=0;k<ws.length;k++) if(t>=ws[k].s-.05) i=k;
  const c0=Math.floor(i/6)*6, chunk=ws.slice(c0,c0+6), size=54; MC0.font=`900 ${size}px P`;
  const wd=chunk.map(w=>MC0.measureText(w.w.toUpperCase()).width+size*.36), tot=wd.reduce((a,b)=>a+b,0);
  let x=W/2-tot/2, g=`<rect y="880" width="${W}" height="200" fill="url(#capfade)"/>`;
  chunk.forEach((w,k)=>{ const cx=x+wd[k]/2; x+=wd[k]; if(t<w.s-.05) return; const on=c0+k===i;
    g+=`<text x="${f(cx)}" y="1030" text-anchor="middle" font-size="${size}" fill="${on?'#FFD21F':'#fff'}" class="cap">${w.w.toUpperCase()}</text>`; });
  return g;
}
// tree value keyframes [time, value]; built once from the timeline
let TREEK=[];
function treeVal(t){ let v=TREEK[0][1]; for(let i=1;i<TREEK.length;i++){ const [t0,v0]=TREEK[i-1],[t1,v1]=TREEK[i]; if(t>=t1) v=v1; else if(t>t0){ v=v0+(v1-v0)*eio((t-t0)/(t1-t0)); break; } } return v; }

