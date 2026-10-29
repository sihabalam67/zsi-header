#!/usr/bin/env python3
"""Coin Theory, episode 2: Why houses got so expensive.

Data (FRED): MSPUS (median sales price of new houses sold, Census/HUD), MEHOINUSA646N (median household
income, Census), MORTGAGE30US (Freddie Mac 30-year rate), HOUST (housing starts, Census), CPIAUCSL (BLS).
check_numbers() refuses to render if the narration disagrees with the data.

    python3 channel/ep02_housing.py [--stills] [--no-short]
"""
import math
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import *  # noqa: E402,F401,F403

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
BUILD = os.path.join(HERE, 'build', 'ep02')


def series(name):
    d = pd.read_csv(os.path.join(HERE, 'data', f'{name}.csv'))
    d.columns = ['date', 'v']
    d['date'] = pd.to_datetime(d['date'])
    d['v'] = pd.to_numeric(d['v'], errors='coerce')
    return d.dropna().set_index('date')['v']


PRICE = series('MSPUS')
INCOME = series('MEHOINUSA646N')
RATE = series('MORTGAGE30US')
STARTS = series('HOUST')
CPI = series('CPIAUCSL')
PA = PRICE.groupby(PRICE.index.year).mean()
IA = INCOME.groupby(INCOME.index.year).mean()
RA = RATE.groupby(RATE.index.year).mean()
CA = CPI.groupby(CPI.index.year).mean()
SA = STARTS.groupby(STARTS.index.year).mean()

P1970, P_NOW = PA[1970], PRICE.iloc[-1]
P1970_REAL = P1970 * CPI.iloc[-1] / CA[1970]
RATIO_YEARS = [y for y in IA.index if y in PA.index]
RATIO = [PA[y] / IA[y] for y in RATIO_YEARS]
R1984, R2022, R_LAST = PA[1984] / IA[1984], PA[2022] / IA[2022], RATIO[-1]
DECADES = [(d, SA.loc[d:d + 9].mean()) for d in range(1960, 2030, 10)]
RATE_X = [d.year + d.dayofyear / 366 for d in RATE.index]
RATE_Y = list(RATE.values)


def payment(price, rate, down=0.2, years=30):
    loan, r, n = price * (1 - down), rate / 100 / 12, years * 12
    return loan * r / (1 - (1 + r) ** -n)


PAY_2021 = payment(PA[2021], RA[2021])
PAY_NOW = payment(P_NOW, RATE.iloc[-1])
SHARE_2021 = PAY_2021 / (IA[2021] / 12) * 100
SHARE_NOW = PAY_NOW / (IA[IA.index.max()] / 12) * 100
SHARE_1984 = payment(PA[1984], RA[1984]) / (IA[1984] / 12) * 100


def thousands(v):
    return f'${round(v, -3):,.0f}'


# ----------------------------------------------------------------- drawing --
def house(c, x, y, s, body=CREAM, roof=CORAL, a=1.0, lit=0.0):
    """Original cartoon house; (x, y) is the middle of the ground line."""
    w, h = 160 * s, 110 * s
    c.rrect(x - w / 2, y - h, x + w / 2, y, 8 * s, body, mix(body, INK, 0.3), 3 * s, a)
    c.poly([(x - w / 2 - 18 * s, y - h + 4 * s), (x, y - h - 80 * s), (x + w / 2 + 18 * s, y - h + 4 * s)],
           roof, mix(roof, INK, 0.35), 3 * s, a)
    c.rrect(x - 18 * s, y - 60 * s, x + 18 * s, y, 5 * s, mix(roof, INK, 0.3), a=a)
    win = mix((120, 170, 220), (255, 220, 120), lit)
    for wx in (-48, 48):
        c.rrect(x + wx * s - 18 * s, y - 88 * s, x + wx * s + 18 * s, y - 56 * s, 4 * s, win,
                mix(body, INK, 0.3), 2 * s, a)


def bar_chart(c, box, labels, values, vmax, k, color, a=1.0, fmt='{:.0f}', highlight=None, hcolor=CORAL):
    x0, y0, x1, y1 = box
    n = len(values)
    bw = (x1 - x0) / n
    c.line([(x0, y1), (x1, y1)], (255, 255, 255, 90), 2, a)
    for i, (lab, v) in enumerate(zip(labels, values)):
        g = ease(seg(k, i / n * 0.6, i / n * 0.6 + 0.4))
        bx = x0 + i * bw + bw * 0.18
        top = y1 - (y1 - y0) * v / vmax * g
        col = hcolor if i == highlight else color
        c.rrect(bx, top, bx + bw * 0.64, y1, 8, col, a=a)
        c.text(bx + bw * 0.32, y1 + 22, lab, 16, MUTED, 700, a=a, shadow=False)
        if g > 0.9:
            c.text(bx + bw * 0.32, top - 18, fmt.format(v), 18, WHITE, 800, a=a * fade(g, 0.9, 0.1))


