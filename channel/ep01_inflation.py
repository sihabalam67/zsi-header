#!/usr/bin/env python3
"""Coin Theory, episode 1: Where did your $100 go? (inflation)

All numbers come from the CSVs in channel/data (BLS via FRED, through Sept 2026), and
check_numbers() refuses to render if the narration disagrees with the data.

    python3 channel/ep01_inflation.py            # long video + captions + Short
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
def series(name):
    d = pd.read_csv(os.path.join(HERE, 'data', f'{name}.csv'))
    d.columns = ['date', 'v']
    d['date'] = pd.to_datetime(d['date'])
    d['v'] = pd.to_numeric(d['v'], errors='coerce')
    return d.dropna().set_index('date')['v']


CPI = series('CPIAUCSL')
ANNUAL = CPI.groupby(CPI.index.year).mean()
YEARS = [y for y in ANNUAL.index if y >= 1950]
CPI_Y = [ANNUAL[y] for y in YEARS]
LATEST = CPI.iloc[-1]
DOLLAR_1970 = LATEST / ANNUAL[1970]
YOY = ((CPI / CPI.shift(12, freq='MS').reindex(CPI.index)) - 1).dropna() * 100
YOY_X = [d.year + (d.month - 1) / 12 for d in YOY.index if d.year >= 1960]
YOY_Y = [v for d, v in YOY.items() if d.year >= 1960]
AVG_SINCE_1970 = ((LATEST / ANNUAL[1970]) ** (1 / (CPI.index[-1].year + CPI.index[-1].month / 12 - 1970.5)) - 1) * 100

FED = series('FEDFUNDS')
FED_X = [d.year + (d.month - 1) / 12 for d in FED.index if d.year >= 1960]
FED_Y = [v for d, v in FED.items() if d.year >= 1960]

PRICES = []  # (icon, label, unit, 1980 average price, latest price)
for sid, icon, label, unit in (('APU0000702111', 'croissant', 'White bread', 'per pound'),
                               ('APU0000708111', 'egg', 'Eggs', 'per dozen'),
                               ('APU0000717311', 'coffee', 'Coffee', 'per pound'),
                               ('APU000074714', 'fuel', 'Gasoline', 'per gallon')):
    s = series(sid)
    PRICES.append((icon, label, unit, s[s.index.year == 1980].mean(), s.iloc[-1]))

WAGE = series('AHETPI')
_j = pd.concat([WAGE, CPI], axis=1, keys=['w', 'c'], sort=True).dropna()
REAL = _j.w / _j.c * CPI.iloc[-1]
WAGE_X = [d.year + (d.month - 1) / 12 for d in WAGE.index]
WAGE_Y = list(WAGE.values)
REAL_X = [d.year + (d.month - 1) / 12 for d in REAL.index]
REAL_Y = list(REAL.values)
REAL_1973 = REAL[REAL.index.year == 1973].mean()
WAGE_1970 = WAGE[WAGE.index.year == 1970].mean()


def money(v):
    return f'{round(v * 100):d} cents' if v < 1 else f'${v:.2f}'


# ----------------------------------------------------------------- scenes ---
def s_hook(c, x):
    t, L = x.t, x.L
    specks(c, t, 1)
    mk = fade(t, 0.1)
    c.rrect(380, 470, 900, 540, 26, (90, 104, 160), (60, 70, 120), 4, a=mk)
    c.rrect(390, 440, 890, 488, 22, CREAM, (200, 196, 186), 3, a=mk)
    k_in = ease(seg(t, L[0] + 1.6, L[0] + 2.8))
    k_out = ease(seg(t, L[1] + 2.0, L[1] + 3.0))
    shrink = ease(seg(t, L[2] + 1.4, L[2] + 3.0))
    bx = lerp(lerp(250, 640, k_in), 640, k_out)
    by = lerp(lerp(300, 470, k_in), 300, k_out)
    if k_in < 1 or k_out > 0:
        bill(c, bx, by, 260 * lerp(1, 0.55, shrink), '100', tint=0.35 * shrink)
    if k_in > 0.9 and k_out < 0.05:
        c.rrect(380, 470, 900, 540, 26, (90, 104, 160), (60, 70, 120), 4)
    if t > L[1] - 0.2:
        yk = ease(seg(t, L[1], L[1] + 2.0))
        c.text(660, 120, str(int(lerp(1970, 2026, yk))), 72, GOLD, 900, a=fade(t, L[1] - 0.2))
        c.icon('calendar', 530, 120, 48, GOLD, a=fade(t, L[1] - 0.2))
    ck = pop(t, L[2] + 2.2)
    if ck > 0:
        c.rrect(870, 230, 1170, 380, 20, (255, 255, 255, 18), MUTED, 2, a=clamp(ck))
        c.text(1020, 270, 'buys what', 22, MUTED, 600, a=clamp(ck))
        c.text(1020, 325, '$12', 54, CORAL, 900, a=clamp(ck))
        c.text(1020, 365, 'bought in 1970', 18, MUTED, 600, a=clamp(ck))
    mood = 'happy' if t < L[2] + 1.4 else 'worried'
    if t > L[3]:
        mood = 'shocked'
    penny(c, 200, 420, 62, t, mood, look=(1, 0), wave=t < L[0] + 1.2, talk=x.talk())
    for i in range(8):
        k = seg(t, L[3] + 0.2 + i * 0.08, L[3] + 1.6 + i * 0.08)
        if 0 < k < 1:
            c.circle(640 + i * 30 * k + 200 * k, 300 - 260 * ease(k) + i * 6, 12, GOLD, GOLD_D, 2, a=1 - k)
    c.text(660, 210, '-$88 ?', 40, CORAL, 900, a=fade(t, L[3] + 0.4))


def s_title(c, x):
    t = x.t
    specks(c, t, 2, 60)
    k = ease_out(seg(t, 0.1, 0.7))
    c.text(640, 300 - 20 * (1 - k), 'WHERE DID YOUR', 58, WHITE, 900, a=k)
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
    if t < L[1]:
        for i in range(3):
            rise = ease(seg(t, L[0] + 1 + i * 0.4, L[0] + 3.5 + i * 0.4))
            price_tag(c, 400 + i * 240, 400 - 60 * rise, 1.1, f'${(2 + i) * (1 + rise * 0.8):.2f}',
                      a=fade(t, L[0] + 0.8 + i * 0.3))
        return
    merge = ease(seg(t, L[3], L[3] + 1.6))
    c.icon('shopping-basket', 640, 400, 110 * (1 - 0.4 * merge), GOLD, a=fade(t, L[1]) * (1 - merge))
    span = x.E[1] - L[1]
    for i, (ic, label) in enumerate(BASKET):
        ang = -math.pi / 2 + i * 2 * math.pi / len(BASKET)
        k = pop(t, L[1] + span * (0.35 + 0.1 * i))
        r = lerp(200, 0, merge)
        ix, iy = 640 + math.cos(ang) * r * 1.25, 400 + math.sin(ang) * r * 0.85
        a = clamp(k) * (1 - merge) ** 3
        c.circle(ix, iy, 46 * k, (255, 255, 255, 22), MUTED, 2, a=a)
        c.icon(ic, ix, iy, 46 * k, WHITE, a=a)
        c.text(ix, iy + 66, label, 18, MUTED, 600, a=a)
    if L[2] <= t < L[3]:
        k = pop(t, L[2] + 0.3)
        c.rrect(840, 540, 1180, 640, 18, (255, 255, 255, 22), GOLD, 2, a=clamp(k))
        c.text(1010, 575, '~80,000 prices', 28, GOLD, 900, a=clamp(k))
        c.text(1010, 612, 'collected every month', 16, MUTED, 600, a=clamp(k))
    if merge > 0.5:
        k = pop(t, L[3] + 1.4)
        c.rrect(470, 340, 810, 460, 24, GOLD, GOLD_D, 4, a=clamp(k))
        c.text(640, 380, 'CONSUMER', 26, INK, 900, a=clamp(k), shadow=False)
        c.text(640, 420, 'PRICE INDEX', 26, INK, 900, a=clamp(k), shadow=False)


def s_prices(c, x):
    t, L, E = x.t, x.L, x.E
    specks(c, t, 10)
    c.text(640, 70, 'Average US prices: 1980 vs today', 34, WHITE, 900, a=fade(t, 0))
    span = E[1] - L[1]
    for i, (icon, label, unit, p0, p1) in enumerate(PRICES):
        cx = 205 + i * 290
        k = pop(t, L[0] + 1.2 + i * 0.25)
        if k <= 0:
            continue
        a = clamp(k)
        c.rrect(cx - 125, 140, cx + 125, 560, 24, (255, 255, 255, 16), (255, 255, 255, 50), 2, a=a)
        c.icon(icon, cx, 205, 64, GOLD, a=a)
        c.text(cx, 265, label, 26, WHITE, 900, a=a)
        c.text(cx, 293, unit, 16, MUTED, 600, a=a)
        c.text(cx, 340, '1980', 16, MUTED, 700, a=a)
        c.text(cx, 372, money(p0), 30, MINT, 900, a=a)
        rk = ease(seg(t, L[1] + span * (0.25 * i + 0.08), L[1] + span * (0.25 * i + 0.22)))
        c.icon('arrow-down', cx, 410, 26, MUTED, a=a)
        c.text(cx, 445, 'today', 16, MUTED, 700, a=a)
        c.text(cx, 480, money(lerp(p0, p1, rk)), 36, CORAL, 900, a=a)
        mk = pop(t, L[1] + span * (0.25 * i + 0.22))
        if mk > 0:
            c.rrect(cx - 50, 510, cx + 50, 546, 18, CORAL, a=clamp(mk))
            c.text(cx, 528, f'x{p1 / p0:.1f}', 20, INK, 900, a=clamp(mk), shadow=False)
    c.text(1180, 600, 'Source: BLS average price data via FRED', 14, MUTED, 400, anchor='rm', a=fade(t, 1),
           shadow=False)
    if len(L) > 2 and t > L[2]:
        penny(c, 90, 610, 32, t, 'worried', talk=x.talk(), a=fade(t, L[2]), look=(1, -0.5))


def s_cpi_chart(c, x):
    t, L = x.t, x.L
    c.text(640, 60, 'US Consumer Price Index, 1950 - 2026', 30, WHITE, 800, a=fade(t, 0))
    k = ease(seg(t, L[0] + 0.5, L[0] + 5.5))
    px, py = line_chart(c, (150, 120, 1150, 560), YEARS, CPI_Y, (1950, 2026), (0, 350), k, GOLD,
                        xticks=range(1950, 2030, 10), yticks=range(0, 351, 50), a=fade(t, 0.1),
                        head_label=(lambda xm: f'{int(xm)}') if k < 1 else None)
    if t > L[1]:
        for yr, label, col, dy, delay in ((1970, '$1.00', MINT, -60, 0.6), (2026, f'${DOLLAR_1970:.2f}', CORAL,
                                                                             70, 3.0)):
            v = ANNUAL[yr] if yr in ANNUAL else LATEST
            kk = pop(t, L[1] + delay)
            if kk > 0:
                c.circle(px(yr), py(v), 9 * kk, col, WHITE, 2)
                bx = min(px(yr), 1080)
                c.rrect(bx - 70, py(v) + dy - 26, bx + 70, py(v) + dy + 26, 14, col, a=clamp(kk))
                c.text(bx, py(v) + dy, label, 28, INK, 900, a=clamp(kk), shadow=False)
                c.text(bx, py(v) + dy + 44, str(yr) if yr < 2026 else 'today', 16, col, 700, a=clamp(kk))
    if t > L[2]:
        k2 = pop(t, L[2] + 0.4)
        c.rrect(200, 150, 520, 230, 18, (255, 255, 255, 25), GOLD, 3, a=clamp(k2))
        c.text(360, 180, f'~{AVG_SINCE_1970:.1f}% a year', 32, GOLD, 900, a=clamp(k2))
        c.text(360, 212, 'average since 1970', 16, MUTED, 600, a=clamp(k2))
    c.text(1150, 600, 'Source: BLS CPI-U via FRED', 14, MUTED, 400, anchor='rm', a=fade(t, 1), shadow=False)


def s_why(c, x):
    t, L = x.t, x.L
    specks(c, t, 4)
    if t < L[1] - 0.2:
        title_card(c, t, 0, 'Why do prices rise?')
        grow = ease(seg(t, L[0] + 2.5, L[0] + 6.5))
        for i in range(int(4 + 14 * grow)):
            c.ellipse(380, 520 - i * 16, 70, 14, GOLD, GOLD_D, 3)
        c.text(380, 580, 'MONEY', 26, GOLD, 900)
        for i in range(4):
            c.rrect(830, 520 - i * 56 - 46, 950, 520 - i * 56 + 8, 8, (180, 140, 100), (120, 90, 60), 3)
        c.text(890, 580, 'STUFF', 26, (210, 170, 130), 900)
        pa = fade(t, L[0] + 2.8)
        price_tag(c, 640, 300 - 120 * grow, 1.2, f'${1 + 1.5 * grow:.2f}', CORAL, a=pa)
        c.icon('arrow-big-up', 640, 400 - 60 * grow, 60, CORAL, a=pa)
    elif t < L[2] - 0.2:
        c.text(640, 80, 'DEMAND-PULL', 44, SKY, 900, a=fade(t, L[1] - 0.2))
        c.text(640, 125, 'everyone spends more than the economy can make', 20, MUTED, 600, a=fade(t, L[1]))
        c.icon('store', 900, 360, 150, WHITE, a=fade(t, L[1]))
        for i in range(3):
            c.rrect(850 + i * 40, 450, 880 + i * 40, 480, 5, (180, 140, 100), (120, 90, 60), 2)
        for i in range(7):
            k = ease(seg(t, L[1] + 0.5 + i * 0.35, L[1] + 2.5 + i * 0.35))
            person(c, lerp(-60, 300 + i * 70, k), 560, 0.7, [SKY, MINT, CORAL, GOLD][i % 4], t, i,
                   'happy', a=clamp(k * 3))
        price_tag(c, 1100, 250 - 40 * ease(seg(t, L[1] + 3, L[1] + 5)), 1.0,
                  f'${3 + 2 * ease(seg(t, L[1] + 3, L[1] + 5)):.2f}', CORAL, a=fade(t, L[1] + 2.5))
    else:
        c.text(640, 80, 'COST-PUSH', 44, CORAL, 900, a=fade(t, L[2] - 0.2))
        c.text(640, 125, 'making things gets more expensive', 20, MUTED, 600, a=fade(t, L[2]))
        steps = [('droplet', 'Oil spikes', 0.15), ('factory', 'Costs rise', 0.4), ('tag', 'You pay more', 0.7)]
        span = x.E[2] - L[2]
        for i, (ic, label, f) in enumerate(steps):
            k = pop(t, L[2] + span * f)
            cx = 280 + i * 360
            c.circle(cx, 360, 90 * k, CORAL_D, CORAL, 3, a=clamp(k))
            c.icon(ic, cx, 360, 80 * k, WHITE, a=clamp(k))
            c.text(cx, 490, label, 26, WHITE, 800, a=clamp(k))
            if i < 2:
                c.icon('arrow-right', cx + 180, 360, 50, MUTED, a=fade(t, L[2] + span * f + 0.3))


def s_spikes(c, x):
    t, L = x.t, x.L
    c.text(640, 60, 'US inflation, % change from a year earlier', 30, WHITE, 800, a=fade(t, 0))
    k = ease(seg(t, L[0] + 0.3, L[0] + 4.5))
    px, py = line_chart(c, (150, 120, 1150, 560), YOY_X, YOY_Y, (1960, 2026.75), (-4, 16), k, SKY,
                        xticks=range(1960, 2030, 10), yticks=range(-4, 17, 4), yfmt='{:.0f}%', a=fade(t, 0.1),
                        width=4)
    c.line([(px(1960), py(2)), (px(2026.75), py(2))], (52, 211, 153, 120), 2, a=fade(t, 0.5))
    c.text(px(1961), py(2) - 14, '2% target', 14, MINT, 700, anchor='lm', a=fade(t, 0.5), shadow=False)
    span = x.E[1] - L[1]
    for when, val, label, f in ((1980.17, 14.6, 'Mar 1980: 14.6%', 0.05), (2022.42, 9.0, 'Jun 2022: ~9%', 0.5)):
        kk = pop(t, L[1] + span * f)
        if kk > 0:
            c.circle(px(when), py(val), 10 * kk, CORAL, WHITE, 2)
            bx = min(px(when), 1045)
            c.rrect(bx - 105, py(val) - 62, bx + 105, py(val) - 22, 14, CORAL, a=clamp(kk))
            c.text(bx, py(val) - 42, label, 20, INK, 800, a=clamp(kk), shadow=False)
    c.text(1150, 600, 'Source: BLS CPI-U via FRED', 14, MUTED, 400, anchor='rm', a=fade(t, 1), shadow=False)


def s_fed(c, x):
    t, L, E = x.t, x.L, x.E
    specks(c, t, 11)
    c.text(640, 80, 'The weapon: interest rates', 40, WHITE, 900, a=fade(t, 0))
    if t < L[1]:
        # big dial with a needle that swings up
        lift = ease(seg(t, L[0] + 2.5, L[0] + 4.5))
        c.arc(640, 430, 200, 180, 360, (255, 255, 255, 50), 26, a=fade(t, 0.3))
        c.arc(640, 430, 200, 180, 180 + 180 * lerp(0.15, 0.85, lift), CORAL, 26, a=fade(t, 0.3))
        ang = math.pi + math.pi * lerp(0.15, 0.85, lift)
        c.line([(640, 430), (640 + 170 * math.cos(ang), 430 + 170 * math.sin(ang))], WHITE, 8, a=fade(t, 0.3))
        c.circle(640, 430, 16, WHITE, a=fade(t, 0.3))
        c.text(640, 490, 'INTEREST RATES', 26, CORAL, 900, a=fade(t, 0.3))
        penny(c, 300, 430, 60, t, 'proud', look=(1, 0), talk=x.talk(), arms=(30, -40) if lift > 0 else (30, 150))
        return
    span = E[1] - L[1]
    steps = [('percent', 'Rates up', CORAL, 'arrow-big-up'), ('banknote', 'Less borrowing', SKY, 'arrow-down'),
             ('shopping-basket', 'Less spending', SKY, 'arrow-down'), ('tag', 'Prices calm', MINT, 'arrow-down')]
    for i, (ic, label, col, arrow) in enumerate(steps):
        k = pop(t, L[1] + span * (0.05 + 0.22 * i))
        cx = 200 + i * 290
        c.circle(cx, 340, 80 * k, (255, 255, 255, 18), col, 4, a=clamp(k))
        c.icon(ic, cx, 340, 70 * k, col, a=clamp(k))
        c.icon(arrow, cx + 58, 280, 34 * k, col, a=clamp(k))
        c.text(cx, 460, label, 24, WHITE, 800, a=clamp(k))
        if i < 3:
            c.icon('arrow-right', cx + 145, 340, 40, MUTED, a=fade(t, L[1] + span * (0.05 + 0.22 * i) + 0.4))


def s_fed_chart(c, x):
    t, L = x.t, x.L
    c.text(640, 60, 'US Federal Reserve key interest rate (Fed funds)', 28, WHITE, 800, a=fade(t, 0))
    k = ease(seg(t, 0.3, L[0] + 3))
    px, py = line_chart(c, (150, 120, 1150, 560), FED_X, FED_Y, (1960, 2026.75), (0, 20), k, CORAL,
                        xticks=range(1960, 2030, 10), yticks=range(0, 21, 5), yfmt='{:.0f}%', a=fade(t, 0.1),
                        width=4)
    kk = pop(t, L[0] + 3)
    if kk > 0:
        c.circle(px(1981.42), py(19.1), 10 * kk, CORAL, WHITE, 2)
        c.rrect(px(1981.42) + 20, py(19.1) - 20, px(1981.42) + 230, py(19.1) + 20, 14, CORAL, a=clamp(kk))
        c.text(px(1981.42) + 125, py(19.1), 'Jun 1981: 19.1%', 20, INK, 800, a=clamp(kk), shadow=False)
    rk = pop(t, L[1] + 2)
    if rk > 0:
        x0, x1 = px(2022.08), px(2023.58)
        c.line([(x0, py(0.08)), (x0, py(7.5)), (x1, py(7.5)), (x1, py(5.33))], GOLD, 3, a=clamp(rk))
        c.rrect(x0 - 300, py(7.5) - 76, x1 + 10, py(7.5) - 22, 14, GOLD, a=clamp(rk))
        c.text((x0 - 300 + x1 + 10) / 2, py(7.5) - 49, '0.08% to 5.33% in 18 months', 20, INK, 800, a=clamp(rk),
               shadow=False)
    c.text(1150, 600, 'Source: Federal Reserve via FRED', 14, MUTED, 400, anchor='rm', a=fade(t, 1), shadow=False)


def s_target(c, x):
    t, L = x.t, x.L
    specks(c, t, 5)
    if t < L[1]:
        k = pop(t, L[0] + 2.5)
        c.circle(640, 320, 140 * k, (255, 255, 255, 18), MINT, 5, a=clamp(k))
        c.text(640, 310, '2%', 110, MINT, 900, a=clamp(k))
        c.text(640, 390, 'the target', 22, MUTED, 600, a=clamp(k))
        penny(c, 300, 400, 56, t, 'shocked' if t < L[0] + 2.4 else 'happy', look=(1, 0), talk=x.talk())
    elif t < L[2]:
        steps = [('hourglass', 'People wait'), ('trending-down', 'Sales drop'), ('user-minus', 'Jobs cut'),
                 ('tag', 'Prices fall')]
        spin = ease(seg(t, L[1] + 2, L[2])) * 0.6
        c.icon('refresh-cw', 640, 360, 120, (255, 255, 255, 60), a=fade(t, L[1]))
        span = x.E[1] - L[1]
        for i, (ic, label) in enumerate(steps):
            ang = -math.pi / 2 + i * math.pi / 2 + spin
            k = pop(t, L[1] + span * (0.3 + 0.15 * i))
            ix, iy = 640 + math.cos(ang) * 230, 360 + math.sin(ang) * 190
            c.circle(ix, iy, 54 * k, CORAL_D, CORAL, 3, a=clamp(k))
            c.icon(ic, ix, iy, 52 * k, WHITE, a=clamp(k))
            c.text(ix, iy + 80, label, 20, WHITE, 700, a=clamp(k))
        c.text(640, 80, 'The deflation spiral', 36, CORAL, 900, a=fade(t, L[1]))
    else:
        penny(c, 640, 380, 80, t, 'happy', wave=True, talk=x.talk())
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
        person(c, cx, 470, k, col, t, li, 'happy' if good else 'sad', a=clamp(k))
        c.icon(ic, cx + 70, 330, 56 * k, col, a=clamp(k))
        c.text(cx, 540, label, 22, WHITE, 800, a=clamp(k))
        c.text(cx, 575, 'WIN' if good else 'LOSE', 28, col, 900, a=fade(t, L[li] + 0.8))
        if li == 1:
            m = ease(seg(t, L[1] + 1, L[1] + 4))
            bill(c, cx - 70, 300, 100 * (1 - 0.45 * m), '100', tint=0.5 * m, a=clamp(k))
        if li == 3:
            g = ease(seg(t, L[3] + 1.2, L[3] + 4))
            c.rrect(cx - 150, 220, cx - 110, 300, 6, SKY, a=clamp(k))
            c.rrect(cx - 100, 300 - 80 * (1 + 0.6 * g), cx - 60, 300, 6, CORAL, a=clamp(k))
            c.text(cx - 130, 315, 'pay', 14, SKY, 700, a=clamp(k), shadow=False)
            c.text(cx - 80, 315, 'prices', 14, CORAL, 700, a=clamp(k), shadow=False)


def s_wages(c, x):
    t, L = x.t, x.L
    if t < L[1] - 0.2:
        specks(c, t, 12)
        penny(c, 640, 360, 80, t, 'happy', talk=x.talk(), look=(0, 0))
        c.icon('briefcase', 800, 270, 70, SKY, a=fade(t, 0.3))
        return
    c.text(640, 60, 'Average hourly pay, US non-manager workers', 28, WHITE, 800, a=fade(t, L[1] - 0.2))
    kn = ease(seg(t, L[1], L[1] + 4))
    kr = ease(seg(t, L[2] + 2.5, L[2] + 6.5))
    px, py = line_chart(c, (150, 120, 1150, 560), WAGE_X, WAGE_Y, (1964, 2026.75), (0, 40), kn, SKY,
                        xticks=range(1970, 2030, 10), yticks=range(0, 41, 10), yfmt='${:.0f}', a=fade(t, L[1]),
                        width=4)
    if kn > 0.98:
        c.text(px(2008), py(WAGE_Y[WAGE_X.index(min(WAGE_X, key=lambda v: abs(v - 2008)))]) + 34, 'on paper', 18, SKY,
               800, a=1 - 0.5 * kr)
    if kr > 0:
        xs = [v for v in REAL_X if v <= lerp(1964, 2026.75, kr)]
        pts = [(px(a), py(b)) for a, b in zip(xs, REAL_Y)]
        if len(pts) > 1:
            c.line(pts, GOLD, 5)
        c.text(px(1966), py(36.5), "in today's dollars", 18, GOLD, 800, anchor='lm', a=fade(t, L[2] + 3))
    bk = pop(t, L[2] + 7)
    if bk > 0 and t < L[3] + 0.5 or (bk > 0 and t >= L[3] + 0.5):
        c.circle(px(1973.5), py(REAL_1973), 9 * bk, GOLD, WHITE, 2)
        c.circle(px(2026.7), py(REAL_Y[-1]), 9 * bk, GOLD, WHITE, 2)
        c.rrect(620, 140, 980, 220, 18, (255, 255, 255, 25), GOLD, 3, a=clamp(bk))
        c.text(800, 170, f'1973: ${REAL_1973:.2f}  ->  now: ${REAL_Y[-1]:.2f}', 22, GOLD, 900, a=clamp(bk))
        c.text(800, 202, f'only +{(REAL_Y[-1] / REAL_1973 - 1) * 100:.0f}% after inflation', 18, WHITE, 700,
               a=clamp(bk))
    c.text(1150, 600, 'Source: BLS (AHETPI, CPI-U) via FRED; excludes benefits', 14, MUTED, 400, anchor='rm',
           a=fade(t, L[1]), shadow=False)


def s_rule70(c, x):
    t, L = x.t, x.L
    specks(c, t, 7)
    k = pop(t, L[0] + 0.5)
    c.rrect(230, 90, 1050, 200, 24, (255, 255, 255, 20), GOLD, 3, a=clamp(k))
    c.text(640, 145, '70 ÷ inflation rate = years to double', 36, GOLD, 900, a=clamp(k))
    span = x.E[1] - L[1]
    for i, (rate, yrs, col, f) in enumerate(((2, 35, MINT, 0.05), (7, 10, CORAL, 0.55))):
        d = L[1] + span * f
        if t < d:
            continue
        y = 330 + i * 140
        g = ease(seg(t, d, d + 1.6))
        c.text(200, y, f'{rate}%', 48, col, 900, a=fade(t, d))
        c.rrect(300, y - 26, 300 + 700 * (yrs / 35) * g, y + 26, 14, col, a=fade(t, d))
        c.text(320 + 700 * (yrs / 35) * g, y, f'{int(round(yrs * g))} years', 30, WHITE, 900, anchor='lm',
               a=fade(t, d))


def s_lesson(c, x):
    t, L = x.t, x.L
    specks(c, t, 8)
    melt = ease(seg(t, L[0] + 1, L[1] + 3))
    for i in range(5):
        y = 420 - i * 22 * (1 - melt * 0.7)
        c.rrect(180 + i * 4, y, 340 + i * 4, y + 20, 6, BILL, BILL_D, 2, a=1 - melt * 0.4)
    c.ellipse(260, 445, 110 * (1 + melt), 14 * (1 + melt), (134, 190, 120, 120))
    c.text(260, 520, 'Cash sitting still', 22, CORAL, 800)
    g = ease(seg(t, L[0] + 2, L[0] + 6))
    c.icon('sprout', 1000, 420 - 60 * g, 80 + 80 * g, MINT)
    c.text(1000, 520, 'Growing with prices', 22, MINT, 800)
    c.icon('trending-up', 640, 360, 70, (255, 255, 255, 120), a=fade(t, L[0] + 2))
    k = pop(t, L[1])
    c.rrect(430, 110, 850, 170, 18, (255, 255, 255, 20), MUTED, 2, a=clamp(k))
    c.text(640, 140, 'Education only - not financial advice', 22, WHITE, 700, a=clamp(k))


def s_outro(c, x):
    """Leaves the right side clear for YouTube end-screen elements (video + subscribe)."""
    t, L = x.t, x.L
    specks(c, t, 9, 50)
    penny(c, 260, 380, 76, t, 'happy', look=(1, 0), talk=x.talk(), wave=t > x.E[-1])
    bill(c, 260, 200, 140, '100', tint=0.3, a=fade(t, 0.2))
    if t > L[1]:
        k = ease_out(seg(t, L[1], L[1] + 0.6))
        c.text(400, 560, 'COIN THEORY', 30, GOLD, 900, anchor='lm', a=k)
        c.text(400, 595, 'money, explained with real data', 18, MUTED, 600, anchor='lm', a=k)
    if t > x.E[-1]:
        k = fade(t, x.E[-1], 0.8)
        for bx, by, bw, bh in ((560, 150, 640, 360), ):
            c.rrect(bx, by, bx + bw, by + bh, 20, (255, 255, 255, 10), (255, 255, 255, 40), 2, a=k)


SCENES = [
    dict(draw=s_hook, chapter='Intro: the mattress experiment', cam=(1.0, 1.06), focus=(0.45, 0.55), lines=[
        "Imagine it's 1970, and you hide a {$100 bill|hundred-dollar bill} under your mattress.",
        "You forget about it for 56 years, and find it again today.",
        "It's still {$100.|a hundred dollars.} But now it only buys about as much as $12 did back then.",
        "So where did the other $88 go?",
    ], sfx=lambda L: [(L[0] + 1.6, 'whoosh'), (L[1] + 2.0, 'whoosh'), (L[2] + 1.4, 'down'), (L[2] + 2.2, 'pop'),
                      (L[3] + 0.2, 'whoosh')]),
    dict(draw=s_title, lines=[], min=3.2, captions=False, cam=(1.0, 1.03), trans='fadeblack',
         sfx=lambda L: [(0.2, 'ding')]),
    dict(draw=s_basket, chapter='What inflation is', trans='fadeblack', lines=[
        "The answer is inflation: the slow, steady rise of prices across the whole economy.",
        "To measure it, the government tracks a huge basket of things people buy: food, rent, fuel, clothes, "
        "transport, and doctor visits.",
        "Every month, it records the prices of about 80,000 items, in thousands of stores, rental homes, and "
        "doctors' offices.",
        "Put it all together, and you get one number: the Consumer Price Index.",
    ], sfx=lambda L: [(L[0], 'pop'), (L[2] + 0.3, 'pop'), (L[3] + 1.4, 'ding')]),
    dict(draw=s_prices, chapter='Everyday prices, 1980 vs today', lines=[
        "Let's make that real. Here's what some everyday things cost in 1980, according to government price "
        "surveys, and what they cost now.",
        "A pound of white bread went from 51 cents to $1.83. A dozen eggs, from 84 cents to $2.27. "
        "A pound of coffee, from $3.14 to $9.33. And a gallon of gas, from $1.25 to $4.48.",
        "Different things rise at different speeds. But the direction is almost always the same: up.",
    ], sfx=lambda L: [(L[0] + 1.2 + i * 0.25, 'pop') for i in range(4)]),
    dict(draw=s_cpi_chart, chapter='70 years of prices', cam=(1.0, 1.05), focus=(0.7, 0.4), lines=[
        "Here's the full index for the United States since 1950. Notice something? It almost never goes down.",
        "Something that cost $1 in 1970 costs about $8.66 today.",
        "That's prices rising by almost 4% a year, on average, for more than half a century.",
    ], sfx=lambda L: [(L[1] + 0.6, 'pop'), (L[1] + 3.0, 'ding'), (L[2] + 0.4, 'pop')]),
    dict(draw=s_why, chapter='Why prices rise', lines=[
        "So why do prices keep climbing? The simplest answer: when more money chases the same amount of stuff, "
        "prices go up.",
        "Economists call one version demand-pull inflation. People, businesses, and governments try to spend "
        "more than the economy can produce, often when borrowing is cheap, so sellers raise prices.",
        "The other is cost-push inflation. When oil spikes or factories shut down, it costs more to make things, "
        "and those costs get passed on to you.",
    ], sfx=lambda L: [(L[1], 'whoosh'), (L[2], 'whoosh')]),
    dict(draw=s_spikes, chapter='When inflation explodes', cam=(1.0, 1.04), lines=[
        "Most of the time, inflation is slow and quiet. But sometimes, it explodes.",
        "In March 1980, prices were rising almost 15% a year. And in June 2022, after the pandemic, inflation "
        "hit about 9%, the highest in four decades.",
    ], sfx=lambda L: [(L[1] + 0.3, 'pop'), (L[1] + 4.0, 'pop')]),
    dict(draw=s_fed, chapter='How the Fed fights back', lines=[
        "When inflation gets out of hand, central banks fight back with one main weapon: interest rates.",
        "Higher rates make borrowing more expensive. People and businesses borrow less and spend less, demand "
        "cools down, and prices calm down with it.",
    ], sfx=lambda L: [(L[0] + 2.5, 'whoosh')]),
    dict(draw=s_fed_chart, cam=(1.0, 1.04), lines=[
        "In 1981, to crush double-digit inflation, the Federal Reserve pushed its key interest rate to about 19%. "
        "It worked, but it also helped trigger a painful recession.",
        "In 2022, it raised rates from almost zero to over 5% in about a year and a half, the fastest climb in "
        "four decades.",
    ], sfx=lambda L: [(L[0] + 3, 'pop'), (L[1] + 2, 'pop')]),
    dict(draw=s_target, chapter='Why not zero inflation?', lines=[
        "So shouldn't the goal be zero inflation? Surprisingly, no. The US Federal Reserve aims for about 2%.",
        "Because falling prices can be even worse. If you expect things to be cheaper next month, you wait. "
        "Businesses sell less, cut jobs, and prices fall even further.",
        "A little inflation keeps money moving.",
    ], sfx=lambda L: [(L[0] + 2.5, 'ding')]),
    dict(draw=s_winners, chapter='Winners and losers', lines=[
        "But inflation doesn't treat everyone the same.",
        "If you keep your savings in cash, you lose. Your money quietly buys less every single year.",
        "If you owe money at a fixed interest rate, you can actually win, because you pay it back with dollars "
        "that are worth less.",
        "And if your pay rises slower than prices, you're getting a pay cut, even if your salary never changes.",
    ], sfx=lambda L: [(L[1], 'pop'), (L[1] + 1, 'down'), (L[2], 'pop'), (L[3], 'pop')]),
    dict(draw=s_wages, chapter='Your pay vs prices', cam=(1.0, 1.04), lines=[
        "And that last one matters more than you might think.",
        "In 1970, a typical non-manager worker in America earned about $3.40 an hour. Today, it's about $32.60. "
        "That looks like a massive raise.",
        "But adjust for inflation, and the picture changes. In today's dollars, that worker's hourly pay is only "
        "about 4% higher than it was in 1973.",
        "Most of the raise was eaten by rising prices. This doesn't count benefits like health insurance, but "
        "the lesson stands: what matters isn't how much you earn. It's what your pay can buy.",
    ], sfx=lambda L: [(L[2] + 2.5, 'whoosh'), (L[2] + 7, 'ding')]),
    dict(draw=s_rule70, chapter='The rule of 70', lines=[
        "Here's a handy trick. Divide 70 by the inflation rate, and you get roughly how many years it takes for "
        "prices to double.",
        "At 2%, prices double in about 35 years. At 7%, in just 10.",
    ], sfx=lambda L: [(L[0] + 0.5, 'ding')]),
    dict(draw=s_lesson, chapter='The lesson', lines=[
        "That's why many people don't leave long-term savings sitting in cash. They look for places where money "
        "can grow at least as fast as prices, knowing that every option comes with its own risks.",
        "This channel isn't financial advice. But the lesson is simple: money that sits still slowly melts.",
    ]),
    dict(draw=s_outro, chapter='Where your $100 went', tail=12, cam=(1.0, 1.02), lines=[
        "So, where did your {$100|hundred dollars} go? Nowhere. It just shrank, a few cents at a time.",
        "If this changed how you see your money, subscribe to Coin Theory. Next time: why houses got so "
        "expensive.",
    ], sfx=lambda L: [(L[1], 'pop')]),
]


def end_card(line):
    def draw(c, x):
        specks(c, x.t, 13, 50)
        penny(c, 640, 330, 90, x.t, 'happy', wave=True, talk=x.talk())
        c.text(640, 560, 'Full story on Coin Theory', 40, GOLD, 900, a=fade(x.t, 0.3))
    return dict(draw=draw, lines=[line], tail=0.8)


SHORTS = {
    'ep01_short_prices': [dict(SCENES[0], tail=0.3), dict(SCENES[3], tail=0.3), end_card(
        "Where does the rest of your money go? Watch the full story on Coin Theory.")],
    'ep01_short_wages': [dict(SCENES[11], lines=[
        "Your boss gives you a raise every year. So why don't you feel richer?"] + SCENES[11]['lines'][1:]),
        end_card("Find out where that money went. Full story on Coin Theory.")],
    'ep01_short_rule70': [dict(SCENES[12], lines=[
        "Want to know how fast your money loses value? Use the rule of 70."] + SCENES[12]['lines'][1:] + [
        "So if inflation runs at 4%, your money buys half as much in about 17 and a half years."]),
        end_card("See where your money really goes. Full story on Coin Theory.")],
}


def check_numbers():
    """Refuse to render if a number in the narration no longer matches the data."""
    script = ' '.join(l for sc in SCENES for l in sc['lines'])
    want = [f'${round(100 * ANNUAL[1970] / LATEST)}', f'${100 - round(100 * ANNUAL[1970] / LATEST)}',
            f'${DOLLAR_1970:.2f}', f'{WAGE_1970:.2f}', f'${WAGE.iloc[-1]:.2f}',
            f'about {round((REAL_Y[-1] / REAL_1973 - 1) * 100)}% higher']
    want += [money(p0) for *_r, p0, p1 in PRICES] + [money(p1) for *_r, p0, p1 in PRICES]
    assert AVG_SINCE_1970 < 4 and 'almost 4%' in script, AVG_SINCE_1970
    assert 14.5 <= YOY['1980-03'].iloc[0] < 15 and 'almost 15%' in script
    assert round(YOY['2022-06'].iloc[0]) == 9 and 'about 9%' in script
    assert round(FED.max()) == 19 and FED.idxmax().year == 1981
    missing = [w for w in want if w not in script]
    assert not missing, f'narration out of date with data: {missing}'
    print('numbers check: OK')


def fmt(sec):
    return f'{int(sec // 60)}:{int(sec % 60):02d}'


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    check_numbers()
    if '--stills' in sys.argv:
        os.makedirs(BUILD, exist_ok=True)
        for i, sc in enumerate(SCENES):
            n = max(1, len(sc['lines']))
            still(sc, 0.5 + 4 * n - 0.5, os.path.join(BUILD, f'still_{i:02d}.png'))
        sys.exit()
    if '--shorts-only' not in sys.argv:
        total, chapters = build(SCENES, os.path.join(OUT, 'ep01_inflation.mp4'), BUILD,
                                srt_path=os.path.join(OUT, 'ep01_inflation.en.srt'))
        with open(os.path.join(OUT, 'ep01_chapters.txt'), 'w') as f:
            for at, name in chapters:
                f.write(f'{fmt(at)} {name}\n')
        print(open(os.path.join(OUT, 'ep01_chapters.txt')).read())
    if '--no-short' not in sys.argv:
        for name, scenes in SHORTS.items():
            if os.path.exists(os.path.join(OUT, f'{name}.mp4')) and '--force-shorts' not in sys.argv:
                continue
            build(scenes, os.path.join(OUT, f'{name}.mp4'), os.path.join(BUILD, name), layout='short')
