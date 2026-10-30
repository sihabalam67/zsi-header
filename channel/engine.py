"""Coin Theory video engine: drawing, characters, charts, captions, voice, music, mix.

Episodes import this module, define SCENES, and call `build(...)`.
Everything runs locally with free tools installed by studio/setup.sh.
"""
import difflib
import hashlib
import math
import os
import random
import re
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
# AUDIO_STYLE=upgrade: GeneralUser GS soundfont (free incl. commercial) + Kenney CC0 interface sounds
AUDIO_STYLE = os.environ.get('AUDIO_STYLE', 'upgrade')  # 'classic' = weeks 1-2 sound
# VOICE_ENGINE=chatterbox: expressive MIT-licensed voice; each line is checked with Whisper, retried, then Kokoro
VOICE_ENGINE = os.environ.get('VOICE_ENGINE', 'chatterbox')  # 'kokoro' = weeks 1-2 voice
VOICELAB_PY = os.environ.get('VOICELAB_PY', '/home/user/voicelab/venv/bin/python')
CB_EXAG, CB_CFG = 0.5, 0.3                         # calmer, slower delivery than Chatterbox's defaults
CB_TEMPO = float(os.environ.get('CB_TEMPO', '0.92'))  # ease to explainer pace (~170 words a minute)
FALLBACKS = []  # lines that could not be voiced by Chatterbox (reported by build so mixed voices never go unnoticed)


def voice_id():
    """Cache key prefix: changes whenever the voice or its settings change."""
    if VOICE_ENGINE == 'kokoro':
        return VOICE
    return f'chatterbox-{CB_EXAG}-{CB_CFG}-{CB_TEMPO}'
KENNEY = os.path.join(STUDIO, 'assets', 'audio', 'kenney')
KENNEY_SFX = {'pop': 'drop_002', 'ding': 'confirmation_002', 'down': 'minimize_005', 'tick': 'tick_002'}

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


def font(size, weight=700, family='Poppins', k=None):
    k = k or K
    key = (size, weight, family, k)
    if key not in _fonts:
        have = sorted(int(f.rsplit('-', 1)[1][:-4]) for f in os.listdir(FONTS) if f.startswith(family + '-'))
        weight = min(have, key=lambda w: abs(w - weight))
        _fonts[key] = ImageFont.truetype(os.path.join(FONTS, f'{family}-{weight}.ttf'), int(size * k))
    return _fonts[key]


def gradient(top, bottom):
    key = (top, bottom)
    if key not in _grad:
        h, w = int(H * K), int(W * K)
        y = np.linspace(0, 1, h)[:, None, None]
        arr = np.array(top) * (1 - y) + np.array(bottom) * y
        _grad[key] = Image.fromarray(np.ascontiguousarray(np.broadcast_to(arr, (h, w, 3)).astype(np.uint8)), 'RGB')
    return _grad[key]


def icon_image(name, color, size, stroke=2.0, k=None):
    k = k or K
    key = (name, color, int(size * k), stroke)
    if key not in _icons:
        import cairosvg
        from io import BytesIO
        svg = open(os.path.join(ICONS, f'{name}.svg')).read()
        hexc = '#%02x%02x%02x' % color[:3]
        svg = svg.replace('currentColor', hexc).replace('stroke-width="2"', f'stroke-width="{stroke}"')
        png = cairosvg.svg2png(bytestring=svg.encode(), output_width=int(size * k), output_height=int(size * k))
        _icons[key] = Image.open(BytesIO(png)).convert('RGBA')
    return _icons[key]


