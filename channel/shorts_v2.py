"""Standalone Shorts, written for Shorts (not cut from a long video). The 10/10 rules, checked on every build:

  1. Hook at 0.0 s: the biggest number is already on screen in frame one, and the first line says it.
  2. Something changes at least every 4 s (engine.pace_report warns otherwise).
  3. Punch zooms on the reveals ('punch'), expressive voice on hook and reveal lines (lines starting with '!').
  4. One continuous scene whose last frame matches the first, built with loop=True: no fade from or to black,
     so the Short runs straight back into its start. The link to the full video lives in the pinned comment.
  5. 30-45 seconds. Every number comes from the episode's own data module (its check_numbers() must pass).

    python3 channel/shorts_v2.py ep03_short_barrel [--stills]
"""
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
NAME = next(a for a in sys.argv[1:] if not a.startswith('-'))
sys.argv = [sys.argv[0]] + [a for a in sys.argv[1:] if a.startswith('-')]

from wk2_art import *  # noqa: E402,F401,F403
from engine import build, still  # noqa: E402

EPN = NAME.split('_')[0]
E = importlib.import_module({'ep01': 'ep01_inflation', 'ep02': 'ep02_housing', 'ep03': 'ep03_gas',
                             'ep04': 'ep04_fed', 'ep05': 'ep05_jobs', 'ep08': 'ep08_midterms'}[EPN])


def big(c, text, y, size, color, k=1.0, sub=None):
    """A headline number, scaled in with k."""
    if k <= 0:
        return
    c.text(360, y, text, int(size * (0.6 + 0.4 * clamp(k))), color, 900, a=clamp(k), stroke=4)
    if sub:
        c.text(360, y + size * 0.62, sub, 28, WHITE, 800, a=clamp(k))


def headline(c, t, at, icon, color, value, caption, sub=None, icon_size=200):
    """The workhorse beat: an icon, then the number punches in, then a caption."""
    if icon:
        c.icon(icon, 360, 400, icon_size, color, a=fade(t, at), stroke=2.2)
    big(c, value, 650, 110, color, pop(t, at + 0.4), None)
    c.text(360, 760, caption, 32, WHITE, 900, a=fade(t, at + 0.6))
    if sub:
        c.text(360, 810, sub, 26, MUTED, 800, a=fade(t, at + 0.9), shadow=False)


def two_bars(c, t, at, a, b, fmt, vmax, title=None, span=1.4, bottom=800):
    if title:
        c.text(360, 220, title, 32, WHITE, 900)
    compare_bars(c, t, (a, b), at, span, vmax, fmt, box=(80, 300, 640, bottom), value_size=60, label_size=30)


