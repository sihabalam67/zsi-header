#!/usr/bin/env python3
"""Second Chances - an original animated explainer, made entirely with code.

Everything is generated here: frames are drawn with Pillow, narration is
synthesized locally with Piper TTS (public-domain "norman" voice by default),
music is composed with numpy, and ffmpeg encodes the result.

Usage:
    pip install piper-tts pillow numpy
    python3 video/render.py            # writes video/second_chances.mp4
    VOICE=joe python3 video/render.py  # use the CC0 "joe" voice instead
"""
import math
import os
import random
import subprocess
import sys
import wave
from multiprocessing import Pool

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, 'build')
OUTPUT = os.path.join(HERE, 'second_chances.mp4')
VOICE = os.environ.get('VOICE', 'norman')
VOICE_MODEL = f'en_US-{VOICE}-medium'

W, H, FPS, SS = 1280, 720, 30, 2
SR = 44100

FONT_DIR = '/usr/share/fonts/opentype/inter/'
_fonts = {}


def font(size, weight='Bold'):
    key = (size, weight)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(f'{FONT_DIR}Inter-{weight}.otf', int(size * SS))
    return _fonts[key]


# ---------------------------------------------------------------- palette ---
NAVY, INDIGO = (14, 18, 44), (36, 42, 100)
HEALTHY, HEALTHY_D = (255, 184, 92), (205, 120, 48)
CANCER, CANCER_D = (178, 70, 200), (108, 32, 136)
TCELL, TCELL_D = (70, 176, 255), (28, 100, 186)
GRAY, GRAY_D = (138, 144, 168), (88, 92, 116)
ANTI, ANTI_D = (110, 232, 160), (40, 150, 90)
RED, WHITE, INK = (240, 74, 96), (255, 255, 255), (20, 22, 40)
CAR = (255, 150, 60)


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
    return clamp((t - a) / (b - a))


def lerp(a, b, k):
    return a + (b - a) * k


def mix(c1, c2, k):
    return tuple(int(lerp(a, b, k)) for a, b in zip(c1, c2))


def along(pts, k):
    lens = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    d = clamp(k) * sum(lens)
    for i, l in enumerate(lens):
        if d <= l or i == len(lens) - 1:
            f = clamp(d / l) if l else 0
            return lerp(pts[i][0], pts[i + 1][0], f), lerp(pts[i][1], pts[i + 1][1], f)
        d -= l


# ---------------------------------------------------------------- canvas ---
_gradients = {}


def gradient(top, bottom):
    key = (top, bottom)
    if key not in _gradients:
        y = np.linspace(0, 1, H * SS)[:, None, None]
        arr = np.array(top) * (1 - y) + np.array(bottom) * y
        arr = np.broadcast_to(arr, (H * SS, W * SS, 3)).astype(np.uint8)
        _gradients[key] = Image.fromarray(np.ascontiguousarray(arr), 'RGB')
    return _gradients[key]


class Canvas:
    """Draws in 1280x720 logical units onto a supersampled image."""

    def __init__(self, top=NAVY, bottom=INDIGO):
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
        if rx <= 0 or ry <= 0:
            return
        s = SS
        self.d.ellipse([(x - rx) * s, (y - ry) * s, (x + rx) * s, (y + ry) * s],
                       fill=self._c(fill, a), outline=self._c(outline, a), width=int(width * s))

    def poly(self, pts, fill=None, outline=None, width=0, a=1.0):
        p = [(x * SS, y * SS) for x, y in pts]
        self.d.polygon(p, fill=self._c(fill, a))
        if outline and width:
            self.d.line(p + [p[0], p[1]], fill=self._c(outline, a), width=int(width * SS), joint='curve')

    def line(self, pts, fill, width, a=1.0):
        self.d.line([(x * SS, y * SS) for x, y in pts], fill=self._c(fill, a),
                    width=max(1, int(width * SS)), joint='curve')

    def rrect(self, x0, y0, x1, y1, r, fill=None, outline=None, width=0, a=1.0):
        self.d.rounded_rectangle([x0 * SS, y0 * SS, x1 * SS, y1 * SS], radius=r * SS,
                                 fill=self._c(fill, a), outline=self._c(outline, a), width=int(width * SS))

    def arc(self, x, y, r, start, end, fill, width, a=1.0):
        self.d.arc([(x - r) * SS, (y - r) * SS, (x + r) * SS, (y + r) * SS], start, end,
                   fill=self._c(fill, a), width=max(1, int(width * SS)))

    def text(self, x, y, s, size, fill=WHITE, weight='Bold', anchor='mm', a=1.0, shadow=True):
        f = font(size, weight)
        if shadow:
            self.d.text(((x + 2) * SS, (y + 3) * SS), s, font=f, fill=self._c((0, 0, 0, 120), a), anchor=anchor)
        self.d.text((x * SS, y * SS), s, font=f, fill=self._c(fill, a), anchor=anchor)

    def frame(self):
        return self.img.resize((W, H), Image.LANCZOS)


# ------------------------------------------------------------- characters ---
def blob_pts(x, y, r, t, phase, wob=0.04, spiky=0.0, n=64):
    pts = []
    for i in range(n):
        th = 2 * math.pi * i / n
        k = 1 + wob * math.sin(3 * th + t * 2.2 + phase) + wob * 0.6 * math.sin(5 * th - t * 1.7 + phase * 2)
        if spiky:
            k += spiky * (0.5 + 0.5 * math.sin(9 * th + phase * 3 + t * 0.8)) ** 3 - spiky * 0.3
        pts.append((x + r * k * math.cos(th), y + r * k * math.sin(th)))
    return pts


