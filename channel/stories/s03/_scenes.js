// ------------------------------------------------------------ story #3 scenes ---
const SCN={};
function lawOffice(){ return `<rect width="${W}" height="${H}" fill="#EDE4D3"/><rect y="${GY}" width="${W}" height="${H-GY}" fill="#8B6340"/><rect y="${GY}" width="${W}" height="12" fill="#6B4A2E"/>`+
  `<rect x="140" y="150" width="380" height="300" rx="8" fill="#7C2D12" stroke="${INK}" stroke-width="6"/>`+[0,1,2,3].map(i=>`<rect x="160" y="${170+i*70}" width="340" height="12" fill="#B45309"/>${[0,1,2,3,4,5,6].map(j=>`<rect x="${170+j*46}" y="${120+i*70+52}" width="30" height="${40+(j*7)%18}" fill="${['#1E3A8A','#B91C1C','#065F46','#92400E'][(i+j)%4]}"/>`).join('')}`).join('')+
  `<rect x="1420" y="160" width="320" height="200" rx="6" fill="#F8FAFC" stroke="${INK}" stroke-width="5"/><text x="1580" y="240" text-anchor="middle" font-size="34" fill="#334155">KOWALSKI</text><text x="1580" y="290" text-anchor="middle" font-size="26" fill="#64748B" style="font-weight:700">ATTORNEY AT LAW</text>`; }
function bigDesk(x=960){ return `<rect x="${x-380}" y="${GY-200}" width="760" height="50" rx="10" fill="#92400E" stroke="${INK}" stroke-width="6"/><rect x="${x-360}" y="${GY-150}" width="720" height="150" fill="#78350F" stroke="${INK}" stroke-width="6"/>`; }
function vault(){ let g=`<rect width="${W}" height="${H}" fill="#475569"/><rect y="${GY}" width="${W}" height="${H-GY}" fill="#334155"/>`;
  for(let i=0;i<8;i++) for(let j=0;j<5;j++) g+=`<rect x="${40+i*240}" y="${60+j*120}" width="220" height="100" rx="8" fill="#94A3B8" stroke="${INK}" stroke-width="4"/><circle cx="${150+i*240}" cy="${110+j*120}" r="10" fill="#FDE047" stroke="${INK}" stroke-width="3"/>`;
  return g+`<rect y="0" width="${W}" height="${H}" fill="#0F172A" opacity=".35"/>`; }
function kitchen(){ return `<rect width="${W}" height="${H}" fill="#FDE7C7"/><rect y="${GY}" width="${W}" height="${H-GY}" fill="#C08A5B"/><rect y="${GY}" width="${W}" height="12" fill="#8B6340"/>`+
  `<rect x="1300" y="200" width="460" height="40" fill="#92400E" stroke="${INK}" stroke-width="5"/>`; }
function court(){ return `<rect width="${W}" height="${H}" fill="#E7E5E4"/><rect y="${GY}" width="${W}" height="${H-GY}" fill="#78716C"/>`+
  `<rect x="660" y="200" width="600" height="${GY-200}" fill="#78350F" stroke="${INK}" stroke-width="7"/><rect x="700" y="160" width="520" height="60" rx="8" fill="#92400E" stroke="${INK}" stroke-width="6"/>`+
  `<circle cx="960" cy="110" r="60" fill="#FDE047" stroke="${INK}" stroke-width="6"/><text x="960" y="128" text-anchor="middle" font-size="52" fill="#78350F">⚖</text>`; }
function sepia(k){ return k>0?`<rect width="${W}" height="${H}" fill="#C08A5B" opacity="${f(.28*k)}" style="mix-blend-mode:multiply"/><rect width="${W}" height="${H}" fill="url(#capfade)" opacity="${f(.3*k)}"/>`:''; }
function storm_jar(x,y,s=1){ return jar({x,y,s,bills:3,label:'STORM JAR'}); }
function judge(x,y,t,o={}){ return CAST.kowalski(Object.assign({x,y,t,h:520,hair:'#E5E7EB',shirt:'#111827',pants:'#111827',hairStyle:'curly',mood:'happy'},o)); }