# ------------------------------------------------------------------ scenes --
def s_hook(c, x):
    t, L = x.t, x.L
    specks(c, t, 21)
    g = ease(seg(t, L[1], L[1] + 1.4))
    house(c, 640, 520, lerp(0.8, 1.6, g), lit=g)
    c.ellipse(640, 528, 330, 16, (0, 0, 0, 60))
    price = lerp(P1970, P_NOW, ease(seg(t, L[1], L[1] + 1.4)))
    tk = pop(t, L[0] + 1.0)
    if tk > 0:
        col = mix(MINT, CORAL, g)
        c.rrect(840, 160, 1180, 260, 20, col, a=clamp(tk))
        c.text(1010, 196, '1970' if g < 0.5 else 'today', 20, INK, 800, a=clamp(tk), shadow=False)
        c.text(1010, 232, f'${price:,.0f}', 40, INK, 900, a=clamp(tk), shadow=False)
    if t > L[2] + 1.2:
        k = pop(t, L[2] + 1.2)
        c.rrect(100, 140, 440, 240, 18, (255, 255, 255, 20), GOLD, 3, a=clamp(k))
        c.text(270, 178, f'x{P_NOW / P1970_REAL:.1f}', 40, GOLD, 900, a=clamp(k))
        c.text(270, 218, 'even after inflation', 16, MUTED, 600, a=clamp(k))
    mood = 'happy' if t < L[1] + 1.4 else 'shocked'
    penny(c, 230, 470, 56, t, mood, look=(1, 0), talk=x.talk())


def s_title(c, x):
    t = x.t
    specks(c, t, 22, 60)
    k = ease_out(seg(t, 0.1, 0.7))
    c.text(640, 280 - 20 * (1 - k), 'WHY HOUSES GOT', 64, WHITE, 900, a=k)
    c.text(640, 370 - 20 * (1 - k), 'SO EXPENSIVE', 96, GOLD, 900, a=k)
    house(c, 640, 600, 0.7, a=fade(t, 0.4))
    c.text(640, 660, 'COIN THEORY', 22, MUTED, 800, a=fade(t, 0.8))


def s_ratio(c, x):
    t, L = x.t, x.L
    if t < L[1] - 0.2:
        specks(c, t, 23)
        house(c, 420, 470, 1.0)
        c.text(420, 540, 'home price', 22, CREAM, 800, a=fade(t, 1))
        c.text(640, 380, '÷', 70, MUTED, 900, a=fade(t, 1.5))
        c.icon('briefcase', 860, 400, 110, SKY, a=fade(t, 2))
        c.text(860, 540, 'yearly income', 22, SKY, 800, a=fade(t, 2))
        c.text(640, 120, 'Years of income to buy a home', 36, WHITE, 900, a=fade(t, 0.3))
        return
    c.text(640, 60, 'Median new-home price ÷ median household income', 28, WHITE, 800, a=fade(t, L[1] - 0.2))
    k = ease(seg(t, L[1], L[2] + 2))
    px, py = line_chart(c, (150, 120, 1150, 560), RATIO_YEARS, RATIO, (1984, RATIO_YEARS[-1]), (0, 7), k, GOLD,
                        xticks=range(1985, 2030, 5), yticks=range(0, 8), yfmt='{:.0f}x', a=fade(t, L[1]))
    for yr, r, label, col, at in ((1984, R1984, f'1984: {R1984:.1f}x', MINT, L[1] + 1),
                                  (2022, R2022, f'2022: {R2022:.1f}x', CORAL, L[2] + 0.5),
                                  (RATIO_YEARS[-1], R_LAST, f'{RATIO_YEARS[-1]}: {R_LAST:.1f}x', GOLD, L[2] + 3.5)):
        kk = pop(t, at)
        if kk > 0:
            c.circle(px(yr), py(r), 9 * kk, col, WHITE, 2)
            bx = min(max(px(yr), 230), 1060)
            c.rrect(bx - 85, py(r) - 62, bx + 85, py(r) - 24, 14, col, a=clamp(kk))
            c.text(bx, py(r) - 43, label, 20, INK, 800, a=clamp(kk), shadow=False)
    c.text(1150, 600, 'Source: Census/HUD (MSPUS), Census (household income) via FRED', 14, MUTED, 400,
           anchor='rm', a=fade(t, 1), shadow=False)


