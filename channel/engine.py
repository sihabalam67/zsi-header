"""Coin Theory video engine: drawing, characters, charts, captions, voice, music, mix.

Episodes import this module, define SCENES, and call `build(...)`.
Everything runs locally with free tools installed by studio/setup.sh.
"""
import math
import os
import random
import subprocess
import sys
from multiprocessing import Pool

import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(ROOT)
STUDIO = os.path.join(REPO, 'studio')
MODELS = os.path.join(STUDIO, 'models')
FONTS = os.path.join(STUDIO, 'assets', 'fonts')
ICONS = os.path.join(STUDIO, 'assets', 'icons', 'lucide')

# Logical canvas is 1280x720; output is 1080p, drawn at 2x and downsampled.
W, H, FPS = 1280, 720, 30
OUT_W, OUT_H = 1920, 1080
K = OUT_W / W * 2
SR = 44100
VOICE = os.environ.get('VOICE', 'af_heart')

# ---------------------------------------------------------------- palette ---
BG1, BG2 = (14, 22, 40), (30, 42, 78)
GOLD, GOLD_D, GOLD_L = (255, 196, 61), (196, 132, 18), (255, 226, 140)
MINT, MINT_D = (52, 211, 153), (14, 140, 98)
CORAL, CORAL_D = (248, 113, 113), (178, 52, 60)
SKY, SKY_D = (96, 165, 250), (37, 99, 200)
CREAM, INK, MUTED = (250, 245, 235), (17, 20, 35), (148, 163, 184)
BILL, BILL_D = (134, 190, 120), (62, 120, 70)
WHITE = (255, 255, 255)

