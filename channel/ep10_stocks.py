"""Episode 10: Stocks fell 6 days in a row. Is a crash coming? (long video, Thu Nov 19 2026, same-day news)

    python3 channel/ep10_stocks.py [--stills] [--only 3,5]

Data (check_numbers recomputes everything from the files; nothing is typed in by hand):
- channel/data/GSPC_max.csv, DJI_max.csv, IXIC_max.csv: Yahoo Finance chart API daily closes for the S&P 500 (^GSPC,
  from 1927), Dow Jones Industrial Average (^DJI, from 1992) and Nasdaq Composite (^IXIC, from 1971), saved Nov 19 2026
  after the close. History statistics use the S&P 500 from 1950 (prices only, no dividends).
- FRED: DGS10 (10-year Treasury yield), DFEDTARU/DFEDTARL (Fed target range), CPIAUCSL (CPI).
No photos: every visual is drawn in code.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from wk2_art import *  # noqa: E402,F401,F403
from engine import build, previews  # noqa: E402
from ep06_banks import head, pulse  # noqa: E402

OUT = os.path.join(HERE, 'out')
BUILD = os.path.join(HERE, 'build', 'ep10_stocks')


def idx(name):
    return pd.read_csv(os.path.join(HERE, 'data', f'{name}_max.csv'), parse_dates=['date']).set_index('date')['close']


SPX, DOW, NDQ = idx('GSPC'), idx('DJI'), idx('IXIC')
TODAY = SPX.index[-1]


def from_record(s):
    return (s.iloc[-1] / s.max() - 1) * 100, s.max(), s.idxmax()


SP_DD, SP_REC, SP_REC_D = from_record(SPX)
DOW_DD, DOW_REC, DOW_REC_D = from_record(DOW)
NDQ_DD, NDQ_REC, NDQ_REC_D = from_record(NDQ)
SP_NOW, DOW_NOW, NDQ_NOW = SPX.iloc[-1], DOW.iloc[-1], NDQ.iloc[-1]
SP_DAY = (SPX.iloc[-1] / SPX.iloc[-2] - 1) * 100
DOW_DAY_PTS = DOW.iloc[-1] - DOW.iloc[-2]


def losing_streak(s):
    n = 0
    for v in s.pct_change()[::-1]:
        if v < 0:
            n += 1
        else:
            break
    return n


STREAK = losing_streak(SPX)
ST0 = SPX.iloc[-STREAK - 1]
ST_PCT = (SP_NOW / ST0 - 1) * 100
LAST7 = SPX.iloc[-STREAK - 1:]
SP_YTD = (SP_NOW / SPX[:'2025-12-31'].iloc[-1] - 1) * 100
SP_10Y = SP_NOW / SPX[:TODAY - pd.Timedelta(days=3653)].iloc[-1]
DOW_BELOW_SINCE = DOW[:DOW.index[-2]][DOW[:DOW.index[-2]] < 50000].index[-1]

# history since 1950 (S&P 500, closes)
HS = SPX['1950':]
_eps, _in = [], False
for d, v in (HS / HS.cummax() - 1).items():
    if not _in and v < 0:
        _in, start, depth = True, d, v
    elif _in:
        depth = min(depth, v)
        if v == 0:
            _eps.append((start, d, depth))
            _in = False
EPS = pd.DataFrame(_eps, columns=['start', 'rec', 'depth'])
N8 = int((EPS.depth <= -0.08).sum())
N10 = int((EPS.depth <= -0.10).sum())
N20 = int((EPS.depth <= -0.20).sum())
CORR = EPS[(EPS.depth <= -0.10) & (EPS.depth > -0.20)]
CORR_DAYS = float((CORR.rec - CORR.start).dt.days.median())
YEARS = (HS.index[-1] - HS.index[0]).days / 365.25
IY = HS.groupby(HS.index.year).apply(lambda s: (s / s.cummax() - 1).min())[:-1]
IY_MED = float(IY.median()) * 100
YR = HS.resample('YE').last().pct_change().dropna()[:-1]
UP_YEARS, ALL_YEARS = int((YR > 0).sum()), len(YR)
_neg = (HS.pct_change() < 0).astype(int)
_run = _neg.groupby((_neg != _neg.shift()).cumsum()).cumsum() * _neg
_hits = [d for d in HS[_run == 6].index if d < TODAY]
F12 = [HS.iloc[HS.index.get_loc(d) + 252] / HS.loc[d] - 1 for d in _hits if HS.index.get_loc(d) + 252 < len(HS)]
N6, UP6 = len(_hits), sum(x > 0 for x in F12)
MED6 = float(np.median(F12)) * 100
LAST6 = _hits[-1]
_r = HS.pct_change().dropna()
BEST10 = _r.nlargest(10)
_worst20 = _r.nsmallest(20).index
NEAR = sum(any(abs((b - w).days) <= 14 for w in _worst20) for b in BEST10.index)

Y10 = series('DGS10')
Y_NOW, Y_DATE = Y10.iloc[-1], Y10.index[-1]
Y_1Y = Y10[:Y_DATE - pd.Timedelta(days=365)].iloc[-1]
FEDU, FEDL = series('DFEDTARU'), series('DFEDTARL')
CPI = series('CPIAUCSL')
INFL = (CPI.iloc[-1] / CPI.iloc[-13] - 1) * 100
HIKE = FEDU[FEDU.diff() > 0].index[-1]

K_REC = 10000 * SP_NOW / SP_REC
_d10 = SPX[:TODAY - pd.Timedelta(days=3653)]
K_10Y, D_10Y = 10000 * SP_NOW / _d10.iloc[-1], _d10.index[-1]
_i6 = HS.index.get_loc(LAST6)
LAST6_CLOSE, LAST6_1Y = HS.iloc[_i6], (HS.iloc[_i6 + 252] / HS.iloc[_i6] - 1) * 100


def episode(peak_before, year):
    pk = SPX[:peak_before].max()
    lo = SPX[str(year)].idxmin()
    rec = SPX[(SPX.index > lo) & (SPX >= pk)].index[0]
    yr = (SPX[str(year)].iloc[-1] / SPX[:f'{year - 1}-12-31'].iloc[-1] - 1) * 100
    return (SPX[lo] / pk - 1) * 100, lo, rec, yr


C20, C20_LOW, C20_REC, C20_YR = episode('2020-02-19', 2020)
MORT = series('MORTGAGE30US')
MORT_NOW, MORT_1Y = MORT.iloc[-1], MORT[:MORT.index[-1] - pd.Timedelta(days=365)].iloc[-1]
PRIME = series('DPRIME').iloc[-1]
CORR_LINE = SP_REC * 0.9
_nb, _db = NDQ[:'2025-12-31'].iloc[-1], DOW[:'2025-12-31'].iloc[-1]
NDQ_PEAK_YTD, NDQ_YTD = (NDQ['2026'].max() / _nb - 1) * 100, (NDQ_NOW / _nb - 1) * 100
DOW_PEAK_YTD, DOW_YTD = (DOW['2026'].max() / _db - 1) * 100, (DOW_NOW / _db - 1) * 100
TICK = (f'S&P 500  {SP_NOW:,.2f}  {SP_DAY:+.2f}%     DOW  {DOW_NOW:,.2f}     NASDAQ  {NDQ_NOW:,.2f}     '
        f'10-YR YIELD  {Y_NOW:.2f}%     FED RATE  {FEDL.iloc[-1]:.2f}-{FEDU.iloc[-1]:.2f}%     CPI  {INFL:.1f}%     ')

C22, C22_LOW, C22_REC, C22_YR = episode('2022-01-03', 2022)

SRC = 'Yahoo Finance daily closes: S&P 500, Dow Jones, Nasdaq Composite'


def pct(v, d=1):
    return f'{v:+.{d}f}%'


# ------------------------------------------------------------------- scenes --
def s_hook(c, x):
    t, L = x.t, x.L
    specks(c, t, 101)
    k = pop(t, L[0] + 0.1, 0.3)
    if k > 0:
        c.text(640, 230, f'{STREAK} DAYS', int(150 * (0.6 + 0.4 * clamp(k))), CORAL, 900, a=clamp(k), stroke=8)
        c.text(640, 330, 'IN A ROW: S&P 500 DOWN', 40, WHITE, 900, a=clamp(k))
    if t > L[1]:
        rows = [('S&P 500', SP_DD), ('Dow Jones', DOW_DD), ('Nasdaq', NDQ_DD)]
        for i, (n, v) in enumerate(rows):
            kk = pop(t, L[1] + 0.4 + 1.6 * i)
            if kk <= 0:
                continue
            y = 420 + i * 62
            c.rrect(360, y - 26, 920, y + 26, 18, (20, 24, 40, 230), CORAL if v <= -10 else GOLD, 3, a=clamp(kk))
            c.text(390, y, n, 28, WHITE, 900, anchor='lm', a=clamp(kk))
            c.text(890, y, f'{v:.1f}% from record', 28, CORAL if v <= -10 else GOLD, 900, anchor='rm', a=clamp(kk))
    if len(L) > 2 and t > L[2]:
        chip(c, 640, 75, 'Is a crash coming? Here is what history says', GOLD, pop(t, L[2] + 0.2), 26)
    if len(L) > 3 and t > L[3]:
        c.rrect(0, 0, W, H, 0, (10, 14, 26, int(240 * fade(t, L[3]))))
        kk = pop(t, L[3] + 0.3)
        c.text(640, 260, f'{N8} drops of 8%+', 64, GOLD, 900, a=clamp(kk), stroke=5)
        c.text(640, 340, 'since 1950', 30, WHITE, 800, a=clamp(kk))
        if t > L[3] + 3.5:
            c.text(640, 450, f'only {N20} became bear markets', 46, MINT, 900, a=fade(t, L[3] + 3.5), stroke=4)
            pulse(c, t, (300, 410, 980, 490), MINT, 30)


def s_promise(c, x):
    t, L = x.t, x.L
    specks(c, t, 102)
    penny(c, 200, 520, 100, t, 'thinking', talk=x.talk())
    items = ['What happened this week', 'Why stocks are falling', 'What history says', 'What it means for you']
    for i, it in enumerate(items):
        k = pop(t, L[0] + 0.5 + 1.4 * i)
        if k > 0:
            c.rrect(420, 150 + i * 105, 1120, 230 + i * 105, 22, (255, 255, 255, 22), GOLD, 3, a=clamp(k))
            c.text(460, 190 + i * 105, f'{i + 1}', 40, GOLD, 900, a=clamp(k))
            c.text(510, 190 + i * 105, it, 34, WHITE, 800, anchor='lm', a=clamp(k))


def s_week(c, x):
    t, L = x.t, x.L
    specks(c, t, 103)
    head(c, t, 'S&P 500, the last 7 trading days (closing level)')
    vals = list(LAST7.values)
    lo, hi = min(vals) * 0.985, max(vals) * 1.004
    n = len(vals)
    bw = 900 / n
    show = min(n, 1 + int(max(0, t - L[0] - 0.3) * 1.4)) if t < L[1] else n
    for i in range(show):
        v = vals[i]
        y = 540 - (v - lo) / (hi - lo) * 380
        x0 = 190 + i * bw
        col = SKY if i == 0 else CORAL
        c.rrect(x0 + 14, y, x0 + bw - 14, 540, 8, col)
        c.text(x0 + bw / 2, y - 22, f'{v:,.0f}', 20, WHITE, 800)
        c.text(x0 + bw / 2, 565, f'{LAST7.index[i]:%b %d}', 17, MUTED, 800, shadow=False)
        if i:
            ch = (v / vals[i - 1] - 1) * 100
            c.text(x0 + bw / 2, y + 22, f'{ch:.1f}%', 17, INK, 900, shadow=False)
    if t > L[1]:
        chip(c, 640, 130, f'{STREAK} losses in a row: {ST_PCT:.1f}% in total', CORAL, pop(t, L[1] + 0.3), 26)
    if len(L) > 2 and t > L[2]:
        chip(c, 900, 200, f'today: {SP_DAY:.1f}%', CORAL, pop(t, L[2] + 0.3), 26)
        pulse(c, t, (190 + (n - 1) * bw, 150, 190 + n * bw, 545), CORAL, 12)
    if len(L) > 3 and t > L[3]:
        c.rrect(0, 0, W, H, 0, (10, 14, 26, int(245 * fade(t, L[3]))))
        kk = pop(t, L[3] + 0.3)
        c.text(640, 250, f'${10000 * (1 + ST_PCT / 100):,.0f}', 110, GOLD, 900, a=clamp(kk), stroke=6)
        c.text(640, 350, f'what $10,000 in an S&P 500 fund became in {STREAK} days', 28, WHITE, 800, a=clamp(kk))
    source(c, t, SRC)


def s_terms(c, x):
    t, L = x.t, x.L
    specks(c, t, 104)
    head(c, t, 'How far each index is below its record')
    items = [('S&P 500', -SP_DD, GOLD), ('Dow Jones', -DOW_DD, GOLD), ('Nasdaq', -NDQ_DD, CORAL)]
    compare_bars(c, t, items, L[0] + 0.3, 3.5, 25, lambda v: f'-{v:.1f}%', box=(200, 150, 820, 520))
    lines = [(10, 'correction', GOLD), (20, 'bear market', CORAL)]
    for i, (lvl, name, col) in enumerate(lines):
        if t > L[1] + 0.5 + 2.5 * i:
            y = 520 - 370 * lvl / 25
            a = fade(t, L[1] + 0.5 + 2.5 * i)
            for xx in range(200, 830, 30):
                c.line([(xx, y), (xx + 16, y)], col, 3, a)
            c.text(850, y, f'-{lvl}%: {name}', 24, col, 900, anchor='lm', a=a)
    if len(L) > 2 and t > L[2]:
        chip(c, 1040, 300, 'Nasdaq: in correction', CORAL, pop(t, L[2] + 0.3), 24)
    if len(L) > 3 and t > L[3]:
        chip(c, 1040, 450, 'Dow: below 50,000', GOLD, pop(t, L[3] + 0.3), 24)
    if len(L) > 4 and t > L[4]:
        y = 520 - 370 * 10 / 25
        chip(c, 420, 125, f'correction line: S&P below {CORR_LINE:,.0f}', GOLD, pop(t, L[4] + 0.3), 22)
        pulse(c, t, (200, y - 12, 830, y + 12), GOLD, 8)
    source(c, t, SRC + ' (records: S&P and Nasdaq Oct 6, Dow Aug 5, 2026)')


def s_yields(c, x):
    t, L = x.t, x.L
    specks(c, t, 105)
    head(c, t, 'Reason 1: safe bonds now pay over 5%')
    y = Y10['2024-01-01':]
    xs = [(d - pd.Timestamp('2024-01-01')).days / 365.25 + 2024 for d in y.index]
    k = clamp((t - L[0] - 0.3) / 4.5) if t < L[1] else 1.0
    px, py = line_chart(c, (150, 140, 1120, 520), xs, list(y.values), (2024, 2027), (3, 6), k, SKY,
                        xticks=(2024, 2025, 2026), yticks=(3, 4, 5, 6), yfmt='{:.0f}%')
    if t > L[0] + 4.8:
        c.text(px(xs[-1]) - 10, py(Y_NOW) - 40, f'{Y_NOW:.2f}%', 40, SKY, 900, anchor='rm', a=fade(t, L[0] + 4.8),
               stroke=4)
    if t > L[1]:
        chip(c, 640, 565, f'a year ago: {Y_1Y:.2f}%', MUTED, pop(t, L[1] + 0.3), 22)
    if len(L) > 2 and t > L[2]:
        c.rrect(0, 0, W, H, 0, (10, 14, 26, int(240 * fade(t, L[2]))))
        kk = pop(t, L[2] + 0.3)
        c.icon('landmark', 360, 300, 140 * clamp(kk), SKY, a=clamp(kk))
        c.text(360, 430, f'Treasury: {Y_NOW:.1f}% a year', 30, SKY, 900, a=clamp(kk))
        c.text(360, 470, 'backed by the U.S. government', 20, WHITE, 700, a=clamp(kk))
        if t > L[2] + 3.0:
            c.icon('trending-up', 920, 300, 140, GOLD, a=fade(t, L[2] + 3.0))
            c.text(920, 430, 'Stocks: no promise', 30, GOLD, 900, a=fade(t, L[2] + 3.0))
            c.text(920, 470, 'they have to compete', 20, WHITE, 700, a=fade(t, L[2] + 3.0))
            c.text(640, 300, 'vs', 40, MUTED, 900, a=fade(t, L[2] + 3.0))
    source(c, t, 'FRED: DGS10 (10-year Treasury yield)')


def s_fed(c, x):
    t, L = x.t, x.L
    specks(c, t, 106)
    head(c, t, 'Reason 2: inflation is back, and the Fed raised rates')
    k = pop(t, L[0] + 0.3)
    if k > 0:
        c.text(330, 260, f'{INFL:.1f}%', int(120 * (0.6 + 0.4 * clamp(k))), CORAL, 900, a=clamp(k), stroke=6)
        c.text(330, 350, 'inflation, year to October', 26, WHITE, 800, a=clamp(k))
    if t > L[1]:
        f = FEDU['2024-06-01':]
        xs = [(d - pd.Timestamp('2024-06-01')).days for d in f.index]
        kk = clamp((t - L[1] - 0.3) / 3.5)
        px, py = line_chart(c, (640, 170, 1140, 470), xs, list(f.values), (0, xs[-1] + 5), (3, 6), kk, GOLD,
                            yticks=(3, 4, 5, 6), yfmt='{:.0f}%', tick_size=16)
        c.text(890, 510, 'Fed rate (top of range), since mid-2024', 18, MUTED, 700, a=fade(t, L[1]))
        if t > L[1] + 3.8:
            hx = px((HIKE - pd.Timestamp('2024-06-01')).days)
            chip(c, hx - 80, py(4.0) - 60, f'hike: {HIKE:%b %d}', CORAL, pop(t, L[1] + 3.8), 20)
    if len(L) > 2 and t > L[2]:
        chip(c, 640, 560, 'higher rates = costlier borrowing for companies and families', SKY, pop(t, L[2] + 0.3), 22)
    if len(L) > 3 and t > L[3]:
        c.rrect(0, 0, W, H, 0, (10, 14, 26, int(240 * fade(t, L[3]))))
        kk = pop(t, L[3] + 0.3)
        c.icon('house', 360, 260, 120 * clamp(kk), GOLD, a=clamp(kk))
        c.text(360, 380, f'{MORT_NOW:.2f}%', 64, GOLD, 900, a=clamp(kk), stroke=4)
        c.text(360, 440, f'30-yr mortgage (a year ago: {MORT_1Y:.2f}%)', 22, WHITE, 800, a=clamp(kk))
        if t > L[3] + 5.0:
            c.icon('credit-card', 920, 260, 120, CORAL, a=fade(t, L[3] + 5.0))
            c.text(920, 380, f'{PRIME:.2f}%', 64, CORAL, 900, a=fade(t, L[3] + 5.0), stroke=4)
            c.text(920, 440, 'prime rate', 22, WHITE, 800, a=fade(t, L[3] + 5.0))
    source(c, t, 'FRED: CPIAUCSL, DFEDTARU, MORTGAGE30US (Freddie Mac), DPRIME')


def s_tech(c, x):
    t, L = x.t, x.L
    specks(c, t, 107)
    head(c, t, 'Reason 3: the biggest winners fell the hardest')
    n = NDQ['2026-01-01':] / NDQ[:'2025-12-31'].iloc[-1] * 100
    d = DOW['2026-01-01':] / DOW[:'2025-12-31'].iloc[-1] * 100
    k = clamp((t - L[0] - 0.3) / 4.0) if t < L[1] else 1.0
    xs = lambda s: [(i - pd.Timestamp('2026-01-01')).days for i in s.index]  # noqa: E731
    px, py = line_chart(c, (150, 140, 1120, 500), xs(n), list(n.values), (0, 330), (80, 125), k, CORAL,
                        yticks=(80, 100, 120), yfmt='{:.0f}')
    line_chart(c, (150, 140, 1120, 500), xs(d), list(d.values), (0, 330), (80, 125), k, GOLD)
    if t > L[0] + 4.3:
        c.text(1000, py(n.max()) - 10, 'Nasdaq (tech-heavy)', 22, CORAL, 900, a=fade(t, L[0] + 4.3))
        c.text(1000, py(d.iloc[-1]) + 40, 'Dow', 22, GOLD, 900, a=fade(t, L[0] + 4.3))
    c.text(640, 518, '2026, start of year = 100', 18, MUTED, 700, a=fade(t, 0.5))
    if t > L[1]:
        if len(L) < 3 or t < L[2]:
            chip(c, 640, 556, f'Nasdaq: {NDQ_DD:.1f}% from its Oct 6 record', CORAL, pop(t, L[1] + 0.3), 24)
    if len(L) > 2 and t > L[2]:
        chip(c, 640, 556, f'2026: Nasdaq peak +{NDQ_PEAK_YTD:.0f}%, now +{NDQ_YTD:.1f}%', CORAL, pop(t, L[2] + 0.3), 24)
    source(c, t, SRC)


def s_history(c, x):
    t, L = x.t, x.L
    specks(c, t, 108)
    head(c, t, 'S&P 500 drops from a record, 1950 to today')
    tiers = [(N8, 'fell 8% or more', GOLD), (N10, 'kept going to 10%+', CORAL), (N20, 'became a 20%+ bear market', CORAL_D)]
    for i, (n, lab, col) in enumerate(tiers):
        at = L[min(i, len(L) - 1)] + (0.4 if i < len(L) else 2.5 * i)
        if t < at:
            continue
        y = 190 + i * 130
        for j in range(n):
            kk = pop(t, at + j * 0.03)
            cx = 150 + (j % 38) * 26
            c.circle(cx, y, 10 * clamp(kk), col, None, 0, a=clamp(kk))
        c.text(150, y + 42, f'{n} {lab}', 26, WHITE, 900, anchor='lm', a=fade(t, at + 0.6))
    if len(L) > 3 and t > L[3]:
        chip(c, 640, 560, f'about 7 in 10 drops that reached 8% never became a bear market', MINT, pop(t, L[3] + 0.3), 22)
    source(c, t, 'Yahoo Finance: S&P 500 daily closes since 1950; our calculation')


def s_streaks(c, x):
    t, L = x.t, x.L
    specks(c, t, 109)
    head(c, t, 'After a 6-day losing streak (S&P 500, since 1950)')
    k = pop(t, L[0] + 0.3)
    if k > 0:
        c.text(330, 260, f'{N6}', int(130 * (0.6 + 0.4 * clamp(k))), GOLD, 900, a=clamp(k), stroke=6)
        c.text(330, 350, 'six-day losing streaks', 26, WHITE, 800, a=clamp(k))
        c.text(330, 390, f'the last one: {LAST6:%B %Y}', 22, MUTED, 800, a=clamp(k))
    if t > L[1]:
        kk = pop(t, L[1] + 0.3)
        c.text(920, 250, f'{UP6} of {len(F12)}', 80, MINT, 900, a=clamp(kk), stroke=5)
        c.text(920, 330, 'times, stocks were higher', 26, WHITE, 800, a=clamp(kk))
        c.text(920, 365, 'one year later', 26, WHITE, 800, a=clamp(kk))
    if len(L) > 2 and t > L[2]:
        chip(c, 920, 450, f'median gain: {MED6:+.0f}%', MINT, pop(t, L[2] + 0.3), 26)
        pulse(c, t, (760, 415, 1080, 485), MINT, 30)
    if len(L) > 3 and t > L[3]:
        chip(c, 640, 560, f'but {len(F12) - UP6} times, they were still lower', CORAL, pop(t, L[3] + 0.3), 24)
    source(c, t, 'Yahoo Finance: S&P 500 daily closes; prices only, no dividends')


def s_normal(c, x):
    t, L = x.t, x.L
    specks(c, t, 110)
    head(c, t, 'Drops happen almost every year')
    iy = IY.loc[2006:] * 100
    yr = (HS.resample('YE').last().pct_change() * 100)['2006':'2025']; yr.index = yr.index.year
    n = len(iy)
    bw = 1000 / n
    show = n if t > L[0] + 5 else int(max(0, t - L[0] - 0.3) * 5)
    for i in range(min(show, n)):
        x0 = 140 + i * bw
        dv = iy.iloc[i]
        c.rrect(x0 + 6, 330, x0 + bw - 6, 330 - dv * 4, 4, CORAL)
        rv = yr.iloc[i]
        top = 330 - max(0, rv) * 4
        c.rrect(x0 + 6, top, x0 + bw - 6, 330 if rv >= 0 else 330 - rv * 4, 4, MINT if rv >= 0 else CORAL_D, a=0.85)
        c.text(x0 + bw / 2, 580, f"'{iy.index[i] % 100:02d}", 15, MUTED, 700, shadow=False)
    c.line([(140, 330), (1140, 330)], (255, 255, 255, 90), 2)
    c.text(140, 112, 'green: the year\'s gain   red: its worst drop along the way', 19, WHITE, 700, anchor='lm',
           a=fade(t, 0.5))
    if L[1] < t < (L[2] if len(L) > 2 else 1e9):
        chip(c, 640, 165, f'typical drop within a year (since 1950): {IY_MED:.0f}%', CORAL, pop(t, L[1] + 0.3), 22)
    if len(L) > 2 and t > L[2]:
        chip(c, 640, 165, f'yet {UP_YEARS} of {ALL_YEARS} years ended higher', MINT, pop(t, L[2] + 0.3), 26)
    source(c, t, 'Yahoo Finance: S&P 500 closes; prices only')


def s_best(c, x):
    t, L = x.t, x.L
    specks(c, t, 111)
    head(c, t, 'The best days hide next to the worst ones')
    k = pop(t, L[0] + 0.3)
    if k > 0:
        c.text(640, 250, f'{NEAR} of 10', 120, GOLD, 900, a=clamp(k), stroke=6)
        c.text(640, 340, 'best days since 1950 came within 2 weeks', 28, WHITE, 800, a=clamp(k))
        c.text(640, 380, 'of one of the 20 worst days', 28, WHITE, 800, a=clamp(k))
    if t > L[1]:
        rows = list(BEST10.items())[:4]
        for i, (d, v) in enumerate(rows):
            kk = pop(t, L[1] + 0.4 + 0.8 * i)
            chip(c, 250 + i * 260, 480, f'{d:%b %Y}: +{v * 100:.1f}%', MINT, kk, 20)
    if len(L) > 2 and t > L[2]:
        chip(c, 640, 555, 'selling in a panic can mean missing the rebound', SKY, pop(t, L[2] + 0.3), 24)
    source(c, t, 'Yahoo Finance: S&P 500 daily closes since 1950; our calculation')


def s_you(c, x):
    t, L = x.t, x.L
    specks(c, t, 112)
    head(c, t, 'What it means for your money')
    items = [('piggy-bank', 'Money you need\nsoon: not in stocks'), ('calendar', 'Long-term money:\ntime matters most'),
             ('shuffle', 'Spread it out:\ndiversify'), ('shield', 'Emergency fund\nfirst')]
    icon_row(c, t, items, L[0] + 0.2, max(4.0, (L[-1] - L[0]) * 0.8), y=300, color=GOLD)
    c.text(640, 570, 'Education only, not financial advice', 18, MUTED, 700, a=fade(t, 1))


def s_index(c, x):
    t, L = x.t, x.L
    specks(c, t, 114)
    head(c, t, 'What these indexes are')
    cards = [('S&P 500', '500 of the biggest\nU.S. companies', GOLD), ('Dow Jones', '30 big, well-known\ncompanies', SKY),
             ('Nasdaq', 'thousands of stocks,\nheavy in tech', CORAL)]
    for i, (n, d, col) in enumerate(cards):
        k = pop(t, L[0] + 0.4 + 1.8 * i)
        if k <= 0:
            continue
        cx = 260 + i * 380
        c.rrect(cx - 160, 170, cx + 160, 420, 26, (255, 255, 255, 18), col, 4, a=clamp(k))
        c.text(cx, 230, n, 38, col, 900, a=clamp(k))
        for j, part in enumerate(d.split('\n')):
            c.text(cx, 310 + j * 38, part, 26, WHITE, 800, a=clamp(k))
    if len(L) > 1 and t > L[1]:
        c.icon('wallet', 330, 520, 60, GOLD, a=fade(t, L[1] + 0.3))
        chip(c, 720, 520, 'in a 401(k) or index fund? you likely own these', GOLD, pop(t, L[1] + 0.3), 22)


def s_dollars(c, x):
    t, L = x.t, x.L
    specks(c, t, 115)
    head(c, t, '$10,000 in an S&P 500 fund (prices only)')
    k = pop(t, L[0] + 0.3)
    if k > 0:
        c.rrect(140, 150, 620, 470, 26, (255, 255, 255, 16), CORAL, 4, a=clamp(k))
        c.text(380, 205, f'bought at the record ({SP_REC_D:%b %d})', 24, WHITE, 800, a=clamp(k))
        c.text(380, 320, f'${K_REC:,.0f}', 84, CORAL, 900, a=clamp(k), stroke=5)
        c.text(380, 410, 'today', 26, MUTED, 800, a=clamp(k))
    if t > L[1]:
        kk = pop(t, L[1] + 0.3)
        c.rrect(660, 150, 1140, 470, 26, (255, 255, 255, 16), MINT, 4, a=clamp(kk))
        c.text(900, 205, f'bought 10 years ago ({D_10Y:%b %Y})', 24, WHITE, 800, a=clamp(kk))
        c.text(900, 320, f'${K_10Y:,.0f}', 84, MINT, 900, a=clamp(kk), stroke=5)
        c.text(900, 410, 'today, even after this drop', 26, MUTED, 800, a=clamp(kk))
    if len(L) > 2 and t > L[2]:
        chip(c, 640, 540, 'the starting point matters less, the longer you hold', SKY, pop(t, L[2] + 0.3), 24)
    source(c, t, SRC)


def s_past(c, x):
    t, L = x.t, x.L
    specks(c, t, 116)
    head(c, t, 'Two recent drops, and how long they lasted')
    rows = [('2020', C20, C20_LOW, C20_REC, C20_YR, SKY), ('2022', C22, C22_LOW, C22_REC, C22_YR, CORAL)]
    for i, (y, dd, lo, rec, yr, col) in enumerate(rows):
        k = pop(t, L[i] + 0.3)
        if k <= 0:
            continue
        yy = 190 + i * 190
        c.rrect(140, yy - 70, 1140, yy + 80, 24, (255, 255, 255, 16), col, 4, a=clamp(k))
        c.text(230, yy, y, 56, col, 900, a=clamp(k))
        c.text(360, yy - 30, f'fell {abs(dd):.0f}% (low {lo:%b %d})', 30, WHITE, 900, anchor='lm', a=clamp(k))
        c.text(360, yy + 15, f'new record: {rec:%b %Y}', 28, MINT if (rec - lo).days < 365 else GOLD, 900,
               anchor='lm', a=clamp(k))
        c.text(360, yy + 52, f'the year ended {yr:+.0f}%', 22, MUTED, 800, anchor='lm', a=clamp(k))
    if len(L) > 2 and t > L[2]:
        chip(c, 640, 560, f'typical 10-20% correction since 1950: ~{CORR_DAYS / 30.4:.0f} months back to a record', GOLD,
             pop(t, L[2] + 0.3), 22)
    source(c, t, 'Yahoo Finance: S&P 500 daily closes; our calculation')


def s_watch(c, x):
    t, L = x.t, x.L
    specks(c, t, 117)
    head(c, t, 'What to watch next')
    items = [('landmark', '10-year\nTreasury yield'), ('shopping-cart', 'Inflation\nreports'),
             ('percent', 'The Fed in\nDecember'), ('briefcase', 'Jobs and\nprofits')]
    icon_row(c, t, items, L[0] + 0.2, max(4.0, (L[-1] - L[0]) * 0.85), y=300, color=SKY)


def s_recap(c, x):
    t, L = x.t, x.L
    specks(c, t, 113)
    head(c, t, 'Recap')
    pts = [f'S&P 500: {STREAK} losses in a row, {SP_DD:.0f}% from record',
           f'Nasdaq in a correction ({NDQ_DD:.0f}%), Dow below 50,000',
           f'Bonds pay {Y_NOW:.1f}%, inflation {INFL:.1f}%, the Fed hiked',
           f'Since 1950: {N8} drops of 8%+, {N20} bear markets',
           f'After 6-day streaks: higher a year later {UP6} of {len(F12)} times']
    step = max(1.6, (L[1] - L[0] - 0.5) / len(pts)) if len(L) > 1 else 2.0
    for i, p in enumerate(pts):
        k = pop(t, L[0] + 0.3 + step * i)
        if k > 0:
            c.circle(170, 170 + i * 80, 10, GOLD, a=clamp(k))
            c.text(200, 170 + i * 80, p, 28, WHITE, 800, anchor='lm', a=clamp(k))
    if len(L) > 1 and t > L[1]:
        chip(c, 640, 600, 'Is a crash coming? Yes or no: tell us in the comments', GOLD, pop(t, L[1] + 0.3), 24)


def ticker(draw):
    """A scrolling market ticker along the top: keeps the frame alive while a chart is being explained."""
    def wrapped(c, x):
        draw(c, x)
        c.rrect(0, 0, W, 40, 0, (8, 10, 20, 210))
        sz = 15
        w = len(TICK) * sz * 0.62
        off = (x.t * 45) % w
        for k in range(3):
            c.text(-off + k * w, 28, TICK, sz, GOLD, 800, anchor='lm', shadow=False)
    return wrapped


SCENES = [
    dict(draw=s_hook, chapter=f'Intro: {STREAK} days down', lead=0.15, gap=0.3, lines=[
        f"!The S&P 500 just fell {STREAK} days in a row.",
        f"It's now {abs(SP_DD):.1f} percent below its record. The Dow is {abs(DOW_DD):.1f} percent down, and the "
        f"Nasdaq is down {abs(NDQ_DD):.1f} percent, which puts it in what Wall Street calls a correction.",
        "So is a crash coming? Here's the short answer from history.",
        f"!Since 1950, the S&P 500 has fallen 8 percent or more from a record {N8} times. Only {N20} of those turned "
        "into a bear market. Most drops this size ended without a crash.",
    ], punch=lambda L: [L[0] + 0.1, L[3] + 0.3],
        sfx=lambda L: [(L[0] + 0.1, 'hit'), (L[1] + 0.4, 'pop'), (L[1] + 2.0, 'pop'), (L[1] + 3.6, 'pop'),
                       (L[2] + 0.2, 'whoosh'), (L[3] + 0.3, 'hit'), (L[3] + 3.5, 'ding')]),
    dict(draw=s_promise, lines=[
        "But most isn't all. In this video: what happened this week, why stocks are falling, what history says "
        "about drops like this, and what it means for your money. If that's useful, subscribe: we break down "
        "money news like this every day.",
    ], sfx=lambda L: [(L[0] + 0.5 + 1.4 * i, 'pop') for i in range(4)]),
    dict(draw=s_week, chapter='What happened this week', lines=[
        f"Let's start with this week. On {LAST7.index[0]:%B} {LAST7.index[0].day}, the S&P 500 closed at "
        f"{ST0:,.0f}. Then it fell. And fell again. {STREAK} trading days, {STREAK} losses.",
        f"Over those {STREAK} days, the index dropped {abs(ST_PCT):.1f} percent.",
        f"Today alone, it fell {abs(SP_DAY):.1f} percent, and the Dow lost about {abs(DOW_DAY_PTS):,.0f} points.",
        f"To put that in dollars: if you had 10,000 dollars in an S&P 500 index fund on {LAST7.index[0]:%B} "
        f"{LAST7.index[0].day}, it was worth about {10000 * (1 + ST_PCT / 100):,.0f} dollars at today's close.",
    ], sfx=lambda L: [(L[0] + 0.3 + i / 1.4, 'down') for i in range(1, 7)] + [(L[1] + 0.3, 'pop'), (L[2] + 0.3, 'hit'),
                                                                              (L[3] + 0.3, 'ding')]),
    dict(draw=s_index, chapter='What the indexes are', lines=[
        "Quick refresher. The S&P 500 tracks 500 of the biggest U.S. companies. The Dow tracks just 30 big, "
        "well-known ones. And the Nasdaq Composite holds thousands of stocks, with a lot of tech.",
        "If you have a 401(k) or an index fund, there's a good chance you own a slice of these companies. So when "
        "the indexes fall, your balance usually falls with them.",
    ], sfx=lambda L: [(L[0] + 0.4, 'pop'), (L[0] + 2.2, 'pop'), (L[0] + 4.0, 'pop'), (L[1] + 0.3, 'ding')]),
    dict(draw=s_terms, chapter='Pullback, correction, bear market', lines=[
        "Here's how far each of the big three indexes is below its record high.",
        "Wall Street has names for these drops. Down 10 percent from a record is called a correction. Down 20 "
        "percent is a bear market.",
        f"!The Nasdaq, packed with tech stocks, is down {abs(NDQ_DD):.1f} percent from its October 6 record. That's "
        "a correction.",
        f"The S&P 500 isn't there yet. And the Dow, which first closed above 50,000 in February, fell back below "
        f"it today, for the first time since {DOW_BELOW_SINCE:%B}.",
        f"For the S&P 500 to officially enter a correction, it would have to close below about {CORR_LINE:,.0f}. "
        f"Today it closed at {SP_NOW:,.0f}.",
    ], punch=lambda L: [L[2] + 0.3], sfx=lambda L: [(L[0] + 0.3, 'pop'), (L[0] + 1.5, 'pop'), (L[0] + 2.7, 'pop'),
                                                    (L[1] + 0.5, 'whoosh'), (L[1] + 3.0, 'whoosh'), (L[2] + 0.3, 'hit'),
                                                    (L[3] + 0.3, 'pop')]),
    dict(draw=s_dollars, chapter='What it means in dollars', lines=[
        f"In dollars: 10,000 dollars put into an S&P 500 fund at the October 6 record is worth about "
        f"{K_REC:,.0f} dollars today.",
        f"But 10,000 dollars put in ten years ago, in {D_10Y:%B %Y}, is worth about {K_10Y:,.0f} dollars today, "
        "even after this drop. Both numbers count prices only, not dividends.",
        "Same index, very different feelings. What matters most is how long you hold, not the week you're in.",
    ], sfx=lambda L: [(L[0] + 0.3, 'down'), (L[1] + 0.3, 'ding'), (L[2] + 0.3, 'pop')]),
    dict(draw=s_yields, chapter='Why: bonds pay 5%', lines=[
        f"So why are stocks falling? Reason one: interest rates. The 10-year Treasury yield, what the U.S. "
        f"government pays to borrow for ten years, is at {Y_NOW:.2f} percent.",
        f"A year ago, it was {Y_1Y:.2f} percent.",
        f"!Think about it from an investor's side. A government bond now pays over 5 percent a year, with almost no "
        "risk. A stock promises nothing. So when safe bonds pay this much, stocks have to compete, and investors "
        "pay less for them.",
    ], punch=lambda L: [L[2] + 0.3], sfx=lambda L: [(L[0] + 0.3, 'whoosh'), (L[0] + 4.8, 'ding'), (L[1] + 0.3, 'pop'),
                                                    (L[2] + 0.3, 'hit'), (L[2] + 3.0, 'pop')]),
    dict(draw=s_fed, chapter='Why: inflation and the Fed', lines=[
        f"Reason two: inflation. Prices rose {INFL:.1f} percent in the year to October, according to the "
        "Consumer Price Index.",
        f"To fight it, the Federal Reserve raised its interest rate on {HIKE:%B} {HIKE.day}, its first hike since "
        f"2023, back to {FEDL.iloc[-1]:.2f} to {FEDU.iloc[-1]:.2f} percent.",
        "Higher rates make borrowing more expensive for companies and families. That can slow spending and "
        "profits, and stock prices follow profits.",
        f"It's already hitting wallets. The average 30-year mortgage rate is {MORT_NOW:.2f} percent, up from "
        f"{MORT_1Y:.2f} a year ago, according to Freddie Mac. And the prime rate, the base for most credit card "
        f"rates, is {PRIME:.0f} percent.",
    ], sfx=lambda L: [(L[0] + 0.3, 'hit'), (L[1] + 0.3, 'whoosh'), (L[1] + 3.8, 'pop'), (L[2] + 0.3, 'pop')]),
    dict(draw=s_tech, chapter='Why: the winners fell hardest', lines=[
        "Reason three: the stocks that rose the most are falling the most. Look at the tech-heavy Nasdaq against "
        "the Dow this year.",
        f"The Nasdaq ran up faster, and since its October record it has fallen {abs(NDQ_DD):.1f} percent. When "
        "investors take profits, the biggest winners usually drop first, and fastest.",
        f"At its peak this year, the Nasdaq was up {NDQ_PEAK_YTD:.1f} percent. Now it's up just {NDQ_YTD:.1f} percent "
        f"for 2026. The Dow was up as much as {DOW_PEAK_YTD:.1f} percent, and now it's up {DOW_YTD:.1f}.",
    ], sfx=lambda L: [(L[0] + 0.3, 'whoosh'), (L[1] + 0.3, 'down')]),
    dict(draw=s_history, chapter='What history says', lines=[
        f"Now the big question. Does a drop like this turn into a crash? We looked at every S&P 500 decline since "
        f"1950. {N8} times, the index fell 8 percent or more from a record.",
        f"{N10} of those kept going to 10 percent or more.",
        f"!And {N20} became bear markets, with drops of 20 percent or more.",
        f"So roughly 7 out of 10 drops that reached 8 percent never became bear markets. But about 3 in 10 did, so "
        "nobody can promise this one stops here.",
    ], punch=lambda L: [L[2] + 0.4], sfx=lambda L: [(L[0] + 0.4, 'pop'), (L[1] + 0.4, 'pop'), (L[2] + 0.4, 'hit'),
                                                    (L[3] + 0.3, 'ding')]),
    dict(draw=s_past, chapter='Two recent drops', lines=[
        f"Let's look at the two most recent big drops. In 2020, when the pandemic hit, the S&P 500 fell "
        f"{abs(C20):.0f} percent in about a month, to a low on {C20_LOW:%B} {C20_LOW.day}. It was back at a record "
        f"by {C20_REC:%B} {C20_REC.day}, and the year ended {C20_YR:.0f} percent higher.",
        f"2022 was different. Inflation and rate hikes pushed the index down {abs(C22):.0f} percent by "
        f"{C22_LOW:%B}. It didn't reach a new record until {C22_REC:%B %Y}, more than a year later.",
        f"For a typical correction, between 10 and 20 percent, the S&P 500 took about {CORR_DAYS / 30.4:.0f} months "
        "to get from its old record back to a new one. Some drops heal fast. Some take years.",
    ], sfx=lambda L: [(L[0] + 0.3, 'pop'), (L[1] + 0.3, 'pop'), (L[2] + 0.3, 'ding')]),
    dict(draw=s_streaks, chapter='After 6-day losing streaks', lines=[
        f"What about losing streaks? Since 1950, the S&P 500 has had {N6} six-day losing streaks. The last one "
        f"before this week was in {LAST6:%B %Y}.",
        f"!A year after those streaks, stocks were higher {UP6} times out of {len(F12)}.",
        f"The median gain over that year was about {MED6:.0f} percent, not counting dividends.",
        f"But {len(F12) - UP6} times, stocks were still lower a year later. Streaks tell you how people feel. They "
        "don't predict the future.",
        f"That {LAST6:%B %Y} streak ended with the S&P 500 near {LAST6_CLOSE:,.0f}. A year later, it was about "
        f"{LAST6_1Y:.0f} percent higher.",
    ], punch=lambda L: [L[1] + 0.3], sfx=lambda L: [(L[0] + 0.3, 'pop'), (L[1] + 0.3, 'hit'), (L[2] + 0.3, 'ding'),
                                                    (L[3] + 0.3, 'down')]),
    dict(draw=s_normal, chapter='Drops are normal', lines=[
        "Here's something most people don't know. Big drops happen almost every year, even in good years. The red "
        "bars show each year's worst drop. The green bars show where the year ended.",
        f"Since 1950, the typical year had a drop of about {abs(IY_MED):.0f} percent along the way.",
        f"!And yet, {UP_YEARS} of the last {ALL_YEARS} full years ended higher.",
    ], punch=lambda L: [L[2] + 0.3], sfx=lambda L: [(L[0] + 0.3, 'whoosh'), (L[1] + 0.3, 'pop'), (L[2] + 0.3, 'ding')]),
    dict(draw=s_best, chapter='Best days, worst days', lines=[
        f"One more pattern. Of the 10 best days for the S&P 500 since 1950, {NEAR} came within two weeks of one of "
        "the 20 worst days.",
        f"The best day of all, a {BEST10.iloc[0] * 100:.1f} percent gain, came in {BEST10.index[0]:%B %Y}, right in "
        "the middle of the financial crisis.",
        "That's why selling in a panic can be costly: the rebound often comes when things look worst.",
    ], sfx=lambda L: [(L[0] + 0.3, 'hit'), (L[1] + 0.4, 'pop'), (L[1] + 1.2, 'pop'), (L[1] + 2.0, 'pop'),
                      (L[1] + 2.8, 'pop'), (L[2] + 0.3, 'pop')]),
    dict(draw=s_watch, chapter='What to watch next', lines=[
        "So what decides where stocks go from here? Here are four things to watch. First, the 10-year Treasury "
        "yield. If it keeps climbing past 5 percent, stocks face more pressure. If it falls, they get relief.",
        "Second, the next inflation reports. Third, the Federal Reserve's meeting in December, where it decides "
        "whether to raise rates again. And fourth, jobs and company profits: as long as people are working and "
        "companies are earning, a drop is less likely to turn into a recession.",
    ], sfx=lambda L: [(L[0] + 0.3, 'pop'), (L[1] + 0.3, 'pop'), (L[1] + 3.0, 'pop'), (L[1] + 6.0, 'pop')]),
    dict(draw=s_you, chapter='What it means for you', lines=[
        "So what does this mean for you? Here's what most financial educators point to. Money you'll need in the "
        "next few years usually doesn't belong in stocks, because a drop like this can come at the wrong moment.",
        "For long-term money, time has mattered more than timing. Spreading money across many investments limits "
        "the damage from any one of them. And an emergency fund means you never have to sell at the bottom.",
        "And if you invest every month, through a 401(k) for example, lower prices mean each contribution buys "
        "more shares.",
    ], sfx=lambda L: [(L[0] + 0.5, 'pop'), (L[0] + 3.0, 'pop'), (L[1] + 0.3, 'pop'), (L[1] + 4.0, 'pop')]),
    dict(draw=s_recap, chapter='Recap', lines=[
        f"Let's recap. The S&P 500 fell {STREAK} days in a row and is {abs(SP_DD):.0f} percent below its record. "
        f"The Nasdaq is in a correction. Bonds pay {Y_NOW:.1f} percent, inflation is {INFL:.1f} percent, and the "
        f"Fed is raising rates. History says most drops like this don't become crashes, but some do.",
        "!So what do you think: is a crash coming? Yes or no, tell me in the comments. And subscribe so you don't "
        "miss tomorrow's update.",
        "This video is for education only. It's not financial advice.",
    ], punch=lambda L: [L[1] + 0.3], sfx=lambda L: [(L[0] + 0.3 + 2.5 * j, 'pop') for j in range(5)]
        + [(L[1] + 0.3, 'ding')]),
]
for _sc in SCENES:
    _sc['draw'] = ticker(_sc['draw'])
SHORTS = {}


def check_numbers():
    script = ' '.join(l for sc in SCENES for l in sc['lines'])
    assert TODAY.strftime('%Y-%m-%d') == '2026-11-19', TODAY
    assert STREAK >= 6 and SP_DD < -5 and NDQ_DD <= -10 and DOW_NOW < 50000 < DOW_REC
    assert SP_REC_D.strftime('%Y-%m-%d') == NDQ_REC_D.strftime('%Y-%m-%d') == '2026-10-06'
    assert DOW_REC_D.strftime('%Y-%m-%d') == '2026-08-05' and DOW[DOW > 50000].index[0].strftime('%Y-%m') == '2026-02'
    assert N8 > N10 > N20 and 0.6 < 1 - N20 / N8 < 0.8, (N8, N10, N20)
    assert HIKE.strftime('%Y-%m-%d') == '2026-09-17' and FEDU[:HIKE - pd.Timedelta(days=1)][FEDU.diff() > 0].index[-1].year == 2023
    assert Y_NOW > 5 and 3.8 < INFL < 4.4 and NEAR >= 7
    assert round(MORT_NOW, 2) == 7.28 and round(MORT_1Y, 2) == 6.24 and PRIME == 7.0 and round(CORR_LINE) == 7037
    assert round(NDQ_PEAK_YTD, 1) == 18.7 and round(NDQ_YTD, 1) == 2.7 and round(DOW_PEAK_YTD, 1) == 13.1 and round(DOW_YTD, 1) == 2.2
    assert round(K_REC) == 9178 and round(K_10Y) == 32888 and round(LAST6_CLOSE) == 4967 and round(LAST6_1Y) == 8
    assert (round(C20, 1), C20_LOW.strftime('%Y-%m-%d'), C20_REC.strftime('%Y-%m-%d'), round(C20_YR)) == (-33.9, '2020-03-23', '2020-08-18', 16)
    assert (round(C22, 1), C22_LOW.strftime('%Y-%m-%d'), C22_REC.strftime('%Y-%m-%d')) == (-25.4, '2022-10-12', '2024-01-19')
    for s in ('not financial advice', 'correction', 'bear market', 'Consumer Price Index', 'since 1950'):
        assert s in script, s
    print(f'numbers check: OK  S&P {SP_NOW:,.2f} ({SP_DAY:+.2f}% today, streak {STREAK}, {ST_PCT:.2f}%), '
          f'{SP_DD:.2f}% from {SP_REC:,.2f}; Dow {DOW_NOW:,.2f} {DOW_DD:.2f}% ({DOW_DAY_PTS:+,.0f} pts), below 50k '
          f'first since {DOW_BELOW_SINCE:%Y-%m-%d}; Nasdaq {NDQ_DD:.2f}%; 10y {Y_NOW:.2f}% ({Y_DATE:%b %d}) vs '
          f'{Y_1Y:.2f}%; CPI {INFL:.2f}%; 8%+ {N8}, 10%+ {N10}, 20%+ {N20}; corr median {CORR_DAYS:.0f} d; '
          f'6-day streaks {N6}, up 12m {UP6}/{len(F12)} med {MED6:.1f}%, last {LAST6:%Y-%m-%d}; intra-yr drop '
          f'{IY_MED:.1f}%, up years {UP_YEARS}/{ALL_YEARS}; best-near-worst {NEAR}/10')


if __name__ == '__main__':
    check_numbers()
    os.makedirs(BUILD, exist_ok=True)
    if '--check' in sys.argv:
        sys.exit()
    if '--stills' in sys.argv:
        previews(SCENES, SHORTS, os.path.join(BUILD, 'previews'))
        sys.exit()
    only = [int(a) for a in sys.argv[sys.argv.index('--only') + 1].split(',')] if '--only' in sys.argv else None
    total, chapters = build(SCENES, os.path.join(OUT, 'ep10_stocks.mp4'), BUILD, only=only,
                            srt_path=os.path.join(OUT, 'ep10_stocks.en.srt'))
    with open(os.path.join(OUT, 'ep10_chapters.txt'), 'w') as f:
        for at, name in chapters:
            f.write(f'{fmt_time(at)} {name}\n')
    print(f'total {total / 60:.1f} min')
