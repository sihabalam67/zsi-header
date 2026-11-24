"""Episode 13: Your groceries cost 32% more. Why? (long video, Tue Nov 24 2026, Thanksgiving week)

What this video does better than the last ones (from channel/LEARNINGS.md and youtube/learn.py):
1. An everyday topic every viewer pays for (groceries, Thanksgiving dinner), framed around "your" money, instead
   of investor jargon. The topic scout measured ~19k views/day for grocery prices, with small channels winning.
2. The hook: the surprising number in sentence 1, a bright photo behind it, and a new price popping on screen every
   2-3 s for the first 15 s; an open loop ("one item more than doubled") paid off in minute 3.
3. Bright photo-real thumbnail (grocery cart) with 2 words + one number; title 34 characters.

    python3 channel/ep13_groceries.py [--check] [--stills] [--only 3,5]

Data (check_numbers recomputes everything from the files):
- FRED / BLS CPI: CUSR0000SAF11 (food at home, seasonally adjusted), CPIAUCSL (all items), CES0500000003 (average
  hourly earnings, private), BLS average prices APU0000708111 (eggs, grade A large, dozen), APU0000703112 (ground
  beef, lb), APU0000717311 (coffee, ground roast, lb), APU0000702111 (white bread, lb), APU0000709112 (whole milk,
  gallon), APU0000711211 (bananas, lb). All through October 2026.
- American Farm Bureau Federation, 41st annual Thanksgiving dinner cost survey, news release Nov 18 2026:
  classic dinner for 10 $58.63 (more than 6% above 2025, $5.42 or 8.5% below the 2022 record of $64.05); 16-lb
  turkey $23.68, up 10.1%; item list and regional averages as in ITEMS / REGIONS below; reasons: diesel, farm
  labor, processing/packaging/transport; USDA: under 6 cents of each retail food dollar goes to the farm.
Photos: Canva AI images (no people, no logos), assets/thumbsrc/ep13_cart.jpg and ep13_dinner.jpg.
"""
import math
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
BUILD = os.path.join(HERE, 'build', 'ep13_groceries')
CART = os.path.join(HERE, 'assets', 'thumbsrc', 'ep13_cart.jpg')
DINNER = os.path.join(HERE, 'assets', 'thumbsrc', 'ep13_dinner.jpg')
FULL = (0, 0, W, H)

BASE = '2020-01-01'
FOOD, ALL, PAY = series('CUSR0000SAF11'), series('CPIAUCSL'), series('CES0500000003')
LAST = FOOD.index[-1]


def since(s, start=BASE):
    return (s.iloc[-1] / s[:start].iloc[-1] - 1) * 100


FOOD_UP, ALL_UP, PAY_UP = since(FOOD), since(ALL), since(PAY)
PAY_NOW = PAY.iloc[-1]
FOOD_MOM = (FOOD.iloc[-1] / FOOD.iloc[-2] - 1) * 100
_prev = FOOD.pct_change()[:-1]
FOOD_MOM_SINCE = _prev[_prev >= FOOD_MOM / 100].index[-1] if (_prev >= FOOD_MOM / 100).any() else None

ITEM_IDS = [('Coffee', 'APU0000717311', 'lb'), ('Ground beef', 'APU0000703112', 'lb'),
            ('Eggs', 'APU0000708111', 'dozen'), ('White bread', 'APU0000702111', 'lb'),
            ('Whole milk', 'APU0000709112', 'gallon'), ('Bananas', 'APU0000711211', 'lb')]
PRICES = {}
for name, sid, unit in ITEM_IDS:
    s = series(sid)
    PRICES[name] = dict(then=s[:BASE].iloc[-1], now=s.iloc[-1], up=since(s), unit=unit, peak=s.max(), peak_d=s.idxmax(),
                        s=s)
EGG = PRICES['Eggs']

# American Farm Bureau Federation, Nov 18 2026 (2026 price, % change vs 2025)
DINNER_TOTAL, DINNER_REC = 58.63, 64.05
ITEMS = [('16-lb turkey', 23.68, 10.1), ('Pumpkin pie mix', 4.24, 1.9), ('Sweet potatoes, 3 lb', 4.20, 5.0),
         ('Whole milk, 1 gal', 4.05, 8.6), ('Stuffing mix', 3.91, 5.4), ('Misc. ingredients', 3.84, 6.4),
         ('Dinner rolls, 1 doz', 3.81, 7.0), ('Pie crusts', 3.28, -2.7), ('Cranberries, 12 oz', 2.48, 8.8),
         ('Frozen peas, 1 lb', 1.99, -2.0), ('Whipping cream', 1.84, -1.6), ('Veggie tray', 1.31, -3.7)]
REGIONS = [('South', 54.33), ('Midwest', 56.89), ('West', 58.74), ('Northeast', 61.57)]
EATOUT_UP = since(series('CUSR0000SEFV'))
BILLS = [('Gas (regular, weekly)', since(series('GASREGW'), '2020-01-31')), ('Electricity', since(series('CUSR0000SEHF01'))),
         ('Eating out', EATOUT_UP), ('Rent', since(series('CUSR0000SEHA'))), ('Groceries', FOOD_UP),
         ('Used cars', since(series('CUSR0000SETA02')))]
HOURS = DINNER_TOTAL / PAY_NOW
PAY_2020 = PAY[:BASE].iloc[-1]
CARD = series('TERMCBCCINTNS')
CARD_NOW, CARD_D, CARD_2020 = CARD.iloc[-1], CARD.index[-1], CARD[:'2020-02-01'].iloc[-1]
CARD_COST = 500 * ((1 + CARD_NOW / 1200) ** 12 - 1)
WEEK = 150  # an example weekly grocery bill in January 2020, for the arithmetic only
SRC_BLS = 'BLS via FRED: CPI food at home (CUSR0000SAF11), average prices'
SRC_AFBF = 'American Farm Bureau Federation Thanksgiving survey, Nov 18, 2026'
TICK = (f'GROCERIES SINCE JAN 2020: +{FOOD_UP:.1f}%     COFFEE +{PRICES["Coffee"]["up"]:.0f}%     GROUND BEEF '
        f'+{PRICES["Ground beef"]["up"]:.0f}%     EGGS +{EGG["up"]:.0f}%     THANKSGIVING DINNER FOR 10: '
        f'${DINNER_TOTAL:.2f}     PAY +{PAY_UP:.1f}%     ')