def face(c, x, y, r, mood='happy', look=(0, 0), a=1.0, t=0.0, phase=0.0):
    ex, ey, er = r * 0.32, y - r * 0.12, r * 0.17
    lw = max(1.5, r * 0.065)
    blink = math.sin(t * 1.3 + phase * 5) > 0.985
    for sx in (-1, 1):
        cx = x + sx * ex
        if blink or mood == 'sleepy':
            c.line([(cx - er, ey + er * 0.2), (cx + er, ey + er * 0.2)], INK, lw, a)
        else:
            c.circle(cx, ey, er, WHITE, a=a)
            c.circle(cx + look[0] * er * 0.4, ey + look[1] * er * 0.4, er * 0.56, INK, a=a)
        if mood == 'angry':
            c.line([(cx - sx * er * 1.3, ey - er * 1.9), (cx + sx * er * 1.1, ey - er * 1.1)], INK, lw, a)
        elif mood in ('scared', 'sad'):
            c.line([(cx - sx * er * 1.2, ey - er * 1.2), (cx + sx * er * 1.0, ey - er * 1.9)], INK, lw * 0.8, a)
    my, mw = y + r * 0.3, r * 0.26
    if mood == 'happy':
        c.arc(x, my - mw * 0.55, mw, 20, 160, INK, lw, a)
    elif mood == 'angry':
        c.line([(x - mw, my), (x - mw * 0.33, my - mw * 0.25), (x + mw * 0.33, my),
                (x + mw, my - mw * 0.25)], INK, lw, a)
    elif mood in ('sad', 'sleepy'):
        c.arc(x, my + mw * 0.75, mw * 0.85, 205, 335, INK, lw, a)
    elif mood == 'scared':
        c.ellipse(x, my, mw * 0.4, mw * 0.5, INK, a=a)


def cell(c, x, y, r, body, dark, t, phase, mood, spiky=0.0, a=1.0, look=(0, 0)):
    if r <= 1:
        return
    c.poly(blob_pts(x, y, r, t, phase, spiky=spiky), body, dark, max(2, r * 0.08), a)
    c.circle(x - r * 0.38, y - r * 0.42, r * 0.16, (255, 255, 255, 80), a=a)
    face(c, x, y, r, mood, look, a, t, phase)


def healthy(c, x, y, r, t, ph=0.0, mood='happy', a=1.0, look=(0, 0)):
    cell(c, x, y, r, HEALTHY, HEALTHY_D, t, ph, mood, a=a, look=look)


def cancer(c, x, y, r, t, ph=0.0, mood='angry', a=1.0, k=1.0, look=(0, 0)):
    cell(c, x, y, r, mix(HEALTHY, CANCER, k), mix(HEALTHY_D, CANCER_D, k), t, ph, mood,
         spiky=0.2 * k, a=a, look=look)


def tcell(c, x, y, r, t, ph=0.0, mood='happy', a=1.0, gray=0.0, car=0.0, look=(0, 0)):
    body, dark = mix(TCELL, GRAY, gray), mix(TCELL_D, GRAY_D, gray)
    for i in range(10):
        th = 2 * math.pi * i / 10 + ph + math.sin(t * 2 + i) * 0.05
        p0 = (x + r * 0.9 * math.cos(th), y + r * 0.9 * math.sin(th))
        p1 = (x + r * 1.22 * math.cos(th), y + r * 1.22 * math.sin(th))
        c.line([p0, p1], dark, max(2, r * 0.07), a)
        c.circle(p1[0], p1[1], r * 0.08, dark, a=a)
    if car > 0:
        for i in range(6):
            th = 2 * math.pi * i / 6 + 0.26 + ph
            p0 = (x + r * 0.9 * math.cos(th), y + r * 0.9 * math.sin(th))
            p1 = (x + r * (1 + 0.5 * car) * math.cos(th), y + r * (1 + 0.5 * car) * math.sin(th))
            c.line([p0, p1], CAR, max(2, r * 0.1), a)
            for s in (-0.5, 0.5):
                c.line([p1, (p1[0] + r * 0.2 * car * math.cos(th + s), p1[1] + r * 0.2 * car * math.sin(th + s))],
                       CAR, max(2, r * 0.08), a)
    cell(c, x, y, r, body, dark, t, ph, mood, a=a, look=look)


def tag(c, x0, y0, x1, y1, a=1.0, dim=0.0):
    """A fake "I'm fine" signal: a green flag sticking out of a cancer cell."""
    c.line([(x0, y0), (x1, y1)], CANCER_D, 5, a)
    col = mix(ANTI, GRAY, dim)
    c.circle(x1, y1, 16, col, ANTI_D, 3, a)
    c.line([(x1 - 7, y1), (x1 - 2, y1 + 6), (x1 + 8, y1 - 6)], WHITE, 3.5, a)


def antibody(c, x, y, s=1.0, a=1.0):
    """A Y-shaped antibody; (x, y) is the fork."""
    c.line([(x, y), (x, y + 42 * s)], ANTI_D, 9 * s, a)
    c.line([(x - 26 * s, y - 28 * s), (x, y), (x + 26 * s, y - 28 * s)], ANTI_D, 9 * s, a)
    c.line([(x, y), (x, y + 42 * s)], ANTI, 5 * s, a)
    c.line([(x - 26 * s, y - 28 * s), (x, y), (x + 26 * s, y - 28 * s)], ANTI, 5 * s, a)


