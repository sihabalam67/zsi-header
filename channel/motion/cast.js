// Coin Theory story cast (SVG strings, pure functions of their inputs). Needs penny.js helpers (f) and kit.js (MK).
// Every character's origin is the point between its feet on the ground. h = total height in px.
const INK = '#2b1a0e', OUT = 5;
const ff = n => (+n).toFixed(1);

function eyes(x, y, r, o) {
  const { look = [0, 0], blink = false, mood = 'happy' } = o; let g = '';
  const big = mood === 'shocked';
  for (const s of [-1, 1]) {
    const ex = x + s * r * 0.36, rx = r * (big ? .2 : .17), ry = r * (big ? .26 : .21) * (blink ? .1 : 1);
    g += `<ellipse cx="${ff(ex)}" cy="${ff(y)}" rx="${ff(rx)}" ry="${ff(ry)}" fill="#fff" stroke="${INK}" stroke-width="${ff(r * .04)}"/>`;
    if (!blink) {
      const pr = r * (big ? .08 : .11), px = ex + look[0] * r * .06, py = y + look[1] * r * .06 + r * .02;
      g += `<circle cx="${ff(px)}" cy="${ff(py)}" r="${ff(pr)}" fill="${INK}"/><circle cx="${ff(px + pr * .35)}" cy="${ff(py - pr * .4)}" r="${ff(pr * .4)}" fill="#fff"/>`;
    }
    const by = y - r * (big ? .4 : .33), tilt = mood === 'sad' || mood === 'worried' ? 1 : mood === 'angry' ? -1 : 0;
    g += `<path d="M${ff(ex - s * r * .16)} ${ff(by + tilt * r * .06)} Q${ff(ex)} ${ff(by - r * .07)} ${ff(ex + s * r * .16)} ${ff(by - tilt * r * .04)}" stroke="${INK}" stroke-width="${ff(r * .055)}" fill="none" stroke-linecap="round"/>`;
  }
  return g;
}
function mouthP(x, y, r, o) {
  const { mood = 'happy', talk = 0 } = o;
  if (mood === 'shocked') return `<ellipse cx="${ff(x)}" cy="${ff(y + r * .04)}" rx="${ff(r * .1)}" ry="${ff(r * .14)}" fill="#5a1410"/>`;
  if (talk > .06) { const op = r * (.04 + .18 * talk);
    return `<path d="M${ff(x - r * .17)} ${ff(y - r * .02)} Q${ff(x)} ${ff(y - r * .05)} ${ff(x + r * .17)} ${ff(y - r * .02)} Q${ff(x + r * .14)} ${ff(y + op)} ${ff(x)} ${ff(y + op)} Q${ff(x - r * .14)} ${ff(y + op)} ${ff(x - r * .17)} ${ff(y - r * .02)}Z" fill="#5a1410"/><ellipse cx="${ff(x)}" cy="${ff(y + op * .75)}" rx="${ff(r * .08)}" ry="${ff(op * .3)}" fill="#FF7A88"/>`; }
  if (mood === 'sad' || mood === 'worried') return `<path d="M${ff(x - r * .14)} ${ff(y + r * .08)} Q${ff(x)} ${ff(y - r * .05)} ${ff(x + r * .14)} ${ff(y + r * .08)}" stroke="#5a1410" stroke-width="${ff(r * .05)}" fill="none" stroke-linecap="round"/>`;
  if (mood === 'laugh') return `<path d="M${ff(x - r * .22)} ${ff(y - r * .04)} Q${ff(x)} ${ff(y + r * .32)} ${ff(x + r * .22)} ${ff(y - r * .04)}Z" fill="#5a1410"/><ellipse cx="${ff(x)}" cy="${ff(y + r * .14)}" rx="${ff(r * .1)}" ry="${ff(r * .05)}" fill="#FF7A88"/>`;
  return `<path d="M${ff(x - r * .17)} ${ff(y - r * .02)} Q${ff(x)} ${ff(y + r * .2)} ${ff(x + r * .17)} ${ff(y - r * .02)}Z" fill="#5a1410"/>`;
}
function limb(x1, y1, x2, y2, col, w, bend = 0) {
  const mx = (x1 + x2) / 2 + bend, my = (y1 + y2) / 2;
  return `<path d="M${ff(x1)} ${ff(y1)} Q${ff(mx)} ${ff(my)} ${ff(x2)} ${ff(y2)}" stroke="${INK}" stroke-width="${ff(w + OUT * 2)}" fill="none" stroke-linecap="round"/>` +
    `<path d="M${ff(x1)} ${ff(y1)} Q${ff(mx)} ${ff(my)} ${ff(x2)} ${ff(y2)}" stroke="${col}" stroke-width="${ff(w)}" fill="none" stroke-linecap="round"/>`;
}
function hand(x, y, r, skin) { return `<circle cx="${ff(x)}" cy="${ff(y)}" r="${ff(r)}" fill="${skin}" stroke="${INK}" stroke-width="${OUT}"/>`; }

