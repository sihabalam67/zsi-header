#!/usr/bin/env python3
"""Coin Theory, episode 1: Where did your $100 go? (inflation)

Data: US CPI-U (CPIAUCSL), Bureau of Labor Statistics via FRED, through Sept 2026.
    python3 channel/ep01_inflation.py            # full render -> channel/out/ep01_inflation.mp4
    python3 channel/ep01_inflation.py --stills   # preview frames only
"""
import math
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import *  # noqa: E402,F401,F403

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
BUILD = os.path.join(HERE, 'build', 'ep01')

# ------------------------------------------------------------------- data ---
_cpi = pd.read_csv(os.path.join(HERE, 'data', 'CPIAUCSL.csv'))
_cpi.columns = ['date', 'cpi']
_cpi['date'] = pd.to_datetime(_cpi['date'])
_cpi['cpi'] = pd.to_numeric(_cpi['cpi'], errors='coerce')
_cpi = _cpi.dropna().set_index('date')['cpi']
ANNUAL = _cpi.groupby(_cpi.index.year).mean()
YEARS = [y for y in ANNUAL.index if y >= 1950]
CPI_Y = [ANNUAL[y] for y in YEARS]
LATEST = _cpi.iloc[-1]
DOLLAR_1970 = LATEST / ANNUAL[1970]                       # ~8.66
_m = _cpi.copy()
YOY = ((_m / _m.shift(12, freq='MS').reindex(_m.index)) - 1).dropna() * 100
YOY_X = [d.year + (d.month - 1) / 12 for d in YOY.index if d.year >= 1960]
YOY_Y = [v for d, v in YOY.items() if d.year >= 1960]


# ----------------------------------------------------------------- scenes ---
def s_hook(c, x):
    t, L = x.t, x.L
    specks(c, t, 1)
    # bedroom: mattress
    mk = fade(t, 0.1)
    c.rrect(380, 470, 900, 540, 26, (90, 104, 160), (60, 70, 120), 4, a=mk)
    c.rrect(390, 440, 890, 488, 22, CREAM, (200, 196, 186), 3, a=mk)
    # bill slides under the mattress, then comes back out
    k_in = ease(seg(t, L[0] + 1.0, L[0] + 2.2))
    k_out = ease(seg(t, L[1] + 2.0, L[1] + 3.0))
    shrink = ease(seg(t, L[2] + 1.6, L[2] + 3.2))
    bx = lerp(lerp(250, 640, k_in), 640, k_out)
    by = lerp(lerp(330, 470, k_in), 300, k_out)
    bw = 260 * lerp(1, 0.55, shrink)
    if k_in < 1 or k_out > 0:
        bill(c, bx, by, bw, '100', a=1, tint=0.35 * shrink)
    c.rrect(380, 470, 900, 540, 26, (90, 104, 160), (60, 70, 120), 4, a=mk * (1 if k_in > 0.9 and k_out < 0.05 else 0))
    # year counter
    yk = ease(seg(t, L[1], L[1] + 2.0))
    if t > L[0]:
        year = int(lerp(1970, 2026, yk))
        c.text(640, 120, str(year), 72, GOLD, 900, a=fade(t, L[0]))
        c.icon('calendar', 520, 120, 48, GOLD, a=fade(t, L[0]))
    # comparison card
    ck = pop(t, L[2] + 2.0)
    if ck > 0:
        c.rrect(860, 230, 1160, 380, 20, (255, 255, 255, 18), MUTED, 2, a=clamp(ck))
        c.text(1010, 270, 'buys what', 22, MUTED, 600, a=clamp(ck))
        c.text(1010, 325, '$12', 54, CORAL, 900, a=clamp(ck))
        c.text(1010, 365, 'bought in 1970', 18, MUTED, 600, a=clamp(ck))
    # Penny reacts
    mood = 'happy'
    if t > L[2] + 1.6:
        mood = 'worried'
    if t > L[3]:
        mood = 'shocked'
    penny(c, 200, 420, 62, t, mood, look=(1, 0), wave=t < L[0] + 1.0)
    # the missing $88 flies away as coins
    for i in range(8):
        k = seg(t, L[3] + 0.2 + i * 0.08, L[3] + 1.6 + i * 0.08)
        if 0 < k < 1:
            c.circle(640 + i * 30 * k + 200 * k, 300 - 260 * ease(k) + i * 6, 12, GOLD, GOLD_D, 2, a=1 - k)
    qa = fade(t, L[3] + 0.4)
    c.text(660, 210, '-$88 ?', 40, CORAL, 900, a=qa)