# ---------------------------------------------------------------- easing ---


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def ease_out(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def back_out(x):
    x = clamp(x)
    c = 1.70158
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


def seg(t, a, b):
    return clamp((t - a) / (b - a)) if b != a else float(t >= a)


def lerp(a, b, k):
    return a + (b - a) * k


def mix(c1, c2, k):
    return tuple(int(lerp(a, b, k)) for a, b in zip(c1, c2))


def pop(t, start, dur=0.45):
    """Scale-in factor with overshoot, 0 before start."""
    return back_out(seg(t, start, start + dur))


def fade(t, start, dur=0.4):
    return ease(seg(t, start, start + dur))


# ---------------------------------------------------------------- canvas ---
_fonts, _grad, _icons = {}, {}, {}


def font(size, weight=700, family='Poppins'):
    key = (size, weight, family)
    if key not in _fonts:
        have = sorted(int(f.rsplit('-', 1)[1][:-4]) for f in os.listdir(FONTS) if f.startswith(family + '-'))
        weight = min(have, key=lambda w: abs(w - weight))
        _fonts[key] = ImageFont.truetype(os.path.join(FONTS, f'{family}-{weight}.ttf'), int(size * K))
    return _fonts[key]


def gradient(top, bottom):
    key = (top, bottom)
    if key not in _grad:
        h, w = int(H * K), int(W * K)
        y = np.linspace(0, 1, h)[:, None, None]
        arr = np.array(top) * (1 - y) + np.array(bottom) * y
        _grad[key] = Image.fromarray(np.ascontiguousarray(np.broadcast_to(arr, (h, w, 3)).astype(np.uint8)), 'RGB')
    return _grad[key]


def icon_image(name, color, size, stroke=2.0):
    key = (name, color, int(size * K), stroke)
    if key not in _icons:
        import cairosvg
        from io import BytesIO
        svg = open(os.path.join(ICONS, f'{name}.svg')).read()
        hexc = '#%02x%02x%02x' % color[:3]
        svg = svg.replace('currentColor', hexc).replace('stroke-width="2"', f'stroke-width="{stroke}"')
        png = cairosvg.svg2png(bytestring=svg.encode(), output_width=int(size * K), output_height=int(size * K))
        _icons[key] = Image.open(BytesIO(png)).convert('RGBA')
    return _icons[key]


class Canvas:
    def __init__(self, top=BG1, bottom=BG2):
        self.img = gradient(top, bottom).copy()
        self.d = ImageDraw.Draw(self.img, 'RGBA')
        self.alpha = 1.0

    def _c(self, c, a=1.0):
        if c is None:
            return None
        base = c[3] / 255 if len(c) == 4 else 1.0
        return (c[0], c[1], c[2], int(255 * clamp(base * a * self.alpha)))

    def circle(self, x, y, r, fill=None, outline=None, width=0, a=1.0):
        self.ellipse(x, y, r, r, fill, outline, width, a)

    def ellipse(self, x, y, rx, ry, fill=None, outline=None, width=0, a=1.0):
        if rx <= 0.2 or ry <= 0.2:
            return
        self.d.ellipse([(x - rx) * K, (y - ry) * K, (x + rx) * K, (y + ry) * K],
                       fill=self._c(fill, a), outline=self._c(outline, a), width=int(width * K))

    def poly(self, pts, fill=None, outline=None, width=0, a=1.0):
        p = [(x * K, y * K) for x, y in pts]
        self.d.polygon(p, fill=self._c(fill, a))
        if outline and width:
            self.d.line(p + [p[0], p[1]], fill=self._c(outline, a), width=int(width * K), joint='curve')

    def line(self, pts, fill, width, a=1.0):
        if len(pts) < 2:
            return
        self.d.line([(x * K, y * K) for x, y in pts], fill=self._c(fill, a), width=max(1, int(width * K)),
                    joint='curve')

    def rrect(self, x0, y0, x1, y1, r, fill=None, outline=None, width=0, a=1.0):
        if x1 <= x0 or y1 <= y0:
            return
        r = min(r, (x1 - x0) / 2, (y1 - y0) / 2)
        self.d.rounded_rectangle([x0 * K, y0 * K, x1 * K, y1 * K], radius=r * K, fill=self._c(fill, a),
                                 outline=self._c(outline, a), width=int(width * K))

    def arc(self, x, y, r, start, end, fill, width, a=1.0):
        self.d.arc([(x - r) * K, (y - r) * K, (x + r) * K, (y + r) * K], start, end, fill=self._c(fill, a),
                   width=max(1, int(width * K)))

    def text(self, x, y, s, size, fill=WHITE, weight=700, anchor='mm', a=1.0, shadow=True, family='Poppins',
             stroke=0, stroke_fill=INK):
        f = font(size, weight, family)
        if shadow:
            self.d.text(((x + 2) * K, (y + 3) * K), s, font=f, fill=self._c((0, 0, 0, 110), a), anchor=anchor,
                        stroke_width=int(stroke * K), stroke_fill=self._c((0, 0, 0, 110), a))
        self.d.text((x * K, y * K), s, font=f, fill=self._c(fill, a), anchor=anchor,
                    stroke_width=int(stroke * K), stroke_fill=self._c(stroke_fill, a))

    def icon(self, name, x, y, size, color=WHITE, a=1.0, stroke=2.0):
        a = clamp(a * self.alpha)
        if a <= 0 or size < 2:
            return
        im = icon_image(name, color, size, stroke)
        if a < 1:
            im = im.copy()
            im.putalpha(im.getchannel('A').point(lambda v: int(v * a)))
        self.img.paste(im, (int((x - size / 2) * K), int((y - size / 2) * K)), im)

    def frame(self):
        return self.img.resize((OUT_W, OUT_H), Image.LANCZOS)


# ------------------------------------------------------------- characters ---
def face(c, x, y, r, mood='happy', look=(0, 0), a=1.0, t=0.0, phase=0.0):
    ex, ey, er = r * 0.33, y - r * 0.12, r * 0.17
    lw = max(1.5, r * 0.065)
    blink = math.sin(t * 1.3 + phase * 5) > 0.985
    for sx in (-1, 1):
        cx = x + sx * ex
        if mood == 'shocked':
            c.circle(cx, ey, er * 1.25, WHITE, a=a)
            c.circle(cx + look[0] * er * 0.3, ey + look[1] * er * 0.3, er * 0.45, INK, a=a)
        elif blink or mood == 'sleepy':
            c.line([(cx - er, ey + er * 0.2), (cx + er, ey + er * 0.2)], INK, lw, a)
        else:
            c.circle(cx, ey, er, WHITE, a=a)
            c.circle(cx + look[0] * er * 0.4, ey + look[1] * er * 0.4, er * 0.56, INK, a=a)
        if mood == 'angry':
            c.line([(cx - sx * er * 1.3, ey - er * 1.9), (cx + sx * er * 1.1, ey - er * 1.1)], INK, lw, a)
        elif mood in ('sad', 'worried'):
            c.line([(cx - sx * er * 1.2, ey - er * 1.3), (cx + sx * er * 1.0, ey - er * 2.0)], INK, lw * 0.8, a)
    my, mw = y + r * 0.3, r * 0.26
    if mood in ('happy', 'proud'):
        c.arc(x, my - mw * 0.55, mw, 20, 160, INK, lw, a)
    elif mood == 'shocked':
        c.ellipse(x, my + r * 0.04, mw * 0.45, mw * 0.6, INK, a=a)
    elif mood in ('sad', 'worried', 'sleepy'):
        c.arc(x, my + mw * 0.75, mw * 0.85, 205, 335, INK, lw, a)
    elif mood == 'angry':
        c.line([(x - mw, my), (x + mw, my)], INK, lw, a)
    elif mood == 'talk':
        o = abs(math.sin(t * 11 + phase)) * 0.5 + 0.2
        c.ellipse(x, my, mw * 0.55, mw * o, INK, a=a)


def penny(c, x, y, r, t, mood='happy', look=(0, 0), a=1.0, arms=(30, 150), wave=False, bounce=True,
          scale_y=1.0):
    """Penny, the channel mascot: a friendly gold coin with arms and legs."""
    if r <= 1:
        return
    by = y - (abs(math.sin(t * 3.2)) * r * 0.06 if bounce else 0)
    lw = max(2, r * 0.08)
    for sx in (-1, 1):  # legs
        fx = x + sx * r * 0.32
        c.line([(fx, by + r * 0.85), (fx, y + r * 1.35)], GOLD_D, lw, a)
        c.ellipse(fx + sx * r * 0.08, y + r * 1.4, r * 0.18, r * 0.09, GOLD_D, a=a)
    for i, sx in enumerate((-1, 1)):  # arms
        ang = math.radians(arms[i])
        if wave and i == 1:
            ang = math.radians(-50 + 25 * math.sin(t * 9))
        sx0 = x + sx * r * 0.95
        ex = sx0 + math.cos(ang) * r * 0.65 * (1 if sx > 0 else 1)
        ey = by + math.sin(ang) * r * 0.65
        if sx < 0:
            ex = sx0 - math.cos(math.radians(180 - arms[0])) * r * 0.65
            ey = by + math.sin(math.radians(180 - arms[0])) * r * 0.65
        c.line([(sx0, by), (ex, ey)], GOLD_D, lw, a)
        c.circle(ex, ey, r * 0.12, GOLD_D, a=a)
    ry = r * scale_y
    c.ellipse(x, by, r, ry, GOLD, GOLD_D, max(2, r * 0.09), a)
    c.ellipse(x, by, r * 0.8, ry * 0.8, None, GOLD_L, max(1.5, r * 0.04), a)
    c.ellipse(x - r * 0.4, by - ry * 0.45, r * 0.16, ry * 0.1, (255, 255, 255, 120), a=a)
    face(c, x, by + r * 0.05, r * 0.95, mood, look, a, t)


def person(c, x, y, s, color, t=0.0, phase=0.0, mood='happy', a=1.0):
    """Simple round character; (x, y) is the feet."""
    bob = math.sin(t * 2 + phase) * 2 * s
    c.rrect(x - 30 * s, y - 70 * s + bob, x + 30 * s, y, 26 * s, color, mix(color, INK, 0.35), 3 * s, a)
    c.circle(x, y - 98 * s + bob, 30 * s, mix(color, WHITE, 0.55), mix(color, INK, 0.35), 3 * s, a)
    face(c, x, y - 98 * s + bob, 30 * s, mood, (0, 0), a, t, phase)


def bill(c, x, y, w, amount='100', a=1.0, tint=0.0, rot_skew=0.0):
    """A cartoon banknote centred at (x, y), width w (height is w/2.3)."""
    h = w / 2.3
    if w < 4:
        return
    col, dark = mix(BILL, (120, 130, 130), tint), mix(BILL_D, (70, 80, 80), tint)
    c.rrect(x - w / 2, y - h / 2, x + w / 2, y + h / 2, w * 0.04, col, dark, max(1.5, w * 0.012), a)
    c.rrect(x - w * 0.44, y - h * 0.38, x + w * 0.44, y + h * 0.38, w * 0.03, None, dark, max(1, w * 0.008), a)
    c.circle(x, y, h * 0.3, mix(col, WHITE, 0.25), dark, max(1, w * 0.008), a)
    c.text(x, y + h * 0.02, '$', max(6, int(h * 0.36)), dark, 800 if False else 700, a=a, shadow=False)
    for sx, sy in ((-1, -1), (1, 1)):
        c.text(x + sx * w * 0.36, y + sy * h * 0.26, amount, max(5, int(h * 0.2)), dark, 700, a=a, shadow=False)


def price_tag(c, x, y, s, label, color=GOLD, a=1.0):
    w, h = 120 * s, 54 * s
    pts = [(x - w / 2, y - h / 2), (x + w / 2 - 18 * s, y - h / 2), (x + w / 2, y), (x + w / 2 - 18 * s, y + h / 2),
           (x - w / 2, y + h / 2)]
    c.poly(pts, color, mix(color, INK, 0.4), 3 * s, a)
    c.circle(x + w / 2 - 22 * s, y, 5 * s, INK, a=a)
    c.text(x - 8 * s, y + 1, label, int(24 * s), INK, 700, a=a, shadow=False)


def burst(c, x, y, k, color, n=16, radius=90, seed=0):
    if k <= 0 or k >= 1:
        return
    rnd = random.Random(seed)
    for _ in range(n):
        ang = rnd.random() * 2 * math.pi
        d = ease_out(k) * radius * rnd.uniform(0.5, 1)
        c.circle(x + math.cos(ang) * d, y + math.sin(ang) * d, (1 - k) * rnd.uniform(3, 9), color, a=1 - k)


def specks(c, t, seed=1, n=34, color=WHITE, amax=0.08):
    rnd = random.Random(seed)
    for _ in range(n):
        x0, y0 = rnd.uniform(0, W), rnd.uniform(0, H)
        r, sp, ph, al = rnd.uniform(2, 8), rnd.uniform(4, 16), rnd.uniform(0, 6), rnd.uniform(0.3, 1)
        y = (y0 - t * sp) % (H + 40) - 20
        c.circle(x0 + math.sin(t * 0.5 + ph) * 12, y, r, color, a=amax * al)


def title_card(c, t, start, text, sub=None, y=90):
    k = ease_out(seg(t, start, start + 0.5))
    c.text(W / 2, y - 12 * (1 - k), text, 44, WHITE, 900, a=k)
    if sub:
        c.text(W / 2, y + 42, sub, 22, MUTED, 600, a=fade(t, start + 0.3))


def counter(value, fmt):
    return fmt.format(value)


# ------------------------------------------------------------------ charts --
def line_chart(c, box, xs, ys, xr, yr, k, color=GOLD, a=1.0, xticks=(), yticks=(), yfmt='{:.0f}',
               head_label=None, width=5):
    """Draw axes plus a line revealed left-to-right up to fraction k of the x range."""
    x0, y0, x1, y1 = box

    def px(x):
        return lerp(x0, x1, (x - xr[0]) / (xr[1] - xr[0]))

    def py(y):
        return lerp(y1, y0, (y - yr[0]) / (yr[1] - yr[0]))

    for v in yticks:
        c.line([(x0, py(v)), (x1, py(v))], (255, 255, 255, 30), 1.5, a)
        c.text(x0 - 12, py(v), yfmt.format(v), 16, MUTED, 600, anchor='rm', a=a, shadow=False)
    for v in xticks:
        c.text(px(v), y1 + 22, str(v), 16, MUTED, 600, a=a, shadow=False)
    c.line([(x0, y1), (x1, y1)], (255, 255, 255, 90), 2, a)
    xmax = lerp(xr[0], xr[1], clamp(k))
    pts = [(px(x), py(y)) for x, y in zip(xs, ys) if x <= xmax]
    if len(pts) >= 2:
        c.line(pts, color, width, a)
        hx, hy = pts[-1]
        c.circle(hx, hy, width * 1.6, color, WHITE, 2, a)
        if head_label:
            c.text(hx + 14, hy - 22, head_label(xmax), 20, color, 700, anchor='lm', a=a)
    return px, py


# ---------------------------------------------------------------- captions --
def caption_chunks(words, max_words=6):
    chunks, cur = [], []
    for w in words:
        cur.append(w)
        end_punct = w['w'].rstrip().endswith(('.', '?', '!', ','))
        if len(cur) >= max_words or end_punct:
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    return chunks


def draw_captions(c, t, chunks):
    for i, ch in enumerate(chunks):
        s = ch[0]['s'] - 0.05
        e = chunks[i + 1][0]['s'] - 0.05 if i + 1 < len(chunks) and chunks[i + 1][0]['s'] - ch[-1]['e'] < 0.6 \
            else ch[-1]['e'] + 0.35
        if not s <= t < e:
            continue
        f = font(30, 800)
        parts = [w['w'].strip() for w in ch]
        widths = [f.getlength(p + ' ') / K for p in parts]
        total = sum(widths)
        x = W / 2 - total / 2
        y = H - 64
        pk = ease_out(seg(t, s, s + 0.15))
        for p, wdt, w in zip(parts, widths, ch):
            col = GOLD if w['s'] <= t else WHITE
            c.text(x, y + 6 * (1 - pk), p, 30, col, 800, anchor='lm', a=pk, shadow=False, stroke=3,
                   stroke_fill=(10, 12, 24))
            x += wdt


# ------------------------------------------------------------------- voice --
_kokoro = None


def tts(text):
    global _kokoro
    if _kokoro is None:
        from kokoro_onnx import Kokoro
        _kokoro = Kokoro(os.path.join(MODELS, 'kokoro-v1.0.onnx'), os.path.join(MODELS, 'voices-v1.0.bin'))
    lang = 'en-gb' if VOICE.startswith('b') else 'en-us'
    s, sr = _kokoro.create(text, voice=VOICE, speed=1.0, lang=lang)
    n = int(len(s) * SR / sr)
    return np.interp(np.linspace(0, len(s) - 1, n), np.arange(len(s)), s).astype(np.float32)


_whisper = None


def word_times(audio):
    """Word-level timings for one narration line (seconds from line start)."""
    global _whisper
    if _whisper is None:
        from faster_whisper import WhisperModel
        _whisper = WhisperModel('base.en', device='cpu', compute_type='int8',
                                download_root=os.path.join(MODELS, 'whisper'))
    a16 = np.interp(np.linspace(0, len(audio) - 1, int(len(audio) * 16000 / SR)), np.arange(len(audio)), audio)
    segs, _ = _whisper.transcribe(a16.astype(np.float32), word_timestamps=True, language='en')
    return [{'w': w.word, 's': w.start, 'e': w.end} for s in segs for w in s.words]


# ------------------------------------------------------------------- audio --
def tone(f, dur, decay=6.0, harmonics=(1, 0.3, 0.1)):
    tt = np.arange(int(dur * SR)) / SR
    out = sum(h * np.sin(2 * np.pi * f * (i + 1) * tt) for i, h in enumerate(harmonics))
    return out * np.exp(-tt * decay)


def sfx(kind):
    rnd = np.random.default_rng(len(kind))
    if kind == 'pop':
        tt = np.arange(int(0.12 * SR)) / SR
        return np.sin(2 * np.pi * (300 + 900 * tt / 0.12) * tt) * np.exp(-tt * 30) * 0.5
    if kind == 'ding':
        a, b = tone(1568, 1.2, 4, (1, 0.4, 0.2)), tone(2093, 1.0, 5, (0.5,))
        a[:len(b)] += b
        return a * 0.25
    if kind == 'whoosh':
        n = int(0.5 * SR)
        noise = rnd.standard_normal(n)
        tt = np.arange(n) / SR
        env = np.sin(np.pi * tt / 0.5) ** 2
        sm = np.convolve(noise, np.ones(30) / 30, 'same')
        return (noise - sm) * env * 0.12
    if kind == 'down':
        tt = np.arange(int(0.6 * SR)) / SR
        return np.sin(2 * np.pi * (600 - 400 * tt / 0.6) * tt) * np.exp(-tt * 4) * 0.25
    if kind == 'tick':
        return tone(2400, 0.05, 80, (1,)) * 0.2
    raise ValueError(kind)


def music(total, path, tempo=86, seed=3):
    """Compose a calm piano/strings/bass/drums bed with FluidSynth."""
    import pretty_midi
    pm = pretty_midi.PrettyMIDI(initial_tempo=tempo)
    piano = pretty_midi.Instrument(program=4)       # electric piano
    pad = pretty_midi.Instrument(program=89)        # warm pad
    bass = pretty_midi.Instrument(program=33)       # finger bass
    drums = pretty_midi.Instrument(program=0, is_drum=True)
    prog = [[53, 57, 60, 64], [52, 55, 59, 62], [50, 53, 57, 60], [48, 52, 55, 59]]  # Fmaj7 Em7 Dm7 Cmaj7
    beat = 60 / tempo
    rnd = random.Random(seed)
    bars = int(total / (4 * beat)) + 2
    for b in range(bars):
        ch = prog[b % 4]
        t0 = b * 4 * beat
        for n in ch:
            pad.notes.append(pretty_midi.Note(42, n, t0, t0 + 4 * beat))
        bass.notes.append(pretty_midi.Note(78, ch[0] - 12, t0, t0 + 1.5 * beat))
        bass.notes.append(pretty_midi.Note(70, ch[0] - 12, t0 + 2.5 * beat, t0 + 3.5 * beat))
        for i in range(8):
            if rnd.random() < 0.75:
                n = ch[rnd.choice([0, 1, 2, 3])] + 12
                s = t0 + i * beat / 2
                piano.notes.append(pretty_midi.Note(rnd.randint(48, 66), n, s, s + beat * 0.9))
        if b >= 2:
            for i in range(4):
                s = t0 + i * beat
                if i in (0, 2):
                    drums.notes.append(pretty_midi.Note(70, 36, s, s + 0.1))
                else:
                    drums.notes.append(pretty_midi.Note(55, 38, s, s + 0.1))
            for i in range(8):
                s = t0 + i * beat / 2
                drums.notes.append(pretty_midi.Note(34 + (8 if i % 2 == 0 else 0), 42, s, s + 0.05))
    pm.instruments += [piano, pad, bass, drums]
    mid = path.replace('.wav', '.mid')
    pm.write(mid)
    subprocess.run(['fluidsynth', '-ni', '-g', '0.5', '-F', path, '-r', str(SR),
                    '/usr/share/sounds/sf2/FluidR3_GM.sf2', mid], check=True, capture_output=True)
    m, _ = sf.read(path, always_2d=True)
    return m[:, :2]


def place(buf, clip, at):
    i0 = int(at * SR)
    if i0 >= len(buf):
        return
    i1 = min(len(buf), i0 + len(clip))
    if buf.ndim == 2 and clip.ndim == 1:
        buf[i0:i1] += clip[:i1 - i0, None]
    else:
        buf[i0:i1] += clip[:i1 - i0]


def master(voice, mus, fx, total):
    import pyloudnorm as pyln
    n = int(total * SR)
    voice = np.pad(voice, (0, max(0, n - len(voice))))[:n]
    mus = np.pad(mus, ((0, max(0, n - len(mus))), (0, 0)))[:n]
    fx = np.pad(fx, (0, max(0, n - len(fx))))[:n]
    v = voice / max(1e-6, np.max(np.abs(voice))) * 0.8
    k = int(0.35 * SR)
    env = np.convolve((np.abs(v) > 0.02).astype(float), np.ones(k) / k, 'same')
    duck = 1 - 0.6 * np.clip(env * 3, 0, 1)
    tt = np.arange(n) / SR
    mus = mus / max(1e-6, np.max(np.abs(mus)))
    mus *= (np.minimum(1, tt / 2) * np.clip((total - tt) / 3, 0, 1))[:, None]
    out = mus * (0.22 * duck)[:, None] + v[:, None] + fx[:, None] * 0.7
    meter = pyln.Meter(SR)
    for _ in range(3):  # normalize to YouTube's -14 LUFS, then limit peaks; repeat to settle
        with np.errstate(all='ignore'):
            out = pyln.normalize.loudness(out, meter.integrated_loudness(out), -14.0)
        out = limit(out, 0.89)
    return out


def limit(x, ceiling):
    """Peak limiter: smooth gain reduction wherever the signal exceeds the ceiling."""
    from scipy.ndimage import minimum_filter1d, uniform_filter1d
    peak = np.max(np.abs(x), axis=1)
    g = np.minimum(1.0, ceiling / np.maximum(peak, 1e-9))
    g = minimum_filter1d(g, int(0.01 * SR))           # hold over 10 ms so the gain dips before peaks
    g = uniform_filter1d(g, int(0.005 * SR))          # smooth the gain curve
    g = minimum_filter1d(g, int(0.005 * SR))
    return np.clip(x * g[:, None], -ceiling, ceiling)


# ------------------------------------------------------------------- build --
class Ctx:
    def __init__(self, t, starts, ends, dur):
        self.t, self.L, self.E, self.dur = t, starts, ends, dur


_JOB = {}  # set before the worker pool forks; scenes hold lambdas that can't be pickled


def _render_scene(si):
    scenes, plan, build_dir = _JOB['scenes'], _JOB['plan'], _JOB['build_dir']
    sc = scenes[si]
    dur, starts, ends, chunks = plan[si]
    path = os.path.join(build_dir, f'seg_{si:02d}.mp4')
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                           '-s', f'{OUT_W}x{OUT_H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset',
                           'medium', '-crf', '18', '-pix_fmt', 'yuv420p', path], stdin=subprocess.PIPE)
    for fi in range(int(round(dur * FPS))):
        t = fi / FPS
        c = Canvas(*sc.get('bg', (BG1, BG2)))
        sc['draw'](c, Ctx(t, starts, ends, dur))
        if sc.get('captions', True):
            draw_captions(c, t, chunks)
        arr = np.asarray(c.frame())
        if sc.get('fade', True):
            f = clamp(min(t / 0.3, (dur - t) / 0.3))
            if f < 1:
                arr = (arr.astype(np.float32) * f).astype(np.uint8)
        ff.stdin.write(arr.tobytes())
    ff.stdin.close()
    ff.wait()
    return path