def ticker(draw):
    def wrapped(c, x):
        draw(c, x)
        c.rrect(0, 0, W, 40, 0, (8, 10, 20, 210))
        w = len(TICK) * 15 * 0.62
        off = (x.t * 45) % w
        for k in range(3):
            c.text(-off + k * w, 28, TICK, 15, GOLD, 800, anchor='lm', shadow=False)
    return wrapped


def tag(c, x, y, text, col, k, size=34):
    """A price tag sticker that pops in."""
    if k <= 0:
        return
    s = 0.6 + 0.4 * clamp(k)
    w = len(text) * size * 0.62 * s + 40
    c.rrect(x - w / 2, y - size * s, x + w / 2, y + size * s, 14, col, WHITE, 4, a=clamp(k))
    c.text(x, y, text, int(size * s), INK, 900, a=clamp(k), shadow=False)


# ------------------------------------------------------------------- scenes --
def s_hook(c, x):
    t, L = x.t, x.L
    img = CART if t < L[1] else DINNER
    fx.photo(c, img, 1.1 - 0.05 * clamp(t / 15), (0.5, 0.5), box=FULL, dark=0.45, sat=1.2)
    c.rrect(0, 0, W, H, 0, (8, 10, 20, 90))
    k = pop(t, L[0] + 0.1, 0.3)
    if k > 0 and t < L[1]:
        c.text(640, 250, f'+{FOOD_UP:.0f}%', int(180 * (0.6 + 0.4 * clamp(k))), GOLD, 900, a=clamp(k), stroke=9)
        c.text(640, 365, 'YOUR GROCERIES SINCE 2020', 40, WHITE, 900, a=clamp(k), stroke=4)
        pops = [('Coffee', 220, 480), ('Ground beef', 640, 520), ('Eggs', 1060, 480)]
        for i, (n, px_, py_) in enumerate(pops):
            p = PRICES[n]
            tag(c, px_, py_, f"{n} +{p['up']:.0f}%", CORAL if i != 2 else GOLD, pop(t, L[0] + 2.2 + 2.0 * i), 26)
    if t > L[1]:
        kk = pop(t, L[1] + 0.2, 0.3)
        c.text(640, 230, f'${DINNER_TOTAL:.2f}', int(150 * (0.6 + 0.4 * clamp(kk))), GOLD, 900, a=clamp(kk), stroke=8)
        c.text(640, 330, 'THANKSGIVING DINNER FOR 10', 38, WHITE, 900, a=clamp(kk), stroke=4)
        if t > L[1] + 2.8:
            tag(c, 640, 440, 'turkey +10%', CORAL, pop(t, L[1] + 2.8), 30)
    if len(L) > 2 and t > L[2]:
        c.rrect(0, 0, W, H, 0, (10, 14, 26, int(235 * fade(t, L[2]))))
        kk = pop(t, L[2] + 0.3)
        c.text(640, 250, 'ONE ITEM MORE THAN DOUBLED', 50, CORAL, 900, a=clamp(kk), stroke=5)
        c.text(640, 330, 'which one? stay for minute 3', 30, WHITE, 800, a=clamp(kk))
        if len(L) > 3 and t > L[3]:
            chip(c, 640, 440, 'and whether your paycheck kept up', MINT, pop(t, L[3] + 0.3), 28)


def s_promise(c, x):
    t, L = x.t, x.L
    specks(c, t, 161)
    penny(c, 200, 520, 100, t, 'thinking', talk=x.talk())
    items = ['Your Thanksgiving receipt', 'What went up the most', 'Why food costs more', 'Did your pay keep up?']
    for i, it in enumerate(items):
        k = pop(t, L[0] + 0.5 + 1.4 * i)
        if k > 0:
            c.rrect(420, 150 + i * 105, 1120, 230 + i * 105, 22, (255, 255, 255, 22), GOLD, 3, a=clamp(k))
            c.text(460, 190 + i * 105, f'{i + 1}', 40, GOLD, 900, a=clamp(k))
            c.text(510, 190 + i * 105, it, 34, WHITE, 800, anchor='lm', a=clamp(k))


def s_receipt(c, x):
    t, L = x.t, x.L
    fx.photo(c, DINNER, 1.08, (0.5, 0.5), box=FULL, dark=0.7, sat=1.0)
    c.rrect(380, 60, 900, 690, 10, CREAM)
    c.text(640, 100, 'THANKSGIVING DINNER FOR 10', 24, INK, 900, shadow=False)
    c.text(640, 128, 'American Farm Bureau survey, 2026', 16, MUTED, 700, shadow=False)
    span = max(6.0, (L[1] - L[0] - 0.5)) if len(L) > 1 else 8.0
    for i, (n, p, ch) in enumerate(ITEMS):
        k = pop(t, L[0] + 0.5 + span * i / len(ITEMS))
        if k <= 0:
            continue
        y = 165 + i * 36
        c.text(410, y, n, 20, INK, 800, anchor='lm', a=clamp(k), shadow=False)
        c.text(760, y, f'${p:.2f}', 20, INK, 900, anchor='rm', a=clamp(k), shadow=False)
        c.text(870, y, f'{ch:+.1f}%', 18, CORAL_D if ch > 0 else MINT_D, 900, anchor='rm', a=clamp(k), shadow=False)
    if len(L) > 1 and t > L[1]:
        k = pop(t, L[1] + 0.3)
        c.line([(400, 600), (880, 600)], INK, 2, a=clamp(k))
        c.text(410, 635, 'TOTAL', 26, INK, 900, anchor='lm', a=clamp(k), shadow=False)
        c.text(870, 635, f'${DINNER_TOTAL:.2f}', 30, CORAL_D, 900, anchor='rm', a=clamp(k), shadow=False)
        pulse(c, t, (395, 610, 885, 662), CORAL, 12)
    if len(L) > 2 and t > L[2]:
        chip(c, 1090, 250, f'about ${DINNER_TOTAL / 10:.2f} a person', GOLD, pop(t, L[2] + 0.3), 22)
        chip(c, 1090, 330, f'2022 record: ${DINNER_REC:.2f}', MINT, pop(t, L[2] + 2.0), 22)
    if len(L) > 3 and t > L[3]:
        for i, (r, v) in enumerate(REGIONS):
            chip(c, 190, 220 + i * 80, f'{r}: ${v:.2f}', SKY if i < 3 else CORAL, pop(t, L[3] + 0.3 + 0.6 * i), 22)
    source(c, t, SRC_AFBF)