def s_title(c, x):
    t = x.t
    specks(c, t, 2, 60)
    k = ease_out(seg(t, 0.1, 0.7))
    c.text(640, 300 - 20 * (1 - k), 'WHERE DID YOUR', 58, WHITE, 900, a=k, family='Poppins')
    c.text(640, 380 - 20 * (1 - k), '$100 GO?', 110, GOLD, 900, a=k)
    penny(c, 640, 560, 40, t, 'happy', wave=True, a=fade(t, 0.5))
    c.text(640, 660, 'COIN THEORY', 22, MUTED, 800, a=fade(t, 0.8))


BASKET = [('apple', 'Food'), ('house', 'Rent'), ('fuel', 'Fuel'), ('shirt', 'Clothes'), ('bus', 'Transport'),
          ('stethoscope', 'Doctor')]


def s_basket(c, x):
    t, L = x.t, x.L
    specks(c, t, 3)
    hk = ease_out(seg(t, L[0], L[0] + 0.5))
    c.text(640, 110 - 10 * (1 - hk), 'INFLATION', 64, CORAL, 900, a=hk)
    c.text(640, 165, 'prices rising across the whole economy', 22, MUTED, 600, a=fade(t, L[0] + 0.6))
    if t < L[1]:  # rising price tags
        for i in range(3):
            rise = ease(seg(t, L[0] + 1 + i * 0.4, L[0] + 3.5 + i * 0.4))
            price = f'${(2 + i) * (1 + rise * 0.8):.2f}'
            price_tag(c, 400 + i * 240, 400 - 60 * rise, 1.1, price, a=fade(t, L[0] + 0.8 + i * 0.3))
    else:
        merge = ease(seg(t, L[2], L[2] + 1.6))
        c.icon('shopping-basket', 640, 400, 110 * (1 - 0.4 * merge), GOLD, a=fade(t, L[1]) * (1 - merge))
        for i, (ic, label) in enumerate(BASKET):
            ang = -math.pi / 2 + i * 2 * math.pi / len(BASKET)
            k = pop(t, L[1] + 1.2 + i * 0.55)
            r = lerp(200, 0, merge)
            ix, iy = 640 + math.cos(ang) * r * 1.25, 400 + math.sin(ang) * r * 0.85
            a = clamp(k) * (1 - merge) ** 3
            c.circle(ix, iy, 46 * k, (255, 255, 255, 22), MUTED, 2, a=a)
            c.icon(ic, ix, iy, 46 * k, WHITE, a=a)
            c.text(ix, iy + 66, label, 18, MUTED, 600, a=a)
        if merge > 0.5:
            k = pop(t, L[2] + 1.4)
            c.rrect(470, 340, 810, 460, 24, GOLD, GOLD_D, 4, a=clamp(k))
            c.text(640, 380, 'CONSUMER', 26, INK, 900, a=clamp(k), shadow=False)
            c.text(640, 420, 'PRICE INDEX', 26, INK, 900, a=clamp(k), shadow=False)


def s_cpi_chart(c, x):
    t, L = x.t, x.L
    c.text(640, 60, 'US Consumer Price Index, 1950 - 2026', 30, WHITE, 800, a=fade(t, 0))
    k = ease(seg(t, L[0] + 0.5, L[0] + 5.5))
    px, py = line_chart(c, (150, 120, 1150, 560), YEARS, CPI_Y, (1950, 2026), (0, 350), k, GOLD,
                        xticks=range(1950, 2030, 10), yticks=range(0, 351, 50), a=fade(t, 0.1),
                        head_label=(lambda xm: f'{int(xm)}') if k < 1 else None)
    if t > L[1]:
        for yr, label, col, dy in ((1970, '$1.00', MINT, -60), (2026, f'${DOLLAR_1970:.2f}', CORAL, -60)):
            v = ANNUAL[yr] if yr in ANNUAL else LATEST
            kk = pop(t, L[1] + (0.3 if yr == 1970 else 2.2))
            if kk > 0:
                c.circle(px(yr), py(v), 9 * kk, col, WHITE, 2)
                c.rrect(px(yr) - 70, py(v) + dy - 26, px(yr) + 70, py(v) + dy + 26, 14, col, a=clamp(kk))
                c.text(px(yr), py(v) + dy, label, 28, INK, 900, a=clamp(kk), shadow=False)
                c.text(px(yr), py(v) + dy + 46, str(yr) if yr < 2026 else 'today', 16, col, 700, a=clamp(kk))
    if t > L[2]:
        k2 = pop(t, L[2] + 0.4)
        c.rrect(200, 150, 520, 230, 18, (255, 255, 255, 25), GOLD, 3, a=clamp(k2))
        c.text(360, 180, '~3.9% a year', 32, GOLD, 900, a=clamp(k2))
        c.text(360, 212, 'average since 1970', 16, MUTED, 600, a=clamp(k2))
    c.text(1150, 600, 'Source: BLS CPI-U via FRED', 14, MUTED, 400, anchor='rm', a=fade(t, 1), shadow=False)


