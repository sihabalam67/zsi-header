"""Episode 8: Stocks after midterm elections (long video, Mon Nov 2 2026) + data for its Short.

    python3 channel/ep08_midterms.py [--stills] [--no-short]

Data: Robert Shiller's monthly S&P 500 (Yale, channel/data/shiller_ie_data.xls), price only, monthly averages.
Window: October of each midterm year (the month before the vote) to October one year later. The dataset ends in
September 2023, so 2022 is measured to September 2023 and said so. Flow clips: assets/flow/ep08 (owner, Google
Flow). check_numbers() refuses to render if the narration disagrees with the data.
"""
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pandas as pd  # noqa: E402
from wk2_art import *  # noqa: E402,F401,F403
from engine import build, previews, line_chart  # noqa: E402

OUT = os.path.join(HERE, 'out')
BUILD = os.path.join(HERE, 'build', 'ep08')
FLOW = os.path.join(HERE, 'assets', 'flow', 'ep08')

_x = pd.read_excel(os.path.join(HERE, 'data', 'shiller_ie_data.xls'), sheet_name='Data', header=None)
_d = _x.iloc[8:, [0, 1]].copy()
_d.columns = ['date', 'P']
_d = _d[pd.to_numeric(_d['date'], errors='coerce').notna()]
_d['date'] = _d['date'].astype(float)
_d['P'] = pd.to_numeric(_d['P'], errors='coerce')
_d = _d.dropna()
P = {(int(v), round((v - int(v)) * 100)): p for v, p in zip(_d['date'], _d['P'])}
LAST = max(P)

MIDS = list(range(1950, 2019, 4))                     # midterms with a full year of data after them
MID = [(y, (P[(y + 1, 10)] / P[(y, 10)] - 1) * 100) for y in MIDS]
OTHER = [(P[(y + 1, 10)] / P[(y, 10)] - 1) * 100 for y in range(1950, 2022) if y % 4 != 2]
AVG = statistics.mean(r for _, r in MID)
MIN_Y, MIN_R = min(MID, key=lambda m: m[1])
MAX_Y, MAX_R = max(MID, key=lambda m: m[1])
OTHER_AVG = statistics.mean(OTHER)
OTHER_NEG = sum(r < 0 for r in OTHER)
SLUMP = [(P[(y, 10)] / P[(y, 1)] - 1) * 100 for y in range(1950, 2023, 4)]
SLUMP_AVG = statistics.mean(SLUMP)
SLUMP_NEG = sum(r < 0 for r in SLUMP)
Y22_SLUMP = (P[(2022, 10)] / P[(2022, 1)] - 1) * 100
Y22_REBOUND = (P[LAST] / P[(2022, 10)] - 1) * 100
PATH22 = [(2022 + (m - 1) / 12, P[(2022, m)]) for m in range(1, 13)] + \
         [(2023 + (m - 1) / 12, P[(2023, m)]) for m in range(1, LAST[1] + 1)]
NOVNOV_1986 = (P[(1987, 11)] / P[(1986, 11)] - 1) * 100
SRC = 'S&P 500 monthly, Robert Shiller (Yale); price only'

# 2026 context, from our own sourced episodes
sys.argv, _argv = [sys.argv[0]], sys.argv
import ep03_gas as GAS  # noqa: E402
import ep04_fed as FED  # noqa: E402
from ep07_binance import F as HACK  # noqa: E402
sys.argv = _argv


def bars18(c, t, start, span, box=(110, 150, 1170, 520), labels=True, k_all=None):
    """The 18 green bars, one per midterm, growing one after another."""
    x0, y0, x1, y1 = box
    n = len(MID)
    bw = (x1 - x0) / n
    c.line([(x0, y1), (x1, y1)], (255, 255, 255, 90), 2)
    for i, (y, r) in enumerate(MID):
        g = 1 if k_all else ease(seg(t, start + span * i / n, start + span * i / n + 0.5))
        if g <= 0:
            continue
        h = (y1 - y0) * r / 35 * g
        c.rrect(x0 + i * bw + bw * 0.15, y1 - h, x0 + (i + 1) * bw - bw * 0.15, y1, 6, MINT)
        if labels:
            c.text(x0 + (i + 0.5) * bw, y1 + 22, f"'{y % 100:02d}", 19, MUTED, 800, shadow=False)