def stop_sign(c, x, y, r, a=1.0):
    if a <= 0 or r <= 0:
        return
    pts = [(x + r * math.cos(math.pi / 8 + i * math.pi / 4), y + r * math.sin(math.pi / 8 + i * math.pi / 4))
           for i in range(8)]
    c.poly(pts, RED, WHITE, max(2, r * 0.1), a)
    c.text(x, y + 1, 'STOP', max(8, int(r * 0.52)), WHITE, 'Black', a=a, shadow=False)


def person(c, x, y, s, fill, a=1.0):
    """Simple person icon; (x, y) is the feet."""
    c.circle(x, y - 92 * s, 20 * s, fill, a=a)
    c.rrect(x - 24 * s, y - 66 * s, x + 24 * s, y, 18 * s, fill, a=a)


def burst(c, x, y, k, color, n=16, radius=90, seed=0):
    if k <= 0 or k >= 1:
        return
    rnd = random.Random(seed)
    for _ in range(n):
        ang = rnd.random() * 2 * math.pi
        d = ease_out(k) * radius * rnd.uniform(0.5, 1)
        c.circle(x + math.cos(ang) * d, y + math.sin(ang) * d, (1 - k) * rnd.uniform(4, 11), color, a=1 - k)


def specks(c, t, seed=1, n=40, color=WHITE, amax=0.12):
    rnd = random.Random(seed)
    for _ in range(n):
        x0, y0 = rnd.uniform(0, W), rnd.uniform(0, H)
        r, sp, ph, al = rnd.uniform(2, 10), rnd.uniform(5, 20), rnd.uniform(0, 6), rnd.uniform(0.3, 1)
        y = (y0 - t * sp) % (H + 40) - 20
        c.circle(x0 + math.sin(t * 0.5 + ph) * 15, y, r, color, a=amax * al)


def header(c, s, a, y=58, size=40):
    c.text(W / 2, y, s, size, WHITE, 'Black', a=a)


GRID = [(col * 118 + (row % 2) * 59 - 20, row * 118 + 42) for row in range(6) for col in range(12)]


# ----------------------------------------------------------------- scenes ---
# Each scene draws itself at animation time t (seconds, on its base timeline).

def s_title(c, t):
    specks(c, t, 3, 60)
    for i in range(8):
        ang = i / 8 * 2 * math.pi + t * 0.15
        x, y = W / 2 + math.cos(ang) * 470, H / 2 + math.sin(ang) * 250
        a = ease(seg(t, 0.2 + i * 0.1, 1.2 + i * 0.1))
        if i == 3:
            tcell(c, x, y, 40, t, i, a=a)
        elif i == 6:
            cancer(c, x, y, 38, t, i, a=a)
        else:
            healthy(c, x, y, 38, t, i, a=a)
    k = ease_out(seg(t, 0.5, 1.6))
    c.text(W / 2, 320 - 24 * (1 - k), 'SECOND CHANCES', 92, WHITE, 'Black', a=k)
    c.text(W / 2, 405, 'How medicine learned to help the body fight late-stage cancer', 26,
           (200, 210, 255), 'Medium', a=ease(seg(t, 1.5, 2.5)))


def s_cells(c, t):
    specks(c, t, 4)
    ka = 1 - ease(seg(t, 6, 7.5))
    if ka > 0:
        c.alpha = ka
        c.circle(400, 200, 62, (190, 205, 255, 230))
        c.rrect(315, 280, 485, 570, 70, (190, 205, 255, 230))
        rnd = random.Random(7)
        for i in range(70):
            x, y = rnd.uniform(335, 465), rnd.uniform(300, 550)
            c.circle(x, y, 6, HEALTHY, a=ease(seg(t, 0.8 + i * 0.05, 1.3 + i * 0.05)))
        n = int(37e12 * ease(seg(t, 1, 5)))
        c.text(840, 330, f'{n:,}', 50, WHITE, 'Black', a=ease(seg(t, 0.8, 1.4)))
        c.text(840, 385, 'cells in one human body', 24, (200, 210, 255), 'Medium', a=ease(seg(t, 1, 1.6)))
        c.alpha = 1.0
    kb = ease(seg(t, 6, 7.5))
    if kb > 0:
        c.alpha = kb
        for i, (x, y) in enumerate(GRID):
            bob = math.sin(t * 1.6 + i) * 4
            healthy(c, x, y + bob, 44 * lerp(0.6, 1, kb), t, i)
        c.alpha = 1.0