// A person. o: {x,y,h, skin, hair, hairStyle:'pony'|'short'|'curly'|'bald', shirt, pants, shoes, mood, talk, t, walk,
// armL, armR (deg, 0=right, 90=down), look, blink, hold:{svg} drawn at right hand, sx, sy, rot, extra(fn)}
const lerpA = (a, b, k) => a + (b - a) * k;
function person(o) {
  const { x, y, h = 420, skin = '#F2C9A0', hair = '#5a3418', hairStyle = 'short', shirt = '#3B82F6', pants = '#334155',
    shoes = '#E5453A', t = 0, walk = 0, armL = 110, armR = 70, sx = 1, sy = 1, rot = 0, beard = false, glasses = false,
    suspenders = false, holdR = '', holdL = '' } = o;
  // ---- "alive" layer: breathing, sway, auto-blink, talking gestures, acting presets ----
  const ph = o.phase !== undefined ? o.phase : (h * .37) % 6.28, talk = o.talk || 0;
  let aL = armL, aR = armR, yOff = 0, rOff = Math.sin(t * .6 + ph) * .4, headRot = Math.sin(t * .5 + ph) * .8, sq = 1;
  if (o.blink === undefined) o.blink = ((t + ph) % 3.6) < .12;
  if (talk > .04 || o.talking) { // calm, readable talking: slow head nods and one hand gesturing (no jitter: k is not driven by loudness)
    const k = .8;
    headRot += Math.sin(t * 2.2 + ph) * 2.2 * k; aR += Math.sin(t * 1.6 + ph) * 9 * k - 14 * k; aL += Math.sin(t * 1.3 + ph + 1) * 4 * k; }
  const act = o.act, at = t - (o.actT || 0);
  if (act === 'wave') { aR = -70 + Math.sin(t * 6) * 20; }
  if (act === 'cheer') { aL = 225 + Math.sin(t * 5) * 8; aR = -45 - Math.sin(t * 5) * 8; yOff -= Math.abs(Math.sin(t * 4)) * h * .035; }
  if (act === 'point') { aR = -15 + Math.sin(t * 4) * 4; }
  if (act === 'shrug') { const k = Math.sin(Math.min(1, at * 3) * Math.PI / 2); aL = lerpA(armL, 150, k); aR = lerpA(armR, 30, k); headRot += 8 * k; }
  if (act === 'facepalm') { aR = -115; headRot -= 10; }
  if (act === 'think') { aR = -95 + Math.sin(t * 2) * 4; headRot += 6; }
  if (act === 'laugh') { rOff += Math.sin(t * 8) * 1.2; yOff -= Math.abs(Math.sin(t * 8)) * h * .006; }
  if (act === 'jump') { const k = (at % 1.1) / 1.1; yOff -= Math.sin(k * Math.PI) * h * .22; sq = k < .08 || k > .92 ? .9 : 1.04; }
  if (act === 'shock') { const k = Math.min(1, at * 4); yOff -= Math.sin(k * Math.PI) * h * .1; aL = 220; aR = -40; rOff += -6 * k; }
  if (act === 'shake') { rOff += Math.sin(t * 10) * 1.5; }
  if (act === 'walk') { o.walk = 1; yOff -= Math.abs(Math.sin(t * 7)) * h * .01; aL = 100 + Math.sin(t * 7) * 18; aR = 80 - Math.sin(t * 7) * 18; }
  const breathe = 1 + Math.sin(t * 1.8 + ph) * .006;
  const hr = h * .17, hy = -h + hr * 1.05, sh = hy + hr * .95, hip = -h * .36, bw = h * .2;
  let g = '';
  // legs
  for (const s of [-1, 1]) {
    const ph2 = (walk || o.walk) ? Math.sin(t * 7 + (s > 0 ? Math.PI : 0)) * h * .06 : 0, lift = (walk || o.walk) ? Math.max(0, Math.cos(t * 7 + (s > 0 ? Math.PI : 0))) * h * .025 : 0;
    g += limb(s * bw * .28, hip, s * bw * .3 + ph2, -h * .04 - lift, pants, h * .075);
    g += `<ellipse cx="${ff(s * bw * .3 + ph2 + s * h * .025)}" cy="${ff(-h * .025 - lift)}" rx="${ff(h * .065)}" ry="${ff(h * .035)}" fill="${shoes}" stroke="${INK}" stroke-width="${OUT}"/>`;
  }
  // arms behind body? left arm first
  const arm = (s, ang, hold) => { const ax = s * bw * .5, ay = sh + h * .05, a = ang * Math.PI / 180, L = h * .27;
    const hx = ax + Math.cos(a) * L, hy2 = ay + Math.sin(a) * L;
    return limb(ax, ay, hx, hy2, shirt, h * .06, s * h * .02) + hand(hx, hy2, h * .04, skin) + (hold ? `<g transform="translate(${ff(hx)} ${ff(hy2)})">${hold}</g>` : ''); };
  g += arm(-1, aL, holdL);
  // body
  g += `<path d="M${ff(-bw * .5)} ${ff(sh + h * .02)} Q${ff(-bw * .62)} ${ff(hip + h * .02)} ${ff(-bw * .45)} ${ff(hip + h * .03)} L${ff(bw * .45)} ${ff(hip + h * .03)} Q${ff(bw * .62)} ${ff(hip + h * .02)} ${ff(bw * .5)} ${ff(sh + h * .02)} Q0 ${ff(sh - h * .02)} ${ff(-bw * .5)} ${ff(sh + h * .02)}Z" fill="${shirt}" stroke="${INK}" stroke-width="${OUT}" stroke-linejoin="round"/>`;
  if (suspenders) for (const s of [-1, 1]) g += `<path d="M${ff(s * bw * .28)} ${ff(sh + h * .01)} L${ff(s * bw * .25)} ${ff(hip + h * .03)}" stroke="#D3302B" stroke-width="${ff(h * .022)}"/>`;
  // head (rotates around the neck)
  g += `<g transform="rotate(${ff(headRot)} 0 ${ff(sh)})">`;
  g += `<rect x="${ff(-h * .03)}" y="${ff(sh - h * .03)}" width="${ff(h * .06)}" height="${ff(h * .05)}" fill="${skin}"/>`;
  if (hairStyle === 'pony') g += `<ellipse cx="${ff(hr * 1.25)}" cy="${ff(hy + hr * .05)}" rx="${ff(hr * .42)}" ry="${ff(hr * .7)}" fill="${hair}" stroke="${INK}" stroke-width="${OUT}" transform="rotate(${ff(20 + Math.sin(t * 5) * 6)} ${ff(hr * .7)} ${ff(hy - hr * .5)})"/>`;
  if (hairStyle === 'curly') for (let i = 0; i < 9; i++) { const a = Math.PI * (1.05 + i * .11); g += `<circle cx="${ff(Math.cos(a) * hr * 1.0)}" cy="${ff(hy + Math.sin(a) * hr * 1.0)}" r="${ff(hr * .3)}" fill="${hair}" stroke="${INK}" stroke-width="${OUT}"/>`; }
  g += `<circle cx="${ff(-hr * .98)}" cy="${ff(hy + hr * .05)}" r="${ff(hr * .2)}" fill="${skin}" stroke="${INK}" stroke-width="${OUT}"/><circle cx="${ff(hr * .98)}" cy="${ff(hy + hr * .05)}" r="${ff(hr * .2)}" fill="${skin}" stroke="${INK}" stroke-width="${OUT}"/>`;
  g += `<circle cx="0" cy="${ff(hy)}" r="${ff(hr)}" fill="${skin}" stroke="${INK}" stroke-width="${OUT}"/>`;
  if (hairStyle === 'short' || hairStyle === 'pony') g += `<path d="M${ff(-hr * .98)} ${ff(hy - hr * .05)} Q${ff(-hr * 1.05)} ${ff(hy - hr * 1.15)} 0 ${ff(hy - hr * 1.05)} Q${ff(hr * 1.05)} ${ff(hy - hr * 1.15)} ${ff(hr * .98)} ${ff(hy - hr * .05)} Q${ff(hr * .5)} ${ff(hy - hr * .62)} ${ff(-hr * .1)} ${ff(hy - hr * .5)} Q${ff(-hr * .6)} ${ff(hy - hr * .45)} ${ff(-hr * .98)} ${ff(hy - hr * .05)}Z" fill="${hair}" stroke="${INK}" stroke-width="${OUT}" stroke-linejoin="round"/>`;
  if (hairStyle === 'curly') g += `<path d="M${ff(-hr * .9)} ${ff(hy - hr * .2)} Q0 ${ff(hy - hr * 1.3)} ${ff(hr * .9)} ${ff(hy - hr * .2)} Q${ff(hr * .2)} ${ff(hy - hr * .6)} ${ff(-hr * .9)} ${ff(hy - hr * .2)}Z" fill="${hair}"/>`;
  if (hairStyle === 'bald') for (const s of [-1, 1]) g += `<path d="M${ff(s * hr * .95)} ${ff(hy + hr * .1)} Q${ff(s * hr * 1.15)} ${ff(hy - hr * .5)} ${ff(s * hr * .55)} ${ff(hy - hr * .75)}" stroke="${hair}" stroke-width="${ff(hr * .32)}" fill="none" stroke-linecap="round"/>`;
  g += eyes(0, hy - hr * .05, hr, o);
  g += `<ellipse cx="${ff(-hr * .5)}" cy="${ff(hy + hr * .25)}" rx="${ff(hr * .13)}" ry="${ff(hr * .08)}" fill="#FF8A7A" opacity=".55"/><ellipse cx="${ff(hr * .5)}" cy="${ff(hy + hr * .25)}" rx="${ff(hr * .13)}" ry="${ff(hr * .08)}" fill="#FF8A7A" opacity=".55"/>`;
  if (glasses) for (const s of [-1, 1]) g += `<circle cx="${ff(s * hr * .36)}" cy="${ff(hy - hr * .05)}" r="${ff(hr * .27)}" fill="none" stroke="${INK}" stroke-width="${ff(hr * .06)}"/>`;
  g += mouthP(0, hy + hr * .42, hr, o);
  if (beard) g += `<path d="M${ff(-hr * .62)} ${ff(hy + hr * .32)} Q${ff(-hr * .3)} ${ff(hy + hr * .12)} 0 ${ff(hy + hr * .28)} Q${ff(hr * .3)} ${ff(hy + hr * .12)} ${ff(hr * .62)} ${ff(hy + hr * .32)} Q${ff(hr * .35)} ${ff(hy + hr * .5)} 0 ${ff(hy + hr * .38)} Q${ff(-hr * .35)} ${ff(hy + hr * .5)} ${ff(-hr * .62)} ${ff(hy + hr * .32)}Z" fill="#F4F4F4" stroke="${INK}" stroke-width="${ff(OUT * .8)}" stroke-linejoin="round"/>`;
  g += `</g>`;
  g += arm(1, aR, holdR);
  if (o.tears) for (const s2 of [-1, 1]) { const ex = s2 * hr * .36, ty = hy + hr * .1;
    g += `<path d="M${ff(ex - hr * .08)} ${ff(ty)} Q${ff(ex - hr * .12)} ${ff(ty + hr * .5)} ${ff(ex - hr * .02)} ${ff(ty + hr * 1.0)} L${ff(ex + hr * .1)} ${ff(ty + hr * 1.0)} Q${ff(ex + hr * .1)} ${ff(ty + hr * .45)} ${ff(ex + hr * .08)} ${ff(ty)}Z" fill="#7DD3FC" stroke="#0369A1" stroke-width="3" opacity=".9"/>`; }
  if (o.extra) g += o.extra(hr, hy);
  return `<g transform="translate(${ff(x)} ${ff(y)})"><ellipse cx="0" cy="0" rx="${ff(h * .16)}" ry="${ff(h * .025)}" fill="#000" opacity=".18"/><g transform="translate(0 ${ff(yOff)}) rotate(${ff(rot + rOff)}) scale(${ff(sx / Math.sqrt(sq * breathe))} ${ff(sy * sq * breathe)})">${g}</g></g>`;
}

