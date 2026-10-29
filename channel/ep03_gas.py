#!/usr/bin/env python3
"""Coin Theory, episode 3: Why gas got so expensive (the 2026 oil shock).

Data (FRED): GASREGW (US regular gasoline, EIA), GASDESW (US diesel, EIA), DCOILWTICO (WTI crude, EIA),
CPIAUCSL and CPIENGSL (BLS). Facts that are not in FRED (the war, the Strait of Hormuz, the federal gas tax,
the US as top producer) are cited in the description. check_numbers() refuses to render if the narration
disagrees with the data.

    python3 channel/ep03_gas.py [--stills] [--no-short] [--shorts-only]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wk2_art import *  # noqa: E402,F401,F403

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
BUILD = os.path.join(HERE, 'build', 'ep03')

GAS = series('GASREGW')
DSL = series('GASDESW')
OIL = series('DCOILWTICO')
CPI = series('CPIAUCSL')
ENERGY = series('CPIENGSL')

G26 = GAS['2026']
G_LOW, G_LOW_AT = G26.min(), G26.idxmin()
G_PEAK, G_PEAK_AT = G26.max(), G26.idxmax()
G_NOW = GAS.iloc[-1]
O26 = OIL['2026']
O_LOW, O_PEAK, O_PEAK_AT, O_NOW = O26.min(), O26.max(), O26.idxmax(), OIL.iloc[-1]
O_SUMMER = OIL[O_PEAK_AT:'2026-08-31'].min()
G_SUMMER = GAS[G_PEAK_AT:'2026-08-31'].min()
UP_CRUDE = (O_PEAK - O_LOW) / 42
UP_GAS = G_PEAK - G_LOW
DN_CRUDE = (O_PEAK - O_SUMMER) / 42
DN_GAS = G_PEAK - G_SUMMER
CRUDE_GAL = O_NOW / 42
CRUDE_SHARE = CRUDE_GAL / G_NOW * 100
D_LOW, D_NOW, D_PEAK = DSL['2026'].min(), DSL.iloc[-1], DSL['2026'].max()
LAST = CPI.index[-1]
YAGO = LAST - pd.DateOffset(years=1)
E_YOY = ENERGY[LAST] / ENERGY[YAGO] * 100 - 100
CPI_NOW = CPI[LAST] / CPI[YAGO] * 100 - 100
CPI_FEB = CPI['2026-02'].iloc[0] / CPI['2025-02'].iloc[0] * 100 - 100
EXTRA = round(G_NOW, 2) - round(G_LOW, 2)
WEEKLY = 15 * EXTRA
YEARLY = WEEKLY * 52
CPI_M = CPI.resample('MS').mean().dropna()  # no CPI was published for Oct 2025
REAL = pd.Series([v * CPI.iloc[-1] / CPI_M[:d].iloc[-1] for d, v in GAS.items()], index=GAS.index)
REAL08, REAL08_AT = REAL['2008'].max(), REAL['2008'].idxmax()
G22, G22_AT = GAS['2022'].max(), GAS['2022'].idxmax()
GAS_X, GAS_Y = decimal_year(GAS.index), list(GAS.values)
REAL_Y = list(REAL.values)
O_X = decimal_year(O26.index)
O_Y = list(O26.values)
G_X26 = decimal_year(G26.index)
G_Y26 = list(G26.values)


def money(v):
    return f'${v:.2f}'


# ------------------------------------------------------------------ scenes --
def s_hook(c, x):
    t, L = x.t, x.L
    specks(c, t, 31)
    g1 = ease(seg(t, L[1], L[1] + 1.6))
    g2 = ease(seg(t, L[1] + 2.4, L[1] + 3.6))
    price = lerp(G_LOW, G_PEAK, g1) if g2 == 0 else lerp(G_PEAK, G_NOW, g2)
    gas_pump(c, 760, 600, 1.55, money(price), color=mix(MINT, CORAL, g1))
    c.ellipse(820, 606, 200, 14, (0, 0, 0, 60))
    lab = 'January 2026' if g1 < 0.5 else ('May 2026' if g2 < 0.5 else 'today')
    chip(c, 760, 140, lab, GOLD, pop(t, L[0] + 0.4), 24)
    if t > L[2]:
        k = pop(t, L[2] + 0.4)
        c.rrect(960, 300, 1230, 410, 18, (255, 255, 255, 20), CORAL, 3, a=clamp(k))
        c.text(1095, 335, f'+{money(EXTRA)}', 40, CORAL, 900, a=clamp(k))
        c.text(1095, 380, 'every gallon', 18, MUTED, 700, a=clamp(k))
    penny(c, 300, 470, 60, t, 'shocked' if t > L[1] + 1.6 else 'happy', look=(1, 0), talk=x.talk())


def s_title(c, x):
    t = x.t
    specks(c, t, 32, 60)
    k = ease_out(seg(t, 0.1, 0.7))
    c.text(640, 250 - 20 * (1 - k), 'WHY GAS GOT', 70, WHITE, 900, a=k)
    c.text(640, 350 - 20 * (1 - k), 'SO EXPENSIVE', 96, CORAL, 900, a=k)
    gas_pump(c, 640, 640, 0.6, '$$$', a=fade(t, 0.4))
    c.text(640, 680, 'COIN THEORY', 22, MUTED, 800, a=fade(t, 0.8))


def s_strait(c, x):
    t, L = x.t, x.L
    strait_map(c, 0, t, a=fade(t, 0), ships=fade(t, L[1]))
    if t > L[2]:
        k = pop(t, L[2] + 0.3)
        c.rrect(110, 560, 520, 610, 16, GOLD, a=clamp(k))
        c.text(315, 585, '~1/5 of the world\'s oil', 24, INK, 900, a=clamp(k), shadow=False)
    source(c, t, 'US Energy Information Administration (World Oil Transit Chokepoints)')


def s_war(c, x):
    t, L = x.t, x.L
    strait_map(c, ease(seg(t, L[1], L[1] + 1)), t, ships=1.0)
    if t < L[1]:
        chip(c, 640, 80, 'February 28, 2026', CORAL, pop(t, L[0] + 0.3), 26)
    if t > L[2]:
        for i, nm in enumerate(('Iraq', 'Saudi Arabia', 'UAE')):
            k = pop(t, L[2] + 0.6 + 0.4 * i)
            chip(c, 300 + i * 220, 470, nm + ': output cut', CORAL, k, 18)
    if t > L[3]:
        k = pop(t, L[3] + 0.3)
        c.rrect(330, 40, 950, 110, 18, (14, 22, 40, 220), CORAL, 3, a=clamp(k))
        c.text(640, 75, 'Supply gone. No spare to replace it.', 28, WHITE, 900, a=clamp(k))
    source(c, t, 'EIA, Today in Energy (Apr 2026); CNN (Mar 2026)')


def s_oil(c, x):
    t, L = x.t, x.L
    c.text(640, 60, 'Price of a barrel of US crude oil (WTI), 2026', 30, WHITE, 800, a=fade(t, 0))
    k = ease(seg(t, L[1], x.E[-1]))
    px, py = line_chart(c, (150, 120, 1150, 540), O_X, O_Y, (2026.0, O_X[-1] + 0.02), (0, 130), k, CORAL,
                        xticks=(), yticks=range(0, 131, 25), yfmt='${:.0f}', a=fade(t, 0.1), width=4)
    for i, mth in enumerate(('Jan', 'Mar', 'May', 'Jul', 'Sep', 'Nov')):
        c.text(px(2026 + 2 * i / 12 + 0.04), 562, mth, 16, MUTED, 600, a=fade(t, 0.1), shadow=False)
    marks = ((O_X[O_Y.index(O_LOW)], O_LOW, f'${O_LOW:.0f}', MINT, L[1] + 0.5),
             (O_X[O_Y.index(O_PEAK)], O_PEAK, f'${O_PEAK:.0f}', CORAL, L[2] + 0.5),
             (O_X[-1], O_NOW, f'today ${O_NOW:.0f}', GOLD, L[-1] + 2.5))
    for xx, v, lab, col, at in marks:
        kk = pop(t, at)
        if kk > 0:
            c.circle(px(xx), py(v), 9 * kk, col, WHITE, 2)
            bx = min(max(px(xx) + 40, 240), 1060)
            c.rrect(bx - 80, py(v) - 64, bx + 80, py(v) - 26, 14, col, a=clamp(kk))
            c.text(bx, py(v) - 45, lab, 20, INK, 800, a=clamp(kk), shadow=False)
    source(c, t, 'EIA, WTI spot price (DCOILWTICO) via FRED')


def s_barrel(c, x):
    t, L = x.t, x.L
    specks(c, t, 33)
    barrel(c, 260, 470, 1.6, f'1 barrel = ${O_NOW:.0f}')
    if t > L[1]:
        k = ease(seg(t, L[1], L[1] + 1.5))
        n = int(42 * k)
        for i in range(n):
            cx, cy = 520 + (i % 14) * 34, 250 + (i // 14) * 50
            c.icon('fuel', cx, cy, 26, SKY)
        c.text(757, 420, f'{n} gallons', 30, SKY, 900)
        c.text(757, 470, f'crude = {money(CRUDE_GAL)} per gallon', 28, WHITE, 800, a=fade(t, L[1] + 2))
    if t > L[2]:
        g = ease(seg(t, L[2], L[2] + 1.2))
        x0, x1, y0 = 470, 1180, 540
        c.rrect(x0, y0, x1, y0 + 44, 12, (255, 255, 255, 25))
        c.rrect(x0, y0, x0 + (x1 - x0) * CRUDE_SHARE / 100 * g, y0 + 44, 12, CORAL)
        c.text(x0 + (x1 - x0) * CRUDE_SHARE / 200, y0 + 22, f'crude oil {CRUDE_SHARE:.0f}%', 20, INK, 900,
               a=g, shadow=False)
        c.text(x0 + (x1 - x0) * (0.5 + CRUDE_SHARE / 200), y0 + 22, 'refining, shipping, station, taxes', 15,
               WHITE, 800, a=fade(t, L[3]), shadow=False)
    if t > L[4]:
        chip(c, 900, 140, 'Federal gas tax: 18.4 cents since 1993', GOLD, pop(t, L[4] + 0.3), 20)


def s_global(c, x):
    t, L = x.t, x.L
    specks(c, t, 34)
    c.icon('globe', 640, 330, 220, SKY, a=fade(t, 0), stroke=1.5)
    if t < L[2]:
        c.text(640, 90, 'The #1 oil producer in the world: the USA', 32, WHITE, 900, a=fade(t, 0.3))
        penny(c, 1050, 470, 56, t, 'worried' if t > L[1] else 'happy', look=(-1, 0), talk=x.talk())
        return
    c.text(640, 90, 'One global market, one price', 34, WHITE, 900, a=fade(t, L[2]))
    k1 = pop(t, L[2] + 0.8)
    chip(c, 330, 520, 'Buyer in Asia: $110', CORAL, k1, 22)
    k2 = pop(t, L[2] + 2.2)
    chip(c, 950, 520, 'Texas seller: "Not $60!"', GOLD, k2, 22)
    if t > L[3]:
        c.icon('trending-up', 640, 330, 120 * pop(t, L[3] + 0.3), CORAL, stroke=3)


def s_history(c, x):
    t, L = x.t, x.L
    c.text(640, 60, 'US gas price per gallon, adjusted to today\'s dollars', 30, WHITE, 800, a=fade(t, 0))
    k = ease(seg(t, L[0] + 0.5, L[-1] + 1))
    px, py = line_chart(c, (150, 120, 1150, 540), GAS_X, REAL_Y, (1990.6, GAS_X[-1] + 0.1), (0, 7), k, GOLD,
                        xticks=range(1995, 2030, 5), yticks=range(0, 8), yfmt='${:.0f}', a=fade(t, 0.1), width=3)
    events = ((1990.8, '1990 Gulf War', L[0] + 1.5), (2008.5, '2008 oil spike', L[1] + 0.3),
              (2022.45, '2022 Ukraine war', L[2] + 0.3), (2026.35, '2026 Iran war', L[3] + 0.3))
    for xx, lab, at in events:
        kk = pop(t, at)
        if kk <= 0 or xx > lerp(1990.6, GAS_X[-1] + 0.1, k):
            continue
        i = min(range(len(GAS_X)), key=lambda j: abs(GAS_X[j] - xx))
        yy = max(REAL_Y[max(0, i - 12):i + 12])
        c.circle(px(xx), py(yy), 7 * kk, CORAL, WHITE, 2)
        bx = min(max(px(xx), 220), 1050)
        c.rrect(bx - 95, py(yy) - 60, bx + 95, py(yy) - 26, 12, CORAL, a=clamp(kk))
        c.text(bx, py(yy) - 43, lab, 17, INK, 800, a=clamp(kk), shadow=False)
    source(c, t, 'EIA (GASREGW), BLS CPI via FRED; Coin Theory inflation adjustment')


def s_feathers(c, x):
    t, L = x.t, x.L
    specks(c, t, 35)
    c.text(640, 70, 'Change per gallon, 2026', 32, WHITE, 900, a=fade(t, 0))
    if t < L[1]:
        penny(c, 640, 380, 70, t, 'worried', talk=x.talk())
        return
    items_up = (('oil (per gallon)', UP_CRUDE, SKY), ('pump price', UP_GAS, CORAL))
    items_dn = (('oil (per gallon)', DN_CRUDE, SKY), ('pump price', DN_GAS, MINT))
    k_up = t > L[1]
    k_dn = t > L[2]
    if k_up:
        c.text(380, 140, 'On the way UP (Jan to spring)', 22, CORAL, 900, a=fade(t, L[1]))
        compare_bars(c, t, [(a, b, col) for a, b, col in items_up], L[1] + 0.3, 2.0, 2.0,
                     lambda v: f'+${v:.2f}', box=(140, 180, 620, 500))
    if k_dn:
        c.text(900, 140, 'On the way DOWN (spring to July)', 22, MINT, 900, a=fade(t, L[2]))
        compare_bars(c, t, [(a, b, col) for a, b, col in items_dn], L[2] + 0.3, 2.0, 2.0,
                     lambda v: f'-${v:.2f}', box=(660, 180, 1140, 500))
    if t > L[3]:
        k = pop(t, L[3] + 0.3)
        c.icon('rocket', 360, 70, 56 * k, CORAL, stroke=2.5)
        c.icon('feather', 920, 70, 56 * k, MINT, stroke=2.5)
    source(c, t, 'EIA via FRED (DCOILWTICO, GASREGW); a barrel holds 42 gallons')


def s_diesel(c, x):
    t, L = x.t, x.L
    specks(c, t, 36)
    if t < L[3]:
        icon_row(c, t, [('truck', 'Trucks'), ('train-front', 'Trains'), ('tractor', 'Tractors'),
                        ('ship', 'Ships')], L[0] + 0.5, max(1.0, L[1] - L[0]), y=250, color=SKY)
        if t > L[1]:
            g = ease(seg(t, L[1] + 0.5, L[1] + 2.5))
            c.text(640, 520, f'Diesel: {money(lerp(D_LOW, D_NOW, g))} / gallon', 48, CORAL, 900,
                   a=fade(t, L[1] + 0.3))
        return
    if t < L[4]:
        c.icon('truck', 300, 340, 160, SKY, a=fade(t, L[3]))
        c.icon('arrow-right', 520, 340, 80, MUTED, a=fade(t, L[3] + 0.6))
        c.icon('shopping-cart', 740, 340, 160, GOLD, a=fade(t, L[3] + 1.2))
        c.icon('trending-up', 960, 340, 120, CORAL, a=fade(t, L[3] + 1.8), stroke=3)
        return
    items = (('Energy prices', E_YOY, CORAL), ('All prices (Feb)', CPI_FEB, MINT), ('All prices (Sep)', CPI_NOW,
                                                                                     GOLD))
    c.text(640, 90, 'Price rise over the past 12 months', 30, WHITE, 900, a=fade(t, L[4]))
    compare_bars(c, t, items, L[4] + 0.3, 3.0, 25, lambda v: f'{v:.1f}%')
    source(c, t, 'BLS CPI (CPIENGSL, CPIAUCSL), EIA diesel (GASDESW) via FRED')


def s_wallet(c, x):
    t, L = x.t, x.L
    specks(c, t, 37)
    gas_pump(c, 260, 560, 0.9, money(G_NOW))
    if t > L[1]:
        k = pop(t, L[1] + 0.3)
        c.text(700, 200, '15 gallons a week', 28, MUTED, 800, a=clamp(k))
        c.text(700, 290, f'+${WEEKLY:.0f} a week', 70, CORAL, 900, a=clamp(k))
    if t > L[2]:
        k = pop(t, L[2] + 0.3)
        c.rrect(480, 380, 920, 500, 22, (255, 255, 255, 20), CORAL, 3, a=clamp(k))
        c.text(700, 420, f'about ${round(YEARLY, -1):,.0f}', 50, WHITE, 900, a=clamp(k))
        c.text(700, 472, 'more per year', 20, MUTED, 700, a=clamp(k))
    if t > L[3]:
        chip(c, 700, 560, 'two cars or driving for work: x2', GOLD, pop(t, L[3] + 0.3), 20)
    penny(c, 1080, 470, 54, t, 'sad' if t > L[2] else 'worried', look=(-1, 0), talk=x.talk())


def s_record(c, x):
    t, L = x.t, x.L
    specks(c, t, 38)
    c.text(640, 70, 'Is this the most expensive gas ever?', 34, WHITE, 900, a=fade(t, 0))
    items = (('today', G_NOW, GOLD), ('June 2022', G22, CORAL), ('2008, in today\'s $', REAL08, CORAL))
    compare_bars(c, t, items, L[1] - 0.2, max(0.5, L[2] - L[1] + 1.5), 7, money, box=(220, 170, 1060, 530))
    source(c, t, 'EIA (GASREGW), BLS CPI via FRED; Coin Theory inflation adjustment')


def s_next(c, x):
    t, L = x.t, x.L
    if t < L[1]:
        strait_map(c, 0.0, t, ships=0.3)
        c.text(640, 70, 'The key: ships moving again', 30, WHITE, 900, a=fade(t, 0.3))
        return
    specks(c, t, 39)
    for i, (lab, ic, col, at) in enumerate((('Tankers pass safely', 'trending-down', MINT, L[1]),
                                            ('Attacks continue', 'trending-up', CORAL, L[2]))):
        k = pop(t, at + 0.3)
        if k <= 0:
            continue
        cx = 360 + i * 560
        c.rrect(cx - 230, 170, cx + 230, 500, 24, (255, 255, 255, 16), col, 3, a=clamp(k))
        c.icon(ic, cx, 300, 120 * k, col, stroke=3)
        c.text(cx, 430, lab, 28, WHITE, 900, a=clamp(k))
    if t > L[3]:
        chip(c, 640, 600, 'Emergency oil reserve = a patch, not a fix', GOLD, pop(t, L[3] + 0.3), 20)


def s_tips(c, x):
    t, L = x.t, x.L
    specks(c, t, 40)
    c.text(640, 80, 'What actually helps', 36, WHITE, 900, a=fade(t, 0))
    span = x.E[-1] - L[1]
    icon_row(c, t, [('smartphone', 'Compare\nstations'), ('gauge', 'Tire\npressure'),
                    ('car', 'Drive\nsmoothly'), ('route', 'Combine\ntrips')], L[1], span * 0.8, y=300)
    if t > L[4]:
        chip(c, 640, 590, 'Education only - not financial advice', MUTED, pop(t, L[4] + 0.3), 18)


def s_outro(c, x):
    t, L = x.t, x.L
    specks(c, t, 41, 50)
    penny(c, 260, 380, 76, t, 'happy', look=(1, 0), talk=x.talk(), wave=t > x.E[-1])
    if t > L[1] and t < x.E[-1]:
        fed_building(c, 820, 480, 0.9, a=fade(t, L[1]))
        c.icon('arrow-up', 1080, 260, 90 * pop(t, L[1] + 1), CORAL, stroke=3)
    if t > L[2]:
        k = ease_out(seg(t, L[2], L[2] + 0.6))
        c.text(400, 560, 'COIN THEORY', 30, GOLD, 900, anchor='lm', a=k)
        c.text(400, 595, 'money, explained with real data', 18, MUTED, 600, anchor='lm', a=k)
    if t > x.E[-1]:
        c.rrect(560, 150, 1200, 510, 20, (255, 255, 255, 10), (255, 255, 255, 40), 2, a=fade(t, x.E[-1], 0.8))


SCENES = [
    dict(draw=s_hook, chapter='Intro: $2.78 to $4.50', cam=(1.0, 1.05), lines=[
        f"In January, a gallon of regular gas in America cost about {money(G_LOW)}.",
        f"By May, it hit {money(G_PEAK)}. Today, it's still around {money(G_NOW)}.",
        f"That's an extra {money(EXTRA)} on every single gallon. So where is all that money going? And when will "
        "it come down?",
    ], sfx=lambda L: [(L[1], 'whoosh'), (L[2] + 0.4, 'ding')]),
    dict(draw=s_title, lines=[], min=3.2, captions=False, trans='fadeblack', sfx=lambda L: [(0.2, 'ding')]),
    dict(draw=s_strait, chapter='One narrow strait', trans='fadeblack', cam=(1.0, 1.06), focus=(0.7, 0.5), lines=[
        "The story starts on the other side of the world, in a narrow channel of water called the Strait of "
        "Hormuz.",
        "It sits between Iran and Oman, and it's the only way for ships to sail out of the Persian Gulf.",
        "Before this year, about a fifth of all the oil the world uses passed through it on tankers, every single "
        "day.",
        "Oil from Saudi Arabia, Iraq, Kuwait, and the United Arab Emirates all squeezes through this one gap.",
    ], sfx=lambda L: [(L[2] + 0.3, 'pop')]),
    dict(draw=s_war, chapter='February 28: the shock', cam=(1.0, 1.06), focus=(0.7, 0.5), lines=[
        "On February 28, the United States and Israel launched strikes on Iran, and the region went to war.",
        "Iran threatened to attack tankers in the strait. Within days, most shipping through it stopped.",
        "Oil producers like Iraq, Saudi Arabia, and the Emirates suddenly had no way to ship their oil out, so "
        "they cut production.",
        "Almost overnight, the world lost a huge chunk of its oil supply, and there was no spare capacity left to "
        "replace it.",
    ], sfx=lambda L: [(L[0] + 0.3, 'pop'), (L[1], 'down'), (L[3] + 0.3, 'pop')]),
    dict(draw=s_oil, chapter='Oil\'s record jump', cam=(1.0, 1.04), lines=[
        "Now watch what happened to the price of oil.",
        f"In early January, a barrel of American crude cost about ${O_LOW:.0f}.",
        f"By April, it hit ${O_PEAK:.0f}. That's more than double, in about three months.",
        "The US Energy Information Administration says the jump in global oil prices in the first three months "
        "of the year was the biggest in its records going back to 1988, even after adjusting for inflation.",
        "Prices cooled off over the summer as some tankers started moving again. Then this fall, a new wave of "
        f"attacks on ships pushed oil back above $100. Today it's around ${O_NOW:.0f} a barrel.",
    ], sfx=lambda L: [(L[1] + 0.5, 'pop'), (L[2] + 0.5, 'pop'), (L[-1] + 2.5, 'ding')]),
    dict(draw=s_barrel, chapter='From barrel to gallon', lines=[
        "So how does a barrel of oil turn into the number on the pump?",
        f"One barrel holds 42 gallons. At about ${O_NOW:.0f} a barrel, the crude oil alone costs about "
        f"{money(CRUDE_GAL)} for every gallon of gas.",
        f"That's about {CRUDE_SHARE:.0f}% of the {money(G_NOW)} you pay at the pump.",
        "The rest pays for refining the crude into gasoline, trucking it to your town, running the gas station, "
        "and taxes.",
        "The federal gas tax is 18.4 cents a gallon, and it hasn't changed since 1993. States add their own tax "
        "on top, which is why prices are so different from state to state.",
        "But because crude is the biggest piece, when oil goes up, your gas goes up. There's no way around it.",
    ], sfx=lambda L: [(L[1], 'whoosh'), (L[2], 'pop'), (L[4] + 0.3, 'pop')]),
    dict(draw=s_global, chapter='Doesn\'t America make its own oil?', lines=[
        "Here's the part that confuses a lot of people. The United States is the biggest oil producer in the "
        "world.",
        "So why should a war on the other side of the planet raise prices here at home?",
        "Because oil is sold on one global market. If a buyer in Asia will pay $110 a barrel, a Texas oil "
        "company won't sell it to you for $60.",
        "When supply disappears anywhere, the price goes up everywhere, including at the gas station down your "
        "street.",
        "Producing a lot of our own oil does help. It keeps supplies flowing and softens the blow. It just can't "
        "make prices here immune to the rest of the world.",
    ], sfx=lambda L: [(L[2] + 0.8, 'pop'), (L[2] + 2.2, 'pop'), (L[3] + 0.3, 'whoosh')]),
    dict(draw=s_history, chapter='We\'ve been here before', cam=(1.0, 1.04), lines=[
        "Oil shocks aren't new. Here's the price of gas since 1990, adjusted for inflation. In 1990, Iraq "
        "invaded Kuwait, and gas jumped.",
        "In 2008, oil hit record highs during a global boom, right before the financial crisis.",
        "In 2022, Russia invaded Ukraine, and gas topped $5 a gallon for the first time.",
        "And now, in 2026, the war with Iran. Every big spike on this chart started with the same thing: oil "
        "supply that suddenly looked unsafe.",
    ], sfx=lambda L: [(L[1] + 0.3, 'pop'), (L[2] + 0.3, 'pop'), (L[3] + 0.3, 'pop')]),
    dict(draw=s_feathers, chapter='Rockets and feathers', lines=[
        "You've probably noticed something else that feels unfair. Gas goes up fast, but comes down slowly.",
        f"From January to the spring peak, oil rose by about {money(UP_CRUDE)} for every gallon's worth of "
        f"crude. Pump prices rose even more, about {money(UP_GAS)}.",
        f"Then, from April to July, oil fell by about {money(DN_CRUDE)} a gallon. But pump prices only fell about "
        f"{money(DN_GAS)}.",
        "Economists have a name for this: rockets and feathers. Prices shoot up like a rocket, and float down like "
        "a feather.",
        "One explanation is that stations raise prices fast to cover their next, more expensive delivery, but cut "
        "them slowly, because drivers don't shop around as hard when prices are falling.",
    ], sfx=lambda L: [(L[1] + 0.3, 'pop'), (L[2] + 0.3, 'pop'), (L[3] + 0.3, 'whoosh')]),
    dict(draw=s_diesel, chapter='Why everything else costs more', lines=[
        "And gas isn't the only fuel. Diesel powers the trucks, trains, tractors, and ships that move almost "
        "everything we buy.",
        f"This year, diesel went from about {money(D_LOW)} a gallon to over $6. Today it's around "
        f"{money(D_NOW)}.",
        "Diesel jumped even more than gasoline, because the Middle East also exports a lot of diesel and jet fuel, "
        "and those shipments were cut off too.",
        "When it costs more to move food and goods, those costs slowly show up on store shelves, too.",
        f"That's why energy prices are up about {E_YOY:.0f}% from a year ago, and overall inflation climbed from "
        f"about {CPI_FEB:.1f}% in February to {CPI_NOW:.1f}% in September.",
    ], sfx=lambda L: [(L[1] + 0.5, 'whoosh'), (L[4] + 0.3, 'pop')]),
    dict(draw=s_wallet, chapter='What it costs you', lines=[
        "So what does all of this mean for your wallet?",
        f"Say you fill up a 15 gallon tank once a week. At {money(EXTRA)} more per gallon than in January, that's "
        f"about ${WEEKLY:.0f} more every single week.",
        f"Over a year, that adds up to about ${round(YEARLY, -1):,.0f}. It's like a new bill that nobody asked "
        "you to sign up for.",
        "And if you drive for work, or your family has two cars, it can easily be double that.",
    ], sfx=lambda L: [(L[1] + 0.3, 'pop'), (L[2] + 0.3, 'down')]),
    dict(draw=s_record, chapter='Is this a record?', lines=[
        "Does it feel like the most expensive gas ever? It isn't, at least not yet.",
        f"In June 2022, the national average peaked at about {money(G22)} a gallon.",
        f"And in the summer of 2008, after adjusting for inflation, gas cost about {money(REAL08)} in today's "
        "money.",
        "So today's prices hurt, but we have been here before, and both of those spikes eventually came back "
        "down.",
    ], sfx=lambda L: [(L[1] + 0.3, 'pop'), (L[2] + 0.3, 'pop')]),
    dict(draw=s_next, chapter='When will it come down?', lines=[
        "So when will gas get cheaper? Honestly, nobody knows for sure. It mostly depends on one thing: ships "
        "moving safely through Hormuz again.",
        "If tankers can pass safely, oil could fall quickly, and pump prices would follow, slowly, like a feather.",
        "If the attacks continue, prices could stay high or climb even further.",
        "The US keeps an emergency stockpile called the Strategic Petroleum Reserve, stored in giant underground "
        "salt caverns along the Gulf Coast.",
        "Releasing some of it adds supply for a while and can calm prices. But no reserve can replace a fifth of "
        "the world's oil for long. It's a patch, not a fix.",
    ], sfx=lambda L: [(L[1] + 0.3, 'pop'), (L[2] + 0.3, 'pop')]),
    dict(draw=s_tips, chapter='What you can do', lines=[
        "In the meantime, a few simple things genuinely help.",
        "Use a gas price app to compare nearby stations. Prices just a mile apart can differ a lot.",
        "Keep your tires properly inflated, drive smoothly, and combine short trips. Hard braking and fast "
        "starts burn extra fuel.",
        "Warehouse clubs and grocery store reward programs often knock a few cents off every gallon, too.",
        "And if you pay at the pump with a credit card, try to pay it off in full, because the next problem is "
        "interest rates.",
    ]),
    dict(draw=s_outro, chapter='Recap', tail=12, cam=(1.0, 1.02), lines=[
        "So gas didn't get expensive by accident. A war shut the world's most important oil route, oil doubled, "
        "and the cost flowed straight into your tank.",
        "Higher fuel prices pushed inflation up so much that the Federal Reserve raised interest rates for the "
        "first time since 2023.",
        "Next time: what that rate hike means for your credit cards, your savings, and your mortgage. Subscribe to "
        "Coin Theory so you don't miss it.",
    ], sfx=lambda L: [(L[1] + 1, 'pop'), (L[2], 'pop')]),
]

SHORTS = {
    'ep03_short_jump': [SCENES[0], SCENES[4], end_card("Here's why, and when it might come down. Full story on "
                                                       "Coin Theory.")],
    'ep03_short_barrel': [SCENES[5], end_card("And that's just the start. Watch the full story on Coin Theory.")],
    'ep03_short_feathers': [SCENES[8], end_card("Why gas got so expensive in the first place? Full story on Coin "
                                                "Theory.")],
}


def check_numbers():
    script = ' '.join(l for sc in SCENES for l in sc['lines'])
    assert G_LOW_AT.month == 1 and G_PEAK_AT.month == 5 and G_LOW_AT.year == G_PEAK_AT.year == 2026
    assert O_PEAK / O_LOW > 2 and 'more than double' in script, O_PEAK / O_LOW
    assert O_PEAK_AT.month == 4 and OIL.idxmin() < O_PEAK_AT and O26.idxmin().month == 1
    assert O_SUMMER < 100 and O_NOW > 100 and OIL['2026-09-01':].max() > 100
    assert OIL[O_PEAK_AT:'2026-08-31'].idxmin().month == 7 and GAS[G_PEAK_AT:'2026-08-31'].idxmin().month == 7
    assert UP_GAS > UP_CRUDE and DN_GAS < DN_CRUDE, (UP_GAS, UP_CRUDE, DN_GAS, DN_CRUDE)
    assert D_PEAK > 6 and D_NOW > 6 and 'to over $6' in script
    assert CPI['2026-02'].index[0].month == 2 and CPI.index[-1].month == 9 and 'in September' in script
    assert G22_AT.month == 6 and G22 > 5 and 'topped $5' in script and G22 == GAS.max()
    assert REAL08 > REAL['2022'].max() and REAL08 > G_NOW and REAL08_AT.year == 2008
    assert GAS.index[0].year == 1990 and 'since 1990' in script
    assert 'February 28' in script and '18.4 cents' in script and 'since 1993' in script
    print('numbers check: OK')
    print(f'  gas {G_LOW:.3f}->{G_PEAK:.3f}->{G_NOW:.3f}, oil {O_LOW}->{O_PEAK}->{O_NOW}, crude/gal {CRUDE_GAL:.2f} '
          f'({CRUDE_SHARE:.1f}%), up {UP_CRUDE:.2f}/{UP_GAS:.2f} down {DN_CRUDE:.2f}/{DN_GAS:.2f}, diesel '
          f'{D_LOW}->{D_NOW}, energy {E_YOY:.1f}% cpi {CPI_FEB:.2f}->{CPI_NOW:.2f}, weekly {WEEKLY:.2f} yearly '
          f'{YEARLY:.0f}, 2022 {G22}, 2008 real {REAL08:.2f}')


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
        total, chapters = build(SCENES, os.path.join(OUT, 'ep03_gas.mp4'), BUILD,
                                srt_path=os.path.join(OUT, 'ep03_gas.en.srt'))
        with open(os.path.join(OUT, 'ep03_chapters.txt'), 'w') as f:
            for at, name in chapters:
                f.write(f'{fmt_time(at)} {name}\n')
        print(open(os.path.join(OUT, 'ep03_chapters.txt')).read())
    if '--no-short' not in sys.argv:
        for name, scenes in SHORTS.items():
            build(scenes, os.path.join(OUT, f'{name}.mp4'), os.path.join(BUILD, name), layout='short')