def s_mutation(c, t):
    cx, cy = 668, 278
    n_cancer = 0 if t < 6 else min(32, 2 ** (int((t - 6) / 1.4) + 1))
    radius = 36 * math.sqrt(max(n_cancer, 1)) + 34 if n_cancer else 0
    for i, (x, y) in enumerate(GRID):
        if (x, y) == (cx, cy):
            continue
        d = math.dist((x, y), (cx, cy))
        mood = 'happy'
        if radius and d < radius + 50:
            mood = 'scared'
            if d < radius:
                f = radius / max(d, 1)
                x, y = cx + (x - cx) * f, cy + (y - cy) * f
        look = ((cx - x) / max(d, 1), (cy - y) / max(d, 1)) if t > 2.5 else (0, 0)
        healthy(c, x, y + math.sin(t * 1.6 + i) * 4, 44, t, i, mood, look=look)
    k = ease(seg(t, 2.8, 4.8))
    for i in range(max(1, n_cancer)):
        if i == 0:
            x, y, s = cx, cy, 1.0
        else:
            g = int(math.log2(i))
            born = 6 + 1.4 * g
            if t < born:
                continue
            ang = i * 2.39996
            rr = 36 * math.sqrt(i)
            x, y = cx + math.cos(ang) * rr, cy + math.sin(ang) * rr * 0.85
            s = back_out(seg(t, born, born + 0.5))
        if i == 0 and k < 1:
            cancer(c, x, y, 44, t, i, 'angry' if k > 0.5 else 'scared', k=k)
        else:
            cancer(c, x, y, 34 * s, t, i)
    if 2.4 < t < 3.4:
        zk = seg(t, 2.4, 3.4)
        c.line([(cx + 40, cy - 120), (cx + 10, cy - 70), (cx + 30, cy - 70), (cx, cy - 30)],
               (255, 240, 120), 6, a=1 - zk)
        burst(c, cx, cy, zk, (255, 240, 120), seed=2)


S3_TARGETS = [(820, 250), (930, 390), (790, 470), (1000, 220)]


def s_patrol(c, t):
    specks(c, t, 5)
    rnd = random.Random(11)
    for i in range(9):
        x, y = rnd.uniform(60, 1220), rnd.choice([rnd.uniform(40, 120), rnd.uniform(580, 660)])
        healthy(c, x, y, 32, t, i, look=(0.5, 0))
    for i, (x, y) in enumerate(S3_TARGETS):
        arr = 1 + i * 1.8 + 2.6
        pk = seg(t, arr, arr + 0.45)
        if pk < 1:
            cancer(c, x, y, 40 * (1 - ease(pk)), t, i, 'scared' if t > arr - 1.2 else 'angry')
        burst(c, x, y, seg(t, arr, arr + 0.9), CANCER, seed=i)
    for i, (x, y) in enumerate(S3_TARGETS):
        dep = 1 + i * 1.8
        k = ease(seg(t, dep, dep + 2.6))
        sx, sy = -80, 200 + i * 110
        px = lerp(sx, x - 78, k)
        py = lerp(sy, y, k) + math.sin(t * 3 + i) * 6 * (1 - k)
        if t > dep + 2.6:
            py -= abs(math.sin((t - dep) * 4)) * 10 * clamp(1 - (t - dep - 2.6) / 3)
        tcell(c, px, py, 38, t, i, look=(1, 0))


def s_disguise(c, t):
    specks(c, t, 6)
    cx, cy, cr = 820, 360, 72
    cancer(c, cx, cy, cr, t, 1.0, 'happy' if t > 6 else 'angry', look=(-1, 0))
    tk = back_out(seg(t, 0.5, 1.2))
    tx = cx - cr - 50 * tk
    if tk > 0:
        tag(c, cx - cr + 6, cy, tx, cy, a=clamp(tk))
    gray = ease(seg(t, 7.5, 9.5))
    reach = ease(seg(t, 1.5, 5))
    back = ease(seg(t, 9.5, 13.5))
    px = lerp(lerp(80, tx - 16 - 64, reach), 380, back)
    py = 360 + math.sin(t * 2) * 5
    tcell(c, px, py, 62, t, 0.4, 'sleepy' if gray > 0.5 else 'happy', gray=gray, look=(1, 0))
    sk = back_out(seg(t, 6, 6.6))
    stop_sign(c, px, py - 110, 34 * sk, a=clamp(sk))
    c.text(tx, cy + 70, 'CHECKPOINT', 22, ANTI, 'Black', a=ease(seg(t, 6.2, 7)))
    if 5 < t < 6.5:
        burst(c, tx - 16, cy, seg(t, 5, 6.5), ANTI, n=10, radius=50, seed=4)


BODY_PATHS = [
    [(590, 255), (615, 180), (640, 125)],
    [(590, 255), (630, 320), (668, 352)],
    [(590, 255), (575, 380), (590, 470), (595, 590)],
]


def s_metastasis(c, t):
    skin, edge = (58, 68, 128), (110, 124, 200)
    for args in [(470, 210, 530, 450, 30), (750, 210, 810, 450, 30), (560, 440, 632, 700, 35),
                 (648, 440, 720, 700, 35), (540, 190, 740, 470, 80)]:
        c.rrect(*args, skin, edge, 3)
    c.circle(640, 118, 60, skin, edge, 3)
    c.ellipse(640, 112, 38, 28, (240, 180, 210))
    c.ellipse(600, 262, 34, 52, (230, 140, 160))
    c.ellipse(680, 262, 34, 52, (230, 140, 160))
    c.ellipse(668, 352, 48, 26, (200, 110, 90))
    c.line([(595, 500), (595, 670)], (235, 230, 220), 12)
    va = ease(seg(t, 2.5, 3.5))
    for p in BODY_PATHS:
        c.line(p, RED, 5, a=0.6 * va)
    cancer(c, 590, 255, lerp(6, 22, ease(seg(t, 0, 4))), t, 0)
    for j, p in enumerate(BODY_PATHS):
        for m in range(3):
            launch = 4 + j * 1.1 + m * 0.7
            k = seg(t, launch, launch + 2)
            if 0 < k < 1:
                x, y = along(p, ease(k))
                c.circle(x, y, 6, CANCER, CANCER_D, 2)
        arrive = 4 + j * 1.1 + 2
        g = ease(seg(t, arrive, arrive + 2.5))
        if g > 0:
            ex, ey = p[-1]
            cancer(c, ex, ey, 6 + 10 * g, t, j + 1)
    sk = ease_out(seg(t, 9.5, 10.3))
    if sk > 0:
        c.rrect(900, 190 - 10 * (1 - sk), 1180, 285 - 10 * (1 - sk), 16, (40, 10, 30, 160), RED, 5, a=sk)
        c.text(1040, 238 - 10 * (1 - sk), 'STAGE IV', 50, RED, 'Black', a=sk)