class Canvas:
    def __init__(self, top=BG1, bottom=BG2, img=None, k=None):
        self.k = k or K
        self.img = img if img is not None else gradient(top, bottom).copy()
        self.d = ImageDraw.Draw(self.img, 'RGBA')
        self.alpha = 1.0

    def _c(self, c, a=1.0):
        if c is None:
            return None
        base = c[3] / 255 if len(c) == 4 else 1.0
        al = int(255 * clamp(base * a * self.alpha))
        return (c[0], c[1], c[2], al) if al > 0 else None

    def circle(self, x, y, r, fill=None, outline=None, width=0, a=1.0):
        self.ellipse(x, y, r, r, fill, outline, width, a)

    def ellipse(self, x, y, rx, ry, fill=None, outline=None, width=0, a=1.0):
        if rx <= 0.2 or ry <= 0.2:
            return
        self.d.ellipse([(x - rx) * self.k, (y - ry) * self.k, (x + rx) * self.k, (y + ry) * self.k],
                       fill=self._c(fill, a), outline=self._c(outline, a), width=int(width * self.k))

    def poly(self, pts, fill=None, outline=None, width=0, a=1.0):
        p = [(x * self.k, y * self.k) for x, y in pts]
        self.d.polygon(p, fill=self._c(fill, a))
        if outline and width:
            self.d.line(p + [p[0], p[1]], fill=self._c(outline, a), width=int(width * self.k), joint='curve')

    def line(self, pts, fill, width, a=1.0):
        if len(pts) < 2:
            return
        if self._c(fill, a) is None:
            return
        self.d.line([(x * self.k, y * self.k) for x, y in pts], fill=self._c(fill, a), width=max(1, int(width * self.k)),
                    joint='curve')

    def rrect(self, x0, y0, x1, y1, r, fill=None, outline=None, width=0, a=1.0):
        if x1 <= x0 or y1 <= y0:
            return
        r = min(r, (x1 - x0) / 2, (y1 - y0) / 2)
        self.d.rounded_rectangle([x0 * self.k, y0 * self.k, x1 * self.k, y1 * self.k], radius=r * self.k, fill=self._c(fill, a),
                                 outline=self._c(outline, a), width=int(width * self.k))

    def arc(self, x, y, r, start, end, fill, width, a=1.0):
        if self._c(fill, a) is None:
            return
        self.d.arc([(x - r) * self.k, (y - r) * self.k, (x + r) * self.k, (y + r) * self.k], start, end, fill=self._c(fill, a),
                   width=max(1, int(width * self.k)))

    def text(self, x, y, s, size, fill=WHITE, weight=700, anchor='mm', a=1.0, shadow=True, family='Poppins',
             stroke=0, stroke_fill=INK):
        if a * self.alpha <= 0.004:
            return
        f = font(size, weight, family, self.k)
        if shadow:
            self.d.text(((x + 2) * self.k, (y + 3) * self.k), s, font=f, fill=self._c((0, 0, 0, 110), a), anchor=anchor,
                        stroke_width=int(stroke * self.k), stroke_fill=self._c((0, 0, 0, 110), a))
        self.d.text((x * self.k, y * self.k), s, font=f, fill=self._c(fill, a), anchor=anchor,
                    stroke_width=int(stroke * self.k), stroke_fill=self._c(stroke_fill, a))

    def icon(self, name, x, y, size, color=WHITE, a=1.0, stroke=2.0):
        a = clamp(a * self.alpha)
        if a <= 0 or size < 2:
            return
        im = icon_image(name, color, size, stroke, self.k)
        if a < 1:
            im = im.copy()
            im.putalpha(im.getchannel('A').point(lambda v: int(v * a)))
        self.img.paste(im, (int((x - size / 2) * self.k), int((y - size / 2) * self.k)), im)

    def frame(self):
        return self.img.resize((OUT_W, OUT_H), Image.LANCZOS)


# ------------------------------------------------------------- characters ---
def face(c, x, y, r, mood='happy', look=(0, 0), a=1.0, t=0.0, phase=0.0, talk=None):
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
        o = abs(math.sin(t * 11 + phase)) * 0.5 + 0.2 if talk is None else 0.08 + 0.85 * talk
        c.ellipse(x, my, mw * 0.55, mw * o, INK, a=a)