# --------------------------------------------------- ep03: what's in a gallon --
def barrel_draw(c, x):
    t, L, Ev = x.t, x.L, x.E
    specks(c, t, 41, 50)
    price, crude = E.money(E.G_NOW), E.money(E.CRUDE_GAL)
    end = x.dur - 0.9  # the last 0.9 s are drawn exactly like frame one, for the loop
    if t < L[1] or t >= end:
        gas_pump(c, 330, 760, 1.9, price, color=CORAL)
        c.ellipse(380, 768, 230, 16, (0, 0, 0, 60))
        chip(c, 360, 215, 'one gallon of gas', GOLD, 1, 30)
        if L[0] + 2.2 < t < L[1]:
            k = pop(t, L[0] + 2.2)
            c.rrect(150, 800, 570, 900, 22, (14, 22, 40, 235), GOLD, 4, a=clamp(k))
            c.text(360, 850, f'{crude} = crude oil', 40, GOLD, 900, a=clamp(k))
        penny(c, 95, 720, 54, t, 'shocked' if L[0] + 2.2 < t < L[1] else 'happy', look=(1, 0), talk=x.talk())
        return
    if t < L[3]:
        barrel(c, 170, 470, 1.25, f'${E.O_NOW:.0f} a barrel')
        n = int(42 * ease(seg(t, L[1] + 0.6, L[1] + 2.2)))
        for i in range(n):
            c.icon('fuel', 330 + (i % 7) * 52, 300 + (i // 7) * 50, 34, SKY)
        c.text(500, 640, f'{n} gallons', 40, SKY, 900, a=fade(t, L[1] + 0.6))
        if t > L[2]:
            k = pop(t, L[2] + 1.6)
            c.text(360, 760, f'${E.O_NOW:.0f} ÷ 42', 52, WHITE, 900, a=fade(t, L[2]))
            big(c, f'= {crude}', 850, 84, GOLD, k, None)
        return
    if t < L[4]:
        k = ease(seg(t, L[3], L[3] + 0.9))
        c.arc(360, 520, 210, -90, -90 + 360, (255, 255, 255, 30), 46)
        c.arc(360, 520, 210, -90, -90 + 360 * E.CRUDE_SHARE / 100 * k, CORAL, 46)
        big(c, f'{E.CRUDE_SHARE * k:.0f}%', 540, 120, WHITE, 1)
        c.text(360, 820, 'of your gas price is crude oil', 30, WHITE, 800, a=fade(t, L[3] + 0.5))
        return
    if t < L[5]:
        x0, x1, y0 = 40, 680, 300
        c.rrect(x0, y0, x1, y0 + 90, 18, (255, 255, 255, 25))
        c.rrect(x0, y0, x0 + (x1 - x0) * E.CRUDE_SHARE / 100, y0 + 90, 18, CORAL)
        c.text(x0 + (x1 - x0) * E.CRUDE_SHARE / 200, y0 + 45, f'crude {E.CRUDE_SHARE:.0f}%', 32, INK, 900,
               shadow=False)
        c.text(x0 + (x1 - x0) * (0.5 + E.CRUDE_SHARE / 200), y0 + 45, 'the rest', 28, WHITE, 800, shadow=False)
        items = (('factory', 'refining'), ('truck', 'trucking'), ('store', 'the station'), ('landmark', 'taxes'))
        for i, (ic, label) in enumerate(items):
            k = pop(t, L[4] + 0.5 + i * 0.75)
            if k <= 0:
                continue
            cx, cy = 200 + (i % 2) * 320, 520 + (i // 2) * 210
            c.circle(cx, cy, 70 * k, (255, 255, 255, 18), GOLD, 3, a=clamp(k))
            c.icon(ic, cx, cy, 64 * k, GOLD, a=clamp(k))
            c.text(cx, cy + 105, label, 30, WHITE, 800, a=clamp(k))
        return
    if t < L[6]:
        c.icon('landmark', 360, 330, 150, GOLD, a=fade(t, L[5]))
        big(c, '18.4¢', 560, 130, GOLD, pop(t, L[5] + 0.2), None)
        c.text(360, 660, 'federal gas tax per gallon', 30, WHITE, 800, a=fade(t, L[5] + 0.6))
        k = pop(t, L[5] + 2.8)
        if k > 0:
            c.icon('calendar', 250, 780, 54, CORAL, a=clamp(k))
            c.text(400, 780, 'since 1993', 44, CORAL, 900, a=clamp(k))
        return
    # back to the pump: oil moves, the pump moves
    gas_pump(c, 330, 760, 1.9, price, color=CORAL)
    c.ellipse(380, 768, 230, 16, (0, 0, 0, 60))
    chip(c, 360, 215, 'one gallon of gas', GOLD, 1, 30)
    k = fade(t, L[6] + 0.3)
    c.icon('droplet', 600, 420, 70, GOLD, a=k * (1 - fade(t, end - 0.4)))
    c.icon('arrow-up', 600, 330, 70, CORAL, a=k * (1 - fade(t, end - 0.4)), stroke=2.5)
    penny(c, 95, 720, 54, t, 'happy', look=(1, 0), talk=x.talk())


def cents(v):
    return f'{round(v * 100)}¢'


def feathers_cover(c, t, x):
    """Frame one (and the last frame, for the loop): up like a rocket, down like a feather."""
    c.rrect(40, 190, 680, 520, 30, (255, 255, 255, 14), CORAL, 3)
    c.icon('rocket', 150, 355, 120, CORAL, stroke=2.5)
    c.text(430, 320, f'+{E.money(E.UP_GAS)}', 96, CORAL, 900, stroke=4)
    c.text(430, 410, 'gas, on the way up', 28, WHITE, 800)
    c.rrect(40, 560, 680, 890, 30, (255, 255, 255, 14), MINT, 3)
    c.icon('feather', 150, 725 + math.sin(t * 2) * 8, 120, MINT, stroke=2.5)
    c.text(430, 690, f'-{cents(E.DN_GAS)}', 96, MINT, 900, stroke=4)
    c.text(430, 780, 'gas, on the way down', 28, WHITE, 800)


def feathers_draw(c, x):
    t, L = x.t, x.L
    specks(c, t, 43, 50)
    end = x.dur - 0.9
    if t < L[1] or t >= end:
        feathers_cover(c, t, x)
        return
    if t < L[3]:
        c.text(360, 215, 'On the way UP (Jan to spring)', 32, CORAL, 900)
        compare_bars(c, t, (('oil, per gallon', E.UP_CRUDE, SKY), ('pump price', E.UP_GAS, CORAL)), L[1] + 0.8,
                     max(1.2, L[2] - L[1]), 2.0, lambda v: f'+${v:.2f}', box=(70, 330, 650, 800), value_size=60,
                     label_size=30)
        if t > L[2] + 0.4:
            chip(c, 360, 925, 'pump price rose MORE than oil', CORAL, pop(t, L[2] + 0.4), 28)
        if t > L[2] + 2.4:
            big(c, f'+${E.UP_GAS - E.UP_CRUDE:.2f} extra a gallon', 1005, 46, GOLD, pop(t, L[2] + 2.4), None)
        return
    if t < L[5]:
        c.text(360, 215, 'On the way DOWN (spring to July)', 32, MINT, 900)
        compare_bars(c, t, (('oil, per gallon', E.DN_CRUDE, SKY), ('pump price', E.DN_GAS, MINT)), L[3] + 0.8,
                     max(1.2, L[4] - L[3]), 2.0, lambda v: f'-${v:.2f}', box=(70, 330, 650, 800), value_size=60,
                     label_size=30)
        return
    if t < L[6]:
        k = ease(seg(t, L[5], L[5] + 2.5))
        c.text(360, 215, 'Rockets and feathers', 44, GOLD, 900, a=fade(t, L[5]))
        c.icon('rocket', 200, 800 - 480 * k, 120, CORAL, stroke=2.5)
        c.icon('feather', 520 + math.sin(t * 3) * 40, 320 + 420 * ease(seg(t, L[5], L[5] + 6)), 110, MINT,
               stroke=2.5)
        c.text(200, 900, 'UP like a rocket', 32, CORAL, 900, a=fade(t, L[5] + 1.0))
        c.text(520, 860, 'DOWN like', 32, MINT, 900, a=fade(t, L[5] + 2.2))
        c.text(520, 900, 'a feather', 32, MINT, 900, a=fade(t, L[5] + 2.2))
        return
    if t < L[7]:
        # the pump price: up fast, down slow
        up = ease(seg(t, L[6] + 0.3, L[6] + 1.2))
        dn = ease(seg(t, L[6] + 2.2, L[7]))
        price = E.G_LOW + (E.G_PEAK - E.G_LOW) * up - (E.G_PEAK - E.G_LOW) * 0.42 * dn
        gas_pump(c, 330, 720, 1.7, E.money(price), color=mix(MINT, CORAL, up - 0.5 * dn))
        chip(c, 360, 215, 'raise fast', CORAL, pop(t, L[6] + 0.3), 30)
        chip(c, 360, 830, 'cut slow', MINT, pop(t, L[6] + 2.2), 30)
        c.icon('rabbit', 600, 300, 70, CORAL, a=fade(t, L[6] + 0.3))
        c.icon('snail', 600, 760, 70, MINT, a=fade(t, L[6] + 2.2))
        return
    feathers_cover(c, t, x)


# ------------------------------------------------------------- ep04: the Fed --
def seam(t, dur):
    """0 at the first and last frame (so the loop seam matches), 1 in between."""
    return clamp(t / 0.5) * clamp((dur - t) / 0.5) if dur else 0


def cards_cover(c, t, dur=None):
    e = seam(t, dur)
    card(c, 360, 380 + 10 * e * math.sin(t * 4), 1.5, color=SKY)
    big(c, f'${round(E.CC_COST, -1):,.0f}', 690 + 9 * e * math.sin(t * 5 + 1), 110, CORAL, 1, None)
    c.text(360, 770, 'a year in interest', 34, WHITE, 900)
    c.text(360, 820, 'on a $5,000 card balance', 28, MUTED, 800, shadow=False)


def cards_draw(c, x):
    t, L = x.t, x.L
    specks(c, t, 56, 50)
    if t < L[1] or t >= x.dur - 0.9:
        cards_cover(c, t, x.dur)
        return
    if t < L[2]:
        dial(c, 360, 560, 220, E.CC_NOW, 30, '', a=fade(t, L[1]), color=CORAL)
        big(c, f'{E.CC_NOW:.1f}%', 690, 100, CORAL, pop(t, L[1] + 0.8), None)
        c.text(360, 790, 'average card rate at banks', 30, WHITE, 800, a=fade(t, L[1] + 0.8))
        return
    if t < L[3]:
        compare_bars(c, t, (('prime rate', E.P_NOW, GOLD), ('avg card rate', E.CC_NOW, CORAL)), L[2] + 0.2, 1.4, 25,
                     lambda v: f'{v:.1f}%', box=(80, 300, 640, 780), value_size=60, label_size=30)
        chip(c, 360, 880, f'about {round(E.CC_NOW / E.P_NOW)}x the prime rate', GOLD, pop(t, L[2] + 2.0), 30)
        return
    if t < L[4]:
        c.text(360, 260, "The Fed's latest hike", 36, WHITE, 900)
        big(c, '+0.25%', 470, 110, GOLD, pop(t, L[3] + 0.3), None)
        c.text(360, 610, 'on a $5,000 balance:', 30, WHITE, 800, a=fade(t, L[3] + 1.5))
        big(c, f'+${E.QUARTER:.2f} a year', 740, 70, MINT, pop(t, L[3] + 2.4), None)
        chip(c, 360, 860, f'about ${E.QUARTER / 12:.0f} a month', MINT, pop(t, L[3] + 4.5), 30)
        return
    if t < L[5]:
        c.icon('flame', 360, 380, 200, CORAL, a=fade(t, L[4]), stroke=2.5)
        big(c, f'{E.CC_NOW:.0f}%', 680, 160, CORAL, pop(t, L[4] + 0.6), None)
        c.text(360, 800, 'is the real problem', 34, WHITE, 900, a=fade(t, L[4] + 1.0))
        return
    k = ease(seg(t, L[5], L[5] + 3))
    card(c, 360, 360, 1.3, color=SKY)
    c.text(360, 600, 'every $1 you pay off', 36, WHITE, 900, a=fade(t, L[5]))
    c.text(360, 660, f'stops costing you {E.CC_NOW:.0f}%', 40, MINT, 900, a=fade(t, L[5] + 1.0))
    for i in range(6):
        c.circle(160 + i * 80, 780 - 60 * k * (i % 2), 22, GOLD, GOLD_D, 2, a=1 - k * 0.5)


def savings_cover(c, t, dur=None):
    e = seam(t, dur)
    dial(c, 190, 470, 140, E.S_NOW, 5, '', color=MINT)
    dial(c, 530, 470, 140, E.CPI_NOW, 5, '', color=CORAL)
    c.text(190, 610, E.pct(E.S_NOW), 64, MINT, 900, stroke=4)
    c.text(190, 670, 'your savings', 28, WHITE, 800)
    c.text(530, 610 + 9 * e * math.sin(t * 5), f'{E.CPI_NOW:.1f}%', int(64 * (1 + 0.08 * e * abs(math.sin(t * 4)))),
           CORAL, 900, stroke=4)
    c.text(530, 670, 'prices', 28, WHITE, 800)
    c.text(360, 220 + 8 * e * math.sin(t * 4 + 2), 'Who wins?', 44, GOLD, 900)


def savings_draw(c, x):
    t, L = x.t, x.L
    specks(c, t, 58, 50)
    if t < L[1] or t >= x.dur - 0.9:
        savings_cover(c, t, x.dur)
        return
    if t < L[2]:
        c.icon('piggy-bank', 360, 430, 230, MINT, a=fade(t, L[1]))
        big(c, E.pct(E.S_NOW), 690, 110, MINT, pop(t, L[1] + 0.5), None)
        c.text(360, 790, 'national average savings rate (FDIC)', 28, WHITE, 800, a=fade(t, L[1] + 0.6))
        return
    if t < L[3]:
        k = ease(seg(t, L[2], L[2] + 2.5))
        c.icon('piggy-bank', 360, 430, 230 * (1 - 0.25 * k), MINT)
        big(c, f'-{E.REAL_LOSS:.1f}%', 690, 110, CORAL, pop(t, L[2] + 1.0), None)
        c.text(360, 790, 'buying power lost every year', 30, WHITE, 800, a=fade(t, L[2] + 1.2))
        return
    if t < L[5]:
        c.text(360, 220, 'A $10,000 emergency fund earns', 32, WHITE, 900)
        compare_bars(c, t, ((f'at {E.pct(E.S_NOW)}', E.EF_NOW, MUTED), ('at 3.5%', E.EF_ALT, MINT)), L[3] + 0.5,
                     max(1.2, L[4] - L[3]), 400, lambda v: f'${v:.0f}', box=(80, 300, 640, 800), value_size=64,
                     label_size=32)
        c.text(360, 880, 'per year', 30, MUTED, 800, shadow=False)
        if t > L[4] + 0.6:
            chip(c, 360, 960, f'about {E.EF_ALT / E.EF_NOW:.0f}x more', MINT, pop(t, L[4] + 0.6), 30)
        return
    if t < L[5] + 4.0:  # 'many online banks pay rates much closer to the Fed's'
        c.icon('landmark', 360, 430, 200, SKY, a=fade(t, L[5]))
        c.text(360, 640, 'many online banks', 36, WHITE, 900, a=fade(t, L[5] + 0.3))
        c.text(360, 700, "pay much closer to the Fed's rate", 30, SKY, 800, a=fade(t, L[5] + 1.2))
        return
    c.icon('shield-check', 360, 420, 200, MINT, a=fade(t, L[5] + 4.0))
    c.text(360, 620, 'FDIC insurance covers', 34, WHITE, 900, a=fade(t, L[5] + 4.0))
    big(c, '$250,000', 720, 80, MINT, pop(t, L[5] + 5.0), None)
    c.text(360, 800, 'per depositor, per bank', 28, MUTED, 800, a=fade(t, L[5] + 5.0), shadow=False)


def why_cover(c, t):
    gas_pump(c, 170, 650, 1.15, '$4.27', color=CORAL)
    c.icon('arrow-up', 170, 270, 80, CORAL, stroke=2.5)
    c.icon('arrow-right', 360, 470, 70, WHITE, stroke=2.5)
    c.icon('landmark', 540, 430, 170, GOLD)
    c.text(540, 590, '+0.25%', 60, GOLD, 900, stroke=4)
    c.text(540, 650, 'the Fed', 30, WHITE, 800)
    c.text(360, 820, 'Why does gas make the Fed', 32, WHITE, 900)
    c.text(360, 862, 'raise interest rates?', 32, WHITE, 900)


def why_draw(c, x):
    t, L = x.t, x.L
    specks(c, t, 54, 50)
    if t < L[1] or t >= x.dur - 0.9:
        why_cover(c, t)
        return
    if t < L[2]:
        tanker(c, 360, 520, 1.6, t=t)
        k = pop(t, L[1] + 1.5)
        if k > 0:
            c.circle(360, 470, 120 * k, None, CORAL, 10, a=clamp(k))
            c.line([(275, 385), (445, 555)], CORAL, 10, a=clamp(k))
        c.text(360, 760, 'Strait of Hormuz', 36, WHITE, 900, a=fade(t, L[1]))
        c.text(360, 810, 'tankers stopped, oil soared', 30, CORAL, 800, a=fade(t, L[1] + 1.5))
        return
    if t < L[3]:
        c.text(360, 220, "Inflation vs the Fed's 2% target", 32, WHITE, 900)
        compare_bars(c, t, (('target', 2.0, MINT), ('Feb 2026', E.CPI_FEB, GOLD), ('Sep 2026', E.CPI_NOW, CORAL)),
                     L[2] + 0.3, max(1.5, L[3] - L[2] - 1.5), 5, lambda v: f'{v:.1f}%', box=(50, 300, 670, 800),
                     value_size=50, label_size=26)
        return
    if t < L[4]:
        steps = (('percent', 'Higher\nrates'), ('shopping-cart', 'Less\nspending'), ('trending-down', 'Prices\ncool'))
        icon_row(c, t, steps, L[3] + 0.2, max(1.0, L[4] - L[3] - 0.5), y=500, x0=0, width=720, ring=95,
                 size=84, label_size=30)
        return
    if t < L[5]:
        barrel(c, 360, 640, 2.2)
        k = pop(t, L[4] + 0.5)
        c.line([(220, 330), (500, 660)], CORAL, 14, a=clamp(k))
        c.text(360, 790, "Rates can't pump oil", 44, CORAL, 900, a=fade(t, L[4] + 0.3))
        return
    c.icon('shopping-cart', 360, 420, 190, GOLD, a=fade(t, L[5]))
    c.text(360, 610, 'They can only slow spending', 36, WHITE, 900, a=fade(t, L[5] + 0.3))
    c.text(360, 670, 'so the fuel shock', 32, MUTED, 800, a=fade(t, L[5] + 1.5))
    c.text(360, 715, "doesn't spread to everything", 32, MUTED, 800, a=fade(t, L[5] + 1.5))


# --------------------------------------------------------------- ep05: jobs --
def layoffs_cover(c, t):
    two_bars(c, 99, 0, ('2019 average', E.L19 / 1000, MUTED), ('August 2026', E.L_NOW / 1000, MINT),
             lambda v: f'{v:.2f}M', 2.4, 'Layoffs per month, US', bottom=740)
    chip(c, 360, 880, 'LOWER than before COVID', MINT, 1, 32)


def layoffs_draw(c, x):
    t, L = x.t, x.L
    specks(c, t, 61, 50)
    if t < L[1] or t >= x.dur - 0.9:
        layoffs_cover(c, t)
        return
    if t < L[2]:
        headline(c, t, L[1], 'user-minus', CORAL, f'{E.L_NOW / 1000:.2f}M', 'laid off or discharged in August')
        return
    if t < L[3]:
        two_bars(c, t, L[2] + 0.3, ('2019 average', E.L19 / 1000, MUTED), ('August 2026', E.L_NOW / 1000, MINT),
                 lambda v: f'{v:.2f}M', 2.4, 'Layoffs per month, US')
        return
    if t < L[4]:
        two_bars(c, t, L[3] + 0.3, ('2019', E.RATE19, MUTED), ('now', E.RATE_NOW, MINT), lambda v: f'{v:.1f}%', 1.6,
                 'Layoffs as a share of all jobs')
        return
    if t < L[5]:
        headline(c, t, L[4], 'triangle-alert', CORAL, f'{E.L_MAX / 1000:.0f} million', 'laid off in March 2020',
                 'in a single month')
        return
    c.icon('user-plus', 360, 420, 200, GOLD, a=fade(t, L[5]))
    c.text(360, 640, 'The real problem:', 36, WHITE, 900, a=fade(t, L[5] + 0.3))
    big(c, 'HIRING', 740, 96, GOLD, pop(t, L[5] + 1.6), None)


def hiring_cover(c, t):
    c.icon('clock', 360, 400, 200, CORAL, stroke=2.2)
    big(c, f'{E.W_NOW:.0f} weeks', 650, 100, CORAL, 1, None)
    c.text(360, 760, 'to find a new job, on average', 32, WHITE, 900)


def hiring_draw(c, x):
    t, L = x.t, x.L
    specks(c, t, 62, 50)
    if t < L[1] or t >= x.dur - 0.9:
        hiring_cover(c, t)
        return
    if t < L[2]:
        two_bars(c, t, L[1] + 0.3, ('March 2022', E.O_PEAK / 1000, GOLD), ('now', E.O_NOW / 1000, CORAL),
                 lambda v: f'{v:.1f}M', 14, 'Open jobs in America', span=max(1.4, L[2] - L[1] - 2))
        return
    if t < L[3]:
        k = pop(t, L[2] + 0.3)
        c.text(360, 230, 'Open jobs per unemployed person', 32, WHITE, 900)
        for i in range(2):
            c.icon('briefcase', 230 + i * 120, 420, 90, GOLD, a=clamp(k))
        c.text(290, 540, f'{E.R_PEAK:.0f} then', 44, GOLD, 900, a=clamp(k))
        k2 = pop(t, L[2] + 2.4)
        c.icon('briefcase', 360, 690, 90, CORAL, a=clamp(k2))
        c.text(360, 810, f'about {E.R_NOW:.0f} now', 50, CORAL, 900, a=clamp(k2))
        return
    if t < L[4]:
        two_bars(c, t, L[3] + 0.3, ('2019', E.H19, MUTED), ('August 2026', E.H_NOW, CORAL), lambda v: f'{v:.1f}%', 5,
                 'Share of workers newly hired', span=max(1.4, L[4] - L[3] - 2))
        return
    if t < L[5]:
        headline(c, t, L[4], 'clock', CORAL, f'{E.W_NOW:.0f} weeks', 'average job search now',
                 f'vs about {E.W19:.0f} weeks in 2019')
        return
    c.text(360, 260, 'low-hire, low-fire', 46, GOLD, 900, a=fade(t, L[5]))
    c.icon('shield-check', 200, 520, 130, MINT, a=fade(t, L[5] + 0.8))
    c.text(200, 650, 'have a job:', 28, WHITE, 800, a=fade(t, L[5] + 0.8))
    c.text(200, 695, 'fairly safe', 34, MINT, 900, a=fade(t, L[5] + 0.8))
    c.icon('search', 520, 520, 130, CORAL, a=fade(t, L[5] + 2.0))
    c.text(520, 650, 'need a job:', 28, WHITE, 800, a=fade(t, L[5] + 2.0))
    c.text(520, 695, 'takes longer', 34, CORAL, 900, a=fade(t, L[5] + 2.0))


# ---------------------------------------------------------- ep01: inflation --
B12 = None  # set in the entries below from the data


def prices_cover(c, t):
    b = round(100 * E.ANNUAL[1970] / E.LATEST)
    bill(c, 360, 380, 380, '100')
    c.text(360, 230, 'A $100 bill from 1970', 34, WHITE, 900)
    c.icon('arrow-down', 360, 560, 70, MUTED, stroke=2.5)
    big(c, f'= ${b}', 690, 120, CORAL, 1, None)
    c.text(360, 790, 'of buying power today', 30, WHITE, 900)


def prices_draw(c, x):
    t, L = x.t, x.L
    specks(c, t, 10, 50)
    if t < L[1] or t >= x.dur - 0.9:
        prices_cover(c, t)
        return
    if t < L[2]:
        c.icon('shopping-cart', 360, 450, 240, GOLD, a=fade(t, L[1]))
        c.text(360, 700, '1980 vs today', 50, WHITE, 900, a=fade(t, L[1] + 0.3))
        return
    for i, (icon, label, unit, p0, p1) in enumerate(E.PRICES):
        if L[2 + i] <= t < (L[3 + i] if 3 + i < len(L) else x.dur - 0.9):
            at = L[2 + i]
            c.icon(icon, 360, 330, 170, GOLD, a=fade(t, at))
            c.text(360, 470, f'{label}, {unit}', 34, WHITE, 900, a=fade(t, at))
            c.text(360, 560, f'1980: {E.money(p0)}', 46, MINT, 900, a=fade(t, at + 0.3))
            rk = ease(seg(t, at + 1.2, at + 2.4))
            big(c, E.money(p0 + (p1 - p0) * rk), 700, 110, CORAL, 1 if rk > 0 else 0, None)
            k = pop(t, at + 2.5)
            if k > 0:
                c.rrect(270, 790, 450, 850, 26, CORAL, a=clamp(k))
                c.text(360, 820, f'x{p1 / p0:.1f}', 36, INK, 900, a=clamp(k), shadow=False)
            return


def wages_cover(c, t):
    c.text(360, 230, 'Average hourly pay', 36, WHITE, 900)
    c.text(360, 350, f'1970: ${E.WAGE_1970:.2f}', 60, MUTED, 900)
    c.icon('arrow-down', 360, 450, 60, MUTED, stroke=2.5)
    big(c, f'now: ${E.WAGE.iloc[-1]:.2f}', 580, 90, MINT, 1, None)
    c.text(360, 720, "So why don't you feel richer?", 34, GOLD, 900)


def wages_draw(c, x):
    t, L = x.t, x.L
    specks(c, t, 12, 50)
    if t < L[1] or t >= x.dur - 0.9:
        wages_cover(c, t)
        return
    if t < L[2]:
        headline(c, t, L[1], 'trending-up', MINT, f'x{E.WAGE.iloc[-1] / E.WAGE_1970:.1f}', 'on paper')
        return
    if t < L[3]:
        c.icon('shopping-cart', 360, 450, 240, CORAL, a=fade(t, L[2]))
        c.text(360, 700, 'But prices rose too', 44, CORAL, 900, a=fade(t, L[2] + 0.3))
        return
    if t < L[4]:
        headline(c, t, L[3], 'scale', GOLD, f'+{round((E.REAL_Y[-1] / E.REAL_1973 - 1) * 100)}%',
                 'real pay since 1973', 'after inflation')
        return
    c.icon('wallet', 360, 420, 200, GOLD, a=fade(t, L[4]))
    c.text(360, 640, "What matters isn't the number", 34, WHITE, 900, a=fade(t, L[4] + 0.5))
    c.text(360, 690, 'on your paycheck.', 34, WHITE, 900, a=fade(t, L[4] + 0.5))
    c.text(360, 760, "It's what it can buy.", 40, GOLD, 900, a=fade(t, L[4] + 2.0))


def rule70_cover(c, t):
    c.rrect(40, 300, 680, 520, 30, (255, 255, 255, 20), GOLD, 4)
    big(c, '70 ÷ inflation', 390, 72, GOLD, 1, None)
    c.text(360, 470, '= years for prices to double', 34, WHITE, 900)
    c.text(360, 640, 'The 2-second money trick', 36, MUTED, 900)


def rule70_draw(c, x):
    t, L = x.t, x.L
    specks(c, t, 7, 50)
    if t < L[1] or t >= x.dur - 0.9:
        rule70_cover(c, t)
        return
    c.text(360, 220, '70 ÷ inflation = years to double', 30, GOLD, 900)
    rows = [(2, 35, MINT, L[1] + 0.3), (4, 17.5, GOLD, L[2] + 0.3), (7, 10, CORAL, L[3] + 0.3)]
    for i, (rate, yrs, col, d) in enumerate(rows):
        if t < d:
            continue
        y = 380 + i * 170
        g = ease(seg(t, d, d + 1.2))
        c.text(90, y, f'{rate}%', 56, col, 900)
        c.rrect(170, y - 30, 170 + 480 * (yrs / 35) * g, y + 30, 14, col)
        n = yrs * g
        c.text(170, y + 66, f'{n:.1f} years' if yrs % 1 else f'{round(n)} years', 34, WHITE, 900, anchor='lm')
    if t > L[4]:
        chip(c, 360, 900, f'US since 1970: almost 4% a year', GOLD, pop(t, L[4] + 0.3), 28)


# ------------------------------------------------------------ ep02: housing --
def price_cover(c, t):
    E.house(c, 360, 640, 2.0)
    c.ellipse(360, 648, 230, 16, (0, 0, 0, 60))
    c.text(360, 230, f'1970: ${E.P1970:,.0f}', 56, MINT, 900, stroke=4)
    big(c, f'now: ${E.P_NOW:,.0f}', 780, 80, CORAL, 1, None)


def price_draw(c, x):
    t, L = x.t, x.L
    specks(c, t, 21, 50)
    if t < L[1] or t >= x.dur - 0.9:
        price_cover(c, t)
        return
    if t < L[2]:
        headline(c, t, L[1], 'house', GOLD, f'x{E.P_NOW / E.P1970_REAL:.1f}', 'even after inflation')
        return
    if t < L[3]:
        E.house(c, 220, 560, 1.2)
        c.text(360, 470, '÷', 80, MUTED, 900, a=fade(t, L[2] + 0.5))
        c.icon('briefcase', 520, 470, 140, SKY, a=fade(t, L[2] + 0.8))
        c.text(360, 720, 'years of income per home', 36, WHITE, 900, a=fade(t, L[2] + 0.3))
        return
    c.text(360, 220, 'Years of income to buy a home', 32, WHITE, 900)
    vals = [('1984', E.R1984, MINT, L[3] + 0.3), ('2022', E.R2022, CORAL, L[4] + 0.2),
            ('today', E.R_LAST, GOLD, L[4] + 2.5)]
    for i, (lab, v, col, d) in enumerate(vals):
        if t < d:
            continue
        g = ease(seg(t, d, d + 0.9))
        bx = 150 + i * 210
        top = 800 - 420 * v / 7 * g
        c.rrect(bx - 70, top, bx + 70, 800, 14, col)
        c.text(bx, top - 40, f'{v * g:.1f}', 54, col, 900)
        c.text(bx, 840, lab, 30, WHITE, 900)


def payment_cover(c, t):
    E.house(c, 360, 560, 1.7)
    c.text(360, 230, 'Same house', 44, WHITE, 900)
    big(c, f'+${round(E.PAY_NOW) - round(E.PAY_2021):,}', 720, 120, CORAL, 1, None)
    c.text(360, 820, 'more every month', 36, WHITE, 900)


def payment_draw(c, x):
    t, L = x.t, x.L
    specks(c, t, 25, 50)
    if t < L[1] or t >= x.dur - 0.9:
        payment_cover(c, t)
        return
    if t < L[2]:
        headline(c, t, L[1], 'percent', MINT, f'{E.RA[2021]:.1f}%', '30-year mortgage rate, 2021')
        return
    if t < L[3]:
        headline(c, t, L[2], 'house', MINT, f'${E.PAY_2021:,.0f}', 'a month, 2021', 'median new home, 20% down')
        return
    if t < L[4]:
        two_bars(c, t, L[3] + 0.3, ('2021', E.PAY_2021, MINT), ('today', E.PAY_NOW, CORAL), lambda v: f'${v:,.0f}',
                 2400, f'Rates now about {E.RATE_Y[-1]:.1f}%', span=max(1.4, L[4] - L[3] - 2))
        return
    if t < L[5]:
        c.text(360, 220, "Share of a typical household's income", 30, WHITE, 900)
        two_bars(c, t, L[4] + 0.3, ('2021', E.SHARE_2021, MINT), ('today', E.SHARE_NOW, CORAL),
                 lambda v: f'{v:.0f}%', 40)
        return
    c.icon('percent', 360, 420, 200, CORAL, a=fade(t, L[5]))
    c.text(360, 640, 'Not just pricier houses.', 36, WHITE, 900, a=fade(t, L[5] + 0.3))
    c.text(360, 700, 'Pricier money.', 46, CORAL, 900, a=fade(t, L[5] + 1.5))


def supply_bars(c, t, at, hi):
    c.text(360, 220, 'New homes started per year', 32, WHITE, 900)
    n = len(E.DECADES)
    for i, (d, v) in enumerate(E.DECADES):
        g = 1 if at is None else ease(seg(t, at + i * 0.25, at + i * 0.25 + 0.8))
        y = 320 + i * 85
        col = CORAL if (hi and d == 2010) else SKY
        c.text(110, y, f'{d}s', 30, MUTED, 800, anchor='rm', shadow=False)
        if g > 0:
            w = 400 * (v / 1000) / 2.0 * g
            c.rrect(130, y - 26, 130 + w, y + 26, 10, col)
            c.text(146 + w, y, f'{v / 1000:.2f}M', 30, WHITE, 900, anchor='lm')


def supply_draw(c, x):
    t, L = x.t, x.L
    specks(c, t, 24, 50)
    if t < L[1] or t >= x.dur - 0.9:
        supply_bars(c, t, None, True)
        chip(c, 360, 920, 'America stopped building', CORAL, 1, 32)
        return
    if t < L[3]:
        supply_bars(c, t, L[1] + 0.2, t > L[2] + 0.5)
        return
    if t < L[5]:
        c.icon('users', 220, 450, 170, GOLD, a=fade(t, L[3]))
        c.text(220, 600, 'more people', 32, GOLD, 900, a=fade(t, L[3] + 0.3))
        c.icon('house', 520, 470, 120, MUTED, a=fade(t, L[3] + 0.8))
        c.text(520, 600, 'fewer homes', 32, MUTED, 900, a=fade(t, L[3] + 0.8))
        k = pop(t, L[4] + 0.3)
        if k > 0:
            c.icon('trending-up', 360, 760, 110 * k, CORAL, stroke=2.5)
            c.text(360, 870, 'prices go up', 40, CORAL, 900, a=clamp(k))
        return
    items = [('house', 'Single-family\nonly'), ('ruler', 'Big minimum\nlots'), ('file-text', 'Slow\npermits')]
    c.text(360, 220, 'Why not just build more?', 36, WHITE, 900)
    icon_row(c, t, items, L[5] + 0.2, max(1.2, x.dur - 1.5 - L[5]), y=480, x0=0, width=720, ring=95, size=84,
             label_size=28)


# --------------------------------------------------------- ep08: midterms --
def mid_cover(c, t):
    big(c, '18 / 18', 300, 150, GOLD, 1, None)
    c.text(360, 400, 'stocks a year after every midterm', 30, WHITE, 900)
    E.bars18(c, 99, 0, 0, box=(60, 470, 660, 820), labels=False, k_all=True)
    c.text(360, 870, 'since 1950', 30, MINT, 900)


def mid_a(c, x):
    t, L = x.t, x.L
    specks(c, t, 90, 50)
    if t < L[1]:
        mid_cover(c, t)
        return
    if t < L[2]:
        c.text(360, 230, 'One year after each midterm', 32, WHITE, 900)
        E.bars18(c, t, L[1] + 0.2, max(1.5, L[2] - L[1] - 0.5), box=(60, 330, 660, 760), labels=False)
        chip(c, 360, 850, '18 up, 0 down', MINT, pop(t, L[1] + 2.0), 32)
        return
    two_bars(c, t, L[2] + 0.2, ('other years', E.OTHER_AVG, MUTED), ('after midterms', E.AVG, MINT),
             lambda v: f'+{v:.0f}%', 22, 'Average 12-month gain')


def mid_b(c, x):
    t, L = x.t, x.L
    k = pop(t, 0.4)
    if k > 0:
        c.text(360, 260, f'2022: {E.Y22_SLUMP:.1f}%', 64, CORAL, 900, a=clamp(k), stroke=6)
    k2 = pop(t, 2.2)
    if k2 > 0:
        c.text(360, 360, f'then +{E.Y22_REBOUND:.0f}%', 80, MINT, 900, a=clamp(k2), stroke=6)


def mid_c(c, x):
    t, L = x.t, x.L
    specks(c, t, 91, 50)
    if t < L[1]:
        c.icon('check', 360, 400, 200, MUTED, a=fade(t, L[0]))
        c.text(360, 640, 'The uncertainty ends', 46, GOLD, 900, a=fade(t, L[0] + 0.5))
        return
    if t < x.dur - 0.9:
        c.text(360, 220, 'small sample', 40, WHITE, 900, a=fade(t, L[1] + 0.3))
        c.text(360, 275, "history isn't a promise", 34, CORAL, 900, a=fade(t, L[1] + 1.5))
        E.bars18(c, t, L[1], 1.6, box=(40, 360, 600, 720), labels=False)
        k = pop(t, L[1] + 3.0)
        if k > 0:  # the 19th bar: 2026, still a question, pulsing
            pulse = 0.55 + 0.45 * abs(math.sin((t - L[1]) * 3.2))
            h = 360 * 18.4 / 35 * clamp(k)
            c.rrect(612, 720 - h, 676, 720, 8, (255, 214, 64, int(90 * pulse)), GOLD, 4, a=clamp(k))
            c.text(644, 720 - h - 40, '?', 54, GOLD, 900, a=clamp(k))
        big(c, '19 / 19 ?', 840, 100 + 8 * math.sin(t * 5), GOLD, pop(t, L[1] + 3.0), None)
        return
    mid_cover(c, t)


SHORTS2 = {
    'ep08_short_midterms': lambda: [
        dict(draw=mid_a, vertical=True, lead=0.1, gap=0.25, tail=0.3, lines=[
            "!Eighteen out of eighteen.",
            "Since 1950, the stock market went up in the year after every single midterm election.",
            f"On average, about {E.AVG:.0f}%. In normal years? About {E.OTHER_AVG:.0f}%.",
        ], punch=lambda L: [0.05, L[1] + 2.0], sfx=lambda L: [(0.0, 'ding'), (L[1] + 0.2, 'whoosh'),
                                                              (L[1] + 2.0, 'ding'), (L[2] + 0.2, 'pop')]),
        dict(draw=mid_b, vertical=True, bg_video=os.path.join(E.FLOW, 'clip1.mp4'), bg_speed=0.9, lead=0.2,
             gap=0.25, tail=0.3, lines=[
                 f"!Even in 2022, when stocks were down {abs(E.Y22_SLUMP):.1f}% before the vote, they came roaring "
                 "back.",
             ], punch=lambda L: [0.4, 2.2], sfx=lambda L: [(0.4, 'down'), (2.2, 'ding')]),
        dict(draw=mid_c, vertical=True, lead=0.2, gap=0.25, tail=0.9, lines=[
            "Why? Analysts say the biggest reason is simple: the uncertainty ends.",
            "But eighteen is a small sample, and history isn't a promise. So will 2026 make it nineteen for "
            "nineteen? Right now, it's",
        ], punch=lambda L: [L[1] + 3.0], sfx=lambda L: [(L[0] + 0.5, 'pop'), (L[1] + 3.0, 'ding')]),
    ],
    'ep05_short_layoffs': lambda: [dict(
        draw=layoffs_draw, vertical=True, lead=0.1, gap=0.25, tail=0.9, lines=[
            "!Everyone says layoffs are surging. The official count says they're lower than before the pandemic.",
            f"In August, US employers laid off or discharged about {E.L_NOW / 1000:.2f} million workers.",
            f"In 2019, before COVID, the average was about {E.L19 / 1000:.2f} million a month.",
            f"As a share of all jobs, that's about {E.RATE_NOW:.0f}% now, versus {E.RATE19:.1f}% in 2019.",
            f"!And in March 2020? Almost {E.L_MAX / 1000:.0f} million, in a single month.",
            "So layoffs aren't the real problem. Hiring is.",
        ],
        punch=lambda L: [0.05, L[1] + 0.4, L[4] + 0.4, L[5] + 1.6],
        sfx=lambda L: [(0.0, 'pop'), (L[1] + 0.4, 'ding'), (L[2] + 0.3, 'pop'), (L[3] + 0.3, 'pop'),
                       (L[4] + 0.4, 'down'), (L[5] + 1.6, 'ding')],
    )],
    'ep05_short_hiring': lambda: [dict(
        draw=hiring_draw, vertical=True, lead=0.1, gap=0.25, tail=0.9, lines=[
            "!Layoffs are low, but finding a job is the hardest it's been in years. Here's why.",
            f"In March 2022, America had about {E.O_PEAK / 1000:.1f} million open jobs. Now it has about "
            f"{E.O_NOW / 1000:.1f} million.",
            f"Back then, there were {E.R_PEAK:.0f} open jobs for every unemployed person. Now there's about "
            f"{E.R_NOW:.0f}.",
            f"Companies are hiring slowly too. Only {E.H_NOW:.1f}% of workers were new hires in August, down from "
            f"{E.H19:.1f}% in 2019.",
            f"!The average unemployed person now looks for about {E.W_NOW:.0f} weeks.",
            "Economists call it a low-hire, low-fire market. Fairly safe if you have a job, hard if you need one.",
        ],
        punch=lambda L: [0.05, L[2] + 2.4, L[4] + 0.4],
        sfx=lambda L: [(0.0, 'pop'), (L[1] + 0.3, 'pop'), (L[2] + 0.3, 'pop'), (L[2] + 2.4, 'down'),
                       (L[3] + 0.3, 'pop'), (L[4] + 0.4, 'ding'), (L[5], 'whoosh')],
    )],
    'ep01_short_prices': lambda: [dict(
        draw=prices_draw, vertical=True, lead=0.1, gap=0.25, tail=0.9, lines=[
            f"!A {{$100 bill|hundred-dollar bill}} from 1970 now buys about as much as "
            f"${round(100 * E.ANNUAL[1970] / E.LATEST)} did back then.",
            "Here's what that looks like at the store.",
        ] + [f"{label}: from {E.money(p0)} in 1980 to {E.money(p1)} today." if i else
             f"A pound of white bread went from {E.money(p0)} in 1980 to {E.money(p1)}."
             for i, (_, label, _u, p0, p1) in enumerate(E.PRICES[:1])] + [
            f"A dozen eggs, from {E.money(E.PRICES[1][3])} to {E.money(E.PRICES[1][4])}.",
            f"A pound of coffee, from {E.money(E.PRICES[2][3])} to {E.money(E.PRICES[2][4])}.",
            f"!And a gallon of gas, from {E.money(E.PRICES[3][3])} to {E.money(E.PRICES[3][4])}.",
        ],
        punch=lambda L: [0.05] + [L[i] + 2.5 for i in range(2, 6)],
        sfx=lambda L: [(0.0, 'pop'), (L[1], 'whoosh')] + [(L[i] + 1.2, 'pop') for i in range(2, 6)] +
                      [(L[i] + 2.5, 'ding') for i in range(2, 6)],
    )],
    'ep01_short_wages': lambda: [dict(
        draw=wages_draw, vertical=True, lead=0.1, gap=0.25, tail=0.9, lines=[
            f"!In 1970, a typical worker earned about ${E.WAGE_1970:.2f} an hour. Today it's about "
            f"${E.WAGE.iloc[-1]:.2f}.",
            "That looks like a massive raise. Almost ten times more.",
            "But prices rose too.",
            f"!Adjusted for inflation, that worker's pay is only about "
            f"{round((E.REAL_Y[-1] / E.REAL_1973 - 1) * 100)}% higher than in 1973.",
            "So what matters isn't the number on your paycheck. It's what it can buy.",
        ],
        punch=lambda L: [0.05, L[1] + 0.4, L[3] + 0.4],
        sfx=lambda L: [(0.0, 'pop'), (L[1] + 0.4, 'ding'), (L[2], 'down'), (L[3] + 0.4, 'ding'), (L[4], 'whoosh')],
    )],
    'ep01_short_rule70': lambda: [dict(
        draw=rule70_draw, vertical=True, lead=0.1, gap=0.25, tail=0.9, lines=[
            "!Here's a 2-second trick to see how fast prices double. Divide 70 by the inflation rate.",
            "At 2% inflation, prices double in about 35 years.",
            "At 4%, in about 17 and a half years.",
            "!At 7%, in just 10.",
            "Since 1970, US inflation has averaged almost 4% a year. Now you can do the math on your own money.",
        ],
        punch=lambda L: [0.05, L[3] + 0.3, L[4] + 0.3],
        sfx=lambda L: [(0.0, 'ding'), (L[1] + 0.3, 'pop'), (L[2] + 0.3, 'pop'), (L[3] + 0.3, 'pop'),
                       (L[4] + 0.3, 'ding')],
    )],
    'ep02_short_price': lambda: [dict(
        draw=price_draw, vertical=True, lead=0.1, gap=0.25, tail=0.9, lines=[
            f"!In 1970, the typical new home in America cost about ${round(E.P1970, -3):,.0f}. Today it's about "
            f"${round(E.P_NOW, -3):,.0f}.",
            "Even after adjusting for inflation, that's almost twice as expensive.",
            "A better way to measure it is how many years of income a home costs.",
            f"In 1984, it was about {E.R1984:.1f} years of a typical household's income.",
            f"!By 2022, almost {E.R2022:.0f} years. Today, it's still about {E.R_LAST:.1f}.",
        ],
        punch=lambda L: [0.05, L[1] + 0.4, L[4] + 0.2],
        sfx=lambda L: [(0.0, 'pop'), (L[1] + 0.4, 'ding'), (L[2] + 0.5, 'pop'), (L[3] + 0.3, 'pop'),
                       (L[4] + 0.2, 'ding'), (L[4] + 2.5, 'pop')],
    )],
    'ep02_short_payment': lambda: [dict(
        draw=payment_draw, vertical=True, lead=0.1, gap=0.25, tail=0.9, lines=[
            f"!Same house. ${round(E.PAY_NOW) - round(E.PAY_2021):,} more, every single month.",
            f"In 2021, 30-year mortgage rates averaged about {E.RA[2021]:.1f}%.",
            f"On the typical new home, with 20% down, the payment was about ${E.PAY_2021:,.0f} a month.",
            f"Now rates are around {E.RATE_Y[-1]:.1f}%, and that payment is about ${E.PAY_NOW:,.0f}.",
            f"!That's a jump from about {E.SHARE_2021:.0f}% to about {E.SHARE_NOW:.0f}% of a typical household's "
            "income.",
            "Houses didn't just get pricier. Money did.",
        ],
        punch=lambda L: [0.05, L[3] + 1.5, L[4] + 0.3],
        sfx=lambda L: [(0.0, 'pop'), (L[1] + 0.4, 'pop'), (L[2] + 0.4, 'pop'), (L[3] + 0.3, 'pop'),
                       (L[4] + 0.3, 'ding'), (L[5] + 1.5, 'down')],
    )],
    'ep02_short_supply': lambda: [dict(
        draw=supply_draw, vertical=True, lead=0.1, gap=0.25, tail=0.9, lines=[
            "!America stopped building homes, and you're paying for it.",
            f"In the 1970s, builders started about {dict(E.DECADES)[1970] / 1000:.2f} million homes a year.",
            f"After the 2008 crash, the 2010s averaged under 1 million a year, the lowest of any decade in the data.",
            "Meanwhile, the population kept growing.",
            "!Fewer new homes, more people. That pushes prices up.",
            "And in many places, local rules make it hard to build more.",
        ],
        punch=lambda L: [0.05, L[2] + 0.5, L[4] + 0.3],
        sfx=lambda L: [(0.0, 'pop'), (L[1] + 0.2, 'whoosh'), (L[2] + 0.5, 'down'), (L[3], 'pop'),
                       (L[4] + 0.3, 'ding'), (L[5] + 0.2, 'pop')],
    )],
    'ep04_short_cards': lambda: [dict(
        draw=cards_draw, vertical=True, lead=0.1, gap=0.25, tail=0.9, lines=[
            f"!If you carry a $5,000 balance on a credit card, you're paying about ${round(E.CC_COST, -1):,.0f} a "
            "year in interest.",
            f"The average credit card rate at banks is now about {E.CC_NOW:.1f}%.",
            f"That's about {['zero', 'one', 'two', 'three', 'four'][round(E.CC_NOW / E.P_NOW)]} times the prime "
            f"rate, which is {E.pct(E.P_NOW)}.",
            f"The Fed's latest hike added a quarter point. On $5,000, that's only about ${E.QUARTER:.2f} more a year.",
            f"!The real problem isn't the hike. It's the {E.CC_NOW:.0f}%.",
            f"Every dollar of card debt you pay off stops costing you {E.CC_NOW:.0f}% a year.",
        ],
        punch=lambda L: [0.05, L[1] + 0.8, L[2] + 2.0, L[4] + 0.6],
        sfx=lambda L: [(0.0, 'pop'), (L[1] + 0.8, 'ding'), (L[2] + 0.2, 'pop'), (L[2] + 2.0, 'ding'),
                       (L[3] + 0.3, 'pop'), (L[3] + 2.4, 'pop'), (L[4] + 0.6, 'down'), (L[5], 'whoosh')],
    )],
    'ep04_short_savings': lambda: [dict(
        draw=savings_draw, vertical=True, lead=0.1, gap=0.25, tail=0.9, lines=[
            f"!Your savings account probably pays {E.pct(E.S_NOW)}. Prices are rising {E.CPI_NOW:.1f}%.",
            "That's the national average savings rate, according to the FDIC.",
            f"So money sitting there loses about {E.REAL_LOSS:.1f}% of its buying power every year.",
            f"On a $10,000 emergency fund, {E.pct(E.S_NOW)} earns about ${E.EF_NOW:.0f} a year.",
            f"!At 3.5%, the same money would earn about ${E.EF_ALT:.0f}.",
            "Many online banks pay rates much closer to the Fed's, and FDIC insurance covers deposits up to "
            "$250,000 per bank.",
        ],
        punch=lambda L: [0.05, L[2] + 1.0, L[4] + 0.3, L[5] + 5.0],
        sfx=lambda L: [(0.0, 'pop'), (L[1] + 0.5, 'ding'), (L[2] + 1.0, 'down'), (L[3] + 0.5, 'pop'),
                       (L[4] + 0.3, 'ding'), (L[4] + 0.6, 'pop'), (L[5], 'whoosh'), (L[5] + 5.0, 'pop')],
    )],
    'ep04_short_why': lambda: [dict(
        draw=why_draw, vertical=True, lead=0.1, gap=0.25, tail=0.9, lines=[
            "!Gas prices went up, so the Fed raised interest rates. Here's why that makes sense.",
            "After the war with Iran stopped tankers in the Strait of Hormuz, oil and gas prices soared.",
            f"Inflation climbed from about {E.CPI_FEB:.1f}% in February to {E.CPI_NOW:.1f}% in September, almost "
            "double the Fed's 2% target.",
            "Higher rates make borrowing more expensive, so people spend a little less, and prices cool down.",
            "!But rates can't pump more oil.",
            "They can only slow spending, so a fuel shock doesn't spread into higher prices for everything.",
        ],
        punch=lambda L: [0.05, L[1] + 1.5, L[4] + 0.5],
        sfx=lambda L: [(0.0, 'pop'), (L[1] + 1.5, 'down'), (L[2] + 0.3, 'pop'), (L[3] + 0.2, 'pop'),
                       (L[4] + 0.5, 'down'), (L[5], 'whoosh')],
    )],
    'ep03_short_feathers': lambda: [dict(
        draw=feathers_draw, vertical=True, lead=0.1, gap=0.25, tail=0.9, lines=[
            f"!When oil went up this year, gas jumped {E.money(E.UP_GAS)} a gallon. When oil fell, gas only dropped "
            f"{round(E.DN_GAS * 100)} cents.",
            f"From January to the spring peak, oil rose about {E.money(E.UP_CRUDE)} for every gallon's worth of "
            "crude.",
            f"But pump prices rose even more: {E.money(E.UP_GAS)}.",
            f"Then, from April to July, oil fell about {E.money(E.DN_CRUDE)} a gallon.",
            f"!Pump prices? Only {round(E.DN_GAS * 100)} cents.",
            "Economists call this rockets and feathers. Up like a rocket, down like a feather.",
            "Stations raise prices fast to cover their next, pricier delivery, but cut them slowly, because drivers "
            "stop shopping around when prices fall.",
            "So when gas jumps overnight but takes weeks to come down, now you know why.",
        ],
        punch=lambda L: [0.05, L[2] + 0.3, L[4] + 0.2, L[5] + 0.3],
        sfx=lambda L: [(0.0, 'pop'), (L[1] + 0.8, 'pop'), (L[2] + 0.3, 'ding'), (L[3] + 0.8, 'pop'),
                       (L[4] + 0.2, 'down'), (L[5] + 0.3, 'whoosh'), (L[6] + 0.3, 'pop'), (L[6] + 2.2, 'pop')],
    )],
    'ep03_short_barrel': lambda: [dict(
        draw=barrel_draw, vertical=True, lead=0.1, gap=0.25, tail=0.9, lines=[
            f"!Out of the {E.money(E.G_NOW)} you pay for a gallon of gas, about {E.money(E.CRUDE_GAL)} is just the "
            "crude oil.",
            f"A barrel holds 42 gallons, and a barrel costs about ${E.O_NOW:.0f} right now.",
            f"Divide one by the other, and you get {E.money(E.CRUDE_GAL)} a gallon, before anything else.",
            f"!That's about {E.CRUDE_SHARE:.0f}% of your gas price.",
            "The rest pays for refining, trucking, the station, and taxes.",
            "The federal gas tax is only 18.4 cents a gallon, and it hasn't changed since 1993.",
            "So when oil jumps, the price on this pump jumps too.",
        ],
        punch=lambda L: [L[0] + 2.2, L[2] + 1.6, L[3] + 0.3, L[5] + 0.2],
        sfx=lambda L: [(0.0, 'pop'), (L[0] + 2.2, 'ding'), (L[1] + 0.6, 'whoosh'), (L[2] + 1.6, 'ding'),
                       (L[3] + 0.3, 'pop'), (L[4] + 0.5, 'pop'), (L[5] + 0.2, 'ding'), (L[6] + 0.3, 'whoosh')],
    )],
}


def check(name):
    """The episode's own number checks, plus the script's numbers against its data."""
    E.check_numbers()
    script = ' '.join(l for sc in SHORTS2[name]() for l in sc['lines'])
    if name == 'ep03_short_barrel':
        assert abs(E.O_NOW / 42 - E.CRUDE_GAL) < 0.005 and f'{E.CRUDE_SHARE:.0f}%' == '58%' and '58%' in script
        assert '18.4 cents' in script and 'since 1993' in script
    if name == 'ep05_short_layoffs':
        assert E.L_NOW < E.L19 and round(E.RATE_NOW) == 1 and round(E.L_MAX / 1000) == 13 and 'Almost 13 million' in script
    if name == 'ep05_short_hiring':
        assert round(E.R_PEAK) == 2 and round(E.R_NOW) == 1 and E.H_NOW < E.H19 and E.W_NOW > E.W19
    if name == 'ep01_short_prices':
        assert round(100 * E.ANNUAL[1970] / E.LATEST) == 12 and all(E.money(p1) in script for *_r, p0, p1 in E.PRICES)
    if name == 'ep01_short_wages':
        assert 9.5 <= E.WAGE.iloc[-1] / E.WAGE_1970 < 10 and 'Almost ten times' in script
    if name == 'ep01_short_rule70':
        assert E.AVG_SINCE_1970 < 4 and 'almost 4%' in script and 70 / 4 == 17.5
    if name == 'ep02_short_price':
        assert 1.8 < E.P_NOW / E.P1970_REAL < 2 and 'almost twice' in script and 5.5 < E.R2022 < 6
    if name == 'ep02_short_payment':
        assert round(E.PAY_NOW) - round(E.PAY_2021) == 876 and '$876 more' in script and round(E.SHARE_2021) == 22 and round(E.SHARE_NOW) == 30
    if name == 'ep02_short_supply':
        d = dict(E.DECADES)
        assert d[2010] < 1000 and d[2010] == min(d.values()) and 'lowest of any decade' in script
    if name == 'ep08_short_midterms':
        assert len(E.MID) == 18 and round(E.AVG) == 18 and round(E.OTHER_AVG) == 6
        assert round(E.Y22_SLUMP, 1) == -18.5 and 'Right now' in script
    if name == 'ep04_short_cards':
        assert round(E.CC_NOW / E.P_NOW) == 3 and 'about three times' in script and E.QUARTER == 12.5
        assert f'${round(E.CC_COST, -1):,.0f}' in script
    if name == 'ep04_short_savings':
        assert abs(E.CPI_NOW - E.S_NOW - E.REAL_LOSS) < 0.05 and E.EF_NOW == 38 and E.EF_ALT == 350
    if name == 'ep04_short_why':
        assert E.CPI_NOW / 2 > 1.8 and 'almost double' in script and f'{E.CPI_FEB:.1f}%' == '2.4%'
    if name == 'ep03_short_feathers':
        assert E.UP_GAS > E.UP_CRUDE and E.DN_GAS < E.DN_CRUDE and 'rose even more' in script
        assert f'{round(E.DN_GAS * 100)} cents' in script and E.money(E.UP_GAS) in script


if __name__ == '__main__':
    check(NAME)
    scenes = SHORTS2[NAME]()
    if '--stills' in sys.argv:
        out = os.path.join(HERE, 'build', EPN, 'v2_previews')
        os.makedirs(out, exist_ok=True)
        n = len(scenes[0]['lines'])
        for i in range(n):
            still(scenes[0], 0.5 + 4 * i + 3.0, os.path.join(out, f'{NAME}_{i}.png'), layout='short')
        print('previews in', out)
        sys.exit()
    build(scenes, os.path.join(HERE, 'out', f'{NAME}.mp4'), os.path.join(HERE, 'build', EPN, NAME + '_v2'),
          layout='short', loop=True)
