#!/usr/bin/env python3
"""Thumbnails v3: three hook types per video on photo-real backgrounds (Canva AI images, owner's footage, Flow art).

    A = SHOCK NUMBER       (one huge verified number/claim)
    B = CURIOSITY WORD     (2-3 words + red "news alert" bar on timely topics)
    C = YOU-STAKES         (fictional shocked face + a question to the viewer)

Built from what the most-clicked finance thumbnails of Aug-Nov 2026 do (face + emotion, 1-4 huge words, one big
number, red alert bars, money in danger). Text is only from each video's verified title/script numbers.

    python3 channel/thumbs_v3.py [name ...]   ->  out/thumbs/<name>_[abc].jpg  + out/thumbs/<name>_sheet.png
Backgrounds: assets/thumbsrc/ai/<name>_<n>.png (exported from Canva), assets/thumbsrc/*.jpg, assets/photos, flow.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from wk2_art import *  # noqa: E402,F401,F403
import thumbkit  # noqa: E402
from thumbkit import Thumb  # noqa: E402
from PIL import Image, ImageEnhance  # noqa: E402
import numpy as np  # noqa: E402

OUT = os.path.join(HERE, 'out', 'thumbs')
AS = os.path.join(HERE, 'assets')
RED, YEL, GRN = (230, 30, 40), (255, 214, 0), (40, 220, 110)

# name: (vertical?, A text, B text, C text, accent, B background (photo key or None = AI #1), alert bar on B?)
SPEC = {
    'ep01_short_prices': (1, '1980\nvs NOW', 'SAME CART\nNEW PRICE', 'YOU PAY\nHOW MUCH?', YEL, 'shoppers1962', 0),
    'ep01_short_rule70': (1, 'RULE\nOF 70', 'MONEY\nMELTING', 'YOUR CASH\nHALVES?', YEL, None, 0),
    'ep01_short_wages': (1, 'RAISE =\nPAY CUT?', 'EATEN BY\nINFLATION', 'IS YOUR\nRAISE REAL?', GRN, 'cashhands', 0),
    'ep02_short_payment': (1, '+$876\n/MONTH', 'SAME\nHOUSE', 'CAN YOU\nAFFORD IT?', YEL, None, 0),
    'ep02_short_price': (1, '$23,000', 'IN\n1970', 'NOW\nGUESS?', YEL, None, 0),
    'ep02_short_supply': (1, 'STOPPED\nBUILDING', 'HOUSING\nSHORTAGE', 'WHERE ARE\nTHE HOMES?', RED, None, 1),
    'ep03_short_barrel': (1, '1\nGALLON', 'WHERE\nIT GOES', 'YOU PAY\nFOR WHAT?', YEL, None, 0),
    'ep03_short_feathers': (1, 'UP FAST\nDOWN SLOW', 'ROCKETS &\nFEATHERS', 'WHY NOT\nCHEAPER?', RED, None, 0),
    'ep03_short_jump': (1, '$4.50', 'GAS\nSHOCK', 'FROM\n$2.78?!', RED, None, 1),
    'ep04_short_cards': (1, '21%', 'CARD\nTRAP', 'YOUR\nCARD?', RED, 'tap', 0),
    'ep04_short_savings': (1, '0.38%', 'LOSING\nVALUE', 'YOUR\nSAVINGS?', YEL, 'piggy', 0),
    'ep04_short_why': (1, 'GAS UP\nRATES UP', 'THE\nLINK', 'WHY?', YEL, 'photos/fed_eccles.jpg', 1),
    'ep05_short_hiring': (1, 'NOBODY\nHIRING', 'THE REAL\nPROBLEM', "CAN'T FIND\nA JOB?", YEL, None, 1),
    'ep05_short_layoffs': (1, 'LOWER\nTHAN 2019', 'LAYOFF\nMYTH', 'SCARED OF\nLAYOFFS?', GRN, None, 0),
    'ep06_short_banks': (1, 'FROM\nNOTHING', 'MONEY FROM\nTHIN AIR', 'WHERE MONEY\nCOMES FROM', YEL, 'photos/ep06s/vault.png', 0),
    'ep07_short_hack': (1, '$6.3B', '20\nMINUTES', 'GONE.', RED, 'flow/binance_vault.jpg', 1),
    'ep08_short_midterms': (1, '18 / 18', 'NEVER\nFAILED', 'WILL 2026\nBREAK IT?', GRN, 'flow/ep08/img6.jpg', 1),
    'sx01_short_compound': (1, '2X', 'SAME\n$200', 'START\nEARLY?', GRN, 'cashjar', 0),
    'sx02_short_cards': (1, '19\nYEARS', 'MINIMUM\nTRAP', 'PAY THE\nMINIMUM?', RED, 'tap', 0),
    'sx03_short_1962': (1, '$1,112', '1962', 'YOUR $100\nTODAY?', YEL, 'shoppers1962', 0),
    'sx04_short_middle': (1, '52%', 'MIDDLE\nCLASS?', 'ARE\nYOU?', YEL, None, 0),
    'sx10_short_midterm_stocks': (1, '19 / 19', 'NEVER\nDOWN', '20 FOR\n20?', GRN, 'cashsuit', 1),
    'ep01_inflation': (0, '$100\nNOW $12', 'WHERE\nIT WENT', 'YOUR\n$100?', YEL, None, 0),
    'ep02_housing': (0, '$23K\nNOW $393K', 'PRICED\nOUT', 'WILL YOU\nEVER BUY?', YEL, None, 0),
    'ep03_gas': (0, '$4.50', 'OIL\nSHOCK', 'WHY SO\nHIGH?', RED, None, 1),
    'ep04_fed': (0, 'RATES\nUP', 'YOUR\nLOANS', 'WHAT\nNOW?', RED, 'photos/fed_eccles.jpg', 1),
    'ep07_binance_long': (0, '$6.3B\nSTOLEN', '20\nMINUTES', 'IS YOUR\nCRYPTO SAFE?', RED, None, 1,
                          ('flow/binance_shock.jpg', 'flow/binance_vault.jpg', 'flow/binance_safe.jpg')),
    'ep08_midterms': (0, '18 / 18', 'NEVER\nFAILED', 'WILL 2026\nBREAK IT?', GRN, None, 1,
                      ('flow/ep08/img6.jpg', 'flow/ep08/img3.jpg', 'flow/ep08/img1.jpg')),
    'ep05_jobs': (0, '60,000\nBUYOUTS', 'LAYOFFS?', 'IS YOUR\nJOB SAFE?', YEL, None, 1),
}


def find(key):
    for p in (os.path.join(AS, 'thumbsrc', key + '.jpg'), os.path.join(AS, key)):
        if os.path.exists(p):
            return p
    raise FileNotFoundError(key)


def ai(name, n):
    p = os.path.join(AS, 'thumbsrc', 'ai', f'{name}_{n}.png')
    return p if os.path.exists(p) else None


def bg(path, vertical, focus=(0.5, 0.5), zoom=1.0, dark=0.55, flip=False):
    """Cover-crop to the canvas, punch up colour, darken where the text goes (top for 9:16, right for 16:9)."""
    tw, th = thumbkit.TW, thumbkit.TH
    im = Image.open(path).convert('RGB')
    if flip:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    w, h = im.size
    cw = min(w, h * tw / th) / zoom
    ch = cw * th / tw
    x0 = min(max(focus[0] * w - cw / 2, 0), w - cw)
    y0 = min(max(focus[1] * h - ch / 2, 0), h - ch)
    im = im.resize((tw, th), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch))
    im = ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(1.3)).enhance(1.12)
    gh, gw = th // 8, tw // 8
    if vertical:
        yy = np.linspace(0, 1, gh)[:, None] * np.ones((1, gw))
        m = 1 - dark * np.clip(1 - yy / 0.5, 0, 1) ** 1.3
    else:
        xx = np.ones((gh, 1)) * np.linspace(0, 1, gw)[None, :]
        m = 1 - dark * np.clip((xx - 0.35) / 0.65, 0, 1) ** 1.1
    v = Image.fromarray((np.clip(m, 0, 1) * 255).astype('uint8'), 'L').resize((tw, th))
    im = Image.composite(im, Image.new('RGB', im.size, (5, 6, 12)), v)
    t = Thumb.__new__(Thumb)
    t.img = im.convert('RGBA')
    return t


def setsize(vertical):
    LW, LH = (720, 1280) if vertical else (1280, 720)
    thumbkit.TW, thumbkit.TH = int(LW * K), int(LH * K)
    return LW, LH


def block(th, txt, cx, cy, maxw, size, color, stroke=16, tilt=0, glow=None):
    lines = txt.split('\n')
    from engine import font

    def fit(ln):
        sz = size
        while sz > 40 and font(sz, 900, k=1).getlength(ln) + 2 * stroke > maxw:
            sz -= 4
        return sz
    sizes = [fit(ln) for ln in lines]
    y = cy - sum(s * 0.95 for s in sizes) / 2 + sizes[0] * 0.48
    for ln, s in zip(lines, sizes):
        th.text(cx, y, ln, s, color=color, stroke=stroke, stroke_color=(0, 0, 0), tilt=tilt, glow=glow)
        y += s * 0.95


def alert_bar(th, LW, LH, vertical):
    def d(c):
        y = LH * (0.80 if vertical else 0.84)
        c.rrect(0, y, LW, y + (70 if vertical else 64), 0, RED)
        c.text(LW / 2, y + (35 if vertical else 32), 'BREAKING  ·  COIN THEORY', 34 if vertical else 30, WHITE, 900,
               shadow=False)
    th.layer(d, outline=0, shadow=True)


def make(name, v):
    vert, ta, tb, tc, acc, bkey, alert = SPEC[name][:7]
    LW, LH = setsize(vert)
    fixed = SPEC[name][7] if len(SPEC[name]) > 7 else None
    a1, a2, a3 = ai(name, 1), ai(name, 2), ai(name, 3)
    if fixed:  # owner's own art for all three
        th = bg(find(fixed['abc'.index(v)]), vert)
        txt, col, glow = {'a': (ta, acc), 'b': (tb, WHITE), 'c': (tc, YEL)}[v] + (None,)
    elif not vert and v == 'b' and a3 and not bkey:  # long videos have a third AI picture for B
        th = bg(a2, vert)
        txt, col, glow = tb, WHITE, None
    elif v == 'a':
        th = bg(a1 or find(bkey), vert)
        txt, col, glow = ta, acc, None
    elif v == 'b':
        th = bg(find(bkey), vert) if bkey else bg(a1, vert, focus=(0.5, 0.62), zoom=1.45, flip=True)
        txt, col, glow = tb, WHITE, None
    else:
        th = bg((a3 if not vert and a3 else a2) or a1, vert, dark=0.45)
        txt, col, glow = tc, YEL, None
    if vert:
        block(th, txt, LW / 2, 300, 620, 170, col, tilt=-3 if v == 'c' else 0, glow=glow)
    else:
        block(th, txt, 930, 330, 600, 190, col, tilt=-3 if v == 'c' else 0, glow=glow)
    if v == 'b' and alert:
        alert_bar(th, LW, LH, vert)
    if v == 'a':  # Penny, the channel mascot, as a small brand mark
        if vert:
            th.layer(lambda c: penny(c, 610, 1150, 70, 0.0, 'shocked', bounce=False, arms=(200, -20)), outline=8)
        else:
            th.layer(lambda c: penny(c, 1180, 620, 70, 0.0, 'shocked', bounce=False, arms=(200, -20)), outline=8)
    out = os.path.join(OUT, f'{name}_{v}.jpg')
    th.img.convert('RGB').resize((1080, 1920) if vert else (1280, 720), Image.LANCZOS).save(out, quality=90)
    return out


def sheet(name, paths):
    ims = [Image.open(p).convert('RGB') for p in paths]
    vert = ims[0].height > ims[0].width
    big = (300, 533) if vert else (480, 270)
    small = (90, 160) if vert else (168, 94)
    sh = Image.new('RGB', (len(ims) * (big[0] + small[0] + 30), big[1] + 10), (255, 255, 255))
    for i, im in enumerate(ims):
        x = i * (big[0] + small[0] + 30)
        sh.paste(im.resize(big, Image.LANCZOS), (x, 5))
        sh.paste(im.resize(small, Image.LANCZOS), (x + big[0] + 8, 5))
    p = os.path.join(OUT, f'{name}_sheet.png')
    sh.save(p)
    return p


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for n in sys.argv[1:] or list(SPEC):
        try:
            sheet(n, [make(n, v) for v in 'abc'])
            print('ok', n)
        except FileNotFoundError as e:
            print('MISSING', n, e)