def s_why(c, x):
    t, L = x.t, x.L
    specks(c, t, 4)
    title_card(c, t, 0, 'Why do prices rise?')
    if t < L[1] + 0.3:
        a = 1 - fade(t, L[1], 0.3)
        grow = ease(seg(t, L[0] + 2, L[0] + 6))
        n_coins = int(4 + 14 * grow)
        for i in range(n_coins):
            c.ellipse(380, 520 - i * 16, 70, 14, GOLD, GOLD_D, 3, a=a)
        c.text(380, 580, 'MONEY', 26, GOLD, 900, a=a)
        for i in range(4):
            c.rrect(830, 520 - i * 56 - 46, 950, 520 - i * 56 + 8, 8, (180, 140, 100), (120, 90, 60), 3, a=a)
        c.text(890, 580, 'STUFF', 26, (210, 170, 130), 900, a=a)
        price_tag(c, 640, 300 - 120 * grow, 1.2, f'${1 + 1.5 * grow:.2f}', CORAL, a=a * fade(t, L[0] + 2.4))
        c.icon('arrow-big-up', 640, 400 - 60 * grow, 60, CORAL, a=a * fade(t, L[0] + 2.4))
    else:
        items = [('landmark', 'Big spending'), ('percent', 'Cheap loans'), ('factory', 'Supply shocks')]
        for i, (ic, label) in enumerate(items):
            k = pop(t, L[1] + 0.3 + i * 1.4)
            cx = 320 + i * 320
            c.circle(cx, 360, 90 * k, (255, 255, 255, 20), GOLD, 3, a=clamp(k))
            c.icon(ic, cx, 360, 80 * k, GOLD, a=clamp(k))
            c.text(cx, 490, label, 26, WHITE, 800, a=clamp(k))


def s_spikes(c, x):
    t, L = x.t, x.L
    c.text(640, 60, 'US inflation, % change from a year earlier', 30, WHITE, 800, a=fade(t, 0))
    k = ease(seg(t, L[0] + 0.3, L[0] + 4.5))
    px, py = line_chart(c, (150, 120, 1150, 560), YOY_X, YOY_Y, (1960, 2026.75), (-4, 16), k, SKY,
                        xticks=range(1960, 2030, 10), yticks=range(-4, 17, 4), yfmt='{:.0f}%', a=fade(t, 0.1),
                        width=4)
    c.line([(px(1960), py(2)), (px(2026.75), py(2))], (52, 211, 153, 120), 2, a=fade(t, 0.5))
    c.text(px(2026.75), py(2) - 14, '2% target', 14, MINT, 700, anchor='rm', a=fade(t, 0.5), shadow=False)
    for when, val, label, delay in ((1980.17, 14.6, 'Mar 1980: 14.6%', 0.4), (2022.42, 9.0, 'Jun 2022: ~9%', 3.0)):
        kk = pop(t, L[1] + delay)
        if kk > 0:
            c.circle(px(when), py(val), 10 * kk, CORAL, WHITE, 2)
            c.rrect(px(when) - 105, py(val) - 62, px(when) + 105, py(val) - 22, 14, CORAL, a=clamp(kk))
            c.text(px(when), py(val) - 42, label, 20, INK, 800, a=clamp(kk), shadow=False)
    c.text(1150, 600, 'Source: BLS CPI-U via FRED', 14, MUTED, 400, anchor='rm', a=fade(t, 1), shadow=False)


