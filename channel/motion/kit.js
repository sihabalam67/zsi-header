// Coin Theory motion kit: the craft rules from STYLE_PLAYBOOK.md section 4 as small pure functions of time.
// Load in a frame(t) page with <script src="../motion/kit.js"></script>; everything lives on window.MK.
// Every function is deterministic: same t in, same picture out (no timers, no unseeded random).
(function () {
  const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
  const seg = (t, a, b) => clamp((t - a) / (b - a));
  const lerp = (a, b, k) => a + (b - a) * k;

  // Critically damped spring step response, 0 -> 1, never overshoots. w = 12 (soft) ... 40 (snappy).
  const spring = (t, w = 18) => (t <= 0 ? 0 : 1 - (1 + w * t) * Math.exp(-w * t));
  // Under-damped spring with a small overshoot (for Penny / playful objects). zeta 0.5-0.8.
  const springBounce = (t, w = 16, zeta = 0.6) => {
    if (t <= 0) return 0;
    const wd = w * Math.sqrt(1 - zeta * zeta);
    return 1 - Math.exp(-zeta * w * t) * (Math.cos(wd * t) + (zeta * w / wd) * Math.sin(wd * t));
  };
  // A value that changes target several times: keys = [[t0, v0], [t1, v1], ...]. Sum of one spring per change.
  const springTo = (t, keys, w = 18, fn = spring) => {
    let v = keys[0][1];
    for (let i = 1; i < keys.length; i++) v += (keys[i][1] - keys[i - 1][1]) * fn(t - keys[i][0], w);
    return v;
  };

  // 120 BPM beat grid. beatT(n) is when beat n lands; moves should start LEAD seconds early.
  const BPM = 120, LEAD = 0.05;
  const beatT = (n, bpm = BPM) => n * 60 / bpm;
  const onBeat = (t, n, w = 18, bpm = BPM) => spring(t - beatT(n, bpm) + LEAD, w);

  // Slow push-in so a hold is never dead: scale 1.00 -> 1.05 over a scene.
  const pushIn = (t, t0, t1, amount = 0.05) => 1 + amount * seg(t, t0, t1);
  // Punch-in on a beat: 1.0 -> 1.08 -> settles back to 1.03.
  const punch = (t, at) => { const k = t - at; return k < 0 ? 1 : 1 + 0.08 * Math.exp(-k * 6) * (k < 0.06 ? k / 0.06 : 1) + 0.03 * spring(k, 10); };
  // Hit-stop: time freezes for `dur` after a big hit (feed the result into the scene instead of t).
  const hitStop = (t, at, dur = 0.08) => (t < at ? t : t < at + dur ? at : t - dur);
  // Camera shake that decays (light hits only), seeded and deterministic.
  const shake = (t, at, amp = 8, dur = 0.25) => {
    const k = t - at; if (k < 0 || k > dur) return [0, 0];
    const d = amp * (1 - k / dur);
    return [Math.sin(k * 90 + 1.3) * d, Math.cos(k * 77 + 0.4) * d];
  };
  // Log-space zoom between two scales (powers-of-ten / follow-the-dollar zooms).
  const zoomLog = (k, s0, s1) => Math.exp(lerp(Math.log(s0), Math.log(s1), k));

  // Count-up that rolls while moving, then settles hard on the exact value.
  const countUp = (t, t0, dur, value, fmt = (v) => Math.round(v).toLocaleString('en-US')) => {
    const k = seg(t, t0, t0 + dur);
    const e = 1 - Math.pow(1 - k, 3);
    return k >= 1 ? fmt(value) : fmt(value * e);
  };

  // Seeded hash noise (use instead of Math.random): same (i, seed) -> same number in [0, 1).
  const rand = (i, seed = 1) => { const x = Math.sin(i * 127.1 + seed * 311.7) * 43758.5453; return x - Math.floor(x); };

  // Cubic Bezier point, for coins flying into a balance or a price tag arcing onto a receipt.
  const bez = (p0, p1, p2, p3, k) => {
    const u = 1 - k;
    return [0, 1].map(i => u * u * u * p0[i] + 3 * u * u * k * p1[i] + 3 * u * k * k * p2[i] + k * k * k * p3[i]);
  };
  // n coins leaving `from` at t0 (staggered) and landing in `to`; returns [{x, y, s, landed}] for drawing.
  const coinsTo = (t, t0, from, to, n = 12, flight = 0.7, stagger = 0.06) => {
    const out = [];
    for (let i = 0; i < n; i++) {
      const k = seg(t, t0 + i * stagger, t0 + i * stagger + flight);
      if (k <= 0) continue;
      const lift = 180 + rand(i, 3) * 160, side = (rand(i, 5) - 0.5) * 320;
      const [x, y] = bez(from, [from[0] + side, from[1] - lift], [to[0] - 60, to[1] - lift * 0.6], to, 1 - Math.pow(1 - k, 2));
      out.push({ x, y, s: 1 - 0.4 * k, landed: k >= 1 });
    }
    return out;
  };
  // How many coins have landed by t (use it to bump the balance: scale 1 + 0.06 * bump).
  const landedBump = (t, t0, n = 12, flight = 0.7, stagger = 0.06) => {
    let b = 0;
    for (let i = 0; i < n; i++) { const k = t - (t0 + i * stagger + flight); if (k >= 0) b = Math.max(b, Math.exp(-k * 12)); }
    return b;
  };

  // Three-stroke shockwave (wide/faint, medium, thin/bright) as an SVG string.
  const shockwave = (t, at, x, y, R = 320, color = '#FFD23F') => {
    const k = seg(t, at, at + 0.6); if (k <= 0 || k >= 1) return '';
    const e = 1 - Math.pow(1 - k, 3);
    return [[1.0, 26, 0.18], [0.85, 12, 0.35], [0.7, 4, 0.9]].map(([rs, w, a]) =>
      `<circle cx="${x}" cy="${y}" r="${(R * rs * e).toFixed(1)}" fill="none" stroke="${color}" stroke-width="${(w * (1 - k) + 1).toFixed(1)}" opacity="${(a * (1 - k)).toFixed(2)}"/>`).join('');
  };

  // Text that rises through a mask line, letter by letter (SVG). Needs a clipPath; give each call a unique id.
  const maskRise = (t, t0, id, x, y, text, size, fill, opts = {}) => {
    const { stagger = 0.03, w = 22, anchor = 'middle', weight = 900, family = 'P', cls = '' } = opts;
    const letters = [...text];
    const k = letters.map((_, i) => spring(t - t0 - i * stagger, w));
    if (k.every(v => v <= 0)) return '';
    const spans = letters.map((ch, i) => `<tspan dy="0" style="opacity:${k[i] > 0 ? 1 : 0}">${ch === ' ' ? '&#160;' : ch}</tspan>`).join('');
    const lift = size * (1 - k[Math.floor(letters.length / 2)]);
    return `<defs><clipPath id="${id}"><rect x="-5000" y="${y - size * 1.1}" width="10000" height="${size * 1.35}"/></clipPath></defs>` +
      `<g clip-path="url(#${id})"><text class="${cls}" x="${x}" y="${(y + lift).toFixed(1)}" text-anchor="${anchor}" font-size="${size}" font-weight="${weight}" font-family="${family}" fill="${fill}">${spans}</text></g>`;
  };

  // Film grain overlay (fresh each frame via a seed tied to the frame number). Put it last in the SVG.
  const grain = (t, W, H, amount = 0.06, fps = 30) => {
    const seed = Math.floor(t * fps) % 997;
    return `<filter id="gr${seed}"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="${seed}"/><feColorMatrix values="0 0 0 0 0.5  0 0 0 0 0.45  0 0 0 0 0.4  0 0 0 ${amount * 4} 0"/></filter>` +
      `<rect width="${W}" height="${H}" filter="url(#gr${seed})" style="mix-blend-mode:multiply" pointer-events="none"/>`;
  };
  // Pencil "boil": wobble a polyline's points with a phase that steps 8x per second (hand-drawn feel).
  const boil = (pts, t, amp = 1.6) => {
    const ph = Math.floor(t * 8);
    return pts.map(([x, y], i) => [x + Math.sin(i * 1.7 + ph * 2.3) * amp, y + Math.cos(i * 2.1 + ph * 1.9) * amp]);
  };
  const path = (pts) => 'M' + pts.map(p => p[0].toFixed(1) + ' ' + p[1].toFixed(1)).join(' L');

  // Squash & stretch for a landing at `land`: returns [sx, sy] (volume-preserving).
  const squash = (t, land, amt = 0.22, dur = 0.35) => {
    const k = seg(t, land, land + dur); if (k <= 0 || k >= 1) return [1, 1];
    const s = 1 - amt * Math.exp(-k * 5) * Math.cos(k * 14);
    return [1 / s, s];
  };

  window.MK = { clamp, seg, lerp, spring, springBounce, springTo, BPM, LEAD, beatT, onBeat, pushIn, punch, hitStop, shake,
    zoomLog, countUp, rand, bez, coinsTo, landedBump, shockwave, maskRise, grain, boil, path, squash };
})();