def s_tools(c, t):
    specks(c, t, 8)
    pa = 1 - ease(seg(t, 6, 6.8))
    if pa > 0:
        for i, (x, label) in enumerate([(260, 'SURGERY'), (640, 'CHEMOTHERAPY'), (1020, 'RADIATION')]):
            k = ease_out(seg(t, 0.3 + i * 1.2, 0.9 + i * 1.2)) * pa
            y = 260 + 20 * (1 - k)
            c.circle(x, y, 100, (255, 255, 255, 28), a=k)
            if i == 0:
                c.rrect(x - 75, y + 4, x + 5, y + 26, 8, (110, 116, 150), a=k)
                c.poly([(x + 5, y), (x + 62, y - 8), (x + 88, y + 8), (x + 5, y + 30)], (220, 228, 240), a=k)
            elif i == 1:
                c.circle(x, y + 18, 42, (170, 230, 90), a=k)
                c.poly([(x - 37, y + 2), (x + 37, y + 2), (x, y - 68)], (170, 230, 90), a=k)
            else:
                for j in range(12):
                    th = j / 12 * 2 * math.pi + t * 0.4
                    l = 62 + 8 * math.sin(t * 6 + j)
                    c.line([(x + 32 * math.cos(th), y + 32 * math.sin(th)),
                            (x + l * math.cos(th), y + l * math.sin(th))], (255, 220, 90), 6, a=k)
                c.circle(x, y, 22, (255, 220, 90), a=k)
            c.text(x, y + 140, label, 26, WHITE, 'Black', a=k)
    rk = ease(seg(t, 6.4, 7.4))
    if rk > 0:
        survivors = (3, 7)
        for i in range(9):
            x, y = 150 + i * 122, 430
            hit = 7.6 + i * 0.25
            hk = seg(t, hit, hit + 0.4)
            dk = seg(t, hit - 1, hit)
            if 0 < dk < 1:
                c.circle(x, lerp(-40, y - 46, ease(dk)), 12, (170, 230, 90))
                c.poly([(x - 10, lerp(-40, y - 46, ease(dk)) - 4), (x + 10, lerp(-40, y - 46, ease(dk)) - 4),
                        (x, lerp(-40, y - 46, ease(dk)) - 26)], (170, 230, 90))
            burst(c, x, y - 40, seg(t, hit, hit + 0.7), (170, 230, 90), n=10, radius=50, seed=i)
            if i % 2 == 0:
                healthy(c, x, y, 44 * lerp(1, 0.75, ease(hk)), t, i, 'sad' if hk > 0 else 'happy', a=rk)
            else:
                fade = 1 if i in survivors else 1 - ease(seg(t, hit + 0.3, hit + 1.2))
                cancer(c, x, y, 44 * lerp(1, 0.7, ease(hk)), t, i, a=rk * fade)
                if i in survivors and t > 10.5:
                    pulse = (t * 1.2) % 1
                    c.circle(x, y, 50 + 40 * pulse, None, RED, 4, a=(1 - pulse) * ease(seg(t, 10.5, 11)))


S7_ROWS = [220, 375, 530]


def s_immuno(c, t):
    specks(c, t, 9)
    header(c, 'IMMUNOTHERAPY', ease(seg(t, 0.2, 1)))
    for j, y in enumerate(S7_ROWS):
        cx, tx = 920, 920 - 50 - 46
        block = 3.5 + j * 0.6
        atk = 6.5 + j * 0.8
        arrive = atk + 2
        pk = seg(t, arrive, arrive + 0.45)
        if pk < 1:
            a = 1 - ease(pk)
            cancer(c, cx, y, 48 * a, t, j, 'scared' if t > atk else 'angry', look=(-1, 0))
            tag(c, cx - 44, y, tx, y, a=a, dim=ease(seg(t, block, block + 0.5)))
            ak = ease(seg(t, 1 + j * 0.6, block))
            antibody(c, lerp(tx + 140, tx, ak), lerp(-80, y, ak), 0.8, a=a)
        burst(c, cx, y, seg(t, arrive, arrive + 0.9), CANCER, seed=j + 5)
        gray = 1 - ease(seg(t, block + 0.3, block + 1.3))
        px = lerp(500, tx - 16 - 56, ease(seg(t, atk, arrive)))
        py = y + math.sin(t * 2 + j) * 5
        tcell(c, px, py, 44, t, j, 'sleepy' if gray > 0.5 else 'happy', gray=gray, look=(1, 0))
        stop_sign(c, px, py - 78, 22, a=gray)