// The family. age: 'kid' (1996) or 'adult' (2026); pass extra options through.
const CAST = {
  grandpa: o => person(Object.assign({ h: 610, skin: '#F1C7A3', hair: '#EDEDED', hairStyle: 'bald', shirt: '#4F7CAC', pants: '#5B4636', shoes: '#4a2c18', beard: true, glasses: true, suspenders: true }, o)),
  mia: o => person(Object.assign({ h: o.adult ? 570 : 430, skin: '#E8B48A', hair: '#2b1608', hairStyle: 'pony', shirt: '#EC4899', pants: '#6D28D9', shoes: '#FACC15' }, o)),
  ben: o => person(Object.assign({ h: o.adult ? 580 : 395, skin: '#F6D2B3', hair: '#C2410C', hairStyle: 'short', shirt: '#22C55E', pants: '#1E3A8A', shoes: '#F97316' }, o)),
  rosie: o => person(Object.assign({ h: o.adult ? 565 : 410, skin: '#8D5A3B', hair: '#1c0f08', hairStyle: 'curly', shirt: '#F59E0B', pants: '#0F766E', shoes: '#EF4444' }, o)),
};

// Nickel the parrot. squawk 0..1 opens the beak and fluffs.
function parrot(o) {
  const { x, y, s = 1, t = 0, squawk = 0, flip = false } = o, b = Math.sin(t * 3) * 4;
  const fl = 1 + squawk * .12;
  return `<g transform="translate(${ff(x)} ${ff(y + b)}) scale(${ff((flip ? -1 : 1) * s * fl)} ${ff(s * fl)})">` +
    `<path d="M-10 60 L-30 120 L-5 112 L5 125 L18 60Z" fill="#1E9E5A" stroke="${INK}" stroke-width="5" stroke-linejoin="round"/>` +
    `<ellipse cx="0" cy="20" rx="48" ry="62" fill="#22C55E" stroke="${INK}" stroke-width="5"/>` +
    `<path d="M-30 0 Q-62 40 -28 78 Q-15 40 -30 0Z" fill="#16A34A" stroke="${INK}" stroke-width="5"/><path d="M-38 58 Q-44 72 -28 80" stroke="#E11D48" stroke-width="10" fill="none"/>` +
    `<circle cx="10" cy="-40" r="40" fill="#22C55E" stroke="${INK}" stroke-width="5"/>` +
    `<circle cx="20" cy="-48" r="13" fill="#fff" stroke="${INK}" stroke-width="4"/><circle cx="23" cy="-48" r="6" fill="${INK}"/>` +
    `<path d="M42 -48 Q78 -40 60 -14 L44 -24Z" fill="#FBBF24" stroke="${INK}" stroke-width="5" stroke-linejoin="round" transform="rotate(${ff(-squawk * 18)} 44 -36)"/>` +
    `<path d="M44 -24 L60 -14 Q52 -6 40 -12Z" fill="#F59E0B" stroke="${INK}" stroke-width="5" transform="rotate(${ff(squawk * 22)} 44 -24)"/>` +
    `<path d="M-20 -72 Q-10 -100 8 -80 Q14 -108 28 -78" stroke="#E11D48" stroke-width="9" fill="none" stroke-linecap="round"/>` +
    `<line x1="-10" y1="80" x2="-14" y2="98" stroke="${INK}" stroke-width="6"/><line x1="12" y1="80" x2="14" y2="98" stroke="${INK}" stroke-width="6"/></g>`;
}

// Inflation Mouse. nibble 0..1 animates jaw; label shows "INFLATION" tag.
function mouse(o) {
  const { x, y, s = 1, t = 0, nibble = 0, tag = true, flip = false } = o, j = Math.sin(t * 22) * 4 * nibble;
  return `<g transform="translate(${ff(x)} ${ff(y)}) scale(${ff((flip ? -1 : 1) * s)} ${ff(s)})">` +
    `<path d="M-60 -10 Q-120 -30 -110 -80 Q-104 -100 -90 -96" stroke="#B9A8A0" stroke-width="7" fill="none" stroke-linecap="round"/>` +
    `<ellipse cx="0" cy="-30" rx="62" ry="40" fill="#A8A29E" stroke="${INK}" stroke-width="5"/>` +
    `<circle cx="40" cy="-80" r="26" fill="#A8A29E" stroke="${INK}" stroke-width="5"/><circle cx="40" cy="-80" r="14" fill="#F9A8D4"/>` +
    `<circle cx="78" cy="-72" r="26" fill="#A8A29E" stroke="${INK}" stroke-width="5"/><circle cx="78" cy="-72" r="14" fill="#F9A8D4"/>` +
    `<ellipse cx="72" cy="-38" rx="40" ry="30" fill="#A8A29E" stroke="${INK}" stroke-width="5"/>` +
    `<circle cx="104" cy="${ff(-34 + j * .3)}" r="9" fill="#F472B6" stroke="${INK}" stroke-width="4"/>` +
    `<circle cx="78" cy="-48" r="7" fill="${INK}"/><circle cx="80" cy="-50" r="2.5" fill="#fff"/>` +
    `<path d="M80 ${ff(-22 + j)} q8 6 16 0" stroke="${INK}" stroke-width="4" fill="none"/><rect x="84" y="${ff(-20 + j)}" width="6" height="8" fill="#fff" stroke="${INK}" stroke-width="2"/>` +
    `<line x1="-20" y1="6" x2="-24" y2="14" stroke="${INK}" stroke-width="6"/><line x1="26" y1="6" x2="30" y2="14" stroke="${INK}" stroke-width="6"/>` +
    (tag ? `<g transform="translate(-10 -24) rotate(-6)"><rect x="-58" y="-16" width="116" height="30" rx="8" fill="#E5202B" stroke="#fff" stroke-width="3"/><text x="0" y="6" text-anchor="middle" font-size="19" fill="#fff" font-family="P" font-weight="900">INFLATION</text></g>` : '') + `</g>`;
}

