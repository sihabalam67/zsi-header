"""Episode 14: Why Nvidia's 37% Crash Hits Your 401(k)  (long news explainer, Thu Nov 26 2026, Thanksgiving)

Angle: "You own Nvidia even if you never bought it." This week's AI/Nvidia selloff, turned into the viewer's own
401(k) / index-fund dollars. For everyday people (23-40), not stock pickers. No forecasts, no personal advice.

What this video does better than the last ones (LEARNINGS rules 0, 0b, 0c, 1b):
1. Back in the market-news lane that earns our browse bursts (0c), but framed on the viewer's own money ("your
   401(k)", "your $100"), the shape that wins for small channels (topic lesson, Nov 21), and riding the
   highest-demand searches this week (ai bubble ~105k views/day, nvidia stock crash ~96k).
2. The opening is the PICTURE of the payoff (a 401(k) phone screen with 100 coins, 6 of them Nvidia-green that
   crack), first line 4 words, the promise + "explained simply" at ~0:15, named chapters every 40-90 s with a
   re-hook question at each turn of the back half.
3. A new look (`bold` = Poster Slam, first test of the template) and new devices (Coins as Data, Crash Quake,
   Follow the Dollar, Timeline Slam), ending at the kitchen table with one household's 401(k) math and a one-word
   comment question. Written from a blank outline; originality.py must PASS.

    python3 channel/ep14_nvidia_401k.py [--check] [--plan] [--stills] [--only 3,5]

CREATIVE BRIEF
<inputs>    Yahoo Finance daily closes (NVDA, ^GSPC, ^NDX, SPY) and the State Street SPY daily holdings file as of
            24-Nov-2026 (channel/fetch_ep14.py -> data/ep14.json); S&P 500 daily closes since 1927
            (data/GSPC_max.csv) for the history of 10%+ declines. AP news report (context only) for the Nov 25
            intraday swing. Title: TITLE below. ~11 min long video.
<direction> Family: Poster Slam on the `bold` look (near-black stage). Hero object: "your $100" as 100 coins, the 6
            Nvidia coins in chip-green (the only fully saturated color; red only for losses). Governing rule: the
            $100 never leaves - a mini 10x10 coin HUD sits top-left in every scene after the coins reveal.
            Fonts: Anton (slams, big numbers), Poppins (labels). Palette: stage #060609/#14141A, chip-green
            #76B900, loss red #FF4646, gold #FFD400 for highlights, slate grays for everyone else.
            BANNED: purple/neon tech gradients, rockets, lens flares, particle spam, constant shake, plain
            crossfades, bouncy UI easing, fake HUD numbers, text over text, holds > 1 s without motion, made-up
            numbers, real people, logos (no Nvidia logo: green coins only), clip-art.
<structure> 0:00 hook (phone + coins + slam) | 0:25 Crash Quake seismograph | aftershocks (whiplash week) |
            Coins as Data (what's in your $100) | Follow the Dollar (paycheck -> 401(k) -> fund -> 6 cents) |
            cracked coins (what it cost) | bubble? (3 drop bars) | Timeline Slam (24 declines since 1950) |
            2000 warning chart | contributions math | 3 things to check | kitchen table | recap + YES/NO
<build>     PIL scenes via engine.build; pop/spring helpers; Anton slams with print misregistration; per-scene
            camera push from the engine plus punch-ins on reveals; build dir in /dev/shm (disk is full).
<gotchas>   caption band starts ~620: keep everything above y=600. Every number asserted in check_numbers.
            Top 10 holdings = 9 companies (Alphabet has 2 share classes). Weights are as of Nov 24 (approximate
            for the October math). History is price only, before dividends.
<start>     --plan (narration, real timings) -> --stills contact sheet -> harsh critique -> fix 3 worst -> render
"""
import csv
import datetime as dt
import json
import math
import os
import statistics
import sys

os.environ.setdefault('STYLE', 'bold')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from wk2_art import *  # noqa: E402,F401,F403
from engine import build, narrate, compose  # noqa: E402

TITLE = "Why Nvidia's 37% Crash Hits Your 401(k)"
SLUG = 'ep14_nvidia_401k'
OUT = os.path.join(HERE, 'out')
BUILD = os.environ.get('EP_BUILD', os.path.join('/dev/shm', SLUG))

# ------------------------------------------------------------------ data --
D = json.load(open(os.path.join(HERE, 'data', 'ep14.json')))
CL = {k: dict(v) for k, v in D['closes'].items()}
NV_SER = D['closes']['nvda']
PEAK_D = '2026-10-06'
LAST_D = NV_SER[-1][0]
NV_PEAK, NV_NOW = CL['nvda'][PEAK_D], CL['nvda'][LAST_D]
NV_DROP = (1 - NV_NOW / NV_PEAK) * 100
NV_YEAR_AGO = NV_SER[0][1]
NV_LOW_D = '2026-11-20'
NV_LOW, NV_JUMP = CL['nvda'][NV_LOW_D], CL['nvda']['2026-11-23']
NV_LOW_DD = (1 - NV_LOW / NV_PEAK) * 100
NV_BOUNCE = (NV_JUMP / NV_LOW - 1) * 100
SP_PEAK, SP_NOW = CL['sp500'][PEAK_D], CL['sp500'][LAST_D]
SP_DROP = (1 - SP_NOW / SP_PEAK) * 100
SP_LOW_DD = (1 - CL['sp500'][NV_LOW_D] / SP_PEAK) * 100
NDX_PEAK, NDX_NOW = CL['ndx'][PEAK_D], CL['ndx'][LAST_D]
NDX_DROP = (1 - NDX_NOW / NDX_PEAK) * 100
NDX_LOW_DD = (1 - CL['ndx'][NV_LOW_D] / NDX_PEAK) * 100
SPY_PEAK, SPY_NOW = CL['spy'][PEAK_D], CL['spy'][LAST_D]
HOLD = D['spy_top10']
W_ = {h['ticker']: h['weight'] for h in HOLD}
NV_W = W_['NVDA']
TOP10 = sum(h['weight'] for h in HOLD)
N_HOLD = D['spy_count']
NV_COST = NV_W * NV_DROP / 100            # dollars of every $100, at today's slice (approximate)
FUND_100 = 100 * SP_NOW / SP_PEAK         # $100 at the record -> now (index price)
NV_SHARE_OF_DROP = NV_COST / SP_DROP * 100
NV_SER_SET = {d for d, _ in NV_SER}
# kitchen-table household (made-up example): $50,000, all in an S&P 500 index fund
HH = 50000
HH_NV, HH_TOP = HH * NV_W / 100, HH * TOP10 / 100
HH_DROP = HH * SP_DROP / 100
MONTHLY = 500
SH_PEAK, SH_NOW = MONTHLY / SPY_PEAK, MONTHLY / SPY_NOW
SH_MORE = (SH_NOW / SH_PEAK - 1) * 100

# coins: one coin = $1 of a $100 S&P 500 fund, rounded from the Nov 24 weights
GROUPS = [('Apple', W_['AAPL'], (200, 202, 212)), ('Nvidia', NV_W, None), ('Microsoft', W_['MSFT'], (104, 150, 214)),
          ('Amazon', W_['AMZN'], (214, 160, 92)), ('Alphabet', W_['GOOGL'] + W_['GOOG'], (150, 132, 210)),
          ('Broadcom', W_['AVGO'], (190, 104, 110)), ('Meta', W_['META'], (96, 176, 196)),
          ('Eli Lilly', W_['LLY'], (206, 120, 168)), ('Tesla', W_['TSLA'], (170, 170, 120))]
COUNTS = [round(w) for _, w, _ in GROUPS]
AI_NAMES = ('Nvidia', 'Microsoft', 'Amazon', 'Alphabet', 'Broadcom', 'Meta')
AI_W = sum(w for n, w, _ in GROUPS if n in AI_NAMES)
GAP_AFTER_JUMP = (1 - NV_JUMP / NV_PEAK) * 100   # still below the peak after the +31.5% day
NEED = (NV_PEAK / NV_NOW - 1) * 100              # rise needed to get back to the peak
SP_NEED = (SP_PEAK / SP_NOW - 1) * 100
NV_YEAR = (NV_NOW / NV_YEAR_AGO - 1) * 100
HH_NV_MONTH = MONTHLY * NV_W / 100


# ------------------------------------------------------ history (1950+) --
def declines(path=os.path.join(HERE, 'data', 'GSPC_max.csv'), since='1950'):
    """Every fall of 10%+ (closing prices) from a record high: peak date, depth, low date, date back at the old
    high (None if not yet). Price only, no dividends."""
    rows = [(r['date'], float(r['close'])) for r in csv.DictReader(open(path))]
    peak, pdate, ev, down = rows[0][1], rows[0][0], [], False
    for d, c in rows:
        if c > peak:
            if down:
                ev[-1]['rec'] = d
            peak, pdate, down = c, d, False
        else:
            dd = c / peak - 1
            if not down and dd <= -0.10:
                down = True
                ev.append(dict(peak=pdate, low=dd, low_d=d, rec=None))
            if down and dd < ev[-1]['low']:
                ev[-1]['low'], ev[-1]['low_d'] = dd, d
    return [e for e in ev if e['peak'] >= since], rows


def months(a, b):
    return (dt.date.fromisoformat(b) - dt.date.fromisoformat(a)).days / 30.44


EVENTS, SPX_ROWS = declines()
DONE = [e for e in EVENTS if e['rec']]
for e in DONE:
    e['mo'] = months(e['peak'], e['rec'])
N_DONE = len(DONE)
MED_MO = statistics.median(e['mo'] for e in DONE)
SMALL = [e for e in DONE if e['low'] > -0.20]
MED_SMALL = statistics.median(e['mo'] for e in SMALL)
EV = {e['peak'][:4]: e for e in DONE}
E2000, E2007, E2020, E1955 = EV['2000'], EV['2007'], EV['2020'], EV['1955']
SLOW = sorted([e for e in DONE if e['mo'] > 60], key=lambda e: e['peak'])
NOW_EV = EVENTS[-1]

# ------------------------------------------------------------ palette --
NV = (118, 185, 0)
NV_L = (178, 235, 70)
RED = CORAL
SLATE = (64, 66, 80)
SLATE_L = (120, 124, 140)
PANEL = (255, 255, 255, 14)
FULL = (0, 0, W, H)
SRC_Y = 'Yahoo Finance daily closes'
SRC_SPY = 'State Street SPY daily holdings, as of Nov 24, 2026'


# ------------------------------------------------------------ helpers --
def spring(u, w=16.0):
    """Critically damped spring 0 -> 1 (no overshoot)."""
    if u <= 0:
        return 0.0
    return 1 - (1 + w * u) * math.exp(-w * u)


def slam(c, x, y, text, size, col, t, at, family='Anton', weight=400, anchor='mm', stroke=0):
    """Poster-slam text: lands big and fast, with a 2-color print misregistration that settles."""
    u = t - at
    if u < 0:
        return
    s = 1 + 0.45 * math.exp(-u * 16)
    d = 9 * math.exp(-u * 7)
    sz = int(size * s)
    if d > 0.4:
        c.text(x - d, y + d * 0.4, text, sz, (255, 70, 70, 170), weight, anchor, family=family, shadow=False)
        c.text(x + d, y - d * 0.4, text, sz, (80, 176, 255, 170), weight, anchor, family=family, shadow=False)
    c.text(x, y, text, sz, col, weight, anchor, a=clamp(u / 0.08), family=family, stroke=stroke)