def s_cart(c, t):
    specks(c, t, 10)
    header(c, 'CAR-T CELL THERAPY', ease(seg(t, 0.2, 1)))
    glow = ease(seg(t, 10, 13))
    pc = mix((190, 205, 255), (120, 200, 255), glow)
    c.circle(180, 300, 44, pc, a=0.85)
    c.rrect(124, 356, 236, 560, 44, pc, a=0.85)
    c.rrect(520, 220, 800, 520, 30, (255, 255, 255, 22), (180, 200, 255), 4)
    c.text(660, 250, 'LAB', 22, (180, 200, 255), 'Black')
    car = ease(seg(t, 3, 5))
    n = 1 if t < 5.5 else min(16, 2 ** (int((t - 5.5) / 0.8) + 1))
    for i in range(n):
        gx, gy = 590 + (i % 4) * 47, 310 + (i // 4) * 50
        if i == 0:
            k = ease(seg(t, 0.5, 3))
            sx, sy = lerp(180, 660, k), lerp(450, 380, k)
            if t >= 5.5:
                sx, sy = lerp(660, gx, ease(seg(t, 5.5, 6))), lerp(380, gy, ease(seg(t, 5.5, 6)))
            r = lerp(34, 18, ease(seg(t, 5.5, 6)))
        else:
            born = 5.5 + 0.8 * int(math.log2(i))
            sx, sy, r = gx, gy, 18 * back_out(seg(t, born, born + 0.4))
        leave = 9 + i * 0.15
        lk = ease(seg(t, leave, leave + 1.8))
        rnd = random.Random(i)
        ex, ey = 180 + rnd.uniform(-35, 35), 440 + rnd.uniform(-60, 80)
        x, y = lerp(sx, ex, lk), lerp(sy, ey, lk) - math.sin(lk * math.pi) * 60
        tcell(c, x, y, r, t, i, car=car, a=1 - ease(seg(t, leave + 1.6, leave + 2.2)))


def s_results(c, t):
    specks(c, t, 12)
    header(c, 'Advanced melanoma: 5-year survival', ease(seg(t, 0.2, 1)), size=36)
    rows = [(250, 'Before modern', 'immunotherapy', 2, 1.5, '~1 in 6', HEALTHY),
            (440, 'Combination', 'immunotherapy', 6, 4.5, '~1 in 2', TCELL)]
    for y, l1, l2, alive, start, label, col in rows:
        ra = ease(seg(t, start - 1, start - 0.3))
        c.text(70, y - 60, l1, 24, WHITE, 'Bold', anchor='lm', a=ra)
        c.text(70, y - 30, l2, 24, WHITE, 'Bold', anchor='lm', a=ra)
        for i in range(12):
            x = 360 + i * 58
            on = i < alive and t > start + i * 0.35
            person(c, x, y + 10, 0.6, col if on else (90, 96, 130), a=ra)
        c.text(1150, y - 30, label, 38, col, 'Black', a=ease(seg(t, start + alive * 0.35, start + alive * 0.35 + 0.6)))
    c.text(70, 520, 'Approximate figures. Combination therapy: CheckMate 067 trial (Larkin et al., NEJM 2019).',
           16, (170, 178, 220), 'Regular', anchor='lm', a=ease(seg(t, 6, 7)))


def s_outro(c, t):
    sy = lerp(640, 470, ease(seg(t, 0, 6)))
    for i in range(5, 0, -1):
        c.circle(640, sy, 110 + i * 34, (255, 210, 150, 22))
    c.circle(640, sy, 110, (255, 224, 160))
    rnd = random.Random(5)
    for i in range(16):
        x0, sp, ph = rnd.uniform(80, 1200), rnd.uniform(14, 30), rnd.uniform(0, 7)
        y = 760 - ((t * sp + ph * 80) % 800)
        fn = tcell if i % 3 == 0 else healthy
        fn(c, x0 + math.sin(t + ph) * 20, y, 14, t, i, a=0.55)
    c.ellipse(640, 910, 920, 340, (34, 24, 64))
    c.circle(640, 478, 16, (34, 24, 64))
    c.rrect(626, 496, 654, 572, 12, (34, 24, 64))
    c.text(W / 2, 140, 'The story of cancer is still being written.', 40, WHITE, 'Black', a=ease(seg(t, 1, 2)))
    c.text(W / 2, 196, 'But more and more often, it has a different ending.', 30, (255, 236, 210), 'SemiBold',
           a=ease(seg(t, 3.5, 4.5)))
    c.text(W / 2, 262, 'Original script & animation, made entirely with code in Claude Code', 18,
           (255, 236, 210), 'Medium', a=ease(seg(t, 7.5, 8.5)))
    c.text(W / 2, 290, f'Voice: Piper TTS ({VOICE})  ·  For education only, not medical advice', 16,
           (255, 236, 210), 'Regular', a=ease(seg(t, 8, 9)))


# (base duration, draw fn, background, narration lines)
SCENES = [
    (6, s_title, (NAVY, INDIGO), []),
    (14, s_cells, (NAVY, INDIGO), [
        "You are a city of about thirty-seven trillion cells.",
        "Each one follows the same rulebook: do your job, divide only when told to, and die when it's time.",
    ]),
    (14, s_mutation, (NAVY, INDIGO), [
        "But every day, tiny copying errors creep into your DNA.",
        "Usually they're harmless. Sometimes, a cell's brakes break, and it starts dividing without stopping.",
        "That is cancer.",
    ]),
    (14, s_patrol, (NAVY, INDIGO), [
        "Luckily, you have a defense force: your immune system.",
        "T cells patrol your body, find broken cells, and destroy them. This probably happened inside you today.",
    ]),
    (14, s_disguise, (NAVY, INDIGO), [
        "But cancer evolves. Some cancer cells learn to flash a fake signal that says: I'm fine.",
        "It hits a brake on the T cell, called an immune checkpoint, and the attack simply stops.",
    ]),
    (15, s_metastasis, ((20, 14, 40), (54, 28, 70)), [
        "Left unchecked, a tumor starts shedding cells into the bloodstream.",
        "They settle in new organs and grow there. This is metastasis, or stage four cancer.",
        "For most of history, this was where the story ended.",
    ]),
    (14, s_tools, (NAVY, INDIGO), [
        "Doctors had three main tools: cut the tumor out, poison it, or burn it with radiation.",
        "They save countless lives. But they also hurt healthy cells, and once cancer has spread, a few rogue cells often survive.",
    ]),
    (16, s_immuno, ((10, 30, 50), (24, 70, 90)), [
        "Then came a radical idea. Don't attack the cancer directly. Unleash the immune system.",
        "Drugs called checkpoint inhibitors are antibodies that cover up the fake I'm fine signal.",
        "With the brakes released, T cells recognize the cancer again, wherever it is hiding.",
    ]),
    (13, s_cart, ((10, 30, 50), (24, 70, 90)), [
        "Other treatments go even further. CAR-T therapy takes some of a patient's own T cells,",
        "re-engineers them in a lab to hunt one specific cancer marker, multiplies them by the millions, and puts them back.",
    ]),
    (15, s_results, (NAVY, INDIGO), [
        "And it can work. In advanced melanoma, one of the deadliest skin cancers,",
        "five-year survival rose from roughly one in six, to about one in two patients in a landmark trial.",
        "It doesn't work for everyone, and it can have serious side effects. But late stage no longer always means the end.",
    ]),
    (13, s_outro, ((40, 30, 90), (250, 140, 110)), [
        "The story of cancer is still being written. But more and more often, it has a different ending.",
    ]),
]


# -------------------------------------------------------------- narration ---
def voice_model():
    vdir = os.path.join(BUILD, 'voices')
    path = os.path.join(vdir, VOICE_MODEL + '.onnx')
    if not os.path.exists(path):
        os.makedirs(vdir, exist_ok=True)
        subprocess.run([sys.executable, '-m', 'piper.download_voices', '--download-dir', vdir, VOICE_MODEL],
                       check=True)
    return path


def read_wav(path):
    with wave.open(path) as w:
        sr = w.getframerate()
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    # resample to SR (linear is fine for speech going up from 22.05k)
    n = int(len(a) * SR / sr)
    return np.interp(np.linspace(0, len(a) - 1, n), np.arange(len(a)), a)


def synth_lines():
    """Synthesize each narration line; returns {(scene, line): samples}."""
    model = voice_model()
    out = {}
    for si, (_, _, _, lines) in enumerate(SCENES):
        for li, text in enumerate(lines):
            path = os.path.join(BUILD, f'vo_{VOICE}_{si:02d}_{li}.wav')
            if not os.path.exists(path):
                subprocess.run([sys.executable, '-m', 'piper', '-m', model, '-f', path,
                                '--length-scale', '1.06', '--sentence-silence', '0.25'],
                               input=text.encode(), check=True, capture_output=True)
            out[si, li] = read_wav(path)
    return out


def plan(vo):
    """Lay narration on each scene's timeline; scene length stretches to fit."""
    timeline = []
    for si, (base, _, _, lines) in enumerate(SCENES):
        cues, t = [], 0.7
        for li, text in enumerate(lines):
            d = len(vo[si, li]) / SR
            cues.append((t, t + d, text, si, li))
            t += d + 0.45
        dur = max(base, t + 0.6)
        timeline.append((dur, cues))
    return timeline


# ---------------------------------------------------------------- captions --
def wrap(text, f, maxw):
    lines, cur = [], ''
    for w in text.split():
        test = (cur + ' ' + w).strip()
        if f.getlength(test) / SS <= maxw:
            cur = test
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def caption(c, text, k):
    f = font(25, 'SemiBold')
    lines = wrap(text, f, 1040)
    lh = 36
    bw = max(f.getlength(l) / SS for l in lines) + 48
    bh = len(lines) * lh + 24
    y0 = H - 26 - bh
    c.rrect(W / 2 - bw / 2, y0, W / 2 + bw / 2, y0 + bh, 16, (6, 8, 24, 175), a=k)
    for i, l in enumerate(lines):
        c.text(W / 2, y0 + 12 + lh * i + lh / 2, l, 25, WHITE, 'SemiBold', a=k, shadow=False)


# ------------------------------------------------------------------ render --
def render_scene(args):
    si, dur, cues = args
    base, fn, bg, _ = SCENES[si]
    path = os.path.join(BUILD, f'seg_{si:02d}.mp4')
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                           '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium',
                           '-crf', '19', '-pix_fmt', 'yuv420p', path], stdin=subprocess.PIPE)
    nframes = int(round(dur * FPS))
    for fi in range(nframes):
        t = fi / FPS
        c = Canvas(*bg)
        fn(c, t * base / dur)
        for s, e, text, _, _ in cues if fn is not s_outro else []:
            k = min(seg(t, s - 0.15, s + 0.15), 1 - seg(t, e + 0.1, e + 0.4))
            if k > 0:
                caption(c, text, k)
        arr = np.asarray(c.frame(), dtype=np.float32)
        fade = min(1.0, t / 0.4, (dur - t) / 0.4)
        ff.stdin.write((arr * clamp(fade)).astype(np.uint8).tobytes())
    ff.stdin.close()
    ff.wait()
    return path