// Money tree. size 0..1 (sapling..huge), leaves 0..1, shake (px), coins = number of gold coins hanging, seed=layout
function tree(o) {
  const { x, y, size = 1, leaves = 1, shake = 0, coins = 0, t = 0 } = o;
  if (size < .2) { // sapling: a thin stick with two leaves
    const hh = 90 + 300 * size, wv = Math.sin(t * 3) * 4 + Math.sin(t * 40) * shake * .3;
    return `<g transform="translate(${ff(x)} ${ff(y)})"><ellipse cx="0" cy="3" rx="40" ry="9" fill="#000" opacity=".15"/><path d="M0 0 Q${ff(wv * .5)} ${ff(-hh * .5)} ${ff(wv)} ${ff(-hh)}" stroke="${INK}" stroke-width="14" fill="none" stroke-linecap="round"/><path d="M0 0 Q${ff(wv * .5)} ${ff(-hh * .5)} ${ff(wv)} ${ff(-hh)}" stroke="#8B5A2B" stroke-width="7" fill="none" stroke-linecap="round"/>` +
      `<path d="M${ff(wv)} ${ff(-hh)} q-50 -10 -60 -45 q45 0 60 45Z" fill="#46C266" stroke="${INK}" stroke-width="4"/><path d="M${ff(wv)} ${ff(-hh + 20)} q50 -10 60 -45 q-45 0 -60 45Z" fill="#2E9E4F" stroke="${INK}" stroke-width="4"/>` +
      (coins ? `<circle cx="${ff(wv + 10)}" cy="${ff(-hh * .55)}" r="14" fill="#FFD23F" stroke="${INK}" stroke-width="4"/>` : '') + `</g>`;
  }
  const H = (120 + 560 * size) * 1.18, tw = (14 + 50 * size) * 1.15, sw = Math.sin(t * 40) * shake;
  let g = `<path d="M${ff(-tw / 2)} 0 Q${ff(-tw * .3)} ${ff(-H * .5)} ${ff(-tw * .25 + sw * .3)} ${ff(-H * .7)} L${ff(tw * .25 + sw * .3)} ${ff(-H * .7)} Q${ff(tw * .3)} ${ff(-H * .5)} ${ff(tw / 2)} 0Z" fill="#8B5A2B" stroke="${INK}" stroke-width="${OUT}"/>`;
  if (size > .25) for (const s of [-1, 1]) g += `<path d="M${ff(s * tw * .1 + sw * .4)} ${ff(-H * .55)} Q${ff(s * H * .18 + sw)} ${ff(-H * .65)} ${ff(s * H * .26 + sw)} ${ff(-H * .78)}" stroke="#8B5A2B" stroke-width="${ff(tw * .35)}" fill="none" stroke-linecap="round"/>`;
  const R = (60 + 300 * size) * 1.18, cy = -H * .78, n = 9;
  const blobs = [];
  for (let i = 0; i < n; i++) { const a = i / n * Math.PI * 2 + .3; blobs.push([Math.cos(a) * R * .55 + sw * 1.2, cy + Math.sin(a) * R * .38 - R * .05, R * (.42 + .12 * Math.sin(i * 2.7))]); }
  blobs.push([sw * 1.2, cy - R * .1, R * .62]);
  const shown = Math.ceil(blobs.length * leaves);
  for (let i = 0; i < blobs.length; i++) {
    const [bx, by, br] = blobs[i], k = i < shown ? 1 : Math.max(0, leaves * blobs.length - i);
    if (k <= 0) continue;
    g += `<circle cx="${ff(bx)}" cy="${ff(by)}" r="${ff(br * (.5 + .5 * k))}" fill="${o.gold ? '#F5B700' : '#2E9E4F'}" stroke="${INK}" stroke-width="${OUT}"/>`;
  }
  for (let i = 0; i < blobs.length; i++) { const [bx, by, br] = blobs[i]; if (i >= shown) continue;
    g += `<circle cx="${ff(bx - br * .25)}" cy="${ff(by - br * .3)}" r="${ff(br * .45)}" fill="${o.gold ? '#FFE066' : '#46C266'}"/>`; }
  for (let i = 0; i < coins; i++) { const a = i * 2.39996, rr = R * .65 * Math.sqrt((i + .5) / Math.max(coins, 1));
    const cx = Math.cos(a) * rr * 1.1 + sw * 1.2, cyy = cy + Math.sin(a) * rr * .7;
    g += `<circle cx="${ff(cx)}" cy="${ff(cyy)}" r="${ff(12 + 10 * size)}" fill="#FFD23F" stroke="${INK}" stroke-width="4"/><text x="${ff(cx)}" y="${ff(cyy + 7 + 3 * size)}" text-anchor="middle" font-size="${ff(16 + 10 * size)}" fill="#A16207" font-family="P" font-weight="900">$</text>`; }
  return `<g transform="translate(${ff(x)} ${ff(y)})"><ellipse cx="0" cy="4" rx="${ff(40 + 160 * size)}" ry="${ff(10 + 18 * size)}" fill="#000" opacity=".15"/>${g}</g>`;
}

// Cookie jar "Fort Cookie" with bills; mouse inside optional.
function jar(o) {
  const { x, y, s = 1, bills = 10, label = 'FORT COOKIE', glow = 0 } = o; let g = '';
  g += `<path d="M-110 -250 Q-140 -230 -140 -180 L-140 -40 Q-140 0 -100 0 L100 0 Q140 0 140 -40 L140 -180 Q140 -230 110 -250Z" fill="#DDF3FF" fill-opacity=".55" stroke="${INK}" stroke-width="6"/>`;
  for (let i = 0; i < bills; i++) g += `<rect x="${ff(-95 + (i % 3) * 8)}" y="${ff(-30 - i * 14)}" width="190" height="34" rx="5" fill="${i % 2 ? '#86C98B' : '#9BD5A0'}" stroke="#2F6B3A" stroke-width="3" transform="rotate(${ff(Math.sin(i * 3.1) * 5)} 0 ${ff(-14 - i * 14)})"/>`;
  g += `<path d="M-110 -250 Q-140 -230 -140 -180 L-140 -40 Q-140 0 -100 0 L100 0 Q140 0 140 -40 L140 -180 Q140 -230 110 -250Z" fill="none" stroke="${INK}" stroke-width="6"/>`;
  g += `<path d="M-115 -205 Q-120 -120 -112 -50" stroke="#fff" stroke-width="10" opacity=".7" fill="none" stroke-linecap="round"/>`;
  g += `<rect x="-120" y="-292" width="240" height="46" rx="14" fill="#D97706" stroke="${INK}" stroke-width="6"/><rect x="-40" y="-312" width="80" height="24" rx="10" fill="#B45309" stroke="${INK}" stroke-width="5"/>`;
  if (label) g += `<g transform="rotate(-4)"><rect x="-100" y="-175" width="200" height="54" rx="10" fill="#FFF7E6" stroke="${INK}" stroke-width="4"/><text x="0" y="-138" text-anchor="middle" font-size="25" fill="#7C2D12" font-family="P" font-weight="900">${label}</text></g>`;
  if (glow) g = `<circle cx="0" cy="-150" r="220" fill="#FFE58A" opacity="${ff(glow * .5)}" filter="url(#soft)"/>` + g;
  return `<g transform="translate(${ff(x)} ${ff(y)}) scale(${ff(s)})">${g}</g>`;
}