def coin(c, x, y, r, col=None, a=1.0, glyph=True, crack=0.0):
    """A coin: rim, face, inner ring, '$'. col=None = Nvidia chip-green. crack 0..1 splits it."""
    if a <= 0 or r < 1:
        return
    col = NV if col is None else col
    rim = mix(col, (0, 0, 0), 0.45)
    c.circle(x, y + r * 0.12, r, (0, 0, 0, 120), a=a)
    c.circle(x, y, r, rim, a=a)
    c.circle(x, y, r * 0.86, col, a=a)
    c.circle(x, y, r * 0.66, None, mix(col, (255, 255, 255), 0.35), max(1, r * 0.07), a=a)
    if glyph and r >= 9:
        c.text(x, y + r * 0.02, '$', int(r * 0.95), mix(col, (0, 0, 0), 0.55), 900, a=a, shadow=False)
    if crack > 0:
        k = clamp(crack)
        pts = [(x - r * 0.2, y - r), (x + r * 0.15, y - r * 0.3), (x - r * 0.25, y + r * 0.2), (x + r * 0.1, y + r)]
        c.line(pts[:1 + int(3 * k + 0.999)], (10, 10, 12), max(1.5, r * 0.12), a=a)


def coin_colors():
    cols = []
    for (name, w, col), n in zip(GROUPS, COUNTS):
        cols += [(name, col)] * n
    cols += [('rest', SLATE)] * (100 - len(cols))
    return cols


COIN_COLS = coin_colors()


def grid_pos(i, cx, cy, step):
    r_, c_ = divmod(i, 10)
    return cx + (c_ - 4.5) * step, cy + (r_ - 4.5) * step


def hud(c, t):
    """Persistent anchor: 'your $100' as a mini 10x10 coin grid, top-left."""
    a = fade(t, 0.1)
    c.rrect(20, 18, 196, 82, 14, (255, 255, 255, 16), (255, 255, 255, 40), 1, a=a)
    for i, (n, col) in enumerate(COIN_COLS):
        x, y = grid_pos(i, 52, 50, 5.4)
        c.circle(x, y, 2.2, NV if n == 'Nvidia' else (88, 90, 104), a=a)
    c.text(92, 40, 'YOUR $100', 15, WHITE, 900, anchor='lm', a=a, shadow=False)
    c.text(92, 62, f'${NV_W:.2f} Nvidia', 14, NV_L, 800, anchor='lm', a=a, shadow=False)


def headline(c, t, text, y=60, size=34):
    c.text(660, y, text, size, WHITE, 400, a=fade(t, 0.05), family='Anton')


def tagbox(c, x, y, text, col, k, size=24, fg=INK):
    if k <= 0:
        return
    s = 0.7 + 0.3 * clamp(k)
    w = len(text) * size * 0.58 * s + 36
    c.rrect(x - w / 2, y - size * s, x + w / 2, y + size * s, 10, col, a=clamp(k))
    c.text(x, y, text, int(size * s), fg, 900, a=clamp(k), shadow=False)


def beat(L, i, off=0.3):
    return L[min(i, len(L) - 1)] + off if i < len(L) else 1e9


def phone(c, x, y, s, a=1.0):
    c.rrect(x - 150 * s, y - 270 * s, x + 150 * s, y + 270 * s, 36 * s, (28, 28, 34), (90, 92, 104), 3, a=a)
    c.rrect(x - 136 * s, y - 250 * s, x + 136 * s, y + 250 * s, 26 * s, (12, 12, 16), a=a)
    c.rrect(x - 30 * s, y - 242 * s, x + 30 * s, y - 230 * s, 6 * s, (40, 40, 48), a=a)


def ser_slice(ser, a, b):
    return [(d, v) for d, v in ser if a <= d <= b]


# ------------------------------------------------------------------ scenes --
def s_hook(c, x):
    t, L = x.t, x.L
    # the payoff picture: a 401(k) app on a phone, 100 coins inside, 6 green ones
    ph = spring(t - 0.05, 10)
    px = 360
    phone(c, px, 330 + 40 * (1 - ph), 1.0, a=ph)
    c.text(px, 115, 'MY 401(k)', 22, WHITE, 900, a=ph, shadow=False)
    c.text(px, 142, 'S&P 500 index fund', 15, SLATE_L, 700, a=ph, shadow=False)
    fill_at = 0.25
    crack_at = beat(L, 2, 0.4)
    for i, (n, col) in enumerate(COIN_COLS):
        k = spring(t - fill_at - 0.012 * i, 22)
        gx, gy = grid_pos(i, px, 345, 25)
        drop = (1 - k) * -60
        cr = clamp((t - crack_at) / 0.5) if n == 'Nvidia' else 0
        fall = 0
        if n == 'Nvidia' and t > crack_at + 0.6:
            fall = 0  # cracked coins stay, dimmed
        al = k * (1 - 0.45 * clamp((t - crack_at - 0.6) / 0.4) if n == 'Nvidia' else k)
        if n != 'Nvidia' and t > beat(L, 1, 1.5):
            al *= 0.55
        coin(c, gx, gy + drop + fall, 10.5, None if n == 'Nvidia' else (col if n != 'rest' else SLATE), al,
             glyph=False, crack=cr)
    if t > beat(L, 1, 1.5) and t < crack_at:
        g = 0.5 + 0.5 * math.sin(t * 6)
        for i, (n, _) in enumerate(COIN_COLS):
            if n == 'Nvidia':
                gx, gy = grid_pos(i, px, 345, 25)
                c.circle(gx, gy, 15, None, NV_L, 2.5, a=0.4 + 0.6 * g)
    c.text(px, 500, f'${100:.2f}', 34, WHITE, 400, a=ph, family='Anton')
    # right side: the poster slam and the beats
    slam(c, 880, 175, 'YOU OWN', 92, WHITE, t, L[0] + 0.05)
    slam(c, 880, 280, 'NVIDIA', 118, NV_L, t, L[0] + 0.55)
    if len(L) > 1:
        tagbox(c, 880, 390, f'${NV_W:.2f} of every $100', NV, pop(t, beat(L, 1, 1.5)), 30)
    if len(L) > 2:
        k = pop(t, crack_at, 0.3)
        if k > 0:
            c.rrect(660, 340, 1110, 600, 20, (10, 10, 14, int(235 * clamp(k))))
            slam(c, 880, 430, f'-{NV_DROP:.1f}%', 130, RED, t, crack_at)
            c.text(880, 520, 'since October 6', 26, WHITE, 800, a=clamp(k))
            tagbox(c, 880, 568, f'one day last week: -{NV_LOW_DD:.1f}%', GOLD, pop(t, crack_at + 3.2), 20)
    if len(L) > 3 and t > L[3]:
        k = pop(t, L[3] + 0.2, 0.3)
        c.rrect(660, 340, 1110, 600, 20, (10, 10, 14, 245), a=clamp(k))
        slam(c, 880, 440, '+31.5%', 120, NV_L, t, L[3] + 0.2)
        c.text(880, 525, 'in ONE trading day?', 30, WHITE, 900, a=clamp(k))
        c.text(880, 566, 'stay for chapter 2', 20, GOLD, 800, a=fade(t, L[3] + 1.4))
    if len(L) > 4 and t > L[4]:
        c.rrect(0, 0, W, H, 0, (6, 6, 9, int(255 * fade(t, L[4], 0.3))))
        slam(c, 640, 150, 'EXPLAINED SIMPLY', 64, WHITE, t, L[4] + 0.2)
        items = ['how much of YOUR 401(k) rides on AI', 'what one crash costs every $100',
                 f'what {N_DONE} past drops say about getting back']
        for i, it in enumerate(items):
            k = spring(t - L[4] - 1.2 - 1.3 * i, 14)
            if k > 0:
                y = 260 + i * 95
                c.rrect(250, y - 36 + 20 * (1 - k), 1030, y + 36 + 20 * (1 - k), 18, (255, 255, 255, 18),
                        NV if i == 0 else SLATE_L, 3, a=k)
                coin(c, 300, y + 20 * (1 - k), 18, None if i == 0 else SLATE_L, k, glyph=True)
                c.text(340, y + 20 * (1 - k), it, 30, WHITE, 800, anchor='lm', a=k)


def s_quake(c, x):
    t, L = x.t, x.L
    hud(c, t)
    headline(c, t, "NVIDIA'S STOCK PRICE, ON A SEISMOGRAPH")
    box = (120, 120, 1180, 540)
    x0, y0, x1, y1 = box
    # recording paper: faint grid that scrolls slowly
    off = (t * 18) % 40
    for gx in range(int(x0 - off), int(x1), 40):
        if gx > x0:
            c.line([(gx, y0), (gx, y1)], (255, 255, 255, 10), 1)
    for v in (100, 150, 200, 250):
        yy = y1 - (v - 90) / (260 - 90) * (y1 - y0)
        c.line([(x0, yy), (x1, yy)], (255, 255, 255, 22), 1)
        c.text(x0 - 12, yy, f'${v}', 16, SLATE_L, 700, anchor='rm', shadow=False)
    ser = NV_SER
    n = len(ser)

    def P(i, v):
        return x0 + (x1 - x0) * i / (n - 1), y1 - (v - 90) / (260 - 90) * (y1 - y0)
    i_peak = next(i for i, (d, _) in enumerate(ser) if d == PEAK_D)
    # the needle draws up to the peak during line 1, then the slip during line 2
    a1 = beat(L, 1, 0.0)
    a2 = beat(L, 2, 0.0)
    if t < a2:
        upto = i_peak * clamp((t - L[0] - 1.0) / max(1.0, a1 - L[0] + 3.0))
    else:
        upto = i_peak + (n - 1 - i_peak) * ease(clamp((t - a2) / 2.2))
    m = int(upto)
    pts = [P(i, v) for i, (d, v) in enumerate(ser[:m + 1])]
    stress = clamp((t - a1) / 3.0) if t < a2 else 0
    col_up = mix(WHITE, GOLD, stress)
    if len(pts) > 1:
        up = pts[:i_peak + 1]
        c.line(up, col_up, 4)
        if m > i_peak:
            c.line(pts[i_peak:], RED, 5)
    if pts:
        hx, hy = pts[-1]
        jit = math.sin(t * 40) * 3 * stress
        c.line([(hx, hy + jit), (x1 + 60, hy + jit)], (255, 255, 255, 60), 2)
        c.circle(hx, hy + jit, 7, GOLD if m <= i_peak else RED)
    if t > a1 + 0.3:
        k = pop(t, a1 + 0.6)
        px_, py_ = P(i_peak, NV_PEAK)
        c.circle(px_, py_, 9, GOLD, a=clamp(k))
        tagbox(c, px_ - 120, py_ - 34, f'Oct 6: ${NV_PEAK:.2f}', GOLD, k, 22)
        if t < a2:
            c.text(px_ - 330, py_ + 70, 'pressure building...', 24, GOLD, 800, a=0.5 + 0.5 * math.sin(t * 5))
        sx, sy = P(0, NV_YEAR_AGO)
        tagbox(c, sx + 120, sy + 46, f'a year ago: ${NV_YEAR_AGO:.2f}', SLATE_L, pop(t, a1 + 0.2), 18)
    if t > a2 + 2.2:
        lx, ly = P(n - 1, NV_NOW)
        tagbox(c, lx - 110, ly + 44, f'Nov 25: ${NV_NOW:.2f}', RED, pop(t, a2 + 2.2), 22)
        slam(c, 420, 480, f'-{NV_DROP:.1f}%', 96, RED, t, a2 + 2.6)
        if t < a2 + 3.0:  # the slip: a flash
            c.rrect(0, 0, W, H, 0, (255, 70, 70, int(70 * (1 - clamp((t - a2 - 2.6) / 0.3)))) if t > a2 + 2.6 else None)
    if len(L) > 3 and t > L[3]:
        k = spring(t - L[3] - 0.2, 14)
        c.rrect(330, 150, 950, 330, 22, (12, 12, 16, 240), WHITE, 2, a=k)
        c.text(640, 200, 'a share bought at the top for $100', 26, WHITE, 800, a=k)
        c.text(640, 275, f'= ${100 - NV_DROP:.2f} on Wednesday', 52, RED, 400, a=k, family='Anton')
    source(c, t, SRC_Y + ' (NVDA)')


