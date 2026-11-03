"""Motion-graphics effects for vertical Shorts (720 x 1280 logical canvas, drawn at K scale).

Each effect is a plain function that draws one frame at local time `u` (seconds since the effect started), so a
scene can switch effects on its narration lines. Photos come from channel/assets/photos (public domain / CC0,
logged in SOURCES.md); everything else is drawn in code. Made-up headlines, apps, chats and magazines only:
no real outlets, brands, logos or people.

    snap_zoom, headline_storm, zoom_through, phone_mockup, chat_takeover, green_screen, digital_zoom,
    paper_cutout, magazine_cover, liquid_glass, orbit, growth_curve, frame_escape, checklist_pop,
    checklist_tally, broll_overlay, zoom_portal, frame_break
"""
import math
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

from engine import (Canvas, K, WHITE, GOLD, MINT, CORAL, SKY, INK, MUTED, clamp, ease, ease_out, back_out, seg,
                    lerp, pop, fade, penny, line_chart, font)

VW, VH = 720, 1280
CREAM = (250, 244, 228)
PAPER = (243, 236, 220)
GREEN = (0, 200, 70)
_cache = {}


# ------------------------------------------------------------------ helpers --
def load(path):
    if path not in _cache:
        _cache[path] = Image.open(path).convert('RGB')
    return _cache[path]


def photo_img(path, w, h, zoom=1.0, focus=(0.5, 0.5), gray=False, tint=None, blur=0, dark=0.0, sat=1.0):
    """A photo cropped to w x h px around `focus` at `zoom` (1 = cover), graded."""
    im = load(path)
    sw, sh = im.size
    s = max(w / sw, h / sh) * zoom
    cw, ch = w / s, h / s
    x0 = clamp(focus[0] * sw - cw / 2, 0, sw - cw)
    y0 = clamp(focus[1] * sh - ch / 2, 0, sh - ch)
    out = im.resize((max(1, int(w)), max(1, int(h))), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))
    if gray:
        out = out.convert('L').convert('RGB')
    if sat != 1.0:
        out = ImageEnhance.Color(out).enhance(sat)
    if tint:
        out = Image.blend(out, Image.new('RGB', out.size, tint), 0.22)
    if blur:
        out = out.filter(ImageFilter.GaussianBlur(blur))
    if dark:
        out = ImageEnhance.Brightness(out).enhance(1 - dark)
    return out


def photo(c, path, zoom=1.0, focus=(0.5, 0.5), box=(0, 0, VW, VH), a=1.0, **kw):
    x0, y0, x1, y1 = box
    w, h = int((x1 - x0) * c.k), int((y1 - y0) * c.k)
    im = photo_img(path, w, h, zoom, focus, **kw)
    paste(c, im, x0, y0, a)


def paste(c, im, x, y, a=1.0, mask=None):
    """Paste an RGB/RGBA image at logical (x, y) top-left."""
    pos = (int(x * c.k), int(y * c.k))
    if im.mode == 'RGBA':
        m = im.getchannel('A')
        if a < 1:
            m = m.point(lambda v: int(v * a))
        c.img.paste(im, pos, m)
    elif a >= 1 and mask is None:
        c.img.paste(im, pos)
    else:
        c.img.paste(im, pos, mask or Image.new('L', im.size, int(255 * clamp(a))))


def sprite(key, w, h, draw):
    """An RGBA sprite of w x h logical units, drawn once with draw(canvas) and cached."""
    if key not in _cache:
        img = Image.new('RGBA', (int(w * K), int(h * K)), (0, 0, 0, 0))
        draw(Canvas(img=img, k=K))
        _cache[key] = img
    return _cache[key]


def place(c, spr, cx, cy, scale=1.0, angle=0.0, a=1.0):
    """Paste a sprite centred at logical (cx, cy), scaled and rotated."""
    if a <= 0 or scale <= 0.01:
        return
    im = spr
    if scale != 1.0:
        im = im.resize((max(1, int(im.size[0] * scale)), max(1, int(im.size[1] * scale))), Image.BILINEAR)
    if angle:
        im = im.rotate(angle, resample=Image.BICUBIC, expand=True)
    paste(c, im, cx - im.size[0] / c.k / 2, cy - im.size[1] / c.k / 2, a)


