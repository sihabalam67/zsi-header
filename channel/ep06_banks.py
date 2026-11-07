"""Episode 6: How banks create money out of thin air (long video, Fri Nov 13 2026).

    python3 channel/ep06_banks.py [--stills]

Facts (checked in check_numbers; every number from data or an official source):
- Bank of England, "Money creation in the modern economy", Quarterly Bulletin 2014 Q1 (McLeay, Radia, Thomas):
  commercial banks create most money by making loans; repaying loans destroys money; the money multiplier
  textbook story is not how it works in practice; bank deposits were 97% of UK broad money.
- Federal Reserve: reserve requirement ratios cut to 0% effective March 26, 2020.
- Federal Reserve, "Review of the Federal Reserve's Supervision and Regulation of Silicon Valley Bank" (April 28,
  2023): depositors withdrew $42 billion on March 9, 2023; SVB was closed on March 10, 2023.
- FDIC: deposits insured up to $250,000 per depositor, per insured bank, for each account ownership category.
- FRED: M2SL (M2, $bn, monthly), WCURCIR (currency in circulation, $m, weekly), WALCL (Fed total assets, $m,
  weekly), CPIAUCSL (CPI, for inflation), DPSACBW027SBOG (commercial bank deposits), TOTLL (loans and leases).
Visuals are drawn in code (made-up bank, people and app); photos: channel/assets/photos/ep06s (PD/CC0).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from wk2_art import *  # noqa: E402,F401,F403
from engine import build, previews  # noqa: E402
import fx  # noqa: E402

OUT = os.path.join(HERE, 'out')
BUILD = os.path.join(HERE, 'build', 'ep06_long')
PH = os.path.join(HERE, 'assets', 'photos', 'ep06s')
CASH, VAULT, BANKP, HOUSES = (os.path.join(PH, f) for f in ('cash.jpg', 'vault.png', 'bank.jpg', 'houses.jpg'))
FULL = (0, 0, W, H)

M2 = series('M2SL')                       # $ billions
CUR = series('WCURCIR')                   # $ millions
FED = series('WALCL')                     # $ millions
CPI = series('CPIAUCSL')
DEP = series('DPSACBW027SBOG')            # $ billions
LNS = series('TOTLL')                     # $ billions
RES = series('TOTRESNS')                  # $ billions, reserves of depository institutions
MORT = series('MORTGAGE30US')             # %, Freddie Mac weekly average 30-year fixed
SAVE = series('SNDR')                     # %, FDIC national savings rate

M2_NOW, M2_DATE = M2.iloc[-1] / 1000, M2.index[-1]          # $ trillions
CASH_NOW = CUR.iloc[-1] / 1e6                                 # $ trillions
SHARE = CASH_NOW / M2_NOW
M2_1960 = M2[M2.index.year == 1960].mean()                    # $ billions
TIMES = M2.iloc[-1] / M2_1960
M2_FEB20, M2_PEAK = M2['2020-02'].iloc[0] / 1000, M2['2020':'2023'].max() / 1000
M2_PEAK_DATE = M2['2020':'2023'].idxmax()
M2_JUMP = (M2_PEAK / M2_FEB20 - 1) * 100
M2_YOY = M2.pct_change(12) * 100
YOY_MAX, YOY_MAX_DATE = M2_YOY.max(), M2_YOY.idxmax()
FED_MAR20 = FED['2020-03-04':'2020-03-04'].iloc[0] / 1e6
FED_PEAK, FED_PEAK_DATE = FED.max() / 1e6, FED.idxmax()
FED_NOW = FED.iloc[-1] / 1e6
INFL = CPI.pct_change(12) * 100
INFL_PEAK, INFL_PEAK_DATE = INFL['2021':'2023'].max(), INFL['2021':'2023'].idxmax()
INFL_PREV = INFL[(INFL >= INFL_PEAK) & (INFL.index < '2021')].index[-1]   # last time it was this high
INFL_NOW = INFL.iloc[-1]
LOAN = 300000
MORT_NOW, MORT_DATE, SAVE_NOW, SAVE_DATE = MORT.iloc[-1], MORT.index[-1], SAVE.iloc[-1], SAVE.index[-1]
_r = MORT_NOW / 100 / 12
PAY = LOAN * _r / (1 - (1 + _r) ** -360)
TOTAL = PAY * 360
INTEREST = TOTAL - LOAN
NEG = (M2.pct_change(12) * 100)
NEG = NEG[NEG < 0]
M2_LOW, M2_LOW_DATE = M2['2023':'2024'].min() / 1000, M2['2023':'2024'].idxmin()
DEP_NOW, LNS_NOW, RES_NOW = DEP.iloc[-1] / 1000, LNS.iloc[-1] / 1000, RES.iloc[-1] / 1000
BOE = 'Bank of England, "Money creation in the modern economy" (2014)'

M2X = [d.year + (d.month - 1) / 12 for d in M2[M2.index.year >= 1960].index]
M2Y = [v / 1000 for v in M2[M2.index.year >= 1960].values]
F19 = FED['2019':]
FX_ = [d.year + (d.dayofyear - 1) / 366 for d in F19.index]
FY_ = [v / 1e6 for v in F19.values]
M19 = M2['2019':]
MX19 = [d.year + (d.month - 1) / 12 for d in M19.index]
MY19 = [v / 1000 for v in M19.values]
I19 = INFL['2019':]
IX19 = [d.year + (d.month - 1) / 12 for d in I19.index]
IY19 = list(I19.values)

BANK_C, MAYA_C, SELL_C = (70, 110, 170), CORAL, SKY


def tn(v):
    return f'${v:.1f} trillion'


# ------------------------------------------------------------------ helpers --
def head(c, t, text, y=62, size=34):
    c.text(640, y, text, size, WHITE, 900, a=fade(t, 0))


def bank(c, x, y, s, a=1.0, label='BANK'):
    """A made-up bank building, (x, y) = base centre."""
    c.poly([(x - 130 * s, y - 150 * s), (x, y - 215 * s), (x + 130 * s, y - 150 * s)], CREAM, mix(CREAM, INK, 0.4),
           3 * s, a)
    c.rrect(x - 120 * s, y - 150 * s, x + 120 * s, y - 130 * s, 4 * s, CREAM, a=a)
    for i in range(5):
        cx = x - 96 * s + i * 48 * s
        c.rrect(cx - 11 * s, y - 128 * s, cx + 11 * s, y - 18 * s, 4 * s, mix(CREAM, WHITE, 0.4),
                mix(CREAM, INK, 0.3), 2 * s, a)
    c.rrect(x - 135 * s, y - 18 * s, x + 135 * s, y, 4 * s, CREAM, mix(CREAM, INK, 0.4), 3 * s, a)
    c.text(x, y - 175 * s, label, int(22 * s), INK, 900, a=a, shadow=False)


def tacct(c, t, x0, y0, w, rows, k=1.0, title=None):
    """A bank's books: assets left, liabilities right. rows: [(appear_t, side, label, value_text, color)]."""
    a = clamp(k)
    if a <= 0:
        return
    c.rrect(x0, y0, x0 + w, y0 + 330, 22, (20, 26, 42), (255, 255, 255, 60), 2, a)
    if title:
        c.text(x0 + w / 2, y0 + 34, title, 26, GOLD, 900, a=a)
    c.text(x0 + w / 4, y0 + 78, 'WHAT IT OWNS', 20, MINT, 900, a=a)
    c.text(x0 + 3 * w / 4, y0 + 78, 'WHAT IT OWES', 20, CORAL, 900, a=a)
    c.line([(x0 + w / 2, y0 + 60), (x0 + w / 2, y0 + 310)], (255, 255, 255, 70), 2, a)
    c.line([(x0 + 20, y0 + 100), (x0 + w - 20, y0 + 100)], (255, 255, 255, 70), 2, a)
    n = {'L': 0, 'R': 0}
    for at, side, label, val, col in rows:
        kk = pop(t, at)
        if kk <= 0:
            continue
        cx = x0 + (w / 4 if side == 'L' else 3 * w / 4)
        cy = y0 + 145 + n[side] * 90
        n[side] += 1
        c.text(cx, cy, label, 20, WHITE, 800, a=clamp(kk) * a)
        c.text(cx, cy + 36, val, int(34 * (0.7 + 0.3 * clamp(kk))), col, 900, a=clamp(kk) * a)