def s_after(c, x):
    t, L = x.t, x.L
    hud(c, t)
    headline(c, t, 'THE AFTERSHOCKS: NVIDIA, DAY BY DAY')
    days = [p for p in NV_SER if p[0] >= '2026-11-10']
    prev = {days[i][0]: (days[i - 1][1] if i else CL['nvda'].get('2026-11-09')) for i in range(len(days))}
    x0, x1, y0, y1 = 150, 1160, 150, 470

    def Y(v):
        return y1 - (v - 110) / (180 - 110) * (y1 - y0)
    for v in (120, 140, 160, 180):
        c.line([(x0, Y(v)), (x1, Y(v))], (255, 255, 255, 18), 1)
        c.text(x0 - 12, Y(v), f'${v}', 16, SLATE_L, 700, anchor='rm', shadow=False)
    step = (x1 - x0) / len(days)
    for i, (d, v) in enumerate(days):
        at = L[0] + 0.4 + 0.35 * i
        k = spring(t - at, 18)
        if k <= 0:
            continue
        p = prev[d]
        cx = x0 + step * (i + 0.5)
        hi, lo = max(p, v), min(p, v)
        col = NV_L if v >= p else RED
        top = Y(hi)
        bot = Y(lo)
        mid = (top + bot) / 2
        h2 = (bot - top) / 2 * k
        c.rrect(cx - step * 0.32, mid - max(2, h2), cx + step * 0.32, mid + max(2, h2), 6, col, a=k)
        c.text(cx, y1 + 30, dt.date.fromisoformat(d).strftime('%b %-d'), 15, SLATE_L, 700, a=k, shadow=False)
        if d == NV_LOW_D and len(L) > 1 and t > L[1]:
            tagbox(c, cx, Y(lo) + 36, f'${NV_LOW:.2f}', RED, pop(t, L[1] + 0.3), 20)
            pulse_ring(c, t, cx, Y(lo), RED)
        if d == '2026-11-23' and len(L) > 2 and t > L[2]:
            tagbox(c, cx, Y(hi) - 34, f'+{NV_BOUNCE:.1f}%  ${NV_JUMP:.2f}', NV, pop(t, L[2] + 0.3), 20)
        if d == LAST_D and len(L) > 3 and t > L[3]:
            tagbox(c, cx - 40, Y(lo) + 36, f'${NV_NOW:.2f}', RED, pop(t, L[3] + 0.3), 20)
    if len(L) > 1 and t > L[1] + 1.5:
        tagbox(c, 400, 125, f'down {NV_LOW_DD:.1f}% from the peak', GOLD, pop(t, L[1] + 1.5), 20)
    if len(L) > 4 and t > L[4]:
        k = spring(t - L[4] - 0.2, 14)
        c.rrect(240, 140, 1040, 470, 24, (10, 10, 14, 245), GOLD, 3, a=k)
        c.text(640, 190, 'Wednesday, Nov 25, during the day (AP report)', 24, GOLD, 800, a=k)
        for j, (lab, v) in enumerate((('S&P 500', '-3.2%'), ('Nasdaq', '-4.6%'))):
            kk = spring(t - L[4] - 1.2 - 0.8 * j, 16)
            c.text(450 + j * 380, 280, v, 86, RED, 400, a=kk, family='Anton')
            c.text(450 + j * 380, 350, f'{lab}: at its worst', 22, WHITE, 800, a=kk)
        c.text(640, 420, '...then both closed only slightly down', 26, WHITE, 800, a=fade(t, L[4] + 3.5))
    if len(L) > 5 and t > L[5]:
        c.rrect(0, 0, W, H, 0, (6, 6, 9, int(255 * fade(t, L[5], 0.3))))
        slam(c, 640, 250, 'NEVER BOUGHT A SHARE?', 70, WHITE, t, L[5] + 0.2)
        slam(c, 640, 350, 'YOU STILL FELT IT.', 70, NV_L, t, L[5] + 1.6)
    source(c, t, SRC_Y + '; AP news report, Nov 25, 2026')


def pulse_ring(c, t, x, y, col):
    g = (t * 1.4) % 1
    c.circle(x, y, 10 + 26 * g, None, col, 3, a=1 - g)


def s_coins(c, x):
    t, L = x.t, x.L
    headline(c, t, 'WHAT IS INSIDE $100 OF AN S&P 500 INDEX FUND')
    cx, cy, step = 380, 335, 42
    # line 0: coins pour in; line 2: companies light up group by group
    light = beat(L, 2, 0.2)
    order = []
    for name, _, _ in GROUPS:
        order.append(name)
    for i, (n, col) in enumerate(COIN_COLS):
        k = spring(t - L[0] - 0.6 - 0.02 * i, 20)
        if k <= 0:
            continue
        gx, gy = grid_pos(i, cx, cy, step)
        gi = order.index(n) if n in order else 99
        lit = gi < 99 and t > light + gi * 0.9 * (1 if gi < 3 else 0.7)
        if n == 'Nvidia' and len(L) > 2 and t > light + 0.9:
            col_ = None
        elif lit:
            col_ = col if col else NV
        else:
            col_ = SLATE
        bump = 0
        if lit and gi < 99:
            at = light + gi * 0.9 * (1 if gi < 3 else 0.7)
            bump = -10 * math.exp(-(t - at) * 8) * math.sin((t - at) * 20)
        coin(c, gx, gy - (1 - k) * 120 + bump, 17.5, col_, k, glyph=n == 'Nvidia' and col_ is None)
    if len(L) > 1:
        tagbox(c, 380, 560, f'{N_HOLD} holdings, as of Nov 24', SLATE_L, pop(t, L[1] + 0.4), 20)
    # legend
    for gi, ((name, w, col), n) in enumerate(zip(GROUPS, COUNTS)):
        at = light + gi * 0.9 * (1 if gi < 3 else 0.7)
        k = spring(t - at, 16)
        if k <= 0:
            continue
        y = 130 + gi * 46
        coin(c, 790, y, 13, col if name != 'Nvidia' else None, k, glyph=False)
        big = name == 'Nvidia'
        c.text(815, y, name, 26 if big else 22, NV_L if big else WHITE, 900 if big else 800, anchor='lm', a=k)
        c.text(1150, y, f'${w:.2f}', 26 if big else 22, NV_L if big else WHITE, 900, anchor='rm', a=k)
    if len(L) > 4 and t > L[4]:
        k = pop(t, L[4] + 0.3)
        c.rrect(770, 535, 1170, 600, 16, GOLD, a=clamp(k))
        c.text(970, 567, f'TOP 10 = ${TOP10:.2f}', 30, INK, 400, a=clamp(k), family='Anton', shadow=False)
        g = 0.5 + 0.5 * math.sin(t * 5)
        c.rrect(cx - 5 * step - 4, cy - 5 * step - 4, cx + 5 * step + 4, cy - 1.3 * step, 12, None, GOLD, 3,
                a=(0.35 + 0.65 * g) * clamp(k))
    source(c, t, SRC_SPY)


def s_comeback(c, x):
    t, L = x.t, x.L
    hud(c, t)
    headline(c, t, 'THE COMEBACK MATH')
    x0, x1, y0, y1 = 170, 760, 140, 520

    def Y(v):
        return y1 - (v - 0) / 260 * (y1 - y0)
    steps = [('Oct 6', NV_PEAK, GOLD), ('Nov 20', NV_LOW, RED), ('Nov 23', NV_JUMP, NV), ('Nov 25', NV_NOW, RED)]
    bw = (x1 - x0) / len(steps)
    c.line([(x0, Y(NV_PEAK)), (x1 + 40, Y(NV_PEAK))], (255, 212, 0, 130), 2)
    for i, (lab, v, col) in enumerate(steps):
        at = L[0] + 0.3 + 0.6 * i
        k = spring(t - at, 16)
        if k <= 0:
            continue
        bx = x0 + bw * i + bw * 0.18
        top = y1 - (y1 - Y(v)) * k
        c.rrect(bx, top, bx + bw * 0.64, y1, 10, col, a=k)
        c.text(bx + bw * 0.32, top - 22, f'${v:.2f}', 22, WHITE, 900, a=k)
        c.text(bx + bw * 0.32, y1 + 24, lab, 18, SLATE_L, 800, a=k, shadow=False)
    if len(L) > 1 and t > L[1]:
        bx = x0 + bw * 2 + bw * 0.5
        k = pop(t, L[1] + 0.3)
        c.line([(bx, Y(NV_JUMP) - 40), (bx, Y(NV_PEAK) + 6)], WHITE, 3, a=clamp(k))
        tagbox(c, bx, (Y(NV_JUMP) + Y(NV_PEAK)) / 2 - 20, f'still -{GAP_AFTER_JUMP:.0f}%', WHITE, k, 20)
    if len(L) > 2 and t > L[2]:
        k = spring(t - L[2] - 0.2, 14)
        c.rrect(820, 150, 1180, 400, 24, (12, 12, 16, 240), NV, 3, a=k)
        c.text(1000, 195, f'after -{NV_DROP:.1f}%', 26, RED, 900, a=k)
        c.text(1000, 285, f'+{NEED * ease(clamp((t - L[2] - 0.6) / 1.4)):.1f}%', 92, NV_L, 400, a=k, family='Anton')
        c.text(1000, 365, 'just to get back', 24, WHITE, 800, a=k)
        if t > L[2] + 4.5:
            tagbox(c, 1000, 450, 'lose half = need to double', GOLD, pop(t, L[2] + 4.5), 20)
    if len(L) > 3 and t > L[3]:
        tagbox(c, 1000, 520, f'your fund: -{SP_DROP:.1f}% needs +{SP_NEED:.1f}%', SLATE_L, pop(t, L[3] + 0.3), 20)
    source(c, t, SRC_Y + ' (NVDA, ^GSPC)')