def s_target(c, x):
    t, L = x.t, x.L
    specks(c, t, 5)
    if t < L[1]:
        k = pop(t, L[0] + 2.5)
        c.circle(640, 320, 140 * k, (255, 255, 255, 18), MINT, 5, a=clamp(k))
        c.text(640, 310, '2%', 110, MINT, 900, a=clamp(k))
        c.text(640, 390, 'the target', 22, MUTED, 600, a=clamp(k))
        penny(c, 300, 400, 56, t, 'shocked' if t < L[0] + 2.4 else 'happy', look=(1, 0))
    elif t < L[2]:
        steps = [('hourglass', 'People wait'), ('trending-down', 'Sales drop'), ('user-minus', 'Jobs cut'),
                 ('tag', 'Prices fall')]
        spin = ease(seg(t, L[1] + 2, L[2])) * 0.6
        c.icon('refresh-cw', 640, 360, 120, (255, 255, 255, 60), a=fade(t, L[1]))
        for i, (ic, label) in enumerate(steps):
            ang = -math.pi / 2 + i * math.pi / 2 + spin
            k = pop(t, L[1] + 0.8 + i * 0.9)
            ix, iy = 640 + math.cos(ang) * 230, 360 + math.sin(ang) * 190
            c.circle(ix, iy, 54 * k, CORAL_D, CORAL, 3, a=clamp(k))
            c.icon(ic, ix, iy, 52 * k, WHITE, a=clamp(k))
            c.text(ix, iy + 80, label, 20, WHITE, 700, a=clamp(k))
        c.text(640, 80, 'The deflation spiral', 36, CORAL, 900, a=fade(t, L[1]))
    else:
        penny(c, 640, 380, 80, t, 'happy', wave=True)
        for i in range(6):
            k = (t * 0.6 + i / 6) % 1
            c.circle(480 + i * 64, 560 - 400 * k, 10, GOLD, GOLD_D, 2, a=math.sin(k * math.pi))


def s_winners(c, x):
    t, L = x.t, x.L
    specks(c, t, 6)
    title_card(c, t, L[0], 'Who loses? Who wins?')
    cols = [(260, 'Cash savers', CORAL, 'piggy-bank', 1), (640, 'Fixed-rate borrowers', MINT, 'house', 2),
            (1020, 'Workers whose pay lags', CORAL, 'briefcase', 3)]
    for cx, label, col, ic, li in cols:
        if t < L[li]:
            continue
        k = pop(t, L[li])
        good = col == MINT
        person(c, cx, 470, 1.0 * k, col, t, li, 'happy' if good else 'sad', a=clamp(k))
        c.icon(ic, cx + 70, 330, 56 * k, col, a=clamp(k))
        c.text(cx, 540, label, 22, WHITE, 800, a=clamp(k))
        c.text(cx, 575, 'WIN' if good else 'LOSE', 28, col, 900, a=fade(t, L[li] + 0.8))
        if li == 1:  # savings melting
            m = ease(seg(t, L[1] + 1, L[1] + 4))
            bill(c, cx - 70, 300, 100 * (1 - 0.45 * m), '100', tint=0.5 * m, a=clamp(k))
        if li == 3:  # salary vs prices bars
            g = ease(seg(t, L[3] + 1.2, L[3] + 4))
            c.rrect(cx - 150, 260 - 40, cx - 110, 260 + 40, 6, SKY, a=clamp(k))
            c.rrect(cx - 100, 260 + 40 - 80 * (1 + 0.6 * g), cx - 60, 260 + 40, 6, CORAL, a=clamp(k))
            c.text(cx - 130, 315, 'pay', 14, SKY, 700, a=clamp(k), shadow=False)
            c.text(cx - 80, 315, 'prices', 14, CORAL, 700, a=clamp(k), shadow=False)


def s_rule70(c, x):
    t, L = x.t, x.L
    specks(c, t, 7)
    k = pop(t, L[0] + 0.5)
    c.rrect(250, 90, 1030, 200, 24, (255, 255, 255, 20), GOLD, 3, a=clamp(k))
    c.text(640, 145, '70 ÷ inflation rate = years to double', 36, GOLD, 900, a=clamp(k))
    rows = [(2, 35, MINT, 0.3), (7, 10, CORAL, 3.0)]
    for i, (rate, yrs, col, d) in enumerate(rows):
        if t < L[1] + d:
            continue
        y = 330 + i * 140
        g = ease(seg(t, L[1] + d, L[1] + d + 1.6))
        c.text(200, y, f'{rate}%', 48, col, 900, a=fade(t, L[1] + d))
        c.rrect(300, y - 26, 300 + 700 * (yrs / 35) * g, y + 26, 14, col, a=fade(t, L[1] + d))
        c.text(320 + 700 * (yrs / 35) * g, y, f'{int(round(yrs * g))} years', 30, WHITE, 900, anchor='lm',
               a=fade(t, L[1] + d))


