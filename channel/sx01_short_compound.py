"""Standalone Short (fx style): start at 25 vs 35, same $200 a month, double the money.

    python3 channel/sx01_short_compound.py [--stills]

Pure math, shown as an example: $200 a month, 7% a year compounded monthly, contributions until 65. 7% is a common
long-run illustration, not a promise; the narration and screen say so. check_numbers() recomputes everything.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from wk2_art import *  # noqa: E402,F401,F403
from engine import build, still  # noqa: E402
import fx  # noqa: E402

OUT = os.path.join(HERE, 'out')
BUILD = os.path.join(HERE, 'build', 'sx01_short_compound')
CASH = os.path.join(HERE, 'assets', 'photos', 'ep06s', 'cash.jpg')
CASH_F = (0.83, 0.72)

PMT, RATE, END = 200, 0.07, 65


def balance_path(start_age):
    r, bal, xs, ys = RATE / 12, 0.0, [start_age], [0.0]
    for m in range((END - start_age) * 12):
        bal = bal * (1 + r) + PMT
        xs.append(start_age + (m + 1) / 12)
        ys.append(bal)
    return xs, ys


AX, AY = balance_path(25)
SX, SY = balance_path(35)
ALEX, SAM = AY[-1], SY[-1]               # about $525k vs $244k
PUT_A, PUT_S = PMT * 12 * 40, PMT * 12 * 30
GAP = ALEX - SAM


def k(v):
    return f'${v / 1000:,.0f}K'


def hook(c, u):
    fx.snap_zoom(c, u, CASH, 'SAME $200\nDOUBLE THE\nMONEY', CASH_F)


def beat(x, n):
    t, L = x.t, x.L
    i = max([j for j in range(n) if t >= L[j] - 0.12] or [0])
    return i, t - L[i]


def s_a(c, x):  # snap zoom, chat takeover, paper cutout
    i, u = beat(x, 3)
    if i == 0 or x.t < x.L[0]:
        return hook(c, max(0.0, x.t - x.L[0]))
    if i == 1:
        return fx.chat_takeover(c, u, [('wait, same money??', 'l'), ('how is that fair', 'l'),
                                       ('one word', 'r'), ('...what', 'l'), ('when', 'r')], step=0.55)
    fx.paper_cutout(c, u, [('ALEX', 56), ('starts at', 26), ('25', 64)], [('SAM', 56), ('starts at', 26), ('35', 64)],
                    'VS')


def s_b(c, x):  # liquid glass, growth curve, digital zoom
    i, u = beat(x, 3)
    if i == 0:
        return fx.liquid_glass(c, u, CASH, [('$200', 'a month, both of them', GOLD),
                                            ('7%', 'a year (example, not a promise)', WHITE)], CASH_F)
    if i == 1:
        return fx.growth_curve(c, u, AX, [v / 1000 for v in AY], k(ALEX), 'Alex, age 25', 2.4,
                               "Alex's balance ($ thousands)", xticks=range(25, 66, 10))
    fx.digital_zoom(c, u, round(SAM), "Sam at 65")


def s_c(c, x):  # paper cutout (what they put in), orbit, frame break back to the hook
    i, u = beat(x, 3)
    if i == 0:
        return fx.paper_cutout(c, u, [('ALEX PUT IN', 30), (f'${PUT_A:,}', 44), (f'GOT {k(ALEX)}', 30)],
                               [('SAM PUT IN', 30), (f'${PUT_S:,}', 44), (f'GOT {k(SAM)}', 30)], 'VS')
    if i == 1:
        return fx.orbit(c, u, 'COMPOUNDING', 'money earning money on its money')

    def before(cv):
        fx.orbit(cv, u + 3, 'COMPOUNDING', 'money earning money on its money')
    fx.frame_break(c, u, x.t, before, lambda cv: hook(cv, 0.0))


S = dict(vertical=True, lead=0.1, gap=0.15, captions=True, cap_y=1060)
SCENES = [
    dict(S, draw=s_a, lines=[
        "!Two friends save the exact same two hundred dollars a month. One ends up with double the money.",
        "The only difference? When they started.",
        "Alex starts at twenty-five. Sam waits until thirty-five.",
    ], punch=lambda L: [0.05], sfx=lambda L: [(0.0, 'down'), (L[1], 'pop'), (L[1] + 1.1, 'pop'), (L[2] + 0.1, 'pop'),
                                              (L[2] + 0.7, 'pop')]),
    dict(S, draw=s_b, lines=[
        "Both earn seven percent a year. That's a common long-run example, not a promise.",
        f"By sixty-five, Alex has about {round(ALEX / 1000)} thousand dollars.",
        f"!Sam? About {round(SAM / 1000)} thousand.",
    ], punch=lambda L: [L[2] + 1.6], sfx=lambda L: [(L[0] + 0.3, 'pop'), (L[0] + 1.2, 'pop'), (L[1] + 2.4, 'ding'),
                                                    (L[2] + 1.6, 'down')]),
    dict(S, draw=s_c, tail=0.3, lines=[
        f"Alex only put in {round((PUT_A - PUT_S) / 1000)} thousand dollars more, but ended up with about "
        f"{round(GAP / 1000)} thousand more.",
        "That's compounding: your money earns money, and then that money earns money too.",
        "So the best time to start was ten years ago. The second best time is today.",
    ], sfx=lambda L: [(L[0] + 0.1, 'pop'), (L[0] + 0.7, 'pop'), (L[1] + 0.2, 'whoosh'), (L[2] + 0.5, 'down')]),
]


def check_numbers():
    script = ' '.join(l for sc in SCENES for l in sc['lines'])
    r = RATE / 12
    for n, v in ((480, ALEX), (360, SAM)):  # closed form of the monthly annuity must match the simulation
        assert abs(PMT * ((1 + r) ** n - 1) / r - v) < 1
    assert 2.0 < ALEX / SAM < 2.3 and 'double the money' in script
    assert round(ALEX / 1000) == 525 and round(SAM / 1000) == 244 and round(GAP / 1000) == 281
    assert PUT_A - PUT_S == 24000 and 'not a promise' in script
    print(f'numbers check: OK  Alex ${ALEX:,.0f} (put in ${PUT_A:,}), Sam ${SAM:,.0f} (put in ${PUT_S:,})')


if __name__ == '__main__':
    check_numbers()
    os.makedirs(BUILD, exist_ok=True)
    if '--stills' in sys.argv:
        out = os.path.join(BUILD, 'stills')
        os.makedirs(out, exist_ok=True)
        for si, sc in enumerate(SCENES):
            starts = [0.1 + 3.2 * j for j in range(3)]
            for j in range(3):
                for du in (0.8, 2.6):
                    still(sc, starts[j] + du, os.path.join(out, f's{si}_{j}_{du}.png'), starts=starts, layout='short')
        print('stills in', out)
        sys.exit()
    build(SCENES, os.path.join(OUT, 'sx01_short_compound.mp4'), BUILD, layout='short', loop=True)
