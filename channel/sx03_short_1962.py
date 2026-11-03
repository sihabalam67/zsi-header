"""Standalone Short: since 1962 the dollar lost about 91% of its buying power. First Short built on real archival
footage (public domain, Prelinger Archives: "American Thrift", 1962) shown with fx.archival, plus fx effects.

    python3 channel/sx03_short_1962.py [--stills]

Facts: CPI-U (FRED CPIAUCSL), 1962 annual average vs the latest month. check_numbers() recomputes everything.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from wk2_art import *  # noqa: E402,F401,F403
from engine import build, still  # noqa: E402
import fx  # noqa: E402

OUT = os.path.join(HERE, 'out')
BUILD = os.path.join(HERE, 'build', 'sx03_short_1962')
FT = os.path.join(HERE, 'assets', 'footage', 'sx03')
COINS, SHOP, MALL, KIDS = (os.path.join(FT, f + '.mp4') for f in ('coins', 'shoppers', 'mall', 'kids'))

CPI = series('CPIAUCSL')
C62 = CPI[CPI.index.year == 1962].mean()
CNOW = CPI.iloc[-1]
RATIO = CNOW / C62                  # about 11.1
THEN_NOW = 100 * RATIO              # $100 in 1962 -> about $1,112 today
NOW_THEN = 100 / RATIO              # today's $100 -> about $9 of 1962 money
LOST = 1 - 1 / RATIO                # about 91% of its buying power


def beat(x, n):
    t, L = x.t, x.L
    i = max([j for j in range(n) if t >= L[j] - 0.12] or [0])
    return i, t - L[i]


def hook(c, u):
    fx.archival(c, COINS, u, 0.8, y=815)
    k = fx.pop(u, 0.12, 0.3)
    if k > 0:
        fx.title(c, f'-{LOST * 100:.0f}%', 300, 190, CORAL, k, stroke=7)
        c.rrect(150, 412, 570, 472, 30, GOLD, a=fx.clamp(fx.pop(u, 0.45)))
        c.text(360, 442, 'the dollar since 1962', 32, INK, 900, a=fx.clamp(fx.pop(u, 0.45)), shadow=False)


def s_hook(c, x):
    hook(c, max(0.0, x.t - x.L[0]))


def s_then(c, x):  # real 1962 shoppers, then the conversion
    u = x.t - x.L[0]
    clip, cu = (SHOP, u) if u < 3.2 else (MALL, u - 3.2)
    fx.archival(c, clip, cu, 1.0, y=560)
    k = fx.pop(u, 2.6, 0.35)
    if k > 0:
        c.rrect(80, 860, 640, 980, 26, (14, 18, 30, 230), GOLD, 3, a=fx.clamp(k))
        c.text(360, 920, f'$100 then = ${THEN_NOW:,.0f} now', 46, GOLD, 400, family='Anton', a=fx.clamp(k))


def s_curve(c, x):  # official CPI since 1962
    u = x.t - x.L[0]
    d = CPI[CPI.index.year >= 1962]
    xs = [t.year + (t.month - 1) / 12 for t in d.index]
    fx.growth_curve(c, u, xs, list(d.values), f'{RATIO:.0f}x', 'prices, 1962', 2.2,
                    'Prices since 1962 (CPI)', xticks=range(1970, 2030, 20))


def s_flip(c, x):
    u = x.t - x.L[0]
    fx.paper_cutout(c, u, [('TODAY', 40), ('$100', 70)], [('BUYS WHAT', 34), (f'${NOW_THEN:.0f}', 70), ('DID IN 1962', 34)],
                    '=')


def s_end(c, x):  # real 1962 kids, the yes/no question, then glass breaks back into the hook
    u = x.t - x.L[0]

    def question(cv):
        fx.archival(cv, KIDS, u, 1.0, y=470, stamp='1962')
        fx.title(cv, 'WILL PRICES EVER\nGO BACK DOWN?', 790, 62, GOLD, 1)
        for j, (lab, col) in enumerate((('YES', MINT), ('NO', CORAL))):
            k = fx.clamp(fx.pop(u, 0.4 + j * 0.25, 0.3))
            bx = 230 + j * 260
            cv.rrect(bx - 100, 960 - 46 * k, bx + 100, 960 + 46 * k, 24, col)
            cv.text(bx, 960, lab, int(56 * k) + 1, INK, 400, family='Anton', shadow=False)
    brk = x.dur - x.L[0] - 0.95
    if u < brk:
        return question(c)
    fx.frame_break(c, u - brk + 0.5, x.t, question, lambda cv: hook(cv, 0.0))


S = dict(vertical=True, lead=0.1, gap=0.15, captions=True, cap_y=1110)
SCENES = [
    dict(S, draw=s_hook, lead=0.05, lines=[
        f"!Since 1962, the dollar has lost about {LOST * 100:.0f} percent of its buying power.",
    ], punch=lambda L: [0.12], sfx=lambda L: [(0.12, 'hit'), (0.45, 'pop')]),
    dict(S, draw=s_then, lines=[
        f"This is real footage of shoppers in 1962. A hundred dollars back then is worth about "
        f"${THEN_NOW:,.0f} today.",
    ], sfx=lambda L: [(L[0] + 0.1, 'whoosh'), (L[0] + 2.6, 'hit')]),
    dict(S, draw=s_curve, cap_y=1150, lines=[
        f"Official inflation data shows prices are about {RATIO:.0f} times higher.",
    ], sfx=lambda L: [(L[0] + 1.2, 'riser'), (L[0] + 2.2, 'hit')]),
    dict(S, draw=s_flip, lines=[
        f"Flip it: today's hundred dollar bill buys what about {NOW_THEN:.0f} dollars bought in 1962.",
    ], sfx=lambda L: [(L[0] + 0.1, 'pop'), (L[0] + 0.7, 'pop'), (L[0] + 1.2, 'hit')]),
    dict(S, draw=s_end, tail=1.0, cam=(1.0, 1.0), lines=[
        "Will prices ever go back down? Yes or no, in the comments.",
    ], sfx=lambda L: [(L[0] + 0.4, 'pop'), (L[0] + 0.65, 'pop')]),
]


def check_numbers():
    script = ' '.join(l for sc in SCENES for l in sc['lines'])
    assert 10.5 < RATIO < 11.6 and f'{RATIO:.0f} times' in script and round(RATIO) == 11
    assert round(LOST * 100) == 91 and '91 percent' in script
    assert round(THEN_NOW) == 1112 and '$1,112' in script and round(NOW_THEN) == 9 and 'about 9 dollars' in script
    assert CPI.index[-1].year == 2026 and 'Yes or no' in script
    for p in (COINS, SHOP, MALL, KIDS):
        assert os.path.exists(p), p
    print(f'numbers check: OK  CPI 1962 {C62:.2f} -> {CPI.index[-1]:%b %Y} {CNOW:.3f}: x{RATIO:.3f}, '
          f'$100 then = ${THEN_NOW:,.0f}, $100 now = ${NOW_THEN:.2f} then, lost {LOST:.1%}')


if __name__ == '__main__':
    check_numbers()
    os.makedirs(BUILD, exist_ok=True)
    if '--stills' in sys.argv:
        out = os.path.join(BUILD, 'stills')
        os.makedirs(out, exist_ok=True)
        for si, sc in enumerate(SCENES):
            for du in (0.2, 1.5, 3.5):
                still(sc, 0.1 + du, os.path.join(out, f's{si}_{du}.png'), starts=[0.1], layout='short')
        print('stills in', out)
        sys.exit()
    build(SCENES, os.path.join(OUT, 'sx03_short_1962.mp4'), BUILD, layout='short', loop=True)
