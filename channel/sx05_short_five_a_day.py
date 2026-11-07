"""Standalone Short (fx style): what $5 a day becomes.

    python3 channel/sx05_short_five_a_day.py [--stills]

Pure math, shown as an example: $5 a day = $5 x 365 / 12 a month, invested monthly at 7% a year compounded monthly.
7% is a common long-run illustration, not a promise; narration and screen say so. Taxes, fees and inflation are not
included (description says so). check_numbers() recomputes everything. Footage: owner's Canva sx05 B-roll
(assets/footage/sx05, Canva Content License; cut from all.mp4, see assets/photos/SOURCES.md).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from wk2_art import *  # noqa: E402,F401,F403
from engine import build, still  # noqa: E402
import fx  # noqa: E402

OUT = os.path.join(HERE, 'out')
BUILD = os.path.join(HERE, 'build', 'sx05_short_five_a_day')
FOOT = os.path.join(HERE, 'assets', 'footage', 'sx05')
CLIP = {k: os.path.join(FOOT, k + '.mp4') for k in ('coffee', 'coins', 'calendar', 'plant', 'phone')}
JAR = os.path.join(FOOT, 'rolljar_end.jpg')

DAY, RATE = 5, 0.07
PMT = DAY * 365 / 12                      # about $152 a month


def path(years):
    r, bal, xs, ys = RATE / 12, 0.0, [0.0], [0.0]
    for m in range(years * 12):
        bal = bal * (1 + r) + PMT
        xs.append((m + 1) / 12)
        ys.append(bal)
    return xs, ys


XS, YS = path(40)
B = {y: YS[y * 12] for y in (10, 20, 30, 40)}
PUT = {y: DAY * 365 * y for y in (10, 20, 30, 40)}
LAST10 = B[30] - B[20]


def k(v):
    return f'${round(v / 1000)}K'


def card(c, u, at, y, text, col=WHITE, fg=INK, size=40, w=520):
    kk = fx.pop(u, at, 0.3)
    if kk <= 0:
        return
    s = 0.7 + 0.3 * fx.clamp(kk)
    c.rrect(360 - w / 2 * s, y - 40 * s, 360 + w / 2 * s, y + 40 * s, 26, col, a=fx.clamp(kk))
    c.text(360, y, text, int(size * s), fg, 400, family='Anton', a=fx.clamp(kk), shadow=False)


def hook_draw(c, u):
    fx.photo(c, JAR, 1.12 - 0.04 * fx.clamp(u / 3), (0.5, 0.55), dark=0.45, sat=1.2)
    c.rrect(0, 0, 720, 1280, 0, (8, 10, 20, 120))
    c.rrect(230, 300, 490, 370, 30, GOLD)
    c.text(360, 335, '$5 A DAY', 44, INK, 400, family='Anton', shadow=False)
    s = 1.0 + 0.07 * max(0.0, 1 - abs(u - 0.15) / 0.15) if u < 0.3 else 1.0
    fx.title(c, f'${B[30]:,.0f}', 500, int(150 * s), MINT, 1, stroke=8)
    kk = fx.clamp(fx.pop(u, 1.2, 0.3))
    if kk > 0:
        c.text(360, 690, 'AFTER 30 YEARS', 48, WHITE, 900, a=kk)
    if u > 0:
        fx.zoom_canvas(c, 1.01 + 0.012 * u, 360, 560)


def s_hook(c, x):
    hook_draw(c, max(0.0, x.t - x.L[0]))


def s_coffee(c, x):  # real clip + three item chips
    u = x.t - x.L[0]
    for j, (txt, col) in enumerate((('1 COFFEE', GOLD), ('1 SNACK', MINT), ('1 DELIVERY FEE', SKY))):
        card(c, u, 0.6 + j * 0.55, 300 + j * 110, txt, col, w=440)
    card(c, u, 2.4, 760, 'EVERY DAY', CORAL, WHITE, 52, 380)


def s_calendar(c, x):  # real clip + the monthly amount, then the 30-year total counts up
    u = x.t - x.L[0]
    l1 = x.L[1] - x.L[0]
    card(c, u, 0.3, 330, '$5 x 365 / 12', WHITE, INK, 36, 400)
    card(c, u, 1.4, 460, f'= ${PMT:.0f} A MONTH', GOLD, INK, 52, 560)
    if u > l1:
        v = PUT[30] * ease(fx.clamp((u - l1 - 0.6) / 1.6))
        c.rrect(80, 610, 640, 830, 30, (14, 18, 30, 230), MINT, 4, a=fade(u, l1))
        c.text(360, 665, 'YOU PUT IN (30 YEARS)', 30, WHITE, 900, a=fade(u, l1))
        c.text(360, 755, f'${v:,.0f}', 92, MINT, 400, family='Anton', a=fade(u, l1))


def s_versus(c, x):  # paper cutout: jar vs invested
    u = x.t - x.L[0]
    l1 = x.L[1] - x.L[0]
    right = [('INVESTED', 40), ('7% / YEAR*', 26), ('?', 54)]
    fx.paper_cutout(c, u, [('IN A JAR', 40), ('0%', 26), (f'${PUT[30]:,}', 54)], right, 'VS')
    kk = fx.clamp(fx.pop(u, l1 + 4.0, 0.3))  # the reveal stamps over the invested card (cutouts are cached sprites)
    if kk > 0:
        s = lerp(1.6, 1.0, kk)
        c.rrect(360 - 250 * s, 800 - 70 * s, 360 + 250 * s, 800 + 70 * s, 24, (14, 18, 30), MINT, 5, a=kk)
        c.text(360, 800, f'${B[30]:,.0f}', int(96 * s), MINT, 400, family='Anton', a=kk, shadow=False)
    if u > l1:
        c.text(360, 980, '*a common long-run example, not a promise', 26, WHITE, 800, a=fade(u, l1))


def s_curve(c, x):  # the line draws itself; milestones pop as they are said
    u = x.t - x.L[0]
    xs, ys = XS[:361], [v / 1000 for v in YS[:361]]
    fx.growth_curve(c, u, xs, ys, k(B[30]), '$5 a day', 3.6, 'balance ($ thousands)', xticks=range(0, 31, 10))
    for j, y in enumerate((10, 20)):
        kk = fx.clamp(fx.pop(u, 0.9 + j * 1.2, 0.3))
        if kk > 0:
            px = 70 + 580 * y / 30
            c.rrect(px - 95, 960 - 38, px + 95, 960 + 38, 20, GOLD, a=kk)
            c.text(px, 960, f'{y} YRS: {k(B[y])}', 32, INK, 400, family='Anton', a=kk, shadow=False)


def s_plant(c, x):  # real clip: the last ten years
    u = x.t - x.L[0]
    card(c, u, 0.3, 300, 'YEARS 21 TO 30', WHITE, INK, 40, 440)
    card(c, u, 1.2, 420, f'+{k(LAST10)}', MINT, INK, 84, 380)
    card(c, u, 2.6, 560, f'YEARS 1 TO 20: {k(B[20])}', GOLD, INK, 36, 520)


def s_forty(c, x):  # real clip + the 40-year number
    u = x.t - x.L[0]
    card(c, u, 0.2, 300, '10 MORE YEARS', WHITE, INK, 40, 440)
    kk = fx.clamp(fx.pop(u, 1.6, 0.3))
    if kk > 0:
        c.rrect(60, 380, 660, 560, 30, (14, 18, 30, 230), MINT, 5, a=kk)
        fx.title(c, f'${B[40]:,.0f}', 470, int(110 * (0.7 + 0.3 * kk)), MINT, kk, stroke=6)


def s_end(c, x):
    u = x.t - x.L[0]

    def question(cv):
        cv.rrect(0, 0, 720, 1280, 0, (14, 18, 30))
        fx.title(cv, 'WOULD YOU\nGIVE UP $5\nA DAY?', 300, int(92 * (1 + 0.04 * math.sin(u * 6))), GOLD, 1)
        for j, (txt, col) in enumerate((('YES', MINT), ('NO', CORAL))):
            kk = fx.clamp(fx.pop(u, 0.3 + j * 0.2, 0.3))
            bx = 230 + j * 260
            cv.rrect(bx - 110, 700 - 60 * kk, bx + 110, 700 + 60 * kk, 30, col)
            cv.text(bx, 700, txt, int(70 * kk) + 1, INK, 400, family='Anton', shadow=False)
        cv.text(360, 840 + 8 * math.sin(u * 4), 'tell me in the comments', 32, WHITE, 900)
    brk = x.dur - x.L[0] - 0.95
    if u < brk:
        return question(c)
    fx.frame_break(c, u - brk + 0.5, x.t, question, lambda cv: hook_draw(cv, 0.0))


S = dict(vertical=True, lead=0.1, gap=0.15, captions=True, cap_y=1080)
SCENES = [
    dict(S, draw=s_hook, lead=0.05, lines=[
        f"!Five dollars a day can turn into about {round(B[30] / 1000)} thousand dollars.",
    ], punch=lambda L: [0.12], sfx=lambda L: [(0.12, 'hit'), (1.2, 'pop')]),
    dict(S, draw=s_coffee, bg_video=CLIP['coffee'], bg_speed=1.0, lines=[
        "That's one coffee, one snack, or one delivery fee. Every day.",
    ], sfx=lambda L: [(L[0] + 0.6 + j * 0.55, 'pop') for j in range(3)] + [(L[0] + 2.4, 'hit')]),
    dict(S, draw=s_calendar, bg_video=CLIP['calendar'], bg_speed=2.2, lines=[
        f"Five dollars a day is about {round(PMT)} dollars a month.",
        "In thirty years, you put in 54,750 dollars.",
    ], sfx=lambda L: [(L[0] + 0.3, 'pop'), (L[0] + 1.4, 'pop'), (L[1] + 0.1, 'whoosh'), (L[1] + 2.2, 'ding')]),
    dict(S, draw=s_versus, lines=[
        "Kept in a jar, that's all you'd have.",
        "Invested at seven percent a year, a common long-run example, not a promise, it grows a lot more.",
    ], sfx=lambda L: [(L[0] + 0.1, 'pop'), (L[0] + 0.7, 'pop'), (L[1] + 3.0, 'riser'), (L[1] + 4.0, 'hit')]),
    dict(S, draw=s_curve, lines=[
        f"Ten years: {round(B[10] / 1000)} thousand. Twenty: {round(B[20] / 1000)} thousand. "
        f"Thirty: {round(B[30] / 1000)} thousand.",
    ], sfx=lambda L: [(L[0] + 0.9, 'pop'), (L[0] + 2.1, 'pop'), (L[0] + 3.6, 'hit')]),
    dict(S, draw=s_plant, bg_video=CLIP['plant'], bg_speed=1.0, lines=[
        f"!The last ten years add {round(LAST10 / 1000)} thousand. More than the first twenty years combined.",
    ], sfx=lambda L: [(L[0] + 0.3, 'pop'), (L[0] + 1.2, 'hit'), (L[0] + 2.6, 'pop')]),
    dict(S, draw=s_forty, bg_video=CLIP['phone'], bg_speed=1.0, lines=[
        f"!Wait ten more years? About {round(B[40] / 1000)} thousand.",
    ], sfx=lambda L: [(L[0] + 0.2, 'pop'), (L[0] + 0.6, 'riser'), (L[0] + 1.6, 'hit')]),
    dict(S, draw=s_end, tail=1.0, cam=(1.0, 1.0), lines=[
        "Time does the heavy lifting. Would you give up five dollars a day for this? Yes or no?",
    ], sfx=lambda L: [(L[0] + 0.3, 'pop'), (L[0] + 0.5, 'pop')]),
]


def check_numbers():
    script = ' '.join(l for sc in SCENES for l in sc['lines'])
    r = RATE / 12
    for y, v in B.items():  # closed form of the monthly annuity must match the simulation
        n = y * 12
        assert abs(PMT * ((1 + r) ** n - 1) / r - v) < 0.01, y
    assert round(PMT) == 152 and PUT[30] == 54750
    assert [round(B[y] / 1000) for y in (10, 20, 30, 40)] == [26, 79, 186, 399], B
    assert round(B[30]) == 185537 and round(B[40]) == 399190
    assert LAST10 > B[20] and round(LAST10 / 1000) == 106
    for s in ('186 thousand', '152 dollars', '54,750', '26 thousand', '79 thousand', '106 thousand',
              '399 thousand', 'not a promise'):
        assert s in script, s
    print(f'numbers check: OK  ${PMT:.2f}/mo; 10y ${B[10]:,.0f} 20y ${B[20]:,.0f} 30y ${B[30]:,.0f} '
          f'40y ${B[40]:,.0f}; put in 30y ${PUT[30]:,}; last 10y +${LAST10:,.0f}')


if __name__ == '__main__':
    check_numbers()
    os.makedirs(BUILD, exist_ok=True)
    if '--stills' in sys.argv:
        out = os.path.join(BUILD, 'stills')
        os.makedirs(out, exist_ok=True)
        for si, sc in enumerate(SCENES):
            starts = [0.1 + 3.4 * j for j in range(len(sc['lines']))]
            for du in (0.0, 2.0, 3.9):
                still(sc, 0.1 + du, os.path.join(out, f's{si}_{du}.png'), starts=starts, layout='short')
        print('stills in', out)
        sys.exit()
    build(SCENES, os.path.join(OUT, 'sx05_short_five_a_day.mp4'), BUILD, layout='short', loop=True)
