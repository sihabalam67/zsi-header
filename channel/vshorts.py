"""Native vertical (9:16) versions of the Shorts made for weeks 1-2, which were 16:9 scenes in a band.

    python3 channel/vshorts.py ep03_short_jump [--stills]

Same lines, timing and sound effects as the original Short (from the episode's SHORTS), drawn for a 720 x 1280
canvas. Rebuilds use the voice and audio style each episode was made with, so the narration matches its long video:
ep01-ep04 Kokoro af_heart + classic music, ep05 Chatterbox + upgraded audio. Writes channel/out/<name>.mp4; then
swap the uploaded copy with `python3 youtube/replace_short.py <name>`.
"""
import importlib
import os
import sys

NAME = next(a for a in sys.argv[1:] if not a.startswith('-'))
EPN = NAME.split('_')[0]
if EPN in ('ep01', 'ep02', 'ep03', 'ep04'):
    os.environ.setdefault('VOICE_ENGINE', 'kokoro')
    os.environ.setdefault('AUDIO_STYLE', 'classic')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.argv = [sys.argv[0]] + [a for a in sys.argv[1:] if a.startswith('-')]  # episode modules read sys.argv

from wk2_art import *  # noqa: E402,F401,F403
from engine import build, line_chart, previews  # noqa: E402

E = importlib.import_module({'ep01': 'ep01_inflation', 'ep02': 'ep02_housing', 'ep03': 'ep03_gas',
                             'ep04': 'ep04_fed', 'ep05': 'ep05_jobs'}[EPN])


def title(c, t, text, sub=None, y=205):
    c.text(360, y, text, 34, WHITE, 900, a=fade(t, 0))
    if sub:
        c.text(360, y + 42, sub, 22, MUTED, 600, a=fade(t, 0.1), shadow=False)


def mark(c, t, px, py, xx, v, lab, col, at, above=True, dx=0):
    """Dot on a chart point with a value label in a pill, kept inside the frame."""
    kk = pop(t, at)
    if kk <= 0:
        return
    c.circle(px(xx), py(v), 12 * kk, col, WHITE, 3)
    w = max(170, len(lab) * 17 + 40)
    bx = min(max(px(xx) + dx, w / 2 + 12), 720 - w / 2 - 12)
    y = py(v) - 57 if above else py(v) + 57
    c.rrect(bx - w / 2, y - 25, bx + w / 2, y + 25, 18, col, a=clamp(kk))
    c.text(bx, y, lab, 28, INK, 800, a=clamp(kk), shadow=False)


# ------------------------------------------------------------------ ep03 gas --
def v03_hook(c, x):
    t, L = x.t, x.L
    specks(c, t, 31, 50)
    g1 = ease(seg(t, L[1], L[1] + 1.6))
    g2 = ease(seg(t, L[1] + 2.4, L[1] + 3.6))
    price = lerp(E.G_LOW, E.G_PEAK, g1) if g2 == 0 else lerp(E.G_PEAK, E.G_NOW, g2)
    lab = 'January 2026' if g1 < 0.5 else ('May 2026' if g2 < 0.5 else 'today')
    chip(c, 360, 215, lab, GOLD, pop(t, L[0] + 0.4), 30)
    gas_pump(c, 340, 770, 1.95, E.money(price), color=mix(MINT, CORAL, g1))
    c.ellipse(390, 778, 230, 16, (0, 0, 0, 60))
    penny(c, 95, 720, 56, t, 'shocked' if t > L[1] + 1.6 else 'happy', look=(1, 0), talk=x.talk())
    if t > L[2]:
        k = pop(t, L[2] + 0.4)
        c.rrect(150, 815, 570, 905, 22, (255, 255, 255, 22), CORAL, 3, a=clamp(k))
        c.text(360, 860, f'+{E.money(E.EXTRA)} every gallon', 34, CORAL, 900, a=clamp(k))