def s_big(c, x):
    t, L = x.t, x.L
    specks(c, t, 162)
    head(c, t, 'Grocery prices (CPI food at home), Jan 2020 = 100')
    f = FOOD['2019-01-01':] / FOOD[:BASE].iloc[-1] * 100
    xs = [d.year + (d.month - 1) / 12 for d in f.index]
    k = clamp((t - L[0] - 0.3) / 5.0) if t < L[1] else 1.0
    px, py = line_chart(c, (150, 130, 1120, 520), xs, list(f.values), (2019, 2027), (90, 140), k, GOLD,
                        xticks=range(2019, 2027), yticks=(90, 100, 110, 120, 130, 140), yfmt='{:.0f}', width=6)
    if t > L[0] + 5.3:
        c.text(px(xs[-1]) - 10, py(f.iloc[-1]) - 40, f'+{FOOD_UP:.1f}%', 46, GOLD, 900, anchor='rm',
               a=fade(t, L[0] + 5.3), stroke=4)
    if t > L[1]:
        chip(c, 640, 560, f'$100 of groceries in Jan 2020 = ${100 + FOOD_UP:.0f} today', CORAL, pop(t, L[1] + 0.3), 26)
    if len(L) > 2 and t > L[2]:
        chip(c, 640, 190, f'last month alone: +{FOOD_MOM:.1f}%', SKY, pop(t, L[2] + 0.3), 24)
    source(c, t, SRC_BLS)


def s_items(c, x):
    t, L = x.t, x.L
    specks(c, t, 163)
    head(c, t, 'Average U.S. price, January 2020 vs October 2026')
    names = ['Bananas', 'Whole milk', 'White bread', 'Eggs', 'Ground beef', 'Coffee']
    for i, n in enumerate(names):
        p = PRICES[n]
        at = L[0] + 0.4 + 1.6 * i if i < 5 else (L[1] + 0.4 if len(L) > 1 else 9)
        k = pop(t, at)
        if k <= 0:
            continue
        y = 130 + i * 78
        col = CORAL if p['up'] > 100 else (GOLD if p['up'] > 40 else SKY)
        w = min(430, p['up'] * 3.5) * ease(clamp((t - at) / 0.8))
        c.text(140, y + 25, n, 26, WHITE, 900, anchor='lm', a=clamp(k))
        c.rrect(380, y + 5, 380 + w, y + 45, 10, col)
        c.text(390 + w + 10, y + 25, f"+{p['up']:.0f}%", 28, col, 900, anchor='lm', a=clamp(k))
        c.text(1160, y + 25, f"${p['then']:.2f} -> ${p['now']:.2f} / {p['unit']}", 20, MUTED, 800, anchor='rm', a=clamp(k))
    if len(L) > 1 and t > L[1] + 1.0:
        pulse(c, t, (120, 130 + 5 * 78, 1170, 130 + 5 * 78 + 52), CORAL, 16)
    source(c, t, 'BLS average prices via FRED (APU series), U.S. city average')


def s_eatout(c, x):
    t, L = x.t, x.L
    specks(c, t, 169)
    head(c, t, 'Cooking at home vs eating out, since January 2020')
    items = [('Groceries', FOOD_UP, GOLD), ('Restaurants', EATOUT_UP, CORAL)]
    compare_bars(c, t, items, L[0] + 0.3, 3.0, 45, lambda v: f'+{v:.1f}%', box=(330, 170, 950, 520))
    if len(L) > 1 and t > L[1]:
        chip(c, 640, 120, 'eating out rose even faster', CORAL, pop(t, L[1] + 0.3), 24)
    source(c, t, 'BLS via FRED: CUSR0000SAF11, CUSR0000SEFV')


def s_chart(c, x, name, ymax, col, seed):
    t, L = x.t, x.L
    specks(c, t, seed)
    p = PRICES[name]
    head(c, t, f"{name}, average U.S. price per {p['unit']}")
    s = p['s']['2019-01-01':]
    xs = [d.year + (d.month - 1) / 12 for d in s.index]
    k = clamp((t - L[0] - 0.3) / 4.5) if t < L[1] else 1.0
    px, py = line_chart(c, (150, 130, 1120, 520), xs, list(s.values), (2019, 2027), (0, ymax), k, col,
                        xticks=range(2019, 2027), yticks=[ymax * i / 4 for i in range(5)], yfmt='${:.0f}', width=6)
    if t > L[1]:
        pk = p['peak_d']
        chip(c, px(pk.year + (pk.month - 1) / 12) - 60, py(p['peak']) - 32, f"record ${p['peak']:.2f} ({pk:%b %Y})",
             CORAL, pop(t, L[1] + 0.3), 20)
    if len(L) > 2 and t > L[2]:
        chip(c, 640, 118, f"${p['then']:.2f} in Jan 2020 -> ${p['now']:.2f} now", GOLD, pop(t, L[2] + 0.3), 24)
    source(c, t, 'BLS average prices via FRED')


def s_coffee(c, x):
    s_chart(c, x, 'Coffee', 12, CORAL, 170)


def s_beef(c, x):
    s_chart(c, x, 'Ground beef', 8, GOLD, 171)