def s_lesson(c, x):
    t, L = x.t, x.L
    specks(c, t, 8)
    melt = ease(seg(t, L[0] + 1, L[1] + 3))
    # melting cash pile
    for i in range(5):
        c.rrect(260 - 80 + i * 4, 420 - i * 22 * (1 - melt * 0.7), 260 + 80 + i * 4, 420 - i * 22 * (1 - melt * 0.7) + 20,
                6, BILL, BILL_D, 2, a=1 - melt * 0.4)
    c.ellipse(260, 445, 110 * (1 + melt), 14 * (1 + melt), (134, 190, 120, 120))
    c.text(260, 520, 'Cash sitting still', 22, CORAL, 800)
    # growing sprout
    g = ease(seg(t, L[0] + 2, L[0] + 6))
    c.icon('sprout', 1000, 420 - 60 * g, 80 + 80 * g, MINT)
    c.text(1000, 520, 'Growing with prices', 22, MINT, 800)
    c.icon('trending-up', 640, 360, 70, (255, 255, 255, 120), a=fade(t, L[0] + 2))
    k = pop(t, L[1])
    c.rrect(430, 110, 850, 170, 18, (255, 255, 255, 20), MUTED, 2, a=clamp(k))
    c.text(640, 140, 'Education only - not financial advice', 22, WHITE, 700, a=clamp(k))


def s_outro(c, x):
    t, L = x.t, x.L
    specks(c, t, 9, 50)
    penny(c, 340, 400, 70, t, 'talk' if t < L[0] + 3 else 'happy', look=(1, 0))
    bill(c, 560, 380, 150, '100', tint=0.3)
    if t > L[1]:
        k = pop(t, L[1])
        c.rrect(700, 200, 1160, 420, 24, (255, 255, 255, 22), GOLD, 3, a=clamp(k))
        c.text(930, 240, 'NEXT EPISODE', 20, GOLD, 800, a=clamp(k))
        c.icon('house', 930, 310, 70, WHITE, a=clamp(k))
        c.text(930, 380, 'Why houses got so expensive', 24, WHITE, 800, a=clamp(k))
        sk = pop(t, L[1] + 2.4)
        c.rrect(810, 460, 1050, 520, 30, CORAL, a=clamp(sk))
        c.icon('bell', 850, 490, 28, WHITE, a=clamp(sk))
        c.text(950, 490, 'SUBSCRIBE', 24, WHITE, 900, a=clamp(sk), shadow=False)