def pulse(c, t, box, col, r=20, on=True):
    """A breathing outline that keeps attention on the element being talked about."""
    if on:
        c.rrect(*box, r, None, col, 5, a=0.3 + 0.7 * (0.5 + 0.5 * math.sin(t * 5)))


def typed(text, t, at, speed=14):
    n = int(clamp((t - at) * speed / max(1, len(text))) * len(text))
    return text[:n]


def phone_app(c, x, y, s, t, amount, a=1.0, label='Checking'):
    """A made-up bank app on a phone."""
    c.rrect(x - 95 * s, y - 190 * s, x + 95 * s, y + 190 * s, 26 * s, (16, 18, 26), (255, 255, 255, 120), 3 * s, a)
    c.rrect(x - 82 * s, y - 165 * s, x + 82 * s, y + 165 * s, 14 * s, (238, 242, 250), a=a)
    c.text(x, y - 135 * s, 'MY BANK', int(18 * s), INK, 900, a=a, shadow=False)
    c.text(x, y - 60 * s, label, int(16 * s), (90, 100, 120), 700, a=a, shadow=False)
    c.text(x, y - 20 * s, amount, int(30 * s), (20, 120, 80), 900, a=a, shadow=False)
    c.rrect(x - 60 * s, y + 60 * s, x + 60 * s, y + 100 * s, 18 * s, (70, 110, 170), a=a)
    c.text(x, y + 80 * s, 'Transfer', int(15 * s), WHITE, 800, a=a, shadow=False)


def digital_bill(c, x, y, w, t, a=1.0, seed=0):
    """A glowing outline bill made of light: 'typed' money."""
    g = 0.6 + 0.4 * math.sin(t * 4 + seed)
    h = w * 0.45
    c.rrect(x - w / 2, y - h / 2, x + w / 2, y + h / 2, 8, (60, 200, 255, int(40 * g)), (110, 220, 255), 3, a)
    c.text(x, y, '$', int(h * 0.7), (150, 230, 255), 900, a=a * g, shadow=False)