def s_aislice(c, x):
    t, L = x.t, x.L
    hud(c, t)
    headline(c, t, 'YOUR HIDDEN AI SLICE')
    cx, cy, step = 380, 330, 40
    roles = {'Nvidia': 'chips', 'Broadcom': 'chips', 'Microsoft': 'cloud', 'Amazon': 'cloud', 'Alphabet': 'cloud',
             'Meta': 'apps'}
    lit_at = {'chips': beat(L, 1, 0.3), 'cloud': beat(L, 1, 3.6), 'apps': beat(L, 1, 8.2)}
    for i, (n, col) in enumerate(COIN_COLS):
        gx, gy = grid_pos(i, cx, cy, step)
        role = roles.get(n)
        on = role is not None and t > lit_at[role]
        k = spring(t - lit_at[role], 16) if on else 0
        colr = mix(SLATE, NV if n == 'Nvidia' else (60, 170, 90), k) if role else (46, 48, 58)
        coin(c, gx, gy - 8 * k * math.exp(-(t - lit_at.get(role, 0)) * 4) if on else gy, 16, colr,
             0.5 + 0.5 * spring(t - L[0] - 0.2, 12), glyph=False)
    rows = [('chips', 'make the chips', 'Nvidia, Broadcom'), ('cloud', 'rent out AI computing', 'Microsoft, Amazon, Alphabet'),
            ('apps', 'build AI into apps', 'Meta')]
    for j, (role, what, who) in enumerate(rows):
        k = spring(t - lit_at[role], 14)
        if k <= 0:
            continue
        y = 170 + j * 105
        c.rrect(760, y - 42, 1180, y + 42, 18, (255, 255, 255, 14), (60, 170, 90), 2, a=k)
        c.text(785, y - 14, what, 24, WHITE, 900, anchor='lm', a=k)
        c.text(785, y + 18, who, 19, SLATE_L, 800, anchor='lm', a=k, shadow=False)
    if len(L) > 2 and t > L[2]:
        k = pop(t, L[2] + 0.3)
        c.rrect(760, 500, 1180, 590, 18, NV, a=clamp(k))
        v = AI_W * ease(clamp((t - L[2] - 0.3) / 1.2))
        c.text(970, 545, f'${v:.2f} of every $100', 36, INK, 400, a=clamp(k), family='Anton', shadow=False)
    source(c, t, SRC_SPY + '; Alphabet = both share classes')


def s_follow(c, x):
    t, L = x.t, x.L
    hud(c, t)
    headline(c, t, 'FOLLOW ONE DOLLAR FROM YOUR PAYCHECK')
    stages = [L[0] + 0.3, beat(L, 0, 4.2), beat(L, 1, 0.3), beat(L, 2, 0.3)]
    cur = max([i for i, s in enumerate(stages) if t >= s] or [0])
    # breadcrumb path at the bottom
    names = ['PAYCHECK', '401(k)', 'INDEX FUND', 'NVIDIA SLICE']
    for i, nm in enumerate(names):
        bx = 230 + i * 270
        on = i <= cur and t >= stages[i]
        c.rrect(bx - 105, 552, bx + 105, 592, 20, NV if (on and i == 3) else ((255, 255, 255, 40) if on else PANEL),
                a=1)
        c.text(bx, 572, nm, 18, INK if (on and i == 3) else (WHITE if on else SLATE_L), 900, shadow=False)
        if i < 3:
            c.line([(bx + 110, 572), (bx + 160, 572)], SLATE_L if not on else WHITE, 3)
    for i in range(4):
        if t < stages[i]:
            continue
        u = t - stages[i]
        nxt = stages[i + 1] if i < 3 else 1e9
        if t >= nxt + 0.5:
            continue
        k_in = spring(u, 14)
        if t >= nxt:  # fly through: grows and fades
            v = (t - nxt) / 0.5
            sc, al = 1 + 2.5 * ease(v), 1 - v
        else:
            sc, al = 0.6 + 0.4 * k_in, k_in
        draw_stage(c, i, 640, 310, sc, al, t, u)
    # a coin travels the breadcrumb
    seg_i = cur + clamp((t - stages[cur]) / 0.8)
    cx_ = 230 + min(3, seg_i) * 270
    coin(c, cx_, 520, 14, None if cur == 3 else GOLD, 1)


def draw_stage(c, i, x, y, s, a, t, u):
    if a <= 0:
        return
    if i == 0:  # pay stub
        c.rrect(x - 230 * s, y - 150 * s, x + 230 * s, y + 150 * s, 16 * s, CREAM, a=a)
        c.text(x - 200 * s, y - 110 * s, 'PAY STUB', int(26 * s), INK, 900, anchor='lm', a=a, shadow=False)
        rows = [('Gross pay', '$2,500.00'), ('401(k) contribution', '-$150.00'), ('Taxes', '...')]
        for j, (l_, v) in enumerate(rows):
            yy = y + (-50 + j * 50) * s
            c.text(x - 200 * s, yy, l_, int(20 * s), INK, 800 if j != 1 else 900, anchor='lm', a=a, shadow=False)
            c.text(x + 200 * s, yy, v, int(20 * s), INK if j != 1 else (20, 120, 40), 900, anchor='rm', a=a,
                   shadow=False)
        c.rrect(x - 210 * s, y - 2 * s + 25 * s, x + 210 * s, y + 25 * s + 28 * s, 6 * s, None, (20, 120, 40), 3, a=a)
        c.text(x, y + 120 * s, 'example pay stub', int(16 * s), MUTED, 700, a=a, shadow=False)
    elif i == 1:  # 401(k) jar
        c.rrect(x - 140 * s, y - 120 * s, x + 140 * s, y + 170 * s, 40 * s, (255, 255, 255, 30), WHITE, 4, a=a)
        c.rrect(x - 110 * s, y - 160 * s, x + 110 * s, y - 120 * s, 10 * s, (200, 200, 210), a=a)
        c.text(x, y - 60 * s, '401(k)', int(48 * s), WHITE, 400, a=a, family='Anton')
        for j in range(9):
            yy = y + 140 * s - j * 15 * s - 8 * s * math.sin(min(u, 3) * 2 + j)
            coin(c, x + ((j % 3) - 1) * 60 * s, yy, 18 * s, GOLD, a * clamp((u - j * 0.12) / 0.2), glyph=False)
        c.text(x, y + 205 * s, 'before taxes, from every paycheck', int(18 * s), SLATE_L, 700, a=a, shadow=False)
    elif i == 2:  # the fund: a pie of hundreds of slices
        r = 170 * s
        n = 60
        for j in range(n):
            a0 = -90 + 360 * j / n
            col = NV if j in (0, 1, 2, 3) else (SLATE if j % 2 else SLATE_L)
            if j == 0 or j == 1 or j == 2 or j == 3:
                pass
            pts = [(x, y)] + [(x + r * math.cos(math.radians(a0 + d * 360 / n / 4)),
                               y + r * math.sin(math.radians(a0 + d * 360 / n / 4))) for d in range(5)]
            c.poly(pts, col, (6, 6, 9), 1.5, a=a * clamp((u - j * 0.015) / 0.2))
        c.circle(x, y, 70 * s, (6, 6, 9), a=a)
        c.text(x, y - 10 * s, f'{N_HOLD}', int(46 * s), WHITE, 400, a=a, family='Anton')
        c.text(x, y + 30 * s, 'holdings', int(18 * s), SLATE_L, 800, a=a, shadow=False)
        tagbox(c, x + 260 * s, y - 120 * s, 'bigger company = bigger slice', GOLD, a * clamp((u - 1.0) / 0.3), int(20 * s))
    else:  # one dollar -> 100 cents, 6 green
        for j in range(100):
            gx, gy = grid_pos(j, x, y - 20, 26 * s)
            green = j < round(NV_W)
            k = clamp((u - j * 0.01) / 0.2)
            c.circle(gx, gy, 10 * s, NV if green else SLATE, a=a * k)
        c.text(x + 330 * s, y - 60 * s, f'{NV_W:.2f}', int(96 * s), NV_L, 400, a=a, family='Anton')
        c.text(x + 330 * s, y + 10 * s, 'cents of every dollar', int(22 * s), WHITE, 800, a=a)
        c.text(x + 330 * s, y + 45 * s, 'go to Nvidia', int(22 * s), WHITE, 800, a=a)


def s_cost(c, x):
    t, L = x.t, x.L
    hud(c, t)
    headline(c, t, 'WHAT THE CRASH COST EVERY $100')
    # left: the Nvidia stack, a 37.6% bite comes off
    k0 = spring(t - L[0] - 0.3, 14)
    stack_h = 6.05 * 52
    base = 520
    cut = clamp((t - L[0] - 3.0) / 1.2)
    lost_h = stack_h * NV_DROP / 100
    c.rrect(200, base - stack_h * k0, 420, base, 12, NV, a=k0)
    if cut > 0:
        yoff = 140 * ease(clamp((t - L[0] - 4.2) / 1.0))
        c.rrect(200, base - stack_h - yoff * 0, 420, base - stack_h + lost_h, 12, RED, a=1)
        c.text(310, base - stack_h + lost_h / 2, f'-${NV_COST:.2f}', 40, WHITE, 400, a=cut, family='Anton')
        c.rrect(200, base - stack_h + lost_h, 420, base, 12, NV)
        c.text(310, base - (stack_h - lost_h) / 2, f'${NV_W - NV_COST:.2f}', 34, INK, 400, a=cut, family='Anton',
               shadow=False)
    c.text(310, base + 34, f'your ${NV_W:.2f} of Nvidia', 22, NV_L, 900, a=k0)
    c.text(310, base + 62, f'x {NV_DROP:.1f}% drop', 18, SLATE_L, 800, a=k0, shadow=False)
    if len(L) > 1 and t > L[1]:
        tagbox(c, 310, 160, 'in October its slice was bigger', GOLD, pop(t, L[1] + 0.3), 18)
    # right: the whole $100 counts down to $91.86
    if len(L) > 2 and t > L[2]:
        k = spring(t - L[2] - 0.2, 14)
        v = 100 - (100 - FUND_100) * ease(clamp((t - L[2] - 0.8) / 2.0))
        c.rrect(560, 150, 1120, 380, 24, (255, 255, 255, 14), WHITE, 2, a=k)
        c.text(840, 195, '$100 in an S&P 500 fund, Oct 6 record', 22, WHITE, 800, a=k)
        c.text(840, 285, f'${v:.2f}', 104, RED if v < 99.5 else WHITE, 400, a=k, family='Anton')
        c.text(840, 355, f'Wednesday: -{SP_DROP:.1f}%', 22, SLATE_L, 800, a=k)
    if len(L) > 3 and t > L[3]:
        k = spring(t - L[3] - 0.2, 14)
        cx, cy, r = 840, 480, 78
        frac = NV_SHARE_OF_DROP / 100
        c.circle(cx, cy, r, SLATE, a=k)
        pts = [(cx, cy)] + [(cx + r * math.cos(math.radians(-90 + 360 * frac * j / 30)),
                              cy + r * math.sin(math.radians(-90 + 360 * frac * j / 30))) for j in range(31)]
        if k > 0.5:
            c.poly(pts, NV, a=k)
        c.text(cx + 110, cy - 18, 'more than a quarter', 24, NV_L, 900, anchor='lm', a=k)
        c.text(cx + 110, cy + 16, 'of the fund\'s drop', 22, WHITE, 800, anchor='lm', a=k)
    source(c, t, 'SPY weights Nov 24 x NVDA change; S&P 500 closes (approximate)')