def penny(c, x, y, r, t, mood='happy', look=(0, 0), a=1.0, arms=(30, 150), wave=False, bounce=True,
          scale_y=1.0, talk=None):
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
    if talk is not None and talk > 0.05 and mood in ('happy', 'proud'):
        mood = 'talk'
    face(c, x, by + r * 0.05, r * 0.95, mood, look, a, t, talk=talk)


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


# ------------------------------------------------------------ spoken text --
_ONES = ('zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen '
         'sixteen seventeen eighteen nineteen').split()
_TENS = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']


def int_words(n):
    if n < 20:
        return _ONES[n]
    if n < 100:
        return _TENS[n // 10] + ('-' + _ONES[n % 10] if n % 10 else '')
    if n < 1000:
        return _ONES[n // 100] + ' hundred' + (' ' + int_words(n % 100) if n % 100 else '')
    for div, name in ((10 ** 9, 'billion'), (10 ** 6, 'million'), (1000, 'thousand')):
        if n >= div:
            return int_words(n // div) + ' ' + name + (' ' + int_words(n % div) if n % div else '')


def year_words(n):
    if 2000 <= n < 2010:
        return 'two thousand' + (' ' + _ONES[n % 10] if n % 10 else '')
    hi, lo = divmod(n, 100)
    if lo == 0:
        return int_words(hi) + ' hundred'
    return int_words(hi) + ' ' + (int_words(lo) if lo >= 10 else 'oh ' + _ONES[lo])


def num_words(s):
    if '.' in s:
        a, b = s.split('.')
        return int_words(int(a or 0)) + ' point ' + ' '.join(_ONES[int(d)] for d in b)
    return int_words(int(s))


_TOK = re.compile(r'^([^\w$~]*)(.*?)([^\w%]*)$')


def say(token):
    """Spoken form of one display token: '$8.66' -> 'eight dollars and sixty-six cents', '1970' -> year."""
    pre, core, post = _TOK.match(token).groups()
    core = core.lstrip('~')
    m = re.fullmatch(r'\$(\d[\d,]*)(?:\.(\d\d))?', core)
    if m:
        d, cents = int(m.group(1).replace(',', '')), int(m.group(2) or 0)
        parts = []
        if d:
            parts.append(int_words(d) + (' dollar' if d == 1 else ' dollars'))
        if cents:
            parts.append(int_words(cents) + (' cent' if cents == 1 else ' cents'))
        word = ' and '.join(parts) or 'zero dollars'
    elif re.fullmatch(r'\d+(\.\d+)?%', core):
        word = num_words(core[:-1]) + ' percent'
    elif re.fullmatch(r'(1[89]|20)\d\ds', core):
        y = year_words(int(core[:4]))
        word = y[:-1] + 'ies' if y.endswith('y') else y + 's'
    elif re.fullmatch(r'(1[89]|20)\d\d', core):
        word = year_words(int(core))
    elif re.fullmatch(r'\d[\d,]*(\.\d+)?', core):
        word = num_words(core.replace(',', ''))
    else:
        word = core
    return pre + word + post


def parse_line(text):
    """Display tokens with spoken forms. Write {shown|spoken} to override, e.g. {$100 bill|hundred-dollar bill}."""
    toks = []
    for m in re.finditer(r'\{([^}|]*)\|([^}]*)\}(\S*)|\S+', text):
        if m.group(1) is not None:
            toks.append((m.group(1) + m.group(3), m.group(2) + m.group(3)))
        else:
            toks.append((m.group(0), say(m.group(0))))
    return toks


def _norm(w):
    return re.sub(r'[^a-z0-9]', '', w.lower())


_CONTRACTIONS = {"they're": 'they are', "it's": 'it is', "that's": 'that is', "you're": 'you are',
                 "don't": 'do not', "isn't": 'is not', "doesn't": 'does not', "didn't": 'did not',
                 "shouldn't": 'should not', "can't": 'cannot', "won't": 'will not', "here's": 'here is',
                 "let's": 'let us', "what's": 'what is', "there's": 'there is', "we'll": 'we will',
                 "you'll": 'you will', "we're": 'we are', "i'm": 'i am'}


def _words(text):
    """Normalized words, with contractions expanded so "they're" matches "they are"."""
    out = []
    for w in text.replace('-', ' ').split():
        key = re.sub(r"[^a-z']", '', w.lower().replace('\u2019', "'"))
        out += [x for x in (_norm(y) for y in _CONTRACTIONS.get(key, w).split()) if x]
    return out


def align(tokens, heard, dur):
    """Time each display token from Whisper's words. Words Whisper invents never match, so never show."""
    spoken = []
    for ti, (_, sp) in enumerate(tokens):
        spoken += [(ti, w) for w in _words(sp)]
    merged = []  # Whisper sometimes splits "$1.83" into "$1" + ".83"; rejoin before matching
    for h in heard:
        w = h['w'].strip()
        if merged and re.fullmatch(r'([.,]\d+%?|%|-\w+)[.,?!]*', w) and re.search(r'\d$', merged[-1]['w'].strip()):
            merged[-1] = {'w': merged[-1]['w'].strip() + w, 's': merged[-1]['s'], 'e': h['e']}
        else:
            merged.append(h)
    heard = merged
    hw = []
    for h in heard:
        sub = _words(say(h['w'].strip()))
        for j, x in enumerate(sub):
            d = (h['e'] - h['s']) / len(sub)
            hw.append((x, h['s'] + j * d, h['s'] + (j + 1) * d))
    sm = difflib.SequenceMatcher(None, [n for _, n in spoken], [x for x, _, _ in hw], autojunk=False)
    times = [None] * len(spoken)
    for a, b, size in sm.get_matching_blocks():
        for k in range(size):
            times[a + k] = (hw[b + k][1], min(hw[b + k][2], dur))
    i = 0
    while i < len(times):  # interpolate runs of unmatched words between their matched neighbours
        if times[i] is None:
            j = i
            while j < len(times) and times[j] is None:
                j += 1
            lo = times[i - 1][1] if i else 0.0
            hi = times[j][0] if j < len(times) else dur
            step = (hi - lo) / (j - i)
            for k in range(i, j):
                times[k] = (lo + (k - i) * step, lo + (k - i + 1) * step)
            i = j
        i += 1
    out = []
    for ti, (disp, _) in enumerate(tokens):
        ts = [times[k] for k, (tj, _) in enumerate(spoken) if tj == ti]
        if ts:
            out.append({'w': disp, 's': min(x[0] for x in ts), 'e': max(x[1] for x in ts)})
    coverage = sum(size for *_, size in sm.get_matching_blocks()) / max(1, len(spoken))
    return out, coverage


# ---------------------------------------------------------------- captions --
def caption_chunks(words, max_words=6):
    chunks, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) >= max_words or w['w'].rstrip('"\'').endswith(('.', '?', '!', ',', ':')):
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    return chunks


def draw_captions(c, t, chunks, x=W / 2, y=H - 64, size=30, maxw=1180):
    for i, ch in enumerate(chunks):
        s = ch[0]['s'] - 0.05
        nxt = chunks[i + 1][0]['s'] - 0.05 if i + 1 < len(chunks) else None
        e = nxt if nxt is not None and nxt - ch[-1]['e'] < 0.6 else ch[-1]['e'] + 0.35
        if not s <= t < e:
            continue
        parts = [w['w'] for w in ch]
        sz = size
        while True:
            f = font(sz, 900, k=c.k)
            widths = [f.getlength(p + ' ') / c.k for p in parts]
            if sum(widths) <= maxw or sz <= 14:
                break
            sz -= 2
        px = x - sum(widths) / 2
        pk = ease_out(seg(t, s, s + 0.15))
        for p, wdt, w in zip(parts, widths, ch):
            col = GOLD if w['s'] <= t else WHITE
            c.text(px, y + 6 * (1 - pk), p, sz, col, 900, anchor='lm', a=pk, shadow=False, stroke=max(2, sz // 9),
                   stroke_fill=(10, 12, 24))
            px += wdt
        return


def write_srt(chunks_abs, path):
    def ts(x):
        ms = int(round(x * 1000))
        return f'{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}'
    with open(path, 'w') as f:
        for i, ch in enumerate(chunks_abs, 1):
            f.write(f"{i}\n{ts(ch[0]['s'])} --> {ts(ch[-1]['e'] + 0.2)}\n{' '.join(w['w'] for w in ch)}\n\n")


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


_cb = None


def _cb_start():
    global _cb
    _cb = subprocess.Popen([VOICELAB_PY, os.path.join(STUDIO, 'chatterbox_worker.py')], stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    while True:
        line = _cb.stdout.readline()
        if not line or line.startswith('{"ready"'):
            return bool(line)


def tts_chatterbox(text, seed=0, _retry=True):
    """One line through the persistent Chatterbox worker; returns float32 audio at SR, or None on failure.
    A crashed worker is restarted once, so one bad line can't silently switch the rest of a video to Kokoro."""
    import json
    import tempfile
    if (_cb is None or _cb.poll() is not None) and not _cb_start():
        return None
    out = tempfile.mktemp(suffix='.wav')
    try:
        _cb.stdin.write(json.dumps({'text': text, 'seed': seed, 'out': out, 'exaggeration': CB_EXAG,
                                    'cfg': CB_CFG}) + '\n')
        _cb.stdin.flush()
        line = _cb.stdout.readline()
        while line and not line.startswith('{'):
            line = _cb.stdout.readline()
    except (BrokenPipeError, OSError):
        line = ''
    if not line:  # worker died mid-line
        return tts_chatterbox(text, seed, _retry=False) if _retry and _cb_start() else None
    if not json.loads(line).get('ok'):
        return None
    if abs(CB_TEMPO - 1) > 0.01:
        slow = out.replace('.wav', '_t.wav')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', out, '-filter:a', f'atempo={CB_TEMPO}', slow], check=True)
        os.replace(slow, out)
    a, sr = sf.read(out, always_2d=True)
    os.remove(out)
    a = a.mean(axis=1)
    n = int(len(a) * SR / sr)
    a = np.interp(np.linspace(0, len(a) - 1, n), np.arange(len(a)), a)
    peak = np.abs(a).max()
    return (a / peak * 0.9 if peak > 0 else a).astype(np.float32)


def speak(toks, min_coverage=0.9):
    """Narrate one line: Chatterbox when enabled (Whisper-checked, up to 5 tries), else or failing that Kokoro."""
    spoken = ' '.join(sp for _, sp in toks)
    if VOICE_ENGINE == 'chatterbox' and os.path.exists(VOICELAB_PY):
        best = None
        for attempt in range(5):
            a = tts_chatterbox(spoken, seed=attempt)
            if a is None:
                break
            cov = align(toks, word_times(a), len(a) / SR)[1]
            if best is None or cov > best[1]:
                best = (a, cov)
            if cov >= min_coverage:
                return a
        if best is not None and best[1] >= 0.8:
            return best[0]
        FALLBACKS.append(spoken)
        print(f'  WARNING chatterbox failed, using Kokoro (mixed voices!) for: {spoken[:60]!r}', flush=True)
    return tts(spoken)


_whisper = None


def word_times(audio):
    """Word-level timings for one narration line (seconds from line start)."""
    global _whisper
    if _whisper is None:
        from faster_whisper import WhisperModel
        _whisper = WhisperModel('base.en', device='cpu', compute_type='int8',
                                download_root=os.path.join(MODELS, 'whisper'))
    a16 = np.interp(np.linspace(0, len(audio) - 1, int(len(audio) * 16000 / SR)), np.arange(len(audio)), audio)
    segs, _ = _whisper.transcribe(a16.astype(np.float32), word_timestamps=True, language='en',
                                  condition_on_previous_text=False)
    return [{'w': w.word, 's': w.start, 'e': w.end} for s in segs for w in s.words]


# ------------------------------------------------------------------- audio --
def tone(f, dur, decay=6.0, harmonics=(1, 0.3, 0.1)):
    tt = np.arange(int(dur * SR)) / SR
    out = sum(h * np.sin(2 * np.pi * f * (i + 1) * tt) for i, h in enumerate(harmonics))
    return out * np.exp(-tt * decay)


def sfx(kind):
    if AUDIO_STYLE == 'upgrade' and kind in KENNEY_SFX:
        a, sr = sf.read(os.path.join(KENNEY, KENNEY_SFX[kind] + '.ogg'), always_2d=True)
        a = a.mean(axis=1)
        if sr != SR:
            a = np.interp(np.arange(int(len(a) * SR / sr)) * sr / SR, np.arange(len(a)), a)
        return a / (np.abs(a).max() + 1e-9) * 0.45
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
    font = os.path.join(MODELS, 'GeneralUser-GS.sf2')
    if AUDIO_STYLE != 'upgrade' or not os.path.exists(font):
        font = '/usr/share/sounds/sf2/FluidR3_GM.sf2'
    subprocess.run(['fluidsynth', '-ni', '-g', '0.5', '-F', path, '-r', str(SR), font, mid], check=True,
                   capture_output=True)
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
XF = 0.4  # crossfade between scenes, seconds


class Ctx:
    def __init__(self, t, starts, ends, dur, env=None):
        self.t, self.L, self.E, self.dur, self._env = t, starts, ends, dur, env

    def talk(self):
        """Narration loudness right now (0..1), for lip-sync."""
        if self._env is None:
            return None
        i = int(self.t * FPS)
        return float(self._env[i]) if 0 <= i < len(self._env) else 0.0


_vig = {}


def vignette(w, h, strength=0.24):
    if (w, h) not in _vig:
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2) / math.sqrt(2)
        _vig[w, h] = (1 - strength * r ** 2.2)[:, :, None]
    return _vig[w, h]


def compose(sc, t, starts, ends, dur, env, chunks, layout='long'):
    """Draw one frame: scene -> slow camera zoom -> vignette -> captions (and vertical layout for Shorts)."""
    from PIL import ImageFilter
    c = Canvas(*sc.get('bg', (BG1, BG2)))
    sc['draw'](c, Ctx(t, starts, ends, dur, env))
    big = c.img
    z0, z1 = sc.get('cam', (1.0, 1.045))
    z = lerp(z0, z1, ease(t / dur)) if dur else z0
    fx, fy = sc.get('focus', (0.5, 0.5))
    bw, bh = big.size
    cw, ch = bw / z, bh / z
    x0 = clamp(fx * bw - cw / 2, 0, bw - cw)
    y0 = clamp(fy * bh - ch / 2, 0, bh - ch)
    box = (x0, y0, x0 + cw, y0 + ch)
    if layout == 'long':
        img = big.resize((OUT_W, OUT_H), Image.LANCZOS, box=box)
        img = Image.fromarray((np.asarray(img).astype(np.float32) * vignette(OUT_W, OUT_H)).astype(np.uint8))
        if sc.get('captions', True):
            draw_captions(Canvas(img=img, k=OUT_W / W), t, chunks)
        return img
    # Shorts: 1080x1920, blurred backdrop, the scene in the middle, big captions underneath
    main = big.resize((1080, 608), Image.LANCZOS, box=box)
    back = big.resize((480, 270), Image.BILINEAR, box=box).filter(ImageFilter.GaussianBlur(10))
    back = back.resize((3413, 1920), Image.BILINEAR).crop((1166, 0, 2246, 1920))
    back = Image.fromarray((np.asarray(back).astype(np.float32) * 0.45).astype(np.uint8))
    back.paste(main, (0, 600))
    cv = Canvas(img=back, k=1.5)  # logical 720 x 1280
    cv.text(360, 300, 'COIN THEORY', 40, GOLD, 900, stroke=4)
    if sc.get('captions', True):
        draw_captions(cv, t, chunks, x=360, y=930, size=46, maxw=660)
    return back


_JOB = {}  # set before the worker pool forks; scenes hold lambdas that can't be pickled


def _render_scene(si):
    scenes, plan, build_dir, layout = _JOB['scenes'], _JOB['plan'], _JOB['build_dir'], _JOB['layout']
    sc = scenes[si]
    dur, starts, ends, chunks, env = plan[si]
    ow, oh = (OUT_W, OUT_H) if layout == 'long' else (1080, 1920)
    path = os.path.join(build_dir, f'{layout}_{si:02d}.mp4')
    if os.environ.get('RESUME') and os.path.exists(path):  # reuse a finished segment after an interruption
        probe = subprocess.run(['ffprobe', '-v', 'error', '-count_packets', '-select_streams', 'v:0', '-show_entries',
                                'stream=nb_read_packets', '-of', 'csv=p=0', path], capture_output=True, text=True)
        if probe.stdout.strip().isdigit() and int(probe.stdout) == int(round(dur * FPS)):
            return path
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                           '-s', f'{ow}x{oh}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset',
                           'medium', '-crf', '16', '-pix_fmt', 'yuv420p', path], stdin=subprocess.PIPE)
    first, last = si == _JOB['first'], si == _JOB['last']
    for fi in range(int(round(dur * FPS))):
        t = fi / FPS
        arr = np.asarray(compose(sc, t, starts, ends, dur, env, chunks, layout))
        f = min(t / 0.5 if first else 1.0, (dur - t) / 0.8 if last else 1.0)
        if f < 1:
            arr = (arr.astype(np.float32) * clamp(f)).astype(np.uint8)
        ff.stdin.write(arr.tobytes())
    ff.stdin.close()
    ff.wait()
    return path


def narrate(scenes, build_dir, min_coverage=0.85):
    """Synthesize every line (cached by text), time captions, and build lip-sync envelopes."""
    plan, voice_parts = [], []
    for si, sc in enumerate(scenes):
        t, starts, ends, words = sc.get('lead', 0.55), [], [], []
        parts = []
        for text in sc['lines']:
            toks = parse_line(text)
            spoken = ' '.join(sp for _, sp in toks)
            key = hashlib.md5(f'{voice_id()}|{spoken}'.encode()).hexdigest()[:12]
            cache = os.path.join(build_dir, f'vo_{key}.npy')
            if os.path.exists(cache):
                a = np.load(cache)
            else:
                a = speak(toks)
                np.save(cache, a)
            dur = len(a) / SR
            timed, cov = align(toks, word_times(a), dur)
            if cov < min_coverage:
                print(f'  WARNING scene {si}: only {cov:.0%} of words recognised in: {text!r}', flush=True)
            starts.append(t)
            ends.append(t + dur)
            words += [{'w': w['w'], 's': t + w['s'], 'e': t + w['e']} for w in timed]
            parts.append((t, a))
            t += dur + sc.get('gap', 0.4)
        dur = round(max(sc.get('min', 0), t + sc.get('tail', 0.6)) * FPS) / FPS
        local = np.zeros(int(dur * SR) + SR)
        for at, a in parts:
            place(local, a, at)
        hop = SR // FPS
        env = np.array([np.sqrt(np.mean(local[i:i + hop] ** 2)) for i in range(0, len(local) - hop, hop)])
        if env.max() > 0:
            env = np.clip(env / np.percentile(env[env > 0.005], 90), 0, 1) if (env > 0.005).any() else env
        plan.append((dur, starts, ends, caption_chunks(words), env))
        voice_parts.append(parts)
    return plan, voice_parts


def build(scenes, out_path, build_dir, layout='long', only=None, srt_path=None):
    """Narrate, render scenes in parallel, crossfade them, mix audio, encode. Returns (total, chapters)."""
    os.makedirs(build_dir, exist_ok=True)
    print('narration + caption timing...', flush=True)
    plan, voice_parts = narrate(scenes, build_dir)
    starts_abs, clock = [], 0.0
    for i, (dur, *_r) in enumerate(plan):
        starts_abs.append(clock)
        clock += dur - (XF if i < len(plan) - 1 else 0)
    total = clock
    print(f'total {total:.1f}s ({total / 60:.1f} min); rendering {layout}...', flush=True)
    _JOB.update(scenes=scenes, plan=plan, build_dir=build_dir, layout=layout, first=0, last=len(scenes) - 1)
    jobs = [i for i in range(len(scenes)) if only is None or i in only]
    jobs.sort(key=lambda i: -plan[i][0])
    with Pool(os.cpu_count()) as pool:
        for p in pool.imap_unordered(_render_scene, jobs):
            print('  done', os.path.basename(p), flush=True)
    # audio
    n = int((total + 1) * SR)
    voice, fx = np.zeros(n), np.zeros(n)
    for si, parts in enumerate(voice_parts):
        for at, a in parts:
            place(voice, a, starts_abs[si] + at)
        for at, kind in scenes[si].get('sfx', lambda L: [])(plan[si][1]):
            place(fx, sfx(kind), starts_abs[si] + at)
    mus = music(total + 2, os.path.join(build_dir, f'music_{layout}.wav'))
    audio = master(voice, mus, fx, total)
    wav = os.path.join(build_dir, f'mix_{layout}.wav')
    sf.write(wav, audio, SR, subtype='PCM_16')
    # video: chain crossfades between scene segments
    inputs, filt, prev = [], [], '0:v'
    for i in range(len(scenes)):
        inputs += ['-i', os.path.join(build_dir, f'{layout}_{i:02d}.mp4')]
    for i in range(1, len(scenes)):
        trans = scenes[i].get('trans', 'fade')
        filt.append(f'[{prev}][{i}:v]xfade=transition={trans}:duration={XF}:offset={starts_abs[i]:.4f}[v{i}]')
        prev = f'v{i}'
    cmd = ['ffmpeg', '-y', '-loglevel', 'error'] + inputs + ['-i', wav]
    if filt:
        cmd += ['-filter_complex', ';'.join(filt), '-map', f'[{prev}]']
    else:
        cmd += ['-map', '0:v']
    cmd += ['-map', f'{len(scenes)}:a', '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p',
            '-c:a', 'aac', '-b:a', '256k', '-t', f'{total:.3f}', '-movflags', '+faststart', out_path]
    subprocess.run(cmd, check=True)
    if srt_path:
        chunks_abs = [[{'w': w['w'], 's': starts_abs[si] + w['s'], 'e': starts_abs[si] + w['e']} for w in ch]
                      for si, pl in enumerate(plan) if scenes[si].get('captions', True) for ch in pl[3]]
        write_srt(chunks_abs, srt_path)
    chapters = [(starts_abs[i], sc['chapter']) for i, sc in enumerate(scenes) if sc.get('chapter')]
    print('wrote', out_path)
    if FALLBACKS:
        print(f'WARNING: {len(FALLBACKS)} line(s) used the backup voice; re-render them before uploading:', FALLBACKS)
    return total, chapters


def still(scene, t, path, starts=None):
    """Render a single preview frame of one scene (no narration needed)."""
    starts = starts or [0.5 + 4 * i for i in range(len(scene['lines']))]
    ends = [s + 3.6 for s in starts]
    dur = ends[-1] + 1 if ends else 6
    compose(dict(scene, captions=False), t, starts, ends, dur, None, [], 'long').save(path)
