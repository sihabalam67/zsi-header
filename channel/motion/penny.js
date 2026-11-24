// Penny (channel mascot) + props as SVG strings. Shared by Shorts pages and thumbnails.
// Needs helpers f(), and defs ids coin/bag/sh in the page.
// ---------------------------------------------------------------- Penny ---
// origin = between the feet on the ground; r = coin radius
function penny(o){
  const {x,y,r=150,t=0,mood='happy',look=[0,0],mouth=0,armL=200,armR=-20,sx=1,sy=1,rot=0,walk=0,hold='',blink=false,sweat=0}=o;
  const leg=r*.55, cy=-(leg+r*.92);
  let g='';
  // legs + sneakers (walk cycle swings the feet)
  for(const s of [-1,1]){
    const ph=walk?Math.sin(t*14+(s>0?Math.PI:0))*r*.28:0, lift=walk?Math.max(0,Math.cos(t*14+(s>0?Math.PI:0)))*r*.12:0;
    const hx=s*r*.34, fx=hx+ph;
    g+=`<path d="M${f(hx)} ${f(cy+r*.8)} Q${f(hx+ph*.3)} ${f(-leg*.4)} ${f(fx)} ${f(-r*.1-lift)}" stroke="#A8670A" stroke-width="${f(r*.12)}" fill="none" stroke-linecap="round"/>`;
    g+=`<ellipse cx="${f(fx+s*r*.07)}" cy="${f(-r*.07-lift)}" rx="${f(r*.23)}" ry="${f(r*.12)}" fill="#E8453A" stroke="#7a1d16" stroke-width="${f(r*.04)}"/>`;
    g+=`<ellipse cx="${f(fx+s*r*.07)}" cy="${f(-r*.02-lift)}" rx="${f(r*.22)}" ry="${f(r*.05)}" fill="#fff" opacity=".9"/>`;
  }
  // arms (angle in degrees, 0 = right, 90 = down) with white gloves
  const arm=(s,ang)=>{
    const ax=s*r*.9, ay=cy+r*.15, a=ang*Math.PI/180, L=r*.78;
    const hx=ax+Math.cos(a)*L, hy=ay+Math.sin(a)*L;
    const mx=ax+Math.cos(a)*L*.5+s*r*.08, my=ay+Math.sin(a)*L*.5+r*.08;
    return {p:`<path d="M${f(ax)} ${f(ay)} Q${f(mx)} ${f(my)} ${f(hx)} ${f(hy)}" stroke="#A8670A" stroke-width="${f(r*.12)}" fill="none" stroke-linecap="round"/>`+
      `<circle cx="${f(hx)}" cy="${f(hy)}" r="${f(r*.17)}" fill="#fff" stroke="#3a2a1a" stroke-width="${f(r*.035)}"/>`+
      `<circle cx="${f(hx-s*r*.07)}" cy="${f(hy-r*.07)}" r="${f(r*.07)}" fill="#fff" stroke="#3a2a1a" stroke-width="${f(r*.03)}"/>`,hx,hy};
  };
  const L=arm(-1,armL), R=arm(1,armR);
  g+=L.p;
  // body: coin with rim, inner ring and gloss
  g+=`<circle cx="0" cy="${f(cy+r*.06)}" r="${f(r)}" fill="#B9740C"/>`;
  g+=`<circle cx="0" cy="${f(cy)}" r="${f(r)}" fill="url(#coin)" stroke="#A8670A" stroke-width="${f(r*.06)}"/>`;
  g+=`<circle cx="0" cy="${f(cy)}" r="${f(r*.82)}" fill="none" stroke="#FFE9A0" stroke-width="${f(r*.035)}" opacity=".85"/>`;
  g+=`<circle cx="0" cy="${f(cy)}" r="${f(r*.78)}" fill="none" stroke="#C98612" stroke-width="${f(r*.02)}" opacity=".6"/>`;
  g+=`<ellipse cx="${f(-r*.42)}" cy="${f(cy-r*.5)}" rx="${f(r*.24)}" ry="${f(r*.12)}" fill="#fff" opacity=".55" transform="rotate(-30 ${f(-r*.42)} ${f(cy-r*.5)})"/>`;
  // face
  const ey=cy-r*.1, shocked=mood==='shocked';
  for(const s of [-1,1]){
    const ex=s*r*.3, rx=r*(shocked?.2:.16), ry=r*(shocked?.25:.21)*(blink?.1:1);
    g+=`<ellipse cx="${f(ex)}" cy="${f(ey)}" rx="${f(rx)}" ry="${f(ry)}" fill="#fff" stroke="#3a2a1a" stroke-width="${f(r*.03)}"/>`;
    if(!blink){
      const pr=r*(shocked?.07:.105), px=ex+look[0]*r*.06, py=ey+look[1]*r*.06+r*.02;
      g+=`<circle cx="${f(px)}" cy="${f(py)}" r="${f(pr)}" fill="#2b1a0e"/>`;
      g+=`<circle cx="${f(px+pr*.35)}" cy="${f(py-pr*.4)}" r="${f(pr*.38)}" fill="#fff"/>`;
      g+=`<circle cx="${f(px-pr*.35)}" cy="${f(py+pr*.35)}" r="${f(pr*.16)}" fill="#fff"/>`;
    }
    // brows
    const by=ey-r*(shocked?.36:.3), tilt=mood==='worried'?-1:mood==='proud'?.4:shocked?0:.2;
    g+=`<path d="M${f(ex-s*r*.14)} ${f(by+tilt*s*0+ (mood==='worried'?-r*.0:0))} Q${f(ex)} ${f(by-r*.07)} ${f(ex+s*r*.14)} ${f(by+(mood==='worried'?r*.08:0))}" stroke="#7a4a08" stroke-width="${f(r*.045)}" fill="none" stroke-linecap="round" transform="rotate(${mood==='worried'?-s*14:0} ${f(ex)} ${f(by)})"/>`;
    g+=`<ellipse cx="${f(s*r*.5)}" cy="${f(cy+r*.16)}" rx="${f(r*.12)}" ry="${f(r*.07)}" fill="#FF7A6B" opacity=".55"/>`;
  }
  // mouth
  const my=cy+r*.28;
  if(shocked){
    g+=`<ellipse cx="0" cy="${f(my+r*.04)}" rx="${f(r*.1)}" ry="${f(r*.14)}" fill="#5a1410"/>`;
  }else if(mouth>.06){
    const o=r*(.04+.17*mouth);
    g+=`<path d="M${f(-r*.17)} ${f(my-r*.02)} Q0 ${f(my-r*.05)} ${f(r*.17)} ${f(my-r*.02)} Q${f(r*.14)} ${f(my+o)} 0 ${f(my+o)} Q${f(-r*.14)} ${f(my+o)} ${f(-r*.17)} ${f(my-r*.02)}Z" fill="#5a1410"/>`;
    g+=`<ellipse cx="0" cy="${f(my+o*.75)}" rx="${f(r*.08)}" ry="${f(o*.3)}" fill="#FF7A88"/>`;
  }else if(mood==='worried'){
    g+=`<path d="M${f(-r*.13)} ${f(my+r*.06)} Q0 ${f(my-r*.05)} ${f(r*.13)} ${f(my+r*.06)}" stroke="#5a1410" stroke-width="${f(r*.045)}" fill="none" stroke-linecap="round"/>`;
  }else{
    g+=`<path d="M${f(-r*.17)} ${f(my-r*.02)} Q0 ${f(my+r*.2)} ${f(r*.17)} ${f(my-r*.02)}Z" fill="#5a1410"/><ellipse cx="0" cy="${f(my+r*.09)}" rx="${f(r*.07)}" ry="${f(r*.03)}" fill="#FF7A88"/>`;
  }
  if(sweat>0){
    g+=`<path d="M${f(r*.72)} ${f(cy-r*.55+sweat*r*.15)} q${f(r*.07)} ${f(r*.12)} 0 ${f(r*.16)} q${f(-r*.07)} ${f(-r*.04)} 0 ${f(-r*.16)}Z" fill="#7CD3FF" stroke="#2a7fb8" stroke-width="3" opacity="${f(sweat)}"/>`;
  }
  g+=R.p;
  if(hold==='bag') g+=coffeeBag(R.hx+r*.05,R.hy-r*.1,r*.0045,-8);
  if(hold==='check') g+=paycheck(R.hx+r*.2,R.hy-r*.25,r*.0042,-10);
  return `<g transform="translate(${f(x)} ${f(y)}) rotate(${f(rot)}) scale(${f(sx)} ${f(sy)})">`+
    `<ellipse cx="0" cy="${f(r*.02)}" rx="${f(r*.75/sy)}" ry="${f(r*.12)}" fill="#5a2a0a" opacity=".18"/>`+g+`</g>`;
}