def build(scenes, out_path, build_dir, only=None):
    """Synthesize narration, time scenes to it, render, mix and encode."""
    os.makedirs(build_dir, exist_ok=True)
    plan, voice_parts, fx_cues = [], [], []
    clock = 0.0
    print('narration + word timings...', flush=True)
    for si, sc in enumerate(scenes):
        t, starts, ends, words = sc.get('lead', 0.5), [], [], []
        for li, text in enumerate(sc['lines']):
            cache = os.path.join(build_dir, f'vo_{VOICE}_{si:02d}_{li}.npy')
            if os.path.exists(cache):
                a = np.load(cache)
            else:
                a = tts(text)
                np.save(cache, a)
            wt = word_times(a)
            starts.append(t)
            ends.append(t + len(a) / SR)
            words += [{'w': w['w'], 's': t + w['s'], 'e': t + w['e']} for w in wt]
            voice_parts.append((clock + t, a))
            t += len(a) / SR + sc.get('gap', 0.35)
        dur = max(sc.get('min', 0), t + sc.get('tail', 0.5))
        dur = round(dur * FPS) / FPS
        for at, kind in sc.get('sfx', lambda L: [])(starts):
            fx_cues.append((clock + at, kind))
        plan.append((dur, starts, ends, caption_chunks(words)))
        clock += dur
    total = clock
    print(f'total {total:.1f}s ({total / 60:.1f} min); rendering...', flush=True)
    _JOB.update(scenes=scenes, plan=plan, build_dir=build_dir)
    jobs = [i for i in range(len(scenes)) if only is None or i in only]
    jobs.sort(key=lambda i: -plan[i][0])
    with Pool(os.cpu_count()) as pool:
        for p in pool.imap_unordered(_render_scene, jobs):
            print('  done', os.path.basename(p), flush=True)
    n = int(total * SR) + SR
    voice = np.zeros(n)
    for at, a in voice_parts:
        place(voice, a, at)
    fx = np.zeros(n)
    for at, kind in fx_cues:
        place(fx, sfx(kind), at)
    mus = music(total + 2, os.path.join(build_dir, 'music.wav'))
    audio = master(voice, mus, fx, total)
    wav = os.path.join(build_dir, 'mix.wav')
    sf.write(wav, audio, SR, subtype='PCM_16')
    lst = os.path.join(build_dir, 'list.txt')
    with open(lst, 'w') as f:
        for i in range(len(scenes)):
            f.write(f"file 'seg_{i:02d}.mp4'\n")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-i', wav,
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', out_path],
                   check=True)
    chapters, clock = [], 0.0
    for sc, (dur, *_rest) in zip(scenes, plan):
        if sc.get('chapter'):
            chapters.append((clock, sc['chapter']))
        clock += dur
    print('wrote', out_path)
    return total, chapters


def still(scene, t, path, starts=None):
    """Render a single preview frame of one scene (no narration needed)."""
    starts = starts or [0.5 + 4 * i for i in range(len(scene['lines']))]
    ends = [s + 3.6 for s in starts]
    c = Canvas(*scene.get('bg', (BG1, BG2)))
    scene['draw'](c, Ctx(t, starts, ends, ends[-1] + 1 if ends else 6))
    c.frame().save(path)