def s_bubble(c, x):
    t, L = x.t, x.L
    hud(c, t)
    headline(c, t, 'IS THE AI BUBBLE BURSTING?')
    # line 0: a trembling bubble
    if t < beat(L, 1, 0.0):
        k = spring(t - L[0] - 0.2, 10)
        r = 150 * k * (1 + 0.03 * math.sin(t * 3))
        jx = math.sin(t * 23) * 2 * clamp((t - L[0] - 2) / 3)
        c.circle(640 + jx, 330, r, (120, 200, 255, 30), (180, 220, 255), 4, a=k)
        c.arc(640 + jx - r * 0.25, 330 - r * 0.25, r * 0.55, 200, 260, (255, 255, 255), 6, a=k)
        c.text(640 + jx, 330, 'AI', 110, WHITE, 400, a=k * 0.8, family='Anton')
        tagbox(c, 640, 540, 'prices racing ahead of profits... then pop', GOLD, pop(t, L[0] + 3.0), 20)
    else:
        items = [('Nvidia', NV_DROP, NV), ('Nasdaq-100 (tech-heavy)', NDX_DROP, (170, 120, 220)),
                 ('S&P 500 (your index fund)', SP_DROP, SLATE_L)]
        for i, (lab, v, col) in enumerate(items):
            at = beat(L, 1, 0.4) + 1.6 * i
            k = spring(t - at, 14)
            if k <= 0:
                continue
            y = 170 + i * 120
            w = v * 14 * ease(clamp((t - at) / 0.9))
            c.text(130, y - 34, lab, 24, WHITE, 800, anchor='lm', a=k)
            c.rrect(130, y - 12, 130 + max(14, w), y + 40, 10, col, a=k)
            c.text(150 + w, y + 14, f'-{v * ease(clamp((t - at) / 0.9)):.1f}%', 40, col if col != SLATE_L else WHITE,
                   400, anchor='lm', a=k, family='Anton')
        if len(L) > 2 and t > L[2]:
            tagbox(c, 860, 520, f'Nov 20: Nasdaq-100 closed {NDX_LOW_DD:.1f}% below its peak', GOLD, pop(t, L[2] + 2.5), 19)
            c.text(1000, 140, 'more tech = bigger fall', 22, GOLD, 900, a=fade(t, L[2] + 0.4))
        if len(L) > 3 and t > L[3]:
            c.rrect(0, 0, W, H, 0, (6, 6, 9, int(255 * fade(t, L[3], 0.3))))
            slam(c, 640, 240, 'BUBBLE OR SHAKEOUT?', 76, WHITE, t, L[3] + 0.2)
            slam(c, 640, 340, 'NOBODY KNOWS YET.', 60, GOLD, t, L[3] + 2.0)
            c.text(640, 430, 'but we do have history', 28, NV_L, 800, a=fade(t, beat(L, 3, 4.5)))
    source(c, t, SRC_Y + ' (NVDA, ^NDX, ^GSPC), Oct 6 to Nov 25')


def s_history(c, x):
    t, L = x.t, x.L
    hud(c, t)
    headline(c, t, f'EVERY 10%+ DROP FROM A RECORD SINCE 1950')
    x0, x1, ya, depth = 110, 1170, 140, 250

    def X(d):
        y_ = int(d[:4]) + (int(d[5:7]) - 1) / 12
        return x0 + (x1 - x0) * (y_ - 1950) / (2027 - 1950)
    c.line([(x0, ya), (x1, ya)], WHITE, 3)
    for yr in range(1950, 2030, 10):
        xx = X(f'{yr}-01-01')
        c.line([(xx, ya - 8), (xx, ya + 8)], WHITE, 2)
        c.text(xx, ya - 26, str(yr), 18, SLATE_L, 800, shadow=False)
    span = max(6.0, beat(L, 1, 0.0) - L[0] - 1.0) if len(L) > 1 else 10
    for j, e in enumerate(DONE):
        at = L[0] + 0.8 + span * j / len(DONE)
        k = spring(t - at, 22)
        if k <= 0:
            continue
        xx = X(e['peak'])
        h = depth * (-e['low']) / 0.6 * k
        col = NV if e['mo'] <= MED_MO else (RED if e['mo'] > 48 else GOLD)
        c.rrect(xx - 6, ya + 4, xx + 6, ya + 4 + h, 4, col, a=k)
    if len(L) > 1 and t > L[1]:
        for e, lab in ((E1955, f"1955: {E1955['mo']:.0f} mo"), (E2020, f"2020: {E2020['mo']:.0f} mo")):
            xx = X(e['peak'])
            tagbox(c, xx + (40 if e is E1955 else -10), ya + 26 + depth * (-e['low']) / 0.6 + 16, lab, NV,
                   pop(t, L[1] + (0.3 if e is E1955 else 2.6)), 17)
    if len(L) > 2 and t > L[2]:
        k = pop(t, L[2] + 0.3)
        c.rrect(400, 408, 880, 498, 20, (10, 10, 14, 235), GOLD, 3, a=clamp(k))
        slam(c, 640, 442, f'MEDIAN: {MED_MO:.0f} MONTHS', 50, GOLD, t, L[2] + 0.3)
        c.text(640, 482, 'from the old high, back to it', 18, WHITE, 800, a=clamp(k))
    if len(L) > 3 and t > L[3]:
        tagbox(c, 640, 530, f'drops that stopped short of 20%: about {MED_SMALL:.0f} months', NV, pop(t, L[3] + 0.3), 19)
        c.text(640, 570, 'price only, before dividends. The past promises nothing.', 17, SLATE_L, 700,
               a=fade(t, L[3] + 1.0), shadow=False)
    if len(L) > 4 and t > L[4]:
        xx = X(NOW_EV['peak'])
        h = depth * (-NOW_EV['low']) / 0.6
        g = 0.5 + 0.5 * math.sin(t * 6)
        c.rrect(xx - 7, ya + 4, xx + 7, ya + 4 + h, 4, WHITE, a=0.5 + 0.5 * g)
        tagbox(c, xx - 120, ya + h + 40, f'#{len(EVENTS)}: now, -{-NOW_EV["low"] * 100:.1f}%', WHITE, pop(t, L[4] + 0.3), 18)
    source(c, t, 'S&P 500 daily closes 1950-2026 (Yahoo Finance ^GSPC), our count')


def s_2000(c, x):
    t, L = x.t, x.L
    hud(c, t)
    headline(c, t, 'THE LAST TIME A TECH BOOM ENDED BADLY')
    rows = [(d, v) for d, v in SPX_ROWS if '1996-01-01' <= d <= '2009-12-31' and d[8:10] <= '07']
    mo = {}
    for d, v in rows:
        mo.setdefault(d[:7], v)
    pts_ = sorted(mo.items())
    x0, x1, y0, y1 = 140, 1160, 130, 470

    def P(d, v):
        y_ = int(d[:4]) + (int(d[5:7]) - 1) / 12
        return x0 + (x1 - x0) * (y_ - 1996) / 14, y1 - (v - 500) / (1700 - 500) * (y1 - y0)
    for v in (600, 1000, 1400):
        c.line([(x0, P('1996-01', v)[1]), (x1, P('1996-01', v)[1])], (255, 255, 255, 18), 1)
        c.text(x0 - 12, P('1996-01', v)[1], f'{v:,}', 16, SLATE_L, 700, anchor='rm', shadow=False)
    for yr in range(1996, 2011, 2):
        c.text(P(f'{yr}-01', 500)[0], y1 + 24, str(yr), 16, SLATE_L, 700, shadow=False)
    k = ease(clamp((t - L[0] - 0.4) / 6.0))
    m = int(len(pts_) * k)
    c.line([P(d, v) for d, v in pts_[:max(2, m)]], WHITE, 4)
    pk = SPX_ROWS[[d for d, _ in SPX_ROWS].index(E2000['peak'])]
    px_, py_ = P(*pk)
    if k > 0.35:
        c.line([(px_, py_), (x1, py_)], (255, 212, 0, 120), 2)
        tagbox(c, px_, py_ - 30, 'Mar 2000 record', GOLD, pop(t, L[0] + 2.4), 18)
    if len(L) > 1 and t > L[1]:
        lo = [p for p in SPX_ROWS if p[0] == E2000['low_d']][0]
        lx, ly = P(*lo)
        slam(c, lx, ly + 50, f'-{-E2000["low"] * 100:.0f}%', 60, RED, t, L[1] + 0.3)
    if len(L) > 2 and t > L[2]:
        rx, _ = P(E2000['rec'], 500)
        g = 0.5 + 0.5 * math.sin(t * 5)
        c.circle(rx, py_, 10, GOLD, a=0.6 + 0.4 * g)
        c.rrect(px_, py_ - 6, rx, py_ + 6, 6, (255, 212, 0, 90))
        tagbox(c, (px_ + rx) / 2, py_ + 40, f'{E2000["mo"] / 12:.1f} years to get back', GOLD, pop(t, L[2] + 0.4), 24)
    if len(L) > 3 and t > L[3]:
        c.rrect(0, 95, W, 600, 0, (6, 6, 9, int(215 * fade(t, L[3], 0.3))))
        k2 = spring(t - L[3] - 0.2, 14)
        for j, (age, txt, col) in enumerate((('60', 'needs the money soon: brutal', RED),
                                             ('30', 'decades to go, still adding', NV))):
            y = 260 + j * 100
            c.rrect(700 - 300, y - 34, 1150 - 300, y + 34, 18, (12, 12, 16, 240), col, 3, a=k2 if j == 0 else
                    spring(t - beat(L, 4, 0.2), 14))
            kk = k2 if j == 0 else spring(t - beat(L, 4, 0.2), 14)
            c.text(440, y, f'age {age}', 26, col, 900, anchor='lm', a=kk)
            c.text(560, y, txt, 21, WHITE, 800, anchor='lm', a=kk)
    source(c, t, 'S&P 500 closes (Yahoo Finance ^GSPC), price only')


