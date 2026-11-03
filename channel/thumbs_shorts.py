#!/usr/bin/env python3
"""Three vertical (9:16) thumbnails for every Short: A = light burst + drawn object, B = real photo / footage frame,
C = colour slab + Penny's reaction. Text only from each video's already-verified title numbers.

    python3 channel/thumbs_shorts.py [name ...]    ->  out/thumbs/<name>_[abc].jpg + a squint sheet per Short
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from wk2_art import *  # noqa: E402,F401,F403
import thumbkit  # noqa: E402
from thumbkit import Thumb, hexrgb  # noqa: E402
from PIL import Image, ImageEnhance  # noqa: E402
import numpy as np  # noqa: E402

VW, VH = 720, 1280
thumbkit.TW, thumbkit.TH = int(VW * K), int(VH * K)  # the kit draws at K x the logical size
OUT = os.path.join(HERE, 'out', 'thumbs')
SRC = os.path.join(HERE, 'assets', 'thumbsrc')
A = os.path.join(HERE, 'assets')


def P(name):
    for p in (os.path.join(SRC, name + '.jpg'), os.path.join(A, name)):
        if os.path.exists(p):
            return p
    raise FileNotFoundError(name)


# name: big text, small line, burst colours, photo, object, slab colour
SPEC = {
    'ep01_short_prices': ('1980\nvs NOW', 'BREAD · EGGS · GAS', ('#ff9f43', '#7a1f0f'), 'shoppers1962', 'tag', CORAL),
    'ep01_short_rule70': ('RULE\nOF 70', 'HOW FAST MONEY SHRINKS', ('#a78bfa', '#2e1065'), 'calendar', 'bill', SKY),
    'ep01_short_wages': ('RAISE?', "DOESN'T FEEL LIKE ONE", ('#34d399', '#064e3b'), 'cashhands', 'bill', MINT),
    'ep02_short_payment': ('+$876', 'A MONTH, SAME HOUSE', ('#60a5fa', '#0b1f4d'), 'photos/ep06s/houses.jpg', 'tag', SKY),
    'ep02_short_price': ('$23,000', 'A HOUSE IN 1970', ('#fbbf24', '#7c2d12'), 'photos/ep06s/houses.jpg', 'tag', GOLD),
    'ep02_short_supply': ('STOPPED\nBUILDING', 'AMERICA', ('#f87171', '#450a0a'), 'photos/ep06s/houses.jpg', None, CORAL),
    'ep03_short_barrel': ('1\nGALLON', 'WHAT YOU REALLY PAY FOR', ('#fb923c', '#431407'), None, 'pump', GOLD),
    'ep03_short_feathers': ('UP FAST\nDOWN SLOW', 'GAS PRICES', ('#f87171', '#3b0764'), None, 'pump', CORAL),
    'ep03_short_jump': ('$4.50', 'FROM $2.78 IN 4 MONTHS', ('#ef4444', '#450a0a'), None, 'pump', CORAL),
    'ep04_short_cards': ('21%', 'ON YOUR CREDIT CARD', ('#f43f5e', '#4c0519'), 'tap', 'card', CORAL),
    'ep04_short_savings': ('0.38%', 'vs 3.7% INFLATION', ('#38bdf8', '#082f49'), 'piggy', 'bill', SKY),
    'ep04_short_why': ('GAS UP\nRATES UP', 'WHY?', ('#fbbf24', '#1e3a8a'), 'photos/fed_eccles.jpg', 'pump', GOLD),
    'ep05_short_hiring': ('NOBODY\nHIRING', 'THE REAL JOB PROBLEM', ('#94a3b8', '#0f172a'), 'phonewoman', None, SKY),
    'ep05_short_layoffs': ('LOWER\nTHAN 2019', 'LAYOFFS', ('#34d399', '#022c22'), 'calendar', None, MINT),
    'ep06_short_banks': ('FROM\nNOTHING', 'HOW BANKS MAKE MONEY', ('#fbbf24', '#422006'), 'photos/ep06s/vault.png', 'bill', GOLD),
    'ep07_short_hack': ('$6.3B', 'GONE IN 20 MINUTES', ('#f43f5e', '#0c0a09'), 'flow/binance_vault.jpg', None, CORAL),
    'ep08_short_midterms': ('18 / 18', 'STOCKS AFTER MIDTERMS', ('#34d399', '#052e16'), 'flow/ep08/img6.jpg', None, MINT),
    'sx01_short_compound': ('2X', 'SAME $200 A MONTH', ('#34d399', '#064e3b'), 'cashjar', 'bill', MINT),
    'sx02_short_cards': ('19\nYEARS', 'PAYING THE MINIMUM', ('#f87171', '#450a0a'), 'tap', 'card', CORAL),
    'sx03_short_1962': ('$1,112', '$100 IN 1962, TODAY', ('#fbbf24', '#451a03'), 'shoppers1962', 'bill', GOLD),
    'sx04_short_middle': ('52%', 'ARE YOU MIDDLE CLASS?', ('#fbbf24', '#1e1b4b'), 'gen/sx04/canva_thumb.png', None, GOLD),
    'sx10_short_midterm_stocks': ('19 / 19', 'STOCKS AFTER MIDTERMS', ('#34d399', '#052e16'), 'cashsuit', None, MINT),
}


def photo_bg(path, focus=(0.5, 0.45)):
    im = Image.open(path).convert('RGB')
    w, h = im.size
    tw, th = thumbkit.TW, thumbkit.TH
    cw = min(w, h * tw / th)
    ch = cw * th / tw
    x0 = min(max(focus[0] * w - cw / 2, 0), w - cw)
    y0 = min(max(focus[1] * h - ch / 2, 0), h - ch)
    im = im.resize((tw, th), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch))
    im = ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(1.3)).enhance(1.12)
    yy = np.linspace(0, 1, th // 8)[:, None] * np.ones((1, tw // 8))  # darker top and bottom for the text
    m = 1 - 0.62 * np.clip(np.maximum(1 - yy / 0.45, (yy - 0.7) / 0.3), 0, 1) ** 1.2
    v = Image.fromarray((np.clip(m, 0, 1) * 255).astype('uint8'), 'L').resize((tw, th))
    im = Image.composite(im, Image.new('RGB', im.size, (6, 8, 16)), v)
    t = Thumb.__new__(Thumb)
    t.img = im.convert('RGBA')
    return t


def draw_obj(kind, cx, cy, s):
    def d(c):
        if kind == 'pump':
            gas_pump(c, cx, cy + 130 * s, 1.5 * s, '$4.50', color=CORAL)
        elif kind == 'card':
            card(c, cx, cy, 1.35 * s, color=SKY)
        elif kind == 'bill':
            bill(c, cx, cy, 400 * s, '100')
        elif kind == 'tag':
            price_tag(c, cx, cy, 2.6 * s, '$?')
    return d


def big_text(th, txt, y, size, color, glow):
    lines = txt.split('\n')
    for i, ln in enumerate(lines):
        sz = size if len(ln) <= 6 else int(size * 6.5 / len(ln)) + 10
        th.text(VW / 2, y + i * size * 0.98, ln, sz, color=color, stroke=14, glow=glow)


def variant_a(name):  # light burst, object, number
    big, sub, burst, photo, obj, col = SPEC[name]
    th = Thumb(burst, center=(0.5, 0.55))
    th.text(VW / 2, 150, sub, 44 if len(sub) < 20 else 36, color=WHITE, stroke=9)
    big_text(th, big, 340, 190, WHITE, col)
    if obj:
        th.layer(draw_obj(obj, VW / 2, 930, 1.0), outline=10, glow=(255, 240, 180), tilt=-6)
    else:
        th.layer(lambda c: penny(c, VW / 2, 950, 150, 0.0, 'shocked', bounce=False, arms=(200, -20)), outline=10,
                 glow=(255, 240, 160))
    return th


def variant_b(name):  # real photo / footage frame
    big, sub, burst, photo, obj, col = SPEC[name]
    if photo:
        th = photo_bg(P(photo))
    else:
        th = Thumb((burst[1], '#000000'), center=(0.5, 0.6), rays=0)
        th.layer(draw_obj(obj, VW / 2, 820, 1.25), outline=12, glow=col)
    big_text(th, big, 230, 175, col, (0, 0, 0))
    c_sub = 46 if len(sub) < 20 else 38
    th.layer(lambda c: c.rrect(60, 1040, 660, 1130, 40, col), outline=0, shadow=True)
    th.text(VW / 2, 1085, sub, c_sub, color=INK, stroke=0)
    return th


def variant_c(name):  # colour slab + Penny's reaction
    big, sub, burst, photo, obj, col = SPEC[name]
    th = Thumb(('#1b2338', '#05070d'), center=(0.5, 0.4), rays=12)
    th.layer(lambda c: c.rrect(40, 230, 680, 700, 46, col), outline=8, tilt=-3, pivot=(360, 465))
    lines = big.split('\n')
    for i, ln in enumerate(lines):
        sz = 170 if len(ln) <= 6 else int(170 * 6.5 / len(ln)) + 8
        th.text(VW / 2, 470 - (len(lines) - 1) * 80 + i * 165, ln, sz, color=INK, stroke=0, tilt=-3)
    th.text(VW / 2, 800, sub, 44 if len(sub) < 20 else 36, color=WHITE, stroke=9)
    th.layer(lambda c: penny(c, VW / 2, 1040, 135, 0.0, 'shocked', look=(0, -1), bounce=False, arms=(210, -30)),
             outline=10, glow=(255, 240, 160))
    return th


def save(th, path):
    th.img.convert('RGB').resize((1080, 1920), Image.LANCZOS).save(path, quality=90)
    return path


def sheet(paths, out):
    ims = [Image.open(p).convert('RGB') for p in paths]
    w = 360
    sh = Image.new('RGB', (len(ims) * (w + 10) + (len(ims)) * 100, 650), (255, 255, 255))
    x = 0
    for im in ims:
        sh.paste(im.resize((w, 640)), (x, 5))
        sh.paste(im.resize((90, 160)), (x + w + 5, 5))  # phone-feed size
        x += w + 110
    sh.save(out)
    return out


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    names = sys.argv[1:] or list(SPEC)
    for n in names:
        ps = [save(f(n), os.path.join(OUT, f'{n}_{v}.jpg')) for f, v in
              ((variant_a, 'a'), (variant_b, 'b'), (variant_c, 'c'))]
        sheet(ps, os.path.join(OUT, f'{n}_sheet.png'))
        print('ok', n)