SCENES = [
    dict(draw=s_hook, chapter='Intro: the mattress experiment', lines=[
        "Imagine it's nineteen seventy, and you hide a hundred-dollar bill under your mattress.",
        "You forget about it for fifty-six years, and find it again today.",
        "It's still a hundred dollars. But now it only buys about as much as twelve dollars did back then.",
        "So where did the other eighty-eight dollars go?",
    ], sfx=lambda L: [(L[0] + 1.0, 'whoosh'), (L[1] + 2.0, 'whoosh'), (L[2] + 1.6, 'down'), (L[2] + 2.0, 'pop'),
                      (L[3] + 0.2, 'whoosh')]),
    dict(draw=s_title, lines=[], min=3.2, captions=False, sfx=lambda L: [(0.2, 'ding')]),
    dict(draw=s_basket, chapter='What inflation is', lines=[
        "The answer is inflation: the slow, steady rise of prices across the whole economy.",
        "To measure it, the government checks the prices of a huge basket of things people buy every month: "
        "food, rent, fuel, clothes, transport, and doctor visits.",
        "Put it all together, and you get one number: the Consumer Price Index.",
    ], sfx=lambda L: [(L[0], 'pop')] + [(L[1] + 1.2 + i * 0.55, 'pop') for i in range(6)] + [(L[2] + 1.4, 'ding')]),
    dict(draw=s_cpi_chart, chapter='70 years of prices', lines=[
        "Here's that index for the United States since nineteen fifty. Notice something? It almost never goes down.",
        "Something that cost one dollar in nineteen seventy costs about eight dollars and sixty-six cents today.",
        "That's prices rising by almost four percent a year, on average, for more than half a century.",
    ], sfx=lambda L: [(L[1] + 0.3, 'pop'), (L[1] + 2.2, 'ding'), (L[2] + 0.4, 'pop')]),
    dict(draw=s_why, chapter='Why prices rise', lines=[
        "So why do prices keep climbing? The simplest answer: when more money chases the same amount of stuff, "
        "prices go up.",
        "That can happen when governments and people spend a lot, when borrowing is cheap, or when supply breaks "
        "down, like when factories close or oil gets expensive.",
    ], sfx=lambda L: [(L[1] + 0.3 + i * 1.4, 'pop') for i in range(3)]),
    dict(draw=s_spikes, chapter='When inflation explodes', lines=[
        "Most of the time, inflation is slow and quiet. But sometimes, it explodes.",
        "In March nineteen eighty, prices were rising almost fifteen percent a year. And in June twenty twenty-two, "
        "after the pandemic, inflation hit about nine percent, the highest in four decades.",
    ], sfx=lambda L: [(L[1] + 0.4, 'pop'), (L[1] + 3.0, 'pop')]),
    dict(draw=s_target, chapter='Why not zero inflation?', lines=[
        "So shouldn't the goal be zero inflation? Surprisingly, no. The US Federal Reserve aims for about two percent.",
        "Because falling prices can be even worse. If you expect things to be cheaper next month, you wait. "
        "Businesses sell less, cut jobs, and prices fall even further.",
        "A little inflation keeps money moving.",
    ], sfx=lambda L: [(L[0] + 2.5, 'ding')] + [(L[1] + 0.8 + i * 0.9, 'pop') for i in range(4)]),
    dict(draw=s_winners, chapter='Winners and losers', lines=[
        "But inflation doesn't treat everyone the same.",
        "If you keep your savings in cash, you lose. Your money quietly buys less every single year.",
        "If you owe money at a fixed interest rate, you can actually win, because you pay it back with dollars "
        "that are worth less.",
        "And if your pay rises slower than prices, you're getting a pay cut, even if your salary never changes.",
    ], sfx=lambda L: [(L[1], 'pop'), (L[1] + 1, 'down'), (L[2], 'pop'), (L[3], 'pop')]),
    dict(draw=s_rule70, chapter='The rule of 70', lines=[
        "Here's a handy trick. Divide seventy by the inflation rate, and you get roughly how many years it takes "
        "for prices to double.",
        "At two percent, prices double in about thirty-five years. At seven percent, in just ten.",
    ], sfx=lambda L: [(L[0] + 0.5, 'ding'), (L[1] + 0.3, 'whoosh'), (L[1] + 3.0, 'whoosh')]),
    dict(draw=s_lesson, chapter='The lesson', lines=[
        "That's why many people don't leave long-term savings sitting in cash. They look for places where money "
        "can grow at least as fast as prices, knowing that every option comes with its own risks.",
        "This channel isn't financial advice. But the lesson is simple: money that sits still slowly melts.",
    ]),
    dict(draw=s_outro, chapter='Where your $100 went', tail=1.5, lines=[
        "So, where did your hundred dollars go? Nowhere. It just shrank, a few cents at a time.",
        "Next time, we'll find out why houses got so expensive. Subscribe so you don't miss it.",
    ], sfx=lambda L: [(L[1], 'pop'), (L[1] + 2.4, 'ding')]),
]


def fmt(sec):
    return f'{int(sec // 60)}:{int(sec % 60):02d}'


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    if '--stills' in sys.argv:
        os.makedirs(BUILD, exist_ok=True)
        for i, sc in enumerate(SCENES):
            n = max(1, len(sc['lines']))
            still(sc, 0.5 + 4 * n - 0.5, os.path.join(BUILD, f'still_{i:02d}.png'))
        sys.exit()
    total, chapters = build(SCENES, os.path.join(OUT, 'ep01_inflation.mp4'), BUILD)
    with open(os.path.join(OUT, 'ep01_chapters.txt'), 'w') as f:
        for at, name in chapters:
            f.write(f'{fmt(at)} {name}\n')
    print(open(os.path.join(OUT, 'ep01_chapters.txt')).read())