def s_shares(c, x):
    t, L = x.t, x.L
    hud(c, t)
    headline(c, t, 'THE PAYCHECK MATH MOST PEOPLE MISS')
    for j, (lab, price, sh, col) in enumerate((('Oct 6, at the top', SPY_PEAK, SH_PEAK, SLATE_L),
                                               ('Wednesday, Nov 25', SPY_NOW, SH_NOW, NV))):
        at = (L[0] + 1.0) if j == 0 else beat(L, 1, 3.4)
        k = spring(t - at, 14)
        if k <= 0:
            continue
        y = 200 + j * 170
        coin(c, 180, y + 10, 36, GOLD, k)
        c.text(240, y - 20, f'${MONTHLY} buys', 26, WHITE, 800, anchor='lm', a=k)
        c.text(240, y + 22, lab, 18, SLATE_L, 700, anchor='lm', a=k, shadow=False)
        g = ease(clamp((t - at - 0.4) / 1.2))
        w = 600 * sh / 0.72 * g
        c.rrect(480, y - 24, 480 + w, y + 36, 12, col, a=k)
        c.text(500 + w, y + 6, f'{sh * g:.3f}', 54, col if col != SLATE_L else WHITE, 400, anchor='lm', a=k,
               family='Anton')
        c.text(480, y + 62, f'shares of the SPY fund at ${price:.2f}', 17, SLATE_L, 700, anchor='lm', a=k, shadow=False)
    if len(L) > 2 and t > L[2]:
        tagbox(c, 820, 130, f'about {SH_MORE:.0f}% more shares for the same $500', NV, pop(t, L[2] + 0.3), 22)
    if len(L) > 3 and t > L[3]:
        c.text(640, 560, 'how regular contributions work. Not a prediction: prices can keep falling.', 19, GOLD, 800,
               a=fade(t, L[3] + 0.3))
    source(c, t, SRC_Y + ' (SPY closes)')


def s_check(c, x):
    t, L = x.t, x.L
    hud(c, t)
    headline(c, t, '3 THINGS YOU CAN LOOK UP TONIGHT (NO TRADING NEEDED)')
    cards = [('search', 'Your fund\'s name', 'its top 10 holdings\nare listed online'),
             ('copy', 'Overlap', 'two funds can both\nhold Nvidia'),
             ('hourglass', 'Your timeline', 'when do you need\nthis money?')]
    for i, (ic, ttl, sub) in enumerate(cards):
        at = beat(L, i + 1, 0.3) if len(L) > i + 1 else L[0] + 1 + 2 * i
        k = max(0.25 * spring(t - L[0] - 0.4 - 0.4 * i, 14), spring(t - at, 14))
        if k <= 0:
            continue
        cx = 260 + i * 380
        y = 330 + 30 * (1 - k)
        c.rrect(cx - 165, y - 170, cx + 165, y + 170, 26, (255, 255, 255, 14), NV if i == 0 else SLATE_L, 3, a=k)
        c.text(cx, y - 125, str(i + 1), 44, GOLD, 400, a=k, family='Anton')
        c.circle(cx, y - 40, 50, (255, 255, 255, 18), a=k)
        c.icon(ic, cx, y - 40, 54, WHITE, a=k)
        c.text(cx, y + 40, ttl, 28, WHITE, 900, a=k)
        for j, part in enumerate(sub.split('\n')):
            c.text(cx, y + 85 + j * 30, part, 20, SLATE_L, 700, a=k, shadow=False)
    c.text(640, 560, 'education only, not financial advice', 18, SLATE_L, 700, a=fade(t, 1), shadow=False)


def person_at(c, x, y, s, col, t, ph, mood):
    person(c, x, y, s, col, t, ph, mood)


def s_table(c, x):
    t, L = x.t, x.L
    hud(c, t)
    headline(c, t, 'THE KITCHEN TABLE: ONE HOUSEHOLD, $50,000')
    # table + two people + a laptop
    c.rrect(120, 470, 1160, 500, 10, (120, 82, 52))
    c.rrect(160, 500, 190, 600, 4, (90, 60, 40))
    c.rrect(1090, 500, 1120, 600, 4, (90, 60, 40))
    mood = 'happy' if t < beat(L, 2, 0.0) else ('thinking' if t < beat(L, 4, 0.0) else 'happy')
    person_at(c, 240, 470, 2.1, (104, 150, 214), t, 0.0, mood)
    person_at(c, 1040, 470, 2.1, (206, 120, 168), t, 1.7, mood)
    c.text(240, 178, 'Jordan, 32', 22, WHITE, 800, a=fade(t, L[0] + 0.5))
    c.text(1040, 178, 'Priya, 32', 22, WHITE, 800, a=fade(t, L[0] + 0.5))
    k = spring(t - L[0] - 0.4, 12)
    c.rrect(380, 120, 900, 460, 18, (30, 30, 36), (90, 92, 104), 3, a=k)
    c.rrect(396, 136, 884, 444, 10, (12, 12, 16), a=k)
    c.text(640, 170, 'OUR 401(k): S&P 500 INDEX FUND (example)', 18, SLATE_L, 800, a=k, shadow=False)
    c.text(640, 225, f'${HH:,}', 60, WHITE, 400, a=k, family='Anton')
    rows = [(1, 'Nvidia (6.05%)', f'${HH_NV:,.0f}', NV_L), (1, f'Top 10 holdings ({TOP10:.2f}%)', f'${HH_TOP:,.0f}', GOLD),
            (2, f'Oct 6 to Nov 25 (-{SP_DROP:.1f}%), on paper', f'-${HH_DROP:,.0f}', RED),
            (3, f'${MONTHLY} a month now buys', f'+{SH_MORE:.0f}% shares', NV_L)]
    for j, (li, lab, val, col) in enumerate(rows):
        at = beat(L, li, 0.3 + (1.8 if j == 1 else 0))
        kk = spring(t - at, 16)
        if kk <= 0:
            continue
        y = 290 + j * 40
        c.text(420, y, lab, 19, WHITE, 800, anchor='lm', a=kk, shadow=False)
        c.text(860, y, val, 22, col, 900, anchor='rm', a=kk, shadow=False)
    if len(L) > 4 and t > L[4]:
        k2 = pop(t, L[4] + 0.3)
        c.rrect(400, 478, 880, 590, 20, GOLD, a=clamp(k2))
        c.text(640, 510, 'THE REAL QUESTION', 22, INK, 900, a=clamp(k2), shadow=False)
        c.text(640, 556, 'when do we need this money?', 26, INK, 900, a=clamp(k2), shadow=False)
    c.text(640, 600, 'made-up example household; real prices and weights', 15, SLATE_L, 700, a=fade(t, 1) * (1 - fade(t, beat(L, 4, 0.0))), shadow=False)


def s_recap(c, x):
    t, L = x.t, x.L
    hud(c, t)
    headline(c, t, 'RECAP')
    pts = [(f'${NV_W:.2f} of every $100 in an S&P 500 fund is Nvidia', NV_L),
           (f'Nvidia: -{NV_DROP:.1f}% from Oct 6; one day +{NV_BOUNCE:.1f}%', RED),
           (f'Top 10 holdings: ${TOP10:.0f} of every $100', GOLD),
           (f'{N_DONE} drops of 10%+ since 1950; median {MED_MO:.0f} months back', WHITE)]
    step = max(1.8, (beat(L, 1, 0.0) - L[0] - 0.6) / len(pts)) if len(L) > 1 else 2.2
    for i, (p, col) in enumerate(pts):
        k = spring(t - L[0] - 0.4 - step * i, 14)
        if k <= 0:
            continue
        y = 140 + i * 72
        coin(c, 175, y, 15, None if i == 0 else SLATE_L, k, glyph=False)
        c.text(205 + 30 * (1 - k), y, p, 27, col, 800, anchor='lm', a=k)
    if len(L) > 1 and t > L[1]:
        k = pop(t, L[1] + 0.3)
        c.rrect(300, 440, 980, 560, 26, (12, 12, 16, 240), NV, 4, a=clamp(k))
        c.text(640, 478, 'Did you know you owned Nvidia?', 28, WHITE, 900, a=clamp(k))
        c.text(640, 525, 'comment  YES  or  NO', 30, NV_L, 400, a=clamp(k), family='Anton')
    if len(L) > 2 and t > L[2]:
        c.text(640, 590, 'Education only, not financial advice', 18, SLATE_L, 700, a=fade(t, L[2]), shadow=False)