def s_supply(c, x):
    t, L = x.t, x.L
    c.text(640, 60, 'New homes started per year, average by decade', 30, WHITE, 800, a=fade(t, 0))
    k = seg(t, L[0] + 0.5, L[1] + 3)
    bar_chart(c, (170, 140, 1110, 540), [f"{d}s" for d, _ in DECADES], [v / 1000 for _, v in DECADES], 2.0, k, SKY,
              fmt='{:.2f}M', highlight=5 if t > L[1] + 4 else None)
    if t > L[2]:
        k2 = pop(t, L[2] + 0.3)
        c.rrect(860, 110, 1170, 190, 18, (255, 255, 255, 22), CORAL, 3, a=clamp(k2))
        c.text(1015, 138, 'fewer homes', 22, CORAL, 900, a=clamp(k2))
        c.text(1015, 168, '+ more people', 22, CORAL, 900, a=clamp(k2))
    c.text(1150, 600, 'Source: Census housing starts (HOUST) via FRED', 14, MUTED, 400, anchor='rm',
           a=fade(t, 1), shadow=False)


def s_rules(c, x):
    t, L = x.t, x.L
    specks(c, t, 24)
    c.text(640, 80, 'Why not just build more?', 40, WHITE, 900, a=fade(t, 0))
    if t < L[1]:
        house(c, 640, 520, 1.2, a=fade(t, 0.3))
        stop_k = pop(t, L[0] + 2)
        if stop_k > 0:
            c.circle(820, 300, 50 * stop_k, CORAL, WHITE, 4)
            c.text(820, 302, 'NO', 30, WHITE, 900, a=clamp(stop_k), shadow=False)
        penny(c, 300, 450, 56, t, 'worried' if t > L[0] + 2 else 'happy', look=(1, 0), talk=x.talk())
        return
    span = x.E[1] - L[1]
    items = [('house', 'Single-family only'), ('ruler', 'Big minimum lots'), ('file-text', 'Slow permits'),
             ('map-pin', 'Scarce land near jobs')]
    for i, (ic, label) in enumerate(items):
        k = pop(t, L[1] + span * (0.05 + 0.2 * i))
        cx = 200 + i * 290
        c.circle(cx, 340, 80 * k, (255, 255, 255, 18), GOLD, 3, a=clamp(k))
        c.icon(ic, cx, 340, 70 * k, GOLD, a=clamp(k))
        c.text(cx, 460, label, 22, WHITE, 800, a=clamp(k))


def s_rates(c, x):
    t, L = x.t, x.L
    c.text(640, 60, '30-year US mortgage rate', 30, WHITE, 800, a=fade(t, 0))
    k = ease(seg(t, L[0] + 0.5, L[1] + 4))
    px, py = line_chart(c, (150, 120, 1150, 560), RATE_X, RATE_Y, (1971.3, RATE_X[-1]), (0, 20), k, CORAL,
                        xticks=range(1975, 2030, 10), yticks=range(0, 21, 5), yfmt='{:.0f}%', a=fade(t, 0.1),
                        width=3)
    hi_x = RATE_X[RATE_Y.index(max(RATE_Y))]
    lo_x = RATE_X[RATE_Y.index(min(RATE_Y))]
    for xx, v, label, at in ((hi_x, max(RATE_Y), f'1981: {max(RATE_Y):.1f}%', L[1] + 0.8),
                             (lo_x, min(RATE_Y), f'Jan 2021: {min(RATE_Y):.2f}%', L[1] + 4)):
        kk = pop(t, at)
        if kk > 0:
            c.circle(px(xx), py(v), 9 * kk, GOLD, WHITE, 2)
            bx = min(max(px(xx) + 110, 260), 1040)
            c.rrect(bx - 100, py(v) - 64 if v > 10 else py(v) - 80, bx + 100,
                    py(v) - 26 if v > 10 else py(v) - 42, 14, GOLD, a=clamp(kk))
            c.text(bx, py(v) - 45 if v > 10 else py(v) - 61, label, 20, INK, 800, a=clamp(kk), shadow=False)
    if t > L[2]:
        k2 = pop(t, L[2] + 0.3)
        c.rrect(760, 140, 1130, 220, 18, (255, 255, 255, 22), MINT, 3, a=clamp(k2))
        c.text(945, 168, 'cheaper loans', 22, MINT, 900, a=clamp(k2))
        c.text(945, 198, '= bigger bids', 22, MINT, 900, a=clamp(k2))
    c.text(1150, 600, 'Source: Freddie Mac (MORTGAGE30US) via FRED', 14, MUTED, 400, anchor='rm', a=fade(t, 1),
           shadow=False)