# ------------------------------------------------------------------- scenes --
def s_hook(c, x):
    t, L = x.t, x.L
    fx.photo(c, CASH, 1.15 - 0.03 * clamp(t / 12), (0.83, 0.72), box=FULL, dark=0.6, sat=1.1)
    c.rrect(0, 0, W, H, 0, (8, 12, 24, 120))
    for i in range(10):  # ten dollars: one real bill, nine made of light
        cx, cy = 200 + (i % 5) * 220, 230 + (i // 5) * 150
        k = pop(t, L[0] + 0.15 + 0.08 * i)
        if k <= 0:
            continue
        if i == 0:
            bill(c, cx, cy, 170 * (0.6 + 0.4 * clamp(k)), '1', a=clamp(k))
        elif t > L[1] + 0.3:
            digital_bill(c, cx, cy, 170, t, clamp(pop(t, L[1] + 0.3 + 0.1 * i)), seed=i)
        else:
            bill(c, cx, cy, 170, '1', a=clamp(k) * 0.35)
    kk = pop(t, L[0] + 0.1)
    if kk > 0:
        c.text(640, 520, '1 IN 10', int(96 * (0.6 + 0.4 * clamp(kk))), GOLD, 900, a=clamp(kk), stroke=7)
        c.text(640, 585, 'dollars in America is actual cash', 28, WHITE, 800, a=clamp(kk))
    if t > L[1] + 0.3:
        c.rrect(870, 110, 1180, 160, 25, (60, 200, 255), a=fade(t, L[1] + 0.3))
        c.text(1025, 135, 'typed into existence', 22, INK, 900, a=fade(t, L[1] + 0.3), shadow=False)


def s_promise(c, x):
    t, L = x.t, x.L
    specks(c, t, 61)
    if t < L[1]:
        k = pop(t, L[0] + 0.4)
        c.icon('landmark', 640, 230, 150 * clamp(k), GOLD, a=clamp(k))
        if t > L[0] + 2.2:
            c.text(640, 370, 'Bank of England', 44, WHITE, 900, a=fade(t, L[0] + 2.2))
            chip(c, 640, 440, '"Money creation in the modern economy", 2014', SKY, pop(t, L[0] + 3.4), 24)
        return
    items = [('banknote', 'how a loan\ncreates money', 0.6), ('trash-2', 'how paying it back\ndestroys money', 2.8),
             ('shield', 'what stops banks', 5.2), ('wallet', 'what it means\nfor you', 6.9)]
    for i, (ic, lab, at) in enumerate(items):
        k = pop(t, L[1] + at)
        if k <= 0:
            continue
        cx = 175 + i * 310
        c.circle(cx, 260, 85 * clamp(k), (255, 255, 255, 18), GOLD, 3)
        c.icon(ic, cx, 260, 80 * clamp(k), GOLD, a=clamp(k))
        for j, part in enumerate(lab.split('\n')):
            c.text(cx, 395 + j * 32, part, 24, WHITE, 800, a=clamp(k))
    c.text(640, 90, 'In the next ten minutes', 34, WHITE, 900, a=fade(t, L[1]))


def s_textbook(c, x):
    t, L = x.t, x.L
    specks(c, t, 62)
    head(c, t, 'The textbook story: the money multiplier')
    if t < L[1]:  # saver deposits $100, bank lends $90
        k = pop(t, L[0] + 0.5)
        person(c, 260, 470, 1.3, SKY, t, 0, 'happy', clamp(k))
        if t > L[0] + 2.0:
            u = clamp((t - L[0] - 2.0) / 1.2)
            bill(c, lerp(330, 560, ease(u)), 330, 120, '100')
        bank(c, 760, 520, 1.1, clamp(pop(t, L[0] + 1.2)))
        if t > L[0] + 4.6:
            chip(c, 760, 590, 'keeps a little, lends the rest', GOLD, pop(t, L[0] + 4.6), 24)
        return
    vals = [100 * 0.9 ** i for i in range(8)]
    for i, v in enumerate(vals):  # the cascade: 100, 90, 81, 72.9 ...
        g = ease(seg(t, L[1] + 0.6 + 0.9 * i, L[1] + 1.3 + 0.9 * i))
        if g <= 0:
            continue
        x0 = 130 + i * 132
        h = 330 * v / 100 * g
        c.rrect(x0, 500 - h, x0 + 92, 500, 8, MINT if i == 0 else mix(MINT, SKY, i / 8))
        c.text(x0 + 46, 520, f'${v:,.0f}' if v >= 10 else f'${v:.1f}', 20, WHITE, 800, a=g)
        c.text(x0 + 46, 545, 'deposit' if i == 0 else f'bank {i + 1}', 15, MUTED, 700, a=g, shadow=False)
    if L[1] < t < L[3]:
        chip(c, 640, 130, 'keep 10% in reserve, lend 90%', SKY, pop(t, L[1] + 0.3), 24)
    if t > L[2]:
        c.rrect(0, 0, W, H, 0, (8, 12, 24, int(150 * fade(t, L[2]))))
        c.text(640, 250, BOE.split(',')[0], 34, WHITE, 900, a=fade(t, L[2] + 0.2))
        c.text(640, 300, '"Money creation in the modern economy", 2014', 24, SKY, 800, a=fade(t, L[2] + 0.4))
        pulse(c, t, (300, 215, 980, 330), SKY, on=t < L[3])
        if L[2] + 3.0 < t < L[3]:
            chip(c, 640, 400, 'in practice: a different story', GOLD, pop(t, L[2] + 3.0), 26)
    if t > L[3]:
        k = pop(t, L[3] + 0.3, 0.3)
        s = lerp(1.8, 1.0, clamp(k))
        c.rrect(640 - 330 * s, 400 - 55 * s, 640 + 330 * s, 400 + 55 * s, 16, None, CORAL, 7, a=clamp(k))
        c.text(640, 400, 'NOT HOW IT WORKS', int(64 * s), CORAL, 900, a=clamp(k))
        if t > L[3] + 2.0:
            c.text(640, 500, 'The loan makes the deposit.', 40, GOLD, 900, a=fade(t, L[3] + 2.0), stroke=4)


def s_maya(c, x):
    t, L = x.t, x.L
    specks(c, t, 63)
    head(c, t, 'Watch money being created')
    k = pop(t, L[0] + 0.5)
    person(c, 270, 520, 1.4, MAYA_C, t, 0, 'happy', clamp(k))
    c.text(270, 560, 'MAYA', 24, WHITE, 900, a=clamp(k))
    if t > L[0] + 2.4:
        kh = pop(t, L[0] + 2.4)
        c.icon('house', 270, 190, 110 * clamp(kh), GOLD, a=clamp(kh))
        chip(c, 270, 285, f'${LOAN:,} mortgage', GOLD, pop(t, L[0] + 3.6), 24)
    bank(c, 900, 540, 1.25, clamp(pop(t, L[0] + 1.2)), 'MAYA\'S BANK')
    if t > L[1]:  # the bank checks income and credit, then approves
        for j, (txt, at) in enumerate((('income checked', 0.5), ('credit checked', 1.5))):
            chip(c, 600, 200 + j * 70, txt, SKY, pop(t, L[1] + at), 22)
        if t > L[1] + 2.8:
            kk = pop(t, L[1] + 2.8, 0.3)
            s = lerp(1.6, 1.0, clamp(kk))
            c.rrect(600 - 120 * s, 360 - 34 * s, 600 + 120 * s, 360 + 34 * s, 12, None, MINT, 5, a=clamp(kk))
            c.text(600, 360, 'APPROVED', int(40 * s), MINT, 900, a=clamp(kk))


def s_type(c, x):
    t, L = x.t, x.L
    specks(c, t, 64)
    if t < L[1] + 0.2:  # no vault, no savings: a keyboard
        k = pop(t, L[0] + 0.3)
        c.icon('vault', 330, 280, 160 * clamp(k), MUTED, a=clamp(k) * (0.4 if t > L[0] + 2.4 else 1))
        if t > L[0] + 2.4:
            c.line([(230, 180), (430, 380)], CORAL, 8)
            c.line([(430, 180), (230, 380)], CORAL, 8)
            c.text(330, 430, "no one else's savings", 26, CORAL, 900, a=fade(t, L[0] + 2.4))
        if t > L[0] + 4.0:
            c.icon('keyboard', 900, 280, 170 * clamp(pop(t, L[0] + 4.0)), GOLD)
            amt = typed(f'${LOAN:,}', t, L[0] + 4.8, 6)
            c.rrect(700, 400, 1100, 480, 18, (20, 26, 42), GOLD, 3, a=fade(t, L[0] + 4.4))
            c.text(900, 440, amt + ('|' if (t * 3) % 1 < 0.5 else ''), 46, GOLD, 900, a=fade(t, L[0] + 4.4))
        return
    rows = [(L[1] + 1.0, 'L', 'Loan to Maya', f'+${LOAN:,}', MINT),
            (L[1] + 5.2, 'R', "Maya's deposit", f'+${LOAN:,}', CORAL)]
    tacct(c, t, 140, 120, 640, rows, pop(t, L[1] + 0.2), "MAYA'S BANK: THE BOOKS")
    if L[1] + 1.0 < t < L[2]:
        pulse(c, t, (150, 235, 455, 335) if t < L[1] + 5.2 else (465, 235, 770, 335), MINT if t < L[1] + 5.2 else CORAL)
    phone_app(c, 1030, 300, 1.05, t, f'${LOAN:,}' if t > L[1] + 5.2 else '$0', clamp(pop(t, L[1] + 0.4)))
    if t > L[2]:
        kk = pop(t, L[2] + 0.4)
        c.rrect(140, 470, 780, 560, 20, GOLD, a=clamp(kk))
        c.text(460, 515, f'${LOAN:,} of brand-new money', 34, INK, 900, a=clamp(kk), shadow=False)
        burst(c, 1030, 280, clamp(seg(t, L[2] + 0.4, L[2] + 1.2)), GOLD, seed=3)


def s_spend(c, x):
    t, L = x.t, x.L
    specks(c, t, 65)
    head(c, t, 'The money moves. It does not disappear.')
    person(c, 220, 520, 1.3, MAYA_C, t, 0, 'happy')
    person(c, 1060, 520, 1.3, SELL_C, t, 1, 'happy')
    c.text(220, 560, 'MAYA', 22, WHITE, 900)
    c.text(1060, 560, 'SELLER', 22, WHITE, 900)
    bank(c, 430, 430, 0.75, 1.0, 'MAYA\'S')
    bank(c, 850, 430, 0.75, 1.0, 'SELLER\'S')
    u = clamp((t - L[0] - 1.0) / 2.5)
    if 0 < u < 1:
        for j in range(3):
            digital_bill(c, lerp(470, 810, ease(clamp(u * 1.2 - j * 0.1))), 220 + j * 30, 100, t, 1.0, j)
    c.icon('house', 640, 470, 110 * clamp(pop(t, L[0] + 3.5)), GOLD)
    if t > L[1]:
        k = pop(t, L[1] + 0.3)
        c.rrect(330, 120, 950, 190, 30, MINT, a=clamp(k))
        c.text(640, 155, 'now part of the money supply', 30, INK, 900, a=clamp(k), shadow=False)


def s_destroy(c, x):
    t, L = x.t, x.L
    specks(c, t, 66)
    head(c, t, 'Paying it back destroys money')
    paid = LOAN * ease(clamp((t - L[1] - 0.8) / 3.5)) if t > L[1] else 0
    left = LOAN - paid
    rows = [(0.2, 'L', 'Loan to Maya', f'${left:,.0f}', MINT), (0.2, 'R', 'Deposits', f'${left:,.0f}', CORAL)]
    tacct(c, t, 140, 110, 640, rows, pop(t, 0.2), 'THE BOOKS SHRINK TOGETHER')
    if t > L[0] + 1.5:
        kk = pop(t, L[0] + 1.5)
        c.icon('trash-2', 1030, 260, 150 * clamp(kk), CORAL)
        c.text(1030, 380, 'money destroyed', 28, CORAL, 900, a=clamp(kk))
    if t > L[2]:
        kk = pop(t, L[2] + 0.3)
        c.rrect(140, 470, 780, 560, 20, GOLD, a=clamp(kk))
        c.text(460, 515, 'interest = the bank\'s income', 32, INK, 900, a=clamp(kk), shadow=False)
        for j, lab in enumerate(('salaries', 'savers', 'profit')):
            chip(c, 1030, 450 + j * 55, lab, SKY, pop(t, L[2] + 2.0 + j * 0.6), 22)


def s_spread(c, x):
    t, L = x.t, x.L
    specks(c, t, 80)
    if t < L[1]:
        head(c, t, 'What banks charge vs what they pay')
        compare_bars(c, t, [('30-year mortgage', MORT_NOW, CORAL), ('Savings account', SAVE_NOW, MINT)], L[0] + 0.5,
                     2.0, 8, lambda v: f'{v:.2f}%', box=(380, 150, 900, 470), value_size=40, label_size=24)
        source(c, t, f'Freddie Mac 30-year rate ({MORT_DATE:%b %d}); FDIC national savings rate ({SAVE_DATE:%b %Y})')
        if t > L[0] + 3.5:
            pulse(c, t, (380, 140, 640, 480), CORAL)
        return
    if t < L[2]:
        head(c, t, f"Maya's ${LOAN:,} loan at {MORT_NOW:.2f}%")
        k = pop(t, L[1] + 0.3)
        c.text(640, 190, f'${PAY:,.0f} a month', int(70 * (0.7 + 0.3 * clamp(k))), GOLD, 900, a=clamp(k), stroke=5)
        g = ease(clamp((t - L[1] - 3.0) / 1.5))
        if g > 0:
            c.rrect(140, 300, 140 + 1000 * LOAN / TOTAL * g, 380, 12, MINT)
            c.rrect(140 + 1000 * LOAN / TOTAL * g, 300, 140 + 1000 * g, 380, 12, CORAL)
            c.text(140 + 500 * LOAN / TOTAL, 410, f'loan ${LOAN:,}', 24, MINT, 900, a=g)
            c.text(140 + 1000 * LOAN / TOTAL + 500 * INTEREST / TOTAL, 410, f'interest ${INTEREST:,.0f}', 24, CORAL,
                   900, a=g)
        if t > L[1] + 4.6:
            c.text(640, 500, f'total paid: ${TOTAL:,.0f}', 44, WHITE, 900, a=fade(t, L[1] + 4.6))
            pulse(c, t, (130, 290, 1150, 390), CORAL, 16)
        return
    head(c, t, 'The gap is how banks earn')
    k = pop(t, L[2] + 0.3)
    c.text(640, 250, f'{MORT_NOW:.2f}%  vs  {SAVE_NOW:.2f}%', int(70 * (0.7 + 0.3 * clamp(k))), GOLD, 900, a=clamp(k))
    chip(c, 640, 380, 'charge borrowers more, pay savers less', MINT, pop(t, L[2] + 3.0), 26)
    pulse(c, t, (300, 190, 980, 310), GOLD)


def s_cycle(c, x):
    t, L = x.t, x.L
    specks(c, t, 67)
    a = t * 0.9
    c.circle(640, 330, 190, None, (255, 255, 255, 50), 3)
    for j in range(8):  # money orbiting: born on one side, erased on the other
        ang = a + j * math.pi / 4
        bx, by = 640 + 190 * math.cos(ang), 330 + 190 * math.sin(ang)
        digital_bill(c, bx, by, 70, t, 0.9, j)
    chip(c, 330, 330, 'new loans: money born', MINT, pop(t, L[0] + 0.8), 24)
    chip(c, 950, 330, 'repayments: money erased', CORAL, pop(t, L[0] + 2.4), 24)
    c.text(640, 330, 'BANKS', 40, GOLD, 900, a=fade(t, 0.2))


def s_atm(c, x):
    t, L = x.t, x.L
    specks(c, t, 78)
    head(c, t, 'Where does cash fit in?')
    if t < L[1]:
        k = pop(t, L[0] + 0.5)
        c.icon('printer', 360, 270, 150 * clamp(k), SKY)
        c.text(360, 400, 'printed by the Treasury', 26, WHITE, 900, a=clamp(k))
        if t > L[0] + 4.2:
            fed_building(c, 920, 420, 0.9, clamp(pop(t, L[0] + 4.2)))
            c.text(920, 460, 'handed out by the Fed', 26, WHITE, 900, a=fade(t, L[0] + 4.2))
        return
    bal = 1000 - 100 * ease(clamp((t - L[1] - 3.6) / 0.8))
    phone_app(c, 330, 330, 1.2, t, f'${bal:,.0f}', clamp(pop(t, L[1] + 0.3)))
    k = pop(t, L[1] + 1.4)
    c.rrect(780, 160, 1080, 500, 20, (40, 46, 64), (255, 255, 255, 90), 3, a=clamp(k))
    c.rrect(820, 200, 1040, 300, 10, (90, 170, 230), a=clamp(k))
    c.text(930, 250, 'ATM', 34, INK, 900, a=clamp(k), shadow=False)
    c.rrect(840, 400, 1020, 418, 6, INK, a=clamp(k))
    if t > L[1] + 3.6:
        u = clamp((t - L[1] - 3.6) / 1.0)
        bill(c, 930, lerp(410, 520, ease(u)), 150, '100', a=clamp(u * 3))
    if t > L[2]:
        kk = pop(t, L[2] + 0.4)
        c.rrect(330, 585 - 30, 950, 585 + 30, 20, GOLD, a=clamp(kk))
        c.text(640, 585, 'same money, new form', 32, INK, 900, a=clamp(kk), shadow=False)
        pulse(c, t, (320, 545, 960, 625), GOLD, 24)



def s_books(c, x):
    t, L = x.t, x.L
    specks(c, t, 79)
    head(c, t, 'What US banks hold right now')
    compare_bars(c, t, [('Deposits (owes)', DEP_NOW, CORAL), ('Loans (owns)', LNS_NOW, MINT)], L[0] + 0.6, 3.0,
                 22, lambda v: f'${v:.1f}T', box=(330, 140, 950, 470), value_size=40, label_size=24)
    if t > L[1]:
        for j, lab in enumerate(('government bonds', 'other securities', 'reserves at the Fed')):
            chip(c, 280 + j * 360, 560, lab, SKY, pop(t, L[1] + 1.0 + 0.9 * j), 24)
    source(c, t, 'FRED: DPSACBW027SBOG, TOTLL (commercial banks)')


def s_m2(c, x):
    t, L = x.t, x.L
    specks(c, t, 68)
    head(c, t, 'How much money is there? (M2)')
    if t < L[2]:
        for i, (lab, at) in enumerate((('cash', 0.8), ('checking', 1.8), ('savings', 2.6), ('similar accounts', 3.4))):
            chip(c, 200 + i * 290, 150, lab, (SKY, MINT, GOLD, CREAM)[i], pop(t, L[0] + at), 24)
        if t > L[1]:
            v = M2_NOW * ease(clamp((t - L[1] - 0.6) / 1.6))
            c.text(640, 330, f'${v:.1f} trillion', 96, GOLD, 900, a=fade(t, L[1]), stroke=6)
            c.text(640, 420, f'M2, {M2_DATE:%B %Y}', 26, WHITE, 800, a=fade(t, L[1]))
        return
    if t < L[3]:  # cash vs everything else
        k = ease(clamp((t - L[2] - 0.4) / 1.2))
        c.rrect(200, 170, 200 + 880 * k, 270, 14, MINT)
        c.text(210, 140, f'M2: {tn(M2_NOW)}', 26, WHITE, 900, anchor='lm', a=fade(t, L[2]))
        kc = ease(clamp((t - L[2] - 1.8) / 1.0))
        c.rrect(200, 330, 200 + 880 * SHARE * kc, 430, 14, GOLD)
        c.text(210, 300, f'Cash: {tn(CASH_NOW)}', 26, WHITE, 900, anchor='lm', a=fade(t, L[2] + 1.8))
        if t > L[2] + 3.2:
            c.text(640, 520, f'{SHARE:.1%} is cash. About 1 dollar in 10.', 38, GOLD, 900, a=fade(t, L[2] + 3.2))
            pulse(c, t, (190, 320, 200 + 880 * SHARE + 12, 440), GOLD, 16)
        source(c, t, 'FRED: M2SL, WCURCIR')
        return
    k = clamp((t - L[3] - 0.3) / 5.0)
    px, py = line_chart(c, (130, 120, 1150, 540), M2X, M2Y, (1960, 2027), (0, 25), k, GOLD,
                        xticks=range(1960, 2030, 10), yticks=(0, 5, 10, 15, 20, 25), yfmt='${:.0f}T')
    if t > L[3] + 0.6:
        c.text(px(1960) + 16, py(M2_1960 / 1000) - 34, f'1960: ${M2_1960:.0f} billion', 22, WHITE, 800,
               anchor='lm', a=fade(t, L[3] + 0.6))
    if t > L[3] + 5.0:
        c.text(760, 330, f'{TIMES:.0f}x', 96, GOLD, 900, anchor='mm', a=fade(t, L[3] + 5.0), stroke=5)
    if t > L[4]:
        chip(c, 560, 250, 'most of it began as a loan', MINT, pop(t, L[4] + 2.8), 24)
    source(c, t, 'FRED: M2SL')


def s_limits(c, x):
    t, L = x.t, x.L
    specks(c, t, 69)
    head(c, t, 'So why not infinite money?')
    if t < L[2]:
        k = pop(t, L[0] + 1.0)
        c.text(640, 210, '?', int(160 * clamp(k)) + 1, GOLD, 900, a=clamp(k))
        if t > L[1]:
            c.text(640, 330, 'the reserve requirement', 44, WHITE, 900, a=fade(t, L[1] + 0.4))
            c.text(640, 385, 'a slice of deposits kept at the central bank', 24, MUTED, 800, a=fade(t, L[1] + 1.4))
        return
    k = pop(t, L[2] + 0.4, 0.3)
    s = lerp(1.8, 1.0, clamp(k))
    c.text(640, 280, '0%', int(200 * s), CORAL, 900, a=clamp(k), stroke=8)
    c.text(640, 420, 'US reserve requirement since March 2020', 30, WHITE, 900, a=fade(t, L[2] + 1.4))
    if len(L) > 3 and t > L[3]:
        chip(c, 640, 520, f'reserves banks hold anyway: about ${RES_NOW:.1f} trillion', MINT, pop(t, L[3] + 1.6), 26)
        pulse(c, t, (250, 488, 1030, 552), MINT, 30, on=t > L[3] + 1.9)
    source(c, t, 'Federal Reserve, effective March 26, 2020; FRED: TOTRESNS')


def s_four(c, x):
    t, L = x.t, x.L
    specks(c, t, 70)
    head(c, t, 'The real limits')
    items = [('user-check', 'Borrowers\nit trusts'), ('shield', 'Capital\n(own money)'), ('percent', 'Interest\nrates'),
             ('handshake', 'Confidence')]
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
            c.text(cx, 385 + j * 32, part, 26, WHITE if on else MUTED, 900, a=clamp(k))
        c.text(cx, 145, str(i + 1), 30, col, 900, a=clamp(k))
    notes = [(0, 1.8, 'a bad loan = the bank takes the loss', CORAL),
             (1, 1.8, "a cushion of shareholders' money", SKY),
             (2, 2.8, 'higher rates: fewer loans, less new money', SKY),
             (3, 1.6, 'your deposit is a promise', GOLD)]
    for i, at, txt, col in notes:
        nxt = L[i + 1] if i + 1 < len(L) else 1e9
        if L[i] + at <= t < nxt:
            chip(c, 640, 530, txt, col, pop(t, L[i] + at), 26)


def s_svb(c, x):
    t, L = x.t, x.L
    specks(c, t, 71)
    head(c, t, 'When the promise breaks: March 2023')
    bank(c, 640, 470, 1.3, 1.0, 'A BANK')
    n = int(clamp((t - L[0] - 0.5) / 12.0) * 16)
    for j in range(n):  # a growing crowd
        px = 140 + (j % 8) * 30 if j % 2 == 0 else 1140 - (j % 8) * 30
        person(c, px, 560 + (j // 8) * 10, 0.55, (SKY, MINT, CORAL, CREAM)[j % 4], t, j, 'sad')
    if L[1] < t < L[2]:
        chip(c, 1040, 160, 'long-term bonds', SKY, pop(t, L[1] + 0.8), 24)
        chip(c, 1040, 230, 'rates jumped: bonds lost value', CORAL, pop(t, L[1] + 3.6), 22)
    if t > L[2]:
        v = 42 * ease(clamp((t - L[2] - 1.0) / 1.5))
        kk = pop(t, L[2] + 1.0)
        c.rrect(860, 110, 1220, 250, 20, (20, 26, 42, 235), CORAL, 4, a=clamp(kk))
        c.text(1040, 165, f'${v:.0f} billion', 50, CORAL, 900, a=clamp(kk))
        c.text(1040, 220, 'pulled in one day: March 9', 22, WHITE, 800, a=clamp(kk))
        pulse(c, t, (850, 100, 1230, 260), CORAL)
    if t > L[2] + 6.0:
        k = pop(t, L[2] + 6.0, 0.3)
        s = lerp(1.7, 1.0, clamp(k))
        c.rrect(640 - 210 * s, 300 - 40 * s, 640 + 210 * s, 300 + 40 * s, 12, CORAL, a=clamp(k))
        c.text(640, 300, 'CLOSED: MARCH 10', int(40 * s), WHITE, 900, a=clamp(k), shadow=False)
    source(c, t, "Federal Reserve review of SVB, April 2023")


def s_fdic(c, x):
    t, L = x.t, x.L
    specks(c, t, 72)
    k = pop(t, L[0] + 0.3)
    c.icon('shield-check', 640, 220, 170 * clamp(k), MINT)
    if t > L[0] + 2.0:
        c.text(640, 380, '$250,000', 90, MINT, 900, a=fade(t, L[0] + 2.0), stroke=6)
    for j, (lab, at) in enumerate((('per depositor', 4.0), ('per bank', 4.8), ('per ownership type', 5.6))):
        chip(c, 300 + j * 340, 490, lab, SKY, pop(t, L[0] + at), 24)
    if t > L[1]:
        chip(c, 640, 570, 'know where your money stands', GOLD, pop(t, L[1] + 0.5), 24)
    source(c, t, 'FDIC deposit insurance')


def s_fed(c, x):
    t, L = x.t, x.L
    specks(c, t, 73)
    head(c, t, "The Federal Reserve's balance sheet")
    if t < L[1]:
        fed_building(c, 640, 470, 1.2, clamp(pop(t, L[0] + 0.3)))
        if t < L[0] + 7.5:
            chip(c, 640, 540, 'reserves: the money banks use to pay each other', SKY, pop(t, L[0] + 3.4), 24)
        else:
            chip(c, 640, 540, 'quantitative easing: buy bonds, pay with new reserves', GOLD, pop(t, L[0] + 7.5), 24)
            pulse(c, t, (250, 505, 1030, 575), GOLD, 30)
        return
    k = clamp((t - L[1] - 0.3) / 6.0)
    px, py = line_chart(c, (150, 130, 1150, 520), FX_, FY_, (2019, 2027), (0, 10), k, MINT,
                        xticks=range(2019, 2028), yticks=(0, 2, 4, 6, 8, 10), yfmt='${:.0f}T')
    if t > L[1] + 1.2:
        c.text(px(2020.2) + 10, py(FED_MAR20) + 40, f'Mar 2020: {tn(FED_MAR20)}', 22, WHITE, 800, anchor='lm',
               a=fade(t, L[1] + 1.2))
    if t > L[1] + 4.6:
        c.text(px(2022.3), py(FED_PEAK) - 30, f'Apr 2022: {tn(FED_PEAK)}', 24, GOLD, 900, a=fade(t, L[1] + 4.6))
    if t > L[2]:
        chip(c, 640, 590, 'plus stimulus checks, plus bank lending', CORAL, pop(t, L[2] + 0.4), 24)
    source(c, t, 'FRED: WALCL')


def s_flood(c, x):
    t, L = x.t, x.L
    specks(c, t, 74)
    if t < L[2]:
        head(c, t, 'M2, 2019 to now')
        k = clamp((t - L[0] - 0.3) / 4.0)
        px, py = line_chart(c, (150, 130, 1150, 520), MX19, MY19, (2019, 2027), (12, 25), k, GOLD,
                            xticks=range(2019, 2028), yticks=(12, 16, 20, 24), yfmt='${:.0f}T')
        if t > L[0] + 1.0:
            c.text(px(2020.1), py(M2_FEB20) + 36, f'Feb 2020: {tn(M2_FEB20)}', 22, WHITE, 800, anchor='lm',
                   a=fade(t, L[0] + 1.0))
        if t > L[0] + 3.8:
            c.text(px(2022.2), py(M2_PEAK) - 32, f'Mar 2022: {tn(M2_PEAK)}', 22, GOLD, 900, a=fade(t, L[0] + 3.8))
            c.text(1100, 180, f'+{M2_JUMP:.0f}%', 70, GOLD, 900, anchor='rm', a=fade(t, L[0] + 4.6), stroke=5)
        if t > L[1]:
            chip(c, 640, 590, f'Feb 2021: growing {YOY_MAX:.0f}% a year, fastest since 1960', CORAL,
                 pop(t, L[1] + 1.0), 24)
        source(c, t, 'FRED: M2SL')
        return
    head(c, t, 'Then came inflation')
    k = clamp((t - L[2] - 0.3) / 3.5)
    px, py = line_chart(c, (150, 130, 1150, 520), IX19, IY19, (2019, 2027), (0, 10), k, CORAL,
                        xticks=range(2019, 2028), yticks=(0, 2, 4, 6, 8, 10), yfmt='{:.0f}%')
    if t > L[2] + 3.0:
        c.text(px(2022.4), py(INFL_PEAK) - 32, f'June 2022: {INFL_PEAK:.0f}%', 26, CORAL, 900,
               a=fade(t, L[2] + 3.0))
    if t > L[3]:
        for j, (lab, col) in enumerate((('the money?', GOLD), ('supply chains?', SKY), ('energy?', MINT))):
            chip(c, 260 + j * 260, 585, lab, col, pop(t, L[3] + 1.0 + 0.8 * j), 24)
    source(c, t, 'FRED: CPIAUCSL, 12-month change')


def s_now(c, x):
    t, L = x.t, x.L
    specks(c, t, 75)
    head(c, t, 'Where things stand now')
    for j, (lab, val, col, at) in enumerate((('Fed balance sheet', tn(FED_NOW), MINT, 0.6),
                                            ('M2', tn(M2_NOW), GOLD, 2.4),
                                            ('Inflation', f'{INFL_NOW:.0f}%', CORAL, L[2] - L[0] + 0.4))):
        k = pop(t, L[0] + at)
        if k <= 0:
            continue
        cx = 240 + j * 400
        c.rrect(cx - 170, 180, cx + 170, 420, 24, (20, 26, 42), col, 3, a=clamp(k))
        c.text(cx, 240, lab, 26, WHITE, 900, a=clamp(k))
        c.text(cx, 330, val, int(42 * (0.7 + 0.3 * clamp(k))), col, 900, a=clamp(k))
    if L[1] < t < L[2]:
        chip(c, 640, 500, f'2023: M2 shrank, first yearly drops since 1960', GOLD, pop(t, L[1] + 0.8), 26)
        pulse(c, t, (470, 180, 810, 420), GOLD, 24)
    source(c, t, 'FRED: WALCL, M2SL, CPIAUCSL')


def s_you(c, x):
    t, L = x.t, x.L
    specks(c, t, 76)
    head(c, t, 'What it means for you (not advice)')
    items = [('lock', 'Your balance is a\npromise, insured\nto $250,000'), ('credit-card', 'Borrowing creates\nnew money: you\npay the interest'),
             ('trending-up', 'Fast money growth\ncan push\nprices up')]
    for i, (ic, lab) in enumerate(items):
        k = pop(t, L[i + 1] + 0.3)
        if k <= 0:
            continue
        cx = 230 + i * 410
        c.circle(cx, 240, 85 * clamp(k), (255, 255, 255, 20), GOLD, 3)
        if L[i + 1] <= t < (L[i + 2] if i + 2 < len(L) else 1e9):
            c.circle(cx, 240, 96 + 8 * math.sin(t * 5), None, GOLD, 3, a=0.4 + 0.4 * math.sin(t * 5))
        c.icon(ic, cx, 240, 80 * clamp(k), GOLD)
        for j, part in enumerate(lab.split('\n')):
            c.text(cx, 370 + j * 32, part, 24, WHITE, 800, a=clamp(k))
    if t < L[1]:
        k = pop(t, L[0] + 1.0)
        c.text(640, 300, '3', int(200 * (0.6 + 0.4 * clamp(k))), GOLD, 900, a=clamp(k), stroke=8)
    if t > L[3] + 3.0:
        chip(c, 640, 560, 'our inflation video shows how much', MINT, pop(t, L[3] + 3.0), 24)


def s_recap(c, x):
    t, L = x.t, x.L
    specks(c, t, 77)
    if t < L[1]:
        head(c, t, 'Recap')
        sp = max(2.0, (L[1] - L[0] - 1.5) / 5)
        rows = [('1 dollar in 10 is cash', 0.3), ('banks create money by lending', 0.3 + sp),
                ('repayments destroy it', 0.3 + 2 * sp), ('reserve requirement: 0%', 0.3 + 3 * sp),
                ('limits: borrowers, capital, rates, trust', 0.3 + 4 * sp)]
        for j, (txt, at) in enumerate(rows):
            k = pop(t, L[0] + at)
            if k <= 0:
                continue
            c.circle(300, 150 + j * 85, 22 * clamp(k), MINT)
            c.icon('check', 300, 150 + j * 85, 26 * clamp(k), INK, stroke=3)
            c.text(340, 150 + j * 85, txt, 32, WHITE, 900, anchor='lm', a=clamp(k))
            if j == 4 or t < L[0] + rows[j + 1][1]:
                pulse(c, t, (270, 150 + j * 85 - 36, 1010, 150 + j * 85 + 36), MINT, 30)
        return
    k = pop(t, L[1] + 0.3)
    c.text(640, 200, 'Did you know banks', 50, WHITE, 900, a=clamp(k))
    c.text(640, 265, 'create money when they lend?', 50, GOLD, 900, a=clamp(k))
    for j, (lab, col) in enumerate((('YES', MINT), ('NO', CORAL))):
        kk = pop(t, L[1] + 1.2 + 0.2 * j) * (1 + 0.06 * math.sin(t * 5 + j * 3) if t > L[1] + 2 else 1)
        cx = 520 + j * 240
        c.rrect(cx - 95, 360 - 45 * clamp(kk), cx + 95, 360 + 45 * clamp(kk), 22, col, a=clamp(kk))
        c.text(cx, 360, lab, int(46 * clamp(kk)) + 1, INK, 900, a=clamp(kk), shadow=False)
    if t > L[1] + 5.0:
        chip(c, 640, 480, 'Next: gold fell 23% from its record. What happened?', GOLD, pop(t, L[1] + 5.0), 24)
    penny(c, 1120, 520, 55, t, 'happy', wave=True, talk=x.talk())


SCENES = [
    dict(draw=s_hook, chapter='Intro: 1 dollar in 10', lead=0.15, gap=0.3, lines=[
        "!Only about one dollar in ten in America is actual cash.",
        "The other nine? They were typed into existence by banks, when they made loans.",
    ], punch=lambda L: [L[0] + 0.1, L[1] + 0.4], sfx=lambda L: [(L[0] + 0.1, 'hit'), (L[1] + 0.3, 'riser'),
                                                               (L[1] + 1.3, 'whoosh')]),
    dict(draw=s_promise, lines=[
        "That's not a conspiracy theory. The Bank of England said it in 2014. And once you see how it works, you'll "
        "never look at your bank balance the same way.",
        "In the next ten minutes: how a loan creates money, how paying it back destroys it, what stops banks from "
        "creating infinite money, and what it all means for you.",
    ], sfx=lambda L: [(L[0] + 0.4, 'pop'), (L[0] + 3.4, 'pop'), (L[1] + 0.6, 'pop'), (L[1] + 2.8, 'pop'),
                      (L[1] + 5.2, 'pop'), (L[1] + 6.9, 'pop')]),
    dict(draw=s_textbook, chapter='The textbook story', lines=[
        "Most of us learned a simple story. You put a hundred dollars in the bank. The bank keeps a little and "
        "lends the rest to someone else.",
        "In the textbook version, called the money multiplier, the bank keeps ten percent and lends out ninety. "
        "That ninety lands in another bank, which lends out eighty-one, and so on.",
        "It sounds neat. But in 2014, the Bank of England published a paper called Money creation in the modern "
        "economy, and it says that isn't how banks work in practice.",
        "!Banks don't wait for your deposit to make a loan. The loan makes the deposit.",
    ], punch=lambda L: [L[3] + 0.3], sfx=lambda L: [(L[0] + 0.5, 'pop'), (L[0] + 2.0, 'whoosh'), (L[0] + 4.6, 'pop')]
        + [(L[1] + 0.6 + 0.9 * i, 'tick') for i in range(8)] + [(L[2] + 0.2, 'whoosh'), (L[3] + 0.3, 'hit')]),
    dict(draw=s_maya, chapter='How a loan creates money', lines=[
        f"Let's watch it happen. Meet Maya. She wants to buy a house, and asks her bank for a {LOAN:,} dollar "
        "mortgage.",
        "The bank checks her income and her credit. Then it says yes.",
    ], sfx=lambda L: [(L[0] + 0.5, 'pop'), (L[0] + 1.2, 'pop'), (L[0] + 2.4, 'pop'), (L[0] + 3.6, 'pop'),
                      (L[1] + 0.5, 'tick'), (L[1] + 1.5, 'tick'), (L[1] + 2.8, 'ding')]),
    dict(draw=s_type, lines=[
        "Now here's the trick. The bank doesn't open a vault and hand her someone else's savings. It types "
        f"{LOAN:,} dollars into Maya's account.",
        f"On the bank's books, two lines appear. Something it owns: Maya owes the bank {LOAN:,} dollars. And "
        f"something it owes: the bank owes Maya {LOAN:,} dollars. That's her new deposit.",
        f"!The two lines balance. And {LOAN:,} dollars of brand-new money now exists that didn't exist a minute ago.",
    ], punch=lambda L: [L[2] + 0.4], sfx=lambda L: [(L[0] + 0.3, 'pop'), (L[0] + 2.4, 'down'), (L[0] + 4.0, 'pop')]
        + [(L[0] + 4.8 + 0.18 * i, 'tick') for i in range(8)] + [(L[1] + 1.0, 'pop'), (L[1] + 5.2, 'pop'),
                                                                 (L[2] + 0.4, 'hit')]),
    dict(draw=s_spend, lines=[
        "Maya pays the seller. The money moves from her bank to the seller's bank, but it doesn't disappear.",
        "It's now part of the money supply: money that you and I could end up holding.",
    ], sfx=lambda L: [(L[0] + 1.0, 'whoosh'), (L[0] + 3.5, 'pop'), (L[1] + 0.3, 'ding')]),
    dict(draw=s_destroy, chapter='Paying it back destroys money', lines=[
        "And here's the part almost nobody knows. When Maya repays her loan, that money is destroyed.",
        "Each payment cancels part of both lines. Her debt shrinks, and the deposit she paid with is gone.",
        "The interest is different. That's the bank's income. It pays salaries, it pays savers, and the rest is "
        "profit.",
    ], sfx=lambda L: [(L[0] + 1.5, 'down'), (L[1] + 0.8, 'riser'), (L[2] + 0.3, 'pop'), (L[2] + 2.0, 'pop'),
                      (L[2] + 2.6, 'pop'), (L[2] + 3.2, 'pop')]),
    dict(draw=s_spread, lines=[
        f"And that interest adds up. In late October, the average 30-year mortgage rate was about "
        f"{MORT_NOW:.1f} percent.",
        f"At that rate, Maya's {LOAN:,} dollar loan costs about {PAY:,.0f} dollars a month. Over thirty years, she "
        f"pays back about {round(TOTAL / 1000)} thousand dollars, and about {round(INTEREST / 1000)} thousand of "
        "that is interest.",
        f"Meanwhile, the average savings account pays about {SAVE_NOW:.2f} percent a year. That gap, between what "
        "banks charge borrowers and what they pay savers, is a big part of how banks make money.",
    ], punch=lambda L: [L[1] + 4.6], sfx=lambda L: [(L[0] + 0.5, 'pop'), (L[0] + 1.5, 'pop'), (L[1] + 0.3, 'hit'),
                                                    (L[1] + 3.0, 'whoosh'), (L[1] + 4.6, 'ding'), (L[2] + 0.3, 'pop'),
                                                    (L[2] + 3.0, 'pop')]),
    dict(draw=s_cycle, lines=[
        "So money is always being born and destroyed. New loans create it. Repayments erase it.",
    ], sfx=lambda L: [(L[0] + 0.8, 'pop'), (L[0] + 2.4, 'pop')]),
    dict(draw=s_atm, chapter='Where cash fits in', lines=[
        "So where does physical cash come in? In the US, paper money is printed by the Treasury, and the Federal "
        "Reserve hands it out to banks.",
        "But cash only reaches you when you take it out of your account. Withdraw a hundred dollars from an ATM, "
        "and your bank balance drops by a hundred.",
        "!No new money was created. It just changed form: from a number on a screen to paper in your hand.",
    ], sfx=lambda L: [(L[0] + 0.5, 'pop'), (L[0] + 4.2, 'pop'), (L[1] + 0.3, 'pop'), (L[1] + 1.4, 'pop'),
                      (L[1] + 3.6, 'whoosh'), (L[2] + 0.4, 'ding')]),
    dict(draw=s_m2, chapter='How much money is there?', lines=[
        "So how much money is out there? In the US, the broad measure is called M2: cash, plus checking and "
        "savings accounts, plus a few similar accounts.",
        f"In {M2_DATE:%B %Y}, M2 was about {M2_NOW:.1f} trillion dollars.",
        f"Physical cash in circulation? About {CASH_NOW:.1f} trillion. That's the one dollar in ten.",
        f"In 1960, M2 was about {M2_1960:.0f} billion dollars. Today, it's more than seventy times bigger.",
        "The economy and prices grew a lot over those decades too. But most of that money was created the same way "
        "Maya's was: by banks making loans.",
    ], punch=lambda L: [L[1] + 1.2], sfx=lambda L: [(L[0] + 0.8, 'pop'), (L[0] + 1.8, 'pop'), (L[0] + 2.6, 'pop'),
                                                    (L[0] + 3.4, 'pop'), (L[1] + 0.6, 'riser'), (L[1] + 2.2, 'hit'),
                                                    (L[2] + 0.4, 'whoosh'), (L[2] + 3.2, 'ding'),
                                                    (L[3] + 0.3, 'whoosh'), (L[3] + 5.0, 'hit'), (L[4] + 2.8, 'pop')]),
    dict(draw=s_books, lines=[
        f"Right now, US commercial banks hold about {DEP_NOW:.1f} trillion dollars of deposits, and about "
        f"{LNS_NOW:.1f} trillion dollars of loans.",
        "Most of the rest of what they own is government bonds, other securities, and reserves at the Fed.",
    ], sfx=lambda L: [(L[0] + 0.6, 'pop'), (L[0] + 2.1, 'pop'), (L[1] + 1.0, 'pop'), (L[1] + 1.9, 'pop'),
                      (L[1] + 2.8, 'pop')]),
    dict(draw=s_limits, chapter='What stops banks?', lines=[
        "So if banks can type money into existence, why don't they create infinite amounts?",
        "You might think it's the reserve requirement: the rule that banks must keep a slice of their deposits at "
        "the central bank.",
        "!In the US, that requirement has been zero since March 2020.",
        f"Banks still hold about {RES_NOW:.0f} trillion dollars of reserves anyway, because they need cash on hand "
        "to pay each other and their customers. So the requirement isn't what holds them back.",
    ], punch=lambda L: [L[2] + 0.4], sfx=lambda L: [(L[0] + 1.0, 'pop'), (L[1] + 0.4, 'whoosh'), (L[2] + 0.3, 'riser'),
                                                    (L[2] + 0.4, 'hit'), (L[3] + 1.6, 'pop')]),
    dict(draw=s_four, lines=[
        "The real limits are different. Limit one: borrowers. A bank needs people it trusts to pay it back. When a "
        "borrower can't pay, the bank takes the loss.",
        "Limit two: capital. Regulators make banks fund part of their loans with their own money, the "
        "shareholders' money, as a cushion against losses.",
        "Limit three: interest rates. The Federal Reserve sets the rate that ripples through every loan. When rates "
        "go up, borrowing gets expensive, fewer people borrow, and less new money gets created.",
        "And limit four: confidence. Your deposit is a promise. If too many people want that promise paid at once, "
        "a bank can run out of cash.",
    ], sfx=lambda L: [(L[i] + 0.3, 'pop') for i in range(4)] + [(L[0] + 1.8, 'pop'), (L[1] + 1.8, 'pop'),
                                                               (L[2] + 2.8, 'pop'), (L[3] + 1.6, 'pop')]),
    dict(draw=s_svb, chapter='When the promise breaks', lines=[
        "That's exactly what happened to Silicon Valley Bank in March 2023.",
        "The bank had put a lot of its customers' money into long-term bonds. When interest rates jumped, those "
        "bonds lost value, and when customers heard, they rushed to get their money out.",
        "On March 9, customers tried to pull out 42 billion dollars in a single day, according to the Federal "
        "Reserve's own review. The next day, the bank was shut down.",
    ], punch=lambda L: [L[2] + 1.0, L[2] + 6.0], sfx=lambda L: [(L[0] + 0.5, 'riser'), (L[1] + 0.8, 'pop'),
                                                               (L[1] + 3.6, 'down'), (L[2] + 1.0, 'hit'),
                                                               (L[2] + 6.0, 'down')]),
    dict(draw=s_fdic, lines=[
        "That's why the US has deposit insurance. The FDIC covers up to 250,000 dollars per depositor, per bank, "
        "for each type of account ownership.",
        "Most people's money sits well under that limit. But it's worth knowing the rule.",
    ], sfx=lambda L: [(L[0] + 0.3, 'pop'), (L[0] + 2.0, 'ding'), (L[0] + 4.0, 'pop'), (L[0] + 4.8, 'pop'),
                      (L[0] + 5.6, 'pop'), (L[1] + 0.5, 'pop')]),
    dict(draw=s_fed, chapter='The Fed and the 2020 money flood', lines=[
        "So where does the Federal Reserve come in? The Fed creates a different kind of money: reserves, the money "
        "banks use to pay each other. It mostly does this by buying government bonds and mortgage bonds, and paying "
        "for them with brand-new reserves. That's called quantitative easing.",
        f"In March 2020, as the pandemic hit, the Fed's balance sheet was about {FED_MAR20:.1f} trillion dollars. "
        "By April 2022, it had more than doubled, to almost 9 trillion.",
        "At the same time, the government sent out stimulus, banks kept lending, and deposits poured in.",
    ], sfx=lambda L: [(L[0] + 0.3, 'pop'), (L[0] + 3.4, 'pop'), (L[1] + 0.3, 'whoosh'), (L[1] + 4.6, 'hit'),
                      (L[2] + 0.4, 'pop')]),
    dict(draw=s_flood, lines=[
        f"From February 2020 to March 2022, M2 jumped about {M2_JUMP:.0f} percent, from {M2_FEB20:.1f} to "
        f"{M2_PEAK:.1f} trillion dollars.",
        f"In February 2021, it was growing almost {YOY_MAX:.0f} percent a year: the fastest pace in data going "
        "back to 1960.",
        f"!And what came next? Inflation hit about {INFL_PEAK:.0f} percent in June 2022, the highest in about "
        "four decades.",
        "Economists still argue about how much of that was the money, and how much was supply chains and energy. "
        "But the timing is hard to ignore.",
    ], punch=lambda L: [L[0] + 4.6, L[2] + 3.0], sfx=lambda L: [(L[0] + 0.3, 'whoosh'), (L[0] + 4.6, 'hit'),
                                                               (L[1] + 1.0, 'pop'), (L[2] + 0.3, 'whoosh'),
                                                               (L[2] + 3.0, 'hit'), (L[3] + 1.0, 'pop'),
                                                               (L[3] + 1.8, 'pop'), (L[3] + 2.6, 'pop')]),
    dict(draw=s_now, lines=[
        f"Since then, the Fed has shrunk its balance sheet to about {FED_NOW:.1f} trillion dollars, and M2 is "
        f"about {M2_NOW:.1f} trillion.",
        "And something rare happened as interest rates rose. From December 2022 to early 2024, M2 was smaller "
        "than a year before: the first yearly drops in data going back to 1960. Fewer new loans, more "
        "repayments, so money was destroyed faster than it was created.",
        f"And inflation today is about {INFL_NOW:.0f} percent.",
    ], sfx=lambda L: [(L[0] + 0.6, 'pop'), (L[0] + 2.4, 'pop'), (L[1] + 0.8, 'down'), (L[2] + 0.4, 'pop')]),
    dict(draw=s_you, chapter='What it means for you', lines=[
        "So what does all this mean for you? Three things. This isn't financial advice, just how the system "
        "works.",
        "One: the money in your bank account is a promise from your bank, insured up to 250,000 dollars. That's "
        "why the limit matters.",
        "Two: when you borrow, you're not borrowing someone else's savings. You're creating new money, and the "
        "interest you pay is how the bank earns from it.",
        "Three: when new money is created faster than the economy grows, prices can rise, and cash sitting still "
        "slowly loses value. Our inflation video shows exactly how much.",
    ], sfx=lambda L: [(L[0] + 1.0, 'pop'), (L[1] + 0.3, 'pop'), (L[2] + 0.3, 'pop'), (L[3] + 0.3, 'pop'),
                      (L[3] + 3.0, 'pop')]),
    dict(draw=s_recap, chapter='Recap', tail=0.6, lines=[
        "Let's recap. Only about one dollar in ten is cash. Banks create most money by making loans, and "
        "repayments destroy it. The reserve requirement is zero, so what really limits banks is borrowers, "
        "capital, interest rates, and trust.",
        "!So here's my question: did you know banks create money when they lend? Yes or no, tell me in the "
        "comments. And subscribe, because on Monday we look at gold: down 23 percent from its record. What "
        "happened?",
        "This video is for education only. It's not financial advice.",
    ], punch=lambda L: [L[1] + 0.3], sfx=lambda L: [(L[0] + 0.3 + max(2.0, (L[1] - L[0] - 1.5) / 5) * j, 'pop') for j in range(5)]
        + [(L[1] + 0.3, 'ding'), (L[1] + 1.2, 'pop'), (L[1] + 1.4, 'pop'), (L[1] + 5.0, 'pop')]),
]
SHORTS = {}


def check_numbers():
    script = ' '.join(l for sc in SCENES for l in sc['lines'])
    assert 0.09 < SHARE < 0.115 and 'one dollar in ten' in script, SHARE
    assert round(M2_NOW, 1) == 23.4 and round(CASH_NOW, 1) == 2.5 and M2_DATE.strftime('%Y-%m') == '2026-09'
    assert round(M2_1960) == 304 and 70 < TIMES < 80 and 'more than seventy times' in script
    assert round(M2_FEB20, 1) == 15.5 and round(M2_PEAK, 1) == 21.8 and M2_PEAK_DATE.strftime('%Y-%m') == '2022-03'
    assert round(M2_JUMP) == 41 or round(M2_JUMP) == 40, M2_JUMP
    assert YOY_MAX_DATE.strftime('%Y-%m') == '2021-02' and round(YOY_MAX) == 27 and 'back to 1960' in script
    assert round(FED_MAR20, 1) == 4.2 and 8.9 < FED_PEAK < 9.0 and FED_PEAK_DATE.strftime('%Y-%m') == '2022-04'
    assert FED_PEAK / FED_MAR20 > 2 and 'more than doubled, to almost 9 trillion' in script
    assert round(FED_NOW, 1) == 6.7 and round(INFL_NOW) == 4
    assert round(MORT_NOW, 2) == 7.32 and round(SAVE_NOW, 2) == 0.38 and round(PAY) == 2061, (MORT_NOW, PAY)
    assert round(TOTAL / 1000) == 742 and round(INTEREST / 1000) == 442, (TOTAL, INTEREST)
    assert NEG.index[0].strftime('%Y-%m') == '2022-12' and NEG.index[-1].strftime('%Y-%m') == '2024-02'
    assert 'back to 1960' in script and 'From December 2022 to early 2024' in script
    assert round(DEP_NOW, 1) == 19.8 and round(LNS_NOW, 1) == 14.2 and round(RES_NOW) == 3 and round(RES_NOW, 1) == 3.0
    assert INFL_PEAK_DATE.strftime('%Y-%m') == '2022-06' and round(INFL_PEAK) == 9
    assert INFL_PREV.year == 1981 and 'about four decades' in script, INFL_PREV
    for s in ('Bank of England', '2014', 'zero since March 2020', '42 billion', 'March 9', '250,000',
              'not financial advice', "It's not financial advice", '23 percent'):
        assert s in script, s
    print(f'numbers check: OK  M2 {tn(M2_NOW)} ({M2_DATE:%b %Y}), cash {tn(CASH_NOW)} = {SHARE:.1%}; '
          f'1960 ${M2_1960:.0f}B -> {TIMES:.0f}x; M2 +{M2_JUMP:.1f}% Feb20-Mar22, yoy max {YOY_MAX:.1f}% '
          f'({YOY_MAX_DATE:%b %Y}); Fed {FED_MAR20:.2f} -> {FED_PEAK:.2f} -> {FED_NOW:.2f}T; CPI peak '
          f'{INFL_PEAK:.1f}% (last higher {INFL_PREV:%b %Y}), now {INFL_NOW:.1f}%; deposits ${DEP.iloc[-1] / 1000:.1f}T, '
          f'loans ${LNS.iloc[-1] / 1000:.1f}T')


if __name__ == '__main__':
    check_numbers()
    os.makedirs(BUILD, exist_ok=True)
    if '--stills' in sys.argv:
        previews(SCENES, SHORTS, os.path.join(BUILD, 'previews'))
        sys.exit()
    only = [int(a) for a in sys.argv[sys.argv.index('--only') + 1].split(',')] if '--only' in sys.argv else None
    total, chapters = build(SCENES, os.path.join(OUT, 'ep06_banks.mp4'), BUILD, only=only,
                            srt_path=os.path.join(OUT, 'ep06_banks.en.srt'))
    with open(os.path.join(OUT, 'ep06_chapters.txt'), 'w') as f:
        for at, name in chapters:
            f.write(f'{fmt_time(at)} {name}\n')
    print(f'total {total / 60:.1f} min')