# --------------------------------------------------------------- script ----
SCENES = [
    dict(draw=s_hook, chapter='You own Nvidia', lead=0.1, gap=0.25, cam=(1.0, 1.03), lines=[
        "!You already own Nvidia.",
        "If you have a {401(k)|four-oh-one-k} with an {S&P|S and P} 500 index fund, about 6 dollars of every 100 "
        "sits in this one chip company.",
        f"!And since October 6th, Nvidia's stock has crashed {NV_DROP:.1f}%. On one day last week it was down "
        "almost half.",
        "Then it did something even stranger. Hold that thought.",
        "Explained simply, by the end you'll know how much of your retirement money rides on AI, what this crash "
        f"cost every 100 dollars you own, and what {N_DONE} past drops say about getting back.",
    ], punch=lambda L: [L[0] + 0.55, L[2] + 0.4],
        sfx=lambda L: [(L[0] + 0.05, 'hit'), (L[0] + 0.55, 'hit'), (L[1] + 0.1, 'whoosh'), (L[1] + 2.1, 'ding'),
                       (L[2] + 0.4, 'hit'), (L[2] + 3.6, 'pop'), (L[3] + 0.2, 'riser'), (L[4] + 0.2, 'whoosh'),
                       (L[4] + 1.2, 'pop'), (L[4] + 2.5, 'pop'), (L[4] + 3.8, 'pop')]),
    dict(draw=s_quake, chapter='The crash on a seismograph', lines=[
        "Picture a seismograph, the machine that records earthquakes. Except this needle isn't measuring the ground. "
        "It's drawing Nvidia's share price, day by day, for the past year.",
        f"For most of that year, pressure built. The price climbed from about {NV_YEAR_AGO:.0f} dollars a year ago to "
        f"a peak of ${NV_PEAK:.2f} on October 6th.",
        f"Then the fault slipped. Seven weeks later, on Wednesday, November 25th, it closed at ${NV_NOW:.2f}. That's "
        f"{NV_DROP:.1f}% below the peak.",
        f"!Put simply: a share that cost 100 dollars at the top was worth about ${100 - NV_DROP:.2f} on Wednesday.",
    ], punch=lambda L: [L[2] + 2.6, L[3] + 0.3],
        sfx=lambda L: [(L[0] + 0.3, 'whoosh'), (L[1] + 0.6, 'ding'), (L[2] + 0.1, 'riser'), (L[2] + 2.6, 'hit'),
                       (L[3] + 0.2, 'pop')]),
    dict(draw=s_after, chapter='+31% in one day?', lines=[
        "Now the strange part I promised. Earthquakes have aftershocks, and so did this one. Each bar is one trading "
        "day: green is up, red is down.",
        f"On Friday, November 20th, Nvidia closed at ${NV_LOW:.2f}. That's {NV_LOW_DD:.1f}% below its peak. Almost "
        "half its value, gone in about six weeks.",
        f"!The very next trading day, Monday, it jumped {NV_BOUNCE:.1f}%, to ${NV_JUMP:.2f}. For one of the biggest "
        "companies in the world, that's an enormous single-day move.",
        f"And then it slid again, two days in a row, back to ${NV_NOW:.2f}.",
        "Wednesday was jumpy for everybody. According to an AP news report, the {S&P|S and P} 500 fell as much as "
        "3.2% during the day, and the Nasdaq 4.6%, before both closed only slightly lower.",
        "Swings like this tell you one thing: investors are very unsure what AI companies are worth right now. But "
        "why should you care, if you never bought a single share?",
    ], punch=lambda L: [L[2] + 0.3],
        sfx=lambda L: [(L[0] + 0.4 + 0.35 * i, 'tick') for i in range(12)] + [
            (L[1] + 0.3, 'down'), (L[2] + 0.3, 'hit'), (L[3] + 0.3, 'down'), (L[4] + 0.3, 'whoosh'),
            (L[5] + 0.2, 'hit'), (L[5] + 1.6, 'hit')]),
    dict(draw=s_comeback, chapter='Why +31% fixed nothing', lines=[
        "Wait. Before we answer that, there's a trap hidden in those numbers. A 31.5% jump sounds like Nvidia got "
        "its money back. It didn't.",
        f"Even after the jump, at ${NV_JUMP:.2f}, the stock was still {GAP_AFTER_JUMP:.0f}% below its October peak. "
        f"And at Wednesday's close it was even {-NV_YEAR:.0f}% lower than a year ago.",
        f"!That's the comeback math. When something falls {NV_DROP:.1f}%, it has to rise {NEED:.1f}% just to get "
        "back to where it was. Lose half, and you need to double.",
        f"Your index fund runs on the same math, only gentler. After an {SP_DROP:.1f}% drop, it needs about "
        f"{SP_NEED:.1f}% to get back. That's not a prediction. It's just how percentages work.",
    ], punch=lambda L: [L[2] + 0.3],
        sfx=lambda L: [(L[0] + 0.3 + 0.6 * i, 'pop') for i in range(4)] + [
            (L[1] + 0.3, 'down'), (L[2] + 0.2, 'riser'), (L[2] + 0.6, 'hit'), (L[2] + 4.5, 'pop'), (L[3] + 0.3, 'ding')]),
    dict(draw=s_coins, chapter="What's inside your $100", lines=[
        "Here's why. Say you have 100 dollars in an {S&P|S and P} 500 index fund. An index fund buys a small piece "
        "of every company on a list, all at once. This list is about 500 of America's biggest companies.",
        f"One of the biggest funds that tracks it, State Street's {{SPY|S P Y}}, held {N_HOLD} holdings as of November 24th. But it "
        "doesn't split your money evenly. Bigger companies get bigger slices.",
        f"So let's turn your 100 dollars into 100 coins. Apple gets about 8 of them. Then Nvidia, the green coins: "
        f"${NV_W:.2f}. Microsoft, almost 6.",
        "Then Amazon. Alphabet, Google's parent company, which counts twice because it has two kinds of shares. "
        "Broadcom, another chip maker. Meta. Eli Lilly, the drug company. And Tesla.",
        f"!Add them up: the 10 biggest holdings, just 9 companies, hold about ${TOP10:.0f} of every 100 dollars. The "
        f"other {N_HOLD - 10} share the rest. If that surprised you, subscribe. We turn the money headlines into "
        "your money, every day.",
    ], punch=lambda L: [L[4] + 0.3],
        sfx=lambda L: [(L[0] + 0.6 + 0.2 * i, 'tick') for i in range(10)] + [
            (L[1] + 0.4, 'pop'), (L[2] + 0.2, 'pop'), (L[2] + 1.1, 'ding'), (L[2] + 2.0, 'pop'), (L[3] + 0.3, 'pop'),
            (L[3] + 1.0, 'pop'), (L[3] + 1.6, 'pop'), (L[4] + 0.3, 'hit')]),
    dict(draw=s_aislice, chapter='Your hidden AI slice', lines=[
        "Now look at those 9 companies again, but through an AI lens. Which of them live or die by the AI boom?",
        "Nvidia and Broadcom make the chips that power AI. Microsoft, Amazon and Alphabet rent out AI computing "
        "power through their cloud businesses. And Meta is building AI into the social apps on your "
        "phone.",
        f"!Together, those 6 companies are about ${AI_W:.0f} of every 100 dollars in an {{S&P|S and P}} 500 fund. "
        "So when investors sour on AI, it isn't one stock in your {401(k)|four-oh-one-k} that feels it. It's about a quarter of "
        "your fund, all at the same time.",
    ], punch=lambda L: [L[2] + 0.3],
        sfx=lambda L: [(L[0] + 0.2, 'whoosh'), (L[1] + 0.3, 'pop'), (L[1] + 3.6, 'pop'), (L[1] + 8.2, 'pop'),
                       (L[2] + 0.3, 'hit')]),
    dict(draw=s_follow, chapter='Follow your paycheck', lines=[
        "Now follow one dollar from your paycheck. It comes out of your pay before taxes and lands in your "
        "{401(k)|four-oh-one-k}.",
        "From there it goes into whatever fund you picked, or the one your plan picked for you. Many plans start "
        "people in a target-date fund, a mix that shifts with the year you plan to retire, and those usually "
        "hold big stock index funds inside.",
        f"!Inside the index fund, your dollar is cut into hundreds of slices. About {NV_W:.0f} cents of it becomes "
        "Nvidia stock.",
        "Here's the part almost nobody notices. The fund sizes each slice by the company's total stock market value. "
        "When a company's price soars, its slice of your dollar grows by itself. Nobody calls to ask you. That's "
        "how a chip maker became the second-biggest piece of your fund, right behind Apple.",
    ], punch=lambda L: [L[2] + 0.3],
        sfx=lambda L: [(L[0] + 0.3, 'whoosh'), (L[0] + 4.2, 'whoosh'), (L[1] + 0.3, 'whoosh'), (L[2] + 0.3, 'hit'),
                       (L[3] + 0.3, 'ding')]),
    dict(draw=s_cost, chapter='What it cost your $100', lines=[
        f"So what did the crash cost you? Let's use today's slices. Your ${NV_W:.2f} of Nvidia, times a "
        f"{NV_DROP:.1f}% drop, comes to about ${NV_COST:.2f} out of every 100 dollars.",
        "And that's the low estimate. Back in October, Nvidia's price was higher, so its slice of your fund was even "
        "bigger.",
        f"Now the whole fund. From its record close on October 6th to Wednesday, the {{S&P|S and P}} 500 fell "
        f"{SP_DROP:.1f}%. So 100 dollars became about ${FUND_100:.2f}.",
        f"!Which means more than a quarter of that whole drop came from one single company. That's what "
        "concentration feels like, even inside a fund built to spread your money around.",
    ], punch=lambda L: [L[3] + 0.3],
        sfx=lambda L: [(L[0] + 0.3, 'pop'), (L[0] + 3.0, 'down'), (L[1] + 0.3, 'pop'), (L[2] + 0.2, 'whoosh'),
                       (L[2] + 0.8, 'tick'), (L[3] + 0.3, 'hit')]),
    dict(draw=s_bubble, chapter='Is the AI bubble bursting?', lines=[
        "So is this the AI bubble bursting? First, what's a bubble? It's when prices race far ahead of what "
        "businesses actually earn, until they pop.",
        f"Here's what we can measure. Nvidia: down {NV_DROP:.1f}% from its October high. The Nasdaq-100, an index "
        f"packed with tech companies: down {NDX_DROP:.1f}%. The {{S&P|S and P}} 500: down {SP_DROP:.1f}%.",
        f"The more tech and AI a fund holds, the harder it fell. On November 20th, the Nasdaq-100 closed "
        f"{NDX_LOW_DD:.1f}% below its peak.",
        "So is it a bubble popping, or a hard shakeout before more growth? Honestly, nobody knows yet, and anyone who "
        "tells you they're sure is guessing. What we do have is history.",
    ], sfx=lambda L: [(L[0] + 0.2, 'pop'), (L[1] + 0.4, 'down'), (L[1] + 2.0, 'down'), (L[1] + 3.6, 'down'),
                      (L[2] + 0.4, 'ding'), (L[3] + 0.2, 'hit'), (L[3] + 2.0, 'hit')]),
    dict(draw=s_history, chapter=f'{N_DONE} drops since 1950', lines=[
        f"How long do drops like this usually last? Since 1950, the {{S&P|S and P}} 500 has fallen 10% or more from "
        f"a record high {N_DONE} times before this one. Watch them land. The deeper the bar, the deeper the fall.",
        f"Some healed fast. In 1955, the index was back at its old high in under 2 months. After the pandemic crash "
        f"of 2020, about {E2020['mo']:.0f} months.",
        f"!The middle case, the median, took about {MED_MO:.0f} months to climb back to the old high.",
        f"For the drops that stopped short of 20%, the median was about {MED_SMALL:.0f} months. These are prices "
        "only, before dividends, and the past doesn't promise anything about this time.",
        f"And this one? At its lowest close, on November 20th, the {{S&P|S and P}} 500 was down "
        f"{-NOW_EV['low'] * 100:.1f}%. Number {len(EVENTS)} on the list.",
    ], punch=lambda L: [L[2] + 0.3],
        sfx=lambda L: [(L[0] + 0.8 + 0.3 * i, 'tick') for i in range(24)] + [
            (L[1] + 0.3, 'pop'), (L[1] + 2.6, 'pop'), (L[2] + 0.3, 'hit'), (L[3] + 0.3, 'ding'), (L[4] + 0.3, 'pop')]),
    dict(draw=s_2000, chapter='When it took 7 years', lines=[
        f"But here's the warning label. The {len(SLOW)} slowest comebacks since 1950 all took more than 5 years: after "
        f"{', '.join(e['peak'][:4] for e in SLOW[:-1])} and {SLOW[-1]['peak'][:4]}. The year 2000 is the one that "
        "started with a tech boom. This is the {{S&P|S and P}} 500 from 1996 to 2009.",
        f"From its record in March 2000, it fell {-E2000['low'] * 100:.0f}%.",
        f"!And it didn't get back to that old high for about {E2000['mo'] / 12:.0f} years, until May 2007.",
        "If you were 60 and needed that money soon, that was brutal.",
        "If you were 30, with decades to go and still adding money from every paycheck, your new money was buying "
        "at lower prices for years. Same crash, very different story. The difference was time.",
    ], punch=lambda L: [L[1] + 0.3, L[2] + 0.4],
        sfx=lambda L: [(L[0] + 0.4, 'whoosh'), (L[0] + 2.4, 'pop'), (L[1] + 0.3, 'hit'), (L[2] + 0.4, 'ding'),
                       (L[3] + 0.2, 'down'), (L[4] + 0.2, 'pop')]),
    dict(draw=s_shares, chapter='The paycheck math', lines=[
        "That leads to one piece of math most people miss. If you add money from every paycheck, a lower price "
        "means each dollar buys more.",
        f"On October 6th, at the top, 500 dollars bought {SH_PEAK:.3f} shares of that State Street {{SPY|S P Y}} fund. On "
        f"Wednesday, the same 500 dollars bought {SH_NOW:.3f} shares.",
        f"That's about {SH_MORE:.0f}% more shares for the same money.",
        "It doesn't make a drop painless, and prices can keep falling after you buy. It's simply how regular "
        "contributions work.",
    ], sfx=lambda L: [(L[0] + 0.3, 'pop'), (L[1] + 0.3, 'pop'), (L[1] + 3.5, 'pop'), (L[2] + 0.3, 'ding'),
                      (L[3] + 0.3, 'pop')]),
    dict(draw=s_check, chapter='3 things to check tonight', lines=[
        "So what can you actually look at, without buying or selling anything? Three things.",
        "One: the name of your fund. Its website lists its top 10 holdings, so you can see your own Nvidia slice "
        "in about a minute.",
        "Two: overlap. If you hold an {S&P|S and P} 500 fund and a tech fund, you might own Nvidia twice, and not "
        "know it.",
        "Three: your timeline. Money you need in 2 years and money you need in 30 years are different stories. For "
        "your own situation, a licensed financial professional can help.",
    ], sfx=lambda L: [(L[1] + 0.3, 'pop'), (L[2] + 0.3, 'pop'), (L[3] + 0.3, 'pop')]),
    dict(draw=s_table, chapter='The kitchen table', lines=[
        "Let's bring it to a kitchen table. Meet an example couple, Jordan and Priya, both 32. They have 50,000 "
        "dollars in a {401(k)|four-oh-one-k}, all in an {S&P|S and P} 500 index fund.",
        f"At today's slices, ${HH_NV:,.0f} of their money is Nvidia, and ${HH_TOP:,.0f} sits in the top 10 holdings.",
        f"If that 50,000 was in the fund at the October record, the {SP_DROP:.1f}% drop took about "
        f"${HH_DROP:,.0f} off their statement. On paper. They haven't sold anything.",
        f"Their 500 dollars a month keeps going in. About ${HH_NV_MONTH:.0f} of it goes to Nvidia automatically, and "
        f"right now each payment buys about {SH_MORE:.0f}% more shares than it did in October.",
        "So their real question isn't what Nvidia does tomorrow. It's when they'll need this money. For them, "
        "that's decades away.",
    ], sfx=lambda L: [(L[0] + 0.4, 'whoosh'), (L[1] + 0.3, 'pop'), (L[1] + 2.1, 'pop'), (L[2] + 0.3, 'down'),
                      (L[3] + 0.3, 'pop'), (L[4] + 0.3, 'ding')]),
    dict(draw=s_recap, chapter='Recap', tail=1.4, lines=[
        f"Quick recap. About {NV_W:.0f} dollars of every 100 in an {{S&P|S and P}} 500 fund is Nvidia. Nvidia fell "
        f"{NV_DROP:.1f}% from its October high, with one wild day of plus {NV_BOUNCE:.0f}%. The top 10 holdings are "
        f"about {TOP10:.0f} dollars of every 100. And since 1950, drops like this took about {MED_MO:.0f} months to "
        "heal, in the middle case.",
        "!So, one word in the comments: did you know you owned Nvidia? Yes, or no? And subscribe for tomorrow's "
        "video.",
        "One last thing: everything here is education only, not financial advice. Enjoy the long weekend.",
    ], punch=lambda L: [L[1] + 0.3],
        sfx=lambda L: [(L[0] + 0.4 + 2.5 * j, 'pop') for j in range(4)] + [(L[1] + 0.3, 'ding')]),
]
SHORTS = {}