def s_bills(c, x):
    t, L = x.t, x.L
    specks(c, t, 172)
    head(c, t, 'Since January 2020: groceries vs your other bills')
    rows = sorted(BILLS, key=lambda r: -r[1])
    for i, (n, v) in enumerate(rows):
        k = pop(t, L[0] + 0.4 + 1.2 * i)
        if k <= 0:
            continue
        y = 120 + i * 72
        col = GOLD if n == 'Groceries' else (CORAL if v > PAY_UP else SKY)
        w = v * 11 * ease(clamp((t - L[0] - 0.4 - 1.2 * i) / 0.8))
        c.text(140, y + 25, n, 24, WHITE, 900, anchor='lm', a=clamp(k))
        c.rrect(430, y + 6, 430 + w, y + 44, 10, col)
        c.text(440 + w + 10, y + 25, f'+{v:.0f}%', 26, col, 900, anchor='lm', a=clamp(k))
    if len(L) > 1 and t > L[1]:
        xx = 430 + PAY_UP * 11
        c.line([(xx, 110), (xx, 560)], MINT, 3, a=fade(t, L[1]))
        chip(c, xx, 585, f'average pay +{PAY_UP:.0f}%', MINT, pop(t, L[1] + 0.3), 22)
    source(c, t, 'BLS CPI via FRED; EIA weekly gas price (GASREGW)')


def s_why(c, x):
    t, L = x.t, x.L
    specks(c, t, 164)
    head(c, t, 'Why food costs more: farm to table')
    items = [('truck', 'Diesel for\ntrucks & tractors'), ('users', 'Farm labor\nshortage'),
             ('package', 'Processing &\npackaging'), ('store', 'Stores &\nwages')]
    icon_row(c, t, items, L[0] + 0.2, max(4.0, (L[1] - L[0]) * 0.9) if len(L) > 1 else 6, y=270, color=GOLD)
    if len(L) > 1 and t > L[1]:
        c.rrect(0, 0, W, H, 0, (10, 14, 26, int(240 * fade(t, L[1]))))
        kk = pop(t, L[1] + 0.3)
        c.text(640, 230, '< 6 cents', 110, MINT, 900, a=clamp(kk), stroke=6)
        c.text(640, 330, 'of every grocery dollar goes back to the farm', 30, WHITE, 900, a=clamp(kk))
        c.text(640, 375, '(USDA estimate, cited by the Farm Bureau)', 20, MUTED, 800, a=clamp(kk))
    if len(L) > 2 and t > L[2]:
        chip(c, 640, 470, 'turkey: higher production costs, flocks still recovering', CORAL, pop(t, L[2] + 0.3), 22)
    source(c, t, SRC_AFBF)


def s_eggs(c, x):
    t, L = x.t, x.L
    specks(c, t, 165)
    head(c, t, 'Eggs, average price per dozen')
    s = EGG['s']['2019-01-01':]
    xs = [d.year + (d.month - 1) / 12 for d in s.index]
    k = clamp((t - L[0] - 0.3) / 5.0) if t < L[1] else 1.0
    px, py = line_chart(c, (150, 130, 1120, 520), xs, list(s.values), (2019, 2027), (0, 7), k, GOLD,
                        xticks=range(2019, 2027), yticks=(0, 2, 4, 6), yfmt='${:.0f}', width=6)
    if t > L[1]:
        pk = EGG['peak_d']
        chip(c, px(pk.year + (pk.month - 1) / 12) + 40, py(EGG['peak']) - 30,
             f"peak: ${EGG['peak']:.2f} ({pk:%b %Y})", CORAL, pop(t, L[1] + 0.3), 22)
    if len(L) > 2 and t > L[2]:
        chip(c, px(xs[-1]) - 110, py(EGG['now']) - 60, f"now: ${EGG['now']:.2f}", MINT, pop(t, L[2] + 0.3), 24)
        pulse(c, t, (px(xs[-1]) - 20, py(EGG['now']) - 20, px(xs[-1]) + 20, py(EGG['now']) + 20), MINT, 20)
    source(c, t, 'BLS average price, eggs grade A large (APU0000708111)')


def s_pay(c, x):
    t, L = x.t, x.L
    specks(c, t, 166)
    head(c, t, 'Since January 2020: did your pay keep up?')
    items = [('Groceries', FOOD_UP, CORAL), ('All prices', ALL_UP, GOLD), ('Average hourly pay', PAY_UP, MINT)]
    compare_bars(c, t, items, L[0] + 0.3, 4.5, 45, lambda v: f'+{v:.1f}%', box=(220, 170, 1060, 520))
    if len(L) > 1 and t > L[1]:
        chip(c, 640, 120, f'average pay: ${PAY_NOW:.2f} an hour', SKY, pop(t, L[1] + 0.3), 24)
    if len(L) > 2 and t > L[2]:
        chip(c, 640, 590, 'on average: barely. Many people are below average.', CORAL, pop(t, L[2] + 0.3), 22)
    source(c, t, 'BLS via FRED: CUSR0000SAF11, CPIAUCSL, CES0500000003')


def s_bill(c, x):
    t, L = x.t, x.L
    specks(c, t, 167)
    head(c, t, 'Your grocery bill, in dollars (example)')
    new = WEEK * (1 + FOOD_UP / 100)
    k = pop(t, L[0] + 0.3)
    if k > 0:
        c.rrect(150, 150, 610, 430, 26, (255, 255, 255, 16), SKY, 4, a=clamp(k))
        c.text(380, 200, 'a week, January 2020', 26, WHITE, 900, a=clamp(k))
        c.text(380, 300, f'${WEEK:,.0f}', 90, SKY, 900, a=clamp(k), stroke=5)
        c.text(380, 390, f'${WEEK * 52:,.0f} a year', 26, MUTED, 800, a=clamp(k))
    if t > L[1] if len(L) > 1 else False:
        kk = pop(t, L[1] + 0.3)
        c.rrect(670, 150, 1130, 430, 26, (255, 255, 255, 16), CORAL, 4, a=clamp(kk))
        c.text(900, 200, 'the same cart today', 26, WHITE, 900, a=clamp(kk))
        c.text(900, 300, f'${new:,.0f}', 90, CORAL, 900, a=clamp(kk), stroke=5)
        c.text(900, 390, f'${new * 52:,.0f} a year', 26, MUTED, 800, a=clamp(kk))
    if len(L) > 2 and t > L[2]:
        chip(c, 640, 510, f'+${(new - WEEK) * 52:,.0f} a year for the same food', CORAL, pop(t, L[2] + 0.3), 28)
        pulse(c, t, (300, 470, 980, 550), CORAL, 30)
    source(c, t, f'example: ${WEEK} a week in Jan 2020 x CPI food at home change')