# ------------------------------------------------------------------- audio --
def midi(m):
    return 440 * 2 ** ((m - 69) / 12)


def reverb(x, seed, secs=2.6):
    rnd = np.random.default_rng(seed)
    n = int(secs * SR)
    ir = rnd.standard_normal(n) * np.exp(-np.arange(n) / SR * 2.4)
    ir /= np.sqrt(np.sum(ir ** 2))
    size = 1 << int(np.ceil(np.log2(len(x) + n)))
    y = np.fft.irfft(np.fft.rfft(x, size) * np.fft.rfft(ir, size), size)[:len(x)]
    return y


def music(total):
    n = int(total * SR)
    dry = np.zeros(n)
    prog = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]  # Am F C G
    clen = 4.0
    for ci in range(int(total / clen) + 1):
        notes = prog[ci % 4]
        s = int(ci * clen * SR)
        L = int((clen + 1.6) * SR)
        tt = np.arange(L) / SR
        env = np.minimum(1, tt / 1.2) * np.clip((clen + 1.6 - tt) / 1.6, 0, 1)
        seg_ = np.zeros(L)
        for m in notes:
            f = midi(m)
            seg_ += (np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * f * 1.004 * tt)
                     + 0.15 * np.sin(2 * np.pi * 2 * f * tt)) * 0.05
        seg_ += np.sin(2 * np.pi * midi(notes[0] - 12) * tt) * 0.09
        seg_ *= env
        if ci * clen > 5:
            for k in range(8):
                ps = int(k * 0.5 * SR)
                pl = int(1.2 * SR)
                pt = np.arange(pl) / SR
                f = midi(notes[k % 3] + 12 + (12 if k in (3, 7) else 0))
                pluck = np.sin(2 * np.pi * f * pt) * np.exp(-pt * 5) * 0.035
                end = min(L, ps + pl)
                seg_[ps:end] += pluck[:end - ps]
        end = min(n, s + L)
        dry[s:end] += seg_[:end - s]
    left = dry + 0.45 * reverb(dry, 1)
    right = dry + 0.45 * reverb(dry, 2)
    mus = np.stack([left, right], 1)
    tt = np.arange(n) / SR
    mus *= (np.minimum(1, tt / 1.5) * np.clip((total - tt) / 4, 0, 1))[:, None]
    return mus / np.max(np.abs(mus)) * 0.5


