"""Standalone Short: "Same $100, four friends" - an original, honest take on the classic $100-and-hens money parable
(the viral versions ignore feed costs and risk; this one includes both and ends on a bird-flu twist).

    python3 channel/sx12_short_hens.py [--stills]

Numbers: channel/hens_math.py (BLS egg prices, CPI, USDA flock rule; story assumptions said on screen).
"""
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from wk2_art import *  # noqa: E402,F401,F403
from engine import build, still, person  # noqa: E402
import fx  # noqa: E402
import hens_math as H  # noqa: E402

OUT = os.path.join(HERE, 'out')
BUILD = os.path.join(HERE, 'build', 'sx12_short_hens')
KEYS = ('jar', 'keeper', 'reinvest', 'borrow')
COLS = (SKY, MINT, GOLD, CORAL)
LANE_Y = (330, 500, 670, 840)  # lane centres
G = {k: round(H.GOOD[k]['net']) for k in KEYS}
F = {k: round(H.FLU[k]['net']) for k in KEYS}
REAL = round(H.GOOD['jar']['real'])
NH = H.GOOD['reinvest']['hens']
PRICE = H.PRICE


def money(v):
    return f'-${abs(v):,.0f}' if v < 0 else f'${v:,.0f}'


def hen(c, x, y, s, a=1.0):
    """A small cartoon hen, feet at (x, y)."""
    c.circle(x, y - 22 * s, 20 * s, CREAM, mix(CREAM, INK, 0.45), 2.5 * s, a)       # body
    c.circle(x + 14 * s, y - 40 * s, 11 * s, CREAM, mix(CREAM, INK, 0.45), 2.5 * s, a)  # head
    c.circle(x + 12 * s, y - 53 * s, 4.5 * s, CORAL, a=a)
    c.circle(x + 18 * s, y - 52 * s, 4 * s, CORAL, a=a)                              # comb
    c.poly([(x + 24 * s, y - 42 * s), (x + 32 * s, y - 39 * s), (x + 24 * s, y - 36 * s)], GOLD, a=a)  # beak
    c.circle(x + 16 * s, y - 42 * s, 2 * s, INK, a=a)
    c.line([(x - 4 * s, y - 4 * s), (x - 4 * s, y)], GOLD, 2.5 * s)
    c.line([(x + 6 * s, y - 4 * s), (x + 6 * s, y)], GOLD, 2.5 * s)


def jar(c, x, y, s, a=1.0):
    c.rrect(x - 28 * s, y - 70 * s, x + 28 * s, y, 12 * s, (210, 235, 245), mix(SKY, INK, 0.3), 3 * s, a * 0.9)
    c.rrect(x - 22 * s, y - 80 * s, x + 22 * s, y - 68 * s, 4 * s, MUTED, a=a)
    bill(c, x, y - 30 * s, 40 * s, '100', a=a)


