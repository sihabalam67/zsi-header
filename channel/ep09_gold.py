"""Episode 9: Gold fell 23% from its record. What happened? (long video, Mon Nov 16 2026)

    python3 channel/ep09_gold.py [--stills] [--only 3,5]

Data (check_numbers recomputes everything; prices are COMEX gold futures, front month, daily closes):
- channel/data/GC_F.csv: Yahoo Finance chart API, symbol GC=F, saved Nov 8 2026 (last close Nov 6 2026).
- FRED: DFII10 (10-year TIPS real yield), DTWEXBGS (broad trade-weighted dollar index), DFEDTARU/DFEDTARL (Fed
  target range), CPIAUCSL (CPI).
- World Gold Council, Gold Demand Trends Q3 2026 press release (Nov 3 2026): central banks +321t (+42% y/y), ETFs
  +211t, ETF holdings record 4,256t, jewellery 313t (-17% y/y, weakest Q3 in the series), bar and coin 268t (-19%),
  Q3 average price $4,262/oz (LBMA PM).
- Jan 30 2026: President Trump named Kevin Warsh as his pick for Fed chair (reported by NBC News, CNBC, Fox News);
  analysts called the run-up speculative and the news the trigger (Axios, CNBC). We only state what the data shows.
Photos: channel/assets/photos/ep09 (CC0 / public domain, Wikimedia Commons, logged in SOURCES.md).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pandas as pd  # noqa: E402
from wk2_art import *  # noqa: E402,F401,F403
from engine import build, previews  # noqa: E402
import fx  # noqa: E402
from ep06_banks import head, pulse  # noqa: E402

OUT = os.path.join(HERE, 'out')
BUILD = os.path.join(HERE, 'build', 'ep09_gold')
PH = os.path.join(HERE, 'assets', 'photos', 'ep09')
BARS, BULLION, KNOX = (os.path.join(PH, f) for f in ('bars.jpg', 'bullion.jpg', 'vault.jpg'))
FULL = (0, 0, W, H)
GOLDC = (240, 190, 70)

G = pd.read_csv(os.path.join(HERE, 'data', 'GC_F.csv'), parse_dates=['date']).set_index('date')['close']
REC, REC_DATE = G.max(), G.idxmax()
NOW, NOW_DATE = G.iloc[-1], G.index[-1]
DROP = (NOW / REC - 1) * 100
LOW_AFTER = G[G.index > REC_DATE]
LOW, LOW_DATE = LOW_AFTER.min(), LOW_AFTER.idxmin()
LOW_DROP = (LOW / REC - 1) * 100
START, START_DATE = G.iloc[0], G.index[0]
TIMES = NOW / START
YAGO = G[:NOW_DATE - pd.Timedelta(days=365)].iloc[-1]
Y1 = (NOW / YAGO - 1) * 100
Y2025 = (G[:'2025-12-31'].iloc[-1] / G[:'2024-12-31'].iloc[-1] - 1) * 100
FIRST = {k: G[G > k].index[0] for k in (2000, 3000, 4000, 5000)}
DAY = G.pct_change()
CRASH, CRASH_DATE = DAY.min() * 100, DAY.idxmin()
MAR = DAY['2026-03'].min() * 100, DAY['2026-03'].idxmin()

RY = series('DFII10')
DXY = series('DTWEXBGS')
FEDU, FEDL = series('DFEDTARU'), series('DFEDTARL')
CPI = series('CPIAUCSL')
RY_REC, RY_NOW, RY_DATE = RY[:REC_DATE].iloc[-1], RY.iloc[-1], RY.index[-1]
DX_REC, DX_NOW, DX_DATE = DXY[:REC_DATE].iloc[-1], DXY.iloc[-1], DXY.index[-1]
DX_UP = (DX_NOW / DX_REC - 1) * 100
DX_2025 = (DXY[:'2025-12-31'].iloc[-1] / DXY[:'2025-01-02'].iloc[-1] - 1) * 100
DX_CRASH = (DXY[:CRASH_DATE].iloc[-1] / DXY[:CRASH_DATE - pd.Timedelta(days=1)].iloc[-1] - 1) * 100
HIKES = FEDU[FEDU.diff() > 0]
CUTS25 = FEDU['2025'][FEDU['2025'].diff() < 0]
HIKE26 = HIKES['2026'].index[0]
PREV_HIKE = HIKES[HIKES.index < HIKE26].index[-1]
INFL = (CPI.iloc[-1] / CPI.iloc[-13] - 1) * 100
GM = pd.read_csv(os.path.join(HERE, 'data', 'GC_F_max.csv'), parse_dates=['date']).set_index('date')['close']
P11, P11_DATE = GM['2011'].max(), GM['2011'].idxmax()
L15, L15_DATE = GM['2012':'2016'].min(), GM['2012':'2016'].idxmin()
BUST = (L15 / P11 - 1) * 100
BACK = GM[(GM.index > L15_DATE) & (GM >= P11)].index[0]
GMH = GM['2008':'2021']
GMX = [d.year + (d.month - 1) / 12 for d in GMH.index]
SI = pd.read_csv(os.path.join(HERE, 'data', 'SI_F.csv'), parse_dates=['date']).set_index('date')['close']
SI_CRASH = (SI[CRASH_DATE] / SI[:CRASH_DATE - pd.Timedelta(days=1)].iloc[-1] - 1) * 100
SI_DOWN = (SI.iloc[-1] / SI.max() - 1) * 100
SP = pd.read_csv(os.path.join(HERE, 'data', 'SP500_10y.csv'), parse_dates=['date']).set_index('date')['close']
SP_REC = (SP.iloc[-1] / SP[:REC_DATE].iloc[-1] - 1) * 100
SP_1Y = (SP.iloc[-1] / SP[:NOW_DATE - pd.Timedelta(days=365)].iloc[-1] - 1) * 100
SP_10 = SP.iloc[-1] / SP.iloc[0]
TIPS = 10000 * RY_NOW / 100
import json  # noqa: E402
_gr = json.load(open(os.path.join(HERE, 'data', 'us_gold_reserve.json')))['data']
_r0 = _gr[0]['record_date']
US_OZ = sum(float(r['fine_troy_ounce_qty']) for r in _gr if r['record_date'] == _r0)
US_BOOK = sum(float(r['book_value_amt']) for r in _gr if r['record_date'] == _r0)
KNOX_OZ = sum(float(r['fine_troy_ounce_qty']) for r in _gr if r['record_date'] == _r0 and 'Fort Knox' in r['location_desc'])
US_VALUE = US_OZ * NOW
_ath = G.cummax()
REC25 = int(((G >= _ath) & (G > _ath.shift(1)))['2025'].sum())
YR = GM.resample('YE').last().pct_change().dropna() * 100
BEST_SINCE_2000 = YR.idxmax().year == 2025
CONTRACT = 100 * REC
CAGR_G, CAGR_S = TIMES ** 0.1 - 1, SP_10 ** 0.1 - 1
WGC = dict(cb=321, cb_yoy=42, etf=211, etf_hold=4256, jew=313, jew_yoy=-17, bar=268, bar_yoy=-19, avg=4262, ytd=675, ytd_yoy=6, elec=72, mine=1071)

GX = [d.year + (d.dayofyear - 1) / 366 for d in G.index]
GY = list(G.values)
G26 = G['2026-01-01':]
GX26 = [(d - pd.Timestamp('2026-01-01')).days for d in G26.index]
GY26 = list(G26.values)
GJ = G['2026-01-20':'2026-02-10']
RY26 = RY['2026-01-01':]
RYX = [(d - pd.Timestamp('2026-01-01')).days for d in RY26.index]
DX26 = DXY['2026-01-01':]
DXX = [(d - pd.Timestamp('2026-01-01')).days for d in DX26.index]
MONTHS = [(pd.Timestamp(f'2026-{m:02d}-01') - pd.Timestamp('2026-01-01')).days for m in range(1, 12)]
SRC = 'Yahoo Finance: COMEX gold futures (GC=F), daily closes'


def usd(v):
    return f'${v:,.0f}'


def month_ticks(c, px, y, a=1.0):
    for i, d in enumerate(MONTHS):
        c.text(px(d), y, 'JFMAMJJASON'[i], 18, MUTED, 700, a=a, shadow=False)


def gold_bar(c, x, y, w, a=1.0, shine=0.0):
    """A drawn gold bar (trapezoid), (x, y) = centre of its base."""
    h = w * 0.32
    c.poly([(x - w / 2, y), (x + w / 2, y), (x + w * 0.38, y - h), (x - w * 0.38, y - h)], GOLDC,
           mix(GOLDC, INK, 0.45), 3, a)
    c.poly([(x - w * 0.38, y - h), (x + w * 0.38, y - h), (x + w * 0.30, y - h * 1.25), (x - w * 0.30, y - h * 1.25)],
           mix(GOLDC, WHITE, 0.35), mix(GOLDC, INK, 0.45), 3, a)
    if shine > 0:
        sx = x - w / 2 + w * (shine % 1)
        c.line([(sx, y - 4), (sx + w * 0.1, y - h + 4)], (255, 255, 255, 160), 6, a)


# ------------------------------------------------------------------- scenes --
def s_hook(c, x):
    t, L = x.t, x.L
    fx.photo(c, BARS, 1.12 - 0.04 * clamp(t / 10), (0.5, 0.5), box=FULL, dark=0.55, sat=1.15)
    c.rrect(0, 0, W, H, 0, (8, 10, 20, 110))
    k = pop(t, L[0] + 0.1, 0.3)
    if k > 0:
        c.text(640, 265, f'-{abs(DROP):.0f}%', int(190 * (0.6 + 0.4 * clamp(k))), CORAL, 900, a=clamp(k), stroke=9)
        c.text(640, 390, 'GOLD, FROM ITS RECORD', 40, WHITE, 900, a=clamp(k))
    if t > L[1]:
        v = REC + (NOW - REC) * ease(clamp((t - L[1] - 3.5) / 1.6))
        c.rrect(420, 440, 860, 540, 22, (20, 20, 30, 220), GOLDC, 4, a=fade(t, L[1]))
        c.text(640, 490, f'{usd(v)} / oz', 56, GOLDC, 900, a=fade(t, L[1]))
        c.text(640, 575, f'record {REC_DATE:%b %d}  ·  now {NOW_DATE:%b %d}', 22, WHITE, 800, a=fade(t, L[1] + 0.4))
    if len(L) > 2 and t > L[2]:
        chip(c, 640, 60, 'What happened? Is gold still a safe haven?', GOLD, pop(t, L[2] + 0.4), 26)


def s_decade(c, x):
    t, L = x.t, x.L
    specks(c, t, 91)
    head(c, t, 'Gold, 10 years (COMEX futures, $ per ounce)')
    k = clamp((t - L[0] - 0.4) / 6.0) if t < L[1] else 1.0
    px, py = line_chart(c, (130, 120, 1150, 540), GX, GY, (2016.8, 2027), (0, 6000), k, GOLDC,
                        xticks=range(2017, 2027, 2), yticks=(0, 2000, 4000, 6000), yfmt='${:,.0f}')
    if t > L[0] + 0.8:
        c.text(px(GX[0]) + 10, py(START) - 30, f'{START_DATE:%b %Y}: {usd(START)}', 22, WHITE, 800, anchor='lm',
               a=fade(t, L[0] + 0.8))
    if t > L[0] + 6.5:
        c.text(560, 200, f'{TIMES:.1f}x', 80, GOLDC, 900, anchor='mm', a=fade(t, L[0] + 6.5), stroke=5)
    if t > L[1]:
        for j, (lvl, at) in enumerate(((2000, 0.6), (3000, 3.0), (4000, 5.0), (5000, 6.8))):
            kk = pop(t, L[1] + at)
            if kk <= 0:
                continue
            d = FIRST[lvl]
            xx = px(d.year + (d.dayofyear - 1) / 366)
            c.line([(xx, py(lvl)), (xx, py(lvl) - 60)], (255, 255, 255, 120), 2)
            chip(c, xx - (120 if lvl >= 4000 else 0), py(lvl) - (40 if lvl == 4000 else 75), f'${lvl:,}: {d:%b %Y}', GOLD, kk, 18)
    if len(L) > 2 and t > L[2]:
        c.rrect(300, 560, 740, 620, 30, MINT, a=fade(t, L[2]))
        c.text(520, 590, f'2025 alone: +{Y2025:.0f}%', 32, INK, 900, a=fade(t, L[2]), shadow=False)
        pulse(c, t, (290, 550, 750, 630), MINT, 30)
    source(c, t, SRC)


def s_forces(c, x):
    t, L = x.t, x.L
    specks(c, t, 92)
    head(c, t, 'Why gold soared')
    items = [('landmark', 'Central banks\nbuying'), ('percent', 'Fed cut rates\n3 times in 2025'),
             ('dollar-sign', f'Dollar fell\n{abs(DX_2025):.1f}% in 2025'), ('triangle-alert', 'Wars, tariffs,\ninflation worries')]
    for i, (ic, lab) in enumerate(items):
        k = pop(t, L[i] + 0.3)
        if k <= 0:
            continue
        cx = 175 + i * 310
        on = L[i] <= t < (L[i + 1] if i + 1 < len(L) else 1e9)
        col = GOLD if on else MUTED
        c.circle(cx, 250, 90 * clamp(k), (255, 255, 255, 30 if on else 12), col, 4 if on else 2)
        if on:
            c.circle(cx, 250, 100 + 8 * math.sin(t * 5), None, GOLD, 3, a=0.4 + 0.4 * math.sin(t * 5))
        c.icon(ic, cx, 250, 85 * clamp(k), col)
        for j, part in enumerate(lab.split('\n')):
            c.text(cx, 385 + j * 32, part, 25, WHITE if on else MUTED, 900, a=clamp(k))
    notes = [(0, 3.0, 'to diversify their reserves', SKY), (1, 3.4, 'gold pays no interest', SKY),
             (2, 3.4, 'gold is priced in dollars', SKY), (3, 2.0, 'by January: a frenzy', CORAL)]
    for i, at, txt, col in notes:
        nxt = L[i + 1] if i + 1 < len(L) else 1e9
        if L[i] + at <= t < nxt:
            chip(c, 640, 530, txt, col, pop(t, L[i] + at), 26)
    source(c, t, 'World Gold Council; FRED: DFEDTARU, DTWEXBGS')


def s_crash(c, x):
    t, L = x.t, x.L
    specks(c, t, 93)
    head(c, t, 'January 30, 2026')
    days = list(GJ.index)
    bw = 900 / len(days)
    lo, hi = 4400, 5500
    show = len(days) if t > L[1] + 3.0 else min(len(days), 1 + int(max(0, t - L[0] - 0.3) * 4))
    for i, d in enumerate(days[:show]):
        v, prev = GJ.iloc[i], GJ.iloc[i - 1] if i else GJ.iloc[0]
        col = MINT if v >= prev else CORAL
        y0 = 540 - (prev - lo) / (hi - lo) * 400
        y1 = 540 - (v - lo) / (hi - lo) * 400
        x0 = 190 + i * bw
        big = d == CRASH_DATE
        if big and t < L[1] + 3.0:
            continue
        c.rrect(x0 + 4, min(y0, y1), x0 + bw - 4, max(y0, y1) + 3, 4, col, WHITE if big else None, 3 if big else 0)
        if d.day in (20, 29) or big or d == days[-1]:
            c.text(x0 + bw / 2, 565, f'{d:%b %d}', 16, WHITE if big else MUTED, 800, shadow=False)
    if t > L[1] + 3.0:
        k = pop(t, L[1] + 3.0, 0.3)
        c.text(1010, 250, f'{CRASH:.1f}%', int(90 * (0.6 + 0.4 * clamp(k))), CORAL, 900, a=clamp(k), stroke=6)
        c.text(1010, 320, 'in one day', 28, WHITE, 900, a=clamp(k))
        pulse(c, t, (870, 190, 1150, 350), CORAL)
    if t > L[1] and t < L[1] + 3.0:
        chip(c, 640, 130, 'Kevin Warsh named as pick for Fed chair', SKY, pop(t, L[1] + 0.4), 24)
    if len(L) > 2 and t > L[2]:
        chip(c, 640, 130, 'worst day in 10 years of data', CORAL, pop(t, L[2] + 0.3), 26)
        if t > L[2] + 3.5:
            chip(c, 640, 600, 'analysts: a speculative run-up, the news was the trigger', GOLD, pop(t, L[2] + 3.5), 22)
    if len(L) > 3 and t > L[3]:
        c.rrect(0, 0, W, H, 0, (8, 12, 24, int(250 * fade(t, L[3]))))
        k = pop(t, L[3] + 0.4, 0.3)
        c.text(640, 260, f'SILVER: {SI_CRASH:.0f}%', int(100 * (0.6 + 0.4 * clamp(k))), CORAL, 900, a=clamp(k),
               stroke=6)
        c.text(640, 360, 'the same day', 30, WHITE, 900, a=clamp(k))
        chip(c, 640, 450, f'now {SI_DOWN:.0f}% below its record', GOLD, pop(t, L[3] + 2.6), 26)
    if len(L) > 4 and t > L[4]:
        c.rrect(0, 0, W, H, 0, (10, 14, 26))
        k = pop(t, L[4] + 0.4)
        gold_bar(c, 330, 330, 260 * (0.6 + 0.4 * clamp(k)), clamp(k), shine=t * 0.4)
        c.text(330, 390, '1 COMEX contract = 100 oz', 26, WHITE, 900, a=clamp(k))
        if t > L[4] + 3.0:
            c.text(900, 230, f'about {usd(CONTRACT)}', 50, GOLDC, 900, a=fade(t, L[4] + 3.0), stroke=4)
            c.text(900, 285, 'of gold at the record', 24, WHITE, 800, a=fade(t, L[4] + 3.0))
        chip(c, 900, 380, 'traders put down only a fraction', SKY, pop(t, L[4] + 6.0), 24)
        chip(c, 900, 460, 'fast drops force selling', CORAL, pop(t, L[4] + 9.0), 24)
        if t > L[4] + 9.0:
            pulse(c, t, (720, 425, 1080, 495), CORAL, 30)
    source(c, t, SRC)


def s_slide(c, x):
    t, L = x.t, x.L
    specks(c, t, 94)
    if t < L[1]:  # the whole year: bounce, then the slide
        head(c, t, 'Gold in 2026')
        k = clamp((t - L[0] - 0.3) / 3.5)
        px, py = line_chart(c, (150, 130, 1150, 520), GX26, GY26, (0, 320), (3500, 5600), k, GOLDC,
                            yticks=(3500, 4000, 4500, 5000, 5500), yfmt='${:,.0f}')
        month_ticks(c, px, 545)
        source(c, t, SRC)
        return
    if t < L[3]:  # real yields
        head(c, t, '10-year real yield (after inflation)')
        k = clamp((t - L[1] - 0.3) / 4.0)
        px, py = line_chart(c, (150, 130, 1150, 500), RYX, list(RY26.values), (0, 320), (1.5, 3.0), k, SKY,
                            yticks=(1.5, 2.0, 2.5, 3.0), yfmt='{:.1f}%')
        month_ticks(c, px, 525)
        if t > L[1] + 3.0:
            c.text(px(28) + 12, py(RY_REC) + 34, f'Jan 29: {RY_REC:.2f}%', 22, WHITE, 800, anchor='lm',
                   a=fade(t, L[1] + 3.0))
        if t > L[1] + 4.5:
            c.text(1100, 160, f'{RY_NOW:.1f}%', 60, SKY, 900, anchor='rm', a=fade(t, L[1] + 4.5), stroke=4)
            pulse(c, t, (960, 115, 1130, 205), SKY, 20, on=t < L[2])
        if L[2] < t < L[2] + 4.6:
            chip(c, 640, 590, 'bonds pay more than inflation; gold pays nothing', GOLD, pop(t, L[2] + 0.4), 24)
        if t >= L[2] + 4.6:
            chip(c, 640, 590, f'$10,000 in TIPS: about {usd(TIPS)} a year above inflation', MINT, pop(t, L[2] + 4.6), 24)
            pulse(c, t, (290, 555, 990, 625), MINT, 30)
        source(c, t, 'FRED: DFII10')
        return
    if t < L[4]:  # the dollar
        head(c, t, 'The dollar (broad index)')
        k = clamp((t - L[3] - 0.3) / 3.0)
        px, py = line_chart(c, (150, 130, 1150, 500), DXX, list(DX26.values), (0, 320), (115, 124), k, MINT,
                            yticks=(116, 118, 120, 122, 124), yfmt='{:.0f}')
        month_ticks(c, px, 525)
        if t > L[3] + 3.0:
            c.text(1100, 160, f'+{DX_UP:.1f}%', 60, MINT, 900, anchor='rm', a=fade(t, L[3] + 3.0), stroke=4)
            c.text(1100, 215, 'since the gold record', 22, WHITE, 800, anchor='rm', a=fade(t, L[3] + 3.0))
        source(c, t, 'FRED: DTWEXBGS')
        return
    head(c, t, 'The Fed')
    if t < L[5]:
        k = pop(t, L[4] + 0.6)
        c.rrect(170, 170, 610, 400, 24, (20, 26, 42), SKY, 3, a=clamp(k))
        c.text(390, 220, 'MARCH: HOLD', 32, SKY, 900, a=clamp(k))
        c.text(390, 300, f'gold next day: {MAR[0]:.1f}%', 30, CORAL, 900, a=fade(t, L[4] + 2.6))
        k2 = pop(t, L[4] + 5.0)
        c.rrect(670, 170, 1110, 400, 24, (20, 26, 42), CORAL, 3, a=clamp(k2))
        c.text(890, 220, 'SEPTEMBER: HIKE', 32, CORAL, 900, a=clamp(k2))
        c.text(890, 300, f'{FEDL.iloc[-1]:.2f}% to {FEDU.iloc[-1]:.2f}%', 30, WHITE, 900, a=clamp(k2))
        c.text(890, 350, f'first since {PREV_HIKE:%B %Y}', 22, MUTED, 800, a=clamp(k2))
        if t > L[4] + 5.0:
            pulse(c, t, (660, 160, 1120, 410), CORAL, 28)
        if t > L[4] + 8.0:
            chip(c, 640, 480, f'inflation back near {INFL:.0f}%, oil shock after the war with Iran', GOLD,
                 pop(t, L[4] + 8.0), 22)
        source(c, t, 'Federal Reserve; FRED: DFEDTARU')
        return
    k = clamp((t - L[5] - 0.2) / 2.5)
    px, py = line_chart(c, (150, 130, 1150, 520), GX26, GY26, (0, 320), (3500, 5600), 1.0, GOLDC,
                        yticks=(3500, 4000, 4500, 5000, 5500), yfmt='${:,.0f}')
    month_ticks(c, px, 545)
    ld = (LOW_DATE - pd.Timestamp('2026-01-01')).days
    if k > 0:
        c.circle(px(ld), py(LOW), 14 * ease(k), CORAL, WHITE, 3)
        c.text(px(ld) - 20, py(LOW) + 40, f'Oct 30: {usd(LOW)} ({LOW_DROP:.0f}%)', 26, CORAL, 900, anchor='rm', a=k)
        pulse(c, t, (px(ld) - 30, py(LOW) - 30, px(ld) + 30, py(LOW) + 30), CORAL, 30)
    source(c, t, SRC)


def s_buyers(c, x):
    t, L = x.t, x.L
    specks(c, t, 95)
    head(c, t, 'Q3 2026 gold demand (tonnes)')
    rows = [('Central banks', WGC['cb'], f'+{WGC["cb_yoy"]}% vs a year ago', MINT, L[1] + 0.4),
            ('Gold funds (ETFs)', WGC['etf'], f'holdings: record {WGC["etf_hold"]:,}t', MINT, L[2] + 0.4),
            ('Jewelry', WGC['jew'], f'{WGC["jew_yoy"]}%: weakest Q3 on record', CORAL, L[3] + 0.6),
            ('Bars and coins', WGC['bar'], f'{WGC["bar_yoy"]}%', CORAL, L[3] + 4.8)]
    if t < L[1]:
        k = pop(t, L[0] + 0.3)
        gold_bar(c, 640, 380, 300 * (0.6 + 0.4 * clamp(k)), clamp(k), shine=t * 0.4)
        c.text(640, 470, 'Not everyone stopped buying', 34, WHITE, 900, a=fade(t, L[0] + 0.6))
    for j, (lab, v, note, col, at) in enumerate(rows):
        nxt = rows[j + 1][4] if j + 1 < len(rows) else (L[4] if len(L) > 4 else 1e9)
        if at <= t < nxt:
            pulse(c, t, (130, 150 + j * 105 - 42, 1150, 150 + j * 105 + 62), col, 18)
        g = ease(seg(t, at, at + 0.9))
        if g <= 0:
            continue
        y = 150 + j * 105
        c.text(150, y, lab, 26, WHITE, 900, anchor='lm', a=g)
        c.rrect(450, y - 30, 450 + 1.6 * v * g, y + 30, 10, col)
        c.text(460 + 1.6 * v * g, y, f'{v}t', 26, col, 900, anchor='lm', a=g)
        c.text(450, y + 46, note, 20, MUTED, 800, anchor='lm', a=g, shadow=False)
    if len(L) > 4 and t > L[4]:
        if t < L[4] + 4.5:
            chip(c, 640, 590, f'Q3 average price: {usd(WGC["avg"])} an ounce', GOLD, pop(t, L[4] + 0.6), 26)
            pulse(c, t, (330, 555, 950, 625), GOLD, 30, on=t > L[4] + 1.0)
        else:
            chip(c, 540, 590, f'mines: a record {WGC["mine"]:,} tonnes for a third quarter', SKY, pop(t, L[4] + 4.5), 24)
            pulse(c, t, (200, 555, 880, 625), SKY, 30)
    if L[1] + 4.5 < t < L[2]:
        chip(c, 900, 620, f'year to date: {WGC["ytd"]}t (+{WGC["ytd_yoy"]}%)', MINT, pop(t, L[1] + 4.5), 20)
    source(c, t, 'World Gold Council, Gold Demand Trends Q3 2026')


def s_promise(c, x):
    t, L = x.t, x.L
    specks(c, t, 90)
    c.text(640, 90, 'In this video', 34, WHITE, 900, a=fade(t, 0))
    items = [('rocket', 'why gold\nsoared', 0.5), ('trending-down', 'the day it\ncrashed', 1.8),
             ('scale', 'who is still\nbuying', 3.2), ('shield', 'is it still a\nsafe haven?', 4.6)]
    for i, (ic, lab, at) in enumerate(items):
        k = pop(t, L[0] + at)
        if k <= 0:
            continue
        cx = 175 + i * 310
        c.circle(cx, 260, 85 * clamp(k), (255, 255, 255, 18), GOLD, 3)
        c.icon(ic, cx, 260, 80 * clamp(k), GOLD, a=clamp(k))
        for j, part in enumerate(lab.split('\n')):
            c.text(cx, 395 + j * 32, part, 24, WHITE, 800, a=clamp(k))


def s_what(c, x):
    t, L = x.t, x.L
    specks(c, t, 99)
    head(c, t, 'What exactly is the gold price?')
    if t < L[1]:
        k = pop(t, L[0] + 0.3)
        fx.photo(c, BULLION, 1.1, (0.5, 0.5), box=(140, 130, 700, 470), dark=0.0, sat=1.1, a=clamp(k))
        c.rrect(140, 130, 700, 470, 8, None, GOLDC, 4, a=clamp(k))
        chip(c, 960, 220, '1 troy ounce = 31.1 grams', GOLD, pop(t, L[0] + 2.4), 24)
        chip(c, 960, 320, 'futures on COMEX, New York', SKY, pop(t, L[0] + 5.0), 24)
        if t > L[0] + 5.0:
            pulse(c, t, (760, 285, 1160, 355), SKY, 30)
        return
    items = [('gem', 'jewelry'), ('trending-up', 'investors'), ('landmark', 'central banks'), ('cpu', 'tech')]
    for i, (ic, lab) in enumerate(items):
        k = pop(t, L[1] + 2.4 + 0.7 * i)
        if k <= 0:
            continue
        cx = 175 + i * 310
        hot = i == 3 and len(L) > 2 and t > L[2]
        c.circle(cx, 260, 85 * clamp(k), (255, 255, 255, 30 if hot else 18), GOLD, 4 if hot else 3)
        if hot:
            c.circle(cx, 260, 96 + 8 * math.sin(t * 5), None, GOLD, 3, a=0.4 + 0.4 * math.sin(t * 5))
        c.icon(ic, cx, 260, 80 * clamp(k), GOLD)
        c.text(cx, 395, lab, 26, WHITE, 900, a=clamp(k))
    if t < L[1] + 2.4:
        chip(c, 640, 520, 'no interest, no dividends', CORAL, pop(t, L[1] + 0.3), 28)
    if len(L) > 2 and t > L[2]:
        chip(c, 640, 520, f'Q3: electronics used {WGC["elec"]} tonnes (AI chips)', MINT, pop(t, L[2] + 0.6), 26)
    source(c, t, 'World Gold Council, Gold Demand Trends Q3 2026')


def s_history(c, x):
    t, L = x.t, x.L
    specks(c, t, 89)
    head(c, t, 'Gold, 2008 to 2021 (monthly closes)')
    k = clamp((t - L[0] - 0.3) / 5.0) if t < L[2] else 1.0
    px, py = line_chart(c, (130, 130, 1150, 520), GMX, list(GMH.values), (2008, 2022), (600, 2200), k, GOLDC,
                        xticks=range(2008, 2023, 2), yticks=(600, 1000, 1400, 1800, 2200), yfmt='${:,.0f}')
    if t > L[0] + 3.0:
        xx = P11_DATE.year + (P11_DATE.month - 1) / 12
        c.circle(px(xx), py(P11), 12, GOLD, WHITE, 3)
        c.text(px(xx), py(P11) - 30, f'{P11_DATE:%b %Y}: {usd(P11)}', 22, GOLD, 900, a=fade(t, L[0] + 3.0))
    if len(L) > 1 and t > L[1] + 1.0:
        xx = L15_DATE.year + (L15_DATE.month - 1) / 12
        c.circle(px(xx), py(L15), 12, CORAL, WHITE, 3)
        c.text(px(xx), py(L15) + 34, f'{L15_DATE:%b %Y}: {usd(L15)} ({BUST:.0f}%)', 22, CORAL, 900,
               a=fade(t, L[1] + 1.0))
        pulse(c, t, (px(xx) - 26, py(L15) - 26, px(xx) + 26, py(L15) + 26), CORAL, 26, on=t < L[2])
    if len(L) > 2 and t > L[2] + 1.0:
        xx = BACK.year + (BACK.month - 1) / 12
        c.circle(px(xx), py(GM[BACK]), 12, MINT, WHITE, 3)
        chip(c, px(xx) - 60, py(GM[BACK]) - 50, f'back by {BACK:%b %Y}', MINT, pop(t, L[2] + 1.0), 20)
    if len(L) > 3 and t > L[3]:
        chip(c, 540, 590, 'not a forecast: just how long a slump can last', GOLD, pop(t, L[3] + 0.5), 24)
    source(c, t, 'Yahoo Finance: COMEX gold futures (GC=F), monthly closes')


def s_vs(c, x):
    t, L = x.t, x.L
    specks(c, t, 88)
    head(c, t, 'Gold vs the S&P 500 (prices only)')
    rows = [('since Jan 29', DROP, SP_REC, L[0] + 0.8), ('12 months', Y1, SP_1Y, L[0] + 4.0),
            ('10 years', (TIMES - 1) * 100, (SP_10 - 1) * 100, L[1] + 0.6)]
    for j, (lab, gv, sv, at) in enumerate(rows):
        nxt = rows[j + 1][3] if j + 1 < len(rows) else (L[2] if len(L) > 2 else 1e9)
        if at <= t < nxt:
            pulse(c, t, (150, 180 + j * 140 - 55, 1160, 180 + j * 140 + 55), GOLD, 18)
        g = ease(seg(t, at, at + 0.9))
        if g <= 0:
            continue
        y = 180 + j * 140
        c.text(170, y, lab, 26, WHITE, 900, anchor='lm', a=g)
        for k2, (v, col, nm) in enumerate(((gv, GOLDC, 'gold'), (sv, MINT, 'S&P 500'))):
            yy = y - 22 + k2 * 44
            wv = 380 * min(abs(v), 260) / 260 * g
            x0 = 640
            c.rrect(x0 if v >= 0 else x0 - wv, yy - 16, x0 + wv if v >= 0 else x0, yy + 16, 8, col)
            lab2 = f'{v:+.0f}%' if j < 2 else f'{v / 100 + 1:.1f}x'
            c.text((x0 + wv + 12) if v >= 0 else (x0 - wv - 12), yy, f'{nm} {lab2}', 20, col, 900,
                   anchor='lm' if v >= 0 else 'rm', a=g)
    c.line([(640, 140), (640, 480)], (255, 255, 255, 80), 2)
    if len(L) > 2 and t > L[2]:
        chip(c, 540, 590, 'and stocks paid dividends on top', SKY, pop(t, L[2] + 0.4), 24)
    source(c, t, 'Yahoo Finance: GC=F, ^GSPC daily closes')


def s_knox(c, x):
    t, L = x.t, x.L
    specks(c, t, 87)
    head(c, t, "America's gold (U.S. Treasury)")
    k = pop(t, L[0] + 0.3)
    fx.photo(c, KNOX, 1.05, (0.5, 0.55), box=(120, 120, 620, 470), dark=0.05, sat=1.0, a=clamp(k))
    c.rrect(120, 120, 620, 470, 8, None, GOLDC, 4, a=clamp(k))
    if t > L[0] + 1.6:
        c.text(950, 180, f'{US_OZ / 1e6:.0f} million oz', 50, GOLDC, 900, a=fade(t, L[0] + 1.6), stroke=4)
        c.text(950, 235, f'Fort Knox: {KNOX_OZ / 1e6:.0f} million', 24, WHITE, 800, a=fade(t, L[0] + 3.4))
        pulse(c, t, (730, 140, 1170, 260), GOLD, 20, on=len(L) < 2 or t < L[1])
    if len(L) > 1 and t > L[1]:
        c.rrect(730, 290, 1170, 380, 18, (20, 26, 42), SKY, 3, a=fade(t, L[1]))
        c.text(950, 320, 'on the books: $42.22 / oz', 24, SKY, 900, a=fade(t, L[1]))
        c.text(950, 355, f'= ${US_BOOK / 1e9:.0f} billion', 26, WHITE, 900, a=fade(t, L[1] + 0.6))
    if len(L) > 2 and t > L[2]:
        kk = pop(t, L[2] + 0.4)
        c.rrect(730, 405, 1170, 495, 18, MINT, a=clamp(kk))
        c.text(950, 450, f'at market: ${US_VALUE / 1e12:.2f} trillion', 30, INK, 900, a=clamp(kk), shadow=False)
        pulse(c, t, (720, 395, 1180, 505), MINT, 24)
    source(c, t, 'U.S. Treasury, Status Report of U.S. Government Gold Reserve, Oct 31 2026')


def s_next(c, x):
    t, L = x.t, x.L
    specks(c, t, 86)
    head(c, t, 'What could turn it around? (no predictions)')
    up = [('real rates fall', 0.4), ('dollar weakens', 1.4), ('Fed cuts again', 2.4), ('central banks buy', 4.6)]
    dn = [('real rates rise', 0.4), ('dollar strengthens', 1.6), ('more Fed hikes', 2.8)]
    c.text(330, 140, 'COULD SUPPORT GOLD', 28, MINT, 900, a=fade(t, L[1] if len(L) > 1 else 0))
    c.text(950, 140, 'COULD KEEP PRESSURE ON', 28, CORAL, 900, a=fade(t, L[2] if len(L) > 2 else 0))
    if len(L) > 1:
        for j, (lab, at) in enumerate(up):
            chip(c, 330, 210 + j * 80, lab, MINT, pop(t, L[1] + at), 26)
    if len(L) > 2:
        for j, (lab, at) in enumerate(dn):
            chip(c, 950, 210 + j * 80, lab, CORAL, pop(t, L[2] + at), 26)
    if t < L[1] if len(L) > 1 else True:
        k = pop(t, L[0] + 0.6)
        c.icon('scale', 640, 330 + 10 * math.sin(t * 3), 160 * clamp(k), GOLD)
        c.circle(640, 330, 120 + 10 * math.sin(t * 5), None, GOLD, 3, a=0.3 + 0.4 * (0.5 + 0.5 * math.sin(t * 5)))


def s_haven(c, x):
    t, L = x.t, x.L
    specks(c, t, 96)
    head(c, t, 'Is gold still a safe haven?')
    if t < L[1]:
        k = pop(t, L[0] + 0.5)
        fx.photo(c, KNOX, 1.05, (0.5, 0.55), box=(340, 120, 940, 520), dark=0.1, sat=1.0, a=clamp(k))
        c.rrect(340, 120, 940, 520, 8, None, GOLDC, 4, a=clamp(k))
        return
    cards = [('10 years', f'{TIMES:.1f}x', MINT, 0.5), ('12 months', f'+{Y1:.0f}%', GOLD, 2.4),
             ('since January', f'{DROP:.0f}%', CORAL, 4.4)]
    for j, (lab, val, col, at) in enumerate(cards):
        k = pop(t, L[1] + at)
        if k <= 0:
            continue
        cx = 240 + j * 400
        c.rrect(cx - 170, 170, cx + 170, 410, 24, (20, 26, 42), col, 3, a=clamp(k))
        c.text(cx, 230, lab, 28, WHITE, 900, a=clamp(k))
        c.text(cx, 320, val, int(70 * (0.7 + 0.3 * clamp(k))), col, 900, a=clamp(k))
        nxt = cards[j + 1][3] if j + 1 < len(cards) else (L[2] - L[1] if len(L) > 2 else 1e9)
        if at + L[1] <= t < nxt + L[1]:
            pulse(c, t, (cx - 182, 158, cx + 182, 422), col, 28)
    if t > L[2]:
        for j, (lab, col) in enumerate((('can hedge a falling dollar', MINT), ('can swing wildly', CORAL),
                                        ('pays no interest', SKY))):
            chip(c, 240 + j * 400, 490, lab, col, pop(t, L[2] + 0.6 + 1.6 * j), 22)
            if L[2] + 0.6 + 1.6 * j <= t < (L[2] + 2.2 + 1.6 * j if j < 2 else (L[3] if len(L) > 3 else 1e9)):
                pulse(c, t, (240 + j * 400 - 175, 460, 240 + j * 400 + 175, 520), col, 30)
    if len(L) > 3 and t > L[3]:
        chip(c, 540, 580, f'inflation about {INFL:.0f}%: a {Y1:.0f}% gain lost value', GOLD, pop(t, L[3] + 0.6), 24)
    source(c, t, f'{SRC}; FRED: CPIAUCSL')


def s_lessons(c, x):
    t, L = x.t, x.L
    specks(c, t, 97)
    head(c, t, 'What the data teaches (not advice)')
    items = [('shield', 'Safe haven is not\na safe price'), ('trending-up', 'Watch real rates\nand the dollar'),
             ('zap', 'Fast up,\nfast down')]
    if t < L[1]:
        k = pop(t, L[0] + 1.0)
        c.text(640, 300, '3', int(200 * (0.6 + 0.4 * clamp(k))), GOLD, 900, a=clamp(k), stroke=8)
        return
    for i, (ic, lab) in enumerate(items):
        k = pop(t, L[i + 1] + 0.3)
        if k <= 0:
            continue
        cx = 230 + i * 410
        on = L[i + 1] <= t < (L[i + 2] if i + 2 < len(L) else 1e9)
        c.circle(cx, 250, 85 * clamp(k), (255, 255, 255, 20), GOLD, 3)
        if on:
            c.circle(cx, 250, 96 + 8 * math.sin(t * 5), None, GOLD, 3, a=0.4 + 0.4 * math.sin(t * 5))
        c.icon(ic, cx, 250, 80 * clamp(k), GOLD)
        for j, part in enumerate(lab.split('\n')):
            c.text(cx, 385 + j * 32, part, 26, WHITE, 900, a=clamp(k))


def s_recap(c, x):
    t, L = x.t, x.L
    specks(c, t, 98)
    if t < L[1]:
        head(c, t, 'Recap')
        sp = max(2.0, (L[1] - L[0] - 1.5) / 5)
        rows = [(f'record {usd(REC)} in January, then {DROP:.0f}%', 0.3), (f'crash day: {CRASH:.1f}%', 0.3 + sp),
                ('higher real rates', 0.3 + 2 * sp), ('stronger dollar, Fed hike', 0.3 + 3 * sp),
                ('central banks kept buying', 0.3 + 4 * sp)]
        for j, (txt, at) in enumerate(rows):
            k = pop(t, L[0] + at)
            if k <= 0:
                continue
            c.circle(300, 150 + j * 85, 22 * clamp(k), MINT)
            c.icon('check', 300, 150 + j * 85, 26 * clamp(k), INK, stroke=3)
            c.text(340, 150 + j * 85, txt, 32, WHITE, 900, anchor='lm', a=clamp(k))
            if j == 4 or t < L[0] + rows[j + 1][1]:
                pulse(c, t, (270, 150 + j * 85 - 36, 1050, 150 + j * 85 + 36), MINT, 30)
        return
    k = pop(t, L[1] + 0.3)
    c.text(640, 200, 'Is gold still', 54, WHITE, 900, a=clamp(k))
    c.text(640, 265, 'a safe haven?', 54, GOLD, 900, a=clamp(k))
    for j, (lab, col) in enumerate((('YES', MINT), ('NO', CORAL))):
        kk = pop(t, L[1] + 1.2 + 0.2 * j) * (1 + 0.06 * math.sin(t * 5 + j * 3) if t > L[1] + 2 else 1)
        cx = 520 + j * 240
        c.rrect(cx - 95, 360 - 45 * clamp(kk), cx + 95, 360 + 45 * clamp(kk), 22, col, a=clamp(kk))
        c.text(cx, 360, lab, int(46 * clamp(kk)) + 1, INK, 900, a=clamp(kk), shadow=False)
    if t > L[1] + 5.0:
        chip(c, 640, 480, 'Watch next: how banks create money out of thin air', GOLD, pop(t, L[1] + 5.0), 24)
    penny(c, 1120, 520, 55, t, 'happy', wave=True, talk=x.talk())


R = round
SCENES = [
    dict(draw=s_hook, chapter=f'Intro: gold fell {abs(DROP):.0f}%', lead=0.15, gap=0.3, lines=[
        f"!Gold just fell {abs(DROP):.0f} percent from its all-time high.",
        f"On January 29, gold futures closed at a record {REC:,.0f} dollars an ounce. On November 6, they closed at "
        f"{NOW:,.0f}.",
        "So what happened? And is gold still the safe haven everyone says it is? Let's look at the data.",
    ], punch=lambda L: [L[0] + 0.1], sfx=lambda L: [(L[0] + 0.1, 'hit'), (L[1] + 0.2, 'whoosh'), (L[1] + 3.5, 'down'),
                                                    (L[2] + 0.4, 'pop')]),
    dict(draw=s_promise, lines=[
        "In the next few minutes: why gold soared, the day it crashed, who is still buying, and whether gold is "
        "still a safe haven.",
    ], sfx=lambda L: [(L[0] + 0.5, 'pop'), (L[0] + 1.8, 'pop'), (L[0] + 3.2, 'pop'), (L[0] + 4.6, 'pop')]),
    dict(draw=s_what, chapter='What is the gold price?', lines=[
        "First, what are we measuring? Gold is priced per troy ounce, about 31 grams. The price on the news "
        "usually comes from gold futures traded in New York, on the COMEX exchange.",
        "Gold doesn't pay interest or dividends. Its price comes from who wants it: jewelry makers, investors, "
        "central banks, and even tech companies.",
        f"In the third quarter, electronics alone used {WGC['elec']} tonnes of gold, helped by AI-related "
        "manufacturing, according to the World Gold Council.",
    ], sfx=lambda L: [(L[0] + 0.3, 'pop'), (L[0] + 2.4, 'pop'), (L[0] + 5.0, 'pop'), (L[1] + 0.3, 'pop')]
        + [(L[1] + 2.4 + 0.7 * i, 'pop') for i in range(4)] + [(L[2] + 0.6, 'ding')]),
    dict(draw=s_knox, lines=[
        f"Here's a fun one. The U.S. government owns about {US_OZ / 1e6:.0f} million ounces of gold, more than half "
        f"of it, about {KNOX_OZ / 1e6:.0f} million ounces, in Fort Knox, Kentucky.",
        f"On the government's books, it's still valued at just 42 dollars and 22 cents an ounce: about "
        f"{US_BOOK / 1e9:.0f} billion dollars.",
        f"At the November 6 price, it's worth about {US_VALUE / 1e12:.2f} trillion dollars.",
    ], sfx=lambda L: [(L[0] + 0.3, 'pop'), (L[0] + 1.6, 'ding'), (L[1] + 0.3, 'pop'), (L[2] + 0.4, 'hit')]),
    dict(draw=s_decade, chapter='The rocket ride', lines=[
        f"First, some perspective. In November 2016, an ounce of gold cost about {START:,.0f} dollars. Even after "
        "the drop, it's more than three times that.",
        f"Gold first closed above 2,000 dollars in {FIRST[2000]:%B %Y}. Above 3,000 in {FIRST[3000]:%B %Y}. Above "
        f"4,000 that {FIRST[4000]:%B}. And above 5,000 in {FIRST[5000]:%B %Y}.",
        f"!In 2025 alone, gold gained about {Y2025:.0f} percent, its best year in data going back to 2000, with "
        f"{REC25} record closes along the way.",
    ], punch=lambda L: [L[2] + 0.3], sfx=lambda L: [(L[0] + 0.4, 'whoosh'), (L[0] + 6.5, 'ding'), (L[1] + 0.6, 'pop'),
                                                    (L[1] + 3.0, 'pop'), (L[1] + 5.0, 'pop'), (L[1] + 6.8, 'pop'),
                                                    (L[2] + 0.3, 'hit')]),
    dict(draw=s_forces, chapter='Why gold soared', lines=[
        "Why? Analysts point to a few big forces. Force one: central banks. Countries have been buying gold for "
        "their reserves, to diversify away from other assets.",
        f"Force two: interest rates. The Fed cut rates {len(CUTS25)} times in 2025. Gold pays no interest, so when "
        "rates fall, holding gold costs you less in missed interest.",
        f"Force three: a weaker dollar. Gold is priced in dollars, and in 2025 the dollar fell about "
        f"{abs(DX_2025):.1f} percent against a broad basket of currencies.",
        "Add worries about wars, tariffs and inflation, and by January, gold was in a frenzy.",
    ], sfx=lambda L: [(L[i] + 0.3, 'pop') for i in range(4)] + [(L[0] + 3.0, 'pop'), (L[1] + 3.4, 'pop'),
                                                               (L[2] + 3.4, 'pop'), (L[3] + 2.0, 'riser')]),
    dict(draw=s_crash, chapter='The crash day', lines=[
        "Then came January 30.",
        "That day, President Trump named Kevin Warsh as his pick to lead the Federal Reserve. The dollar rose, and "
        f"gold futures fell {abs(CRASH):.1f} percent in a single day.",
        "It was gold's worst day in our ten years of data. Many analysts said the run-up had become speculative, "
        "and the news was simply the trigger.",
        f"Silver had it even worse. Silver futures fell {abs(SI_CRASH):.0f} percent that same day, and today "
        f"silver is about {abs(SI_DOWN):.0f} percent below its record.",
        f"Part of the reason is how futures work. One COMEX gold contract is 100 ounces: about "
        f"{round(CONTRACT / 1000)} thousand dollars of gold at the record. But traders only put down a fraction of "
        "that. When prices fall fast, many are forced to sell, and that pushes prices down even faster.",
    ], punch=lambda L: [L[1] + 3.0, L[3] + 0.4], sfx=lambda L: [(L[0] + 0.3, 'riser'), (L[1] + 0.4, 'pop'),
                                                               (L[1] + 3.0, 'hit'), (L[2] + 0.3, 'down'),
                                                               (L[2] + 3.5, 'pop'), (L[3] + 0.4, 'hit'),
                                                               (L[3] + 2.6, 'pop'), (L[4] + 0.4, 'whoosh'),
                                                               (L[4] + 3.0, 'ding'), (L[4] + 6.0, 'pop'),
                                                               (L[4] + 9.0, 'down')]),
    dict(draw=s_slide, chapter='The slow slide', lines=[
        "Gold bounced back for a while. But since then, three things have kept pushing it down.",
        f"One: real interest rates. That's what safe government bonds pay after inflation. On January 29, the "
        f"ten-year real yield was {RY_REC:.2f} percent. Now it's about {RY_NOW:.1f}.",
        "When safe bonds pay more than inflation, gold, which pays nothing, looks less attractive. Ten thousand "
        f"dollars in inflation-protected Treasury bonds would earn about {TIPS:,.0f} dollars a year above "
        "inflation. Ten thousand dollars of gold earns nothing; it only pays if the price goes up.",
        f"Two: the dollar got stronger. Since the record, the broad dollar index is up about {DX_UP:.1f} percent.",
        f"Three: the Fed. In March, it held rates steady, and gold fell almost {abs(MAR[0]):.0f} percent the next "
        f"day. In September, it raised rates for the first time since {PREV_HIKE:%Y}, fighting inflation that had "
        f"climbed back to about {INFL:.0f} percent, partly because of the oil shock after the war with Iran.",
        f"!By October 30, gold was down about {abs(LOW_DROP):.0f} percent from its record.",
    ], punch=lambda L: [L[5] + 0.4], sfx=lambda L: [(L[2] + 4.6, 'pop'), (L[0] + 0.3, 'whoosh'), (L[1] + 0.3, 'whoosh'),
                                                    (L[1] + 3.0, 'pop'), (L[1] + 4.5, 'ding'), (L[2] + 0.4, 'pop'),
                                                    (L[3] + 0.3, 'whoosh'), (L[3] + 3.0, 'ding'), (L[4] + 0.6, 'pop'),
                                                    (L[4] + 2.6, 'down'), (L[4] + 5.0, 'pop'), (L[5] + 0.4, 'hit')]),
    dict(draw=s_history, chapter='This has happened before', lines=[
        f"Has this happened before? Yes. In {P11_DATE:%B %Y}, gold's monthly close hit about {P11:,.0f} dollars.",
        f"Over the next four years, it fell {abs(BUST):.0f} percent, to about {L15:,.0f} dollars in "
        f"{L15_DATE:%B %Y}.",
        f"It took until {BACK:%B %Y}, almost nine years after that peak, for gold to get back to its 2011 high.",
        "That doesn't mean it will happen again. But it shows how long a gold slump can last.",
    ], sfx=lambda L: [(L[0] + 0.3, 'whoosh'), (L[0] + 3.0, 'pop'), (L[1] + 1.0, 'down'), (L[2] + 1.0, 'ding'),
                      (L[3] + 0.5, 'pop')]),
    dict(draw=s_buyers, chapter="Who's still buying", lines=[
        "But here's the twist. Not everyone stopped buying.",
        f"In the third quarter, central banks added {WGC['cb']} tonnes of gold, up {WGC['cb_yoy']} percent from a "
        f"year earlier, according to the World Gold Council. So far this year, they've bought {WGC['ytd']} tonnes, "
        f"{WGC['ytd_yoy']} percent more than last year.",
        f"Gold funds took in {WGC['etf']} tonnes, and their total holdings hit a record {WGC['etf_hold']:,} tonnes. "
        "These funds let regular investors own gold without storing a single bar.",
        f"So who stopped? Regular buyers. Jewelry demand fell {abs(WGC['jew_yoy'])} percent, the weakest third "
        f"quarter in the council's data. Gold bars and coins fell {abs(WGC['bar_yoy'])} percent, with China the one "
        "big exception, up 7 percent.",
        f"Even after the drop, gold averaged {WGC['avg']:,} dollars an ounce in the third quarter. For most people, "
        f"that's still very expensive. And mines dug up a record {WGC['mine']:,} tonnes for a third quarter.",
    ], sfx=lambda L: [(L[0] + 0.3, 'pop'), (L[1] + 0.4, 'whoosh'), (L[2] + 0.4, 'whoosh'), (L[3] + 0.6, 'down'),
                      (L[3] + 4.8, 'down'), (L[4] + 0.6, 'pop')]),
    dict(draw=s_vs, chapter='Gold vs stocks', lines=[
        f"How does that compare with stocks? Since January 29, the S&P 500 is up about {SP_REC:.0f} percent. Over "
        f"the last twelve months, about {SP_1Y:.0f} percent.",
        f"Over ten years, both roughly tripled. Gold, about {TIMES:.1f} times. The S&P 500, about {SP_10:.1f} times, "
        f"counting prices only. That's about {CAGR_G * 100:.0f} percent a year for gold, and {CAGR_S * 100:.0f} for "
        "stocks.",
        "And stocks paid dividends on top. Gold never pays anything while you hold it.",
    ], sfx=lambda L: [(L[0] + 0.8, 'pop'), (L[0] + 4.0, 'pop'), (L[1] + 0.6, 'pop'), (L[2] + 0.4, 'pop')]),
    dict(draw=s_haven, chapter='Is gold still a safe haven?', lines=[
        "So is gold still a safe haven? It depends what you mean.",
        f"Over ten years, gold has more than tripled. Over the last twelve months, it's up only about {Y1:.0f} "
        "percent. And since January, it's down almost a quarter. Anyone who bought one ounce at the record is down "
        f"about {REC - NOW:,.0f} dollars.",
        "Gold's big strength is that it isn't anyone's debt: no company or government has to pay it back, and it "
        "can help when the dollar falls. But it can swing wildly, and it pays no interest or dividends.",
        f"And with inflation at about {INFL:.0f} percent, that {Y1:.0f} percent gain over a year actually lost "
        "value.",
    ], sfx=lambda L: [(L[0] + 0.5, 'pop'), (L[1] + 0.5, 'ding'), (L[1] + 2.4, 'pop'), (L[1] + 4.4, 'down'),
                      (L[2] + 0.6, 'pop'), (L[2] + 2.2, 'pop'), (L[2] + 3.8, 'pop'), (L[3] + 0.6, 'pop')]),
    dict(draw=s_next, chapter='What could turn it around?', lines=[
        "So what could turn gold around? Nobody knows, and we don't make predictions. But the same forces that "
        "pushed it down can work in reverse.",
        "If real interest rates fall, if the dollar weakens, or if the Fed starts cutting again, gold could get "
        "support. And central banks are still buying.",
        "And if rates and the dollar keep rising, the pressure could continue.",
    ], sfx=lambda L: [(L[0] + 0.6, 'pop'), (L[1] + 0.4, 'pop'), (L[1] + 1.4, 'pop'), (L[1] + 2.4, 'pop'),
                      (L[1] + 4.6, 'pop'), (L[2] + 0.4, 'pop'), (L[2] + 1.6, 'pop'), (L[2] + 2.8, 'pop')]),
    dict(draw=s_lessons, chapter='What it means for you', lines=[
        "We don't give financial advice, but the data teaches three lessons.",
        f"One: a safe haven doesn't mean a safe price. Gold fell almost {abs(R(CRASH)):.0f} percent in one day, "
        f"and silver {abs(SI_CRASH):.0f}.",
        "Two: watch real interest rates and the dollar. This year, when they went up, gold went down.",
        f"Three: when something rises {Y2025:.0f} percent in a year, the ride down can be fast too. And after 2011, "
        "the wait to get back took almost nine years. If you own gold, know why you own it.",
    ], sfx=lambda L: [(L[0] + 1.0, 'pop'), (L[1] + 0.3, 'pop'), (L[2] + 0.3, 'pop'), (L[3] + 0.3, 'pop')]),
    dict(draw=s_recap, chapter='Recap', tail=0.6, lines=[
        f"Let's recap. Gold hit a record {REC:,.0f} dollars in January, then fell {abs(DROP):.0f} percent. The crash "
        "day came with a new pick for Fed chair. Since then, higher real rates, a stronger dollar and a Fed hike "
        "pushed it lower, while central banks kept buying. Over ten years, gold still more than tripled, but it pays "
        "nothing while you wait, and slumps can last for years.",
        "!So here's my question: is gold still a safe haven? Yes or no, tell me in the comments. And if you missed "
        "it, watch our video on how banks create money out of thin air.",
        "This video is for education only. It's not financial advice.",
    ], punch=lambda L: [L[1] + 0.3], sfx=lambda L: [(L[0] + 0.3 + max(2.0, (L[1] - L[0] - 1.5) / 5) * j, 'pop')
                                                    for j in range(5)]
        + [(L[1] + 0.3, 'ding'), (L[1] + 1.2, 'pop'), (L[1] + 1.4, 'pop'), (L[1] + 5.0, 'pop')]),
]
SHORTS = {}


def check_numbers():
    script = ' '.join(l for sc in SCENES for l in sc['lines'])
    assert REC_DATE.strftime('%Y-%m-%d') == '2026-01-29' and round(REC, 1) == 5318.4
    assert NOW_DATE.strftime('%Y-%m-%d') == '2026-11-06' and round(NOW, 1) == 4074.9 and round(DROP) == -23
    assert LOW_DATE.strftime('%Y-%m-%d') == '2026-10-30' and round(LOW, 1) == 3898.9 and round(LOW_DROP) == -27
    assert START_DATE.strftime('%Y-%m') == '2016-11' and round(START) == 1273 and 3.0 < TIMES < 3.3
    assert round(Y2025) == 64 and round(Y1) == 2 and round(INFL) == 4
    assert [FIRST[k].strftime('%Y-%m') for k in (2000, 3000, 4000, 5000)] == ['2020-08', '2025-03', '2025-10',
                                                                              '2026-01']
    assert CRASH_DATE.strftime('%Y-%m-%d') == '2026-01-30' and round(CRASH, 1) == -10.8 and DX_CRASH > 0
    assert MAR[1].strftime('%Y-%m-%d') == '2026-03-19' and round(MAR[0]) == -6
    assert round(RY_REC, 2) == 1.89 and round(RY_NOW, 1) == 2.6 and round(DX_UP, 1) == 3.6 and round(DX_2025, 1) == -7.5
    assert len(CUTS25) == 3 and HIKE26.strftime('%Y-%m-%d') == '2026-09-17' and PREV_HIKE.year == 2023
    assert (FEDL.iloc[-1], FEDU.iloc[-1]) == (3.75, 4.0)
    assert round(P11, 1) == 1828.5 and P11_DATE.strftime('%Y-%m') == '2011-08' and round(BUST) == -42
    assert round(L15, 1) == 1060.3 and L15_DATE.strftime('%Y-%m') == '2015-12' and BACK.strftime('%Y-%m') == '2020-07'
    assert round(US_OZ) == 261498926 and round(US_BOOK / 1e9) == 11 and round(US_VALUE / 1e12, 2) == 1.07
    assert KNOX_OZ / US_OZ > 0.5 and REC25 == 55 and BEST_SINCE_2000 and round(CONTRACT / 1000) == 532
    assert round(CAGR_G * 100) == 12 and round(CAGR_S * 100) == 13
    assert round(SI_CRASH) == -31 and round(SI_DOWN) == -55
    assert round(SP_REC) == 6 and round(SP_1Y) == 10 and round(SP_10, 1) == 3.5 and round(TIPS) == 260
    for s in ('321 tonnes', '42 percent', '211 tonnes', '4,256 tonnes', '17 percent', '19 percent',
              '4,262 dollars', 'World Gold Council', 'Kevin Warsh', 'not financial advice', "It's not financial advice",
              'more than three times', 'almost a quarter', 'first time since 2023', 'war with Iran', '1,243 dollars'):
        assert s in script, s
    print(f'numbers check: OK  record ${REC:,.1f} ({REC_DATE:%b %d}) -> ${NOW:,.1f} ({NOW_DATE:%b %d}) = {DROP:.1f}%; '
          f'low ${LOW:,.1f} ({LOW_DATE:%b %d}) {LOW_DROP:.1f}%; 10y {TIMES:.2f}x; 2025 +{Y2025:.1f}%; 1y {Y1:+.1f}%; '
          f'crash {CRASH:.1f}% (dollar {DX_CRASH:+.2f}%); Mar {MAR[0]:.1f}%; real yld {RY_REC:.2f}->{RY_NOW:.2f}; '
          f'dollar +{DX_UP:.1f}% since record, {DX_2025:.1f}% in 2025; cuts 2025 {len(CUTS25)}; CPI {INFL:.1f}%')


if __name__ == '__main__':
    check_numbers()
    os.makedirs(BUILD, exist_ok=True)
    if '--stills' in sys.argv:
        previews(SCENES, SHORTS, os.path.join(BUILD, 'previews'))
        sys.exit()
    only = [int(a) for a in sys.argv[sys.argv.index('--only') + 1].split(',')] if '--only' in sys.argv else None
    total, chapters = build(SCENES, os.path.join(OUT, 'ep09_gold.mp4'), BUILD, only=only,
                            srt_path=os.path.join(OUT, 'ep09_gold.en.srt'))
    with open(os.path.join(OUT, 'ep09_chapters.txt'), 'w') as f:
        for at, name in chapters:
            f.write(f'{fmt_time(at)} {name}\n')
    print(f'total {total / 60:.1f} min')
