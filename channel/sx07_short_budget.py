"""Standalone Short (fx style): the 50/30/20 budget on a typical paycheck.

    python3 channel/sx07_short_budget.py [--stills]

Take-home pay comes from channel/sx06_short_paycheck.py (BLS median full-time weekly earnings x 52, minus 2026 federal
income tax for a single filer with the standard deduction and FICA; state tax not included). The 50/30/20 rule was
popularized by Elizabeth Warren and Amelia Warren Tyagi in "All Your Worth" (2005): 50% of after-tax income to needs,
30% to wants, 20% to savings and extra debt payments. The 10-year figure is pure math at an example 7% a year
(compounded monthly), said on screen as an example, not a promise.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
_argv, sys.argv = sys.argv, [sys.argv[0]]
from wk2_art import *  # noqa: E402,F401,F403
from engine import build, still  # noqa: E402
import fx  # noqa: E402
import sx06_short_paycheck as P  # noqa: E402
sys.argv = _argv

OUT = os.path.join(HERE, 'out')
BUILD = os.path.join(HERE, 'build', 'sx07_short_budget')

MONTH = P.NET / 12
NEEDS, WANTS, SAVE = round(MONTH * 0.5), round(MONTH * 0.3), round(MONTH * 0.2)
TOTAL = NEEDS + WANTS + SAVE
RATE, YEARS = 0.07, 10
_r = RATE / 12
FV = SAVE * ((1 + _r) ** (YEARS * 12) - 1) / _r
PUT_IN = SAVE * 12 * YEARS
PARTS = [('NEEDS', 50, NEEDS, SKY, 'rent · groceries · insurance · minimum debt payments'),
         ('WANTS', 30, WANTS, GOLD, 'eating out · streaming · trips'),
         ('SAVE', 20, SAVE, MINT, 'savings · extra debt payments')]


def money(v):
    return f'${v:,.0f}'


def bar(c, t, x, focus=None, grow=1.0):
    """The month's take-home as one bar split 50/30/20; the part being talked about is lit."""
    x0, x1, y0, y1 = 70, 650, 420, 560
    c.text(360, 370, f'{money(TOTAL)} a month', 44, WHITE, 900)
    pos = x0
    for i, (lab, pct, amt, col, _) in enumerate(PARTS):
        w = (x1 - x0) * pct / 100 * grow
        on = focus is None or focus == i
        c.rrect(pos, y0, pos + w - 4, y1, 16, col, a=1.0 if on else 0.25)
        if w > 60:
            c.text(pos + w / 2, (y0 + y1) / 2, f'{pct}%', 40, INK, 400, family='Anton', a=1.0 if on else 0.4,
                   shadow=False)
        if focus == i:
            c.rrect(pos - 6, y0 - 6, pos + w + 2, y1 + 6, 20, None, WHITE, 5,
                    a=0.4 + 0.6 * (0.5 + 0.5 * math.sin(t * 5)))
        pos += w