// Storm cloud with rain and lightning. k = intensity 0..1
function storm(o) {
  const { x, y, w = 900, k = 1, t = 0, bolt = false } = o; if (k <= 0) return '';
  let g = '';
  for (let i = 0; i < 40 * k; i++) { const rx = x - w / 2 + ((i * 97 + t * 900) % w), ry = y + 60 + ((i * 53 + t * 1400) % 700);
    g += `<line x1="${ff(rx)}" y1="${ff(ry)}" x2="${ff(rx - 14)}" y2="${ff(ry + 46)}" stroke="#93C5FD" stroke-width="5" opacity=".7" stroke-linecap="round"/>`; }
  for (let i = 0; i < 7; i++) { const cx = x - w / 2 + w * (i + .5) / 7 + Math.sin(t * .8 + i) * 20, r = 90 + 40 * Math.sin(i * 2.1);
    g += `<circle cx="${ff(cx)}" cy="${ff(y + Math.sin(i * 1.7) * 26)}" r="${ff(r)}" fill="#4B5563" stroke="${INK}" stroke-width="${OUT}"/>`; }
  for (let i = 0; i < 7; i++) { const cx = x - w / 2 + w * (i + .5) / 7 + Math.sin(t * .8 + i) * 20, r = 90 + 40 * Math.sin(i * 2.1);
    g += `<circle cx="${ff(cx)}" cy="${ff(y + Math.sin(i * 1.7) * 26)}" r="${ff(r - 6)}" fill="#6B7280"/><circle cx="${ff(cx - r * .25)}" cy="${ff(y - r * .3)}" r="${ff(r * .45)}" fill="#7C8594"/>`; }
  if (bolt) g += `<path d="M${x + 60} ${y + 70} L${x - 10} ${y + 260} L${x + 50} ${y + 250} L${x - 40} ${y + 470} L${x + 110} ${y + 220} L${x + 40} ${y + 230} L${x + 100} ${y + 70}Z" fill="#FDE047" stroke="#fff" stroke-width="8"/>`;
  return `<g opacity="${ff(Math.min(1, k * 1.5))}">${g}</g>`;
}

// Shopping cart with groceries; fill 0..1 shrinks the pile; s scale
function cart(o) {
  const { x, y, s = 1, fill = 1 } = o; let g = '';
  const items = [['#FDE68A', -90, 'bread'], ['#F87171', -40, 'apple'], ['#FFFFFF', 10, 'milk'], ['#86EFAC', 60, 'veg'], ['#FCA5A5', -65, 'meat'], ['#FDBA74', 35, 'box'], ['#C4B5FD', -15, 'cereal'], ['#FEF08A', 80, 'banana']];
  const n = Math.round(items.length * fill);
  for (let i = 0; i < n; i++) { const [c, dx] = items[i], row = i < 4 ? 0 : 1;
    g += `<rect x="${dx - 28}" y="${-190 - row * 60}" width="56" height="${70 + (i % 3) * 14}" rx="10" fill="${c}" stroke="${INK}" stroke-width="5"/>`; }
  g += `<path d="M-150 -170 L150 -170 L120 -40 L-120 -40Z" fill="#CBD5E1" fill-opacity=".55" stroke="${INK}" stroke-width="7" stroke-linejoin="round"/>`;
  for (let i = -2; i <= 2; i++) g += `<line x1="${i * 55}" y1="-170" x2="${i * 46}" y2="-40" stroke="${INK}" stroke-width="3"/>`;
  g += `<path d="M150 -170 L190 -230 L225 -230" stroke="${INK}" stroke-width="9" fill="none" stroke-linecap="round"/><line x1="-120" y1="-40" x2="-130" y2="-12" stroke="${INK}" stroke-width="7"/>`;
  g += `<circle cx="-95" cy="-6" r="20" fill="#334155" stroke="${INK}" stroke-width="5"/><circle cx="95" cy="-6" r="20" fill="#334155" stroke="${INK}" stroke-width="5"/>`;
  return `<g transform="translate(${ff(x)} ${ff(y)}) scale(${ff(s)})">${g}</g>`;
}

// Envelope; open 0..1
function envelope(o) {
  const { x, y, s = 1, rot = 0, open = 0, label = '$1,000' } = o;
  return `<g transform="translate(${ff(x)} ${ff(y)}) rotate(${ff(rot)}) scale(${ff(s)})">` +
    (open > 0 ? `<g transform="translate(0 ${ff(-open * 80)})"><rect x="-80" y="-60" width="160" height="80" rx="6" fill="#86C98B" stroke="#2F6B3A" stroke-width="4"/><text x="0" y="-8" text-anchor="middle" font-size="34" fill="#14532D" font-family="P" font-weight="900">${label}</text></g>` : '') +
    `<rect x="-100" y="-55" width="200" height="120" rx="10" fill="#FEF3C7" stroke="${INK}" stroke-width="5"/>` +
    `<path d="M-100 -55 L0 ${ff(15 - open * 90)} L100 -55" fill="#FDE68A" stroke="${INK}" stroke-width="5" stroke-linejoin="round"/></g>`;
}

// Speech bubble
function bubble(o) {
  const { x, y, text, size = 44, k = 1, tail = 'left', color = '#fff', tcol = INK } = o; if (k <= 0) return '';
  MC0.font = `900 ${size}px P`; const w = MC0.measureText(text).width + size * 1.1, h = size * 1.7;
  const tx = tail === 'left' ? -w * .3 : w * .3;
  return `<g transform="translate(${ff(x)} ${ff(y)}) scale(${ff(k)})" filter="url(#sh)"><path d="M${ff(tx - 20)} ${ff(h / 2 - 4)} L${ff(tx - (tail === 'left' ? 50 : -50))} ${ff(h / 2 + 50)} L${ff(tx + 20)} ${ff(h / 2 - 4)}Z" fill="${color}" stroke="${INK}" stroke-width="5"/>` +
    `<rect x="${ff(-w / 2)}" y="${ff(-h / 2)}" width="${ff(w)}" height="${ff(h)}" rx="${ff(h / 2)}" fill="${color}" stroke="${INK}" stroke-width="5"/><rect x="${ff(tx - 18)}" y="${ff(h / 2 - 10)}" width="36" height="12" fill="${color}"/>` +
    `<text x="0" y="${ff(size * .36)}" text-anchor="middle" font-size="${size}" fill="${tcol}" font-family="P" font-weight="900">${text}</text></g>`;
}
const MC0 = document.createElement('canvas').getContext('2d');

// Axe
function axe(o) { const { x, y, rot = 0, s = 1 } = o;
  return `<g transform="translate(${ff(x)} ${ff(y)}) rotate(${ff(rot)}) scale(${ff(s)})"><rect x="-8" y="-170" width="16" height="190" rx="6" fill="#A16207" stroke="${INK}" stroke-width="4"/><path d="M8 -170 Q70 -180 78 -120 Q40 -128 8 -110Z" fill="#CBD5E1" stroke="${INK}" stroke-width="5"/></g>`; }

// Old gadgets box (Mia's junk)
function gadgets(o) { const { x, y, s = 1, t = 0, beep = 0 } = o;
  return `<g transform="translate(${ff(x)} ${ff(y)}) scale(${ff(s)})">` +
    `<rect x="-50" y="-205" width="100" height="70" rx="10" fill="#1F2937" stroke="${INK}" stroke-width="5" transform="rotate(-8)"/><rect x="-40" y="-197" width="80" height="50" rx="6" fill="${beep > 0 && Math.sin(t * 30) > 0 ? '#A3E635' : '#4B5563'}" transform="rotate(-8)"/>` +
    `<ellipse cx="80" cy="-180" rx="34" ry="44" fill="#F472B6" stroke="${INK}" stroke-width="5"/><rect x="70" y="-196" width="20" height="24" fill="#BEF264" stroke="${INK}" stroke-width="3"/>` +
    `<path d="M-120 -175 q30 -40 70 -10 l10 20 l-90 6z" fill="#F8FAFC" stroke="${INK}" stroke-width="5"/><circle cx="-100" cy="-150" r="6" fill="#F43F5E"/><circle cx="-80" cy="-150" r="6" fill="#22D3EE"/>` +
    `<rect x="-150" y="-140" width="300" height="140" rx="10" fill="#C08A5B" stroke="${INK}" stroke-width="6"/><path d="M-150 -140 L-190 -175 L-110 -175 L-80 -140Z" fill="#D9A374" stroke="${INK}" stroke-width="5"/><path d="M150 -140 L190 -175 L110 -175 L80 -140Z" fill="#D9A374" stroke="${INK}" stroke-width="5"/>` +
    `<text x="0" y="-55" text-anchor="middle" font-size="34" fill="#6B3E1E" font-family="P" font-weight="900">MIA'S STUFF</text></g>`; }