def s_hours(c, x):
    t, L = x.t, x.L
    specks(c, t, 173)
    head(c, t, 'The weekly cart, in hours of average pay')
    new = WEEK * (1 + FOOD_UP / 100)
    for i, (lab, cost, pay, col) in enumerate((('January 2020', WEEK, PAY_2020, SKY), ('Today', new, PAY_NOW, GOLD))):
        k = pop(t, L[min(i, len(L) - 1)] + 0.3)
        if k <= 0:
            continue
        cx = 380 + i * 520
        c.rrect(cx - 220, 150, cx + 220, 450, 26, (255, 255, 255, 16), col, 4, a=clamp(k))
        c.text(cx, 200, lab, 28, WHITE, 900, a=clamp(k))
        c.text(cx, 300, f'{cost / pay:.1f} hours', 72, col, 900, a=clamp(k), stroke=5)
        c.text(cx, 390, f'${cost:.0f} / ${pay:.2f} an hour', 22, MUTED, 800, a=clamp(k))
    if len(L) > 2 and t > L[2]:
        chip(c, 640, 520, 'about the same, on average: the average hides who fell behind', CORAL, pop(t, L[2] + 0.3), 22)
    source(c, t, 'BLS: CES0500000003 average hourly earnings; example cart')


def s_card(c, x):
    t, L = x.t, x.L
    fx.photo(c, CART, 1.06, (0.5, 0.5), box=FULL, dark=0.75, sat=1.0)
    head(c, t, 'Before Black Friday: the credit card math')
    k = pop(t, L[0] + 0.3)
    if k > 0:
        c.text(640, 230, f'{CARD_NOW:.2f}%', int(130 * (0.6 + 0.4 * clamp(k))), CORAL, 900, a=clamp(k), stroke=7)
        c.text(640, 320, f'average card rate on balances that pay interest ({CARD_D:%b %Y})', 24, WHITE, 900, a=clamp(k))
        if t > L[0] + 4:
            chip(c, 640, 380, f'early 2020: {CARD_2020:.2f}%', SKY, pop(t, L[0] + 4), 22)
    if len(L) > 1 and t > L[1]:
        kk = pop(t, L[1] + 0.3)
        c.rrect(330, 430, 950, 560, 24, (20, 24, 40, 235), GOLD, 4, a=clamp(kk))
        c.text(640, 470, '$500 of holiday shopping, left on the card a year', 24, WHITE, 900, a=clamp(kk))
        c.text(640, 520, f'about ${CARD_COST:.0f} in interest', 38, GOLD, 900, a=clamp(kk))
    source(c, t, 'Federal Reserve G.19 via FRED (TERMCBCCINTNS); monthly compounding, no payments')