// ---------------------------------------------------------------- props ---
function coffeeBag(x,y,s,rot){ // s = scale (1 => 220 px wide)
  return `<g transform="translate(${f(x)} ${f(y)}) rotate(${f(rot)}) scale(${s})" filter="url(#sh)">
   <path d="M-110 -150 L110 -150 L128 150 Q0 168 -128 150Z" fill="url(#bag)"/>
   <path d="M-110 -150 L110 -150 L104 -112 L-104 -112Z" fill="#7d4a22"/>
   <path d="M-96 -150 L-90 -190 L90 -190 L96 -150Z" fill="#C98B52"/>
   <path d="M-90 -178 L90 -178" stroke="#7d4a22" stroke-width="6" stroke-dasharray="10 8"/>
   <rect x="-82" y="-80" width="164" height="170" rx="18" fill="#FFF7EA"/>
   <text x="0" y="-36" text-anchor="middle" font-size="32" fill="#5a2f12">COFFEE</text>
   <ellipse cx="0" cy="20" rx="30" ry="40" fill="#5a2f12" transform="rotate(25 0 20)"/>
   <path d="M-6 -14 Q14 20 -4 56" stroke="#C98B52" stroke-width="7" fill="none" transform="rotate(25 0 20)"/>
   <text x="0" y="82" text-anchor="middle" font-size="22" fill="#a0603a">1 LB</text>
  </g>`;
}
function tag(x,y,label,col,rot,s=1){
  return `<g transform="translate(${f(x)} ${f(y)}) rotate(${f(rot)}) scale(${f(s)})" filter="url(#sh)">
   <path d="M0 -150 L0 -60" stroke="#6b4a2a" stroke-width="5"/>
   <path d="M-150 -60 L120 -60 Q150 -60 150 -30 L150 70 Q150 100 120 100 L-150 100 L-200 20Z" fill="${col}" stroke="#fff" stroke-width="8" stroke-linejoin="round"/>
   <circle cx="-150" cy="20" r="14" fill="#FFF3DC"/>
   <text x="10" y="50" text-anchor="middle" font-size="96" fill="#fff">${label}</text>
  </g>`;
}
function paycheck(x,y,s,rot){
  return `<g transform="translate(${f(x)} ${f(y)}) rotate(${f(rot)}) scale(${s})" filter="url(#sh)">
   <rect x="-150" y="-80" width="300" height="160" rx="14" fill="#E9FFF3" stroke="#16A673" stroke-width="8"/>
   <text x="-130" y="-30" font-size="30" fill="#16A673">PAYCHECK</text>
   <circle cx="95" cy="-30" r="32" fill="#16A673"/><text x="95" y="-17" text-anchor="middle" font-size="40" fill="#fff">$</text>
   <rect x="-130" y="10" width="170" height="12" rx="6" fill="#9ad9bb"/><rect x="-130" y="40" width="110" height="12" rx="6" fill="#9ad9bb"/>
  </g>`;
}
function mug(x,y,s,t,run){ // a running coffee mug with a face
  const b=run?Math.abs(Math.sin(t*14))*18:0;
  let g=`<g transform="translate(${f(x)} ${f(y-b)}) scale(${s})">`;
  for(const k of [-1,1]){const ph=run?Math.sin(t*14+(k>0?Math.PI:0))*40:0;
    g+=`<path d="M${k*40} 60 L${f(k*40+ph)} ${f(150+b)}" stroke="#5a2f12" stroke-width="16" stroke-linecap="round"/><ellipse cx="${f(k*40+ph+12)}" cy="${f(152+b)}" rx="34" ry="16" fill="#3b82f6"/>`;}
  for(let i=0;i<3;i++){const w=Math.sin(t*4+i*2)*14;
    g+=`<path d="M${-40+i*40} -110 q${f(w)} -30 0 -60 q${f(-w)} -30 0 -60" stroke="#fff" stroke-width="12" fill="none" stroke-linecap="round" opacity=".75"/>`;}
  g+=`<path d="M95 -40 q70 0 70 50 q0 50 -70 50" stroke="#F5F0E8" stroke-width="26" fill="none"/>`;
  g+=`<path d="M-110 -100 L110 -100 L95 70 Q0 90 -95 70Z" fill="#FFFDF8" stroke="#d8cfc0" stroke-width="6" filter="url(#sh)"/>`;
  g+=`<ellipse cx="0" cy="-100" rx="110" ry="24" fill="#6b3a17" stroke="#d8cfc0" stroke-width="6"/>`;
  g+=`<circle cx="-38" cy="-30" r="15" fill="#2b1a0e"/><circle cx="38" cy="-30" r="15" fill="#2b1a0e"/><circle cx="-33" cy="-35" r="5" fill="#fff"/><circle cx="43" cy="-35" r="5" fill="#fff"/>`;
  g+=`<path d="M-30 10 Q0 40 30 10" stroke="#2b1a0e" stroke-width="9" fill="none" stroke-linecap="round"/>`;
  g+=`<text x="0" y="62" text-anchor="middle" font-size="34" fill="#E0392B">+122%</text></g>`;
  return g;
}
function steak(x,y,s){return `<g transform="translate(${x} ${y}) scale(${s})"><path d="M-40 -20 Q-30 -45 10 -40 Q50 -35 45 0 Q40 35 0 35 Q-45 35 -40 -20Z" fill="#E2574C" stroke="#fff" stroke-width="6"/><circle cx="12" cy="-4" r="10" fill="#fff"/></g>`}
function egg(x,y,s){return `<g transform="translate(${x} ${y}) scale(${s})"><ellipse cx="0" cy="0" rx="32" ry="42" fill="#FFF9EF" stroke="#e8d8bd" stroke-width="6"/><ellipse cx="-10" cy="-14" rx="8" ry="12" fill="#fff"/></g>`}
function bread(x,y,s){return `<g transform="translate(${x} ${y}) scale(${s})"><path d="M-42 34 L-42 -6 Q-50 -40 0 -40 Q50 -40 42 -6 L42 34Z" fill="#E9A85B" stroke="#a8652a" stroke-width="6"/><path d="M-30 -6 Q0 -22 30 -6" stroke="#a8652a" stroke-width="5" fill="none"/></g>`}
function bean(x,y,s,rot){return `<g transform="translate(${f(x)} ${f(y)}) rotate(${f(rot)}) scale(${f(s)})"><ellipse rx="22" ry="30" fill="#6b3a17"/><path d="M-3 -24 Q10 0 -3 24" stroke="#C98B52" stroke-width="5" fill="none"/></g>`}