// Phone (old flip phone) ringing
function phone(o) { const { x, y, s = 1, t = 0, ring = 0 } = o, w = ring ? Math.sin(t * 40) * 8 : 0;
  return `<g transform="translate(${ff(x)} ${ff(y)}) rotate(${ff(w)}) scale(${ff(s)})"><rect x="-40" y="-90" width="80" height="170" rx="14" fill="#334155" stroke="${INK}" stroke-width="5"/><rect x="-28" y="-74" width="56" height="60" rx="6" fill="#A7F3D0"/>` +
    (ring ? `<path d="M55 -70 q20 20 0 40 M75 -85 q35 35 0 70 M-55 -70 q-20 20 0 40 M-75 -85 q-35 35 0 70" stroke="#FDE047" stroke-width="8" fill="none" stroke-linecap="round"/>` : '') + `</g>`; }

// Hot chocolate mug with steam
function cocoa(o) { const { x, y, s = 1, t = 0 } = o; let g = '';
  for (let i = 0; i < 3; i++) { const w = Math.sin(t * 3 + i * 2) * 10; g += `<path d="M${-25 + i * 25} -70 q${ff(w)} -25 0 -50 q${ff(-w)} -25 0 -50" stroke="#fff" stroke-width="8" fill="none" opacity=".8" stroke-linecap="round"/>`; }
  return `<g transform="translate(${ff(x)} ${ff(y)}) scale(${ff(s)})">${g}<path d="M60 -50 q45 0 45 30 q0 30 -45 30" stroke="${INK}" stroke-width="22" fill="none"/><path d="M60 -50 q45 0 45 30 q0 30 -45 30" stroke="#EF4444" stroke-width="12" fill="none"/><rect x="-65" y="-70" width="130" height="110" rx="18" fill="#EF4444" stroke="${INK}" stroke-width="5"/><ellipse cx="0" cy="-66" rx="58" ry="12" fill="#7C2D12"/></g>`; }

// Big scoreboard with three rows {name, value text, color}
function scoreboard(o) { const { x, y, rows, k = 1 } = o; let g = `<rect x="-420" y="-260" width="840" height="520" rx="30" fill="#1E293B" stroke="${INK}" stroke-width="8"/><rect x="-400" y="-240" width="800" height="80" rx="16" fill="#0F172A"/><text x="0" y="-182" text-anchor="middle" font-size="52" fill="#FDE047" font-family="P" font-weight="900">GRANDPA'S SCOREBOARD</text>`;
  rows.forEach((r, i) => { if (!r.show) return; const yy = -90 + i * 120;
    g += `<rect x="-390" y="${yy}" width="780" height="100" rx="16" fill="#334155"/><text x="-360" y="${yy + 68}" font-size="54" fill="${r.color}" font-family="P" font-weight="900">${r.name}</text><text x="360" y="${yy + 68}" text-anchor="end" font-size="58" fill="#fff" font-family="P" font-weight="900">${r.value}</text>`; });
  return `<g transform="translate(${ff(x)} ${ff(y)}) scale(${ff(k)})" filter="url(#sh)">${g}</g>`; }

// ---------------------------------------------------------------- story #2 cast & props ---
Object.assign(CAST, {
  jay: o => person(Object.assign({ h: 560, skin: '#D9A27A', hair: '#1a120b', hairStyle: 'short', shirt: '#EF4444', pants: '#111827', shoes: '#F8FAFC',
    extra: o.shades ? (hr, hy) => `<rect x="${ff(-hr * .7)}" y="${ff(hy - hr * .3)}" width="${ff(hr * 1.4)}" height="${ff(hr * .38)}" rx="${ff(hr * .15)}" fill="#111"/>` : undefined }, o)),
  sam: o => person(Object.assign({ h: 555, skin: '#F3D0B0', hair: '#6B4226', hairStyle: 'short', shirt: '#5B7DB1', pants: '#A8865B', shoes: '#4B5563', glasses: true }, o)),
  ava: o => person(Object.assign({ h: 535, skin: '#C68B5E', hair: '#2b1608', hairStyle: 'pony', shirt: '#8B5CF6', pants: '#1F2937', shoes: '#F59E0B' }, o)),
  hank: o => person(Object.assign({ h: 560, skin: '#F1C7A3', hair: '#9CA3AF', hairStyle: 'bald', shirt: '#F1F5F9', pants: '#475569', shoes: '#3f2a1a', glasses: true,
    extra: (hr, hy) => `<path d="M0 ${ff(hy + hr * 1.05)} l${ff(hr * .14)} ${ff(hr * .2)} l-${ff(hr * .1)} ${ff(hr * 1.3)} l-${ff(hr * .08)} ${ff(hr * .2)} l-${ff(hr * .08)} -${ff(hr * .2)} l-${ff(hr * .1)} -${ff(hr * 1.3)}z" fill="#B91C1C" stroke="${INK}" stroke-width="3"/>` }, o)),
});
// red sports car / beige sedan. kind: 'red'|'sedan'; tilt for towing; wheelsSpin
function car(o) {
  const { x, y, s = 1, kind = 'red', t = 0, tilt = 0, flip = false } = o, red = kind === 'red';
  const body = red ? '#E11D48' : '#D6C7A1', dark = red ? '#9F1239' : '#A8956B';
  let g = red
    ? `<path d="M-300 -60 Q-290 -120 -200 -130 L-90 -200 Q60 -215 140 -140 L270 -120 Q320 -110 320 -60 L320 -20 L-300 -20Z" fill="${body}" stroke="${INK}" stroke-width="7" stroke-linejoin="round"/><path d="M-70 -185 L-10 -190 L-10 -135 L-150 -135Z M10 -190 Q80 -190 120 -138 L10 -136Z" fill="#BAE6FD" stroke="${INK}" stroke-width="5"/><path d="M-290 -75 L310 -75" stroke="#fff" stroke-width="10" opacity=".5"/>`
    : `<path d="M-300 -50 L-300 -120 L-200 -125 L-140 -220 L130 -220 L190 -125 L300 -115 L300 -50Z" fill="${body}" stroke="${INK}" stroke-width="7" stroke-linejoin="round"/><path d="M-125 -205 L-10 -205 L-10 -130 L-180 -130Z M10 -205 L120 -205 L170 -130 L10 -130Z" fill="#BAE6FD" stroke="${INK}" stroke-width="5"/><circle cx="-60" cy="-95" r="14" fill="#8B5A2B" opacity=".6"/><circle cx="150" cy="-80" r="20" fill="#8B5A2B" opacity=".5"/>`;
  g += `<rect x="-300" y="-55" width="620" height="40" rx="10" fill="${dark}" stroke="${INK}" stroke-width="6"/>`;
  for (const wx of [-170, 190]) { const sp = t * 400 % 360;
    g += `<circle cx="${wx}" cy="-10" r="62" fill="#1F2937" stroke="${INK}" stroke-width="6"/>` + (red || wx < 0 ? `<g transform="rotate(${ff(sp)} ${wx} -10)"><circle cx="${wx}" cy="-10" r="34" fill="#CBD5E1" stroke="${INK}" stroke-width="4"/><path d="M${wx - 30} -10 L${wx + 30} -10 M${wx} -40 L${wx} 20" stroke="${INK}" stroke-width="5"/></g>` : `<circle cx="${wx}" cy="-10" r="20" fill="#6B7280"/>`); }
  return `<g transform="translate(${ff(x)} ${ff(y)}) rotate(${ff(tilt)}) scale(${ff((flip ? -1 : 1) * s)} ${ff(s)})"><ellipse cx="0" cy="40" rx="330" ry="20" fill="#000" opacity=".18"/>${g}</g>`;
}
function towtruck(o) { const { x, y, s = 1, t = 0 } = o;
  return `<g transform="translate(${ff(x)} ${ff(y)}) scale(${ff(s)})"><rect x="-40" y="-170" width="380" height="140" rx="12" fill="#F59E0B" stroke="${INK}" stroke-width="7"/><rect x="200" y="-260" width="150" height="110" rx="12" fill="#F59E0B" stroke="${INK}" stroke-width="7"/><rect x="225" y="-240" width="100" height="60" fill="#BAE6FD" stroke="${INK}" stroke-width="5"/>` +
    `<path d="M0 -170 L-160 -250 L-230 -140" stroke="#334155" stroke-width="14" fill="none"/><circle cx="${ff(Math.sin(t * 20) * 2 + 40)}" cy="-260" r="16" fill="#FDE047" stroke="${INK}" stroke-width="4"/><circle cx="40" cy="-20" r="50" fill="#1F2937" stroke="${INK}" stroke-width="6"/><circle cx="270" cy="-20" r="50" fill="#1F2937" stroke="${INK}" stroke-width="6"/>` +
    `<text x="130" y="-85" text-anchor="middle" font-size="40" fill="#7C2D12" font-family="P" font-weight="900">TOW</text></g>`; }