def s_payment(c, x):
    t, L = x.t, x.L
    specks(c, t, 25)
    c.text(640, 70, 'Monthly payment on the median new home (20% down)', 30, WHITE, 900, a=fade(t, 0))
    if t < L[1]:
        g = ease(seg(t, L[0] + 0.5, L[0] + 2.5))
        c.text(640, 330, f'{lerp(min(RATE_Y), RATE_Y[-1], g):.2f}%', 120, CORAL, 900, a=fade(t, 0.3))
        c.text(640, 420, '30-year mortgage rate today', 22, MUTED, 600, a=fade(t, 0.3))
        return
    span = x.E[1] - L[1]
    for i, (label, pay, share, col, f) in enumerate((('2021', PAY_2021, SHARE_2021, MINT, 0.2),
                                                     ('today', PAY_NOW, SHARE_NOW, CORAL, 0.55))):
        g = ease(seg(t, L[1] + span * f, L[1] + span * f + 1.2))
        bx = 380 + i * 520
        top = 560 - 340 * (pay / 2400) * g
        c.rrect(bx - 90, top, bx + 90, 560, 14, col, a=fade(t, L[1] + span * f))
        c.text(bx, top - 30, f'${pay * g:,.0f}', 40, col, 900, a=fade(t, L[1] + span * f))
        c.text(bx, 590, label, 24, WHITE, 800, a=fade(t, L[1] + span * f))
        if t > L[2]:
            k = pop(t, L[2] + 0.5 + i * 1.5)
            c.rrect(bx - 120, 160, bx + 120, 220, 16, (255, 255, 255, 22), col, 3, a=clamp(k))
            c.text(bx, 190, f'{share:.0f}% of income', 24, col, 900, a=clamp(k))


def s_1984(c, x):
    t, L = x.t, x.L
    specks(c, t, 26)
    for i, (yr, home, loan, col_h, col_l) in enumerate((('1984', 'cheap', 'expensive', MINT, CORAL),
                                                       ('today', 'expensive', 'expensive', CORAL, CORAL))):
        at = 0.3 if i == 0 else L[1]
        k = pop(t, at)
        if k <= 0:
            continue
        cx = 360 + i * 560
        c.rrect(cx - 220, 150, cx + 220, 520, 24, (255, 255, 255, 16), (255, 255, 255, 50), 2, a=clamp(k))
        c.text(cx, 200, yr, 44, GOLD, 900, a=clamp(k))
        house(c, cx - 90, 380, 0.6, a=clamp(k))
        c.text(cx - 90, 420, 'homes', 18, MUTED, 700, a=clamp(k))
        c.text(cx - 90, 455, home, 26, col_h, 900, a=clamp(k))
        c.icon('percent', cx + 100, 310, 70, WHITE, a=clamp(k))
        c.text(cx + 100, 420, 'loans', 18, MUTED, 700, a=clamp(k))
        c.text(cx + 100, 455, loan, 26, col_l, 900, a=clamp(k))
        if i == 0:
            c.text(cx, 495, f'payments: ~{SHARE_1984:.0f}% of income', 18, WHITE, 700, a=fade(t, L[0] + 3))


def s_split(c, x):
    t, L = x.t, x.L
    specks(c, t, 27)
    k1 = pop(t, L[0] + 0.5)
    house(c, 330, 470, 1.0 * k1, lit=1, a=clamp(k1))
    person(c, 470, 520, 0.9 * k1, MINT, t, 1, 'happy', a=clamp(k1))
    c.icon('trending-up', 330, 220, 70 * k1, MINT, a=clamp(k1))
    c.text(400, 590, 'Owners who bought early', 22, MINT, 800, a=clamp(k1))
    k2 = pop(t, L[1])
    if k2 > 0:
        person(c, 900, 520, 0.9 * k2, CORAL, t, 2, 'sad', a=clamp(k2))
        house(c, 1060, 470, 0.7 * k2, roof=(120, 120, 140), a=clamp(k2) * 0.6)
        c.icon('lock', 1060, 330, 50 * k2, CORAL, a=clamp(k2))
        c.text(960, 590, 'First-time buyers', 22, CORAL, 800, a=clamp(k2))