def mixdown(timeline, vo, total, path):
    mus = music(total)
    voice = np.zeros(len(mus))
    start = 0.0
    for dur, cues in timeline:
        for s, _, _, si, li in cues:
            a = vo[si, li]
            i0 = int((start + s) * SR)
            i1 = min(len(voice), i0 + len(a))
            voice[i0:i1] += a[:i1 - i0]
        start += dur
    voice = voice / max(1e-6, np.max(np.abs(voice))) * 0.85
    # duck the music under the narration
    k = int(0.3 * SR)
    envl = np.convolve(np.abs(voice) > 0.01, np.ones(k) / k, 'same')
    duck = 1 - 0.55 * np.clip(envl * 4, 0, 1)
    out = mus * (0.55 * duck)[:, None] + voice[:, None]
    out /= max(1.0, np.max(np.abs(out)) / 0.95)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((out * 32767).astype(np.int16).tobytes())


def main():
    os.makedirs(BUILD, exist_ok=True)
    print('narration...', flush=True)
    vo = synth_lines()
    timeline = plan(vo)
    total = sum(round(d * FPS) / FPS for d, _ in timeline)
    print(f'total {total:.1f}s; rendering {len(SCENES)} scenes...', flush=True)
    jobs = sorted(((i, d, cues) for i, (d, cues) in enumerate(timeline)), key=lambda j: -j[1])
    with Pool(os.cpu_count()) as pool:
        for p in pool.imap_unordered(render_scene, jobs):
            print('  done', os.path.basename(p), flush=True)
    timeline = [(round(d * FPS) / FPS, cues) for d, cues in timeline]
    audio = os.path.join(BUILD, 'audio.wav')
    mixdown(timeline, vo, total, audio)
    lst = os.path.join(BUILD, 'list.txt')
    with open(lst, 'w') as f:
        for i in range(len(SCENES)):
            f.write(f"file 'seg_{i:02d}.mp4'\n")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-i', audio,
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', OUTPUT],
                   check=True)
    print('wrote', OUTPUT)


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == '--still':
        # preview: python3 render.py --still <scene> <t>
        si, t = int(sys.argv[2]), float(sys.argv[3])
        base, fn, bg, lines = SCENES[si]
        c = Canvas(*bg)
        fn(c, t)
        if lines:
            caption(c, lines[0], 1)
        c.frame().save(os.path.join(BUILD, f'still_{si}_{t}.png'))
    else:
        main()
