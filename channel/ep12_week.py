"""Episode 12: The Nasdaq's worst week since 2020. What happens after a correction? (long video, Sat Nov 21 2026)

    python3 channel/ep12_week.py [--check] [--stills] [--only 3,5]

Data (check_numbers recomputes everything from the files):
- channel/data/GSPC_max.csv, IXIC_max.csv, DJI_max.csv, VIX_max.csv: Yahoo Finance chart API daily closes (S&P 500,
  Nasdaq Composite, Dow Jones Industrial Average, Cboe VIX), through Fri Nov 20 2026.
- FRED: DGS10 (10-year Treasury yield), DFEDTARU/DFEDTARL, CPIAUCSL, MORTGAGE30US.
History statistics are our calculations from S&P 500 closes since 1950 (prices only, no dividends). A correction
is a close 10%+ below the prior record; it counts as finished once the index closes at a new record.
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
BUILD = os.path.join(HERE, 'build', 'ep12_week')


def load(name):
    return pd.read_csv(os.path.join(HERE, 'data', f'{name}_max.csv'), parse_dates=['date']).set_index('date')['close']


SPX, NDQ, DOW, VIX = load('GSPC'), load('IXIC'), load('DJI'), load('VIX')
FRI = SPX.index[-1]
SP_NOW, NDQ_NOW, DOW_NOW, V_NOW = SPX.iloc[-1], NDQ.iloc[-1], DOW.iloc[-1], VIX.iloc[-1]
SP_REC, SP_REC_D = SPX.max(), SPX.idxmax()
NDQ_REC = NDQ.max()
DOW_REC, DOW_REC_D = DOW.max(), DOW.idxmax()
SP_DD = (SP_NOW / SP_REC - 1) * 100
NDQ_DD = (NDQ_NOW / NDQ_REC - 1) * 100
DOW_DD = (DOW_NOW / DOW_REC - 1) * 100


def weekly(s):
    w = s.resample('W-FRI').last().pct_change() * 100
    worst_since = w[:-1][w[:-1] <= w.iloc[-1]].index[-1]
    return w.iloc[-1], worst_since


SP_WK, SP_WK_SINCE = weekly(SPX)
NDQ_WK, NDQ_WK_SINCE = weekly(NDQ)
DOW_WK, _ = weekly(DOW)
WEEK = SPX[FRI - pd.Timedelta(days=4):]
WEEK_CH = (WEEK / SPX.shift(1).reindex(WEEK.index) - 1) * 100
NDQ_FRI = (NDQ.iloc[-1] / NDQ.iloc[-2] - 1) * 100
SP_FRI = WEEK_CH.iloc[-1]
K_WEEK = 10000 * (1 + SP_WK / 100)
K_REC = 10000 * SP_NOW / SP_REC

# S&P 500 corrections since 1950 (finished ones only: the index got back to a record)
HS = SPX['1950':]
_eps, _in = [], False
for d, v in (HS / HS.cummax() - 1).items():
    if not _in and v < 0:
        _in, st, dep, low, hit = True, d, v, d, None
    elif _in:
        if v < dep:
            dep, low = v, d
        if v <= -0.10 and hit is None:
            hit = d
        if v == 0:
            _eps.append((st, hit, low, d, dep))
            _in = False
EPS = pd.DataFrame(_eps, columns=['start', 'hit', 'low', 'rec', 'depth'])
C = EPS[EPS.hit.notna()].copy()
C['r12'] = [HS.iloc[HS.index.get_loc(d) + 252] / HS[d] - 1 if HS.index.get_loc(d) + 252 < len(HS) else np.nan
            for d in C.hit]
N_CORR = len(C)
N_BEAR = int((C.depth <= -0.20).sum())
N_STOP = N_CORR - N_BEAR
NB = C[C.depth > -0.20]
NB_DEPTH = float(NB.depth.median()) * 100
NB_TO_LOW = float((NB.low - NB.hit).dt.days.median())
NB_TO_REC = float((NB.rec - NB.hit).dt.days.median())
UP12 = int((C.r12 > 0).sum())
N12 = int(C.r12.notna().sum())
MED12 = float(C.r12.median()) * 100
RECENT = C[C.start >= '2015-01-01']

# worst weeks since 1950
WK = HS.resample('W-FRI').last().pct_change().dropna()
BAD = WK[WK <= SP_WK / 100]
_bad_prev = [d for d in BAD.index if d < FRI - pd.Timedelta(days=2)]
F_BAD = []
for d in _bad_prev:
    i = HS.index.get_indexer([d], method='pad')[0]
    if i + 252 < len(HS):
        F_BAD.append(HS.iloc[i + 252] / HS.iloc[i] - 1)
BAD_UP, BAD_MED = sum(x > 0 for x in F_BAD), float(np.median(F_BAD)) * 100

def wk(name):
    q = load(name)
    a, b = q[:'2026-11-13'].iloc[-1], q[:'2026-11-20'].iloc[-1]
    return b, (b / a - 1) * 100, (b / q.max() - 1) * 100, q.idxmax()


GOLD_P, GOLD_WK, GOLD_DD, GOLD_REC_D = wk('GCF')
BTC_P, BTC_WK, BTC_DD, BTC_REC_D = wk('BTC')
DXY_P, DXY_WK, _, _ = wk('DXY')
BEST12, BEST12_D = float(C.r12.max()) * 100, C.loc[C.r12.idxmax(), 'hit']
WORST12, WORST12_D = float(C.r12.min()) * 100, C.loc[C.r12.idxmin(), 'hit']
Y10 = series('DGS10')
Y_WK0, Y_WK1, Y_WK1_D = Y10[:'2026-11-13'].iloc[-1], Y10.iloc[-1], Y10.index[-1]
Y_NOW = Y10.iloc[-1]
Y_1Y = Y10[:Y10.index[-1] - pd.Timedelta(days=365)].iloc[-1]
CPI = series('CPIAUCSL')
INFL = (CPI.iloc[-1] / CPI.iloc[-13] - 1) * 100
FEDU, FEDL = series('DFEDTARU'), series('DFEDTARL')
HIKE = FEDU[FEDU.diff() > 0].index[-1]
MORT = series('MORTGAGE30US').iloc[-1]

SRC = 'Yahoo Finance daily closes: S&P 500, Nasdaq Composite, Dow Jones'
TICK = (f'WEEK:  S&P 500 {SP_WK:+.1f}%     NASDAQ {NDQ_WK:+.1f}%     DOW {DOW_WK:+.1f}%     VIX {V_NOW:.1f}     '
        f'10-YR {Y_NOW:.2f}%     S&P {SP_NOW:,.2f} ({SP_DD:.1f}% from record)     ')


def ticker(draw):
    def wrapped(c, x):
        draw(c, x)
        c.rrect(0, 0, W, 40, 0, (8, 10, 20, 210))
        w = len(TICK) * 15 * 0.62
        off = (x.t * 45) % w
        for k in range(3):
            c.text(-off + k * w, 28, TICK, 15, GOLD, 800, anchor='lm', shadow=False)
    return wrapped


def days_words(d):
    return f'about {d / 7:.0f} weeks' if d < 120 else f'about {d / 30.4:.0f} months'


# ------------------------------------------------------------------- scenes --
def s_hook(c, x):
    t, L = x.t, x.L
    specks(c, t, 141)
    k = pop(t, L[0] + 0.1, 0.3)
    if k > 0:
        c.text(640, 210, f'{NDQ_WK:.0f}%', int(170 * (0.6 + 0.4 * clamp(k))), CORAL, 900, a=clamp(k), stroke=8)
        c.text(640, 320, f'NASDAQ IN ONE WEEK: WORST SINCE {NDQ_WK_SINCE:%Y}', 36, WHITE, 900, a=clamp(k))
    if t > L[1]:
        chip(c, 640, 420, f'S&P 500: {SP_WK:.1f}% this week, {SP_DD:.1f}% from record', GOLD, pop(t, L[1] + 0.3), 26)
        if t > L[1] + 3.5:
            chip(c, 640, 500, 'officially a correction', CORAL, pop(t, L[1] + 3.5), 26)
    if len(L) > 2 and t > L[2]:
        c.rrect(0, 0, W, H, 0, (10, 14, 26, int(240 * fade(t, L[2]))))
        kk = pop(t, L[2] + 0.3)
        c.text(640, 220, f'{N_CORR} corrections since 1950', 60, GOLD, 900, a=clamp(kk), stroke=5)
        if t > L[2] + 3.0:
            c.text(640, 320, f'{N_STOP} stopped short of a bear market', 40, MINT, 900, a=fade(t, L[2] + 3.0), stroke=4)
        if len(L) > 3 and t > L[3]:
            c.text(640, 410, f'a year later: higher {UP12} of {N12} times', 40, MINT, 900, a=fade(t, L[3] + 0.3),
                   stroke=4)
            pulse(c, t, (300, 370, 980, 450), MINT, 30)


def s_promise(c, x):
    t, L = x.t, x.L
    specks(c, t, 142)
    penny(c, 200, 520, 100, t, 'thinking', talk=x.talk())
    items = ['The week, day by day', 'Why stocks fell', 'Every correction since 1950', 'What it means for you']
    for i, it in enumerate(items):
        k = pop(t, L[0] + 0.5 + 1.4 * i)
        if k > 0:
            c.rrect(420, 150 + i * 105, 1120, 230 + i * 105, 22, (255, 255, 255, 22), GOLD, 3, a=clamp(k))
            c.text(460, 190 + i * 105, f'{i + 1}', 40, GOLD, 900, a=clamp(k))
            c.text(510, 190 + i * 105, it, 34, WHITE, 800, anchor='lm', a=clamp(k))


def s_week(c, x):
    t, L = x.t, x.L
    specks(c, t, 143)
    head(c, t, 'S&P 500, day by day this week')
    days = list(WEEK_CH.items())
    for i, (d, ch) in enumerate(days):
        at = L[0] + 0.5 + i * 1.3 if t < L[1] else -1
        k = pop(t, at)
        if k <= 0:
            continue
        cx = 220 + i * 210
        hgt = abs(ch) * 85 * clamp(k)
        c.rrect(cx - 60, 170, cx + 60, 170 + hgt, 10, CORAL if ch < 0 else MINT)
        c.text(cx, 190 + hgt + 30, f'{ch:+.2f}%', 28, CORAL if ch < 0 else MINT, 900)
        c.text(cx, 150, f'{d:%a}', 26, WHITE, 900)
    if len(L) > 1 and t > L[1]:
        chip(c, 640, 560, f'the week: {SP_WK:.1f}%, worst since {SP_WK_SINCE:%B %Y}', CORAL, pop(t, L[1] + 0.3), 24)
    if len(L) > 2 and t > L[2]:
        c.rrect(0, 0, W, H, 0, (10, 14, 26, int(240 * fade(t, L[2]))))
        kk = pop(t, L[2] + 0.3)
        c.text(640, 250, f'${K_WEEK:,.0f}', 110, GOLD, 900, a=clamp(kk), stroke=6)
        c.text(640, 350, 'what $10,000 in an S&P 500 fund became this week', 28, WHITE, 800, a=clamp(kk))
        if len(L) > 3 and t > L[3]:
            chip(c, 640, 450, f'Friday alone: S&P {SP_FRI:.1f}%, Nasdaq {NDQ_FRI:.1f}%', CORAL, pop(t, L[3] + 0.3), 24)
    source(c, t, SRC)


def s_corr(c, x):
    t, L = x.t, x.L
    specks(c, t, 144)
    head(c, t, 'How far each index is below its record')
    items = [('S&P 500', -SP_DD, CORAL), ('Dow Jones', -DOW_DD, GOLD), ('Nasdaq', -NDQ_DD, CORAL)]
    compare_bars(c, t, items, L[0] + 0.3, 3.5, 25, lambda v: f'-{v:.1f}%', box=(200, 150, 820, 520))
    for i, (lvl, name, col) in enumerate(((10, 'correction', GOLD), (20, 'bear market', CORAL))):
        if t > L[1] + 0.3 + 2.0 * i:
            y = 520 - 370 * lvl / 25
            a = fade(t, L[1] + 0.3 + 2.0 * i)
            for xx in range(200, 830, 30):
                c.line([(xx, y), (xx + 16, y)], col, 3, a)
            c.text(850, y, f'-{lvl}%: {name}', 24, col, 900, anchor='lm', a=a)
    if len(L) > 2 and t > L[2]:
        chip(c, 1040, 300, 'S&P and Nasdaq: in correction', CORAL, pop(t, L[2] + 0.3), 22)
    if len(L) > 3 and t > L[3]:
        chip(c, 1040, 450, f'$10,000 at the record: ${K_REC:,.0f}', GOLD, pop(t, L[3] + 0.3), 22)
    source(c, t, SRC + f' (records: S&P and Nasdaq Oct 6, Dow {DOW_REC_D:%b %d})')


def s_why(c, x):
    t, L = x.t, x.L
    specks(c, t, 145)
    head(c, t, 'Why stocks fell')
    items = [('landmark', f'10-yr yield\n{Y_NOW:.2f}%'), ('shopping-cart', f'Inflation\n{INFL:.1f}%'),
             ('percent', f'Fed hiked\n{HIKE:%b %d}'), ('cpu', f'Tech unwind:\nNasdaq {NDQ_DD:.0f}%'),
             ('triangle-alert', f'Fear index\n{V_NOW:.0f}')]
    for i, (ic, lab) in enumerate(items):
        k = pop(t, L[min(i, len(L) - 1)] + (0.3 if i < len(L) else 2.5))
        if k <= 0:
            continue
        cx = 150 + i * 245
        on = L[min(i, len(L) - 1)] <= t < (L[i + 1] if i + 1 < len(L) else 1e9)
        col = CORAL if on else MUTED
        c.circle(cx, 260, 80 * clamp(k), (255, 255, 255, 30 if on else 12), col, 4 if on else 2)
        c.icon(ic, cx, 260, 70 * clamp(k), col)
        for j, part in enumerate(lab.split('\n')):
            c.text(cx, 380 + j * 32, part, 24, WHITE if on else MUTED, 900, a=clamp(k))
    source(c, t, 'FRED: DGS10, CPIAUCSL, DFEDTARU; Yahoo Finance: Nasdaq, VIX')


def s_where(c, x):
    t, L = x.t, x.L
    specks(c, t, 154)
    head(c, t, 'Where did the money go this week?')
    rows = [('Gold', GOLD_WK, f'${GOLD_P:,.0f} an ounce'), ('Bitcoin', BTC_WK, f'${BTC_P:,.0f}'),
            ('U.S. dollar index', DXY_WK, f'{DXY_P:.1f}'),
            ('10-year Treasury yield', None, f'{Y_WK0:.2f}% -> {Y_WK1:.2f}% (bond prices up)')]
    for i, (n, v, note) in enumerate(rows):
        k = pop(t, L[min(i, len(L) - 1)] + (0.3 if i < len(L) else 1.5 * i))
        if k <= 0:
            continue
        y = 140 + i * 105
        col = MINT if (v is None or v > 0) else CORAL
        c.rrect(120, y, 1160, y + 88, 20, (255, 255, 255, 16), col, 3, a=clamp(k))
        c.text(150, y + 44, n, 30, WHITE, 900, anchor='lm', a=clamp(k))
        if v is not None:
            c.text(700, y + 44, f'{v:+.1f}%', 36, col, 900, anchor='mm', a=clamp(k))
        c.text(1135, y + 44, note, 22, MUTED, 800, anchor='rm', a=clamp(k))
    source(c, t, 'Yahoo Finance: COMEX gold (GC=F), BTC-USD, U.S. dollar index; FRED: DGS10 (to Nov 19)')


def s_history(c, x):
    t, L = x.t, x.L
    specks(c, t, 146)
    head(c, t, f'S&P 500 corrections since 1950: {N_CORR}')
    for j, (_, r) in enumerate(C.iterrows()):
        k = pop(t, L[0] + 0.4 + 0.12 * j)
        if k <= 0:
            continue
        cx = 120 + j * 40
        hgt = -r.depth * 100 * 6 * clamp(k)
        bear = r.depth <= -0.20
        show_bear = len(L) > 1 and t > L[1]
        col = (CORAL_D if bear else MINT) if show_bear else GOLD
        c.rrect(cx - 14, 150, cx + 14, 150 + hgt, 6, col)
        if j % 3 == 0:
            c.text(cx, 140, f"'{r.hit.year % 100:02d}", 14, MUTED, 700, shadow=False)
    for lvl in (10, 20, 30, 50):
        y = 150 + lvl * 6
        c.line([(100, y), (1180, y)], (255, 255, 255, 40), 1.5)
        c.text(1190, y, f'-{lvl}%', 16, MUTED, 700, anchor='lm', shadow=False)
    if len(L) > 1 and t > L[1]:
        chip(c, 400, 560, f'{N_STOP} stopped before -20%', MINT, pop(t, L[1] + 0.3), 24)
        chip(c, 880, 560, f'{N_BEAR} became bear markets', CORAL, pop(t, L[1] + 1.5), 24)
    source(c, t, 'Yahoo Finance: S&P 500 closes since 1950; deepest drop of each correction; our calculation')


def s_time(c, x):
    t, L = x.t, x.L
    specks(c, t, 147)
    head(c, t, f'The {N_STOP} corrections that stopped before -20%: the typical path')
    pts = [(0, 0), (1, -10), (2, NB_DEPTH), (5, 0)]
    xs = [180 + p[0] * 190 for p in pts]
    ys = [180 - p[1] * 22 for p in pts]
    kk = clamp((t - L[0] - 0.3) / 3.0)
    n = 1 + int(kk * 3)
    c.line(list(zip(xs[:n + 1], ys[:n + 1])), GOLD, 6)
    labels = [('record', 0), ('-10%: correction', 1), (f'bottom: about {abs(NB_DEPTH):.0f}% down', 2), ('new record', 3)]
    for lab, i in labels:
        if i <= n:
            c.circle(xs[i], ys[i], 10, GOLD, WHITE, 2)
            c.text(xs[i], ys[i] + (40 if i in (1, 2) else -30), lab, 22, WHITE, 900)
    if len(L) > 1 and t > L[1]:
        chip(c, (xs[1] + xs[2]) / 2 + 40, 560, f'bottom: about {NB_TO_LOW:.0f} days after crossing -10%', CORAL,
             pop(t, L[1] + 0.3), 20)
    if len(L) > 2 and t > L[2]:
        chip(c, 960, 470, f'new record: {days_words(NB_TO_REC)} after crossing -10%', MINT, pop(t, L[2] + 0.3), 20)
    source(c, t, 'Yahoo Finance: S&P 500 closes; medians; our calculation')


def s_after(c, x):
    t, L = x.t, x.L
    specks(c, t, 148)
    head(c, t, 'One year after the S&P 500 first hit -10%')
    vals = sorted(C.r12.dropna() * 100)
    bw = 1000 / len(vals)
    show = len(vals) if t > L[0] + 4 else int(max(0, t - L[0] - 0.3) * 7)
    for i, v in enumerate(vals[:show]):
        x0 = 140 + i * bw
        top = 330 - max(0, v) * 5
        c.rrect(x0 + 4, top, x0 + bw - 4, 330 if v >= 0 else 330 - v * 5, 4, MINT if v > 0 else CORAL)
    c.line([(140, 330), (1140, 330)], (255, 255, 255, 90), 2)
    if len(L) > 1 and t > L[1]:
        chip(c, 640, 520, f'higher {UP12} of {N12} times; median {MED12:+.0f}%', MINT, pop(t, L[1] + 0.3), 26)
    if len(L) > 2 and t > L[2]:
        chip(c, 640, 578, f'lower {N12 - UP12} times', CORAL, pop(t, L[2] + 0.3), 22)
    source(c, t, 'Yahoo Finance: S&P 500 closes; prices only; our calculation')


def s_recent(c, x):
    t, L = x.t, x.L
    specks(c, t, 149)
    head(c, t, 'Corrections since 2015')
    rows = list(RECENT.iterrows())
    for i, (_, r) in enumerate(rows):
        k = pop(t, L[min(i // 2, len(L) - 1)] + 0.3 + (i % 2) * 1.5)
        if k <= 0:
            continue
        y = 120 + i * 76
        bear = r.depth <= -0.20
        col = CORAL if bear else MINT
        c.rrect(120, y, 1160, y + 62, 16, (255, 255, 255, 16), col, 3, a=clamp(k))
        c.text(150, y + 31, f'{r.start:%b %Y}', 24, col, 900, anchor='lm', a=clamp(k))
        c.text(380, y + 31, f'fell {abs(r.depth) * 100:.0f}%', 24, WHITE, 900, anchor='lm', a=clamp(k))
        c.text(600, y + 31, f'bottom {r.low:%b %Y}', 22, WHITE, 800, anchor='lm', a=clamp(k))
        c.text(870, y + 31, f'new record {r.rec:%b %Y}', 22, WHITE, 800, anchor='lm', a=clamp(k))
    source(c, t, 'Yahoo Finance: S&P 500 closes; our calculation')


def s_weeks(c, x):
    t, L = x.t, x.L
    specks(c, t, 150)
    head(c, t, f'S&P 500 weeks this bad or worse since 1950: {len(BAD)}')
    for i, d in enumerate(BAD.index):
        k = pop(t, L[0] + 0.4 + 0.35 * i)
        if k <= 0:
            continue
        cx = 110 + (i % 6) * 190
        cy = 190 + (i // 6) * 150
        now = d >= FRI - pd.Timedelta(days=2)
        c.rrect(cx - 85, cy - 55, cx + 85, cy + 55, 16, (255, 255, 255, 18), CORAL if now else GOLD, 3, a=clamp(k))
        c.text(cx, cy - 18, f'{d:%b %Y}' if not now else 'THIS WEEK', 22, CORAL if now else WHITE, 900, a=clamp(k))
        c.text(cx, cy + 20, f'{BAD[d] * 100:.1f}%', 26, CORAL, 900, a=clamp(k))
    if len(L) > 1 and t > L[1]:
        chip(c, 640, 540, f'a year after the earlier {len(F_BAD)}: higher {BAD_UP} times, median {BAD_MED:+.0f}%', MINT,
             pop(t, L[1] + 0.3), 22)
    source(c, t, 'Yahoo Finance: S&P 500 weekly closes; our calculation')


def s_watch(c, x):
    t, L = x.t, x.L
    specks(c, t, 151)
    head(c, t, 'What to watch next week')
    items = [('calendar', 'Short week:\nThanksgiving'), ('shopping-cart', 'Inflation\ndata'),
             ('landmark', '10-year\nyield'), ('activity', 'Fear index\nVIX')]
    icon_row(c, t, items, L[0] + 0.2, max(4.0, (L[-1] - L[0]) * 0.85), y=300, color=SKY)


def s_you(c, x):
    t, L = x.t, x.L
    specks(c, t, 152)
    head(c, t, 'What it means for your money')
    items = [('piggy-bank', 'Money you need\nsoon: not in stocks'), ('calendar', 'Long-term money:\ntime matters most'),
             ('shuffle', 'Diversify'), ('shield', 'Emergency fund\nfirst')]
    icon_row(c, t, items, L[0] + 0.2, max(4.0, (L[-1] - L[0]) * 0.8), y=300, color=GOLD)
    c.text(640, 570, 'Education only, not financial advice', 18, MUTED, 700, a=fade(t, 1))


def s_recap(c, x):
    t, L = x.t, x.L
    specks(c, t, 153)
    head(c, t, 'Recap')
    pts = [f'Nasdaq {NDQ_WK:.0f}% this week: worst since {NDQ_WK_SINCE:%Y}',
           f'S&P 500 {SP_WK:.1f}%, now {SP_DD:.1f}% from record: a correction',
           f'Since 1950: {N_CORR} corrections, {N_STOP} stopped before -20%',
           f'A year after hitting -10%: higher {UP12} of {N12} times',
           f'Weeks this bad: higher a year later {BAD_UP} of {len(F_BAD)}']
    step = max(1.6, (L[1] - L[0] - 0.5) / len(pts)) if len(L) > 1 else 2.0
    for i, p in enumerate(pts):
        k = pop(t, L[0] + 0.3 + step * i)
        if k > 0:
            c.circle(170, 150 + i * 80, 10, GOLD, a=clamp(k))
            c.text(200, 150 + i * 80, p, 28, WHITE, 800, anchor='lm', a=clamp(k))
    if len(L) > 1 and t > L[1]:
        chip(c, 640, 560, 'Will stocks be higher by New Year? Tell us below', GOLD, pop(t, L[1] + 0.3), 24)


SCENES = [
    dict(draw=s_hook, chapter="Intro: the worst week since 2020", lead=0.15, gap=0.3, lines=[
        f"!The Nasdaq just had its worst week since {NDQ_WK_SINCE:%B %Y}: down {abs(NDQ_WK):.0f} percent in five "
        "days.",
        f"The S&P 500 fell {abs(SP_WK):.1f} percent this week, its worst week since {SP_WK_SINCE:%B %Y}. It's now "
        f"{abs(SP_DD):.1f} percent below its October record. That's officially a correction.",
        f"So what happens after a correction? Here's the short answer from history. Since 1950, the S&P 500 has "
        f"had {N_CORR} corrections. {N_STOP} of them stopped before becoming a bear market.",
        f"!And a year after the S&P 500 first crossed that 10 percent line, it was higher {UP12} times out of {N12}.",
    ], punch=lambda L: [L[0] + 0.1, L[3] + 0.3],
        sfx=lambda L: [(L[0] + 0.1, 'hit'), (L[1] + 0.3, 'pop'), (L[1] + 3.5, 'down'), (L[2] + 0.3, 'whoosh'),
                       (L[2] + 3.0, 'pop'), (L[3] + 0.3, 'ding')]),
    dict(draw=s_promise, lines=[
        "But that's not a promise. In this video: the week, day by day. Why stocks fell. Every correction since "
        "1950, how deep they went and how long they lasted. And what it means for your money. If you want the "
        "money news explained like this every day, subscribe.",
    ], sfx=lambda L: [(L[0] + 0.5 + 1.4 * i, 'pop') for i in range(4)]),
    dict(draw=s_week, chapter='The week, day by day', lines=[
        "Here's how the week went for the S&P 500. Monday, down. Tuesday, down. Wednesday, a small loss. Thursday, "
        "down again. And then Friday, the biggest drop of all.",
        f"Add it up and the S&P 500 lost {abs(SP_WK):.1f} percent in a week, its worst since {SP_WK_SINCE:%B %Y}. "
        f"It has now fallen seven days in a row.",
        f"In dollars: 10,000 dollars in an S&P 500 index fund at last Friday's close was worth about "
        f"{K_WEEK:,.0f} dollars by this Friday's close.",
        f"Friday alone, the S&P 500 fell {abs(SP_FRI):.1f} percent and the Nasdaq fell {abs(NDQ_FRI):.1f} percent. "
        f"Wall Street's fear index, the VIX, closed at {V_NOW:.1f}, its highest close since April 2025.",
    ], sfx=lambda L: [(L[0] + 0.5 + i * 1.3, 'down') for i in range(5)] + [(L[1] + 0.3, 'pop'), (L[2] + 0.3, 'ding'),
                                                                          (L[3] + 0.3, 'hit')]),
    dict(draw=s_corr, chapter='What a correction is', lines=[
        "Here's where each of the big three indexes stands compared with its record high.",
        "Wall Street uses two lines. A drop of 10 percent from a record is a correction. A drop of 20 percent is a "
        "bear market.",
        f"The S&P 500 is {abs(SP_DD):.1f} percent down, and the tech-heavy Nasdaq is {abs(NDQ_DD):.1f} percent down. "
        f"Both are in a correction. The Dow is {abs(DOW_DD):.1f} percent below its record from {DOW_REC_D:%B}.",
        f"If you had 10,000 dollars in an S&P 500 fund at the October 6 record, it's worth about {K_REC:,.0f} "
        "dollars now, counting prices only.",
    ], sfx=lambda L: [(L[0] + 0.3, 'pop'), (L[0] + 1.5, 'pop'), (L[0] + 2.7, 'pop'), (L[1] + 0.3, 'whoosh'),
                      (L[1] + 2.3, 'whoosh'), (L[2] + 0.3, 'hit'), (L[3] + 0.3, 'ding')]),
    dict(draw=s_why, chapter='Why stocks fell', lines=[
        f"So why did stocks fall? Reason one: interest rates. The 10-year Treasury yield is {Y_NOW:.2f} percent, up "
        f"from {Y_1Y:.2f} a year ago. When a safe government bond pays over 5 percent, stocks have to compete.",
        f"Reason two: inflation. Prices rose {INFL:.1f} percent in the year to October, according to the Consumer "
        "Price Index.",
        f"Reason three: the Federal Reserve. It raised rates on {HIKE:%B} {HIKE.day}, its first hike since 2023, to "
        f"{FEDL.iloc[-1]:.2f} to {FEDU.iloc[-1]:.2f} percent. Higher rates make borrowing more expensive: the "
        f"average 30-year mortgage rate is {MORT:.2f} percent.",
        f"Reason four: the tech unwind. The stocks that rose the most this year are falling the most. The Nasdaq is "
        f"down {abs(NDQ_DD):.0f} percent from its record.",
        f"And reason five: fear feeds on itself. The VIX closed at {V_NOW:.0f}. When investors rush to protect "
        "themselves at the same time, selling speeds up.",
    ], sfx=lambda L: [(L[i] + 0.3, 'pop') for i in range(5)]),
    dict(draw=s_where, chapter='Where the money went', lines=[
        f"So where did the money go? Not into gold. Gold futures fell {abs(GOLD_WK):.1f} percent this week, to about "
        f"{GOLD_P:,.0f} dollars an ounce. That's now {abs(GOLD_DD):.0f} percent below gold's record in January.",
        f"Not into bitcoin either. It fell about {abs(BTC_WK):.0f} percent, to around {BTC_P:,.0f} dollars, more than "
        f"half below its record from {BTC_REC_D:%B %Y}.",
        f"The U.S. dollar barely moved, up {DXY_WK:.1f} percent.",
        f"The one thing that worked: government bonds. The 10-year Treasury yield fell from {Y_WK0:.2f} to "
        f"{Y_WK1:.2f} percent through Thursday. When yields fall, bond prices rise. In a panic, many investors run "
        "to the safest thing they can find.",
    ], sfx=lambda L: [(L[0] + 0.3, 'down'), (L[1] + 0.3, 'down'), (L[2] + 0.3, 'pop'), (L[3] + 0.3, 'ding')]),
    dict(draw=s_history, chapter='Every correction since 1950', lines=[
        f"Now, history. Each bar is one S&P 500 correction since 1950, {N_CORR} in total, and how deep it went "
        "before the index recovered.",
        f"!{N_STOP} of them stopped before reaching 20 percent. {N_BEAR} kept going and became bear markets. So "
        "most corrections end as corrections. But roughly 4 in 10 got worse.",
        "The deepest ones you'll recognize: the 1970s, the crash of 1987, the dot-com bust, 2008, and the pandemic "
        "in 2020.",
    ], punch=lambda L: [L[1] + 0.3], sfx=lambda L: [(L[0] + 0.4, 'whoosh'), (L[1] + 0.3, 'hit'), (L[1] + 1.5, 'pop'),
                                                    (L[2] + 0.3, 'pop')]),
    dict(draw=s_time, chapter='How long corrections last', lines=[
        f"For the {N_STOP} corrections that stopped short of a bear market, here's the typical path. The index "
        f"crossed minus 10 percent, kept falling to a bottom about {abs(NB_DEPTH):.0f} percent below the record, "
        "then climbed back.",
        f"The bottom usually came fast: a median of about {NB_TO_LOW:.0f} calendar days after crossing the 10 "
        "percent line.",
        f"And the new record came {days_words(NB_TO_REC)} after crossing that line. That's the typical case. "
        "Bear markets took much longer, sometimes years.",
    ], sfx=lambda L: [(L[0] + 0.3, 'whoosh'), (L[1] + 0.3, 'down'), (L[2] + 0.3, 'ding')]),
    dict(draw=s_after, chapter='One year later', lines=[
        f"What about the year after? Each bar here is one correction, showing how the S&P 500 did over the 12 "
        "months after it first crossed minus 10 percent, sorted from worst to best.",
        f"!It was higher {UP12} times out of {N12}, with a median gain of about {MED12:.0f} percent, not counting "
        "dividends.",
        f"But {N12 - UP12} times it was lower a year later. Those were mostly the corrections that turned into bear "
        "markets.",
        f"The range is wide. The best year after a correction began came after {BEST12_D:%B %Y}: up about "
        f"{BEST12:.0f} percent. The worst came after {WORST12_D:%B %Y}, as the financial crisis began: down about "
        f"{abs(WORST12):.0f} percent.",
    ], punch=lambda L: [L[1] + 0.3], sfx=lambda L: [(L[0] + 0.3, 'whoosh'), (L[1] + 0.3, 'hit'), (L[2] + 0.3, 'down')]),
    dict(draw=s_recent, chapter='Recent corrections', lines=[
        "Here are the corrections since 2015. In 2015 the S&P 500 fell about 14 percent, and in early 2018 about 10. "
        "Both recovered within months.",
        "Late 2018 came within a hair of a bear market, about 20 percent, but hit a new record by April 2019. The "
        "pandemic crash of 2020 went to 34 percent, and was back at a record by August.",
        "2022 was the slow one: a 25 percent bear market that took until January 2024 to recover. And in 2025, the "
        "tariff shock took the S&P 500 down about 19 percent, with a new record by June.",
        "Notice the pattern: the corrections that stayed shallow tended to heal within months. The ones that turned "
        "into bear markets are the ones that took years.",
    ], sfx=lambda L: [(L[0] + 0.3, 'pop'), (L[0] + 1.8, 'pop'), (L[1] + 0.3, 'pop'), (L[1] + 1.8, 'pop'),
                      (L[2] + 0.3, 'pop'), (L[2] + 1.8, 'pop')]),
    dict(draw=s_weeks, chapter='Weeks this bad', lines=[
        f"How rare is a week like this? Since 1950, the S&P 500 has had only {len(BAD)} weeks this bad or worse, "
        "including this one. They cluster in famous crises: 1987, 2008, the pandemic, and the tariff shock of 2025.",
        f"!A year after the earlier {len(F_BAD)}, the S&P 500 was higher {BAD_UP} times, with a median gain of about "
        f"{BAD_MED:.0f} percent. But the other {len(F_BAD) - BAD_UP} times, it was still lower. A terrible week has "
        "been followed by both rebounds and deeper slides.",
    ], punch=lambda L: [L[1] + 0.3], sfx=lambda L: [(L[0] + 0.4 + 0.35 * i, 'tick') for i in range(0, 12, 2)]
        + [(L[1] + 0.3, 'hit')]),
    dict(draw=s_watch, chapter='What to watch next week', lines=[
        "So what should you watch next week? First, it's a short week. U.S. markets are closed on Thanksgiving "
        "Thursday and close early on Friday, so trading can be thin and moves can be jumpy.",
        "Second, new inflation data. Third, the 10-year Treasury yield: if it keeps rising, pressure on stocks "
        "stays. And fourth, the fear index. When fear fades, the VIX usually falls back toward 20.",
    ], sfx=lambda L: [(L[0] + 0.3, 'pop'), (L[1] + 0.3, 'pop'), (L[1] + 3.0, 'pop'), (L[1] + 6.0, 'pop')]),
    dict(draw=s_you, chapter='What it means for you', lines=[
        "What does this mean for you? Here's what most financial educators point to. Money you'll need in the next "
        "few years usually doesn't belong in stocks, because a drop like this can come at the worst moment.",
        "For long-term money, time has mattered more than timing. Spreading money across many investments limits "
        "the damage from any one. And an emergency fund means you never have to sell at the bottom.",
        "If you invest every month through a 401(k), prices this week are lower than they were in October, so each "
        "contribution buys more shares. Nobody knows if this is the bottom, and that's exactly why steady investors "
        "don't try to guess.",
    ], sfx=lambda L: [(L[0] + 0.5, 'pop'), (L[0] + 3.0, 'pop'), (L[1] + 0.3, 'pop'), (L[2] + 0.3, 'pop')]),
    dict(draw=s_recap, chapter='Recap', lines=[
        f"Let's recap. The Nasdaq just had its worst week since {NDQ_WK_SINCE:%Y}, and the S&P 500 is in a "
        f"correction, {abs(SP_DD):.1f} percent below its record. Since 1950, {N_STOP} of {N_CORR} corrections "
        f"stopped before a bear market, and the S&P 500 was higher a year after hitting minus 10 percent {UP12} "
        f"times out of {N12}. But some corrections got much worse, so nobody can promise this one is close to over.",
        "!So what do you think: will stocks be higher by New Year's Day? Tell me in the comments. And subscribe, so "
        "you don't miss next week's updates.",
        "This video is for education only. It's not financial advice.",
    ], punch=lambda L: [L[1] + 0.3], sfx=lambda L: [(L[0] + 0.3 + 2.5 * j, 'pop') for j in range(5)]
        + [(L[1] + 0.3, 'ding')]),
]
for _sc in SCENES:
    _sc['draw'] = ticker(_sc['draw'])
SHORTS = {}


def check_numbers():
    script = ' '.join(l for sc in SCENES for l in sc['lines'])
    assert FRI.strftime('%Y-%m-%d') == '2026-11-20' and NDQ.index[-1] == FRI and VIX.index[-1] == FRI
    assert round(SP_WK, 2) == -8.61 and SP_WK_SINCE.strftime('%Y-%m') == '2025-04'
    assert round(NDQ_WK, 2) == -10.02 and NDQ_WK_SINCE.strftime('%Y-%m') == '2020-03'
    assert round(SP_DD, 1) == -11.6 and NDQ_DD <= -10 and SP_REC_D.strftime('%Y-%m-%d') == '2026-10-06'
    assert [round(v, 2) for v in WEEK_CH] == [-1.92, -1.03, -0.23, -2.02, -3.70] and round(NDQ_FRI, 2) == -5.28
    assert round(V_NOW, 1) == 37.4 and VIX[:-1][VIX[:-1] >= V_NOW].index[-1].strftime('%Y-%m') == '2025-04'
    assert N_CORR == 26 and N_BEAR == 11 and UP12 == 18 and N12 == 26 and round(MED12, 1) == 13.6
    assert round(NB_DEPTH) == -14 and NB_TO_LOW == 18 and NB_TO_REC == 119
    assert len(BAD) == 12 and len(F_BAD) == 11 and BAD_UP == 7 and round(BAD_MED, 1) == 19.7
    r = [(d.strftime('%Y-%m'), round(v * 100)) for d, v in zip(RECENT.start, RECENT.depth)]
    assert r == [('2015-05', -14), ('2018-01', -10), ('2018-09', -20), ('2020-02', -34), ('2022-01', -25),
                 ('2025-02', -19)], r
    assert [d.strftime('%Y-%m') for d in RECENT.rec] == ['2016-07', '2018-08', '2019-04', '2020-08', '2024-01', '2025-06']
    assert round(GOLD_WK, 1) == -9.5 and round(GOLD_DD) == -34 and round(BTC_WK, 1) == -13.8 and BTC_DD < -50
    assert round(DXY_WK, 1) == 0.4 and (Y_WK0, Y_WK1) == (5.15, 5.04) and Y_WK1_D.strftime('%Y-%m-%d') == '2026-11-19'
    assert round(BEST12) == 28 and BEST12_D.strftime('%Y-%m') == '2020-02' and round(WORST12) == -39 and WORST12_D.strftime('%Y-%m') == '2007-11'
    assert HIKE.strftime('%Y-%m-%d') == '2026-09-17' and Y_NOW > 5 and 3.8 < INFL < 4.4
    for s in ('not financial advice', 'correction', 'bear market', 'Consumer Price Index', 'since 1950', 'Thanksgiving'):
        assert s in script, s
    words = len(script.split())
    print(f'numbers check: OK  ({words} words)  S&P week {SP_WK:.2f}% (worst since {SP_WK_SINCE:%Y-%m}), Nasdaq '
          f'{NDQ_WK:.2f}% (since {NDQ_WK_SINCE:%Y-%m}), Dow {DOW_WK:.2f}%; S&P {SP_DD:.2f}% from record; VIX {V_NOW:.2f}; '
          f'corrections {N_CORR}, bear {N_BEAR}, up12 {UP12}/{N12} med {MED12:.1f}%; non-bear depth {NB_DEPTH:.1f}% '
          f'low {NB_TO_LOW:.0f}d rec {NB_TO_REC:.0f}d; bad weeks {len(BAD)}, after: {BAD_UP}/{len(F_BAD)} med {BAD_MED:.1f}%')


if __name__ == '__main__':
    check_numbers()
    os.makedirs(BUILD, exist_ok=True)
    if '--check' in sys.argv:
        sys.exit()
    if '--stills' in sys.argv:
        previews(SCENES, SHORTS, os.path.join(BUILD, 'previews'))
        sys.exit()
    only = [int(a) for a in sys.argv[sys.argv.index('--only') + 1].split(',')] if '--only' in sys.argv else None
    total, chapters = build(SCENES, os.path.join(OUT, 'ep12_week.mp4'), BUILD, only=only,
                            srt_path=os.path.join(OUT, 'ep12_week.en.srt'))
    with open(os.path.join(OUT, 'ep12_chapters.txt'), 'w') as f:
        for at, name in chapters:
            f.write(f'{fmt_time(at)} {name}\n')
    print(f'total {total / 60:.1f} min')