def s_fix(c, x):
    t, L = x.t, x.L
    specks(c, t, 28)
    n = int(1 + 9 * ease(seg(t, L[0] + 1.5, L[1] + 2)))
    for i in range(n):
        house(c, 170 + (i % 5) * 235, 340 + (i // 5) * 190, 0.55, roof=[CORAL, SKY, MINT, GOLD][i % 4], lit=0.6)
    c.text(640, 80, 'Build more homes where people want to live', 34, WHITE, 900, a=fade(t, 0.3))
    if t > L[1]:
        k = pop(t, L[1] + 0.5)
        c.rrect(410, 600, 870, 650, 16, (255, 255, 255, 22), MUTED, 2, a=clamp(k))
        c.text(640, 625, 'Education only - not financial advice', 20, WHITE, 700, a=clamp(k))


def s_outro(c, x):
    t, L = x.t, x.L
    specks(c, t, 29, 50)
    penny(c, 260, 380, 76, t, 'happy', look=(1, 0), talk=x.talk(), wave=t > x.E[-1])
    house(c, 260, 220, 0.5, a=fade(t, 0.2))
    if t > L[1]:
        k = ease_out(seg(t, L[1], L[1] + 0.6))
        c.text(400, 560, 'COIN THEORY', 30, GOLD, 900, anchor='lm', a=k)
        c.text(400, 595, 'money, explained with real data', 18, MUTED, 600, anchor='lm', a=k)
    if t > x.E[-1]:
        c.rrect(560, 150, 1200, 510, 20, (255, 255, 255, 10), (255, 255, 255, 40), 2, a=fade(t, x.E[-1], 0.8))


SCENES = [
    dict(draw=s_hook, chapter='Intro: $23,000 to $393,000', cam=(1.0, 1.05), lines=[
        f"In 1970, the typical new home in America sold for about {thousands(P1970)}.",
        f"Today? About {thousands(P_NOW)}.",
        "Even after adjusting for inflation, that's almost twice as expensive. So what happened to houses?",
    ], sfx=lambda L: [(L[0] + 1.0, 'pop'), (L[1], 'whoosh'), (L[2] + 1.2, 'ding')]),
    dict(draw=s_title, lines=[], min=3.2, captions=False, trans='fadeblack', sfx=lambda L: [(0.2, 'ding')]),
    dict(draw=s_ratio, chapter='Years of income per home', trans='fadeblack', lines=[
        "The best way to measure it isn't the price tag. It's how many years of income a home costs.",
        f"In 1984, the typical new home cost about {R1984:.1f} times the typical household's yearly income.",
        f"By 2022, it was almost {math.ceil(R2022)} times. Today, it's still around {R_LAST:.1f} times.",
    ], sfx=lambda L: [(L[1] + 1, 'pop'), (L[2] + 0.5, 'pop'), (L[2] + 3.5, 'pop')]),
    dict(draw=s_supply, chapter='Reason 1: we stopped building', cam=(1.0, 1.04), lines=[
        "Reason number one is simple: America stopped building enough homes.",
        f"In the 1970s, builders started about {DECADES[1][1] / 1000:.2f} million homes a year. After the 2008 "
        "crash, that collapsed, and the 2010s averaged under 1 million a year, the lowest of any decade since "
        "records began in 1959.",
        "Meanwhile, the population kept growing. Fewer new homes, more people, higher prices.",
    ], sfx=lambda L: [(L[1] + 4, 'down'), (L[2] + 0.3, 'pop')]),
    dict(draw=s_rules, chapter='Reason 2: the rules', lines=[
        "So why didn't builders just build more? In many places, they're not allowed to.",
        "Local zoning rules often ban anything except single-family houses, require big lots, and add slow "
        "permit processes. Land near good jobs is scarce, and every extra rule adds cost.",
    ], sfx=lambda L: [(L[0] + 2, 'down')]),
    dict(draw=s_rates, chapter='Reason 3: the price of money', cam=(1.0, 1.04), lines=[
        "Reason number three is the price of money.",
        f"In 1981, the 30-year mortgage rate peaked near {max(RATE_Y):.1f}%. Over the next forty years, rates "
        f"kept falling, all the way to {min(RATE_Y):.2f}% in January 2021.",
        "Cheaper loans let buyers borrow more, so they could bid prices higher.",
    ], sfx=lambda L: [(L[1] + 0.8, 'pop'), (L[1] + 4, 'pop'), (L[2] + 0.3, 'ding')]),
    dict(draw=s_payment, chapter='The payment shock', lines=[
        f"Then rates jumped back up. Today they're around {RATE_Y[-1]:.1f}%.",
        f"On the typical new home, with 20% down, the monthly payment went from about ${PAY_2021:,.0f} in 2021 "
        f"to about ${PAY_NOW:,.0f} today.",
        f"That's a jump from about {SHARE_2021:.0f}% to about {SHARE_NOW:.0f}% of a typical household's income.",
    ], sfx=lambda L: [(L[1] + 1, 'pop'), (L[1] + 4, 'pop'), (L[2] + 0.5, 'ding')]),
    dict(draw=s_1984, chapter='Was it easier before?', lines=[
        f"To be fair, buying was never easy. In 1984, with rates near {round(RA[1984])}%, payments took an even "
        f"bigger bite, about {SHARE_1984:.0f}% of income.",
        "The difference is that back then, homes were cheap and loans were expensive. Today, homes are "
        "expensive, and loans are expensive too.",
    ], sfx=lambda L: [(L[1], 'whoosh')]),
    dict(draw=s_split, chapter='Who wins, who loses', lines=[
        "This has split the country in two. People who bought years ago watched their home's value soar.",
        "People trying to buy their first home face high prices and high rates at the same time.",
    ], sfx=lambda L: [(L[0] + 0.5, 'pop'), (L[1], 'down')]),
    dict(draw=s_fix, chapter='What would help', lines=[
        "So what would actually help? Many economists argue the long-term answer is simple: build a lot more "
        "homes, especially near jobs.",
        "Some cities are already loosening zoning to allow apartments, townhouses, and backyard homes. Where "
        "supply grows faster, prices tend to rise more slowly.",
    ]),
    dict(draw=s_outro, chapter='Recap', tail=12, cam=(1.0, 1.02), lines=[
        "So houses didn't get expensive by accident. Too few homes, strict rules, and the price of money all "
        "pushed in the same direction.",
        "Next time: how banks create money out of thin air. Subscribe to Coin Theory so you don't miss it.",
    ], sfx=lambda L: [(L[1], 'pop')]),
]


def end_card(line):
    def draw(c, x):
        specks(c, x.t, 30, 50)
        penny(c, 640, 330, 90, x.t, 'happy', wave=True, talk=x.talk())
        c.text(640, 560, 'Full story on Coin Theory', 40, GOLD, 900, a=fade(x.t, 0.3))
    return dict(draw=draw, lines=[line], tail=1.2)


SHORTS = {
    'ep02_short_price': [SCENES[0], SCENES[2], end_card("Want to know why? Watch the full story on Coin Theory.")],
    'ep02_short_payment': [SCENES[6], end_card("Here's why houses got this expensive. Full story on Coin Theory.")],
    'ep02_short_supply': [SCENES[3], SCENES[4], end_card("There's a third reason too. Watch the full story on Coin "
                                                         "Theory.")],
}


def check_numbers():
    script = ' '.join(l for sc in SCENES for l in sc['lines'])
    assert 1.85 <= P_NOW / P1970_REAL < 2.0 and 'almost twice' in script, P_NOW / P1970_REAL
    assert 5.5 <= R2022 < 6 and 'almost 6 times' in script, R2022
    assert DECADES[5][0] == 2010 and DECADES[5][1] < 1000 and DECADES[5][1] == min(v for _, v in DECADES)
    assert STARTS.index[0].year == 1959 and 'since records began in 1959' in script
    assert RATE.idxmax().year == 1981 and RATE.idxmin().strftime('%Y-%m') == '2021-01'
    assert 13.5 <= RA[1984] < 14.5 and SHARE_1984 > SHARE_NOW, (RA[1984], SHARE_1984)
    assert '20% down' in script
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
        total, chapters = build(SCENES, os.path.join(OUT, 'ep02_housing.mp4'), BUILD,
                                srt_path=os.path.join(OUT, 'ep02_housing.en.srt'))
        with open(os.path.join(OUT, 'ep02_chapters.txt'), 'w') as f:
            for at, name in chapters:
                f.write(f'{fmt(at)} {name}\n')
        print(open(os.path.join(OUT, 'ep02_chapters.txt')).read())
    if '--no-short' not in sys.argv:
        for name, scenes in SHORTS.items():
            build(scenes, os.path.join(OUT, f'{name}.mp4'), os.path.join(BUILD, name), layout='short')