def lane(c, i, t, val, hens=0, focus=None, flu=0.0, tag=None, tagcol=None, crown=False, loan=False):
    y = LANE_Y[i]
    dim = 1.0 if focus in (None, i) else 0.35
    c.rrect(30, y - 78, 690, y + 78, 26, (24, 30, 48), COLS[i] if focus == i else None, 4, dim)
    c.circle(78, y, 26, COLS[i], a=dim)
    c.text(78, y, str(i + 1), 34, INK, 400, family='Anton', a=dim, shadow=False)
    person(c, 150, y + 58, 0.62, COLS[i], t, i, 'happy' if flu < 0.5 or i == 0 else 'sad', dim)
    if i == 0:
        jar(c, 245, y + 50, 1.0, dim)
    else:
        n = hens
        cols = 10 if n > 8 else max(1, n)
        sc = 0.62 if n > 8 else 0.85
        for j in range(n):  # hens in rows, fading out if the flu hits
            hx = 215 + (j % cols) * (34 if n > 8 else 44)
            hy = y + 14 + (j // cols) * 42 - (20 if n > 10 else 0)
            hen(c, hx, hy + (0 if n <= 8 else 6), sc, dim * (1 - flu))
    if loan:
        c.rrect(205, y - 70, 345, y - 40, 14, CORAL, a=dim)
        c.text(275, y - 55, f'LOAN ${H.LOAN:.0f}', 20, INK, 400, family='Anton', a=dim, shadow=False)
    vc = CORAL if val < 0 else (MINT if val > 100 else WHITE)
    c.text(605, y - 6, money(val), 52, vc, 400, family='Anton', a=dim)
    if tag:
        c.text(672, y + 46, tag, 18, tagcol or MUTED, 900, a=dim, shadow=False, anchor='rm')
    if crown:
        c.text(605, y - 62, 'WINNER', 22, GOLD, 900, a=dim)


def board(c, t, vals, hens=(0, 4, 4, 20), focus=None, flu=0.0, tags=None, crown=None, loan=False, title=None):
    c.rrect(0, 0, 720, 1280, 0, (14, 18, 30))
    if title:
        c.text(360, 190, title, 40, WHITE, 900)
    for i in range(4):
        tg = (tags or {}).get(i)
        lane(c, i, t, vals[i], hens[i], focus, flu, tg[0] if tg else None, tg[1] if tg else None, crown == i,
             loan and i == 3)


def count(a, b, u, t0=0.2, d=1.4):
    return a + (b - a) * ease(fx.clamp((u - t0) / d))


def hook_draw(c, u, t=0.0):
    board(c, t, [100, 100, 100, 100], (0, 4, 4, 20), title=None)
    c.rrect(0, 0, 720, 1280, 0, (8, 10, 20, 170))
    c.text(360, 200, 'SAME $100. FOUR FRIENDS.', 40, WHITE, 900)
    s = 1.0 + 0.06 * max(0.0, 1 - abs(u - 0.15) / 0.15) if u < 0.3 else 1.0
    fx.title(c, money(G['borrow']), 470, int(190 * s), MINT, 1, stroke=8)
    ko = fx.clamp(fx.pop(u, 2.4, 0.3))
    if ko > 0:
        c.text(360, 640, 'OR', 54, WHITE, 900, a=ko)
        fx.title(c, money(F['borrow']), 790, int(150 * (0.6 + 0.4 * ko) * s), CORAL, ko, stroke=8)
    if u > 0:
        fx.zoom_canvas(c, 1.01 + 0.012 * u, 360, 600)


def s_hook(c, x):
    hook_draw(c, max(0.0, x.t - x.L[0]), x.t)


def s_rules(c, x):  # the story math, with the real egg price
    u = x.t - x.L[0]
    c.rrect(0, 0, 720, 1280, 0, (14, 18, 30))
    c.rrect(250, 170, 470, 215, 22, GOLD, a=fade(u, 0))
    c.text(360, 192, 'STORY MATH', 26, INK, 400, family='Anton', a=fade(u, 0), shadow=False)
    hen(c, 360, 560, 4.2 * (0.6 + 0.4 * fx.clamp(fx.pop(u, 0.1, 0.4))))
    l1 = x.L[1] - x.L[0] if len(x.L) > 1 else 3.0
    rows = ((f'HEN: ${H.HEN:.0f}', 0.4), (f'{H.DOZEN_YR:.0f} DOZEN EGGS / YEAR', 1.6),
            (f'EGGS SELL ${PRICE:.2f} / DOZEN', l1 + 0.1), (f'FEED: ${H.FEED_YR:.0f} / YEAR', l1 + 2.2))
    for j, (txt, at) in enumerate(rows):
        k = fx.pop(u, at, 0.3)
        if k > 0:
            c.rrect(110, 640 + j * 82, 610, 706 + j * 82, 26, WHITE, a=fx.clamp(k))
            c.text(360, 673 + j * 82, txt, 34, INK, 400, family='Anton', a=fx.clamp(k), shadow=False)
    if u > l1:
        c.text(360, 245, f'egg price: US average, BLS, {H.PRICE_DATE:%b %Y}', 22, MUTED, 800, a=fade(u, l1))
    fx.zoom_canvas(c, 1.01 + 0.006 * max(0.0, u), 360, 560)


def s_jar(c, x):
    u = x.t - x.L[0]
    tag = (f'WORTH ${REAL} AFTER INFLATION', CORAL) if u > 2.6 else None
    board(c, x.t, [100, 100, 100, 100], (0, 4, 4, 20), focus=0, tags={0: tag} if tag else None,
          title='1: KEEPS IT SAFE')


def s_keeper(c, x):
    u = x.t - x.L[0]
    board(c, x.t, [100, count(100, G['keeper'], u), 100, 100], (0, 4, 4, 20), focus=1,
          tags={1: ('SELLS THE EGGS', MUTED)}, title='2: BUYS 4 HENS')


def s_reinvest(c, x):
    u = x.t - x.L[0]
    nh = 4 + int((NH - 4) * ease(fx.clamp((u - 0.6) / 3.2)))
    board(c, x.t, [100, G['keeper'], count(100, G['reinvest'], u, 0.6, 3.2), 100], (0, 4, nh, 20), focus=2,
          tags={2: (f'{nh} HENS', GOLD)}, title='3: BUYS MORE HENS')


def s_borrow(c, x):
    u = x.t - x.L[0]
    win = u > 3.6
    board(c, x.t, [100, G['keeper'], G['reinvest'], count(100, G['borrow'], u, 1.4, 2.0)], (0, 4, NH, 20),
          focus=None if win else 3, loan=True, crown=3 if win else None, title='4: BORROWS $400')


def s_flu(c, x):  # the twist: the flock is culled
    u = x.t - x.L[0]
    k = fx.clamp((u - 1.2) / 0.8)
    board(c, x.t, [100, G['keeper'], G['reinvest'], G['borrow']], (0, 4, NH, 20), flu=k, loan=True)
    if u > 0.2:
        c.rrect(0, 0, 720, 1280, 0, (200, 30, 40, int(70 * (0.6 + 0.4 * math.sin(u * 8)))))
    kb = fx.pop(u, 0.2, 0.3)
    if kb > 0:
        sc = lerp(2.0, 1.0, fx.clamp(kb))
        c.rrect(360 - 260 * sc, 585 - 70 * sc, 360 + 260 * sc, 585 + 70 * sc, 22, CORAL, WHITE, 6, a=fx.clamp(kb))
        c.text(360, 585, 'BIRD FLU', int(104 * sc), WHITE, 400, family='Anton', a=fx.clamp(kb), shadow=False)
    fx.zoom_canvas(c, 1.01 + 0.01 * u, 360, 600)


def s_after(c, x):
    u = x.t - x.L[0]
    vals = [100] + [count(G[k], F[k], u, 0.3, 1.8) for k in KEYS[1:]]
    win = u > 2.4
    board(c, x.t, vals, (0, 0, 0, 0), flu=1.0, crown=0 if win else None, loan=True,
          tags={3: ('STILL OWES THE LOAN', CORAL)} if u > 3.5 else None, title='AFTER THE FLU')


def s_end(c, x):
    u = x.t - x.L[0]

    def question(cv):
        cv.rrect(0, 0, 720, 1280, 0, (14, 18, 30))
        fx.title(cv, 'WHICH FRIEND\nARE YOU?', 380, int(96 * (1 + 0.05 * math.sin(u * 6))), GOLD, 1)
        for j in range(4):
            kk = fx.clamp(fx.pop(u, 0.3 + j * 0.15, 0.3))
            bx = 135 + j * 150
            cv.rrect(bx - 60, 680 - 60 * kk, bx + 60, 680 + 60 * kk, 26, COLS[j])
            cv.text(bx, 680, str(j + 1), int(80 * kk) + 1, INK, 400, family='Anton', shadow=False)
        cv.text(360, 820 + 8 * math.sin(u * 4), 'comment 1, 2, 3 or 4', 34, WHITE, 900)
    brk = x.dur - x.L[0] - 0.95
    if u < brk:
        return question(c)
    fx.frame_break(c, u - brk + 0.5, x.t, question, lambda cv: hook_draw(cv, 0.0))


S = dict(vertical=True, lead=0.1, gap=0.15, captions=True, cap_y=1080)
SCENES = [
    dict(S, draw=s_hook, lead=0.05, lines=[
        f"!Four friends get the same 100 dollars. One turns it into {G['borrow']}... or ends up owing {abs(F['borrow'])}.",
    ], punch=lambda L: [0.12], sfx=lambda L: [(0.12, 'hit')]),
    dict(S, draw=s_rules, lines=[
        f"Story math: a hen costs {H.HEN:.0f} dollars and lays {H.DOZEN_YR:.0f} dozen eggs a year.",
        f"Eggs sell for {int(PRICE)} dollars and {round(PRICE * 100) % 100} cents a dozen. Feed costs {H.FEED_YR:.0f} dollars a year.",
    ], sfx=lambda L: [(L[0] + 0.1, 'pop'), (L[0] + 0.4, 'pop'), (L[0] + 1.6, 'pop'), (L[1] + 0.1, 'pop'),
                      (L[1] + 2.2, 'pop')]),
    dict(S, draw=s_jar, lines=[
        f"Friend one keeps it safe in a jar. A year later, still 100 dollars, but inflation makes it worth {REAL}.",
    ], sfx=lambda L: [(L[0] + 0.1, 'whoosh'), (L[0] + 2.6, 'down')]),
    dict(S, draw=s_keeper, lines=[
        f"Friend two buys four hens and sells the eggs: {G['keeper']} dollars.",
    ], sfx=lambda L: [(L[0] + 0.1, 'whoosh'), (L[0] + 1.6, 'ding')]),
    dict(S, draw=s_reinvest, lines=[
        f"Friend three buys a new hen every time he can. By December he has {NH} hens: {G['reinvest']} dollars.",
    ], sfx=lambda L: [(L[0] + 0.1, 'whoosh')] + [(L[0] + 0.8 + j * 0.45, 'pop') for j in range(7)]
                      + [(L[0] + 3.9, 'ding')]),
    dict(S, draw=s_borrow, lines=[
        f"!Friend four borrows 400 dollars and buys 20 hens. Even after interest: {G['borrow']} dollars.",
    ], sfx=lambda L: [(L[0] + 0.1, 'whoosh'), (L[0] + 2.6, 'riser'), (L[0] + 3.6, 'hit')]),
    dict(S, draw=s_flu, lines=[
        "!But in June, bird flu hits the farm, and the whole flock has to be culled.",
    ], sfx=lambda L: [(L[0] + 0.2, 'hit'), (L[0] + 1.2, 'down')]),
    dict(S, draw=s_after, lines=[
        f"Now the jar wins. Friend four still owes on his loan: minus {abs(F['borrow'])} dollars.",
    ], sfx=lambda L: [(L[0] + 0.3, 'down'), (L[0] + 2.4, 'ding'), (L[0] + 3.5, 'hit')]),
    dict(S, draw=s_end, tail=1.0, cam=(1.0, 1.0), lines=[
        "Borrowing multiplies wins and losses. Which friend are you? One, two, three or four?",
    ], sfx=lambda L: [(L[0] + 0.3 + j * 0.15, 'pop') for j in range(4)]),
]


def check_numbers():
    script = ' '.join(l for sc in SCENES for l in sc['lines'])
    assert PRICE == 2.27 and H.PRICE_DATE.year == 2026 and H.PRICE_2025 == 4.25
    assert abs(H.PROFIT_YR - 30.4) < 0.01
    assert (G['jar'], G['keeper'], G['reinvest'], G['borrow']) == (100, 222, 293, 660), G
    assert (F['jar'], F['keeper'], F['reinvest'], F['borrow']) == (100, 61, 21, -144), F
    assert NH == 11 and REAL == 96
    for n in ('660', '144', '222', '293', '2 dollars and 27 cents', f'worth {REAL}', f'{NH} hens'):
        assert n in script, n
    print(f'numbers check: OK  good {G}  flu {F}  eggs ${PRICE} ({H.PRICE_DATE:%b %Y}), inflation {H.INFL:.1%}')


if __name__ == '__main__':
    check_numbers()
    os.makedirs(BUILD, exist_ok=True)
    if '--stills' in sys.argv:
        out = os.path.join(BUILD, 'stills')
        os.makedirs(out, exist_ok=True)
        for si, sc in enumerate(SCENES):
            starts = [0.1 + 3.4 * j for j in range(len(sc['lines']))]
            for du in (0.0, 1.8, 3.8):
                still(sc, 0.1 + du, os.path.join(out, f's{si}_{du}.png'), starts=starts, layout='short')
        print('stills in', out)
        sys.exit()
    build(SCENES, os.path.join(OUT, 'sx12_short_hens.mp4'), BUILD, layout='short', loop=True)