function couch(o) { const { x, y, s = 1 } = o;
  return `<g transform="translate(${ff(x)} ${ff(y)}) scale(${ff(s)})"><rect x="-330" y="-230" width="660" height="150" rx="40" fill="#0EA5E9" stroke="${INK}" stroke-width="7"/><rect x="-360" y="-130" width="720" height="110" rx="30" fill="#38BDF8" stroke="${INK}" stroke-width="7"/><rect x="-380" y="-200" width="80" height="180" rx="30" fill="#0284C7" stroke="${INK}" stroke-width="7"/><rect x="300" y="-200" width="80" height="180" rx="30" fill="#0284C7" stroke="${INK}" stroke-width="7"/><rect x="-330" y="-20" width="20" height="30" fill="${INK}"/><rect x="310" y="-20" width="20" height="30" fill="${INK}"/></g>`; }
function laptop(o) { const { x, y, s = 1, screen = '', k = 1 } = o;
  return `<g transform="translate(${ff(x)} ${ff(y)}) scale(${ff(s * k)})" filter="url(#sh)"><rect x="-300" y="-380" width="600" height="380" rx="20" fill="#1E293B" stroke="${INK}" stroke-width="8"/><rect x="-270" y="-350" width="540" height="320" rx="8" fill="#F8FAFC"/>${screen}<path d="M-360 0 L360 0 L320 40 L-320 40Z" fill="#94A3B8" stroke="${INK}" stroke-width="7"/></g>`; }
function form(o) { const { x, y, s = 1, rot = 0, checked = 0, crumple = 0, title = '401(k) ENROLLMENT' } = o;
  const sk = 1 - crumple * .6;
  return `<g transform="translate(${ff(x)} ${ff(y)}) rotate(${ff(rot + crumple * 40)}) scale(${ff(s * sk)})" filter="url(#sh)"><rect x="-170" y="-220" width="340" height="440" rx="8" fill="#fff" stroke="${INK}" stroke-width="5"/>` +
    `<text x="0" y="-170" text-anchor="middle" font-size="30" fill="${INK}" font-family="P" font-weight="900">${title}</text>` + [0, 1, 2, 3].map(i => `<rect x="-130" y="${-130 + i * 40}" width="${200 + (i % 2) * 50}" height="12" rx="6" fill="#CBD5E1"/>`).join('') +
    `<rect x="-130" y="40" width="64" height="64" rx="8" fill="#fff" stroke="${INK}" stroke-width="6"/>` + (checked > 0 ? `<path d="M-120 72 L-102 ${ff(72 + 20 * Math.min(1, checked * 2))} L${ff(-102 + 40 * Math.max(0, checked * 2 - 1))} ${ff(92 - 50 * Math.max(0, checked * 2 - 1))}" stroke="#16A34A" stroke-width="12" fill="none" stroke-linecap="round"/>` : '') +
    `<text x="-50" y="85" font-size="26" fill="${INK}" font-family="P" font-weight="900">YES, MATCH ME</text>` + (crumple > 0 ? `<path d="M-170 -220 L170 220 M170 -220 L-170 220" stroke="#94A3B8" stroke-width="4" opacity="${ff(crumple)}"/>` : '') + `</g>`; }
function stringLights(t, y = 130) { let g = `<path d="M0 ${y} Q480 ${y + 90} 960 ${y} Q1440 ${y + 90} 1920 ${y}" stroke="${INK}" stroke-width="4" fill="none"/>`;
  for (let i = 0; i < 24; i++) { const x = 40 + i * 80, q = (x % 960) / 960, yy = y + Math.sin(q * Math.PI) * 45 + 10, on = Math.sin(t * 3 + i) > -.3;
    g += `<circle cx="${x}" cy="${ff(yy)}" r="13" fill="${['#FDE047', '#F472B6', '#60A5FA', '#4ADE80'][i % 4]}" opacity="${on ? 1 : .5}" stroke="${INK}" stroke-width="3"/>`; } return g; }
function door(o) { const { x, y, s = 1, open = 0 } = o;
  return `<g transform="translate(${ff(x)} ${ff(y)}) scale(${ff(s)})"><rect x="-150" y="-560" width="300" height="560" fill="#7C2D12" stroke="${INK}" stroke-width="8"/><rect x="-130" y="-540" width="${ff(260 * (1 - open * .8))}" height="540" fill="#9A3412" stroke="${INK}" stroke-width="6"/><circle cx="${ff(90 - open * 200)}" cy="-280" r="12" fill="#FDE047"/><rect x="-210" y="-20" width="420" height="30" fill="#A8A29E" stroke="${INK}" stroke-width="5"/></g>`; }
function phonePost(o) { const { x, y, s = 1, place = 'CANCUN', likes = 0, bg = '#38BDF8', rot = 0 } = o;
  return `<g transform="translate(${ff(x)} ${ff(y)}) rotate(${ff(rot)}) scale(${ff(s)})" filter="url(#sh)"><rect x="-150" y="-280" width="300" height="560" rx="36" fill="#111827" stroke="${INK}" stroke-width="6"/><rect x="-130" y="-250" width="260" height="300" rx="10" fill="${bg}"/><circle cx="60" cy="-180" r="40" fill="#FDE047"/><path d="M-130 20 Q-40 -60 50 0 Q100 30 130 -10 L130 50 L-130 50Z" fill="#FDE68A"/>` +
    `<text x="0" y="110" text-anchor="middle" font-size="34" fill="#fff" font-family="P" font-weight="900">${place}</text><text x="0" y="170" text-anchor="middle" font-size="30" fill="#F472B6" font-family="P" font-weight="900">♥ ${likes.toLocaleString('en-US')}</text></g>`; }