# --------------------------------------------------------------------- scenes --
def s_hook(c, x):
    t, L = x.t, x.L
    k = pop(t, L[0] + 0.2)
    if k > 0:
        c.text(640, 330, '18 / 18', int(150 * (0.6 + 0.4 * clamp(k))), GOLD, 900, a=clamp(k), stroke=9)
    if t > L[1] + 1.0:
        k2 = pop(t, L[1] + 1.0)
        c.rrect(370, 420, 910, 480, 30, MINT, a=clamp(k2))
        c.text(640, 450, 'stocks higher a year after every midterm', 24, INK, 900, a=clamp(k2), shadow=False)


def s_every(c, x):
    t, L = x.t, x.L
    specks(c, t, 81)
    for i in range(18):  # 18 ticks lighting up
        k = pop(t, L[0] + 0.1 * i)
        cx, cy = 190 + (i % 9) * 112, 170 + (i // 9) * 120
        if k > 0:
            c.circle(cx, cy, 42 * k, MINT, WHITE, 3)
            c.icon('check', cx, cy, 46 * k, INK, stroke=3)
    k = pop(t, L[1] + 0.6)
    if k > 0:
        c.text(640, 430, f'+{AVG:.0f}%', int(110 * (0.6 + 0.4 * clamp(k))), GOLD, 900, a=clamp(k), stroke=6)
        c.text(640, 505, 'average gain in the year after', 26, WHITE, 800, a=clamp(k))
    if t > L[2]:
        chip(c, 640, 580, 'Election Day: Tuesday, November 3', CORAL, pop(t, L[2] + 0.3), 24)
    penny(c, 1150, 560, 55, t, 'shocked' if t > L[1] else 'happy', look=(-1, 0), talk=x.talk())


def s_what(c, x):
    t, L = x.t, x.L
    specks(c, t, 82)
    c.text(640, 80, 'What is a midterm?', 40, WHITE, 900, a=fade(t, 0))
    k = pop(t, L[0] + 1.0)
    if k > 0:
        c.icon('landmark', 330, 280, 150 * k, GOLD)
        c.text(330, 410, 'House: all 435 seats', 30, WHITE, 900, a=clamp(k))
        c.text(950, 410, 'Senate: about 1 in 3', 30, WHITE, 900, a=fade(t, L[0] + 2.2))
        c.icon('landmark', 950, 280, 150 * clamp(pop(t, L[0] + 2.2)), SKY)
    if t > L[1]:
        chip(c, 640, 500, "halfway through the president's term", GOLD, pop(t, L[1] + 0.3), 24)
    if t > L[2]:
        chip(c, 640, 570, 'Congress controls taxes and spending', MINT, pop(t, L[2] + 0.3), 24)


def s_chart(c, x):
    t, L = x.t, x.L
    c.text(640, 60, 'S&P 500, one year after each midterm (Oct to Oct)', 28, WHITE, 800, a=fade(t, 0))
    bars18(c, t, L[1], max(2.0, L[3] - L[1]))
    yl = 520 - 370 * AVG / 35
    if t > L[4]:
        k = fade(t, L[4])
        c.line([(110, yl), (1170, yl)], (255, 255, 255, int(200 * k)), 3)
        c.text(1160, yl - 22, f'average +{AVG:.1f}%', 22, GOLD, 900, anchor='rm', a=k)
    if t > L[2]:
        chip(c, 640, 590, f'{MAX_Y}: +{MAX_R:.0f}%   {MIN_Y}: +{MIN_R:.0f}%', GOLD, pop(t, L[2] + 0.4), 22)
    if t > L[5]:
        chip(c, 640, 640, f'2022: +{Y22_REBOUND:.0f}% by Sept 2023 (data ends)', SKY, pop(t, L[5] + 0.4), 22)
    source(c, t, SRC)


def s_compare(c, x):
    t, L = x.t, x.L
    specks(c, t, 83)
    c.text(640, 70, 'The same 12 months: after midterms vs every other year', 28, WHITE, 800, a=fade(t, 0))
    compare_bars(c, t, (('every other year', OTHER_AVG, MUTED), ('after midterms', AVG, MINT)), L[0] + 0.5,
                 max(1.5, L[1] - L[0]), 22, lambda v: f'+{v:.1f}%', box=(250, 140, 1030, 470))
    if t > L[1]:
        c.text(400, 560, f'lost money: {OTHER_NEG} of {len(OTHER)} years', 26, CORAL, 900, a=fade(t, L[1] + 0.5))
        c.text(880, 560, f'lost money: 0 of {len(MID)}', 26, MINT, 900, a=fade(t, L[1] + 1.5))
    source(c, t, SRC)


def s_slump(c, x):
    t, L = x.t, x.L
    c.text(640, 60, 'The twist: the midterm year itself', 32, WHITE, 900, a=fade(t, 0))
    if t < L[2]:
        k = pop(t, L[0] + 2.5)
        if k > 0:
            c.text(640, 280, f'+{SLUMP_AVG:.1f}%', int(130 * (0.6 + 0.4 * clamp(k))), MUTED, 900, a=clamp(k),
                   stroke=6)
            c.text(640, 370, 'average, January to October of midterm years', 26, WHITE, 800, a=clamp(k))
        if t > L[1]:
            chip(c, 640, 470, f'stocks fell in {SLUMP_NEG} of the last {len(SLUMP)}', CORAL, pop(t, L[1] + 1.5), 26)
        return
    xs, ys = [p[0] for p in PATH22], [p[1] for p in PATH22]
    k = ease(seg(t, L[2], L[2] + 3.5))
    px, py = line_chart(c, (150, 130, 1150, 520), xs, ys, (2022, xs[-1] + 0.05), (3000, 5000), k, GOLD,
                        yticks=range(3000, 5001, 500), yfmt='{:,.0f}', a=fade(t, L[2]))
    for i, mlab in enumerate(('Jan 2022', 'Jul 2022', 'Jan 2023', 'Jul 2023')):
        c.text(px(2022 + i * 0.5), 548, mlab, 18, MUTED, 600, a=fade(t, L[2]), shadow=False)
    ex = 2022 + 10 / 12
    if k > 0.45:
        c.line([(px(ex), 130), (px(ex), 520)], (255, 255, 255, 120), 2)
        c.text(px(ex), 115, 'the vote', 20, WHITE, 900)
    if t > L[2] + 1.5:
        chip(c, px(2022.4), 470, f'{Y22_SLUMP:.1f}% by October', CORAL, pop(t, L[2] + 1.5), 22)
    if t > L[2] + 3.6:
        chip(c, px(2023.3), 200, f'+{Y22_REBOUND:.0f}% after', MINT, pop(t, L[2] + 3.6), 22)
    source(c, t, SRC)


def s_rebound(c, x):
    t, L = x.t, x.L
    k = pop(t, 1.2)
    if k > 0:
        c.text(640, 120, 'SLUMP BEFORE THE VOTE.', int(56 * (0.6 + 0.4 * clamp(k))), WHITE, 900, a=clamp(k), stroke=6)
    k2 = pop(t, 2.6)
    if k2 > 0:
        c.text(640, 200, 'REBOUND AFTER.', int(72 * (0.6 + 0.4 * clamp(k2))), MINT, 900, a=clamp(k2), stroke=6)


def s_reason1(c, x):
    t, L = x.t, x.L
    k = pop(t, 0.6)
    if k > 0:
        c.rrect(60, 60, 600, 150, 24, (14, 22, 40, 210), GOLD, 3, a=clamp(k))
        c.text(330, 105, '1  UNCERTAINTY ENDS', 38, GOLD, 900, a=clamp(k))


def s_reasons23(c, x):
    t, L = x.t, x.L
    specks(c, t, 84)
    c.text(640, 70, 'Why it happens: three explanations', 34, WHITE, 900, a=fade(t, 0))
    items = [('check', '1  Uncertainty ends', MUTED, 0), ('scale', '2  Gridlock', GOLD, L[0] + 0.3),
             ('calendar', '3  The next election', GOLD, L[1] + 0.3)]
    for i, (ic, lab, col, at) in enumerate(items):
        k = pop(t, at) if at else 1
        if k <= 0:
            continue
        cx = 240 + i * 400
        c.circle(cx, 290, 95 * k, (255, 255, 255, 18), col, 3)
        c.icon(ic, cx, 290, 90 * k, col)
        c.text(cx, 430, lab, 28, WHITE, 900, a=clamp(k))
    if t > L[0] and t < L[1]:
        c.text(640, 520, 'split control = fewer big surprises', 26, MUTED, 800, a=fade(t, L[0] + 1.2))
    if t > L[1]:
        c.text(640, 520, 'governments push for growth before a presidential election', 26, MUTED, 800,
               a=fade(t, L[1] + 1.2))
    if t > L[2]:
        chip(c, 640, 600, 'explanations, not laws of nature', CORAL, pop(t, L[2] + 0.3), 24)


def s_fine(c, x):
    t, L = x.t, x.L
    specks(c, t, 85)
    c.text(640, 70, 'The fine print', 40, WHITE, 900, a=fade(t, 0))
    rows = [('coins', f'{len(MID)} is a small sample', L[1] + 0.3),
            ('ruler', 'Nov to Nov: 1986 was flat (about 0%)', L[2] + 0.3),
            ('percent', 'prices only: dividends add a bit more', L[3] + 0.3)]
    for i, (ic, lab, at) in enumerate(rows):
        k = pop(t, at)
        if k <= 0:
            continue
        y = 190 + i * 130
        c.circle(260, y, 50 * k, (255, 255, 255, 18), GOLD, 3)
        c.icon(ic, 260, y, 52 * k, GOLD)
        c.text(340, y, lab, 32, WHITE, 900, anchor='lm', a=clamp(k))
    penny(c, 1120, 560, 60, t, 'worried', look=(-1, 0), talk=x.talk())


def s_risks(c, x):
    t, L = x.t, x.L
    specks(c, t, 86)
    c.text(640, 70, 'Why 2026 is different', 40, WHITE, 900, a=fade(t, 0))
    cards = [('trending-up', f'inflation {FED.CPI_NOW:.1f}%', CORAL, L[0] + 0.5),
             ('landmark', 'Fed raised rates', GOLD, L[1] + 0.3),
             ('fuel', f'gas {GAS.money(GAS.G_NOW)}', CORAL, L[2] + 0.2),
             ('shield-alert', f'${HACK["amount_bn"]}B crypto hack', CORAL, L[2] + 2.0)]
    for i, (ic, lab, col, at) in enumerate(cards):
        k = pop(t, at)
        if k <= 0:
            continue
        cx, cy = 340 + (i % 2) * 600, 220 + (i // 2) * 190
        c.rrect(cx - 250, cy - 70, cx + 250, cy + 70, 22, (255, 255, 255, 16), col, 3, a=clamp(k))
        c.icon(ic, cx - 170, cy, 70 * k, col)
        c.text(cx + 40, cy, lab, 32, WHITE, 900, a=clamp(k))
    if t > L[3]:
        chip(c, 640, 590, 'some analysts: stocks already look expensive', GOLD, pop(t, L[3] + 0.3), 24)
    if t > L[4]:
        chip(c, 640, 650, "history isn't a promise", CORAL, pop(t, L[4] + 0.3), 24)


def s_lessons(c, x):
    t, L = x.t, x.L
    specks(c, t, 87)
    c.text(640, 70, 'What the data teaches (not advice)', 36, WHITE, 900, a=fade(t, 0))
    items = [('users', 'Both parties held\nCongress in the streak'), ('triangle-alert', 'Election bets\nare risky'),
             ('trending-up', 'Inflation, rates, jobs\nmove your money most')]
    icon_row(c, t, items, L[1] - 0.3, max(1.5, L[3] - L[1]), y=300)


def s_end(c, x):
    t, L = x.t, x.L
    specks(c, t, 88)
    if t < L[1]:
        bars18(c, t, 0, 0, box=(200, 120, 1080, 420), labels=False, k_all=True)
        c.text(640, 500, f'+{AVG:.0f}% vs +{OTHER_AVG:.0f}%', 54, GOLD, 900, a=fade(t, 0.5))
        return
    k = pop(t, L[1] + 0.3)
    c.text(640, 260, '19 / 19 ?', int(150 * (0.6 + 0.4 * clamp(k))), GOLD, 900, a=clamp(k), stroke=8)
    c.text(640, 380, 'Tell me in the comments', 34, WHITE, 900, a=fade(t, L[1] + 1.0))
    penny(c, 640, 560, 70, t, 'happy', wave=True, talk=x.talk())


B18 = 'eighteen'
SCENES = [
    dict(draw=s_hook, chapter='Intro: 18 out of 18', bg_video=os.path.join(FLOW, 'clip3.mp4'), bg_speed=0.85,
         lead=0.3, gap=0.3, tail=0.4, lines=[
             "!Eighteen out of eighteen.",
             "Since 1950, there have been eighteen midterm elections we can measure. In the year after every single "
             "one, the stock market went up.",
         ], punch=lambda L: [L[0] + 0.2, L[1] + 1.0], sfx=lambda L: [(L[0] + 0.2, 'ding'), (L[1] + 1.0, 'pop')]),
    dict(draw=s_every, lines=[
        "Not most of the time. Every time.",
        f"On average, the market gained about {AVG:.0f}% in those twelve months.",
        "And on Tuesday, America votes again. So does the streak continue? And what does it actually mean for your "
        "money? Let's look at the data.",
    ], punch=lambda L: [L[1] + 0.6], sfx=lambda L: [(L[0], 'whoosh'), (L[1] + 0.6, 'ding'), (L[2] + 0.3, 'pop')]),
    dict(draw=s_what, chapter='What is a midterm?', lines=[
        "First, what is a midterm? Every two years, Americans vote for all 435 seats in the House of Representatives, "
        "and about a third of the Senate.",
        "When that happens halfway through a president's four-year term, it's called a midterm, and it's often "
        "treated as a report card on the president.",
        "And Congress controls taxes and spending, so markets pay very close attention.",
    ], sfx=lambda L: [(L[0] + 1.0, 'pop'), (L[0] + 2.2, 'pop'), (L[1] + 0.3, 'pop'), (L[2] + 0.3, 'pop')]),
    dict(draw=s_chart, chapter='18 green bars', lines=[
        "Here's what the stock market actually did. We used Yale economist Robert Shiller's S&P 500 data, which "
        "goes back to 1871.",
        "For every midterm since 1950, we measured from October, right before the vote, to October one year later.",
        f"After {MAX_Y}, stocks rose {MAX_R:.0f}%. After {MIN_Y}, the weakest year, still up {MIN_R:.0f}%.",
        "!Eighteen elections. Eighteen green bars.",
        f"The average gain was about {AVG:.0f}%.",
        f"And 2022, the most recent midterm? Our data ends in late 2023, but by September 2023, the market was "
        f"already up about {Y22_REBOUND:.0f}% from October 2022.",
    ], punch=lambda L: [L[3] + 0.2], sfx=lambda L: [(L[1], 'whoosh'), (L[2] + 0.4, 'pop'), (L[3] + 0.2, 'ding'),
                                                    (L[4], 'pop'), (L[5] + 0.4, 'pop')]),
    dict(draw=s_compare, chapter='Normal years vs midterm years', lines=[
        "Is that unusual? Compare it with every other year since 1950.",
        f"In normal years, the same twelve months averaged about {OTHER_AVG:.0f}%, and the market lost money in "
        f"about one year out of three.",
        f"!After midterms? About three times the gain, and not a single losing year.",
    ], punch=lambda L: [L[2] + 0.3], sfx=lambda L: [(L[0] + 0.5, 'pop'), (L[1] + 0.5, 'down'), (L[2] + 0.3, 'ding')]),
    dict(draw=s_slump, chapter='The twist: the midterm slump', lines=[
        "But here's the twist. The midterm year itself is often bad.",
        f"From January to October of midterm years, stocks averaged almost nothing, about {SLUMP_AVG:.1f}%. They "
        f"fell in {SLUMP_NEG} of the last {len(SLUMP)}.",
        f"2022 is the perfect example. By October 2022, the S&P 500 was down about {abs(Y22_SLUMP):.1f}% for the "
        "year.",
    ], punch=lambda L: [L[0] + 2.5, L[2] + 1.5], sfx=lambda L: [(L[0] + 2.5, 'down'), (L[1] + 1.5, 'pop'),
                                                               (L[2], 'whoosh'), (L[2] + 1.5, 'down')]),
    dict(draw=s_rebound, bg_video=os.path.join(FLOW, 'clip4.mp4'), bg_speed=0.9, lead=0.3, gap=0.3, tail=0.5,
         lines=[
             "!Then the votes were counted, and stocks climbed right back.",
             "Slump before the vote. Rebound after.",
         ], punch=lambda L: [1.2, 2.6], sfx=lambda L: [(1.2, 'ding'), (2.6, 'ding')]),
    dict(draw=s_reason1, chapter='Why it happens', bg_video=os.path.join(FLOW, 'clip2.mp4'), bg_speed=0.6,
         lead=0.3, gap=0.3, tail=0.4, lines=[
             "So why does this happen? Nobody knows for sure, but analysts point to three main reasons.",
             "Reason one: uncertainty ends. Markets hate not knowing. Before an election, nobody knows who will "
             "control Congress. Once the votes are counted, the fog lifts, even if people don't like the result.",
         ], sfx=lambda L: [(0.6, 'pop')]),
    dict(draw=s_reasons23, lines=[
        "Reason two: gridlock. Midterms often split control of government, so big surprises get harder to pass. "
        "For markets, fewer surprises can be a good thing.",
        "Reason three: the next election. After a midterm, a presidential election is two years away, and "
        "governments have historically pushed for a strong economy heading into one.",
        "Remember, these are explanations, not laws of nature.",
    ], sfx=lambda L: [(L[0] + 0.3, 'pop'), (L[1] + 0.3, 'pop'), (L[2] + 0.3, 'down')]),
    dict(draw=s_fine, chapter='The fine print', lines=[
        "Now, before anyone bets the farm on this, here's the fine print.",
        "One: eighteen is a small number. Flip a coin eighteen times and strange streaks happen.",
        "Two: the exact numbers depend on how you measure. Measure November to November instead, and 1986 comes "
        "out roughly flat.",
        "Three: these are prices only. Dividends would add a bit more on top.",
    ], sfx=lambda L: [(L[1] + 0.3, 'pop'), (L[2] + 0.3, 'pop'), (L[3] + 0.3, 'pop')]),
    dict(draw=s_risks, chapter='Why 2026 is different', lines=[
        f"And 2026 has real risks of its own. Inflation is {FED.CPI_NOW:.1f}% and rising, mostly because of the oil "
        "shock after the war with Iran.",
        "The Fed just raised interest rates for the first time since 2023.",
        f"Gas is still around {GAS.money(GAS.G_NOW)} a gallon. And crypto just had the biggest hack in history.",
        "Some analysts also warn that stocks already look expensive compared with company profits.",
        "!History says the odds have been good. History doesn't promise anything.",
    ], punch=lambda L: [L[4] + 0.3], sfx=lambda L: [(L[0] + 0.5, 'pop'), (L[1] + 0.3, 'pop'), (L[2] + 0.2, 'pop'),
                                                    (L[2] + 2.0, 'down'), (L[3] + 0.3, 'pop'), (L[4] + 0.3, 'ding')]),
    dict(draw=s_lessons, chapter='What it means for you', lines=[
        "So what does this mean for you? We don't give financial advice, but the data teaches three useful lessons.",
        "One: both parties have controlled Congress during this streak. The pattern was never about who won.",
        "Two: big moves based on election predictions are risky. Anyone who sold in the 2022 slump missed the "
        "rebound.",
        "Three: what moves your money most is what we cover here every week: inflation, interest rates, and jobs.",
    ], sfx=lambda L: [(L[1], 'pop'), (L[2], 'pop'), (L[3], 'pop')]),
    dict(draw=s_end, chapter='Recap', lines=[
        f"Let's recap. Eighteen midterms. The market was higher a year later every time, about {AVG:.0f}% on "
        f"average, versus about {OTHER_AVG:.0f}% in other years. A slump before the vote, a rebound after.",
        "!So, will 2026 make it nineteen for nineteen? Tell me what you think in the comments, and subscribe, "
        "because a year from now, we'll come back and check.",
        "This video is for education only. It's not financial advice.",
    ], punch=lambda L: [L[1] + 0.3], sfx=lambda L: [(L[1] + 0.3, 'ding')]),
]
SHORTS = {}


def check_numbers():
    script = ' '.join(l for sc in SCENES for l in sc['lines'])
    assert len(MID) == 18 and all(r > 0 for _, r in MID), 'the streak must hold in the data'
    assert round(AVG) == 18 and round(OTHER_AVG) == 6 and 2.5 < AVG / OTHER_AVG < 3.6 and 'three times' in script
    assert (MAX_Y, round(MAX_R), MIN_Y, round(MIN_R)) == (1954, 31, 2010, 3)
    assert abs(OTHER_NEG / len(OTHER) - 1 / 3) < 0.03 and 'one year out of three' in script
    assert round(SLUMP_AVG, 1) == 0.3 and SLUMP_NEG == 9 and len(SLUMP) == 19
    assert round(Y22_SLUMP, 1) == -18.5 and round(Y22_REBOUND) == 21 and LAST == (2023, 9)
    assert abs(NOVNOV_1986) < 0.5 and 'roughly flat' in script
    assert round(FED.CPI_NOW, 1) == 3.7 and GAS.money(GAS.G_NOW) == '$4.27' and HACK['amount_bn'] == 6.3
    print('numbers check: OK')
    print(f'  avg {AVG:.1f} other {OTHER_AVG:.1f} ({OTHER_NEG}/{len(OTHER)} neg) slump {SLUMP_AVG:.2f} '
          f'({SLUMP_NEG}/{len(SLUMP)}) 2022 {Y22_SLUMP:.1f}/{Y22_REBOUND:.1f} 1986nov {NOVNOV_1986:.2f}')


if __name__ == '__main__':
    check_numbers()
    os.makedirs(BUILD, exist_ok=True)
    if '--stills' in sys.argv:
        previews(SCENES, SHORTS, os.path.join(BUILD, 'previews'))
        sys.exit()
    total, chapters = build(SCENES, os.path.join(OUT, 'ep08_midterms.mp4'), BUILD,
                            srt_path=os.path.join(OUT, 'ep08_midterms.en.srt'))
    with open(os.path.join(OUT, 'ep08_chapters.txt'), 'w') as f:
        for at, name in chapters:
            f.write(f'{fmt_time(at)} {name}\n')
    print(f'total {total / 60:.1f} min')