def check_numbers():
    script = ' '.join(l for sc in SCENES for l in sc['lines'])
    words = len(script.split())
    assert LAST_D == '2026-11-25' and max(NV_SER, key=lambda p: p[1])[0] == PEAK_D
    assert (NV_PEAK, NV_NOW, round(NV_DROP, 1)) == (239.24, 149.30, 37.6), NV_DROP
    assert (NV_LOW, NV_JUMP, round(NV_BOUNCE, 1), round(NV_LOW_DD, 1)) == (125.53, 165.05, 31.5, 47.5)
    assert min(NV_SER[-60:], key=lambda p: p[1])[0] == NV_LOW_D
    assert [d for d, _ in NV_SER].index('2026-11-23') == [d for d, _ in NV_SER].index(NV_LOW_D) + 1  # next trading day
    assert CL['nvda']['2026-11-24'] < NV_JUMP and NV_NOW < CL['nvda']['2026-11-24']  # slid two days in a row
    assert round(NV_YEAR_AGO) == 180 and NV_SER[0][0] == '2025-11-26'
    assert (SP_PEAK, SP_NOW, round(SP_DROP, 1)) == (7818.93, 7182.78, 8.1)
    assert (NDX_PEAK, NDX_NOW, round(NDX_DROP, 1), round(NDX_LOW_DD, 1)) == (31224.47, 26046.90, 16.6, 19.8)
    assert max(D['closes']['ndx'], key=lambda p: p[1])[0] == PEAK_D
    assert 'As of 24-Nov-2026' in D['spy_asof'] and N_HOLD == 505
    assert [h['ticker'] for h in HOLD] == ['AAPL', 'NVDA', 'MSFT', 'AMZN', 'GOOGL', 'AVGO', 'GOOG', 'META', 'LLY', 'TSLA']
    assert round(NV_W, 2) == 6.05 and round(TOP10, 2) == 36.96 and round(W_['AAPL'], 2) == 8.31
    assert round(W_['MSFT'], 2) == 5.92 and sum(COUNTS) == 37 and COUNTS[:3] == [8, 6, 6]
    assert sorted(HOLD, key=lambda h: -h['weight'])[1]['ticker'] == 'NVDA'  # second-biggest, behind Apple
    assert round(NV_COST, 2) == 2.27 and round(FUND_100, 2) == 91.86 and NV_SHARE_OF_DROP > 25
    assert round(100 - NV_DROP, 2) == 62.41
    assert round(HH_NV) == 3023 and round(HH_TOP) == 18479 and round(HH_DROP) == 4068
    assert (SPY_PEAK, SPY_NOW, round(SH_PEAK, 3), round(SH_NOW, 3), round(SH_MORE)) == (779.09, 716.70, 0.642, 0.698, 9)
    # history: S&P 500 declines of 10%+ from a record since 1950 (price only)
    assert SPX_ROWS[-1][0] == '2026-11-20' and N_DONE == 24 and len(EVENTS) == 25 and NOW_EV['rec'] is None
    assert NOW_EV['peak'] == PEAK_D and round(-NOW_EV['low'] * 100, 1) == round(SP_LOW_DD, 1) == 11.6
    assert round(MED_MO) == 14 and round(MED_SMALL) == 7 and len(SMALL) == 13
    assert E1955['mo'] < 2 and round(E2020['mo']) == 6 and E2000['peak'] == '2000-03-24'
    assert [e['peak'][:4] for e in SLOW] == ['1973', '2000', '2007'] and round(AI_W, 2) == 25.09
    assert round(GAP_AFTER_JUMP) == 31 and round(NEED, 1) == 60.2 and round(SP_NEED, 1) == 8.9 and round(NV_YEAR) == -17
    assert round(HH_NV_MONTH) == 30
    assert round(-E2000['low'] * 100) == 49 and E2000['rec'][:7] == '2007-05' and round(E2000['mo'] / 12) == 7
    for s in ('not financial advice', 'AP news report', 'State Street', 'prices only, before dividends',
              'November 24th', '10 biggest holdings, just 9 companies'):
        assert s in script, s
    assert script.count('not financial advice') == 1
    for banned in ('bear market', 'Huang', 'billion', 'rate hike'):
        assert banned not in script, banned
    print(f'numbers check: OK  ({words} words)  NVDA {NV_PEAK}->{NV_NOW} -{NV_DROP:.2f}%  low {NV_LOW} (-{NV_LOW_DD:.1f}%) '
          f'bounce +{NV_BOUNCE:.2f}%  S&P -{SP_DROP:.2f}% NDX -{NDX_DROP:.2f}%  NV weight {NV_W:.3f}% top10 {TOP10:.2f}% '
          f'cost ${NV_COST:.2f} ({NV_SHARE_OF_DROP:.0f}% of drop)  history {N_DONE} done, median {MED_MO:.1f} mo, '
          f'<20% median {MED_SMALL:.1f} mo, 2000: {E2000["mo"]:.0f} mo')


def plan_report():
    plan, _ = narrate(SCENES, BUILD)
    clock, rows = 0.0, []
    for i, (dur, *_r) in enumerate(plan):
        rows.append((clock, dur, SCENES[i].get('chapter', '')))
        clock += dur - (0.4 if i < len(plan) - 1 else 0)
    for at, dur, ch in rows:
        print(f'  {fmt_time(at):>6}  {dur:6.1f}s  {ch}')
    print(f'TOTAL {clock:.1f}s = {clock / 60:.2f} min')
    json.dump([(p[0], p[1], p[2]) for p in plan], open(os.path.join(BUILD, 'plan.json'), 'w'))
    return plan


def stills(per_scene=4):
    """Contact sheet with real narration timings: per scene, frames at the end of each line (+ hook every 1 s)."""
    from PIL import Image
    pj = os.path.join(BUILD, 'plan.json')
    plan = json.load(open(pj)) if os.path.exists(pj) else None
    folder = os.path.join(BUILD, 'stills')
    os.makedirs(folder, exist_ok=True)
    tiles = []
    for i, sc in enumerate(SCENES):
        if plan:
            dur, starts, ends = plan[i]
        else:
            starts = [0.5 + 4 * j for j in range(len(sc['lines']))]
            ends = [s + 3.6 for s in starts]
            dur = ends[-1] + 1
        ts = [min(dur - 0.05, e - 0.1) for e in ends]
        if i == 0:
            ts = sorted(set([round(k * 1.0, 1) for k in range(1, int(min(dur, 26)) + 1)] + ts))
        for tt in ts:
            img = compose(dict(sc, captions=False), tt, starts, ends, dur, None, [], 'long')
            img = img.resize((480, 270))
            tiles.append((i, tt, img))
    cols = 6
    rows_ = (len(tiles) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * 484, rows_ * 290), (40, 40, 40))
    from PIL import ImageDraw
    d = ImageDraw.Draw(sheet)
    for j, (i, tt, img) in enumerate(tiles):
        x, y = (j % cols) * 484, (j // cols) * 290
        sheet.paste(img, (x + 2, y + 2))
        d.text((x + 6, y + 274), f's{i} t={tt:.1f}', fill=(255, 255, 0))
    path = os.path.join(folder, 'sheet.jpg')
    sheet.save(path, quality=85)
    for j, (i, tt, img) in enumerate(tiles):
        pass
    print('contact sheet', path, len(tiles), 'tiles')


if __name__ == '__main__':
    check_numbers()
    os.makedirs(BUILD, exist_ok=True)
    if '--check' in sys.argv:
        sys.exit()
    if '--plan' in sys.argv:
        plan_report()
        sys.exit()
    if '--stills' in sys.argv:
        stills()
        sys.exit()
    only = [int(a) for a in sys.argv[sys.argv.index('--only') + 1].split(',')] if '--only' in sys.argv else None
    out_mp4 = os.environ.get('EP_OUT', os.path.join(OUT, f'{SLUG}.mp4'))
    total, chapters = build(SCENES, out_mp4, BUILD, only=only, srt_path=os.path.join(OUT, f'{SLUG}.en.srt'))
    with open(os.path.join(OUT, 'ep14_chapters.txt'), 'w') as f:
        for at, name in chapters:
            f.write(f'{fmt_time(at)} {name}\n')
    print(f'total {total / 60:.2f} min')