SCN.open=(t,s,L)=>{
  Object.assign(POS,{K:960,D:560,L:1380});
  let g=lawOffice()+bigDesk(960);
  g+=CAST.kowalski({x:960,y:GY-150,t,talk:talkOf(t,'K'),mood:'happy'});
  g+=CAST.derek({x:560,y:GY,t,talk:talkOf(t,'D'),mood:t>L[2]?'shocked':'happy',act:t>L[2]&&t<L[3]+.4?'shock':undefined,actT:L[2],look:[1,0]});
  g+=CAST.lily({x:1380,y:GY,t,talk:talkOf(t,'L'),mood:t>L[2]&&t<L[7]?'shocked':'happy',look:[-1,0]});
  g+=`<rect x="900" y="${GY-215}" width="120" height="16" fill="#fff" stroke="${INK}" stroke-width="3"/>`;
  if(t>=L[2]&&t<L[5]){ ov(bigNum(960,220,countUp(t,L[2]+.3,1.6,TL.N.now,v=>'$'+Math.round(v).toLocaleString('en-US')),120,'#FDE047',pop(t,L[2]+.2))+shockwave(t,L[2]+1.9,960,180,520,'#FDE047')); }
  if(t>=L[3]&&t<L[5]) ov(bubble({x:620,y:330,text:'SOUP. EVERY. NIGHT!',size:40,k:pop(t,L[3]+.5)}));
  if(t>=L[4]&&t<L[6]) ov(label(1640,150,'11 SAFETY PINS',46,'#fff','#475569',pop(t,L[4]+1.4)));
  if(t>=L[5]&&t<L[6]){ const k=pop(t,L[5]); ov(`<g transform="translate(1500 470) scale(${f(k)})"><circle r="240" fill="#FEF3C7" stroke="${INK}" stroke-width="8" filter="url(#sh)"/><clipPath id="cw"><circle r="235"/></clipPath><g clip-path="url(#cw)">${CAST.walter({x:0,y:560,h:720,t,mood:'happy',act:'think'})}</g></g>`+label(1500,770,'WALTER · SCHOOL JANITOR',38,'#fff','#7C5A3A',k)); }
  if(t>=L[6]&&t<L[7]) ov(bigNum(960,250,'HOW?',150,'#E11D48',pop(t,L[6]+.6)));
  if(t>=L[7]&&t<L[9]){ const p=eo(seg(t,L[7]+.3,L[7]+2.2)); g+=`<g transform="translate(${f(lerp(960,1260,p))} ${GY-212}) rotate(${f(p*90)})"><circle r="16" fill="none" stroke="#FDE047" stroke-width="7"/><rect x="10" y="-5" width="60" height="10" fill="#FDE047"/><rect x="50" y="5" width="8" height="14" fill="#FDE047"/></g>`;
    if(t>L[8]) ov(label(1260,150,'"HE LEFT YOU SOMETHING ELSE."',38,INK,'#FDE047',pop(t,L[8]+.8))); }
  if(t>=L[9]){ const k=pop(t,L[9],.5); ov(`<rect width="${W}" height="${H}" fill="#FFF1DC" opacity="${f(.9*Math.min(1,k))}"/>`+penny({x:960,y:800,r:180,t,mouth:TL.mouth[Math.round(t*30)]||0,blink:blinkAt(t),armL:150,armR:-40,sx:k,sy:k})+label(960,230,'MADE-UP PEOPLE',46,'#fff','#334155',pop(t,L[9]+1))+label(960,330,'REAL NUMBERS',58,'#14532D','#86EFAC',pop(t,L[9]+2)));
    if(t>L[9]+3.4) ov(`<rect width="${W}" height="${H}" fill="#1E293B" opacity="${f(.9*seg(t,L[9]+3.4,L[9]+3.8))}"/>`+label(960,540,'ONE WEEK EARLIER',80,'#FDE047','#1E293B',pop(t,L[9]+3.6))); }
  return g;
};
SCN.lily=(t,s,L)=>{
  let g='';
  if(t<L[4]||(t>=L[11]&&t<L[12])){ Object.assign(POS,{L:800});
    g+=kitchen();
    g+=CAST.lily({x:800,y:GY,t,talk:talkOf(t,'L'),mood:t<L[2]?'worried':'happy',look:[1,0],holdR:t>=L[2]&&t<L[4]?soup({x:40,y:0,s:.6,t}):''});
    if(t<L[2]) [0,1,2].forEach(i=>{ const k=pop(t,L[0]+1.5+i*.4); if(k>0) ov(`<g transform="translate(${1250+i*180} ${400+Math.sin(t*1.5+i)*8}) rotate(${(i-1)*8}) scale(${f(k)})" filter="url(#sh)"><rect x="-80" y="-50" width="160" height="100" rx="12" fill="${['#E11D48','#7C3AED','#0EA5E9'][i]}" stroke="${INK}" stroke-width="5"/><rect x="-60" y="-28" width="36" height="26" rx="4" fill="#FDE047"/><text x="0" y="35" text-anchor="middle" font-size="24" fill="#fff">MAXED</text><path d="M-60 -60 l14 -22 l14 22 M30 -60 l14 -22 l14 22" fill="#E11D48" stroke="${INK}" stroke-width="3"/></g>`); });
    if(t>=L[0]&&t<L[2]) ov(label(800,150,'RENT DUE',52,'#fff','#E11D48',pop(t,L[0]+.8)));
    if(t>=L[11]) ov(`<rect width="${W}" height="${H}" fill="#0F172A" opacity="${f(.6*seg(t,L[11],L[11]+.5))}"/>`+door({x:1400,y:GY,s:.9})+label(1400,200,'NO ANSWER',54,'#fff','#334155',pop(t,L[11]+1.2)));
  } else if(t<L[12]){ Object.assign(POS,{W:760,L:1240});
    g+=kitchen()+storm_jar(1550,GY-200,.55*(t>L[8]?pop(t,L[8]):0));
    g+=CAST.walter({x:760,y:GY,t,talk:talkOf(t,'W'),mood:t>L[6]&&t<L[8]?'laugh':'happy',look:[1,0],holdR:soup({x:40,y:0,s:.6,t})});
    g+=CAST.lily({x:1240,y:GY,t,talk:talkOf(t,'L'),mood:t>L[7]&&t<L[8]?'laugh':'happy',look:[-1,0],holdR:soup({x:40,y:0,s:.6,t})});
    g+=sepia(1); ov(label(300,110,'FLASHBACK',44,'#fff','#7C5A3A',pop(t,L[4])));
    if(t>=L[8]) ov(label(1550,280,'STORM JAR',40,'#fff','#334155',pop(t,L[8]+.6)));
  } else { Object.assign(POS,{K:960,D:520,L:1380});
    g+=lawOffice()+bigDesk(960)+CAST.kowalski({x:960,y:GY-150,t,talk:talkOf(t,'K'),mood:'happy'});
    const dx=lerp(-300,520,eo(seg(t,L[12],L[12]+1.4)));
    g+=CAST.derek({x:dx,y:GY,t,talk:talkOf(t,'D'),mood:'happy',act:t<L[12]+1.4?'walk':(t>L[14]&&t<L[16]?'point':undefined),look:[1,0],holdR:t>L[14]&&t<L[16]?`<g><ellipse cx="20" cy="-10" rx="44" ry="28" fill="#D97706" stroke="${INK}" stroke-width="4"/><circle cx="5" cy="-30" r="14" fill="#E11D48"/><circle cx="30" cy="-34" r="12" fill="#84CC16"/></g>`:''});
    g+=CAST.lily({x:1380,y:GY,t,talk:talkOf(t,'L'),mood:t>L[17]?'worried':'happy',look:[-1,0]});
    if(t>=L[12]&&t<L[13]) ov(label(500,150,'BANG!',80,'#fff','#E11D48',pop(t,L[12]+.2),-6));
    if(t>=L[14]&&t<L[16]) ov(label(1380,150,'VISITS: 1 (2011)',44,'#fff','#334155',pop(t,L[14]+.5)));
    if(t>=L[18]){ const k=pop(t,L[18]+.3); ov(`<g transform="translate(960 420) scale(${f(k*2.2)})" filter="url(#sh)"><circle r="40" fill="none" stroke="#FDE047" stroke-width="16"/><rect x="30" y="-12" width="150" height="24" fill="#FDE047" stroke="${INK}" stroke-width="3"/><rect x="140" y="12" width="16" height="30" fill="#FDE047"/></g>`+label(960,620,'BOX 467',70,INK,'#FDE047',pop(t,L[18]+1.4)));
      if(t>=L[19]) ov(label(960,150,'WHAT IS INSIDE?',60,'#fff','#1E293B',pop(t,L[19]+.4))); }
  }
  return g;
};
SCN.box=(t,s,L)=>{
  Object.assign(POS,{D:420,K:1500,L:1180});
  let g=vault();
  // loot-reveal: charge (shake + light leaks) -> burst -> lid opens
  const charge=seg(t,L[2]+.5,L[3]), burst=seg(t,L[3],L[3]+.6), open=eo(seg(t,L[3],L[3]+1));
  const sh=charge>0&&charge<1?Math.sin(t*40)*charge*4:0;
  g+=`<g transform="translate(${f(sh)} 0)">`+safebox({x:820,y:GY-20,s:1.1,open,glow:Math.max(charge*.4,burst>0?1-burst*.3:0),t})+'</g>';
  if(burst>0&&burst<1) g+=shockwave(t,L[3],820,GY-260,600,'#FDE047');
  g+=CAST.derek({x:420,y:GY,t,talk:talkOf(t,'D'),mood:t>L[3]&&t<L[4]?'shocked':'happy',look:[1,0]});
  g+=CAST.lily({x:1180,y:GY,t,talk:talkOf(t,'L'),mood:t>L[7]&&t<L[11]?'shocked':'happy',look:[-1,0]});
  g+=CAST.kowalski({x:1500,y:GY,t,talk:talkOf(t,'K'),mood:'happy',look:[-1,0]});
  const items=[[L[4],'notebook'],[L[5],'news'],[L[6],'env'],[L[7],'card']];
  items.forEach(([st,k],i)=>{ const p=pop(t,st+.3); if(p<=0||t>=L[15]) return; const x=420+i*360, y=330;
    if(k==='notebook') ov(`<g transform="translate(${x} ${y}) rotate(-6) scale(${f(p)})" filter="url(#sh)"><rect x="-120" y="-150" width="240" height="300" rx="10" fill="#1E3A8A" stroke="${INK}" stroke-width="6"/><rect x="-90" y="-100" width="180" height="70" fill="#FEF3C7"/><text x="0" y="-55" text-anchor="middle" font-size="26" fill="${INK}">WALTER'S RULES</text></g>`);
    if(k==='news') ov(newspaper({x,y,s:.38*p,rot:4}));
    if(k==='env') ov(envelopes({x,y:y+100,s:.55*p,n:14}));
    if(k==='card') ov(card({x,y,s:.6*p,rot:-5})); });
  if(t>=L[8]&&t<L[9]) ov(label(1500,150,'"LILY"',60,'#9D174D','#FBCFE8',pop(t,L[8]+.2)));
  if(t>=L[11]&&t<L[15]){ const k=pop(t,L[11]); ov(`<rect width="${W}" height="${H}" fill="#0F172A" opacity="${f(.55*Math.min(1,k))}"/><g transform="translate(960 470) scale(${f(k)})" filter="url(#sh)"><rect x="-520" y="-260" width="1040" height="520" rx="12" fill="#FEF9C3" stroke="${INK}" stroke-width="6"/>`+
    `<text x="-460" y="-160" font-size="42" fill="#92400E" style="font-weight:700">WALTER'S RULES · page 0</text><text x="-460" y="-40" font-size="50" fill="${INK}">Read the envelopes first.</text><text x="-460" y="50" font-size="50" fill="${INK}">The card goes last.</text><text x="-460" y="160" font-size="50" fill="#16A34A">Patience, kid. That's the whole trick.</text></g>`); }
  if(t>=L[15]) ov(label(960,170,'THE ANSWER TO $2 MILLION IS IN THIS BOX',48,'#fff','#1E293B',pop(t,L[15]+.3)));
  return g;
};
SCN.envelopes=(t,s,L)=>{
  Object.assign(POS,{L:620,K:1500,D:1500});
  let g=kitchen();
  const n=Math.round(467*eio(seg(t,L[1],L[3]+2)));
  g+=envelopes({x:1060,y:GY-40,s:.9,n:Math.min(46,Math.ceil(n/10.2))});
  g+=CAST.lily({x:620,y:GY,t,talk:talkOf(t,'L'),mood:t>L[3]&&t<L[6]?'laugh':'happy',act:t>L[4]&&t<L[5]?'cheer':undefined,look:[1,0]});
  g+=t<L[8]||t>=L[13]?CAST.kowalski({x:1500,y:GY,t,talk:talkOf(t,'K'),mood:'happy',look:[-1,0]}):CAST.derek({x:1500,y:GY,t,talk:talkOf(t,'D'),mood:t>L[12]?'happy':'shocked',look:[-1,0]});
  if(t>=L[0]&&t<L[6]) ov(label(1060,150,`ENVELOPES: ${n}`,58,'#fff','#B45309',1));
  if(t>=L[0]&&t<L[2]) ov(label(620,260,'$300',70,'#fff','#16A34A',pop(t,L[0]+1.5)));
  if(t>=L[2]&&t<L[3]){ const k=pop(t,L[2]+.3); let gg=`<g transform="translate(1060 380) scale(${f(k)})" filter="url(#sh)"><rect x="-260" y="-130" width="520" height="260" rx="24" fill="#fff" stroke="${INK}" stroke-width="5"/>`;
    for(let i=0;i<50;i++) gg+=`<rect x="${-220+(i%10)*44}" y="${-100+Math.floor(i/10)*38}" width="30" height="${22+(i*7)%10}" rx="3" fill="${['#60A5FA','#F472B6','#FBBF24','#34D399'][i%4]}"/>`;
    ov(gg+`<text x="0" y="110" text-anchor="middle" font-size="28" fill="${INK}">500 BIGGEST US COMPANIES</text></g>`); }
  if(t>=L[3]&&t<L[6]) ov(bigNum(1060,300,'467',150,'#FDE047',pop(t,L[3]+.3)));
  if(t>=L[6]&&t<L[8]){ const k=pop(t,L[6]+.3); ov(`<rect width="${W}" height="${H}" fill="#0F172A" opacity="${f(.55*Math.min(1,k))}"/><g transform="translate(960 450) rotate(-3) scale(${f(k)})" filter="url(#sh)"><rect x="-460" y="-200" width="920" height="400" rx="10" fill="#FEF3C7" stroke="${INK}" stroke-width="6"/><text x="0" y="-110" text-anchor="middle" font-size="40" fill="#92400E" style="font-weight:700">ENVELOPE #93 · 1995</text>`+
    `<text x="0" y="-10" text-anchor="middle" font-size="46" fill="${INK}">Car died on the highway today.</text><text x="0" y="70" text-anchor="middle" font-size="46" fill="${INK}">Took the bus home.</text><text x="0" y="150" text-anchor="middle" font-size="46" fill="#16A34A">Envelope still goes in.</text></g>`); }
  if(t>=L[10]&&t<L[14]) ov(bigNum(960,260,countUp(t,L[10]+.3,1.4,TL.N.paid_monthly,v=>'$'+Math.round(v).toLocaleString('en-US')),120,'#FDE047',pop(t,L[10]+.2)));
  if(t>=L[11]&&t<L[14]) ov(label(960,400,'NOT $2,000,000',50,'#fff','#E11D48',pop(t,L[11]+1.2)));
  if(t>=L[14]) ov(label(960,170,'WHERE DID THE REST COME FROM?',54,'#fff','#1E293B',pop(t,L[14]+.4)));
  return g;
};
SCN.crash=(t,s,L)=>{
  Object.assign(POS,{L:1450,W:1450,K:1450,D:1450});
  let g=kitchen();
  // crash-as-earthquake: the newspaper cracks and the screen shakes once
  const q=seg(t,L[1]+.4,L[1]+1.4), qs=q>0&&q<1?Math.sin(t*35)*6*(1-q):0;
  if(t<L[7]) g+=`<g transform="translate(${f(qs)} 0)">`+newspaper({x:700,y:470,s:.85,rot:-3,crack:q})+'</g>';
  if(t>=L[1]&&t<L[4]){ ov(bigNum(700,640,`${TL.N.black_monday}%`,150,'#E11D48',pop(t,L[1]+1.6))+label(700,780,'IN ONE DAY · OCT 19, 1987',40,'#fff','#E11D48',pop(t,L[1]+2.4))); }
  if(t>=L[2]&&t<L[4]) ov(`<g transform="rotate(-4 1100 330)">`+label(1150,300,'"Everybody\'s selling.',38,INK,'#FEF3C7',pop(t,L[3]))+label(1150,370,'The stores are having a sale."',38,INK,'#FEF3C7',pop(t,L[3]+1.6))+'</g>');
  const who=t<L[5]?'W':(t<L[9]?'L':(t<L[12]?'W':(t<L[14]?'L':'D')));
  if(who==='W') g+=sepia(.0)+CAST.walter({x:1450,y:GY,t,talk:talkOf(t,'W'),mood:'happy',look:[-1,0]});
  else if(who==='D') g+=CAST.derek({x:1450,y:GY,t,talk:talkOf(t,'D'),mood:'worried',act:'think',look:[-1,0]});
  else g+=CAST.lily({x:1450,y:GY,t,talk:talkOf(t,'L'),mood:t>L[9]&&t<L[10]?'shocked':'happy',act:t>L[9]&&t<L[10]?'shock':undefined,actT:L[9],look:[-1,0]});
  if(t>=L[7]){ const recs=[['OCT 9, 2002',TL.N.c2002],['MAR 9, 2009',TL.N.c2009],['MAR 23, 2020',TL.N.c2020]];
    g+=storm_jar(380,GY,.6);
    recs.forEach(([d,v],i)=>{ const k=pop(t,L[8]+i*.6); if(k<=0) return; const x=470+i*290, y=380;
      ov(`<g transform="translate(${x} ${y}) rotate(${(i-1)*4}) scale(${f(k)})" filter="url(#sh)"><rect x="-130" y="-150" width="260" height="300" rx="8" fill="#fff" stroke="${INK}" stroke-width="5"/><text x="0" y="-95" text-anchor="middle" font-size="28" fill="#B91C1C">${d}</text><text x="0" y="-30" text-anchor="middle" font-size="46" fill="${INK}">$5,000</text>`+
        (t>=L[12]+(i===2?.0:i*1.6)||t>=L[13]&&i===2?`<text x="0" y="40" text-anchor="middle" font-size="26" fill="#64748B" style="font-weight:700">TODAY</text><text x="0" y="100" text-anchor="middle" font-size="48" fill="#16A34A">${money(v)}</text>`:'')+`</g>`); });
    if(t>=L[10]&&t<L[12]) ov(label(760,640,'"Everyone thinks I\'m crazy. Good."',40,INK,'#FEF3C7',pop(t,L[10]+.6),-3));
    if(t>=L[15]) ov(label(760,150,'$15,000 · STILL NOT $2 MILLION',46,'#fff','#334155',pop(t,L[15]+.3))); }
  if(t>=L[17]){ const k=pop(t,L[17]); ov(`<rect width="${W}" height="${H}" fill="#0F172A" opacity="${f(.75*Math.min(1,k))}"/>`+penny({x:700,y:820,r:170,t,mouth:TL.mouth[Math.round(t*30)]||0,blink:blinkAt(t),armL:150,armR:-30,sx:k,sy:k}));
    const pr=t>L[17]+2.6; ov(`<g transform="translate(1250 470) scale(${f(pop(t,L[17]+.8))})" filter="url(#sh)"><rect x="-260" y="-75" width="520" height="150" rx="75" fill="${pr?'#475569':'#E5202B'}"/><text x="0" y="24" text-anchor="middle" font-size="64" fill="#fff">${pr?'SUBSCRIBED ✓':'SUBSCRIBE'}</text></g>`); }
  return g;
};
SCN.growth=(t,s,L)=>{
  Object.assign(POS,{W:960,L:960,K:960,D:960});
  let g=`<rect width="${W}" height="${H}" fill="#FFF7E6"/>`;
  const pts=[[1988,0],[1996,TL.N.v1996],[2006,TL.N.v2006],[2016,TL.N.v2016],[2026.9,TL.N.now]];
  const x0=180,x1=1300,y0=880,yt=170, px=y=>x0+(y-1988)/(2027-1988)*(x1-x0), py=v=>y0-v/2100000*(y0-yt);
  const reveal=t<L[1]?0:t<L[3]?1:t<L[5]?2:t<L[7]?3:4, kk=reveal<4?1:eio(seg(t,L[7]+.3,L[7]+3));
  let d=`M${px(1988)} ${py(0)}`; for(let i=1;i<=reveal;i++){ const [yr,v]=pts[i], [py0,pv0]=pts[i-1]; const k=i<reveal?1:(i===4?kk:1); const yy=py0+(yr-py0)*k, vv=pv0+(v-pv0)*Math.pow(k,1.6); d+=` Q${f(px((py0+yy)/2))} ${f(py(pv0+(vv-pv0)*.25))} ${f(px(yy))} ${f(py(vv))}`; }
  g+=`<rect x="${x0-60}" y="${yt-40}" width="${x1-x0+120}" height="${y0-yt+110}" rx="24" fill="#fff" stroke="${INK}" stroke-width="6" filter="url(#sh)"/><line x1="${x0}" y1="${y0}" x2="${x1}" y2="${y0}" stroke="${INK}" stroke-width="5"/>`;
  [1988,1996,2006,2016,2026].forEach(y=>g+=`<text x="${f(px(y))}" y="${y0+48}" text-anchor="middle" font-size="30" fill="#475569">${y}</text>`);
  g+=`<path d="${d}" stroke="#16A34A" stroke-width="14" fill="none" stroke-linecap="round"/>`;
  g+=`<text x="${x0}" y="${yt+20}" font-size="40" fill="${INK}">WALTER'S BALANCE, EVERY 10 YEARS</text>`;
  for(let i=1;i<=Math.min(reveal,3);i++){ const [yr,v]=pts[i]; g+=`<circle cx="${f(px(yr))}" cy="${f(py(v))}" r="14" fill="#16A34A" stroke="#fff" stroke-width="4"/>`+label(px(yr),py(v)-50,money(v),36,'#fff','#16A34A',pop(t,[L[1],L[3],L[5]][i-1]+.3)); }
  if(reveal>=4){ g+=label(px(2026),py(TL.N.now*kk)-50,money(TL.N.now*kk),42,'#fff','#16A34A',1); if(t>=L[8]) g+=`<rect x="${f(px(2016))}" y="${yt}" width="${f(px(2026.9)-px(2016))}" height="${y0-yt}" fill="#FDE047" opacity=".25"/>`; }
  if(t>=L[8]&&t<L[11]) ov(bigNum(600,330,`${TL.N.last10_share}% IN THE LAST 10 YEARS`,70,'#E11D48',pop(t,L[8]+.3)));
  const who=t<L[6]?'W':(t<L[10]?'L':(t<L[11]?'K':(t<L[12]?'W':(t<L[13]?'D':'L'))));
  const C={W:CAST.walter,L:CAST.lily,K:CAST.kowalski,D:CAST.derek}[who];
  g+=(who==='W'?'':'')+C({x:1600,y:GY+20,t,talk:talkOf(t,who),mood:who==='D'?'worried':'happy',look:[-1,0]});
  if(t>=L[11]&&t<L[12]){ // snowball rolls and grows
    const p=seg(t,L[11],L[12]); g+=`<circle cx="${f(300+p*900)}" cy="${f(y0-30-p*60)}" r="${f(20+p*120)}" fill="#F8FAFC" stroke="${INK}" stroke-width="5"/>`; }
  if(t>=L[14]){ const dx=lerp(1600,2300,seg(t,L[14]+.5,L[14]+2.5)); g+=CAST.derek({x:dx,y:GY+20,t,act:'walk',mood:'angry'}); ov(label(1620,110,'TO THE COURTHOUSE',54,'#fff','#7E22CE',pop(t,L[14]+.4))); }
  return g;
};
SCN.contest=(t,s,L)=>{
  Object.assign(POS,{K:960,D:520,L:1400});
  let g=lawOffice()+bigDesk(960)+CAST.kowalski({x:960,y:GY-150,t,talk:talkOf(t,'K'),mood:'happy'});
  g+=CAST.derek({x:520,y:GY,t,talk:talkOf(t,'D'),mood:t>L[8]?'laugh':'happy',act:t>L[2]&&t<L[3]?'shake':(t>L[9]&&t<L[10]?'cheer':undefined),look:[1,0]});
  g+=CAST.lily({x:1400,y:GY,t,talk:talkOf(t,'L'),mood:t>L[7]?'worried':'happy',look:[-1,0]});
  if(t>=L[0]&&t<L[2]) ov(`<g transform="translate(960 380) rotate(3) scale(${f(pop(t,L[0]+.4))})" filter="url(#sh)"><rect x="-260" y="-160" width="520" height="320" rx="8" fill="#fff" stroke="${INK}" stroke-width="5"/><text x="0" y="-90" text-anchor="middle" font-size="36" fill="#B91C1C">NOTICE OF CONTEST</text>`+[0,1,2,3].map(i=>`<rect x="-200" y="${-40+i*40}" width="${360-(i%2)*80}" height="12" fill="#CBD5E1"/>`).join('')+`</g>`);
  if(t>=L[6]&&t<L[10]) ov(label(960,160,'HEARING: FRIDAY 9 A.M.',58,'#fff','#E11D48',pop(t,L[6]+.6)));
  if(t>=L[9]&&t<L[10]) ov(`<g transform="translate(560 330) scale(${f(pop(t,L[9]+.6))})" filter="url(#sh)"><path d="M-160 40 L160 40 L120 90 L-120 90Z" fill="#F8FAFC" stroke="${INK}" stroke-width="5"/><path d="M0 40 L0 -110 L100 20Z" fill="#FDE047" stroke="${INK}" stroke-width="5"/><text x="0" y="78" text-anchor="middle" font-size="28" fill="${INK}">THE SOUP</text></g>`);
  if(t>=L[10]){ ov(`<rect width="${W}" height="${H}" fill="#0F172A" opacity="${f(.6*seg(t,L[10],L[10]+.5))}"/>`+label(960,170,'4 DAYS LEFT',70,'#fff','#E11D48',pop(t,L[10]+.3))+card({x:960,y:520,s:1.1*pop(t,L[10]+1.4),rot:-4})); }
  return g;
};
SCN.card=(t,s,L)=>{
  Object.assign(POS,{L:1400,W:1400});
  let g=nightSky()+`<rect y="${GY}" width="${W}" height="${H-GY}" fill="#57534E"/>`+door({x:400,y:GY,s:.9})+`<rect x="250" y="${GY-20}" width="300" height="40" fill="#A8A29E" stroke="${INK}" stroke-width="4"/>`;
  const walterSpeaks=t>=L[1]&&t<L[3]||t>=L[4]&&t<L[5]||t>=L[9]&&t<L[10]||t>=L[13];
  g+=CAST.lily({x:1400,y:GY,t,talk:talkOf(t,'L'),mood:t>L[6]&&t<L[12]?'sad':'happy',tears:t>L[7]&&t<L[12],look:[-1,.4],holdR:card({x:30,y:-20,s:.25})});
  if(walterSpeaks) g+=`<g opacity=".55">${CAST.walter({x:800,y:GY,t,talk:talkOf(t,'W'),mood:'happy',look:[1,0]})}</g>`;
  if(t>=L[0]&&t<L[6]) ov(card({x:900,y:380,s:1.0*pop(t,L[0]+.6),rot:-3}));
  if(t>=L[1]&&t<L[5]) ov(label(900,700,'"Today you were born, right next door."',38,INK,'#FBCFE8',pop(t,L[1]+.4)));
  if(t>=L[2]&&t<L[4]) ov(`<g transform="translate(1180 320) scale(${f(pop(t,L[2]+.5)*1.5)})"><path d="M-40 0 l70 0 a14 14 0 0 1 0 28 l-70 0" stroke="#CBD5E1" stroke-width="10" fill="none"/><circle cx="-40" cy="0" r="8" fill="#CBD5E1"/></g>`);
  if(t>=L[5]&&t<L[8]){ ov(label(700,330,'$1,000 · JUNE 1998',50,'#fff','#334155',pop(t,L[5]+.3))); if(t>=L[6]) ov(bigNum(700,560,money(TL.N.gift),150,'#FDE047',pop(t,L[6]+1.2))+shockwave(t,L[6]+1.3,700,500,420,'#FDE047')+confetti(t,L[6]+1.3,40)); }
  if(t>=L[8]&&t<L[12]) ov(`<g transform="translate(800 420) rotate(-4) scale(${f(pop(t,L[8]+.4))})" filter="url(#sh)"><rect x="-330" y="-150" width="660" height="300" fill="#FEF08A" stroke="${INK}" stroke-width="5"/><text x="0" y="-40" text-anchor="middle" font-size="44" fill="${INK}">P.S. You brought me soup.</text><text x="0" y="50" text-anchor="middle" font-size="44" fill="#16A34A">I planted you a tree. Fair trade.</text></g>`+tree({x:800,y:880,size:.06*pop(t,L[9]+1),leaves:1,t}));
  if(t>=L[12]) ov(label(900,330,'"If Derek makes trouble, read him page one."',40,INK,'#FEF3C7',pop(t,L[13]+.2)));
  return g;
};
SCN.friday=(t,s,L)=>{
  Object.assign(POS,{D:420,K:1500,W:960});
  let g=court()+judge(960,GY-120,t,{mood:t>L[9]?'laugh':'happy'})+`<rect x="660" y="${GY-140}" width="600" height="140" fill="#92400E" stroke="${INK}" stroke-width="6"/>`;
  g+=gavel({x:1140,y:GY-200,s:.7,hit:t>L[10]&&t<L[10]+.4?1:0});
  g+=CAST.derek({x:420,y:GY,t,talk:talkOf(t,'D'),mood:t>L[10]&&t<L[15]?'shocked':'happy',shades:t<L[10],act:t>L[10]&&t<L[11]+.5?'shock':undefined,actT:L[10],look:[1,0],extra:t<L[10]?(hr,hy)=>`<path d="M${f(-hr*1.1)} ${f(hy-hr*.6)} L${f(hr*1.1)} ${f(hy-hr*.6)} L${f(hr*.8)} ${f(hy-hr*1.2)} L${f(-hr*.8)} ${f(hy-hr*1.2)}Z" fill="#F8FAFC" stroke="${INK}" stroke-width="4"/><rect x="${f(-hr*.9)}" y="${f(hy-hr*.75)}" width="${f(hr*1.8)}" height="${f(hr*.15)}" fill="#1E3A8A"/>`:undefined,
    ...(t>=L[15]?{shirt:'#7C5A3A'}:{})});
  g+=CAST.lily({x:1260,y:GY,t,mood:t>L[10]?'laugh':'worried',act:t>L[10]&&t<L[11]?'cheer':undefined,look:[-1,0]});
  g+=CAST.kowalski({x:1500,y:GY,t,talk:talkOf(t,'K'),mood:'happy',look:[-1,0]});
  if(t>=L[3]&&t<L[8]){ const rules=['1. PAY YOURSELF FIRST: $300, EVERY MONTH','2. WHEN THE WORLD PANICS, GO SHOPPING','3. DON\'T TOUCH IT. TIME DOES THE WORK','4. BUY FREEDOM, NOT STUFF','5. IT GOES TO THE LIBRARY & THE HOSPITAL'];
    ov(`<rect width="${W}" height="${H}" fill="#0F172A" opacity="${f(.6*seg(t,L[3],L[3]+.4))}"/><g filter="url(#sh)"><rect x="380" y="200" width="1160" height="${f(70+rules.length*72)}" rx="16" fill="#FEF9C3" stroke="${INK}" stroke-width="5"/></g>`); rules.forEach((r,i)=>{ if(t>=L[3+i]) ov(`<text x="420" y="${275+i*72}" font-size="44" fill="${INK}" opacity="${f(seg(t,L[3+i],L[3+i]+.4))}">${r}</text>`); }); }
  if(t>=L[10]&&t<L[12]) ov(label(960,170,'THE WILL STANDS',80,'#fff','#16A34A',pop(t,L[10]+.3))+confetti(t,L[10]+.3,40));
  if(t>=L[13]&&t<L[15]) ov(`<g transform="translate(960 430) scale(${f(pop(t,L[13]+.3))})" filter="url(#sh)"><rect x="-150" y="-230" width="300" height="460" rx="20" fill="#334155" stroke="${INK}" stroke-width="6"/><rect x="-120" y="-180" width="240" height="380" rx="20" fill="#7C5A3A"/>${[0,1,2,3,4].map(i=>`<path d="M-40 ${-120+i*70} l60 0 a10 10 0 0 1 0 20 l-60 0" stroke="#CBD5E1" stroke-width="6" fill="none"/>`).join('')}</g>`);
  if(t>=L[15]&&t<L[16]+.5) ov(`<circle cx="${f(420+(t-L[15])*60)}" cy="${f(GY-300+Math.min(1,(t-L[15]))*-80+Math.pow(Math.max(0,t-L[15]-1),2)*200)}" r="10" fill="#CBD5E1" stroke="${INK}" stroke-width="3"/>`);
  return g;
};
SCN.ending=(t,s,L)=>{
  let g='';
  if(t<L[2]){ Object.assign(POS,{L:1300});
    g+=sky(t)+ground()+`<g filter="url(#sh)"><rect x="300" y="300" width="700" height="${GY-300}" fill="#F5F5F4" stroke="${INK}" stroke-width="7"/><path d="M260 310 L650 160 L1040 310Z" fill="#D6D3D1" stroke="${INK}" stroke-width="7"/><text x="650" y="280" text-anchor="middle" font-size="44" fill="${INK}">TOWN LIBRARY</text>${[0,1,2,3].map(i=>`<rect x="${380+i*160}" y="330" width="40" height="${GY-330}" fill="#E7E5E4" stroke="${INK}" stroke-width="5"/>`).join('')}</g>`;
    for(let i=0;i<4;i++){ const kx=lerp(-100-i*120,500+i*90,seg(t,L[0]+i*.4,L[0]+3+i*.4)); g+=CAST[['lily','ava','sam','mia'][i]||'lily']({x:kx,y:GY,h:300,t,act:'walk',mood:'happy',shirt:['#F472B6','#60A5FA','#FBBF24','#34D399'][i],adult:false}); }
    g+=CAST.lily({x:1300,y:GY,t,talk:talkOf(t,'L'),mood:'happy',look:[-1,0]});
  } else if(t<L[6]){ Object.assign(POS,{L:860});
    g+=kitchen()+storm_jar(1550,GY-200,.55*pop(t,L[5]));
    g+=CAST.lily({x:860,y:GY,t,talk:talkOf(t,'L'),mood:t>L[3]?'laugh':'happy',act:t>L[3]&&t<L[4]?'cheer':undefined,look:[1,0]});
    const cut=t>=L[3]; ov(`<g transform="translate(1250 420)">`+(cut?`<g transform="translate(-40 ${f(Math.min(120,(t-L[3])*160))}) rotate(-20)"><rect x="-80" y="-50" width="80" height="100" rx="10" fill="#0EA5E9" stroke="${INK}" stroke-width="5"/></g><g transform="translate(40 ${f(Math.min(140,(t-L[3])*180))}) rotate(25)"><rect x="0" y="-50" width="80" height="100" rx="10" fill="#0EA5E9" stroke="${INK}" stroke-width="5"/></g>`:`<rect x="-80" y="-50" width="160" height="100" rx="12" fill="#0EA5E9" stroke="${INK}" stroke-width="5"/><text x="0" y="35" text-anchor="middle" font-size="24" fill="#fff">DRAGON #3</text>`)+'</g>');
    if(t>=L[3]&&t<L[4]) ov(bigNum(1250,250,'SNIP!',110,'#E11D48',pop(t,L[3]+.1)));
    if(t>=L[4]) ov(envelopes({x:1250,y:700,s:.6*pop(t,L[4]+2),n:1})+label(1250,560,'$300 · NEXT MONTH',40,'#fff','#16A34A',pop(t,L[4]+2.5)));
  } else if(t<L[10]){
    g+=`<rect width="${W}" height="${H}" fill="#FFF1DC"/>`;
    if(t<L[8]) ov(label(960,330,'REAL PEOPLE HAVE DONE THIS',64,'#fff','#1E293B',pop(t,L[6]+.2))+label(960,470,'2014 · A VERMONT JANITOR LEFT ABOUT $8 MILLION',44,INK,'#FDE047',pop(t,L[7]+.3)));
    else ov(`<g transform="translate(960 480) scale(${f(pop(t,L[8]))})" filter="url(#sh)"><rect x="-720" y="-220" width="1440" height="440" rx="30" fill="#fff" stroke="${INK}" stroke-width="6"/>`+
      ['Walter, Lily and Derek are made up. So are their choices.','Market returns are real (S&amp;P 500 with dividends, before fees and taxes).','Past results don\'t promise the future.','Education, not financial advice.'].map((s2,i)=>`<text x="-650" y="${-110+i*85}" font-size="42" fill="#334155" style="font-weight:700">• ${s2}</text>`).join('')+'</g>'+
      `<text x="960" y="820" text-anchor="middle" font-size="26" fill="#64748B" style="font-weight:700">Data: S&amp;P 500 Total Return (Yahoo ^SP500TR); S&amp;P 500 daily closes (^GSPC) for Oct 19, 1987.</text>`);
  } else { Object.assign(POS,{L:1300});
    g+=`<rect width="${W}" height="${H}" fill="#FFF1DC"/>`+CAST.walter({x:620,y:GY+40,t,mood:'happy',act:'wave',holdR:soup({x:40,y:0,s:.5,t})})+CAST.lily({x:1300,y:GY+40,t,talk:talkOf(t,'L'),mood:'laugh',look:[-1,0]});
    ov(label(960,170,'COULD YOU LIVE LIKE WALTER FOR 10 YEARS?',62,'#fff','#1E293B',pop(t,L[10]))+label(760,330,'YES',70,'#fff','#16A34A',pop(t,L[10]+1.5),-5)+label(1160,330,'NO',70,'#fff','#E11D48',pop(t,L[10]+1.9),5));
    if(t>=L[13]){ ov(`<rect width="${W}" height="${H}" fill="#FFF1DC" opacity="${f(.92*seg(t,L[13],L[13]+.4))}"/>`+penny({x:760,y:900,r:220,t,mouth:TL.mouth[Math.round(t*30)]||0,blink:blinkAt(t),armL:150,armR:-120+Math.sin(t*6)*18}));
      const pr=t>L[13]+1.6; ov(`<g transform="translate(1320 500) scale(${f(pop(t,L[13]+.4))})" filter="url(#sh)"><rect x="-280" y="-80" width="560" height="160" rx="80" fill="${pr?'#475569':'#E5202B'}"/><text x="0" y="26" text-anchor="middle" font-size="66" fill="#fff">${pr?'SUBSCRIBED ✓':'SUBSCRIBE'}</text></g>`); }
  }
  return g;
};