// ---------------------------------------------------------------- story #3 cast & props ---
Object.assign(CAST, {
  walter: o => person(Object.assign({ h: 560, skin: '#EBC3A0', hair: '#D1D5DB', hairStyle: 'bald', shirt: '#7C5A3A', pants: '#4B5563', shoes: '#3f2a1a', glasses: true, beard: false,
    extra: (hr, hy) => `<path d="M${ff(-hr * 1.05)} ${ff(hy - hr * .55)} Q0 ${ff(hy - hr * 1.45)} ${ff(hr * 1.05)} ${ff(hy - hr * .55)} L${ff(hr * 1.3)} ${ff(hy - hr * .45)} L${ff(-hr * 1.05)} ${ff(hy - hr * .45)}Z" fill="#57534E" stroke="${INK}" stroke-width="4"/>` +
      [0, 1, 2].map(i => `<path d="M${ff(-hr * .5 + i * hr * .45)} ${ff(hy + hr * 1.9 + i * hr * .5)} l${ff(hr * .22)} 0 a${ff(hr * .06)} ${ff(hr * .06)} 0 0 1 0 ${ff(hr * .12)} l-${ff(hr * .22)} 0" stroke="#CBD5E1" stroke-width="4" fill="none"/>`).join('') }, o)),
  lily: o => person(Object.assign({ h: 540, skin: '#F1C6A3', hair: '#B45309', hairStyle: 'pony', shirt: '#10B981', pants: '#1E3A8A', shoes: '#F43F5E' }, o)),
  derek: o => person(Object.assign({ h: 570, skin: '#E9B994', hair: '#111827', hairStyle: 'short', shirt: '#7E22CE', pants: '#581C87', shoes: '#111827',
    extra: (hr, hy) => `<path d="M${ff(-hr * .9)} ${ff(hy - hr * .7)} q${ff(hr * .9)} ${ff(-hr * .7)} ${ff(hr * 1.9)} ${ff(-hr * .05)}" stroke="#111827" stroke-width="${ff(hr * .22)}" fill="none" stroke-linecap="round"/><path d="M${ff(-hr * .25)} ${ff(hy + hr * .58)} q${ff(hr * .25)} ${ff(hr * .1)} ${ff(hr * .5)} 0" stroke="${INK}" stroke-width="3" fill="none"/>` }, o)),
  kowalski: o => person(Object.assign({ h: 540, skin: '#C9926B', hair: '#3f2a1a', hairStyle: 'curly', shirt: '#475569', pants: '#334155', shoes: '#111827', glasses: true }, o)),
});
// safe-deposit box: open 0..1, glow 0..1 (loot reveal: charge -> burst handled by the scene)
function safebox(o) { const { x, y, s = 1, open = 0, glow = 0, t = 0 } = o;
  let g = glow > 0 ? `<circle cx="0" cy="-120" r="${ff(260 + glow * 80)}" fill="#FFE58A" opacity="${ff(glow * .6)}" filter="url(#soft)"/>` + [0, 1, 2, 3, 4, 5].map(i => { const a = -Math.PI / 2 + (i - 2.5) * .35 + Math.sin(t) * .05; return `<path d="M0 -120 L${ff(Math.cos(a - .08) * 700)} ${ff(-120 + Math.sin(a - .08) * 700)} L${ff(Math.cos(a + .08) * 700)} ${ff(-120 + Math.sin(a + .08) * 700)}Z" fill="#FFF3A0" opacity="${ff(glow * .35)}"/>`; }).join('') : '';
  g += `<rect x="-240" y="-200" width="480" height="200" rx="18" fill="#94A3B8" stroke="${INK}" stroke-width="7"/><rect x="-220" y="-180" width="440" height="160" rx="10" fill="#64748B"/>`;
  g += `<g transform="translate(0 -200) rotate(${ff(-open * 70)} -240 0)"><rect x="-240" y="-60" width="480" height="60" rx="14" fill="#CBD5E1" stroke="${INK}" stroke-width="7"/><rect x="-30" y="-38" width="60" height="22" rx="6" fill="#FDE047" stroke="${INK}" stroke-width="4"/></g>`;
  return `<g transform="translate(${ff(x)} ${ff(y)}) scale(${ff(s)})" filter="url(#sh)">${g}</g>`; }
function newspaper(o) { const { x, y, s = 1, rot = 0, crack = 0 } = o;
  return `<g transform="translate(${ff(x)} ${ff(y)}) rotate(${ff(rot)}) scale(${ff(s)})" filter="url(#sh)"><rect x="-300" y="-380" width="600" height="760" fill="#F5EBD0" stroke="${INK}" stroke-width="6"/>` +
    `<text x="0" y="-320" text-anchor="middle" font-size="40" fill="#44403C" font-family="A" style="font-family:A">THE DAILY LEDGER · OCT 20, 1987</text><line x1="-270" y1="-300" x2="270" y2="-300" stroke="#44403C" stroke-width="4"/>` +
    `<text x="0" y="-200" text-anchor="middle" font-size="104" fill="#111" font-family="A" style="font-family:A">STOCKS</text><text x="0" y="-90" text-anchor="middle" font-size="104" fill="#B91C1C" font-family="A" style="font-family:A">CRASH</text>` +
    `<text x="0" y="-20" text-anchor="middle" font-size="44" fill="#111" font-family="A" style="font-family:A">WORST DAY IN HISTORY: -20.5%</text>` + [0, 1, 2, 3, 4, 5, 6].map(i => `<rect x="-270" y="${30 + i * 44}" width="${250 + (i % 3) * 20}" height="14" fill="#A8A29E"/><rect x="20" y="${30 + i * 44}" width="${230 - (i % 2) * 30}" height="14" fill="#A8A29E"/>`).join('') +
    (crack > 0 ? `<path d="M-300 -150 L-120 -120 L-60 -40 L80 -70 L170 20 L300 0" stroke="#111" stroke-width="${ff(6 * crack)}" fill="none"/>` : '') + `</g>`; }
function envelopes(o) { const { x, y, s = 1, n = 30 } = o; let g = '';
  for (let i = 0; i < n; i++) g += `<g transform="translate(${ff(Math.sin(i * 2.3) * 14)} ${-i * 9}) rotate(${ff(Math.sin(i * 1.7) * 4)})"><rect x="-120" y="-40" width="240" height="80" rx="6" fill="${i % 2 ? '#FEF3C7' : '#FDE68A'}" stroke="${INK}" stroke-width="3"/><path d="M-120 -40 L0 10 L120 -40" fill="none" stroke="${INK}" stroke-width="3"/></g>`;
  return `<g transform="translate(${ff(x)} ${ff(y)}) scale(${ff(s)})" filter="url(#sh)">${g}</g>`; }
function card(o) { const { x, y, s = 1, open = 0, rot = 0 } = o;
  return `<g transform="translate(${ff(x)} ${ff(y)}) rotate(${ff(rot)}) scale(${ff(s)})" filter="url(#sh)"><rect x="-220" y="-160" width="440" height="320" rx="14" fill="#FBCFE8" stroke="${INK}" stroke-width="6"/>` +
    `<text x="0" y="-60" text-anchor="middle" font-size="48" fill="#9D174D" font-family="P" font-weight="900">FOR LILY</text><text x="0" y="0" text-anchor="middle" font-size="32" fill="#9D174D" font-family="P" font-weight="700">June 1, 1998</text>` +
    `<path d="M-40 70 C-80 40 -60 0 0 30 C60 0 80 40 40 70 L0 110Z" fill="#F43F5E" stroke="${INK}" stroke-width="4" transform="scale(.7) translate(0 60)"/></g>`; }
function soup(o) { const { x, y, s = 1, t = 0 } = o;
  return `<g transform="translate(${ff(x)} ${ff(y)}) scale(${ff(s)})">${[0, 1, 2].map(i => `<path d="M${-30 + i * 30} -50 q${ff(Math.sin(t * 3 + i) * 10)} -25 0 -50" stroke="#fff" stroke-width="7" fill="none" opacity=".8"/>`).join('')}<path d="M-90 -40 L90 -40 Q80 40 0 45 Q-80 40 -90 -40Z" fill="#F97316" stroke="${INK}" stroke-width="6"/><ellipse cx="0" cy="-40" rx="90" ry="16" fill="#FDBA74" stroke="${INK}" stroke-width="5"/></g>`; }
function gavel(o) { const { x, y, s = 1, hit = 0 } = o;
  return `<g transform="translate(${ff(x)} ${ff(y)}) scale(${ff(s)})"><g transform="rotate(${ff(-35 + hit * 35)} 60 0)"><rect x="-20" y="-120" width="40" height="160" rx="10" fill="#92400E" stroke="${INK}" stroke-width="5" transform="rotate(-90 0 0) translate(40 -60)"/><rect x="-70" y="-60" width="140" height="70" rx="14" fill="#B45309" stroke="${INK}" stroke-width="6"/></g><rect x="-90" y="40" width="180" height="30" rx="8" fill="#78350F" stroke="${INK}" stroke-width="5"/></g>`; }