def s_down(c, x):
    t, L = x.t, x.L
    fx.photo(c, DINNER, 1.06, (0.5, 0.5), box=FULL, dark=0.72, sat=1.0)
    head(c, t, 'What got cheaper this Thanksgiving')
    downs = [(n, p, ch) for n, p, ch in ITEMS if ch < 0]
    for i, (n, p, ch) in enumerate(downs):
        k = pop(t, L[0] + 0.5 + 1.3 * i)
        tag(c, 300 + (i % 2) * 680, 220 + (i // 2) * 150, f'{n} {ch:.1f}%', MINT, k, 26)
    if len(L) > 1 and t > L[1]:
        chip(c, 640, 560, 'a third of the dinner items fell in price; low wheat prices helped', SKY, pop(t, L[1] + 0.3), 22)
    source(c, t, SRC_AFBF)


def s_save(c, x):
    t, L = x.t, x.L
    fx.photo(c, CART, 1.06, (0.5, 0.5), box=FULL, dark=0.72, sat=1.0)
    head(c, t, 'Ways people cut the grocery bill')
    items = [('scale', 'Compare the\nunit price'), ('tag', 'Store brands'), ('calendar', 'Plan the week,\nwaste less'),
             ('snowflake', 'Frozen fruit\n& veg')]
    icon_row(c, t, items, L[0] + 0.2, max(4.0, (L[-1] - L[0]) * 0.85), y=300, color=GOLD)
    c.text(640, 570, 'Education only, not financial advice', 18, MUTED, 700, a=fade(t, 1))


def s_recap(c, x):
    t, L = x.t, x.L
    specks(c, t, 168)
    head(c, t, 'Recap')
    pts = [f'Groceries: +{FOOD_UP:.1f}% since January 2020',
           f'Thanksgiving dinner for 10: ${DINNER_TOTAL:.2f}, turkey +10%',
           f"Coffee +{PRICES['Coffee']['up']:.0f}%, beef +{PRICES['Ground beef']['up']:.0f}%, eggs back down to "
           f"${EGG['now']:.2f}",
           'Diesel, labor, packaging: under 6 cents per dollar to farms',
           f'Average pay +{PAY_UP:.1f}%: barely ahead of groceries']
    step = max(1.6, (L[1] - L[0] - 0.5) / len(pts)) if len(L) > 1 else 2.0
    for i, p in enumerate(pts):
        k = pop(t, L[0] + 0.3 + step * i)
        if k > 0:
            c.circle(170, 150 + i * 80, 10, GOLD, a=clamp(k))
            c.text(200, 150 + i * 80, p, 27, WHITE, 800, anchor='lm', a=clamp(k))
    if len(L) > 1 and t > L[1]:
        chip(c, 640, 560, 'Which grocery price shocked you most? Tell us below', GOLD, pop(t, L[1] + 0.3), 24)


SCENES = [
    dict(draw=s_hook, chapter='Your groceries: +32%', lead=0.15, gap=0.3, lines=[
        f"!Your groceries cost {FOOD_UP:.0f} percent more than in January 2020. Look: coffee, beef, eggs.",
        f"This Thursday's Thanksgiving dinner for 10? {DINNER_TOTAL:.2f} dollars. The turkey alone is up 10 percent "
        "from last year.",
        "And one item in your cart more than doubled since 2020. Which one? Stay for minute 3.",
        "By the end, you'll know what this costs your family each year, and whether your paycheck kept up.",
    ], punch=lambda L: [L[0] + 0.1, L[2] + 0.3],
        sfx=lambda L: [(L[0] + 0.1, 'hit'), (L[0] + 2.2, 'pop'), (L[0] + 4.2, 'pop'), (L[0] + 6.2, 'pop'),
                       (L[1] + 0.2, 'whoosh'), (L[1] + 2.8, 'pop'), (L[2] + 0.3, 'hit'), (L[3] + 0.3, 'ding')]),
    dict(draw=s_promise, lines=[
        "Here's the plan: your Thanksgiving receipt, line by line. What went up the most. Why food really costs "
        "more. And whether your pay kept up.",
    ], sfx=lambda L: [(L[0] + 0.5 + 1.4 * i, 'pop') for i in range(4)]),
    dict(draw=s_receipt, chapter='Thanksgiving, line by line', lines=[
        "Here's your receipt. Watch the right column: red went up, green got cheaper. Every year since 1986, the "
        "American Farm Bureau, a farmers' group, prices the same menu for 10: a 16-pound turkey, stuffing, sweet "
        "potatoes, rolls, peas, cranberries, a veggie tray, pumpkin pie with whipped cream, and milk.",
        f"This year, it adds up to {DINNER_TOTAL:.2f} dollars. That's more than 6 percent higher than last year.",
        f"That's about {DINNER_TOTAL / 10:.2f} per person. And the good news: it's still {DINNER_REC - DINNER_TOTAL:.2f} "
        f"dollars below the record of {DINNER_REC:.2f} set in 2022.",
        "Where you live matters too. The South has the cheapest average dinner, at 54.33. The Northeast pays the "
        "most: 61.57.",
    ], sfx=lambda L: [(L[0] + 0.5 + 0.7 * i, 'tick') for i in range(12)] + [(L[1] + 0.3, 'hit'), (L[2] + 0.3, 'pop'),
                                                                           (L[2] + 2.0, 'ding'), (L[3] + 0.3, 'pop')]),
    dict(draw=s_big, chapter='What happened after 2021?', lines=[
        "Now zoom out from one dinner to everything you buy at the grocery store. This line is the government's "
        "price tag for a typical grocery cart, set to 100 in January 2020. Watch what happens after 2021.",
        f"!It's now about {100 + FOOD_UP:.0f}. In plain terms: groceries that cost 100 dollars in January 2020 cost "
        f"about {100 + FOOD_UP:.0f} dollars today.",
        f"And it's still climbing. In October alone, grocery prices rose {FOOD_MOM:.1f} percent"
        + (f", the biggest one-month jump since {FOOD_MOM_SINCE:%B}." if FOOD_MOM_SINCE is not None else "."),
    ], punch=lambda L: [L[1] + 0.3], sfx=lambda L: [(L[0] + 0.3, 'whoosh'), (L[0] + 5.3, 'ding'), (L[1] + 0.3, 'hit'),
                                                    (L[2] + 0.3, 'pop')]),
    dict(draw=s_eatout, chapter='Is eating out the answer?', lines=[
        f"So is eating out the answer? Not really. Since January 2020, grocery prices rose about {FOOD_UP:.0f} "
        f"percent. Restaurant prices rose about {EATOUT_UP:.0f} percent.",
        "Eating out went up even faster, because restaurants pay for the same food, plus wages, rent and energy. "
        "Cooking at home is still the cheaper way to eat.",
    ], sfx=lambda L: [(L[0] + 0.3, 'pop'), (L[0] + 1.6, 'pop'), (L[1] + 0.3, 'ding')]),
    dict(draw=s_items, chapter='The item that doubled', lines=[
        f"So which item doubled? Let's count up to it. Bananas are up only {PRICES['Bananas']['up']:.0f} percent since 2020. A "
        f"gallon of whole milk, {PRICES['Whole milk']['up']:.0f} percent. White bread, "
        f"{PRICES['White bread']['up']:.0f}. Eggs, {EGG['up']:.0f}. And ground beef, up "
        f"{PRICES['Ground beef']['up']:.0f} percent, from {PRICES['Ground beef']['then']:.2f} to "
        f"{PRICES['Ground beef']['now']:.2f} a pound.",
        f"!And here's the one that more than doubled: coffee. A pound of ground coffee averaged "
        f"{PRICES['Coffee']['then']:.2f} in January 2020. In October, it was {PRICES['Coffee']['now']:.2f}. That's up "
        f"{PRICES['Coffee']['up']:.0f} percent. Your morning cup costs more than twice what it did. "
        "If that surprised you, subscribe: we explain everyday money in plain English, every day.",
    ], punch=lambda L: [L[1] + 0.3], sfx=lambda L: [(L[0] + 0.4 + 1.6 * i, 'pop') for i in range(5)]
        + [(L[1] + 0.3, 'hit')]),
    dict(draw=s_coffee, chapter='How high did it go?', lines=[
        "Let's look closer at coffee. This line is the average price of a pound of ground coffee in U.S. stores. "
        "It barely moved for years, then took off.",
        f"It hit a record of {PRICES['Coffee']['peak']:.2f} dollars a pound in {PRICES['Coffee']['peak_d']:%B %Y}.",
        f"It has eased a little since, to {PRICES['Coffee']['now']:.2f}, but that's still more than double the "
        f"{PRICES['Coffee']['then']:.2f} it cost in January 2020.",
    ], sfx=lambda L: [(L[0] + 0.3, 'whoosh'), (L[1] + 0.3, 'hit'), (L[2] + 0.3, 'pop')]),
    dict(draw=s_beef, chapter='Why burgers cost more', lines=[
        "Beef is the other big one, and it matters for a lot of family dinners. This is the average price of a "
        "pound of ground beef.",
        f"It set a record of {PRICES['Ground beef']['peak']:.2f} dollars a pound in "
        f"{PRICES['Ground beef']['peak_d']:%B %Y}, just a few months ago.",
        f"In October it was {PRICES['Ground beef']['now']:.2f}, compared with {PRICES['Ground beef']['then']:.2f} in "
        "January 2020. Burgers, tacos and chili all cost a lot more to make at home.",
    ], sfx=lambda L: [(L[0] + 0.3, 'whoosh'), (L[1] + 0.3, 'hit'), (L[2] + 0.3, 'pop')]),
    dict(draw=s_why, chapter='Only 6 cents to the farm?', lines=[
        "So why does food cost so much more? The Farm Bureau's economists point to the trip from the farm to your "
        "table. Diesel for the trucks and tractors. A shortage of farm workers. And the cost of processing, "
        "packaging and shipping everything.",
        "Here's the part most people don't know: by the USDA's estimate, less than 6 cents of every dollar you "
        "spend on groceries goes back to the farmer. The rest pays for everything that happens after the farm.",
        "Turkey has its own story. Production costs are higher, and turkey flocks are still recovering, which "
        "pushed the price of a 16-pound bird to 23.68 dollars.",
    ], sfx=lambda L: [(L[0] + 0.5, 'pop'), (L[0] + 2.5, 'pop'), (L[0] + 4.5, 'pop'), (L[1] + 0.3, 'hit'),
                      (L[2] + 0.3, 'pop')]),
    dict(draw=s_eggs, chapter='The price that crashed', lines=[
        f"But prices don't only go up. Remember eggs? In January 2020, a dozen averaged {EGG['then']:.2f}.",
        f"Then, as bird flu hit flocks, the price exploded, to a peak of {EGG['peak']:.2f} a dozen in "
        f"{EGG['peak_d']:%B %Y}.",
        f"Today it's back down to {EGG['now']:.2f}. Still higher than 2020, but way off the peak. When supply "
        "recovers, prices can fall fast.",
    ], sfx=lambda L: [(L[0] + 0.3, 'whoosh'), (L[1] + 0.3, 'hit'), (L[2] + 0.3, 'ding')]),
    dict(draw=s_pay, chapter='Did your pay keep up?', lines=[
        f"Now the big question. Did your pay keep up? Since January 2020, grocery prices rose {FOOD_UP:.1f} percent. "
        f"All consumer prices, {ALL_UP:.1f} percent. And average hourly pay for workers at private companies rose "
        f"{PAY_UP:.1f} percent.",
        f"Average pay is now {PAY_NOW:.2f} dollars an hour. So this year's Thanksgiving dinner for 10 costs about "
        f"{HOURS:.1f} hours of average pay.",
        "So on average, pay just barely stayed ahead of groceries. But that's an average. If your raises were "
        "smaller, or you're on a fixed income, money that doesn't rise with prices, groceries have taken a bigger bite out of your budget. That's why "
        "so many people feel squeezed, even when the averages look okay.",
    ], sfx=lambda L: [(L[0] + 0.3, 'pop'), (L[0] + 1.8, 'pop'), (L[0] + 3.3, 'pop'), (L[1] + 0.3, 'ding'),
                      (L[2] + 0.3, 'down')]),
    dict(draw=s_bills, chapter='Bills that beat your pay', lines=[
        f"And groceries aren't the only bill that grew. Here's how much the main household costs went up since "
        f"January 2020. Gas at the pump is up the most, about {BILLS[0][1]:.0f} percent. Electricity, about "
        f"{BILLS[1][1]:.0f} percent. Eating out, {BILLS[2][1]:.0f}. Rent, {BILLS[3][1]:.0f}. Groceries, "
        f"{BILLS[4][1]:.0f}. And used cars, {BILLS[5][1]:.0f}.",
        f"Now the green line: average hourly pay, up {PAY_UP:.0f} percent. Everything to the right of that line "
        "rose faster than pay. Gas, electricity and eating out all beat it, and rent just barely. That's why a budget that worked in "
        "2019 feels tight today.",
    ], sfx=lambda L: [(L[0] + 0.4 + 1.2 * i, 'pop') for i in range(6)] + [(L[1] + 0.3, 'hit')]),
    dict(draw=s_bill, chapter='What it costs you a year', lines=[
        f"Let's put that in dollars. Say your family spent {WEEK} dollars a week on groceries in January 2020. That's "
        f"{WEEK * 52:,.0f} dollars a year.",
        f"The same cart today costs about {WEEK * (1 + FOOD_UP / 100):.0f} dollars a week, or "
        f"{WEEK * 52 * (1 + FOOD_UP / 100):,.0f} a year.",
        f"!That's about {WEEK * 52 * FOOD_UP / 100:,.0f} dollars more every year, for the exact same food.",
    ], punch=lambda L: [L[2] + 0.3], sfx=lambda L: [(L[0] + 0.3, 'pop'), (L[1] + 0.3, 'pop'), (L[2] + 0.3, 'hit')]),
    dict(draw=s_hours, chapter='How many hours per cart?', lines=[
        f"Here's another way to measure it: how many hours of work does that weekly cart cost? In January 2020, "
        f"average pay was {PAY_2020:.2f} an hour, so a {WEEK} dollar cart took about {WEEK / PAY_2020:.1f} hours of work.",
        f"Today, the bigger bill divided by today's higher pay comes to about "
        f"{WEEK * (1 + FOOD_UP / 100) / PAY_NOW:.1f} hours. Almost exactly the same.",
        "So for the average worker, groceries take about the same slice of time. But averages hide a lot. If your "
        "pay grew slower than average, the same cart takes you more hours than it used to.",
    ], sfx=lambda L: [(L[0] + 0.3, 'pop'), (L[1] + 0.3, 'pop'), (L[2] + 0.3, 'down')]),
    dict(draw=s_down, chapter='What got cheaper', lines=[
        "Not everything on the Thanksgiving table went up this year. The veggie tray, pie crusts, frozen peas and "
        "whipping cream all got a little cheaper.",
        "In fact, a third of the dinner items fell in price, and the Farm Bureau says low wheat prices helped keep "
        "flour-based foods down.",
    ], sfx=lambda L: [(L[0] + 0.5 + 1.3 * i, 'pop') for i in range(4)] + [(L[1] + 0.3, 'ding')]),
    dict(draw=s_card, chapter='The credit card trap', lines=[
        f"One warning before Black Friday. The average credit card rate on balances that charge interest is now "
        f"{CARD_NOW:.2f} percent, according to the Federal Reserve. In early 2020 it was {CARD_2020:.2f}.",
        f"So if you put 500 dollars of holiday shopping on a card and leave it there for a year, you'd pay about "
        f"{CARD_COST:.0f} dollars in interest. That can wipe out the discount you were chasing.",
    ], sfx=lambda L: [(L[0] + 0.3, 'hit'), (L[0] + 4, 'pop'), (L[1] + 0.3, 'ding')]),
    dict(draw=s_save, chapter='4 ways to cut the bill', lines=[
        "So what can you actually do? These are the habits consumer experts recommend most. Compare the unit "
        "price on the shelf tag, not the sticker price: it shows the cost per ounce or per pound.",
        "Try store brands, which usually cost less for similar products. Plan the week's meals so less food gets "
        "thrown away. And frozen fruit and vegetables keep longer and often cost less than fresh.",
    ], sfx=lambda L: [(L[0] + 0.5, 'pop'), (L[0] + 3.5, 'pop'), (L[1] + 0.3, 'pop'), (L[1] + 3.5, 'pop')]),
    dict(draw=s_recap, chapter='Recap', lines=[
        f"Let's recap. Your groceries cost about {FOOD_UP:.0f} percent more than in January 2020. Thanksgiving "
        f"dinner for 10 is {DINNER_TOTAL:.2f} dollars this year, with the turkey up 10 percent. Coffee more than "
        "doubled, beef is up nearly three quarters, and eggs came back down. Most of what you pay goes to fuel, "
        "labor and packaging, not the farm. And average pay only barely kept up.",
        "!So tell me: which grocery price shocked you the most? Drop it in the comments. And subscribe, so you "
        "don't miss tomorrow's video.",
        "This video is for education only. It's not financial advice. Happy Thanksgiving.",
    ], punch=lambda L: [L[1] + 0.3], sfx=lambda L: [(L[0] + 0.3 + 2.5 * j, 'pop') for j in range(5)]
        + [(L[1] + 0.3, 'ding')]),
]
for _sc in SCENES:
    _sc['draw'] = ticker(_sc['draw'])
SHORTS = {}


def check_numbers():
    script = ' '.join(l for sc in SCENES for l in sc['lines'])
    assert LAST.strftime('%Y-%m') == '2026-10' and round(FOOD_UP, 1) == 32.5 and round(ALL_UP, 1) == 30.2
    assert round(PAY_UP, 1) == 33.7 and PAY_NOW == 38.0
    assert round(sum(p for _, p, _ in ITEMS), 2) == DINNER_TOTAL and len(ITEMS) == 12
    assert sum(ch < 0 for _, _, ch in ITEMS) == 4 and round(DINNER_REC - DINNER_TOTAL, 2) == 5.42
    exp = {'Coffee': (4.174, 9.249, 122), 'Ground beef': (3.886, 6.755, 74), 'Eggs': (1.461, 2.32, 59),
           'White bread': (1.351, 1.861, 38), 'Whole milk': (3.253, 4.101, 26), 'Bananas': (0.57, 0.655, 15)}
    for n, (a, b, u) in exp.items():
        p = PRICES[n]
        assert (round(p['then'], 3), round(p['now'], 3), round(p['up'])) == (a, b, u), (n, p['then'], p['now'], p['up'])
    assert round(EGG['peak'], 2) == 6.23 and EGG['peak_d'].strftime('%Y-%m') == '2025-03'
    assert round(PAY_2020, 2) == 28.43 and CARD_NOW == 22.36 and CARD_2020 == 16.61 and round(CARD_COST) == 124
    assert round(FOOD_MOM, 1) == 0.4 and round(EATOUT_UP, 1) == 38.6 and round(HOURS, 1) == 1.5
    assert [(n, round(v)) for n, v in BILLS] == [('Gas (regular, weekly)', 52), ('Electricity', 45), ('Eating out', 39),
                                                 ('Rent', 34), ('Groceries', 32), ('Used cars', 29)], BILLS
    assert round(PRICES['Coffee']['peak'], 2) == 9.72 and PRICES['Coffee']['peak_d'].strftime('%Y-%m') == '2026-04'
    assert round(PRICES['Ground beef']['peak'], 2) == 6.92 and PRICES['Ground beef']['peak_d'].strftime('%Y-%m') == '2026-08'
    for s in ('not financial advice', 'American Farm Bureau', 'USDA', '6 cents', 'more than 6 percent'):
        assert s in script, s
    print(f'numbers check: OK  ({len(script.split())} words)  food +{FOOD_UP:.2f}% all +{ALL_UP:.2f}% pay +{PAY_UP:.2f}% '
          f'(${PAY_NOW}); Oct m/m +{FOOD_MOM:.2f}% (biggest since {FOOD_MOM_SINCE}); '
          + ', '.join(f"{n} {p['then']:.2f}->{p['now']:.2f} ({p['up']:+.0f}%)" for n, p in PRICES.items()))


if __name__ == '__main__':
    check_numbers()
    os.makedirs(BUILD, exist_ok=True)
    if '--check' in sys.argv:
        sys.exit()
    if '--stills' in sys.argv:
        previews(SCENES, SHORTS, os.path.join(BUILD, 'previews'))
        sys.exit()
    only = [int(a) for a in sys.argv[sys.argv.index('--only') + 1].split(',')] if '--only' in sys.argv else None
    total, chapters = build(SCENES, os.path.join(OUT, 'ep13_groceries.mp4'), BUILD, only=only,
                            srt_path=os.path.join(OUT, 'ep13_groceries.en.srt'))
    with open(os.path.join(OUT, 'ep13_chapters.txt'), 'w') as f:
        for at, name in chapters:
            f.write(f'{fmt_time(at)} {name}\n')
    print(f'total {total / 60:.1f} min')