def shadowed(spr, blur=18, off=(0, 14), alpha=0.55):
    """Sprite with a soft drop shadow under it (cached per sprite)."""
    key = ('shadow', id(spr), blur)
    if key not in _cache:
        pad = blur * 3
        w, h = spr.size
        out = Image.new('RGBA', (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
        sh = Image.new('RGBA', out.size, (0, 0, 0, 0))
        m = spr.getchannel('A').point(lambda v: int(v * alpha))
        sh.paste((0, 0, 0, 255), (pad + off[0], pad + off[1]), m)
        out = Image.alpha_composite(out, sh.filter(ImageFilter.GaussianBlur(blur)))
        out.alpha_composite(spr, (pad, pad))
        _cache[key] = out
    return _cache[key]


def zoom_canvas(c, z, cx=VW / 2, cy=VH / 2):
    """Zoom what is already drawn on the canvas by z around (cx, cy) (for snap / digital zooms)."""
    if abs(z - 1) < 1e-3:
        return
    W_, H_ = c.img.size
    cw, ch = W_ / z, H_ / z
    x0 = clamp(cx * c.k - cw / 2, 0, W_ - cw)
    y0 = clamp(cy * c.k - ch / 2, 0, H_ - ch)
    c.img.paste(c.img.resize((W_, H_), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch)))


def shake(u, amp, freq=40.0, decay=6.0, seed=0):
    r = random.Random(seed + int(u * freq))
    d = math.exp(-u * decay)
    return (r.uniform(-1, 1) * amp * d, r.uniform(-1, 1) * amp * d)


def title(c, text, y, size, color=WHITE, k=1.0, family='Anton', weight=400, stroke=5):
    """Big stacked headline text (Anton), popping in with k."""
    if k <= 0:
        return
    for i, line in enumerate(text.split('\n')):
        c.text(360, y + i * size * 1.05, line, int(size * (0.7 + 0.3 * clamp(k))), color, weight, a=clamp(k),
               family=family, stroke=stroke)


# ------------------------------------------------------------- 1 snap zoom --
def snap_zoom(c, u, img, text, focus=(0.5, 0.5), zoom_from=1.9, zoom_to=1.05, color=GOLD):
    """A photo slams in (fast zoom out + shake), then the headline lands word-stack style."""
    z = lerp(zoom_from, zoom_to, ease_out(clamp(u / 0.28)))
    dx, dy = shake(u, 14, seed=3) if u > 0.2 else (0, 0)
    photo(c, img, z, focus, box=(dx - 10, dy - 10, VW + 10 + dx, VH + 10 + dy), dark=0.25, sat=1.15)
    c.rrect(0, 0, VW, VH, 0, (0, 0, 0, 60))
    title(c, text, 360, 92, color, pop(u, 0.25, 0.3))


# --------------------------------------------------------- 2 headline storm --
def _headline_card(text, i):
    def draw(cv):
        cv.rrect(6, 6, 514, 194, 10, (252, 250, 245), (30, 30, 30), 3)
        cv.rrect(6, 6, 514, 40, 10, (190, 30, 40) if i % 2 else (25, 25, 30))
        cv.text(30, 23, ['BREAKING', 'MONEY', 'ANALYSIS', 'EXPLAINER'][i % 4], 18, WHITE, 900, anchor='lm',
                shadow=False)
        for j, part in enumerate(text.split('\n')):
            cv.text(260, 95 + j * 52, part, 40, (20, 20, 25), 400, family='DMSerif', shadow=False)
    return sprite(('hl', text), 520, 200, draw)


def headline_storm(c, u, headlines, bg=(14, 18, 30)):
    """Made-up headline cards fly in from every side and pile up, faster and faster."""
    c.rrect(0, 0, VW, VH, 0, bg)
    rnd = random.Random(7)
    for i, h in enumerate(headlines):
        at = 0.12 * i + 0.02 * i * i * 0.3
        k = ease_out(clamp((u - at) / 0.35))
        if k <= 0:
            continue
        side = rnd.choice([(-600, 0), (1320, 0), (0, -400), (0, 1700)])
        tx, ty = 360 + rnd.uniform(-120, 120), 330 + (i * 97) % 680 + rnd.uniform(-40, 40)
        x = lerp(side[0] if side[0] else tx, tx, k)
        y = lerp(side[1] if side[1] else ty, ty, k)
        ang = rnd.uniform(-14, 14) * (1.6 - 0.6 * k)
        drift = 0.03 * u  # the pile keeps moving
        place(c, shadowed(_headline_card(h, i)), x + 20 * math.sin(u * 2 + i), y, 0.92 + drift, ang)


# ---------------------------------------------------------- 3 zoom through --
def zoom_through(c, u, dur, into_img, text='$', focus=(0.5, 0.5), label=None):
    """Dive into a big symbol: it grows past the screen (a white flash), and we come out inside a photo."""
    mid = dur * 0.4
    if u < mid:
        c.rrect(0, 0, VW, VH, 0, (14, 18, 30))
        c.text(360, 640, text, 240, GOLD, 400, family='Anton', stroke=6)
        zoom_canvas(c, math.exp(lerp(0, 3.4, ease(u / mid) ** 2)), 360, 610)  # dive into the symbol
        if u > mid - 0.12:
            c.rrect(0, 0, VW, VH, 0, (255, 255, 255, int(255 * seg(u, mid - 0.12, mid))))
        return
    v = u - mid
    photo(c, into_img, lerp(1.6, 1.15, ease_out(clamp(v / (dur - mid)))), focus, gray=True, tint=(40, 70, 120),
          dark=0.15)
    c.rrect(0, 0, VW, VH, 0, (255, 255, 255, int(255 * (1 - clamp(v / 0.25)))))
    if label:
        title(c, label, 330, 80, WHITE, pop(v, 0.2))


# ---------------------------------------------------------- 4 phone mockup --
def phone(c, x, y, s, screen):
    """A phone (centre x, y; scale s) whose screen content is drawn by screen(c, x0, y0, x1, y1)."""
    w, h = 330 * s, 680 * s
    x0, y0 = x - w / 2, y - h / 2
    c.rrect(x0 + 10, y0 + 18, x0 + w + 10, y0 + h + 18, 48 * s, (0, 0, 0, 90))
    c.rrect(x0, y0, x0 + w, y0 + h, 48 * s, (22, 24, 30), (90, 96, 110), 3)
    sx0, sy0, sx1, sy1 = x0 + 14 * s, y0 + 14 * s, x0 + w - 14 * s, y0 + h - 14 * s
    c.rrect(sx0, sy0, sx1, sy1, 38 * s, (246, 248, 252))
    c.rrect(x - 50 * s, sy0 + 10 * s, x + 50 * s, sy0 + 34 * s, 12 * s, (22, 24, 30))
    screen(c, sx0, sy0, sx1, sy1)


def phone_mockup(c, u, amount, bg_img=None):
    """A made-up banking app on a phone: the loan amount counts up, then APPROVED stamps on."""
    if bg_img:
        photo(c, bg_img, 1.2, (0.7, 0.6), blur=14, dark=0.55)
    else:
        c.rrect(0, 0, VW, VH, 0, (14, 18, 30))
    k = ease_out(clamp(u / 0.5))
    y = lerp(1500, 600, k)

    def screen(cv, x0, y0, x1, y1):
        cx = (x0 + x1) / 2
        cv.rrect(x0, y0 + 50, x1, y0 + 130, 0, (22, 60, 140))
        cv.text(cx, y0 + 90, 'COIN BANK', 26, WHITE, 900, shadow=False)
        cv.text(cx, y0 + 190, 'Home loan', 26, (90, 96, 110), 700, shadow=False)
        n = amount * ease(clamp((u - 0.6) / 1.0))
        cv.text(cx, y0 + 260, f'${n:,.0f}', 54, (20, 24, 32), 900, shadow=False)
        cv.text(cx, y0 + 320, 'deposited to your account', 20, (90, 96, 110), 600, shadow=False)
        kk = pop(u, 1.8, 0.35)
        if kk > 0:
            cv.rrect(cx - 130, y0 + 380, cx + 130, y0 + 450, 16, None, (0, 170, 90), 6, a=clamp(kk))
            cv.text(cx, y0 + 415, 'APPROVED', int(38 * (1.6 - 0.6 * clamp(kk))), (0, 170, 90), 900, a=clamp(kk),
                    shadow=False)
        cv.rrect(x0 + 30, y1 - 120, x1 - 30, y1 - 60, 30, (22, 60, 140))
        cv.text(cx, y1 - 90, 'View balance', 22, WHITE, 800, shadow=False)
    phone(c, 360, y, 1.0, screen)


# --------------------------------------------------------- 5 chat takeover --
def chat_takeover(c, u, msgs, step=0.55):
    """Chat bubbles pour in from the bottom and push older ones up until they fill the screen.
    msgs: list of (text, side) with side 'l' (them) or 'r' (us)."""
    c.rrect(0, 0, VW, VH, 0, (236, 238, 243))
    shown = [m for i, m in enumerate(msgs) if u >= i * step]
    y = 950  # stack sits above the captions
    for i in range(len(shown) - 1, -1, -1):
        text, side = shown[i]
        age = u - i * step
        k = ease_out(clamp(age / 0.25))
        lines = text.split('\n')
        h = 50 + 44 * len(lines)
        w = min(560, 40 + max(len(l) for l in lines) * 20)
        y -= h * k + 18
        if y < 150:
            break
        x0 = 40 if side == 'l' else VW - 40 - w
        col = (255, 255, 255) if side == 'l' else (40, 120, 255)
        tc = (25, 25, 30) if side == 'l' else WHITE
        sc = 0.6 + 0.4 * back_out(clamp(age / 0.3))
        cx, cy = x0 + w / 2, y + h / 2
        ww, hh = w * sc, h * sc
        c.rrect(cx - ww / 2, cy - hh / 2, cx + ww / 2, cy + hh / 2, 26, col)
        for j, l in enumerate(lines):
            c.text(cx, cy - 22 * (len(lines) - 1) + j * 44, l, int(32 * sc), tc, 700, shadow=False)
    nxt = len(shown)
    if nxt < len(msgs):  # typing dots
        for d in range(3):
            c.circle(80 + d * 28, 985, 9 + 3 * abs(math.sin(u * 8 + d)), (150, 150, 160))


# ----------------------------------------------------------- 6 green screen --
def ledger(c, top=0):
    c.rrect(0, top, VW, VH, 0, (238, 232, 210))
    for i in range(30):
        y = top + 40 + i * 44
        c.line([(40, y), (680, y)], (170, 190, 210), 2)
    c.line([(470, top), (470, VH)], (210, 120, 120), 3)
    rnd = random.Random(11)
    for i in range(1, 29, 2):
        c.text(80, top + 40 + i * 44 - 4, rnd.choice(['Loan #', 'Deposit', 'Transfer', 'Interest']) +
               f' {rnd.randint(1000, 9999)}', 22, (80, 80, 100), 600, anchor='lm', shadow=False)
        c.text(650, top + 40 + i * 44 - 4, f'{rnd.randint(1, 900):,}.{rnd.randint(10, 99)}', 22, (60, 60, 80), 700,
               anchor='rm', shadow=False)


def green_screen(c, u, t_abs, key_at=0.4, key_dur=0.8):
    """Penny on a green screen; a keying sweep wipes the green away and drops her onto a giant ledger."""
    ledger(c)
    k = clamp((u - key_at) / key_dur)
    edge = VH * (1 - ease(k))
    if edge > 0:
        c.rrect(0, 0, VW, edge, 0, GREEN)
        c.line([(0, edge), (VW, edge)], (180, 255, 200), 6)
        if k > 0:
            c.text(360, max(180, edge - 40), 'KEYING...', 24, WHITE, 900, a=1 - k)
    c.rrect(160, 850, 560, 980, 20, (90, 60, 40))  # desk
    c.rrect(250, 770, 470, 860, 10, (40, 44, 56))  # laptop
    c.text(360, 815, '$300,000', 28, MINT, 900, a=fade(u, 0.9), shadow=False)
    penny(c, 360, 640, 110, t_abs, 'happy', look=(0, 0.4), arms=(60, 120))


# ---------------------------------------------------------- 7 digital zoom --
def digital_zoom(c, u, value, label='new money'):
    """'Enhance!': a screen of digits, a target box, then a pixelated zoom that sharpens on the number."""
    c.rrect(0, 0, VW, VH, 0, (8, 12, 20))
    rnd = random.Random(5)
    for i in range(26):
        for j in range(10):
            c.text(36 + j * 70, 160 + i * 42, str(rnd.randint(0, 9)), 26, (40, 90, 70), 700, shadow=False)
    digits = f'{value:,}'
    n = int(len(digits) * clamp((u - 0.1) / 0.8))
    c.rrect(80, 560, 640, 720, 14, (8, 12, 20), MINT, 4)
    c.text(360, 640, digits[:n] + ('|' if (u * 3) % 1 < 0.5 else ''), 80, MINT, 900, family='Montserrat')
    kz = clamp((u - 1.0) / 0.9)
    if kz > 0:
        z = lerp(1, 1.25, ease(kz))
        zoom_canvas(c, z, 360, 640)
        px = int(lerp(28, 1, ease(kz)) * c.k / 3)
        if px > 1:  # pixelated mid-zoom, sharpening as it lands
            w, h = c.img.size
            c.img.paste(c.img.resize((w // px, h // px), Image.NEAREST).resize((w, h), Image.NEAREST))
    if u < 1.0:
        s = 1 - 0.3 * ease(clamp(u / 0.8))
        c.rrect(360 - 300 * s, 640 - 110 * s, 360 + 300 * s, 640 + 110 * s, 6, None, CORAL, 4)
        c.text(360, 640 - 130 * s, 'ENHANCE', 22, CORAL, 900)
    title(c, label.upper(), 960, 64, GOLD, pop(u, 1.6))


# ---------------------------------------------------------- 8 paper cutout --
def _paper(key, w, h, color, lines, ink=(30, 30, 35)):
    def draw(cv):
        rnd = random.Random(hash(key) & 0xffff)
        pts = []
        for i in range(24):  # hand-cut edge
            a = 2 * math.pi * i / 24
            rx, ry = w / 2 - 12 + rnd.uniform(-5, 5), h / 2 - 12 + rnd.uniform(-5, 5)
            pts.append((w / 2 + max(-1, min(1, math.cos(a) * 1.6)) * rx, h / 2 + max(-1, min(1, math.sin(a) * 1.6)) * ry))
        cv.poly([(x + 6, y + 6) for x, y in pts], (255, 255, 255))
        cv.poly(pts, color)
        for j, (txt, size) in enumerate(lines):
            cv.text(w / 2, h / 2 - (len(lines) - 1) * size * 0.6 + j * size * 1.2, txt, size, ink, 400,
                    family='Anton', shadow=False)
    return sprite(('paper', key), w, h, draw)


def paper_cutout(c, u, left, right, mid='=', bg=PAPER):
    """Stop-motion paper pieces (2 frames a beat, slight wobble) slide in and lock together."""
    c.rrect(0, 0, VW, VH, 0, bg)
    rnd = random.Random(int(u * 8))  # wobble changes 8 times a second: the stop-motion look
    for i in range(40):
        c.circle(random.Random(i).uniform(0, VW), random.Random(i + 99).uniform(0, VH), 2, (210, 200, 180))
    kl, kr = ease_out(clamp(u / 0.45)), ease_out(clamp((u - 0.6) / 0.45))
    a = shadowed(_paper('L' + left[0][0], 300, 300, CORAL, left), 10, (6, 10), 0.4)
    b = shadowed(_paper('R' + right[0][0], 300, 300, MINT, right), 10, (6, 10), 0.4)
    place(c, a, lerp(-200, 360, kl), 400, 1, rnd.uniform(-3, 3) - 4 * (1 - kl))
    place(c, b, lerp(920, 360, kr), 780, 1, rnd.uniform(-3, 3) + 4 * (1 - kr))
    k = pop(u, 1.2)
    if k > 0:
        c.text(360, 590, mid, int(110 * clamp(k)), INK, 400, family='Anton', shadow=False)


# --------------------------------------------------------- 9 magazine cover --
def magazine_cover(c, u, img, mast, quote, attrib, focus=(0.5, 0.5)):
    """A made-up magazine cover drops onto a table: masthead, cover photo, the quote as the cover line."""
    c.rrect(0, 0, VW, VH, 0, (60, 42, 30))
    for i in range(0, VH, 36):  # wood grain
        c.line([(0, i), (VW, i + 10)], (75, 52, 36), 3)
    k = ease_out(clamp(u / 0.5))

    def cover_spr():
        key = ('mag', mast, quote)
        if key not in _cache:
            w, h = 600, 960
            img_ = Image.new('RGBA', (int(w * K), int(h * K)), (0, 0, 0, 255))
            img_.paste(photo_img(img, w * K, h * K, 1.0, focus, sat=1.1))
            cv = Canvas(img=img_, k=K)
            cv.rrect(0, 0, w, 210, 0, (0, 0, 0, 90))
            cv.text(w / 2, 110, mast, 110, (255, 255, 255), 400, family='DMSerif', shadow=False)
            cv.rrect(0, h - 330, w, h, 0, (0, 0, 0, 150))
            for j, part in enumerate(quote.split('\n')):
                cv.text(w / 2, h - 270 + j * 62, part, 50, GOLD, 400, family='DMSerif')
            cv.text(w / 2, h - 60, attrib, 24, WHITE, 700)
            cv.text(40, 260, 'SPECIAL', 22, WHITE, 900, anchor='lm')
            cv.text(40, 290, 'REPORT', 22, WHITE, 900, anchor='lm')
            _cache[key] = img_
        return _cache[key]
    place(c, shadowed(cover_spr(), 26, (10, 24), 0.7), 360, 590, lerp(1.2, 0.8, k), lerp(-12, -3, k))


# ----------------------------------------------------------- 10 liquid glass --
def glass_panel(c, x0, y0, x1, y1, r=36, tint=(255, 255, 255)):
    """Frosted-glass panel: blur what's behind it, brighten, add a rim light and a sheen."""
    b = (int(x0 * c.k), int(y0 * c.k), int(x1 * c.k), int(y1 * c.k))
    region = c.img.crop(b).filter(ImageFilter.GaussianBlur(10 * c.k))
    region = ImageEnhance.Brightness(region).enhance(1.25)
    mask = Image.new('L', region.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, region.size[0] - 1, region.size[1] - 1], radius=int(r * c.k),
                                           fill=255)
    c.img.paste(region, b[:2], mask)
    c.rrect(x0, y0, x1, y1, r, tint + (34,), (255, 255, 255, 140), 2)
    c.rrect(x0 + 8, y0 + 8, x1 - 8, y0 + (y1 - y0) * 0.35, r - 8, (255, 255, 255, 26))


def liquid_glass(c, u, bg_img, cards, focus=(0.5, 0.5)):
    """Big glass cards float over a blurred photo, wobbling like liquid. cards: (big, small, color)."""
    photo(c, bg_img, 1.2 + 0.05 * u, focus, sat=1.3, dark=0.2)
    for i in range(6):  # moving colour blobs behind the glass
        cx = 360 + 260 * math.sin(u * 0.9 + i * 1.7)
        cy = 640 + 420 * math.cos(u * 0.7 + i * 2.3)
        c.circle(cx, cy, 120, ((GOLD, MINT, SKY)[i % 3]) + (90,))
    for i, (big_t, small, col) in enumerate(cards):
        at = 0.3 + i * 0.9
        k = ease_out(clamp((u - at) / 0.5))
        if k <= 0:
            continue
        wob = 6 * math.sin(u * 3 + i)
        y0 = 330 + i * 340 + 60 * (1 - k)
        glass_panel(c, 70 + wob, y0, 650 + wob, y0 + 280)
        c.text(360 + wob, y0 + 115, big_t, int(120 * (0.7 + 0.3 * k)), col, 400, family='Anton', a=k, stroke=4)
        c.text(360 + wob, y0 + 220, small, 32, WHITE, 900, a=k)


# ---------------------------------------------------------------- 11 orbit --
def bill_spr():
    def draw(cv):
        cv.rrect(4, 4, 156, 76, 8, (120, 170, 110), (60, 100, 60), 3)
        cv.circle(80, 40, 22, (160, 200, 150), (60, 100, 60), 2)
        cv.text(80, 41, '$', 28, (40, 80, 40), 900, shadow=False)
    return sprite('bill', 160, 80, draw)


def orbit(c, u, center_text, center_sub, n=9):
    """Coins and bills orbit a tiny pile of cash on a tilted ring (3D-ish: they shrink and dim behind it)."""
    c.rrect(0, 0, VW, VH, 0, (14, 18, 30))
    cx, cy, rx, ry = 360, 560, 290, 110
    c.ellipse(cx, cy, rx, ry, None, (255, 255, 255, 40), 2)
    items = []
    for i in range(n):
        a = u * 1.4 + 2 * math.pi * i / n
        x, y, d = cx + rx * math.cos(a), cy + ry * math.sin(a), math.sin(a)
        items.append((d, x, y, i))
    for d, x, y, i in sorted(items):
        s = 0.7 + 0.35 * (d + 1) / 2
        al = 0.45 + 0.55 * (d + 1) / 2
        if i % 3 == 0:
            place(c, bill_spr(), x, y, 0.6 * s, math.degrees(math.sin(u + i)) * 0.3, al)
        else:
            c.circle(x, y, 26 * s, GOLD + (int(255 * al),), (180, 130, 30, int(255 * al)), 3)
        if d < 0 and i == items[-1][3]:
            pass
    k = pop(u, 0.2)
    place(c, bill_spr(), cx, cy - 10, 0.9 * clamp(k))
    place(c, bill_spr(), cx + 8, cy - 26, 0.9 * clamp(k), 6)
    title(c, center_text, 830, 100, GOLD, pop(u, 0.6))
    c.text(360, 950, center_sub, 28, WHITE, 800, a=fade(u, 0.9))


# --------------------------------------------------------- 12 growth curve --
def growth_curve(c, u, xs, ys, label_end, label_start, dur=2.6, ttl='US money supply'):
    """The line draws itself with a glowing head; the end value pops at the top."""
    c.rrect(0, 0, VW, VH, 0, (14, 18, 30))
    k = ease(clamp(u / dur))
    c.text(360, 230, ttl, 40, WHITE, 900, a=fade(u, 0))
    px, py = line_chart(c, (70, 330, 650, 900), xs, ys, (xs[0], xs[-1]), (0, max(ys) * 1.08), k, MINT,
                        xticks=range(1960, 2030, 20), yticks=(), a=1)
    i = max(1, int(k * (len(xs) - 1)))
    hx, hy = px(xs[i]), py(ys[i])
    c.circle(hx, hy, 22, MINT + (70,))
    c.circle(hx, hy, 10, WHITE)
    c.text(px(xs[0]) + 10, py(ys[0]) - 40, label_start, 30, MUTED, 900, anchor='lm', a=fade(u, 0.2))
    kk = pop(u, dur)
    if kk > 0:
        c.text(px(xs[-1]) - 10, py(ys[-1]) - 50, label_end, int(64 * (0.7 + 0.3 * clamp(kk))), GOLD, 400,
               family='Anton', anchor='rm', a=clamp(kk), stroke=4)


# --------------------------------------------------------- 13 frame escape --
def frame_escape(c, u, t_abs, inside, question):
    """Penny climbs out of a framed picture, over its edge and into our world."""
    c.rrect(0, 0, VW, VH, 0, (24, 20, 34))
    x0, y0, x1, y1 = 100, 330, 620, 890
    inside(c, x0, y0, x1, y1)  # the picture inside the frame
    k = ease(clamp(u / 1.4))
    py = lerp(840, 300, k)  # Penny rises from inside the frame to standing on its top edge
    if k < 0.55:  # still inside: the frame covers her lower half
        penny(c, 360, py, 80, t_abs, 'shocked', look=(0, -0.4))
        c.rrect(x0 - 30, y1, x1 + 30, y1 + 300, 0, (24, 20, 34))
    c.rrect(x0 - 24, y0 - 24, x1 + 24, y1 + 24, 8, None, (200, 160, 80), 22)
    c.rrect(x0 - 8, y0 - 8, x1 + 8, y1 + 8, 4, None, (120, 90, 40), 6)
    if k >= 0.55:  # out: in front of the frame
        penny(c, 360, py, 80, t_abs, 'worried', look=(0, 0.3), arms=(20, 160))
    title(c, question, 1000, 62, WHITE, pop(u, 0.9))


# ------------------------------------------------------- 14 checklist pop --
def checklist_pop(c, u, items, step=0.9, ttl=None):
    """Boxes pop in one by one; each gets a big check that overshoots."""
    c.rrect(0, 0, VW, VH, 0, (14, 18, 30))
    if ttl:
        title(c, ttl, 240, 64, GOLD, pop(u, 0))
    for i, txt in enumerate(items):
        at = 0.2 + i * step
        k = pop(u, at, 0.35)
        if k <= 0:
            continue
        y = 420 + i * 190
        s = 0.6 + 0.4 * back_out(clamp((u - at) / 0.35))
        c.rrect(60, y - 75 * s, 660, y + 75 * s, 26, (255, 255, 255, 18), (255, 255, 255, 60), 2)
        c.rrect(90, y - 40, 170, y + 40, 14, None, WHITE, 5)
        kc = pop(u, at + 0.3, 0.3)
        if kc > 0:
            c.icon('check', 130, y - 6, 110 * (0.6 + 0.6 * back_out(clamp((u - at - 0.3) / 0.3))), MINT, stroke=3.5)
        c.text(200, y, txt, 38, WHITE, 900, anchor='lm', a=clamp(k))


# ----------------------------------------------------- 15 checklist tally --
def checklist_tally(c, u, start, end, label, stamp):
    """A counter rolls down, tally marks get struck through, then a date stamp slams on."""
    c.rrect(0, 0, VW, VH, 0, (14, 18, 30))
    c.text(360, 260, label, 40, WHITE, 900, a=fade(u, 0))
    k = ease(clamp((u - 0.3) / 1.4))
    v = round(lerp(start, end, k))
    c.text(360, 520, f'{v}%', 220, CORAL if v else MINT, 400, family='Anton', stroke=6)
    for i in range(start):  # one tally mark per point, struck through as the counter passes it
        x = 150 + i * 46
        c.line([(x, 700), (x, 800)], WHITE, 8)
        if v <= start - 1 - i:
            c.line([(x - 20, 790), (x + 20, 710)], CORAL, 8)
    ks = pop(u, 1.9, 0.25)
    if ks > 0:
        sc = lerp(2.2, 1.0, clamp(ks))
        c.rrect(360 - 220 * sc, 900 - 60 * sc, 360 + 220 * sc, 900 + 60 * sc, 12, None, CORAL, 8, a=clamp(ks))
        c.text(360, 900, stamp, int(64 * sc), CORAL, 400, family='Anton', a=clamp(ks), shadow=False)


# --------------------------------------------------------- 16 b-roll overlay --
def broll_overlay(c, u, img, top, bottom, focus=(0.5, 0.5)):
    """A slow drift over a photo with bold lower-third style text and money dissolving into dust."""
    photo(c, img, 1.25 + 0.08 * u, (focus[0] + 0.02 * u, focus[1]), sat=1.2, dark=0.3)
    c.rrect(0, 0, VW, VH, 0, (0, 0, 0, 70))
    title(c, top, 300, 70, WHITE, pop(u, 0.1))
    k = clamp((u - 0.9) / 1.2)
    place(c, bill_spr(), 360, 660, 1.6, 0, 1 - k)
    rnd = random.Random(21)
    for i in range(60):  # the bill turns to dust
        if k <= 0:
            break
        sx, sy = 360 + rnd.uniform(-120, 120), 660 + rnd.uniform(-60, 60)
        c.circle(sx + rnd.uniform(-1, 1) * 200 * k, sy - rnd.uniform(0.3, 1) * 260 * k, 5 * (1 - k) + 1,
                 (140, 190, 130, int(255 * (1 - k))))
    title(c, bottom, 880, 84, CORAL, pop(u, 1.4))


# ------------------------------------------------------------ 17 zoom portal --
def zoom_portal(c, u, inner, text):
    """A glowing ring opens in the middle and we fly through it into the next picture (inner(c))."""
    c.rrect(0, 0, VW, VH, 0, (10, 10, 22))
    k = ease(clamp(u / 1.6))
    r = lerp(10, 900, k ** 2)
    layer = Image.new('RGBA', c.img.size, (0, 0, 0, 0))
    cv = Canvas(img=layer, k=c.k)
    inner(cv)
    mask = Image.new('L', c.img.size, 0)
    ImageDraw.Draw(mask).ellipse([(360 - r) * c.k, (640 - r) * c.k, (360 + r) * c.k, (640 + r) * c.k], fill=255)
    c.img.paste(layer, (0, 0), Image.composite(layer.getchannel('A'), mask, mask))
    for j in range(16):  # spinning ring segments
        a0 = u * 120 + j * 22.5
        c.arc(360, 640, r + 10, a0, a0 + 12, (SKY, GOLD)[j % 2], 10)
    c.circle(360, 640, r + 24, None, (120, 180, 255, 80), 8)
    if k < 0.6:
        title(c, text, 1020, 60, WHITE, pop(u, 0.1))


# ------------------------------------------------------------ 18 frame break --
def frame_break(c, u, t_abs, before, after):
    """Penny punches through the screen: cracks spread, shards fly, and `after` is behind the glass."""
    hit = 0.5
    if u < hit:
        before(c)
        penny(c, 360, lerp(1100, 700, ease(u / hit)), lerp(60, 140, ease(u / hit)), t_abs, 'shocked')
        return
    after(c)
    v = u - hit
    layer = Image.new('RGBA', c.img.size, (0, 0, 0, 0))
    lc = Canvas(img=layer, k=c.k)
    before(lc)
    rnd = random.Random(4)
    for i in range(18):  # shards of the old frame fly outward and fall
        a = 2 * math.pi * i / 18 + rnd.uniform(-0.1, 0.1)
        d = 60 + 900 * ease_out(clamp(v / 0.9))
        cx, cy = 360 + math.cos(a) * d, 640 + math.sin(a) * d + 400 * v * v
        size = rnd.uniform(60, 140)
        pts = [(cx + size * math.cos(a + o), cy + size * math.sin(a + o)) for o in (0, 2.2, 4.1)]
        c.poly(pts, (220, 230, 255, int(200 * (1 - clamp(v / 1.0)))), (255, 255, 255, 220), 2)
    for i in range(10):  # crack lines at the moment of impact
        a = 2 * math.pi * i / 10
        if v < 0.35:
            c.line([(360, 640), (360 + math.cos(a) * 500, 640 + math.sin(a) * 500)], (255, 255, 255, int(255 * (1 - v / 0.35))), 4)
    c.rrect(0, 0, VW, VH, 0, (255, 255, 255, int(200 * (1 - clamp(v / 0.15)))))