def v03_oil(c, x):
    t, L = x.t, x.L
    title(c, t, 'US crude oil, price per barrel', '2026 (WTI)')
    k = ease(seg(t, L[1], x.E[-1]))
    px, py = line_chart(c, (120, 330, 640, 820), E.O_X, E.O_Y, (2026.0, E.O_X[-1] + 0.02), (0, 130), k, CORAL,
                        yticks=range(0, 131, 25), yfmt='${:.0f}', a=fade(t, 0.1), width=5, tick_size=24)
    for i, mth in enumerate(('Jan', 'Mar', 'May', 'Jul', 'Sep', 'Nov')):
        c.text(px(2026 + 2 * i / 12 + 0.04), 850, mth, 22, MUTED, 600, a=fade(t, 0.1), shadow=False)
    mark(c, t, px, py, E.O_X[E.O_Y.index(E.O_LOW)], E.O_LOW, f'${E.O_LOW:.0f}', MINT, L[1] + 0.5, above=False)
    mark(c, t, px, py, E.O_X[E.O_Y.index(E.O_PEAK)], E.O_PEAK, f'${E.O_PEAK:.0f}', CORAL, L[2] + 0.5)
    mark(c, t, px, py, E.O_X[-1], E.O_NOW, f'today ${E.O_NOW:.0f}', GOLD, L[-1] + 2.5, above=False)
    source_v(c, t, 'EIA via FRED (DCOILWTICO)')


