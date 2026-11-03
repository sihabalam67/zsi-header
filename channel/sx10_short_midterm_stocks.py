"""Standalone news Short (Nov 4, 2026, the day after the midterms): stocks one year after every midterm since 1950.

    python3 channel/sx10_short_midterm_stocks.py [--stills]

Facts (all recomputed in check_numbers() from channel/data/SP500_midterms.csv):
- S&P 500 daily closes (Yahoo Finance ^GSPC): close on election day (or the last trading day before it; the market
  used to close on election day) vs the close on the same date one year later, for all 19 midterms 1950-2022.
- 19 of 19 higher; average +15.1%; worst +1.1% (1986); best +33.2% (1954). Price only (no dividends).
Nonpartisan: no parties, no candidates, no results. Not financial advice; history is not a promise.
Real footage: Canva stock (owner's Canva Teams licence), assets/footage/canva_h/cash_count_suit.mp4.
"""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from wk2_art import *  # noqa: E402,F401,F403
from engine import build, still  # noqa: E402
import fx  # noqa: E402

OUT = os.path.join(HERE, 'out')
BUILD = os.path.join(HERE, 'build', 'sx10_short_midterm_stocks')
CLIP = os.path.join(HERE, 'assets', 'footage', 'canva_h', 'cash_count_suit.mp4')
DATA = os.path.join(HERE, 'data', 'SP500_midterms.csv')

ROWS = [(int(r['midterm_year']), float(r['close']), float(r['close_year_later'])) for r in csv.DictReader(open(DATA))]
RET = [(y, (b / a - 1) * 100) for y, a, b in ROWS]
N, UP = len(RET), sum(r > 0 for _, r in RET)
AVG = sum(r for _, r in RET) / N
WORST = min(RET, key=lambda x: x[1])
BEST = max(RET, key=lambda x: x[1])


def hook_overlay(c, u):
    """Drawn over the cash clip. Fully visible at u=0 (payoff first), then a small punch."""
    c.rrect(0, 0, 720, 1280, 0, (8, 10, 20, 150))
    c.text(360, 250, 'STOCKS 1 YEAR AFTER', 40, WHITE, 900)
    c.text(360, 300, 'EVERY MIDTERM SINCE 1950', 40, WHITE, 900)
    s = 1.0 + 0.06 * max(0.0, 1 - abs(u - 0.15) / 0.15) if u < 0.3 else 1.0
    fx.title(c, f'{UP} / {N}', 520, int(190 * s), MINT, 1, stroke=8)
    c.rrect(170, 690, 550, 770, 36, MINT)
    c.text(360, 730, 'ALL HIGHER', 48, INK, 400, family='Anton', shadow=False)


def s_hook(c, x):
    hook_overlay(c, max(0.0, x.t - x.L[0]))


def s_bars(c, x):  # 19 bars grow one after another, all green
    u = x.t - x.L[0]
    c.rrect(0, 0, 720, 1280, 0, (14, 18, 30))
    c.text(360, 200, 'S&P 500, election day to 1 year later', 30, WHITE, 900, a=fade(u, 0))
    x0, step, base, top = 64, 31, 930, 420
    vmax = BEST[1]
    c.line([(40, base), (680, base)], (255, 255, 255, 140), 4)
    for i, (y, r) in enumerate(RET):
        g = ease(seg(u, 0.2 + i * 0.12, 0.5 + i * 0.12))
        if g <= 0:
            continue
        h = (base - top) * r / vmax * g
        bx = x0 + i * step
        col = GOLD if (y, r) in (WORST, BEST) else MINT
        c.rrect(bx, base - max(h, 4), bx + 22, base, 6, col)
        if y in (1950, 1986, 2022):
            c.text(bx + 11, base + 34, f"'{y % 100:02d}", 22, MUTED, 800, shadow=False)
    k = fx.pop(u, 0.2 + N * 0.12 + 0.2, 0.3)
    if k > 0:
        c.rrect(150, 300 - 10, 570, 370, 30, MINT, a=fx.clamp(k))
        c.text(360, 330, f'{UP} UP, 0 DOWN', 46, INK, 400, family='Anton', a=fx.clamp(k), shadow=False)


def s_avg(c, x):  # the average counts up
    u = x.t - x.L[0]
    c.rrect(0, 0, 720, 1280, 0, (14, 18, 30))
    c.text(360, 330, 'AVERAGE GAIN', 44, WHITE, 900, a=fade(u, 0))
    k = ease(fx.clamp((u - 0.1) / 1.1))
    fx.title(c, f'+{AVG * k:.0f}%', 600, 230, MINT, 1, stroke=8)
    ks = fx.pop(u, 1.3, 0.3)
    if ks > 0:
        c.text(360, 820, 'in the 12 months after', 36, MUTED, 800, a=fx.clamp(ks))


def s_range(c, x):  # worst and best as two cards
    u = x.t - x.L[0]
    c.rrect(0, 0, 720, 1280, 0, (14, 18, 30))
    for j, (lab, (y, r), at) in enumerate((('WORST', WORST, 0.1), ('BEST', BEST, 3.0))):
        k = fx.pop(u, at, 0.35)
        if k <= 0:
            continue
        y0 = 300 + j * 330
        c.rrect(90, y0, 630, y0 + 270, 30, (24, 30, 48), GOLD if j else MUTED, 4, a=fx.clamp(k))
        c.text(360, y0 + 55, f'{lab}: {y}', 40, WHITE, 900, a=fx.clamp(k))
        cnt = r * ease(fx.clamp((u - at) / 1.0))  # the number counts up
        c.text(360, y0 + 165, f'+{cnt:.1f}%', int(120 * (0.7 + 0.3 * fx.clamp(k))), GOLD if j else MINT, 400,
               family='Anton', a=fx.clamp(k))
    fx.zoom_canvas(c, 1.01 + 0.012 * max(0.0, u), 360, 560)  # slow push so the frame never sits still


