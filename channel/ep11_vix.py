"""Episode 11: Wall Street's fear index just doubled. What happens next? (long video, Fri Nov 20 2026, same-day)

    python3 channel/ep11_vix.py [--check] [--stills] [--only 3,5]

Data (check_numbers recomputes everything from the files):
- channel/data/VIX_max.csv: Yahoo Finance chart API daily closes of the Cboe Volatility Index (^VIX), from 1990.
- channel/data/GSPC_max.csv, IXIC_max.csv: Yahoo Finance daily closes of the S&P 500 and Nasdaq Composite.
- FRED: DGS10 (10-year Treasury yield), CPIAUCSL (CPI).
Saved Nov 20 2026 after the close. History statistics are our calculations (prices only, no dividends).
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
BUILD = os.path.join(HERE, 'build', 'ep11_vix')


def load(name):
    return pd.read_csv(os.path.join(HERE, 'data', f'{name}_max.csv'), parse_dates=['date']).set_index('date')['close']


VIX, SPX, NDQ = load('VIX'), load('GSPC'), load('IXIC')
TODAY = VIX.index[-1]
V_NOW = VIX.iloc[-1]
V_PREV = VIX.iloc[-2]
SP_REC, SP_REC_D = SPX.max(), SPX.idxmax()
V_AT_REC = VIX[:SP_REC_D].iloc[-1]
V_X = V_NOW / V_AT_REC
V_MED, V_AVG = VIX.median(), VIX.mean()
V_MAX, V_MAX_D = VIX.max(), VIX.idxmax()
V08 = VIX['2008'].max()
SHARE30 = (VIX >= 30).mean() * 100
ABOVE30 = V_NOW >= 30
_hi = VIX[:-1][VIX[:-1] >= V_NOW]
HIGHEST_SINCE = _hi.index[-1] if len(_hi) else None
MOVE_1M = V_NOW / math.sqrt(12)  # one-standard-deviation monthly move implied by the VIX, in percent

SP_NOW = SPX.iloc[-1]
SP_DAY = (SP_NOW / SPX.iloc[-2] - 1) * 100
SP_DD = (SP_NOW / SP_REC - 1) * 100
CORR_LINE = SP_REC * 0.9
IN_CORR = SP_NOW < CORR_LINE


def losing_streak(s):
    n = 0
    for v in s.pct_change()[::-1]:
        if v < 0:
            n += 1
        else:
            break
    return n


STREAK = losing_streak(SPX)
NDQ_DD = (NDQ.iloc[-1] / NDQ.max() - 1) * 100

# every time the VIX first closed at 30+ after 60+ trading days below 30, and what the S&P 500 did next
_firsts, _last = [], None
for d, a in (VIX >= 30).items():
    if a and (_last is None or VIX.index.get_loc(d) - VIX.index.get_loc(_last) > 60):
        _firsts.append(d)
    if a:
        _last = d
PAST = [d for d in _firsts if d < TODAY and d in SPX.index]


def fwd(d, n):
    i = SPX.index.get_loc(d)
    return SPX.iloc[i + n] / SPX.iloc[i] - 1 if i + n < len(SPX) else None


F1 = [x for x in (fwd(d, 21) for d in PAST) if x is not None]
F12 = [x for x in (fwd(d, 252) for d in PAST) if x is not None]
UP1, UP12 = sum(x > 0 for x in F1), sum(x > 0 for x in F12)
MED12 = float(np.median(F12)) * 100


def calm_days(d):
    j = VIX.index.get_loc(d)
    k = j
    while k < len(VIX) and VIX.iloc[k] >= 20:
        k += 1
    return k - j


EX = {}
for key, d in (('2008', '2008-09-15'), ('2020', '2020-02-27'), ('2024', '2024-08-05'), ('2025', '2025-04-03')):
    d = pd.Timestamp(d)
    j = VIX.index.get_loc(d)
    EX[key] = dict(date=d, peak=VIX.iloc[j:j + 63].max(), calm=calm_days(d), r12=fwd(d, 252) * 100)
_runs = (VIX >= 30).groupby(((VIX >= 30) != (VIX >= 30).shift()).cumsum()).sum()
RUN_MED = float(_runs[_runs > 0].median())
MED1 = float(np.median(F1)) * 100
V_MIN, V_MIN_D = VIX.min(), VIX.idxmin()

_j = pd.concat([VIX.pct_change(), SPX.pct_change()], axis=1, keys=['v', 'g'], sort=True).dropna()['1990-01-03':]
SEESAW = (_j[_j.g < 0].v > 0).mean() * 100
_sr = SPX['1990':].pct_change()
_vprev = VIX.shift(1).reindex(_sr.index)
BEST20 = int(sum(_vprev[d] >= 30 for d in _sr.nlargest(20).index))
WORST20 = int(sum(_vprev[d] >= 30 for d in _sr.nsmallest(20).index))
MOVE_HI = _sr.abs()[_vprev >= 30].mean() * 100
MOVE_LO = _sr.abs()[_vprev < 15].mean() * 100
MAR = pd.Timestamp('2026-03-27')
MAR_PEAK = VIX['2026-03-01':'2026-04-30'].max()
MAR_CALM = calm_days(MAR)
SP_LOW26, SP_LOW26_D = SPX['2026'].min(), SPX['2026'].idxmin()
MAR_RUN = (SP_REC / SP_LOW26 - 1) * 100
EX18, EX22 = calm_days(pd.Timestamp('2018-02-05')), calm_days(pd.Timestamp('2022-09-26'))
Y10 = series('DGS10')
Y_NOW = Y10.iloc[-1]
CPI = series('CPIAUCSL')
INFL = (CPI.iloc[-1] / CPI.iloc[-13] - 1) * 100

SRC = 'Yahoo Finance: Cboe Volatility Index (^VIX) and S&P 500 daily closes'
TICK = (f'VIX  {V_NOW:.2f}  {(V_NOW / V_PREV - 1) * 100:+.1f}%     S&P 500  {SP_NOW:,.2f}  {SP_DAY:+.2f}%     '
        f'NASDAQ  {NDQ.iloc[-1]:,.2f}     10-YR YIELD  {Y_NOW:.2f}%     CPI  {INFL:.1f}%     ')
DOUBLED = 'doubled' if V_X >= 1.95 else 'nearly doubled'


def ticker(draw):
    def wrapped(c, x):
        draw(c, x)
        c.rrect(0, 0, W, 40, 0, (8, 10, 20, 210))
        w = len(TICK) * 15 * 0.62
        off = (x.t * 45) % w
        for k in range(3):
            c.text(-off + k * w, 28, TICK, 15, GOLD, 800, anchor='lm', shadow=False)
    return wrapped


def gauge(c, cx, cy, r, value, k=1.0, vmax=80):
    """A fear gauge from 0 to vmax: green, yellow, red bands and a needle."""
    for a0, a1, col in ((0, 20, MINT), (20, 30, GOLD), (30, vmax, CORAL)):
        pts = []
        for v in np.linspace(a0, a1, 24):
            ang = math.pi * (1 - v / vmax)
            pts.append((cx + r * math.cos(ang), cy - r * math.sin(ang)))
        c.line(pts, col, 26)
    for v in (0, 20, 30, 50, 80):
        ang = math.pi * (1 - v / vmax)
        c.text(cx + (r + 38) * math.cos(ang), cy - (r + 38) * math.sin(ang), str(v), 20, MUTED, 800, shadow=False)
    val = value * clamp(k)
    ang = math.pi * (1 - min(val, vmax) / vmax)
    c.line([(cx, cy), (cx + (r - 30) * math.cos(ang), cy - (r - 30) * math.sin(ang))], WHITE, 8)
    c.circle(cx, cy, 16, WHITE)


# ------------------------------------------------------------------- scenes --
def s_hook(c, x):
    t, L = x.t, x.L
    specks(c, t, 121)
    k = pop(t, L[0] + 0.1, 0.4)
    gauge(c, 640, 430, 230, V_NOW, ease(clamp((t - L[0] - 0.2) / 1.5)))
    if k > 0:
        c.text(640, 120, 'THE FEAR INDEX', 56, WHITE, 900, a=clamp(k), stroke=6)
        c.text(640, 560, f'{V_NOW:.1f}', 90, CORAL, 900, a=clamp(k), stroke=6)
    if t > L[1]:
        chip(c, 640, 200, f'{V_AT_REC:.0f} on {SP_REC_D:%b %d}  ->  {V_NOW:.0f} today', GOLD, pop(t, L[1] + 0.3), 26)
    if len(L) > 2 and t > L[2]:
        c.rrect(0, 0, W, H, 0, (10, 14, 26, int(240 * fade(t, L[2]))))
        kk = pop(t, L[2] + 0.3)
        c.text(640, 250, f'{UP12} of {len(F12)}', 110, MINT, 900, a=clamp(kk), stroke=6)
        c.text(640, 350, 'times the S&P 500 was higher a year later', 30, WHITE, 800, a=clamp(kk))
        c.text(640, 395, 'after the VIX first hit 30 (since 1990)', 26, MUTED, 800, a=clamp(kk))
        if len(L) > 3 and t > L[3]:
            chip(c, 640, 480, f'but {len(F12) - UP12} times it was lower', CORAL, pop(t, L[3] + 0.3), 26)


def s_promise(c, x):
    t, L = x.t, x.L
    specks(c, t, 122)
    penny(c, 200, 520, 100, t, 'thinking', talk=x.talk())
    items = ['What the fear index is', 'Why it just jumped', 'Every past spike above 30', 'What it means for you']
    for i, it in enumerate(items):
        k = pop(t, L[0] + 0.5 + 1.4 * i)
        if k > 0:
            c.rrect(420, 150 + i * 105, 1120, 230 + i * 105, 22, (255, 255, 255, 22), GOLD, 3, a=clamp(k))
            c.text(460, 190 + i * 105, f'{i + 1}', 40, GOLD, 900, a=clamp(k))
            c.text(510, 190 + i * 105, it, 34, WHITE, 800, anchor='lm', a=clamp(k))


def s_what(c, x):
    t, L = x.t, x.L
    specks(c, t, 123)
    head(c, t, 'What is the VIX?')
    items = [('activity', 'Expected swings\nnext 30 days'), ('chart-candlestick', 'Read from S&P 500\noptions prices'),
             ('triangle-alert', 'Higher number =\nmore fear')]
    icon_row(c, t, items, L[0] + 0.2, max(4.0, (L[1] - L[0]) * 0.9), y=270, color=SKY)
    if len(L) > 1 and L[1] < t < (L[2] if len(L) > 2 else 1e9):
        chip(c, 640, 520, 'introduced by Cboe in 1993; values back to 1990', MUTED, pop(t, L[1] + 0.3), 22)
    if len(L) > 2 and t > L[2]:
        c.rrect(0, 0, W, H, 0, (10, 14, 26, int(240 * fade(t, L[2]))))
        kk = pop(t, L[2] + 0.3)
        c.text(640, 210, f'VIX {V_NOW:.0f}', 70, CORAL, 900, a=clamp(kk), stroke=5)
        c.text(640, 300, f'= the market expects swings of about {MOVE_1M:.1f}%', 32, WHITE, 900, a=clamp(kk))
        c.text(640, 345, 'up or down, over the next month (rule of thumb)', 24, MUTED, 800, a=clamp(kk))
        if len(L) > 3 and t > L[3]:
            v0 = V_AT_REC / math.sqrt(12)
            chip(c, 640, 440, f'at the October record: VIX {V_AT_REC:.0f} = about {v0:.1f}%', MINT, pop(t, L[3] + 0.3), 24)
    source(c, t, 'Cboe; rule of thumb: VIX / square root of 12')


def s_scale(c, x):
    t, L = x.t, x.L
    specks(c, t, 124)
    head(c, t, 'How high is 30?')
    gauge(c, 380, 450, 220, V_NOW, 1.0)
    rows = [(f'Typical day since 1990: about {V_MED:.0f}', MINT), (f'Days at 30 or higher: {SHARE30:.0f}%', GOLD),
            (f'2008 crisis peak: {V08:.0f}', CORAL), (f'Record: {V_MAX:.0f} ({V_MAX_D:%b %Y})', CORAL)]
    for i, (txt, col) in enumerate(rows):
        at = L[min(i, len(L) - 1)] + (0.3 if i < len(L) else 2.0 * (i - len(L) + 1))
        k = pop(t, at)
        if k > 0:
            c.rrect(690, 150 + i * 95, 1180, 220 + i * 95, 20, (255, 255, 255, 18), col, 3, a=clamp(k))
            c.text(715, 185 + i * 95, txt, 26, WHITE, 900, anchor='lm', a=clamp(k))
    c.text(380, 545, f'today: {V_NOW:.1f}', 34, CORAL, 900, a=fade(t, 0.5))
    source(c, t, SRC)


def s_jump(c, x):
    t, L = x.t, x.L
    specks(c, t, 125)
    head(c, t, 'Since the S&P 500 record on October 6')
    v = VIX['2026-08-01':]
    s = SPX['2026-08-01':]
    xs = lambda q: [(d - pd.Timestamp('2026-08-01')).days for d in q.index]  # noqa: E731
    k = clamp((t - L[0] - 0.3) / 4.0) if t < L[1] else 1.0
    px, py = line_chart(c, (150, 110, 1120, 330), xs(s), list(s.values), (0, xs(s)[-1] + 4),
                        (s.min() * 0.98, s.max() * 1.01), k, GOLD, yticks=(), width=4)
    c.text(160, 120, 'S&P 500', 22, GOLD, 900, anchor='lm', a=fade(t, 0.3))
    px2, py2 = line_chart(c, (150, 370, 1120, 560), xs(v), list(v.values), (0, xs(v)[-1] + 4), (10, 35), k, CORAL,
                          yticks=(10, 20, 30), yfmt='{:.0f}', width=4, tick_size=16)
    c.text(160, 380, 'VIX (fear index)', 22, CORAL, 900, anchor='lm', a=fade(t, 0.3))
    if t > L[1]:
        chip(c, 800, 352, f'S&P: {STREAK} losses in a row, {SP_DD:.1f}% from record', GOLD, pop(t, L[1] + 0.3), 22)
    if len(L) > 2 and t > L[2]:
        chip(c, 900, 420, f'VIX: {V_AT_REC:.0f} -> {V_NOW:.0f}, {DOUBLED}', CORAL, pop(t, L[2] + 0.3), 22)
        pulse(c, t, (px2(xs(v)[-1]) - 22, py2(V_NOW) - 22, px2(xs(v)[-1]) + 22, py2(V_NOW) + 22), CORAL, 20)
    source(c, t, SRC)


def s_why(c, x):
    t, L = x.t, x.L
    specks(c, t, 126)
    head(c, t, 'Why fear is rising')
    items = [('trending-down', f'{STREAK} straight\ndown days'), ('cpu', f'Tech sell-off:\nNasdaq {NDQ_DD:.0f}%'),
             ('landmark', f'10-yr yield\n{Y_NOW:.1f}%'), ('shopping-cart', f'Inflation\n{INFL:.1f}%')]
    for i, (ic, lab) in enumerate(items):
        k = pop(t, L[min(i, len(L) - 1)] + (0.3 if i < len(L) else 2.5))
        if k <= 0:
            continue
        cx = 175 + i * 310
        c.circle(cx, 260, 90 * clamp(k), (255, 255, 255, 22), CORAL, 3)
        c.icon(ic, cx, 260, 80 * clamp(k), CORAL)
        for j, part in enumerate(lab.split('\n')):
            c.text(cx, 395 + j * 32, part, 25, WHITE, 900, a=clamp(k))
    source(c, t, 'Yahoo Finance; FRED: DGS10, CPIAUCSL')


def s_history(c, x):
    t, L = x.t, x.L
    specks(c, t, 127)
    head(c, t, f'Every time the VIX first hit 30 (since 1990): {len(PAST)}')
    x0, x1 = 120, 1160
    c.line([(x0, 330), (x1, 330)], (255, 255, 255, 90), 3)
    for yr in range(1990, 2030, 5):
        xx = x0 + (yr - 1990) / 37 * (x1 - x0)
        c.text(xx, 365, str(yr), 18, MUTED, 700, shadow=False)
    for i, d in enumerate(PAST + [TODAY]):
        k = pop(t, L[0] + 0.4 + i * 0.25)
        if k <= 0:
            continue
        xx = x0 + (d.year + d.dayofyear / 366 - 1990) / 37 * (x1 - x0)
        now = d == TODAY
        c.circle(xx, 330, (16 if now else 10) * clamp(k), CORAL if now else GOLD, WHITE if now else None, 3 if now else 0)
    labels = [('2008', 'Lehman: Sep 2008'), ('2020', 'Pandemic: Feb 2020'), ('2024', 'Aug 2024'), ('2025', 'Tariffs: Apr 2025')]
    if len(L) > 1 and t > L[1]:
        for i, (key, lab) in enumerate(labels):
            d = EX[key]['date']
            xx = x0 + (d.year + d.dayofyear / 366 - 1990) / 37 * (x1 - x0)
            kk = pop(t, L[1] + 0.4 + i * 1.2)
            yy = (230, 440, 180, 490)[i]
            if kk > 0:
                c.line([(xx, 330), (xx, yy + (20 if yy < 330 else -20))], (255, 255, 255, 120), 2, a=clamp(kk))
                chip(c, min(max(xx, 150), 1060), yy, lab, SKY, kk, 18)
    if len(L) > 2 and t > L[2]:
        chip(c, 640, 540, f'the VIX usually stays above 30 for only about {RUN_MED:.0f} days at a time',
             MINT, pop(t, L[2] + 0.3), 22)
    source(c, t, SRC + '; our calculation')


def s_next(c, x):
    t, L = x.t, x.L
    specks(c, t, 128)
    head(c, t, 'What the S&P 500 did next')
    k = pop(t, L[0] + 0.3)
    if k > 0:
        c.text(330, 250, f'{UP1} of {len(F1)}', 80, GOLD, 900, a=clamp(k), stroke=5)
        c.text(330, 320, 'higher one month later', 26, WHITE, 800, a=clamp(k))
    if t > L[1]:
        kk = pop(t, L[1] + 0.3)
        c.text(920, 250, f'{UP12} of {len(F12)}', 80, MINT, 900, a=clamp(kk), stroke=5)
        c.text(920, 320, 'higher one year later', 26, WHITE, 800, a=clamp(kk))
        if t > L[1] + 3.0:
            chip(c, 920, 390, f'median: {MED12:+.0f}%', MINT, pop(t, L[1] + 3.0), 26)
    if len(L) > 2 and t > L[2]:
        chip(c, 640, 500, f'worst case on our list: Sep 2008, {EX["2008"]["r12"]:.0f}% a year later', CORAL,
             pop(t, L[2] + 0.3), 24)
    source(c, t, SRC + '; prices only')


def s_cases(c, x):
    t, L = x.t, x.L
    specks(c, t, 129)
    head(c, t, 'Four fear spikes, four endings')
    rows = [('2008', 'Lehman collapse', CORAL), ('2020', 'Pandemic', SKY), ('2024', 'August scare', MINT),
            ('2025', 'Tariff shock', GOLD)]
    for i, (key, name, col) in enumerate(rows):
        k = pop(t, L[min(i, len(L) - 1)] + (0.3 if i < len(L) else 2.0))
        if k <= 0:
            continue
        e = EX[key]
        y = 140 + i * 105
        c.rrect(120, y, 1160, y + 88, 20, (255, 255, 255, 16), col, 3, a=clamp(k))
        c.text(150, y + 44, f"{e['date']:%b %Y}", 26, col, 900, anchor='lm', a=clamp(k))
        c.text(330, y + 44, name, 26, WHITE, 900, anchor='lm', a=clamp(k))
        c.text(640, y + 44, f"VIX peak {e['peak']:.0f}", 24, WHITE, 800, anchor='lm', a=clamp(k))
        c.text(840, y + 44, f"calm in {e['calm']} days", 24, WHITE, 800, anchor='lm', a=clamp(k))
        c.text(1135, y + 44, f"{e['r12']:+.0f}%", 28, MINT if e['r12'] > 0 else CORAL, 900, anchor='rm', a=clamp(k))
    c.text(1135, 125, '1 year later', 16, MUTED, 800, anchor='rm', a=fade(t, 0.5), shadow=False)
    c.text(840, 125, 'trading days until VIX < 20', 16, MUTED, 800, anchor='lm', a=fade(t, 0.5), shadow=False)
    source(c, t, SRC + '; our calculation')


def s_money(c, x):
    t, L = x.t, x.L
    specks(c, t, 133)
    head(c, t, f'What a {MOVE_1M:.1f}% swing means in dollars')
    for i, (amt, col) in enumerate(((10000, GOLD), (100000, SKY))):
        k = pop(t, L[0] + 0.3 + 2.5 * i)
        if k <= 0:
            continue
        cx = 360 + i * 560
        c.rrect(cx - 230, 140, cx + 230, 400, 26, (255, 255, 255, 16), col, 4, a=clamp(k))
        c.text(cx, 190, f'${amt:,} invested', 28, WHITE, 900, a=clamp(k))
        c.text(cx, 280, f'+/- ${amt * MOVE_1M / 100:,.0f}', 58, col, 900, a=clamp(k), stroke=4)
        c.text(cx, 360, 'a typical month at this VIX', 22, MUTED, 800, a=clamp(k))
    if len(L) > 1 and t > L[1]:
        kk = pop(t, L[1] + 0.3)
        c.text(640, 470, f'average daily S&P 500 move: {MOVE_HI:.2f}% when VIX was 30+', 26, CORAL, 900, a=clamp(kk))
        c.text(640, 515, f'vs {MOVE_LO:.2f}% when it was under 15', 26, MINT, 900, a=clamp(kk))
        pulse(c, t, (250, 440, 1030, 545), CORAL, 20)
    source(c, t, SRC + '; our calculation')


def s_seesaw(c, x):
    t, L = x.t, x.L
    specks(c, t, 134)
    head(c, t, 'The VIX and stocks move like a seesaw')
    ang = 0.18 * math.sin(clamp((t - L[0] - 0.3) / 2.0) * math.pi / 2) * (1 + 0.15 * math.sin(t * 2))
    cx, cy = 640, 380
    dx, dy = 360 * math.cos(ang), 360 * math.sin(ang)
    c.poly([(cx - 40, cy + 70), (cx + 40, cy + 70), (cx, cy)], MUTED)
    c.line([(cx - dx, cy - dy), (cx + dx, cy + dy)], WHITE, 10)
    c.text(cx - dx, cy - dy - 50, 'VIX', 40, CORAL, 900)
    c.text(cx + dx, cy + dy - 50, 'S&P 500', 40, GOLD, 900)
    if len(L) > 1 and t > L[1]:
        chip(c, 640, 540, f'on {SEESAW:.0f}% of S&P 500 down days since 1990, the VIX rose', CORAL, pop(t, L[1] + 0.3), 24)
    source(c, t, SRC + '; our calculation')


def s_march(c, x):
    t, L = x.t, x.L
    specks(c, t, 135)
    head(c, t, 'This already happened once this year')
    s = SPX['2026-01-01':]
    xs = [(d - pd.Timestamp('2026-01-01')).days for d in s.index]
    k = clamp((t - L[0] - 0.3) / 4.0) if t < L[2] else 1.0
    px, py = line_chart(c, (150, 130, 1120, 520), xs, list(s.values), (0, xs[-1] + 4), (6000, 8000), k, GOLD,
                        yticks=(6000, 7000, 8000), yfmt='{:,.0f}')
    lx = px((SP_LOW26_D - pd.Timestamp('2026-01-01')).days)
    if t > L[0] + 2.0:
        chip(c, lx + 60, py(SP_LOW26) + 45, f'Mar 30 low: {SP_LOW26:,.0f}  (VIX {MAR_PEAK:.0f})', CORAL,
             pop(t, L[0] + 2.0), 20)
    if len(L) > 1 and t > L[1]:
        chip(c, lx + 120, 200, f'VIX below 20 again in {MAR_CALM} trading days', MINT, pop(t, L[1] + 0.3), 20)
    if len(L) > 2 and t > L[2]:
        rx = px((SP_REC_D - pd.Timestamp('2026-01-01')).days)
        chip(c, rx - 120, py(SP_REC) - 35, f'+{MAR_RUN:.0f}% to the Oct 6 record', MINT, pop(t, L[2] + 0.3), 22)
    source(c, t, SRC)


def s_bestdays(c, x):
    t, L = x.t, x.L
    specks(c, t, 136)
    head(c, t, 'Big days happen when fear is high (S&P 500, since 1990)')
    for i, (n, lab, col) in enumerate(((BEST20, 'of the 20 best days', MINT), (WORST20, 'of the 20 worst days', CORAL))):
        k = pop(t, L[min(i, len(L) - 1)] + 0.3)
        if k <= 0:
            continue
        y = 200 + i * 170
        for j in range(20):
            kk = pop(t, L[min(i, len(L) - 1)] + 0.3 + 0.08 * j)
            col_j = col if j < n else (90, 100, 120)
            c.rrect(150 + j * 50, y - 30, 190 + j * 50, y + 30, 8, col_j, a=clamp(kk))
        c.text(150, y + 62, f'{n} {lab} came when the VIX was 30 or higher', 26, WHITE, 900, anchor='lm', a=clamp(k))
    if len(L) > 2 and t > L[2]:
        chip(c, 640, 555, 'missing the scary weeks can mean missing the best days', SKY, pop(t, L[2] + 0.3), 24)
    source(c, t, SRC + '; VIX on the previous close; our calculation')


def s_watch(c, x):
    t, L = x.t, x.L
    specks(c, t, 130)
    head(c, t, 'What to watch next')
    items = [('activity', 'VIX back\nbelow 20?'), ('landmark', '10-year\nyield'), ('percent', 'Fed in\nDecember'),
             ('cpu', 'Chip and AI\nstocks')]
    icon_row(c, t, items, L[0] + 0.2, max(4.0, (L[-1] - L[0]) * 0.85), y=300, color=SKY)


def s_you(c, x):
    t, L = x.t, x.L
    specks(c, t, 131)
    head(c, t, 'What it means for your money')
    items = [('arrow-up-down', 'Swings cut\nboth ways'), ('calendar', 'Time horizon\nmatters most'),
             ('shield', 'Emergency fund\nfirst'), ('ban', 'Panic selling\nlocks in losses')]
    icon_row(c, t, items, L[0] + 0.2, max(4.0, (L[-1] - L[0]) * 0.8), y=300, color=GOLD)
    c.text(640, 570, 'Education only, not financial advice', 18, MUTED, 700, a=fade(t, 1))


def s_recap(c, x):
    t, L = x.t, x.L
    specks(c, t, 132)
    head(c, t, 'Recap')
    pts = [f'VIX {V_NOW:.0f}: {DOUBLED} since the Oct 6 record',
           f'S&P 500: {STREAK} losses in a row, {SP_DD:.1f}% from record',
           f'VIX at 30+ on only {SHARE30:.0f}% of days since 1990',
           f'After VIX first hit 30: higher a year later {UP12} of {len(F12)}',
           'Fear spikes are usually short, but not always']
    step = max(1.6, (L[1] - L[0] - 0.5) / len(pts)) if len(L) > 1 else 2.0
    for i, p in enumerate(pts):
        k = pop(t, L[0] + 0.3 + step * i)
        if k > 0:
            c.circle(170, 150 + i * 80, 10, GOLD, a=clamp(k))
            c.text(200, 150 + i * 80, p, 28, WHITE, 800, anchor='lm', a=clamp(k))
    if len(L) > 1 and t > L[1]:
        chip(c, 640, 560, 'Buying, holding or selling? Tell us in the comments', GOLD, pop(t, L[1] + 0.3), 24)


corr_line = (f"It's now {abs(SP_DD):.1f} percent below its record, which officially puts it in a correction."
             if IN_CORR else
             f"It's now {abs(SP_DD):.1f} percent below its October 6 record, close to the 10 percent line Wall Street "
             f"calls a correction.")
SCENES = [
    dict(draw=s_hook, chapter='Intro: the fear index', lead=0.15, gap=0.3, lines=[
        f"!Wall Street's fear index just {DOUBLED}.",
        f"The VIX was at {V_AT_REC:.0f} on October 6, the day the S&P 500 hit its record. Today it closed at "
        f"{V_NOW:.1f}.",
        f"So what happens after fear spikes like this? Here's the short answer. Since 1990, the VIX has jumped above "
        f"30 for the first time in months {len(PAST)} times. A year later, the S&P 500 was higher {UP12} times out of "
        f"{len(F12)}.",
        f"But not every time. {len(F12) - UP12} times, stocks were still lower a year later, and one of those was "
        "2008.",
    ], punch=lambda L: [L[0] + 0.1, L[2] + 0.3],
        sfx=lambda L: [(L[0] + 0.1, 'hit'), (L[1] + 0.3, 'pop'), (L[2] + 0.3, 'whoosh'), (L[3] + 0.3, 'down')]),
    dict(draw=s_promise, lines=[
        "In this video: what the fear index actually measures, why it just jumped, every past spike above 30 and "
        "what happened next, and what it means for your money. If you want the money news explained like this "
        "every day, subscribe.",
    ], sfx=lambda L: [(L[0] + 0.5 + 1.4 * i, 'pop') for i in range(4)]),
    dict(draw=s_what, chapter='What is the VIX?', lines=[
        "First, what is the VIX? It's run by Cboe, the options exchange in Chicago. It measures how much the S&P "
        "500 is expected to swing over the next 30 days, based on the prices people pay for S&P 500 options, "
        "which work like insurance against big moves. When investors get nervous, they pay more for that "
        "insurance, and the VIX goes up.",
        "Cboe introduced the VIX in 1993, and it has calculated values back to 1990, which is why our history "
        "starts there.",
        f"!Here's a simple way to read it. Divide the VIX by about three and a half. A VIX of {V_NOW:.0f} means the "
        f"market expects the S&P 500 to swing about {MOVE_1M:.1f} percent, up or down, over the next month.",
        f"Back at the October record, the VIX was {V_AT_REC:.0f}, which meant expected swings of only about "
        f"{V_AT_REC / math.sqrt(12):.1f} percent.",
    ], punch=lambda L: [L[2] + 0.3], sfx=lambda L: [(L[0] + 0.5, 'pop'), (L[0] + 3.0, 'pop'), (L[0] + 5.5, 'pop'),
                                                    (L[1] + 0.3, 'pop'), (L[2] + 0.3, 'hit'), (L[3] + 0.3, 'ding')]),
    dict(draw=s_money, chapter='What it means in dollars', lines=[
        f"Let's put that in dollars. If you have 10,000 dollars in an S&P 500 index fund, a {MOVE_1M:.1f} percent "
        f"swing is about {100 * MOVE_1M:,.0f} dollars in a month, up or down. With 100,000 dollars in a 401(k), "
        f"it's about {1000 * MOVE_1M:,.0f} dollars.",
        f"And the daily moves get bigger too. Since 1990, when the VIX was 30 or higher, the S&P 500 moved about "
        f"{MOVE_HI:.1f} percent on an average day. When the VIX was under 15, it moved about {MOVE_LO:.1f} "
        "percent. That's more than four times calmer.",
    ], sfx=lambda L: [(L[0] + 0.3, 'pop'), (L[0] + 2.8, 'pop'), (L[1] + 0.3, 'hit')]),
    dict(draw=s_scale, chapter='How high is 30?', lines=[
        f"So how high is {V_NOW:.0f}? On a typical day since 1990, the VIX has been around {V_MED:.0f}.",
        f"It has closed at 30 or higher on only about {SHARE30:.0f} percent of trading days.",
        f"In the 2008 financial crisis, it peaked at {V08:.0f}.",
        f"And the all-time record is {V_MAX:.0f}, set in {V_MAX_D:%B %Y}, when the pandemic hit. The lowest close "
        f"ever was {V_MIN:.1f}, in {V_MIN_D:%B %Y}, one of the calmest stretches the market has ever had. Today's "
        f"reading is about {V_NOW / V_MIN:.1f} times that.",
    ], sfx=lambda L: [(L[0] + 0.3, 'pop'), (L[1] + 0.3, 'pop'), (L[2] + 0.3, 'down'), (L[3] + 0.3, 'hit')]),
    dict(draw=s_jump, chapter='Why it just jumped', lines=[
        "Here's what changed. On top, the S&P 500 since August. On the bottom, the VIX.",
        f"The S&P 500 has now fallen {STREAK} days in a row. {corr_line} Today it closed at {SP_NOW:,.0f}.",
        f"Meanwhile the VIX went from {V_AT_REC:.0f} to {V_NOW:.0f}. "
        + (f"That's its highest close since {HIGHEST_SINCE:%B %Y}." if HIGHEST_SINCE is not None else
           "That's a new high for this year."),
    ], sfx=lambda L: [(L[0] + 0.3, 'whoosh'), (L[1] + 0.3, 'down'), (L[2] + 0.3, 'hit')]),
    dict(draw=s_seesaw, chapter='A seesaw', lines=[
        "Here's the pattern to remember: the VIX and the stock market usually move like a seesaw. When stocks "
        "fall, fear goes up. When stocks rise, fear goes down.",
        f"Since 1990, on {SEESAW:.0f} percent of the days the S&P 500 fell, the VIX rose. That's why people call "
        "it the fear index.",
    ], sfx=lambda L: [(L[0] + 0.3, 'whoosh'), (L[1] + 0.3, 'pop')]),
    dict(draw=s_why, chapter='Why investors are nervous', lines=[
        f"Why are investors so nervous? Start with the losing streak itself: {STREAK} down days in a row make "
        "people want insurance.",
        f"Then there's the sell-off in tech and chip stocks. The Nasdaq is now {abs(NDQ_DD):.0f} percent below its "
        "record.",
        f"Interest rates are high: the 10-year Treasury yield is about {Y_NOW:.1f} percent, so safe bonds pay well "
        "and stocks have to compete.",
        f"And inflation is running at {INFL:.1f} percent, which makes more rate hikes from the Federal Reserve "
        "more likely.",
    ], sfx=lambda L: [(L[i] + 0.3, 'pop') for i in range(4)]),
    dict(draw=s_history, chapter='Every spike above 30', lines=[
        f"Now let's look at history. Each dot is a time the VIX closed above 30 for the first time in at least "
        f"three months. Since 1990, there have been {len(PAST)} of them, plus today.",
        "Some you'll recognize: the collapse of Lehman Brothers in September 2008, the pandemic in February 2020, "
        "the scare of August 2024, and the tariff shock of April 2025.",
        f"Here's the thing most people don't know. Once the VIX goes above 30, it usually doesn't stay there long. "
        f"The typical stretch lasted only about {RUN_MED:.0f} trading days.",
    ], sfx=lambda L: [(L[0] + 0.4 + 0.25 * i, 'tick') for i in range(0, 24, 3)] + [(L[1] + 0.4, 'pop'),
                                                                                  (L[2] + 0.3, 'ding')]),
    dict(draw=s_next, chapter='What stocks did next', lines=[
        f"So what did stocks do next? One month after those first spikes above 30, the S&P 500 was higher {UP1} "
        f"times out of {len(F1)}, with a median gain of about {MED1:.0f} percent.",
        f"!One year later, it was higher {UP12} times out of {len(F12)}, with a median gain of about {MED12:.0f} "
        "percent, not counting dividends.",
        f"But look at the worst case. After the VIX passed 30 in September 2008, the S&P 500 was still "
        f"{abs(EX['2008']['r12']):.0f} percent lower a year later. Fear can be right.",
    ], punch=lambda L: [L[1] + 0.3], sfx=lambda L: [(L[0] + 0.3, 'pop'), (L[1] + 0.3, 'hit'), (L[1] + 3.0, 'ding'),
                                                    (L[2] + 0.3, 'down')]),
    dict(draw=s_cases, chapter='Four fear spikes', lines=[
        f"Let's compare four big ones. September 2008: the VIX peaked at {EX['2008']['peak']:.0f}, and it took "
        f"{EX['2008']['calm']} trading days to fall back below 20. Stocks were {abs(EX['2008']['r12']):.0f} percent "
        "lower a year later.",
        f"February 2020: the VIX hit its record, {EX['2020']['peak']:.0f}. But a year later, stocks were "
        f"{EX['2020']['r12']:.0f} percent higher.",
        f"August 2024: a short scare. The VIX peaked at {EX['2024']['peak']:.0f} and was back below 20 within "
        f"{EX['2024']['calm']} trading days.",
        f"And April 2025, the tariff shock: a peak of {EX['2025']['peak']:.0f}, calm again in {EX['2025']['calm']} "
        f"trading days, and stocks up {EX['2025']['r12']:.0f} percent a year later.",
        f"Most spikes faded fast. In February 2018, the VIX was back below 20 in {EX18} trading days. The slow ones, "
        f"like September 2022, took {EX22}.",
    ], sfx=lambda L: [(L[i] + 0.3, 'pop') for i in range(4)]),
    dict(draw=s_march, chapter='It already happened this year', lines=[
        f"And here's something many people already forgot. This happened once before this year. On March 27, the "
        f"VIX closed at {MAR_PEAK:.0f}, and the S&P 500 hit its 2026 low of {SP_LOW26:,.0f} on March 30.",
        f"The fear faded fast. The VIX was back below 20 within {MAR_CALM} trading days.",
        f"!From that March low, the S&P 500 climbed {MAR_RUN:.0f} percent to its record in October. Anyone who sold "
        "at the bottom in March missed that.",
    ], punch=lambda L: [L[2] + 0.3], sfx=lambda L: [(L[0] + 0.3, 'whoosh'), (L[0] + 2.0, 'down'), (L[1] + 0.3, 'pop'),
                                                    (L[2] + 0.3, 'ding')]),
    dict(draw=s_bestdays, chapter='Best and worst days', lines=[
        f"One more pattern. Of the 20 best days for the S&P 500 since 1990, {BEST20} came when the VIX was already "
        "at 30 or higher.",
        f"And of the 20 worst days, {WORST20} did too. The biggest days, good and bad, cluster in fearful markets.",
        "So if fear makes you sell, you risk being out of the market on exactly the days that tend to matter most.",
    ], sfx=lambda L: [(L[0] + 0.3, 'pop'), (L[1] + 0.3, 'down'), (L[2] + 0.3, 'ding')]),
    dict(draw=s_watch, chapter='What to watch next', lines=[
        "So what should you watch from here? First, the VIX itself. When fear fades, it usually drops back below "
        "20. Second, the 10-year Treasury yield: if it keeps rising, pressure on stocks stays.",
        "Third, the Federal Reserve's December meeting, and whether it raises rates again. And fourth, chip and AI "
        "stocks, which led this year's gains and are now leading the losses.",
    ], sfx=lambda L: [(L[0] + 0.3, 'pop'), (L[0] + 4.0, 'pop'), (L[1] + 0.3, 'pop'), (L[1] + 4.0, 'pop')]),
    dict(draw=s_you, chapter='What it means for you', lines=[
        "What does this mean for you? A high VIX means bigger swings, and swings cut both ways: some of the "
        "biggest up days come during fearful weeks. Your time horizon matters most: money you need soon carries "
        "more risk in a market like this.",
        "An emergency fund means you never have to sell at a bad time. And history shows that selling in a panic "
        "can lock in losses right before a rebound, though no one can promise a rebound comes quickly.",
        "And if you invest the same amount every month, through a 401(k) for example, months like this mean your "
        "money buys shares at lower prices than it did in October.",
    ], sfx=lambda L: [(L[0] + 0.5, 'pop'), (L[0] + 3.5, 'pop'), (L[1] + 0.3, 'pop'), (L[1] + 3.5, 'pop')]),
    dict(draw=s_recap, chapter='Recap', lines=[
        f"Let's recap. Wall Street's fear index {DOUBLED}, to {V_NOW:.0f}, as the S&P 500 fell {STREAK} days in a "
        f"row. Readings that high are rare: only about {SHARE30:.0f} percent of days since 1990. After past first "
        f"spikes above 30, stocks were higher a year later {UP12} times out of {len(F12)}. Most fear spikes were "
        "short. Some, like 2008, were not.",
        "!So what are you doing right now: buying, holding, or selling? Tell me in the comments. And subscribe, "
        "so you don't miss the next update.",
        "This video is for education only. It's not financial advice.",
    ], punch=lambda L: [L[1] + 0.3], sfx=lambda L: [(L[0] + 0.3 + 2.5 * j, 'pop') for j in range(5)]
        + [(L[1] + 0.3, 'ding')]),
]
for _sc in SCENES:
    _sc['draw'] = ticker(_sc['draw'])
SHORTS = {}


def check_numbers():
    script = ' '.join(l for sc in SCENES for l in sc['lines'])
    assert TODAY.strftime('%Y-%m-%d') == '2026-11-20' and SPX.index[-1] == TODAY, (TODAY, SPX.index[-1])
    assert SP_REC_D.strftime('%Y-%m-%d') == '2026-10-06' and round(V_AT_REC, 2) == 15.01
    assert V_NOW > 25 and STREAK >= 7, (V_NOW, STREAK)
    assert round(V_MAX, 2) == 82.69 and V_MAX_D.strftime('%Y-%m-%d') == '2020-03-16' and round(V08) == 81
    assert 6 < SHARE30 < 10 and 16 < V_MED < 19
    assert len(PAST) == 22 and len(F12) == 21 and UP12 == 14 and len(F1) == 22 and UP1 == 15, (len(PAST), UP12, UP1)
    assert round(SEESAW) == 77 and BEST20 == 19 and WORST20 == 17 and round(MOVE_HI, 2) == 1.86 and round(MOVE_LO, 2) == 0.42
    assert round(MAR_PEAK) == 31 and MAR_CALM == 8 and SP_LOW26_D.strftime('%Y-%m-%d') == '2026-03-30' and round(MAR_RUN) == 23
    assert EX18 == 7 and EX22 == 47 and round(MED1) == 3 and round(V_MIN, 2) == 9.14 and V_MIN_D.year == 2017
    assert round(EX['2008']['r12']) == -12 and EX['2008']['calm'] == 321 and round(EX['2008']['peak']) == 81
    assert round(EX['2020']['r12']) == 28 and round(EX['2020']['peak']) == 83
    assert EX['2024']['calm'] == 6 and round(EX['2024']['peak']) == 39 and round(EX['2024']['r12']) == 22
    assert EX['2025']['calm'] == 26 and round(EX['2025']['peak']) == 52 and round(EX['2025']['r12']) == 23
    for s in ('not financial advice', 'Cboe', 'since 1990', 'correction'):
        assert s in script, s
    print(f'numbers check: OK  VIX {V_NOW:.2f} (prev {V_PREV:.2f}; {V_X:.2f}x the {V_AT_REC:.2f} at the record; '
          f'highest since {HIGHEST_SINCE}); 1-month move {MOVE_1M:.1f}%; S&P {SP_NOW:,.2f} {SP_DAY:+.2f}% streak '
          f'{STREAK}, {SP_DD:.2f}% from record (correction: {IN_CORR}); Nasdaq {NDQ_DD:.1f}%; median {V_MED:.1f} avg '
          f'{V_AVG:.1f}; days>=30 {SHARE30:.1f}%; firsts {len(PAST)}: 1m {UP1}/{len(F1)}, 12m {UP12}/{len(F12)} med '
          f'{MED12:.1f}%; run median {RUN_MED:.0f}d; 10y {Y_NOW:.2f}; CPI {INFL:.2f}')


if __name__ == '__main__':
    check_numbers()
    os.makedirs(BUILD, exist_ok=True)
    if '--check' in sys.argv:
        sys.exit()
    if '--stills' in sys.argv:
        previews(SCENES, SHORTS, os.path.join(BUILD, 'previews'))
        sys.exit()
    only = [int(a) for a in sys.argv[sys.argv.index('--only') + 1].split(',')] if '--only' in sys.argv else None
    total, chapters = build(SCENES, os.path.join(OUT, 'ep11_vix.mp4'), BUILD, only=only,
                            srt_path=os.path.join(OUT, 'ep11_vix.en.srt'))
    with open(os.path.join(OUT, 'ep11_chapters.txt'), 'w') as f:
        for at, name in chapters:
            f.write(f'{fmt_time(at)} {name}\n')
    print(f'total {total / 60:.1f} min')