def v03_barrel(c, x):
    t, L = x.t, x.L
    specks(c, t, 33, 50)
    barrel(c, 360, 390, 1.25, f'1 barrel = ${E.O_NOW:.0f}')
    if t > L[1]:
        k = ease(seg(t, L[1], L[1] + 1.5))
        n = int(42 * k)
        for i in range(n):
            c.icon('fuel', 74 + (i % 14) * 44, 490 + (i // 14) * 46, 30, SKY)
        c.text(360, 650, f'{n} gallons', 40, SKY, 900)
        c.text(360, 700, f'crude = {E.money(E.CRUDE_GAL)} per gallon', 32, WHITE, 800, a=fade(t, L[1] + 2))
    if t > L[2]:
        g = ease(seg(t, L[2], L[2] + 1.2))
        x0, x1, y0 = 60, 660, 745
        c.rrect(x0, y0, x1, y0 + 54, 14, (255, 255, 255, 25))
        c.rrect(x0, y0, x0 + (x1 - x0) * E.CRUDE_SHARE / 100 * g, y0 + 54, 14, CORAL)
        c.text(x0 + (x1 - x0) * E.CRUDE_SHARE / 200, y0 + 27, f'crude oil {E.CRUDE_SHARE:.0f}%', 24, INK, 900,
               a=g, shadow=False)
        c.text(x0 + (x1 - x0) * (0.5 + E.CRUDE_SHARE / 200), y0 + 27, 'the rest', 22, WHITE, 800,
               a=fade(t, L[3]), shadow=False)
        c.text(360, y0 + 84, 'refining, shipping, station, taxes', 22, MUTED, 700, a=fade(t, L[3]), shadow=False)
    if t > L[4]:
        chip(c, 360, 880, 'Federal gas tax: 18.4 cents since 1993', GOLD, pop(t, L[4] + 0.3), 22)


def v03_feathers(c, x):
    t, L = x.t, x.L
    specks(c, t, 35, 50)
    title(c, t, 'Change per gallon, 2026', y=200)
    if t < L[1]:
        penny(c, 360, 540, 110, t, 'worried', talk=x.talk())
        return
    rk = pop(t, L[3] + 0.3)
    c.text(360, 275, 'On the way UP (Jan to spring)', 26, CORAL, 900, a=fade(t, L[1]))
    compare_bars(c, t, [('oil (per gallon)', E.UP_CRUDE, SKY), ('pump price', E.UP_GAS, CORAL)], L[1] + 0.3,
                 2.0, 2.0, lambda v: f'+${v:.2f}', box=(90, 330, 630, 520), value_size=40, label_size=22)
    if rk > 0:
        c.icon('rocket', 655, 275, 50 * rk, CORAL, stroke=2.5)
    if t > L[2]:
        c.text(360, 615, 'On the way DOWN (spring to July)', 26, MINT, 900, a=fade(t, L[2]))
        compare_bars(c, t, [('oil (per gallon)', E.DN_CRUDE, SKY), ('pump price', E.DN_GAS, MINT)], L[2] + 0.3,
                     2.0, 2.0, lambda v: f'-${v:.2f}', box=(90, 670, 630, 825), value_size=40, label_size=22)
        if rk > 0:
            c.icon('feather', 670, 615, 50 * rk, MINT, stroke=2.5)
    source_v(c, t, 'EIA via FRED; a barrel holds 42 gallons')


# ------------------------------------------------------------------ ep04 fed --
def v04_why(c, x):
    t, L = x.t, x.L
    specks(c, t, 54, 50)
    if t < L[2]:
        barrel(c, 215, 700, 1.6, 'oil shock', a=fade(t, 0.2))
        gas_pump(c, 500, 720, 1.2, '$4.27', a=fade(t, L[1]))
        return
    if t < L[3]:
        title(c, t - L[2], 'Inflation vs the Fed\'s 2% target', y=210)
        compare_bars(c, t, (('target', 2.0, MINT), ('Feb 2026', E.CPI_FEB, GOLD), ('Sep 2026', E.CPI_NOW, CORAL)),
                     L[2] + 0.3, 3.0, 5, lambda v: f'{v:.1f}%', box=(60, 320, 660, 800), value_size=44,
                     label_size=24)
        source_v(c, t, 'BLS CPI (CPIAUCSL) via FRED')
        return
    if t < L[4]:
        steps = (('percent', 'Higher\nrates'), ('shopping-cart', 'Less borrowing\n& spending'),
                 ('trending-down', 'Prices\ncool'))
        icon_row(c, t, steps, L[3], max(1.0, L[4] - L[3]), y=520, x0=0, width=720, ring=88, size=78,
                 label_size=26)
        return
    barrel(c, 360, 600, 1.9)
    k = pop(t, L[4] + 1)
    c.line([(230, 330), (490, 620)], CORAL, 12, a=clamp(k))
    c.text(360, 740, 'Rates can\'t make oil.', 40, WHITE, 900, a=fade(t, L[4] + 0.5))
    c.text(360, 800, 'They can only slow spending.', 32, GOLD, 800, a=fade(t, L[4] + 2.5))


def v04_cards(c, x):
    t, L = x.t, x.L
    specks(c, t, 56, 50)
    card(c, 360, 330, 1.4, a=fade(t, 0), color=SKY)
    if L[1] < t < L[4]:
        chip(c, 360, 510, 'variable rate = moves with prime', GOLD, pop(t, L[1] + 0.3), 24)
    if t > L[4]:
        chip(c, 360, 510, f'this hike: +0.25% = +${E.QUARTER:.2f}/yr', GOLD, pop(t, L[4] + 0.3), 26)
    if t > L[2]:
        compare_bars(c, t, (('prime rate', E.P_NOW, GOLD), ('avg card rate', E.CC_NOW, CORAL)), L[2] + 0.5, 2.5,
                     25, lambda v: f'{v:.1f}%', box=(110, 580, 610, 770), value_size=42, label_size=24)
    if t > L[3]:
        k = pop(t, L[3] + 0.3)
        c.rrect(30, 850, 690, 910, 18, (14, 22, 40, 230), CORAL, 3, a=clamp(k))
        c.text(360, 880, f'$5,000 balance = about ${round(E.CC_COST, -1):,.0f} interest a year', 25, WHITE, 900,
               a=clamp(k))
    elif t > L[2]:
        source_v(c, t, 'Federal Reserve via FRED')


def v04_savings(c, x):
    t, L = x.t, x.L
    specks(c, t, 58, 50)
    c.icon('piggy-bank', 360, 350, 180, MINT, a=fade(t, 0))
    if t > L[1]:
        dial(c, 190, 620, 120, E.S_NOW, 5, f'savings: {E.pct(E.S_NOW)}', a=fade(t, L[1]), color=MINT)
        dial(c, 530, 620, 120, E.CPI_NOW, 5, f'inflation: {E.CPI_NOW:.1f}%', a=fade(t, L[1] + 1.5), color=CORAL)
    if L[2] < t < L[4]:
        chip(c, 360, 790, f'losing about {E.REAL_LOSS:.1f}% a year', CORAL, pop(t, L[2] + 0.3), 30)
    if t > L[4]:
        k = pop(t, L[4] + 0.5)
        c.rrect(20, 760, 700, 860, 18, (14, 22, 40, 230), GOLD, 3, a=clamp(k))
        c.text(360, 792, f'$10,000 at {E.pct(E.S_NOW)} earns ${E.EF_NOW:.0f} a year', 26, WHITE, 900, a=clamp(k))
        c.text(360, 830, f'at 3.5% it earns ${E.EF_ALT:.0f}', 26, GOLD, 900, a=clamp(k))
    if t > L[5]:
        chip(c, 360, 205, 'CD: lock in a rate', GOLD, pop(t, L[5] + 0.3), 24)
    source_v(c, t, 'FDIC (SNDR), BLS CPI via FRED')


# ------------------------------------------------------------ ep01 inflation --
def v01_hook(c, x):
    t, L = x.t, x.L
    specks(c, t, 1, 50)
    mk = fade(t, 0.1)
    c.rrect(90, 650, 630, 730, 28, (90, 104, 160), (60, 70, 120), 4, a=mk)
    c.rrect(100, 618, 620, 668, 24, CREAM, (200, 196, 186), 3, a=mk)
    k_in = ease(seg(t, L[0] + 1.6, L[0] + 2.8))
    k_out = ease(seg(t, L[1] + 2.0, L[1] + 3.0))
    shrink = ease(seg(t, L[2] + 1.4, L[2] + 3.0))
    bx = lerp(lerp(400, 360, k_in), 360, k_out)
    by = lerp(lerp(450, 650, k_in), 440, k_out)
    if k_in < 1 or k_out > 0:
        bill(c, bx, by, 330 * lerp(1, 0.55, shrink), '100', tint=0.35 * shrink)
    if k_in > 0.9 and k_out < 0.05:
        c.rrect(90, 650, 630, 730, 28, (90, 104, 160), (60, 70, 120), 4)
    if t > L[1] - 0.2:
        yk = ease(seg(t, L[1], L[1] + 2.0))
        c.icon('calendar', 250, 245, 56, GOLD, a=fade(t, L[1] - 0.2))
        c.text(390, 245, str(int(lerp(1970, 2026, yk))), 84, GOLD, 900, a=fade(t, L[1] - 0.2))
    ck = pop(t, L[2] + 2.2)
    if ck > 0:
        c.rrect(170, 765, 550, 905, 22, (255, 255, 255, 18), MUTED, 2, a=clamp(ck))
        c.text(360, 795, 'buys what', 24, MUTED, 600, a=clamp(ck))
        c.text(360, 842, '$12', 58, CORAL, 900, a=clamp(ck))
        c.text(360, 885, 'bought in 1970', 22, MUTED, 600, a=clamp(ck))
    mood = 'happy' if t < L[2] + 1.4 else 'worried'
    if t > L[3]:
        mood = 'shocked'
    penny(c, 120, 470, 62, t, mood, look=(1, 0), wave=t < L[0] + 1.2, talk=x.talk())
    for i in range(8):
        k = seg(t, L[3] + 0.2 + i * 0.08, L[3] + 1.6 + i * 0.08)
        if 0 < k < 1:
            c.circle(360 + i * 22 * k + 120 * k, 440 - 200 * ease(k) + i * 6, 14, GOLD, GOLD_D, 2, a=1 - k)
    c.text(530, 345, '-$88 ?', 48, CORAL, 900, a=fade(t, L[3] + 0.4))


def v01_prices(c, x):
    t, L, Ev = x.t, x.L, x.E
    specks(c, t, 10, 50)
    c.text(360, 200, 'Average US prices', 34, WHITE, 900, a=fade(t, 0))
    c.text(360, 238, '1980 vs today', 24, MUTED, 700, a=fade(t, 0), shadow=False)
    span = Ev[1] - L[1]
    for i, (icon, label, unit, p0, p1) in enumerate(E.PRICES):
        cx, top = 200 + (i % 2) * 320, 270 + (i // 2) * 300
        k = pop(t, L[0] + 1.2 + i * 0.25)
        if k <= 0:
            continue
        a = clamp(k)
        c.rrect(cx - 150, top, cx + 150, top + 285, 24, (255, 255, 255, 16), (255, 255, 255, 50), 2, a=a)
        c.icon(icon, cx - 85, top + 52, 56, GOLD, a=a)
        c.text(cx + 30, top + 42, label, 28, WHITE, 900, a=a)
        c.text(cx + 30, top + 74, unit, 18, MUTED, 600, a=a)
        c.text(cx, top + 122, f'1980: {E.money(p0)}', 28, MINT, 900, a=a)
        rk = ease(seg(t, L[1] + span * (0.25 * i + 0.08), L[1] + span * (0.25 * i + 0.22)))
        c.text(cx, top + 165, 'today', 20, MUTED, 700, a=a)
        c.text(cx, top + 210, E.money(lerp(p0, p1, rk)), 46, CORAL, 900, a=a)
        mk = pop(t, L[1] + span * (0.25 * i + 0.22))
        if mk > 0:
            c.rrect(cx - 55, top + 238, cx + 55, top + 274, 18, CORAL, a=clamp(mk))
            c.text(cx, top + 256, f'x{p1 / p0:.1f}', 22, INK, 900, a=clamp(mk), shadow=False)
    source_v(c, t, 'BLS average price data via FRED')


def v01_wages(c, x):
    t, L = x.t, x.L
    if t < L[1] - 0.2:
        specks(c, t, 12, 50)
        penny(c, 330, 560, 110, t, 'happy', talk=x.talk(), look=(0, 0))
        c.icon('briefcase', 520, 410, 90, SKY, a=fade(t, 0.3))
        return
    title(c, t - L[1] + 0.2, 'Average hourly pay, US', 'non-manager workers')
    kn = ease(seg(t, L[1], L[1] + 4))
    kr = ease(seg(t, L[2] + 2.5, L[2] + 6.5))
    px, py = line_chart(c, (120, 380, 650, 800), E.WAGE_X, E.WAGE_Y, (1964, 2026.75), (0, 40), kn, SKY,
                        xticks=range(1970, 2030, 10), yticks=range(0, 41, 10), yfmt='${:.0f}', a=fade(t, L[1]),
                        width=5, tick_size=22)
    if kn > 0.98:
        near = min(E.WAGE_X, key=lambda v: abs(v - 2008))
        c.text(px(2008), py(E.WAGE_Y[E.WAGE_X.index(near)]) + 38, 'on paper', 24, SKY, 800, a=1 - 0.5 * kr)
    if kr > 0:
        xs = [v for v in E.REAL_X if v <= lerp(1964, 2026.75, kr)]
        pts = [(px(a), py(b)) for a, b in zip(xs, E.REAL_Y)]
        if len(pts) > 1:
            c.line(pts, GOLD, 6)
        c.text(px(1966), py(37), "in today's dollars", 24, GOLD, 800, anchor='lm', a=fade(t, L[2] + 3))
    bk = pop(t, L[2] + 7)
    if bk > 0:
        c.circle(px(1973.5), py(E.REAL_1973), 11 * bk, GOLD, WHITE, 2)
        c.circle(px(2026.7), py(E.REAL_Y[-1]), 11 * bk, GOLD, WHITE, 2)
        c.rrect(60, 278, 660, 360, 18, (14, 22, 40, 230), GOLD, 3, a=clamp(bk))
        c.text(360, 305, f'1973: ${E.REAL_1973:.2f}  ->  now: ${E.REAL_Y[-1]:.2f}', 26, GOLD, 900, a=clamp(bk))
        c.text(360, 340, f'only +{(E.REAL_Y[-1] / E.REAL_1973 - 1) * 100:.0f}% after inflation', 22, WHITE, 700,
               a=clamp(bk))
    source_v(c, t, 'BLS (AHETPI, CPI-U) via FRED; excludes benefits')


def v01_rule70(c, x):
    t, L = x.t, x.L
    specks(c, t, 7, 50)
    k = pop(t, L[0] + 0.5)
    c.rrect(40, 220, 680, 330, 24, (255, 255, 255, 20), GOLD, 3, a=clamp(k))
    c.text(360, 258, '70 ÷ inflation rate', 34, GOLD, 900, a=clamp(k))
    c.text(360, 300, '= years for prices to double', 28, WHITE, 800, a=clamp(k))
    span = x.E[1] - L[1]
    rows = [(2, 35, MINT, L[1] + span * 0.05), (7, 10, CORAL, L[1] + span * 0.55)]
    if len(L) > 2:
        rows.append((4, 17.5, GOLD, L[2] + 0.3))
    for i, (rate, yrs, col, d) in enumerate(rows):
        if t < d:
            continue
        y = 440 + i * 160
        g = ease(seg(t, d, d + 1.6))
        c.text(95, y, f'{rate}%', 52, col, 900, a=fade(t, d))
        c.rrect(170, y - 28, 170 + 480 * (yrs / 35) * g, y + 28, 14, col, a=fade(t, d))
        n = yrs * g
        c.text(170, y + 62, f'{n:.1f} years' if yrs % 1 else f'{int(round(n))} years', 32, WHITE, 900,
               anchor='lm', a=fade(t, d))


# -------------------------------------------------------------- ep02 housing --
def v02_hook(c, x):
    t, L = x.t, x.L
    specks(c, t, 21, 50)
    g = ease(seg(t, L[1], L[1] + 1.4))
    E.house(c, 380, 760, lerp(1.2, 2.2, g), lit=g)
    c.ellipse(380, 768, 260, 16, (0, 0, 0, 60))
    price = lerp(E.P1970, E.P_NOW, g)
    tk = pop(t, L[0] + 1.0)
    if tk > 0:
        col = mix(MINT, CORAL, g)
        c.rrect(170, 205, 550, 315, 22, col, a=clamp(tk))
        c.text(360, 240, '1970' if g < 0.5 else 'today', 24, INK, 800, a=clamp(tk), shadow=False)
        c.text(360, 284, f'${price:,.0f}', 50, INK, 900, a=clamp(tk), shadow=False)
    if t > L[2] + 1.2:
        k = pop(t, L[2] + 1.2)
        c.rrect(170, 800, 550, 900, 18, (14, 22, 40, 230), GOLD, 3, a=clamp(k))
        c.text(360, 838, f'x{E.P_NOW / E.P1970_REAL:.1f}', 44, GOLD, 900, a=clamp(k))
        c.text(360, 878, 'even after inflation', 22, MUTED, 600, a=clamp(k))
    mood = 'happy' if t < L[1] + 1.4 else 'shocked'
    penny(c, 95, 700, 56, t, mood, look=(1, 0), talk=x.talk())


def v02_ratio(c, x):
    t, L = x.t, x.L
    if t < L[1] - 0.2:
        specks(c, t, 23, 50)
        c.text(360, 220, 'Years of income', 38, WHITE, 900, a=fade(t, 0.3))
        c.text(360, 268, 'to buy a home', 38, WHITE, 900, a=fade(t, 0.3))
        E.house(c, 360, 560, 1.2)
        c.text(360, 598, 'home price', 26, CREAM, 800, a=fade(t, 1))
        c.text(360, 668, '÷', 70, MUTED, 900, a=fade(t, 1.5))
        c.icon('briefcase', 360, 770, 100, SKY, a=fade(t, 2))
        c.text(360, 852, 'yearly income', 26, SKY, 800, a=fade(t, 2))
        return
    title(c, t - L[1] + 0.2, 'Home price ÷ household income', 'median new home, median income')
    k = ease(seg(t, L[1], L[2] + 2))
    px, py = line_chart(c, (110, 340, 650, 800), E.RATIO_YEARS, E.RATIO, (1984, E.RATIO_YEARS[-1]), (0, 7), k,
                        GOLD, xticks=range(1985, 2030, 10), yticks=range(0, 8), yfmt='{:.0f}x', a=fade(t, L[1]),
                        tick_size=22)
    mark(c, t, px, py, 1984, E.R1984, f'1984: {E.R1984:.1f}x', MINT, L[1] + 1)
    mark(c, t, px, py, 2022, E.R2022, f'2022: {E.R2022:.1f}x', CORAL, L[2] + 0.5)
    mark(c, t, px, py, E.RATIO_YEARS[-1], E.R_LAST, f'{E.RATIO_YEARS[-1]}: {E.R_LAST:.1f}x', GOLD, L[2] + 3.5,
         above=False)
    source_v(c, t, 'Census/HUD (MSPUS), Census income via FRED')


def v02_supply(c, x):
    t, L = x.t, x.L
    title(c, t, 'New homes started per year', 'average by decade')
    k = seg(t, L[0] + 0.5, L[1] + 3)
    n = len(E.DECADES)
    for i, (d, v) in enumerate(E.DECADES):
        g = ease(seg(k, i / n * 0.6, i / n * 0.6 + 0.4))
        y = 330 + i * (470 / max(1, n - 1))
        col = CORAL if (t > L[1] + 4 and i == 5) else SKY
        c.text(105, y, f'{d}s', 26, MUTED, 800, anchor='rm', shadow=False)
        if g > 0:
            w = 430 * (v / 1000) / 2.0 * g
            c.rrect(125, y - 22, 125 + w, y + 22, 10, col)
            c.text(140 + w, y, f'{v / 1000:.2f}M', 26, WHITE, 800, anchor='lm', a=fade(g, 0.6, 0.4))
    if t > L[2]:
        k2 = pop(t, L[2] + 0.3)
        c.rrect(150, 840, 570, 905, 18, (14, 22, 40, 230), CORAL, 3, a=clamp(k2))
        c.text(360, 872, 'fewer homes + more people', 28, CORAL, 900, a=clamp(k2))
    else:
        source_v(c, t, 'Census housing starts (HOUST) via FRED')


def v02_rules(c, x):
    t, L = x.t, x.L
    specks(c, t, 24, 50)
    title(c, t, 'Why not just build more?')
    if t < L[1]:
        E.house(c, 380, 720, 1.8, a=fade(t, 0.3))
        stop_k = pop(t, L[0] + 2)
        if stop_k > 0:
            c.circle(560, 400, 62 * stop_k, CORAL, WHITE, 4)
            c.text(560, 402, 'NO', 36, WHITE, 900, a=clamp(stop_k), shadow=False)
        penny(c, 110, 680, 58, t, 'worried' if t > L[0] + 2 else 'happy', look=(1, 0), talk=x.talk())
        return
    span = x.E[1] - L[1]
    items = [('house', 'Single-family\nonly'), ('ruler', 'Big minimum\nlots'), ('file-text', 'Slow\npermits'),
             ('map-pin', 'Scarce land\nnear jobs')]
    for i, (ic, label) in enumerate(items):
        k = pop(t, L[1] + span * (0.05 + 0.2 * i))
        cx, cy = 200 + (i % 2) * 320, 400 + (i // 2) * 290
        c.circle(cx, cy, 82 * k, (255, 255, 255, 18), GOLD, 3, a=clamp(k))
        c.icon(ic, cx, cy, 72 * k, GOLD, a=clamp(k))
        for j, part in enumerate(label.split('\n')):
            c.text(cx, cy + 125 + j * 34, part, 26, WHITE, 800, a=clamp(k))


def v02_payment(c, x):
    t, L = x.t, x.L
    specks(c, t, 25, 50)
    title(c, t, 'Monthly payment, median new home', '30-year mortgage, 20% down')
    if t < L[1]:
        g = ease(seg(t, L[0] + 0.5, L[0] + 2.5))
        c.text(360, 540, f'{lerp(min(E.RATE_Y), E.RATE_Y[-1], g):.2f}%', 130, CORAL, 900, a=fade(t, 0.3))
        c.text(360, 640, '30-year mortgage rate today', 26, MUTED, 600, a=fade(t, 0.3))
        return
    span = x.E[1] - L[1]
    for i, (label, pay, share, col, f) in enumerate((('2021', E.PAY_2021, E.SHARE_2021, MINT, 0.0),
                                                     ('today', E.PAY_NOW, E.SHARE_NOW, CORAL, 0.45))):
        g = ease(seg(t, L[1] + span * f, L[1] + span * f + 1.2))
        bx = 200 + i * 320
        top = 800 - 400 * (pay / 2400) * g
        c.rrect(bx - 95, top, bx + 95, 800, 16, col, a=fade(t, L[1] + span * f))
        c.text(bx, top - 34, f'${pay * g:,.0f}', 46, col, 900, a=fade(t, L[1] + span * f))
        c.text(bx, 835, label, 28, WHITE, 800, a=fade(t, L[1] + span * f))
        if t > L[2]:
            k = pop(t, L[2] + 0.5 + i * 1.5)
            c.rrect(bx - 140, 300, bx + 140, 360, 16, (255, 255, 255, 22), col, 3, a=clamp(k))
            c.text(bx, 330, f'{share:.0f}% of income', 28, col, 900, a=clamp(k))


# ----------------------------------------------------------------- ep05 jobs --
def v05_layoffs(c, x):
    t, L = x.t, x.L
    title(c, t, 'Layoffs per month, US', 'layoffs and discharges, millions')
    k = ease(seg(t, L[0] + 0.5, L[1] + 2))
    px, py = line_chart(c, (100, 340, 650, 800), E.LAY_X, E.LAY_Y, (2001, E.LAY_X[-1] + 0.2), (0, 4), k, CORAL,
                        xticks=range(2002, 2027, 8), yticks=range(0, 5), yfmt='{:.0f}M', a=fade(t, 0.1), width=4,
                        tick_size=24)
    if t > L[3] - 0.5:
        c.text(px(2019.9), 372, f'Mar 2020: {E.L_MAX / 1000:.1f}M', 24, CORAL, 900, anchor='rm',
               a=fade(t, L[3] - 0.3))
        c.text(px(2019.9), 402, '(off the chart)', 20, CORAL, 700, anchor='rm', a=fade(t, L[3] - 0.3))
    mark(c, t, px, py, 2019.5, E.L19 / 1000, f'2019 avg: {E.L19 / 1000:.2f}M', GOLD, L[2] + 1, above=False,
         dx=-130)
    mark(c, t, px, py, E.LAY_X[-1], E.L_NOW / 1000, f'now: {E.L_NOW / 1000:.2f}M', MINT, L[1] + 2, above=False)
    if t > L[2] + 3:
        chip(c, 360, 880, f'Share of all jobs: {E.RATE_NOW:.1f}% now vs {E.RATE19:.1f}% in 2019', GOLD,
             pop(t, L[2] + 3.3), 24)
    else:
        source_v(c, t, 'BLS JOLTS (JTSLDL) via FRED')


def v05_hiring(c, x):
    t, L = x.t, x.L
    if t < L[3]:
        title(c, t, 'Job openings, US', 'millions')
        k = ease(seg(t, L[1], L[1] + 3))
        px, py = line_chart(c, (100, 340, 650, 800), E.OPEN_X, E.OPEN_Y, (2001, E.OPEN_X[-1] + 0.2), (0, 14), k,
                            SKY, xticks=range(2002, 2027, 8), yticks=range(0, 15, 2), yfmt='{:.0f}M',
                            a=fade(t, 0.1), width=4, tick_size=24)
        pk = E.OPEN_X[E.OPEN_Y.index(E.O_PEAK / 1000)]
        mark(c, t, px, py, pk, E.O_PEAK / 1000, f'Mar 2022: {E.O_PEAK / 1000:.1f}M', GOLD, L[1] + 2)
        mark(c, t, px, py, E.OPEN_X[-1], E.O_NOW / 1000, f'now: {E.O_NOW / 1000:.1f}M', CORAL, L[1] + 4,
             above=False)
        if t > L[2]:
            chip(c, 360, 880, f'Open jobs per jobless person: {E.R_PEAK:.0f} then, {E.R_NOW:.0f} now', GOLD,
                 pop(t, L[2] + 0.3), 24)
        else:
            source_v(c, t, 'BLS JOLTS (JTSJOL), unemployed (UNEMPLOY) via FRED')
        return
    specks(c, t, 75, 50)
    title(c, t - L[3], 'A low-hire, low-fire', None)
    c.text(360, 250, 'job market', 34, WHITE, 900, a=fade(t, L[3]))
    compare_bars(c, t, (('hiring rate 2019', E.H19, GOLD), ('hiring rate now', E.H_NOW, CORAL)), L[3] + 0.3, 2.0,
                 5, lambda v: f'{v:.1f}%', box=(90, 330, 630, 540), value_size=42, label_size=24)
    if t > L[5]:
        compare_bars(c, t, (('weeks to find work 2019', E.W19, GOLD), ('now', E.W_NOW, CORAL)), L[5] + 0.3, 2.0,
                     30, lambda v: f'{v:.0f} wks', box=(90, 640, 630, 830), value_size=42, label_size=24)
    source_v(c, t, 'BLS JOLTS (JTSHIR), UEMPMEAN via FRED')


VERTICAL = {
    'ep01_short_prices': [v01_hook, v01_prices],
    'ep01_short_wages': [v01_wages],
    'ep01_short_rule70': [v01_rule70],
    'ep02_short_price': [v02_hook, v02_ratio],
    'ep02_short_payment': [v02_payment],
    'ep02_short_supply': [v02_supply, v02_rules],
    'ep05_short_layoffs': [v05_layoffs],
    'ep05_short_hiring': [v05_hiring],
    'ep04_short_cards': [v04_cards],
    'ep04_short_savings': [v04_savings],
    'ep04_short_why': [v04_why],
    'ep03_short_jump': [v03_hook, v03_oil],
    'ep03_short_barrel': [v03_barrel],
    'ep03_short_feathers': [v03_feathers],
}


def scenes_for(name):
    """The original Short's scenes with their drawings swapped for the vertical versions. Week 1 episodes have
    their own 16:9 end card; it becomes the shared vertical end card (same line, same timing)."""
    out = []
    draws = list(VERTICAL[name])
    for sc in E.SHORTS[name]:
        if sc.get('vertical'):
            out.append(sc)
            continue
        sc = {k: v for k, v in sc.items() if k not in ('focus', '_crop')}
        draw = draws.pop(0) if draws else end_card(sc['lines'][0])['draw']
        out.append(dict(sc, draw=draw, vertical=True))
    return out


if __name__ == '__main__':
    scenes = scenes_for(NAME)
    build_dir = os.path.join(HERE, 'build', EPN, NAME)
    os.makedirs(build_dir, exist_ok=True)
    if '--stills' in sys.argv:
        previews([], {NAME: scenes}, os.path.join(HERE, 'build', EPN, 'vshorts'))
        sys.exit()
    build(scenes, os.path.join(HERE, 'out', f'{NAME}.mp4'), build_dir, layout='short')