def s_caveat(c, x):
    u = x.t - x.L[0]
    c.rrect(0, 0, 720, 1280, 0, (14, 18, 30))
    k = fx.pop(u, 0.1, 0.35)
    c.rrect(80, 380, 640, 820, 30, (40, 22, 26), CORAL, 5, a=fx.clamp(k))
    fx.title(c, 'HISTORY,\nNOT A\nPROMISE', 520, 96, CORAL, k)
    c.text(360, 880, 'S&P 500 price only, no dividends', 30, MUTED, 800, a=fx.clamp(fx.pop(u, 0.9, 0.3)))


def hook_frame(cv):
    from engine import clip_frame, cover
    cv.img.paste(cover(clip_frame(CLIP, 0), cv.img.size[0], cv.img.size[1]))
    hook_overlay(cv, 0.0)


def s_end(c, x):  # yes/no question, then glass breaks back into the hook's first frame
    u = x.t - x.L[0]

    def question(cv):
        cv.rrect(0, 0, 720, 1280, 0, (14, 18, 30))
        pulse = 1 + 0.06 * math.sin(u * 6)
        fx.title(cv, f'{N + 1} FOR\n{N + 1}?', 400, int(150 * pulse), GOLD, 1)
        for j, (lab, col) in enumerate((('YES', MINT), ('NO', CORAL))):
            k = fx.clamp(fx.pop(u, 0.4 + j * 0.25, 0.3))
            bx = 230 + j * 260
            cv.rrect(bx - 105, 740 - 52 * k, bx + 105, 740 + 52 * k, 26, col)
            cv.text(bx, 740, lab, int(64 * k) + 1, INK, 400, family='Anton', shadow=False)
        cv.text(360, 870 + 8 * math.sin(u * 4), 'comment below', 34, WHITE, 900)
    brk = x.dur - x.L[0] - 0.95
    if u < brk:
        return question(c)
    fx.frame_break(c, u - brk + 0.5, x.t, question, hook_frame)


S = dict(vertical=True, lead=0.1, gap=0.15, captions=True, cap_y=1080)
SCENES = [
    dict(S, draw=s_hook, bg_video=CLIP, bg_speed=1.0, lead=0.05, lines=[
        f"!Every midterm since 1950, stocks were higher one year later. {N} for {N}.",
    ], punch=lambda L: [0.12], sfx=lambda L: [(0.12, 'hit')]),
    dict(S, draw=s_bars, lines=[
        "That's the S&P 500, from election day to one year later. Not one went down.",
    ], sfx=lambda L: [(L[0] + 0.2, 'whoosh'), (L[0] + 0.2 + N * 0.12 + 0.2, 'ding')]),
    dict(S, draw=s_avg, lines=[
        f"The average gain: about {AVG:.0f} percent.",
    ], sfx=lambda L: [(L[0] + 0.1, 'riser'), (L[0] + 1.2, 'hit')]),
    dict(S, draw=s_range, lines=[
        f"The worst year still made {WORST[1]:.0f} percent, in {WORST[0]}. The best made {BEST[1]:.0f}, in {BEST[0]}.",
    ], sfx=lambda L: [(L[0] + 0.1, 'pop'), (L[0] + 2.0, 'riser'), (L[0] + 3.0, 'hit')]),
    dict(S, draw=s_caveat, lines=[
        "But that's history, not a promise. Past results don't guarantee anything.",
    ], sfx=lambda L: [(L[0] + 0.1, 'down')]),
    dict(S, draw=s_end, tail=1.0, cam=(1.0, 1.0), lines=[
        f"So, {N + 1} for {N + 1}? Yes or no, in the comments.",
    ], sfx=lambda L: [(L[0] + 0.4, 'pop'), (L[0] + 0.65, 'pop')]),
]


def check_numbers():
    script = ' '.join(l for sc in SCENES for l in sc['lines'])
    assert N == 19 and UP == 19, (N, UP)
    assert [y for y, _ in RET] == list(range(1950, 2023, 4))
    assert round(AVG) == 15 and f'about {round(AVG)} percent' in script
    assert WORST[0] == 1986 and round(WORST[1], 1) == 1.1 and BEST[0] == 1954 and round(BEST[1], 1) == 33.2
    assert '19 for 19' in script and '20 for 20' in script and 'not a promise' in script
    assert os.path.exists(CLIP)
    print(f'numbers check: OK  {UP}/{N} up, average +{AVG:.1f}%, worst {WORST[0]} +{WORST[1]:.1f}%, '
          f'best {BEST[0]} +{BEST[1]:.1f}%')


if __name__ == '__main__':
    check_numbers()
    os.makedirs(BUILD, exist_ok=True)
    if '--stills' in sys.argv:
        out = os.path.join(BUILD, 'stills')
        os.makedirs(out, exist_ok=True)
        for si, sc in enumerate(SCENES):
            for du in (0.0, 1.5, 3.5):
                still(sc, 0.1 + du, os.path.join(out, f's{si}_{du}.png'), starts=[0.1], layout='short')
        print('stills in', out)
        sys.exit()
    build(SCENES, os.path.join(OUT, 'sx10_short_midterm_stocks.mp4'), BUILD, layout='short', loop=True)
