"""Episode 7 (long): the Binance hack. Built from confirmed facts only, as reported up to Nov 1, 2026.

    python3 channel/ep07_long.py [--hook-only] [--stills]

The opening uses a Google Flow clip made by the channel owner (assets/flow/binance_vault_clip.mp4) under our own
narration, captions and graphics; its own audio is not used. Every number lives in L below (or F in ep07_binance.py)
with its source, and check_numbers() refuses to render if the narration disagrees with it. Anything that is a
company's or an analyst's claim is said to be one.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from wk2_art import *  # noqa: E402,F401,F403
from engine import build, previews  # noqa: E402
from ep07_binance import F  # noqa: E402

OUT = os.path.join(HERE, 'out')
BUILD = os.path.join(HERE, 'build', 'ep07_long')
CLIP = os.path.join(HERE, 'assets', 'flow', 'binance_vault_clip.mp4')
BOOM = 2.55 / 0.72  # when the vault door blows open (clip played at 0.72x speed)

LONGF = {
    # biggest crypto thefts, US$ billions at the time (Decrypt, Benzinga, Cointelegraph lists; FBI for Bybit)
    'record': (('Mt. Gox', 2014, 0.46), ('Poly Network', 2021, 0.61), ('Ronin', 2022, 0.625),
               ('Bybit', 2025, 1.5), ('Binance', 2026, 6.3)),
    'nk_2025_bn': 2.02,       # Chainalysis, Dec 18 2025: North Korea-linked thefts in 2025 (record year)
    'nk_share_2025': 59,      # ... about 59% of all crypto stolen in 2025 (Chainalysis)
    'covered_sat': 90,        # Binance, Oct 31: backing restored for about 90% of affected assets (CNBC)
    'covered_sun': 95,        # Binance, Nov 1: 95% covered (TechCrunch, Nov 1)
    'top_coins': 10,          # BTC, ETH, USDT, BNB, SOL, USDC, XRP, USD1, RLUSD, ZEC "fully backed 100%" (CNBC)
}
LF = LONGF
SRC = 'Binance; FBI; TRM Labs; CNBC; TechCrunch (Oct 29 - Nov 1, 2026)'


# ------------------------------------------------------------------ scenes --
def s_hook(c, x):
    """Over the Flow clip: the number lands the moment the vault blows."""
    t, L = x.t, x.L
    k = pop(t, BOOM)
    if k > 0:
        c.text(640, 300, f'${F["amount_bn"]} BILLION', int(120 * (0.6 + 0.4 * clamp(k))), GOLD, 900, a=clamp(k),
               stroke=8)
    k2 = pop(t, BOOM + 1.6)
    if k2 > 0:
        c.rrect(420, 370, 860, 440, 34, CORAL, a=clamp(k2))
        c.text(640, 405, f'GONE IN ABOUT {F["minutes"]} MINUTES', 30, INK, 900, a=clamp(k2), shadow=False)
    if len(L) > 1 and t > L[1]:
        penny(c, 1120, 600, 70, t, 'shocked', look=(-1, -0.3), talk=x.talk(), a=fade(t, L[1]))


def s_record(c, x):
    t, L = x.t, x.L
    specks(c, t, 71)
    c.text(640, 60, 'The biggest crypto thefts ever (US$, at the time)', 30, WHITE, 900, a=fade(t, 0))
    vmax, x0, x1 = 6.6, 330, 1150
    for i, (name, yr, v) in enumerate(LF['record']):
        at = L[0] + 0.6 + i * 1.3 if i < 4 else L[1] + 0.3
        if t < at:
            continue
        g = ease(seg(t, at, at + 0.9 if i < 4 else at + 2.2))
        y = 150 + i * 88
        col = CORAL if name == 'Binance' else (SKY if name == 'Bybit' else MUTED)
        c.text(x0 - 20, y, name, 28, WHITE, 900, anchor='rm')
        c.text(x0 - 20, y + 28, str(yr), 18, MUTED, 700, anchor='rm', shadow=False)
        c.rrect(x0, y - 26, x0 + max(14, (x1 - x0) * v / vmax * g), y + 26, 12, col)
        c.text(x0 + (x1 - x0) * v / vmax * g + 16, y, f'${v * g:.2f}B' if v < 1 else f'${v * g:.1f}B', 26,
               col, 900, anchor='lm')
    if t > L[2]:
        chip(c, 420, 580, f'about {round(F["amount_bn"] / F["bybit_bn"])}x the old record', GOLD,
             pop(t, L[2] + 0.4), 26)
    if t > L[3]:
        chip(c, 420, 640, f'more than North Korea stole in all of 2025 (${LF["nk_2025_bn"]:.2f}B)', SKY,
             pop(t, L[3] + 0.5), 22)
    source(c, t, 'Decrypt, Benzinga, FBI, Chainalysis, Binance')


def s_exchange(c, x):
    t, L = x.t, x.L
    specks(c, t, 72)
    c.text(640, 60, 'Where an exchange keeps your crypto', 34, WHITE, 900, a=fade(t, 0))
    # you -> exchange
    k = pop(t, L[0] + 0.5)
    if k > 0:
        c.icon('users', 170, 300, 110 * k, WHITE)
        c.text(170, 390, 'customers', 24, WHITE, 800, a=clamp(k))
        c.icon('arrow-right', 300, 300, 60 * k, MUTED)
        c.icon('building-2', 440, 300, 130 * k, GOLD)
        c.text(440, 400, 'the exchange', 24, GOLD, 900, a=clamp(k))
    k = pop(t, L[1] + 0.4)
    if k > 0:  # cold
        c.rrect(640, 150, 1180, 300, 24, (255, 255, 255, 16), SKY, 3, a=clamp(k))
        c.icon('snowflake', 720, 225, 80 * k, SKY)
        c.text(960, 200, 'COLD storage', 34, SKY, 900, a=clamp(k))
        c.text(960, 245, 'offline, most of the money', 24, WHITE, 800, a=clamp(k))
    k = pop(t, L[2] + 0.4)
    if k > 0:  # hot
        c.rrect(640, 330, 1180, 480, 24, (255, 255, 255, 16), CORAL, 3, a=clamp(k))
        c.icon('flame', 720, 405, 80 * k, CORAL)
        c.text(960, 380, 'HOT wallets', 34, CORAL, 900, a=clamp(k))
        c.text(960, 425, 'online, pays out withdrawals', 24, WHITE, 800, a=clamp(k))
    if t > L[3]:
        chip(c, 910, 540, 'this time: the hot wallets were drained', CORAL, pop(t, L[3] + 0.4), 24)
        c.icon('arrow-down', 1150, 490, 44 * clamp(pop(t, L[3] + 0.4)), CORAL)
    if t > L[3] + 3.5:
        penny(c, 170, 560, 48, t, 'worried', look=(1, 0), talk=x.talk(), a=fade(t, L[3] + 3.5))
    source(c, t, 'CNBC; Binance')


def s_how(c, x):
    t, L = x.t, x.L
    specks(c, t, 73)
    c.text(640, 60, 'How they got in: what Binance has said so far', 32, WHITE, 900, a=fade(t, 0))
    steps = [('laptop', "an engineer's\nlaptop", CORAL, L[0] + 0.8), ('container', 'a service\ncontainer', GOLD,
                                                                        L[0] + 4.0),
             ('key', 'no sign the\nprivate keys leaked', MINT, L[1] + 0.5)]
    for i, (ic, lab, col, at) in enumerate(steps):
        k = pop(t, at)
        if k <= 0:
            continue
        cx = 230 + i * 410
        c.circle(cx, 260, 95 * k, (255, 255, 255, 18), col, 3)
        c.icon(ic, cx, 260, 90 * k, col)
        for j, part in enumerate(lab.split('\n')):
            c.text(cx, 400 + j * 34, part, 26, WHITE, 900, a=clamp(k))
        if i < 2:
            c.icon('arrow-right', cx + 205, 260, 54 * clamp(pop(t, steps[i + 1][3] - 0.3)), MUTED)
    if t > L[2]:
        chip(c, 640, 540, 'Co-CEO Richard Teng: "more complex" than one engineer', GOLD, pop(t, L[2] + 0.4), 24)
    if t > L[2] + 4.0:
        c.text(640, 610, 'the full incident report is still to come', 24, MUTED, 800, a=fade(t, L[2] + 4.0))
    source(c, t, 'Binance; CNBC')


def s_burst(c, x):
    t, L = x.t, x.L
    specks(c, t, 74)
    c.text(640, 60, 'Planned in advance, fired in one burst', 34, WHITE, 900, a=fade(t, 0))
    # a timeline: weeks of quiet staging, then everything at once
    y = 330
    g = ease(seg(t, L[0] + 0.5, L[0] + 5.0))
    c.line([(120, y), (120 + 1040 * g, y)], (255, 255, 255, 110), 4)
    for i in range(7):
        k = pop(t, L[0] + 0.8 + i * 0.6)
        if k > 0:
            cx = 150 + i * 110
            c.circle(cx, y, 12 * k, MUTED)
    if t > L[0] + 1.2:
        c.text(480, y - 60, 'staging: weeks before', 26, MUTED, 900, a=fade(t, L[0] + 1.2))
    k = pop(t, L[1] + 0.3)
    if k > 0:
        c.circle(1030, y, 60 * k, CORAL, WHITE, 4)
        c.icon('zap', 1030, y, 60 * k, WHITE)
        c.text(1030, y - 100, 'one burst', 30, CORAL, 900, a=clamp(k))
    if t > L[2]:
        for i in range(F['chains']):  # ~10 blockchains at once
            kk = ease(seg(t, L[2] + 0.3 + i * 0.12, L[2] + 1.1 + i * 0.12))
            if kk <= 0:
                continue
            ang = math.pi * (0.1 + 0.8 * i / (F['chains'] - 1))
            ex, ey = 1030 + math.cos(ang) * 170 * kk, y + math.sin(ang) * 190 * kk
            c.line([(1030, y), (ex, ey)], (255, 255, 255, 70), 3)
            c.circle(ex, ey, 16, SKY, WHITE, 2)
        chip(c, 470, 470, f'about {F["chains"]} blockchains', SKY, pop(t, L[2] + 1.2), 28)
        chip(c, 470, 540, f'about {F["minutes"]} minutes', CORAL, pop(t, L[2] + 3.0), 28)
    source(c, t, 'TRM Labs (via CNBC)')


def s_launder(c, x):
    t, L = x.t, x.L
    specks(c, t, 75)
    if t < L[2]:
        c.text(640, 60, 'Step two: hide the money', 34, WHITE, 900, a=fade(t, 0))
        coins = [('USDT', SKY), ('BNB', GOLD), ('SOL', MINT), ('XRP', MUTED), ('more', MUTED)]
        for i, (lab, col) in enumerate(coins):
            at = L[0] + 0.6 + i * 0.4
            g = ease(seg(t, L[1] + 0.3 + i * 0.2, L[1] + 1.6 + i * 0.2))
            if t < at:
                continue
            x0, y0 = 220, 160 + i * 80
            cx, cy = x0 + (860 - x0) * g, y0 + (320 - y0) * g
            c.circle(cx, cy, 30, col, WHITE, 2, a=1 - 0.8 * g)
            c.text(cx, cy, lab, 16, INK, 900, a=1 - 0.8 * g, shadow=False)
        k = pop(t, L[1] + 0.3)
        if k > 0:
            c.circle(900, 320, 90 * k, (120, 130, 255), WHITE, 4)
            c.text(900, 320, 'ETH', int(48 * clamp(k)), WHITE, 900)
            c.text(900, 450, 'converted mostly into Ethereum', 26, WHITE, 900, a=clamp(k))
        if t > L[1] + 3.5:
            chip(c, 900, 520, 'FBI: more laundering steps expected', CORAL, pop(t, L[1] + 3.5), 22)
        source(c, t, 'FBI (Oct 31); TRM Labs')
        return
    c.text(640, 60, "Some crypto can be frozen. Some can't.", 34, WHITE, 900, a=fade(t, L[2]))
    k = pop(t, L[2] + 0.5)
    if k > 0:
        c.rrect(110, 150, 600, 470, 26, (255, 255, 255, 14), SKY, 3, a=clamp(k))
        c.icon('snowflake', 355, 250, 110 * k, SKY)
        c.text(355, 370, 'Stablecoins (USDT, USDC)', 28, WHITE, 900, a=clamp(k))
        c.text(355, 410, 'the issuer can freeze them', 24, SKY, 800, a=clamp(k))
    k = pop(t, L[3] + 0.3)
    if k > 0:
        c.rrect(680, 150, 1170, 470, 26, (255, 255, 255, 14), CORAL, 3, a=clamp(k))
        c.icon('ban', 925, 250, 110 * k, CORAL)
        c.text(925, 370, 'Bitcoin and Ethereum', 28, WHITE, 900, a=clamp(k))
        c.text(925, 410, 'no one can freeze them', 24, CORAL, 800, a=clamp(k))
    if t > L[4]:
        chip(c, 640, 550, f'about ${F["frozen_bn"]:.0f}B frozen so far (Binance)', SKY, pop(t, L[4] + 0.4), 28)
    source(c, t, 'Binance; Tether; Circle')


def s_who(c, x):
    t, L = x.t, x.L
    specks(c, t, 76)
    if t < L[2]:
        c.icon('landmark', 330, 260, 150, SKY, a=fade(t, L[0]))
        c.text(330, 390, 'FBI, October 31', 30, SKY, 900, a=fade(t, L[0] + 0.3))
        k = pop(t, L[0] + 2.0)
        if k > 0:
            c.text(860, 230, 'NORTH KOREA', int(70 * (0.6 + 0.4 * clamp(k))), CORAL, 900, a=clamp(k), stroke=5)
            c.text(860, 310, 'a group known as TraderTraitor', 28, WHITE, 900, a=clamp(k))
        if t > L[1]:
            chip(c, 640, 500, 'same playbook as Bybit (2025) and KelpDAO (April 2026)', GOLD, pop(t, L[1] + 0.5),
                 24)
        if t > L[1] + 4.0:
            c.text(640, 570, 'small Tornado Cash withdrawals, staging long before the theft', 22, MUTED, 800,
                   a=fade(t, L[1] + 4.0))
        source(c, t, 'FBI; TRM Labs (via CNBC)')
        return
    c.text(640, 60, 'North Korea and crypto theft', 34, WHITE, 900, a=fade(t, L[2]))
    k = pop(t, L[2] + 0.6)
    if k > 0:
        c.text(400, 260, f'${LF["nk_2025_bn"]:.2f}B', int(110 * (0.6 + 0.4 * clamp(k))), CORAL, 900, a=clamp(k),
               stroke=6)
        c.text(400, 350, 'stolen in 2025, a record', 28, WHITE, 900, a=clamp(k))
    k = pop(t, L[3] + 0.4)
    if k > 0:
        c.text(900, 260, f'{LF["nk_share_2025"]}%', int(110 * (0.6 + 0.4 * clamp(k))), GOLD, 900, a=clamp(k),
               stroke=6)
        c.text(900, 350, 'of all crypto stolen that year', 28, WHITE, 900, a=clamp(k))
    if t > L[4]:
        chip(c, 640, 480, 'UN experts: the money helps fund weapons programs', CORAL, pop(t, L[4] + 0.4), 24)
    if t > L[4] + 3.6:
        penny(c, 110, 560, 50, t, 'worried', look=(1, 0), talk=x.talk(), a=fade(t, L[4] + 3.6))
    source(c, t, 'Chainalysis (Dec 2025); UN Panel of Experts')


def s_pays(c, x):
    t, L = x.t, x.L
    specks(c, t, 77)
    c.text(640, 60, 'Who pays? Binance says: not the customers', 34, WHITE, 900, a=fade(t, 0))
    items = [('shield-check', 'SAFU\nemergency fund', L[1] + 0.3), ('scale', 'futures\ninsurance fund', L[1] + 2.0),
             ('building-2', 'company\ntreasury', L[1] + 3.6)]
    for i, (ic, lab, at) in enumerate(items):
        k = pop(t, at)
        if k <= 0:
            continue
        cx = 260 + i * 380
        c.circle(cx, 230, 80 * k, (255, 255, 255, 18), MINT, 3)
        c.icon(ic, cx, 230, 76 * k, MINT)
        for j, part in enumerate(lab.split('\n')):
            c.text(cx, 345 + j * 32, part, 26, WHITE, 900, a=clamp(k))
    if t > L[2]:  # coverage bar: 90% Saturday, 95% Sunday
        x0, x1, y0 = 140, 1140, 450
        c.rrect(x0, y0, x1, y0 + 56, 18, (255, 255, 255, 25), a=fade(t, L[2]))
        g = ease(seg(t, L[2] + 0.4, L[2] + 2.0))
        pct = LF['covered_sat'] + (LF['covered_sun'] - LF['covered_sat']) * ease(seg(t, L[3] + 0.3, L[3] + 1.5))
        c.rrect(x0, y0, x0 + (x1 - x0) * pct / 100 * g, y0 + 56, 18, MINT)
        c.text(640, y0 + 28, f'{pct * g:.0f}% covered', 30, INK, 900, shadow=False)
        day = 'Saturday' if t < L[3] + 0.3 else 'Sunday'
        c.text(640, y0 + 92, day, 24, MUTED, 800)
    if t > L[4]:
        chip(c, 420, 620, f'top {LF["top_coins"]} coins fully backed; the rest being bought', GOLD,
             pop(t, L[4] + 0.4), 22)
    source(c, t, 'Binance via CNBC, TechCrunch')


def s_withdraw(c, x):
    t, L = x.t, x.L
    specks(c, t, 78)
    c.text(640, 60, 'Can people get their money out?', 34, WHITE, 900, a=fade(t, 0))
    k = pop(t, L[0] + 0.4)
    if k > 0:
        chip(c, 640, 150, 'Oct 29: deposits and withdrawals paused', CORAL, k, 26)
    nets = [('Bitcoin', 'bitcoin', GOLD), ('Ethereum', 'link', SKY), ('BNB Smart Chain', 'coins', GOLD)]
    for i, (lab, ic, col) in enumerate(nets):
        at = L[1] + 0.6 + i * 1.6
        kk = pop(t, at)
        if kk <= 0:
            continue
        cx = 280 + i * 360
        c.circle(cx, 320, 70 * kk, (255, 255, 255, 18), MINT, 3)
        c.icon(ic, cx, 320, 64 * kk, col)
        c.text(cx, 425, lab, 26, WHITE, 900, a=clamp(kk))
        c.icon('check', cx + 55, 270, 40 * kk, MINT, stroke=3)
    if t > L[2]:
        chip(c, 640, 520, 'Nov 1: back in phases, with delays', MINT, pop(t, L[2] + 0.3), 26)
    if t > L[2] + 3.4:
        c.text(420, 590, 'Binance: a fuller incident report will follow', 24, MUTED, 800, a=fade(t, L[2] + 3.4))
    source(c, t, 'Binance; CNBC; TechCrunch (Nov 1)')


def s_market(c, x):
    t, L = x.t, x.L
    specks(c, t, 79)
    c.icon('bitcoin', 360, 280, 190, GOLD, a=fade(t, 0))
    k = pop(t, L[0] + 0.8)
    if k > 0:
        c.icon('trending-down', 560, 320, 120 * k, CORAL, stroke=2.5)
    c.text(860, 230, 'Bitcoin briefly fell', 36, WHITE, 900, a=fade(t, L[0] + 0.5))
    c.text(860, 300, f'below ${F["btc_below"]:,}', 64, CORAL, 900, a=fade(t, L[0] + 1.0), stroke=4)
    if t > L[1]:
        chip(c, 640, 480, 'a scare, not a collapse', GOLD, pop(t, L[1] + 0.4), 28)
    if t > L[1] + 3.0:
        penny(c, 110, 560, 50, t, 'happy', look=(1, 0), talk=x.talk(), a=fade(t, L[1] + 3.0))
    source(c, t, 'CoinDesk, The Block (Oct 29)')


def s_lessons(c, x):
    t, L = x.t, x.L
    specks(c, t, 80)
    c.text(640, 60, 'What this teaches (not financial advice)', 34, WHITE, 900, a=fade(t, 0))
    items = [('building-2', 'On an exchange,\nthey hold the keys'), ('shield-check', 'Reserves and insurance\n'
                                                                    'funds matter'),
             ('fish', 'After a hack,\nscammers pose as support'), ('key', 'Holding it yourself\nhas risks too')]
    for i, (ic, lab) in enumerate(items):
        k = pop(t, L[i + 1] + 0.3)
        if k <= 0:
            continue
        cx = 170 + i * 313
        c.circle(cx, 260, 80 * k, (255, 255, 255, 18), GOLD, 3)
        c.icon(ic, cx, 260, 72 * k, GOLD)
        for j, part in enumerate(lab.split('\n')):
            c.text(cx, 375 + j * 30, part, 22, WHITE, 900, a=clamp(k))
    if t > L[3] + 3.0:
        chip(c, 640, 540, 'real support never asks for your password or recovery phrase', CORAL,
             pop(t, L[3] + 3.0), 22)


def s_end(c, x):
    t, L = x.t, x.L
    specks(c, t, 81)
    if t < L[1]:
        rows = [(f'${F["amount_bn"]}B', 'stolen, a record', CORAL, L[0] + 0.5),
                (f'~{F["minutes"]} min', 'one planned burst', GOLD, L[0] + 3.0),
                ('FBI', 'North Korea', SKY, L[0] + 5.5),
                (f'{LF["covered_sun"]}%', 'covered by Binance so far', MINT, L[0] + 8.0)]
        for i, (big_t, small, col, at) in enumerate(rows):
            k = pop(t, at)
            if k <= 0:
                continue
            y = 130 + i * 115
            c.text(420, y, big_t, int(64 * (0.6 + 0.4 * clamp(k))), col, 900, anchor='rm', a=clamp(k), stroke=4)
            c.text(460, y, small, 32, WHITE, 900, anchor='lm', a=clamp(k))
        return
    k = pop(t, L[1] + 0.3)
    c.text(640, 250, 'Would you keep crypto on an exchange?', int(52 * (0.6 + 0.4 * clamp(k))), GOLD, 900,
           a=clamp(k), stroke=5)
    c.text(640, 340, 'Tell me in the comments', 32, WHITE, 900, a=fade(t, L[1] + 1.0))
    penny(c, 640, 525, 60, t, 'happy', wave=True, talk=x.talk())


B63 = '{$6.3 billion|six point three billion dollars}'
SCENES = [
    dict(draw=s_hook, chapter='Intro: $6.3 billion in 20 minutes', bg_video=CLIP, bg_speed=0.72, lead=0.3, gap=0.3,
         tail=0.6, cam=(1.0, 1.1), lines=[
             f"!{{$6.3 billion|Six point three billion dollars}}. Gone, in about {F['minutes']} minutes.",
             "This is the biggest crypto theft in history. Here's exactly how it happened, who did it, and what it "
             "means for anyone who keeps money on an exchange.",
         ], punch=lambda L: [BOOM, BOOM + 1.6], sfx=lambda L: [(BOOM, 'down'), (BOOM + 1.6, 'pop')]),
    dict(draw=s_record, chapter='How big is this?', lines=[
        "First, how big is this? Here are the biggest crypto thefts ever. Mt. Gox in 2014, about 460 million "
        "dollars. Poly Network and Ronin, a little over 600 million each. Bybit in 2025, about 1.5 billion.",
        f"!And Binance: about {B63}.",
        f"That's roughly four times the old record.",
        f"It's even more than North Korea stole in all of 2025, which was already a record at about "
        f"{LF['nk_2025_bn']:.2f} billion dollars.",
    ], punch=lambda L: [L[1] + 0.3], sfx=lambda L: [(L[0] + 0.6, 'pop'), (L[0] + 1.9, 'pop'), (L[0] + 3.2, 'pop'),
                                                    (L[0] + 4.5, 'pop'), (L[1] + 0.3, 'ding'), (L[2] + 0.4, 'pop'),
                                                    (L[3] + 0.5, 'pop')]),
    dict(draw=s_exchange, chapter='Hot wallets vs cold storage', lines=[
        "To understand how it happened, you need to know where an exchange keeps your crypto. When you buy on an "
        "exchange, the coins usually sit in wallets the exchange controls, not you.",
        "Most of it is kept in cold storage: offline, much harder to reach.",
        "But some has to stay online, in so-called hot wallets, so the exchange can pay out withdrawals quickly.",
        "This time, it was the hot wallets that were drained. That's where the attackers aimed.",
    ], sfx=lambda L: [(L[0] + 0.5, 'whoosh'), (L[1] + 0.4, 'pop'), (L[2] + 0.4, 'pop'), (L[3] + 0.4, 'down')]),
    dict(draw=s_how, chapter='How they got in', lines=[
        "So how did they get in? Binance's first findings point to one engineer's laptop. Hackers compromised it, "
        "and that gave them access to a service container, a piece of the exchange's internal systems.",
        "Binance says it has found no evidence that its private keys, the master passwords to its wallets, leaked.",
        "But Binance's co-CEO, Richard Teng, has said the attack was more complex than one engineer's access. The "
        "full incident report is still to come.",
    ], sfx=lambda L: [(L[0] + 0.8, 'pop'), (L[0] + 4.0, 'pop'), (L[1] + 0.5, 'pop'), (L[2] + 0.4, 'pop')]),
    dict(draw=s_burst, chapter='Planned in advance', lines=[
        "What we do know is that this was planned. Blockchain investigators at TRM Labs found the staging started "
        "well before the theft.",
        "!Then it all happened at once. In TRM's words: signatures obtained in advance, then executed in one "
        "burst.",
        f"The money moved across about {F['chains']} different blockchains, and most of it was gone in about "
        f"{F['minutes']} minutes.",
    ], punch=lambda L: [L[1] + 0.3], sfx=lambda L: [(L[0] + 0.5, 'whoosh'), (L[1] + 0.3, 'down'),
                                                    (L[2] + 0.3, 'whoosh'), (L[2] + 3.0, 'pop')]),
    dict(draw=s_launder, chapter='Hiding the money', lines=[
        "Step two for any thief is hiding the money. The stolen coins included all kinds of tokens.",
        "According to the FBI, the hackers have been converting them mostly into Ethereum, and it expects more "
        "laundering steps to follow.",
        "Here's why that matters. Some crypto can be frozen. Stablecoins like Tether and USDC are run by "
        "companies that can block stolen coins.",
        "Bitcoin and Ethereum have no company in charge. No one can freeze them.",
        f"So far, Binance says about {{$3 billion|three billion dollars}} has been frozen with help from partners "
        "including Tether and Circle.",
    ], sfx=lambda L: [(L[0] + 0.6, 'pop'), (L[1] + 0.3, 'whoosh'), (L[1] + 3.5, 'pop'), (L[2] + 0.5, 'pop'),
                      (L[3] + 0.3, 'down'), (L[4] + 0.4, 'ding')]),
    dict(draw=s_who, chapter='Who did it: North Korea', lines=[
        "Who did it? On October 31st, the FBI said North Korea was responsible, naming a hacking group known as "
        "TraderTraitor.",
        "Investigators say the attack follows the same playbook as the Bybit hack in 2025 and the KelpDAO hack "
        "this April, right down to how the attackers funded their wallets.",
        f"And this is a pattern. According to Chainalysis, North Korea-linked hackers stole about "
        f"{LF['nk_2025_bn']:.2f} billion dollars in crypto in 2025, a record.",
        f"That was about {LF['nk_share_2025']}% of all the crypto stolen worldwide that year.",
        "United Nations experts have said this stolen money helps fund the country's weapons programs.",
    ], punch=lambda L: [L[0] + 2.0], sfx=lambda L: [(L[0] + 2.0, 'down'), (L[1] + 0.5, 'pop'), (L[2] + 0.6, 'ding'),
                                                    (L[3] + 0.4, 'pop'), (L[4] + 0.4, 'pop')]),
    dict(draw=s_pays, chapter='Who pays for it?', lines=[
        "So who pays? Binance says it will absorb the losses, not its customers.",
        "It's using its emergency fund for users, called SAFU, part of its futures insurance fund, and money from "
        "its own treasury.",
        f"On Saturday, Binance said about {LF['covered_sat']}% of the affected assets were covered.",
        f"!By Sunday, it said {LF['covered_sun']}%.",
        f"The {LF['top_coins']} biggest coins, including bitcoin and ether, are fully backed, it says. The rest are "
        "smaller tokens it's still buying back.",
    ], punch=lambda L: [L[3] + 0.3], sfx=lambda L: [(L[1] + 0.3, 'pop'), (L[1] + 2.0, 'pop'), (L[1] + 3.6, 'pop'),
                                                    (L[2] + 0.4, 'whoosh'), (L[3] + 0.3, 'ding'),
                                                    (L[4] + 0.4, 'pop')]),
    dict(draw=s_withdraw, chapter='Can people withdraw?', lines=[
        "Right after the hack, Binance paused deposits and withdrawals.",
        "On Sunday, November 1st, withdrawals started coming back in phases: first the Bitcoin network, then "
        "Ethereum and BNB Smart Chain.",
        "Binance warned of delays, and says a fuller incident report will follow once its investigation is done.",
    ], sfx=lambda L: [(L[0] + 0.4, 'down'), (L[1] + 0.6, 'pop'), (L[1] + 2.2, 'pop'), (L[1] + 3.8, 'pop'),
                      (L[2] + 0.3, 'ding')]),
    dict(draw=s_market, chapter='What it did to bitcoin', lines=[
        f"The news hit the whole market. The night of the hack, bitcoin briefly fell below "
        f"${F['btc_below']:,}.",
        "It was a scare, not a collapse, but it shows how much of crypto runs through a single exchange.",
    ], sfx=lambda L: [(L[0] + 0.8, 'down'), (L[1] + 0.4, 'pop')]),
    dict(draw=s_lessons, chapter='What it means for you', lines=[
        "So what does this mean for you? We don't give financial advice, but this hack teaches four things.",
        "One: when your crypto sits on an exchange, the exchange holds the keys. You're trusting its security.",
        "Two: an exchange's reserves and insurance funds matter. They're why Binance customers may not lose money "
        "this time.",
        "Three: after every big hack, scammers pretend to be support staff. Real support will never ask for your "
        "password or your recovery phrase.",
        "Four: holding crypto yourself removes the exchange risk, but if you lose your own keys, nobody can get "
        "them back.",
    ], sfx=lambda L: [(L[1] + 0.3, 'pop'), (L[2] + 0.3, 'pop'), (L[3] + 0.3, 'pop'), (L[3] + 3.0, 'down'),
                      (L[4] + 0.3, 'pop')]),
    dict(draw=s_end, chapter='Recap', lines=[
        f"Let's recap. About {B63}, the biggest crypto theft ever, taken in one planned burst of about "
        f"{F['minutes']} minutes. The FBI says North Korea did it. And Binance says it has covered "
        f"{LF['covered_sun']}% so far, with its own money.",
        "!Would you keep your crypto on an exchange after this? Tell me in the comments, and subscribe so you "
        "don't miss the full incident report when it comes out.",
        "This video is for education only. It's not financial advice.",
    ], punch=lambda L: [L[1] + 0.3], sfx=lambda L: [(L[0] + 0.5, 'pop'), (L[0] + 3.0, 'pop'), (L[0] + 5.5, 'pop'),
                                                    (L[0] + 8.0, 'pop'), (L[1] + 0.3, 'ding')]),
]


def check_numbers():
    script = ' '.join(l for sc in SCENES for l in sc['lines'])
    rec = dict((n, v) for n, _, v in LF['record'])
    assert rec['Binance'] == F['amount_bn'] == 6.3 and rec['Bybit'] == F['bybit_bn'] == 1.5
    assert max(v for n, v in rec.items() if n != 'Binance') == F['bybit_bn'], 'Bybit must be the old record'
    assert round(F['amount_bn'] / F['bybit_bn']) == 4 and 'roughly four times the old record' in script
    assert F['amount_bn'] > LF['nk_2025_bn'] and f"{LF['nk_2025_bn']:.2f} billion" in script
    assert 'about 460 million' in script and 'a little over 600 million each' in script
    assert LF['covered_sat'] == 90 and LF['covered_sun'] == 95 and '90%' in script and '95%' in script
    assert F['frozen_bn'] == 3.0 and 'about {$3 billion' in script
    assert f"about {F['chains']} different blockchains" in script and f"about {F['minutes']} minutes" in script
    assert 'FBI said North Korea' in script and 'TraderTraitor' in script
    assert f"below ${F['btc_below']:,}" in script and 'briefly' in script
    assert 'not financial advice' in script.lower() or "don't give financial advice" in script
    print('numbers check: OK')


if __name__ == '__main__':
    check_numbers()
    os.makedirs(BUILD, exist_ok=True)
    if '--hook-only' in sys.argv:
        build(SCENES[:1], os.path.join(OUT, 'ep07_hook_test.mp4'), BUILD, layout='long')
        sys.exit()
    if '--stills' in sys.argv:
        previews(SCENES, {}, os.path.join(BUILD, 'previews'))
        sys.exit()
    total, chapters = build(SCENES, os.path.join(OUT, 'ep07_binance_long.mp4'), BUILD,
                            srt_path=os.path.join(OUT, 'ep07_binance_long.en.srt'))
    with open(os.path.join(OUT, 'ep07_chapters.txt'), 'w') as f:
        for at, name in chapters:
            f.write(f'{fmt_time(at)} {name}\n')
    print(f'total {total / 60:.1f} min')