def part_beat(c, x, i):
    t, u = x.t, x.t - x.L[0]
    lab, pct, amt, col, ex = PARTS[i]
    c.rrect(0, 0, 720, 1280, 0, (14, 18, 30))
    bar(c, t, x, focus=i)
    k = fx.pop(u, 0.3, 0.35)
    fx.title(c, f'{lab}: {money(amt)}', 690, int(80 * (0.7 + 0.3 * fx.clamp(k))), col, k, stroke=6)
    items = ex.split(' · ')
    for j, item in enumerate(items):
        kk = fx.clamp(fx.pop(u, 1.4 + 0.6 * j, 0.3))
        if kk > 0:
            cx = 360 if (len(items) % 2 and j == len(items) - 1) or len(items) == 1 else (210 if j % 2 == 0 else 510)
            chip(c, cx, 800 + (j // 2) * 66, item, col, kk, 24)
    fx.zoom_canvas(c, 1.01 + 0.006 * u, 360, 600)


def hook_draw(c, u):
    c.rrect(0, 0, 720, 1280, 0, (14, 18, 30))
    s = 1.0 + 0.07 * max(0.0, 1 - abs(u - 0.15) / 0.15) if u < 0.3 else 1.0
    c.text(360, 340, 'THE 50/30/20 RULE SAYS', 38, WHITE, 900)
    fx.title(c, f'SAVE {money(SAVE)}', 510, int(110 * s), MINT, 1, stroke=7)
    c.text(360, 630, 'a month, on a typical paycheck', 34, WHITE, 900)
    k = fx.clamp(fx.pop(u, 1.4, 0.3))
    if k > 0:
        c.rrect(190, 730, 530, 790, 30, GOLD, a=k)
        c.text(360, 760, 'COULD YOU?', 36, INK, 400, family='Anton', a=k, shadow=False)
    if u > 0:
        fx.zoom_canvas(c, 1.01 + 0.012 * u, 360, 450)


def s_hook(c, x):
    hook_draw(c, max(0.0, x.t - x.L[0]))


def s_pay(c, x):
    u = x.t - x.L[0]
    c.rrect(0, 0, 720, 1280, 0, (14, 18, 30))
    bar(c, x.t, x, grow=ease(fx.clamp((u - 0.4) / 1.4)))
    c.text(360, 680, 'typical full-time take-home', 32, WHITE, 900, a=fade(u, 0.3))
    c.text(360, 730, 'after federal taxes, before state tax', 24, MUTED, 800, a=fade(u, 0.8))
    fx.zoom_canvas(c, 1.01 + 0.01 * u, 360, 550)


def s_needs(c, x):
    part_beat(c, x, 0)


def s_wants(c, x):
    part_beat(c, x, 1)


def s_save(c, x):
    part_beat(c, x, 2)


def s_grow(c, x):
    u = x.t - x.L[0]
    c.rrect(0, 0, 720, 1280, 0, (14, 18, 30))
    c.text(360, 330, f'{money(SAVE)} a month for {YEARS} years', 36, WHITE, 900, a=fade(u, 0))
    v = FV * ease(fx.clamp((u - 0.6) / 2.0))
    fx.title(c, money(v), 510, 120, MINT, 1, stroke=7)
    c.text(360, 630, f'you put in {money(PUT_IN)}', 32, WHITE, 900, a=fade(u, 1.0))
    if u > 2.8:
        c.rrect(110, 700, 610, 760, 30, GOLD, a=fade(u, 2.8))
        c.text(360, 730, f'{RATE * 100:.0f}% a year: an example, not a promise', 24, INK, 900, a=fade(u, 2.8),
               shadow=False)
    fx.zoom_canvas(c, 1.01 + 0.01 * u, 360, 450)


def s_end(c, x):
    u = x.t - x.L[0]

    def question(cv):
        cv.rrect(0, 0, 720, 1280, 0, (14, 18, 30))
        fx.title(cv, 'COULD YOU LIVE\nON 50/30/20?', 320, int(84 * (1 + 0.04 * math.sin(u * 6))), GOLD, 1)
        for j, (txt, col) in enumerate((('YES', MINT), ('NO', CORAL))):
            kk = fx.clamp(fx.pop(u, 0.3 + j * 0.2, 0.3))
            bx = 230 + j * 260
            cv.rrect(bx - 110, 640 - 60 * kk, bx + 110, 640 + 60 * kk, 30, col)
            cv.text(bx, 640, txt, int(70 * kk) + 1, INK, 400, family='Anton', shadow=False)
        cv.text(360, 780 + 8 * math.sin(u * 4), 'tell me in the comments', 32, WHITE, 900)
    brk = x.dur - x.L[0] - 0.95
    if u < brk:
        return question(c)
    fx.frame_break(c, u - brk + 0.5, x.t, question, lambda cv: hook_draw(cv, 0.0))


S = dict(vertical=True, lead=0.1, gap=0.15, captions=True, cap_y=1080)
SCENES = [
    dict(S, draw=s_hook, lead=0.05, lines=[
        f"!On a typical paycheck, the 50 30 20 rule says save {SAVE} dollars a month.",
    ], punch=lambda L: [0.12], sfx=lambda L: [(0.12, 'hit'), (1.4, 'pop')]),
    dict(S, draw=s_pay, lines=[
        f"The typical full-time worker takes home about {TOTAL:,} dollars a month, after federal taxes.",
    ], sfx=lambda L: [(L[0] + 0.4, 'whoosh'), (L[0] + 1.8, 'ding')]),
    dict(S, draw=s_needs, lines=[
        f"Fifty percent, {NEEDS:,} dollars, goes to needs: rent, groceries, insurance, minimum debt payments.",
    ], sfx=lambda L: [(L[0] + 0.3, 'pop')] + [(L[0] + 1.4 + 0.6 * j, 'pop') for j in range(4)]),
    dict(S, draw=s_wants, lines=[
        f"Thirty percent, {WANTS:,} dollars, goes to wants: eating out, streaming, trips.",
    ], sfx=lambda L: [(L[0] + 0.3, 'pop')] + [(L[0] + 1.4 + 0.6 * j, 'pop') for j in range(3)]),
    dict(S, draw=s_save, lines=[
        f"!And twenty percent, {SAVE} dollars, goes to savings or paying off extra debt.",
    ], punch=lambda L: [L[0] + 0.4], sfx=lambda L: [(L[0] + 0.3, 'hit'), (L[0] + 1.4, 'pop'), (L[0] + 2.0, 'pop')]),
    dict(S, draw=s_grow, lines=[
        f"Invested at an example {RATE * 100:.0f} percent a year, ten years of that grows to about "
        f"{round(FV / 1000)} thousand dollars. An example, not a promise.",
    ], sfx=lambda L: [(L[0] + 0.6, 'tick'), (L[0] + 2.6, 'ding'), (L[0] + 2.8, 'pop')]),
    dict(S, draw=s_end, tail=1.0, cam=(1.0, 1.0), lines=[
        "So, could you live on this budget? Yes or no?",
    ], sfx=lambda L: [(L[0] + 0.3, 'pop'), (L[0] + 0.5, 'pop')]),
]


def check_numbers():
    script = ' '.join(l for sc in SCENES for l in sc['lines'])
    P.check_numbers()
    assert round(P.NET) == 53948 and TOTAL == 4496 and (NEEDS, WANTS, SAVE) == (2248, 1349, 899)
    assert abs(TOTAL - MONTH) < 1 and round(FV / 1000) == 156 and PUT_IN == 107880
    r = RATE / 12
    sim = 0.0
    for _ in range(YEARS * 12):
        sim = sim * (1 + r) + SAVE
    assert abs(sim - FV) < 0.01
    for s in ('899 dollars', '4,496 dollars', '2,248 dollars', '1,349 dollars', '156 thousand', 'not a promise',
              'after federal taxes'):
        assert s in script, s
    print(f'numbers check: OK  take-home ${P.NET:,.0f}/yr = ${MONTH:,.2f}/mo -> {NEEDS}/{WANTS}/{SAVE}; '
          f'10y at 7%: ${FV:,.0f} (put in ${PUT_IN:,})')


if __name__ == '__main__':
    check_numbers()
    os.makedirs(BUILD, exist_ok=True)
    if '--stills' in sys.argv:
        out = os.path.join(BUILD, 'stills')
        os.makedirs(out, exist_ok=True)
        for si, sc in enumerate(SCENES):
            for du in (0.0, 2.2, 3.8):
                still(sc, 0.1 + du, os.path.join(out, f's{si}_{du}.png'), starts=[0.1], layout='short')
        print('stills in', out)
        sys.exit()
    build(SCENES, os.path.join(OUT, 'sx07_short_budget.mp4'), BUILD, layout='short', loop=True)
