#!/usr/bin/env python3
"""Coin Theory, episode 4: The Fed just raised rates. What it means for your money.

Data (FRED): DFEDTARU/DFEDTARL (Fed funds target range), DPRIME (bank prime loan rate), TERMCBCCALLNS (credit
card plan rates, all accounts), TERMCBAUTO48NS (48-month new car loans), MORTGAGE30US (Freddie Mac), SNDR (FDIC
national savings rate), CPIAUCSL (BLS), UNRATE (BLS). The October vote is from the Fed's statement, cited in the
description. check_numbers() refuses to render if the narration disagrees with the data.

    python3 channel/ep04_fed.py [--stills] [--no-short] [--shorts-only]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wk2_art import *  # noqa: E402,F401,F403

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
BUILD = os.path.join(HERE, 'build', 'ep04')

UP = series('DFEDTARU')
LO = series('DFEDTARL')
PRIME = series('DPRIME')
CC = series('TERMCBCCALLNS')
AUTO = series('TERMCBAUTO48NS')
MORT = series('MORTGAGE30US_wk2')
SAVE = series('SNDR')
CPI = series('CPIAUCSL')
UNRATE = series('UNRATE')
FF = series('FEDFUNDS')
FF_PEAK, FF_PEAK_AT = FF.max(), FF.idxmax()
CPI_YOY = (CPI / CPI.shift(12) * 100 - 100)['1974':'1981']
INF_70S, INF_70S_AT = CPI_YOY.max(), CPI_YOY.idxmax()
FF_X, FF_Y = decimal_year(FF.index), list(FF.values)

N_HIKES = int((UP['2022-01-01':'2023-12-31'].diff() > 0).sum())
PEAK_U = UP['2022':'2024'].max()
LAST_HIKE_BEFORE = UP[:'2026-01-01'][UP[:'2026-01-01'].diff() > 0].index[-1]
HIKE_DAY = UP[UP.diff() > 0].index[-1]
LOW_U, LOW_L = UP['2025-12-31'], LO['2025-12-31']
NOW_U, NOW_L = UP.iloc[-1], LO.iloc[-1]
LAST = CPI.index[-1]
YAGO = LAST - pd.DateOffset(years=1)
CPI_NOW = CPI[LAST] / CPI[YAGO] * 100 - 100
CPI_FEB = CPI['2026-02-01'] / CPI['2025-02-01'] * 100 - 100
P_NOW = PRIME.iloc[-1]
CC_NOW = CC.iloc[-1]
CC_COST = 5000 * CC_NOW / 100
AUTO_NOW = AUTO.iloc[-1]
M26 = MORT['2026']
M_LOW, M_LOW_AT = M26[:'2026-06-30'].min(), M26[:'2026-06-30'].idxmin()
M_PEAK, M_PEAK_AT = M26.max(), M26.idxmax()
M_NOW = MORT.iloc[-1]
S_NOW = SAVE.iloc[-1]
U_NOW = UNRATE.iloc[-1]
REAL_LOSS = round(CPI_NOW, 1) - round(S_NOW, 2)
EF_NOW = 10000 * S_NOW / 100
EF_ALT = 10000 * 3.5 / 100
RATE_X, RATE_Y = decimal_year(UP['2015':].index), list(UP['2015':].values)
M_X, M_Y = decimal_year(M26.index), list(M26.values)


def payment(loan, rate, years=30):
    r, n = rate / 100 / 12, years * 12
    return loan * r / (1 - (1 + r) ** -n)


PAY_LOW, PAY_NOW = payment(300000, M_LOW), payment(300000, M_NOW)
QUARTER = 5000 * 0.25 / 100


def pct(v):
    s = f'{v:.2f}'.rstrip('0').rstrip('.')
    return s + '%'


# ------------------------------------------------------------------ scenes --
def s_hook(c, x):
    t, L = x.t, x.L
    specks(c, t, 51)
    fed_building(c, 760, 480, 1.0, a=fade(t, 0.2))
    k = pop(t, L[0] + 2.5)
    if k > 0:
        c.icon('arrow-up', 1060, 230, 130 * k, CORAL, stroke=3)
        chip(c, 760, 110, 'Sept 17, 2026: rates UP', CORAL, k, 26)
    if t > L[2]:
        for i, (ic, col) in enumerate((('credit-card', SKY), ('car', GOLD), ('house', CORAL), ('piggy-bank', MINT))):
            kk = pop(t, L[2] + 1 + 0.6 * i)
            c.circle(475 + i * 190, 560, 46 * kk, (14, 22, 40, 230), col, 3, a=clamp(kk))
            c.icon(ic, 475 + i * 190, 560, 48 * kk, col, a=clamp(kk))
    penny(c, 220, 470, 60, t, 'shocked' if L[0] + 2.5 < t < L[2] else 'happy', look=(1, 0), talk=x.talk())


def s_title(c, x):
    t = x.t
    specks(c, t, 52, 60)
    k = ease_out(seg(t, 0.1, 0.7))
    c.text(640, 240 - 20 * (1 - k), 'THE FED JUST', 70, WHITE, 900, a=k)
    c.text(640, 340 - 20 * (1 - k), 'RAISED RATES', 96, CORAL, 900, a=k)
    c.text(640, 430, 'what it means for your money', 30, GOLD, 800, a=fade(t, 0.5))
    c.text(640, 660, 'COIN THEORY', 22, MUTED, 800, a=fade(t, 0.8))


def s_what(c, x):
    t, L = x.t, x.L
    specks(c, t, 53)
    if t < L[1]:
        for i, (ic, lab) in enumerate((('house', 'mortgage rate'), ('credit-card', 'card rate'))):
            k = pop(t, 0.3 + i * 0.5)
            cx = 420 + i * 440
            c.icon(ic, cx, 320, 120 * k, MUTED, a=clamp(k))
            c.text(cx, 430, lab, 24, MUTED, 800, a=clamp(k))
            if t > L[0] + 2.5:
                c.line([(cx - 90, 230), (cx + 90, 410)], CORAL, 8)
        return
    if t < L[3]:
        landmark_k = fade(t, L[1])
        c.icon('landmark', 300, 330, 150, GOLD, a=landmark_k)
        c.icon('arrow-left-right', 640, 330, 110, MUTED, a=fade(t, L[1] + 1.5))
        c.icon('landmark', 980, 330, 150, GOLD, a=landmark_k)
        c.text(640, 140, 'Banks lending to each other, overnight', 30, WHITE, 900, a=fade(t, L[1] + 0.5))
        if t > L[2]:
            chip(c, 640, 520, f'Target: {pct(NOW_L)} to {pct(NOW_U)}', GOLD, pop(t, L[2] + 0.3), 30)
        return
    steps = (('landmark', 'The Fed'), ('building-2', 'Banks'), ('credit-card', 'Your loans'))
    for i, (ic, lab) in enumerate(steps):
        k = pop(t, L[3] + 0.4 + 0.9 * i)
        cx = 260 + i * 380
        c.circle(cx, 320, 90 * k, (255, 255, 255, 18), GOLD, 3, a=clamp(k))
        c.icon(ic, cx, 320, 80 * k, GOLD, a=clamp(k))
        c.text(cx, 450, lab, 26, WHITE, 900, a=clamp(k))
        if i:
            c.icon('arrow-right', cx - 190, 320, 60 * k, MUTED, a=clamp(k))


def s_history(c, x):
    t, L = x.t, x.L
    c.text(640, 60, 'Fed funds target rate (top of the range)', 30, WHITE, 800, a=fade(t, 0))
    k = ease(seg(t, L[0] + 0.5, x.E[-1]))
    px, py = line_chart(c, (150, 120, 1150, 530), RATE_X, RATE_Y, (2015, RATE_X[-1] + 0.1), (0, 6), k, GOLD,
                        xticks=range(2015, 2027, 2), yticks=range(0, 7), yfmt='{:.0f}%', a=fade(t, 0.1), width=4)
    marks = ((2023.57, PEAK_U, f'{N_HIKES} hikes to {pct(PEAK_U)}', CORAL, L[1] + 2),
             (2025.95, LOW_U, f'cut to {pct(LOW_U)}', MINT, L[2] + 1),
             (RATE_X[-1], NOW_U, f'Sept 2026: {pct(NOW_U)}', CORAL, L[3] + 0.5))
    for xx, v, lab, col, at in marks:
        kk = pop(t, at)
        if kk > 0:
            c.circle(px(xx), py(v), 9 * kk, col, WHITE, 2)
            bx = min(max(px(xx), 230), 1040)
            dy = 45 if col == MINT else -45
            bx = bx - 120 if col == MINT else bx
            c.rrect(bx - 110, py(v) + dy - 19, bx + 110, py(v) + dy + 19, 14, col, a=clamp(kk))
            c.text(bx, py(v) + dy, lab, 19, INK, 800, a=clamp(kk), shadow=False)
    source(c, t, 'Federal Reserve (DFEDTARU) via FRED')


def s_why(c, x):
    t, L = x.t, x.L
    specks(c, t, 54)
    if t < L[2]:
        barrel(c, 400, 480, 1.6, 'oil shock', a=fade(t, 0.2))
        gas_pump(c, 860, 560, 1.0, '$4.27', a=fade(t, L[1]))
        return
    if t < L[3]:
        c.text(640, 90, 'Inflation vs the Fed\'s 2% target', 32, WHITE, 900, a=fade(t, L[2]))
        compare_bars(c, t, (('target', 2.0, MINT), ('Feb 2026', CPI_FEB, GOLD), ('Sep 2026', CPI_NOW, CORAL)),
                     L[2] + 0.3, 3.0, 5, lambda v: f'{v:.1f}%')
        source(c, t, 'BLS CPI (CPIAUCSL) via FRED')
        return
    if t < L[4]:
        steps = (('percent', 'Higher rates'), ('shopping-cart', 'Less borrowing\n& spending'),
                 ('trending-down', 'Prices cool'))
        icon_row(c, t, steps, L[3], max(1.0, L[4] - L[3]), y=300)
        return
    barrel(c, 400, 480, 1.4)
    k = pop(t, L[4] + 1)
    c.line([(300, 260), (500, 500)], CORAL, 10, a=clamp(k))
    c.text(830, 300, 'Rates can\'t make oil.', 34, WHITE, 900, a=fade(t, L[4] + 0.5))
    c.text(830, 360, 'They can only slow spending.', 30, GOLD, 800, a=fade(t, L[4] + 2.5))


def s_70s(c, x):
    t, L = x.t, x.L
    c.text(640, 60, 'Fed funds rate since 1954', 30, WHITE, 800, a=fade(t, 0))
    k = ease(seg(t, L[0] + 0.5, L[2] + 1))
    px, py = line_chart(c, (150, 120, 1150, 530), FF_X, FF_Y, (1954.5, FF_X[-1] + 0.5), (0, 20), k, GOLD,
                        xticks=range(1960, 2030, 10), yticks=range(0, 21, 5), yfmt='{:.0f}%', a=fade(t, 0.1),
                        width=3)
    xx = FF_X[FF_Y.index(FF_PEAK)]
    kk = pop(t, L[2] + 0.5)
    if kk > 0:
        c.circle(px(xx), py(FF_PEAK), 9 * kk, CORAL, WHITE, 2)
        c.rrect(px(xx) + 20, py(FF_PEAK) - 18, px(xx) + 230, py(FF_PEAK) + 18, 14, CORAL, a=clamp(kk))
        c.text(px(xx) + 125, py(FF_PEAK), f'1981: about {FF_PEAK:.0f}%', 19, INK, 800, a=clamp(kk), shadow=False)
    if t > L[3]:
        kk = pop(t, L[3] + 0.3)
        c.circle(px(FF_X[-1]), py(FF_Y[-1]), 9 * kk, MINT, WHITE, 2)
        chip(c, 1000, 200, 'today: small steps', MINT, kk, 22)
    source(c, t, 'Federal Reserve (FEDFUNDS) via FRED')


def s_fixed(c, x):
    t, L = x.t, x.L
    specks(c, t, 62)
    c.text(640, 80, 'Does the hike change your payment?', 34, WHITE, 900, a=fade(t, 0))
    cols = (('FIXED RATE', 'lock', MINT, 'no change', L[0] + 1.5, ('existing mortgage', 'existing car loan')),
            ('VARIABLE RATE', 'trending-up', CORAL, 'goes up', L[1], ('credit cards', 'home equity lines',
                                                                       'adjustable mortgages')))
    for i, (head, ic, col, verdict, at, rows) in enumerate(cols):
        k = pop(t, at)
        if k <= 0:
            continue
        cx = 360 + i * 560
        c.rrect(cx - 240, 140, cx + 240, 560, 24, (255, 255, 255, 14), col, 3, a=clamp(k))
        c.text(cx, 185, head, 28, col, 900, a=clamp(k))
        c.icon(ic, cx, 270, 90 * k, col, stroke=2.5)
        for j, r in enumerate(rows):
            c.text(cx, 360 + j * 40, r, 22, WHITE, 700, a=clamp(k))
        c.text(cx, 520, verdict, 30, col, 900, a=clamp(k))


def s_vote(c, x):
    t, L = x.t, x.L
    specks(c, t, 55)
    c.text(640, 80, 'October 28 vote', 34, WHITE, 900, a=fade(t, 0))
    for i in range(12):
        k = pop(t, L[0] + 1 + i * 0.12)
        dissent = i >= 10
        cx, cy = 230 + (i % 6) * 165, 230 + (i // 6) * 170
        person(c, cx, cy + 60, 0.6 * k, CORAL if dissent else SKY, t, i, 'worried' if dissent else 'happy',
               a=clamp(k))
    c.text(400, 590, '10: hold', 26, SKY, 900, a=fade(t, L[0] + 3))
    c.text(880, 590, '2: raise again', 26, CORAL, 900, a=fade(t, L[0] + 3.5))
    if t > L[3]:
        chip(c, 640, 140, f'Unemployment: {U_NOW}%', MINT, pop(t, L[3] + 0.3), 22)


def s_cards(c, x):
    t, L = x.t, x.L
    specks(c, t, 56)
    card(c, 330, 330, 1.3, a=fade(t, 0), color=SKY)
    if t > L[1]:
        chip(c, 330, 520, 'variable rate = moves with prime', GOLD, pop(t, L[1] + 0.3), 18)
    if t > L[2]:
        compare_bars(c, t, (('prime rate', P_NOW, GOLD), ('avg card rate', CC_NOW, CORAL)), L[2] + 0.5, 2.5, 25,
                     lambda v: f'{v:.1f}%', box=(640, 160, 1180, 500))
    if t > L[3]:
        k = pop(t, L[3] + 0.3)
        c.rrect(460, 560, 1180, 620, 18, (14, 22, 40, 230), CORAL, 3, a=clamp(k))
        c.text(820, 590, f'$5,000 balance = about ${round(CC_COST, -1):,.0f} interest a year', 22, WHITE, 900,
               a=clamp(k))
    if t > L[4]:
        chip(c, 330, 140, f'this hike: +0.25% = +${QUARTER:.2f}/yr', GOLD, pop(t, L[4] + 0.3), 20)
    source(c, t, 'Federal Reserve (DPRIME, TERMCBCCALLNS) via FRED') if t < L[3] else None


def s_mortgage(c, x):
    t, L = x.t, x.L
    if t < L[4]:
        c.text(640, 60, '30-year mortgage rate, 2026', 30, WHITE, 800, a=fade(t, 0))
        k = ease(seg(t, L[1], L[2] + 2))
        px, py = line_chart(c, (150, 120, 1150, 530), M_X, M_Y, (2026.0, M_X[-1] + 0.03), (5, 8), k, CORAL,
                            yticks=(5, 6, 7, 8), yfmt='{:.0f}%', a=fade(t, 0.1), width=4)
        for i, mth in enumerate(('Jan', 'Mar', 'May', 'Jul', 'Sep', 'Nov')):
            c.text(px(2026 + 2 * i / 12 + 0.04), 552, mth, 16, MUTED, 600, a=fade(t, 0.1), shadow=False)
        for xx, v, lab, col, at in ((M_X[M_Y.index(M_LOW)], M_LOW, pct(M_LOW), MINT, L[1] + 1),
                                    (M_X[M_Y.index(M_PEAK)], M_PEAK, pct(M_PEAK), CORAL, L[1] + 4),
                                    (M_X[-1], M_NOW, 'now ' + pct(M_NOW), GOLD, L[1] + 6)):
            kk = pop(t, at)
            if kk > 0:
                c.circle(px(xx), py(v), 9 * kk, col, WHITE, 2)
                bx = min(max(px(xx), 230), 1060)
                c.rrect(bx - 75, py(v) - 64, bx + 75, py(v) - 26, 14, col, a=clamp(kk))
                c.text(bx, py(v) - 45, lab, 20, INK, 800, a=clamp(kk), shadow=False)
        if t > L[3]:
            chip(c, 640, 600, 'Owners keep low rates = fewer homes for sale', MINT, pop(t, L[3] + 0.3), 22)
        elif t > L[2]:
            chip(c, 640, 600, f'$300,000 loan: ${PAY_LOW:,.0f} vs ${PAY_NOW:,.0f} a month', GOLD,
                 pop(t, L[2] + 0.5), 22)
        source(c, t, 'Freddie Mac (MORTGAGE30US) via FRED') if t < L[2] else None
        return
    specks(c, t, 57)
    c.icon('car-front', 640, 300, 200, SKY, a=fade(t, L[4]))
    chip(c, 640, 480, f'4-year new car loan: {pct(AUTO_NOW)}', SKY, pop(t, L[4] + 0.5), 28)
    source(c, t, 'Federal Reserve (TERMCBAUTO48NS) via FRED')


def s_savings(c, x):
    t, L = x.t, x.L
    specks(c, t, 58)
    c.icon('piggy-bank', 250, 330, 200, MINT, a=fade(t, 0))
    if t > L[1]:
        dial(c, 640, 380, 140, S_NOW, 5, f'avg savings: {pct(S_NOW)}', a=fade(t, L[1]), color=MINT)
        dial(c, 1000, 380, 140, CPI_NOW, 5, f'inflation: {CPI_NOW:.1f}%', a=fade(t, L[1] + 1.5), color=CORAL)
    if t > L[2] and t < L[4]:
        chip(c, 820, 140, f'losing about {REAL_LOSS:.1f}% a year', CORAL, pop(t, L[2] + 0.3), 24)
    if t > L[4]:
        k = pop(t, L[4] + 0.5)
        c.rrect(480, 120, 1180, 200, 18, (14, 22, 40, 230), GOLD, 3, a=clamp(k))
        c.text(830, 160, f'$10,000: ${EF_NOW:.0f}/yr at {pct(S_NOW)}  vs  ${EF_ALT:.0f}/yr at 3.5%', 24, WHITE, 900,
               a=clamp(k))
    if t > L[5]:
        chip(c, 250, 520, 'CD: lock in a rate', GOLD, pop(t, L[5] + 0.3), 20)
    source(c, t, 'FDIC national savings rate (SNDR), BLS CPI via FRED')


def s_checklist(c, x):
    t, L = x.t, x.L
    specks(c, t, 59)
    c.text(640, 80, 'Your rate-hike checklist', 38, WHITE, 900, a=fade(t, 0))
    items = (('credit-card', 'Pay down the\nhighest rate first'), ('phone', 'Ask for a\nlower rate'),
             ('piggy-bank', 'Make savings\nearn more'), ('search', 'Compare 3+\nlenders'))
    icon_row(c, t, items, L[1] - 0.3, x.E[-1] - L[1], y=300)
    if t > x.E[-1] - 1:
        chip(c, 640, 590, 'Education only - not financial advice', MUTED, pop(t, x.E[-1] - 0.7), 18)


def s_next(c, x):
    t, L = x.t, x.L
    specks(c, t, 60)
    c.text(640, 80, 'Will the Fed raise rates again?', 34, WHITE, 900, a=fade(t, 0))
    for i, (lab, ic, col, at) in enumerate((('Ships move, oil falls', 'trending-down', MINT, L[1]),
                                            ('Oil stays above $100', 'trending-up', CORAL, L[2]))):
        k = pop(t, at + 0.3)
        if k <= 0:
            continue
        cx = 360 + i * 560
        c.rrect(cx - 230, 170, cx + 230, 500, 24, (255, 255, 255, 16), col, 3, a=clamp(k))
        c.icon(ic, cx, 290, 110 * k, col, stroke=3)
        c.text(cx, 400, lab, 26, WHITE, 900, a=clamp(k))
        c.text(cx, 445, 'fewer hikes' if i == 0 else 'more hikes possible', 22, col, 800, a=clamp(k))
    if t > L[4]:
        chip(c, 640, 590, 'Next Fed meeting: December', GOLD, pop(t, L[4] + 0.3), 22)


def s_outro(c, x):
    t, L = x.t, x.L
    specks(c, t, 61, 50)
    penny(c, 260, 380, 76, t, 'happy', look=(1, 0), talk=x.talk(), wave=t > x.E[-1])
    if t < L[2]:
        fed_building(c, 820, 480, 0.9, a=fade(t, 0.2))
    if t > L[2]:
        k = ease_out(seg(t, L[2], L[2] + 0.6))
        c.text(400, 560, 'COIN THEORY', 30, GOLD, 900, anchor='lm', a=k)
        c.text(400, 595, 'money, explained with real data', 18, MUTED, 600, anchor='lm', a=k)
    if t > x.E[-1]:
        c.rrect(560, 150, 1200, 510, 20, (255, 255, 255, 10), (255, 255, 255, 40), 2, a=fade(t, x.E[-1], 0.8))


SCENES = [
    dict(draw=s_hook, chapter='Intro: the first hike since 2023', cam=(1.0, 1.05), lines=[
        "On September 17, the Federal Reserve did something it hadn't done in more than three years. It raised "
        "interest rates.",
        "Then in October, it held them there, and two officials voted to raise them again.",
        "If you have a credit card, a car loan, a mortgage, or even just a savings account, this affects you. "
        "Here's exactly how.",
    ], sfx=lambda L: [(L[0] + 2.5, 'pop'), (L[2] + 1, 'pop')]),
    dict(draw=s_title, lines=[], min=3.2, captions=False, trans='fadeblack', sfx=lambda L: [(0.2, 'ding')]),
    dict(draw=s_what, chapter='What the Fed actually controls', trans='fadeblack', lines=[
        "First, what does the Fed actually control? It's not your mortgage rate, and it's not your credit card "
        "rate. At least, not directly.",
        "It sets a target for the federal funds rate. That's the interest rate banks charge each other for "
        "overnight loans.",
        f"Right now, that target is {pct(NOW_L)} to {pct(NOW_U)}.",
        "When banks pay more to borrow, they charge you more to borrow. That's how one number ripples through the "
        "whole economy.",
        "Congress gave the Fed two jobs: keep prices stable, and keep as many people working as possible. "
        "Economists call it the dual mandate, and those two jobs sometimes pull in opposite directions.",
    ], sfx=lambda L: [(L[0] + 2.5, 'down'), (L[2] + 0.3, 'pop')]),
    dict(draw=s_history, chapter='The rollercoaster since 2022', cam=(1.0, 1.04), lines=[
        "Here's where that rate has been over the last ten years.",
        f"In early 2022, it was close to zero. Then inflation took off, and the Fed raised rates {N_HIKES} times "
        f"in about a year and a half, up to {pct(PEAK_U)}.",
        f"Once inflation cooled, it started cutting, in 2024 and 2025, down to a range of {pct(LOW_L)} to "
        f"{pct(LOW_U)}.",
        "Then, in September 2026, it turned around and raised rates again.",
    ], sfx=lambda L: [(L[1] + 2, 'pop'), (L[2] + 1, 'pop'), (L[3] + 0.5, 'ding')]),
    dict(draw=s_why, chapter='Why raise rates now?', lines=[
        "So why now? In one word: oil.",
        "After the war with Iran stopped tankers in the Strait of Hormuz, gas and diesel prices soared. We "
        "broke that down in our last video.",
        f"Inflation climbed from about {CPI_FEB:.1f}% in February to {CPI_NOW:.1f}% in September, almost double "
        "the Fed's 2% target.",
        "The Fed's job is to keep prices stable, and its main tool is interest rates. Higher rates make borrowing "
        "more expensive, so people and businesses spend a little less, and that cools prices down.",
        "But there's a catch. The Fed can't pump more oil, and higher rates can't reopen a shipping lane. They can "
        "only slow spending, so a fuel shock doesn't turn into higher prices for everything.",
    ], sfx=lambda L: [(L[2] + 0.3, 'pop'), (L[4] + 1, 'down')]),
    dict(draw=s_70s, chapter='Why not just keep rates low?', cam=(1.0, 1.04), lines=[
        "You might wonder: why doesn't the Fed just keep rates low and make life easier?",
        "Because if inflation gets stuck, everyone's paycheck buys a little less every single year.",
        f"That's what happened in the 1970s. Inflation hit about {INF_70S:.0f}% in 1980, and the Fed had to push "
        f"this rate to about {FF_PEAK:.0f}% in 1981 to break it, which helped cause a deep recession.",
        "Small, early steps today are meant to avoid ever needing medicine that strong again.",
    ], sfx=lambda L: [(L[2] + 0.5, 'pop'), (L[3] + 0.3, 'ding')]),
    dict(draw=s_vote, chapter='A split decision', lines=[
        "At its meeting on October 28, the Fed held rates steady. But the vote was 10 to 2, and both officials "
        "who disagreed wanted another hike.",
        "Twelve people vote on rates: the seven Fed governors in Washington, the president of the New York Fed, "
        "and four of the other regional Fed presidents, who take turns.",
        "That shows the debate inside the Fed right now. Some worry inflation is getting stuck. Others worry about "
        "slowing the economy too much.",
        f"So far, the job market is holding up. Unemployment was {U_NOW}% in September.",
    ], sfx=lambda L: [(L[0] + 3.5, 'pop'), (L[3] + 0.3, 'pop')]),
    dict(draw=s_fixed, chapter='Does this change your payment?', lines=[
        "Before we go through your bills, one important point. If your mortgage or car loan has a fixed rate, "
        "this hike doesn't change your payment at all.",
        "It matters for new loans, and for anything with a variable rate: credit cards, home equity lines of "
        "credit, and adjustable rate mortgages. Those can go up within a month or two.",
    ], sfx=lambda L: [(L[0] + 1.5, 'pop'), (L[1], 'pop')]),
    dict(draw=s_cards, chapter='Your credit card', lines=[
        "Now, what does this mean for you? Let's start with the most expensive debt most people have: credit "
        "cards.",
        "Most credit cards have variable rates tied to the prime rate, which moves almost one for one with the "
        "Fed.",
        f"The prime rate is now {pct(P_NOW)}, and the average interest rate on credit card accounts at banks is "
        f"about {CC_NOW:.1f}%.",
        f"If you carry a $5,000 balance at that rate, you'd pay about ${round(CC_COST, -1):,.0f} a year in "
        "interest.",
        f"This hike itself added a quarter of a percentage point. On that same $5,000, that's only about "
        f"${QUARTER:.2f} more a year. The real problem is the 21% itself.",
        "That's why paying down card debt is one of the best guaranteed returns you can get. Every dollar you "
        "pay off stops costing you over 21% a year.",
    ], sfx=lambda L: [(L[2] + 0.5, 'pop'), (L[3] + 0.3, 'down')]),
    dict(draw=s_mortgage, chapter='Mortgages and car loans', cam=(1.0, 1.04), lines=[
        "Mortgage rates don't follow the Fed directly. They follow what investors expect for inflation and "
        "interest rates over the next several years.",
        f"In late February, the 30 year mortgage rate was about {pct(M_LOW)}. As oil and inflation jumped, it "
        f"climbed as high as {pct(M_PEAK)} in October. This week, it's about {pct(M_NOW)}.",
        f"On a $300,000 loan, that's the difference between about ${PAY_LOW:,.0f} and ${PAY_NOW:,.0f} a month, "
        f"or about ${(PAY_NOW - PAY_LOW) * 12:,.0f} more every year.",
        "Higher rates also keep many homeowners from selling, because they don't want to give up the low rate "
        "they already have. That means fewer homes for sale.",
        f"Car loans are pricier too. The average rate on a four year new car loan from a bank is about "
        f"{pct(AUTO_NOW)}.",
    ], sfx=lambda L: [(L[1] + 1, 'pop'), (L[1] + 4, 'pop'), (L[2] + 0.5, 'ding')]),
    dict(draw=s_savings, chapter='Your savings', lines=[
        "Higher rates do have a bright side. Savers can earn more, but only if they go looking.",
        f"According to the FDIC, the national average rate on savings accounts is just {pct(S_NOW)}.",
        f"With inflation at {CPI_NOW:.1f}%, money sitting there loses about {REAL_LOSS:.1f}% of its buying "
        "power every year.",
        "Many online banks pay savings rates much closer to the Fed's rate. As long as the bank is FDIC insured, "
        "your deposits are protected up to $250,000.",
        f"On a $10,000 emergency fund, {pct(S_NOW)} earns you about ${EF_NOW:.0f} a year. An account paying 3.5% "
        f"would earn about ${EF_ALT:.0f}.",
        "And if you won't need some money for a while, a certificate of deposit, or CD, can lock in today's "
        "higher rate for months or even years.",
    ], sfx=lambda L: [(L[1] + 0.3, 'pop'), (L[2] + 0.3, 'down'), (L[4] + 0.5, 'ding')]),
    dict(draw=s_checklist, chapter='Your rate-hike checklist', lines=[
        "So here's a simple checklist.",
        "One: pay down variable rate debt first, starting with whatever charges the highest rate.",
        "Two: if you carry a card balance, call your card company and ask for a lower rate. It works more often "
        "than you'd think.",
        "Three: make sure your savings are actually earning something.",
        "And four: if you're buying a home or a car, compare at least three lenders. A small difference in rate "
        "can add up to thousands of dollars.",
        "And five: don't panic. Rates move slowly, and you have time to make a plan.",
    ]),
    dict(draw=s_next, chapter='What happens next?', lines=[
        "So, will the Fed raise rates again? It mostly depends on oil.",
        "If shipping through Hormuz recovers and energy prices fall, inflation could cool, and the Fed may not "
        "need to hike again.",
        "If oil stays above $100 and higher prices keep spreading, more hikes are possible.",
        "Watch the monthly inflation report. If energy prices keep easing, that's a sign the pressure is fading.",
        "The Fed meets again in December, and we'll break it down when it does.",
    ], sfx=lambda L: [(L[1] + 0.3, 'pop'), (L[2] + 0.3, 'pop')]),
    dict(draw=s_outro, chapter='Recap', tail=12, cam=(1.0, 1.02), lines=[
        "So the Fed raised rates to fight inflation caused by an oil shock. It can't fix the oil, but it can make "
        "borrowing more expensive, and that touches almost every part of your financial life.",
        "Pay down expensive debt, make your savings work for you, and compare before you borrow.",
        "Next time: how banks create money out of thin air. Subscribe to Coin Theory so you don't miss it.",
    ], sfx=lambda L: [(L[2], 'pop')]),
]

SHORTS = {
    'ep04_short_cards': [SCENES[8], end_card("What else the rate hike changes? Full story on Coin Theory.")],
    'ep04_short_savings': [SCENES[10], end_card("Here's everything the rate hike changes. Full story on Coin "
                                               "Theory.")],
    'ep04_short_why': [SCENES[4], end_card("What it means for your money? Watch the full story on Coin Theory.")],
}


def check_numbers():
    script = ' '.join(l for sc in SCENES for l in sc['lines'])
    assert HIKE_DAY.strftime('%Y-%m-%d') == '2026-09-17' and 'September 17' in script
    assert (HIKE_DAY - LAST_HIKE_BEFORE).days > 3 * 365 and LAST_HIKE_BEFORE.year == 2023
    assert 'more than three years' in script
    assert UP.loc['2026-10-28'] == NOW_U == 4.0 and NOW_L == 3.75
    assert UP['2022-01-03'] == 0.25 and N_HIKES == 11 and PEAK_U == 5.5, (N_HIKES, PEAK_U)
    assert UP['2024-01-01':'2025-12-31'].diff().max() <= 0 and LOW_U == 3.75 and LOW_L == 3.5
    assert 1.7 <= CPI_NOW / 2 < 2 and 'almost double' in script, CPI_NOW
    assert LAST.month == 9 and 'in September' in script
    assert P_NOW == NOW_U + 3, P_NOW
    assert CC_NOW > 21 and 'over 21%' in script and CC.index[-1].year == 2026
    assert M_LOW_AT.month == 2 and M_LOW_AT.day > 20 and M_PEAK_AT.month == 10 and MORT.index[-1].month == 10
    assert 3.5 < NOW_L and 'October 28' in script and '10 to 2' in script
    assert UNRATE.index[-1].month == 9
    assert FF_PEAK_AT.year == 1981 and 18.5 < FF_PEAK < 19.5 and INF_70S_AT.year == 1980 and 14 < INF_70S < 15
    assert NOW_U - UP['2026-09-16'] == 0.25 and 'a quarter of a percentage point' in script
    print('numbers check: OK')
    print(f'  hikes {N_HIKES} peak {PEAK_U} low {LOW_L}-{LOW_U} now {NOW_L}-{NOW_U}; cpi {CPI_FEB:.2f}->{CPI_NOW:.2f};'
          f' prime {P_NOW} cc {CC_NOW} cost {CC_COST:.0f}; mort {M_LOW}({M_LOW_AT.date()}) {M_PEAK}({M_PEAK_AT.date()}) '
          f'{M_NOW}; pay {PAY_LOW:.0f}->{PAY_NOW:.0f}; auto {AUTO_NOW}; save {S_NOW} loss {REAL_LOSS:.2f}; u {U_NOW}')


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
        total, chapters = build(SCENES, os.path.join(OUT, 'ep04_fed.mp4'), BUILD,
                                srt_path=os.path.join(OUT, 'ep04_fed.en.srt'))
        with open(os.path.join(OUT, 'ep04_chapters.txt'), 'w') as f:
            for at, name in chapters:
                f.write(f'{fmt_time(at)} {name}\n')
        print(open(os.path.join(OUT, 'ep04_chapters.txt')).read())
    if '--no-short' not in sys.argv:
        for name, scenes in SHORTS.items():
            build(scenes, os.path.join(OUT, f'{name}.mp4'), os.path.join(BUILD, name), layout='short')
