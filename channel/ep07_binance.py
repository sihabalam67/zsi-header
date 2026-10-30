"""Breaking news Short: the Binance hack (Oct 29, 2026). The long episode follows once the facts settle.

    python3 channel/ep07_binance.py [--stills]

Every number comes from FACTS below, each with its sources as reported on Oct 29-30, 2026. Where sources disagree,
the script uses Binance's own figure and says "about"; anything unconfirmed is said to be unconfirmed.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from wk2_art import *  # noqa: E402,F401,F403
from engine import build, previews  # noqa: E402

OUT = os.path.join(HERE, 'out')
BUILD = os.path.join(HERE, 'build', 'ep07')

FACTS = {
    # Binance's own estimate of the impact; other estimates: Bitcoin Magazine $5.8B, Chainalysis ~$5.9B,
    # Arkham $6.01B, TRM Labs $6.36B (CNBC, Forbes, Fox Business, Bitcoin Magazine, Unchained; Oct 29-30, 2026)
    'amount_bn': 6.3, 'estimates_bn': (5.8, 5.9, 6.01, 6.3, 6.36),
    'minutes': 20,          # most of it moved in about 20 minutes (TRM Labs via CNBC, Unchained)
    'chains': 10,           # TRM Labs: ~10 networks (Arkham counts 9)
    'bybit_bn': 1.5,        # previous record: Bybit, Feb 21 2025, ~$1.5B (FBI PSA I-022625-PSA)
    'bybit_year': 2025,
    'frozen_bn': 3.0,       # Binance: ~$3B frozen with partners incl. Tether and Circle (TRM: ~$2.7B)
    'btc_below': 77000,     # bitcoin briefly fell below $77,000 (CoinDesk, The Block, Cointelegraph, Oct 29)
}
F = FACTS
SOURCES = 'Binance, TRM Labs, CNBC, NBC, Bloomberg, CoinDesk (Oct 29-30, 2026)'


# ------------------------------------------------------------------ scenes --
def s_hook(c, x):
    t, L = x.t, x.L
    specks(c, t, 81, 50)
    if t < L[1]:
        k = ease(seg(t, L[0] + 0.3, L[0] + 3.2))
        c.icon('landmark', 360, 360, 200, SKY, a=fade(t, 0))
        c.text(360, 490, 'Binance', 34, WHITE, 900, a=fade(t, 0))
        for i in range(14):  # coins pouring out of the exchange
            ck = seg(t, L[0] + 0.3 + i * 0.18, L[0] + 1.6 + i * 0.18)
            if 0 < ck < 1:
                c.circle(360 + (i % 5 - 2) * 40 * ck + 160 * ck, 520 + 180 * ease(ck), 16, GOLD, GOLD_D, 2,
                         a=1 - ck * 0.6)
        chip(c, 360, 215, f'about {F["minutes"]} minutes', CORAL, pop(t, L[0] + 0.6), 30)
        c.text(360, 770, f'${F["amount_bn"] * k:.1f} BILLION', 74, GOLD, 900, stroke=4, a=fade(t, L[0] + 0.3))
        c.text(360, 840, 'drained from the exchange', 28, WHITE, 800, a=fade(t, L[0] + 1.5))
        return
    c.text(360, 210, 'Biggest crypto thefts ever', 34, WHITE, 900, a=fade(t, L[1]))
    vmax, y1 = 7.0, 780
    for i, (label, sub, v, col) in enumerate((('Bybit', str(F['bybit_year']), F['bybit_bn'], MUTED),
                                              ('Binance', '2026', F['amount_bn'], CORAL))):
        at = L[1] + 0.4 + i * 1.6
        g = ease(seg(t, at, at + 1.0))
        if t < at:
            continue
        bx = 200 + i * 320
        top = y1 - 430 * v / vmax * g
        c.rrect(bx - 95, top, bx + 95, y1, 16, col)
        c.text(bx, top - 40, f'${v * g:.1f}B', 50, col if i else WHITE, 900)
        c.text(bx, y1 + 36, label, 30, WHITE, 900)
        c.text(bx, y1 + 72, sub, 22, MUTED, 700, shadow=False)
    chip(c, 360, 300, f'about {round(F["amount_bn"] / F["bybit_bn"])}x the old record', GOLD,
         pop(t, L[1] + 3.6), 28)
    source_v(c, t, 'Binance; FBI (Bybit, 2025)')


def s_how(c, x):
    t, L = x.t, x.L
    specks(c, t, 82, 50)
    if t < L[2]:
        # the hot wallet, then the money fanning out across ~10 blockchains
        c.rrect(200, 360, 520, 560, 28, (255, 255, 255, 18), CORAL, 3, a=fade(t, 0))
        c.icon('wallet', 360, 440, 110, GOLD, a=fade(t, 0))
        c.icon('flame', 470, 395, 54, CORAL, a=fade(t, 0.4))
        c.text(360, 525, 'HOT WALLET', 30, WHITE, 900, a=fade(t, 0.2))
        c.text(360, 215, 'Online wallets that', 30, WHITE, 800, a=fade(t, 0.3))
        c.text(360, 255, 'pay out withdrawals', 30, WHITE, 800, a=fade(t, 0.3))
        if t > L[1]:
            for i in range(F['chains']):
                k = ease(seg(t, L[1] + i * 0.12, L[1] + 0.8 + i * 0.12))
                if k <= 0:
                    continue
                ang = math.pi * (0.08 + 0.84 * i / (F['chains'] - 1))
                ex, ey = 360 + math.cos(ang) * 300 * k, 560 + math.sin(ang) * 260 * k
                c.line([(360, 560), (ex, ey)], (255, 255, 255, 70), 3)
                c.circle(ex, ey, 22, SKY, WHITE, 2)
            chip(c, 360, 880, f'about {F["chains"]} blockchains at once', GOLD, pop(t, L[1] + 1.4), 28)
        return
    c.icon('laptop', 360, 430, 210, SKY, a=fade(t, L[2]))
    k = pop(t, L[2] + 0.8)
    if k > 0:
        c.circle(470, 340, 52 * k, CORAL, WHITE, 3)
        c.icon('skull', 470, 340, 56 * k, WHITE)
    c.text(360, 610, 'Started with a hacked', 34, WHITE, 900, a=fade(t, L[2] + 0.5))
    c.text(360, 655, "engineer's laptop", 34, WHITE, 900, a=fade(t, L[2] + 0.5))
    c.text(360, 700, '(Binance, first findings)', 22, MUTED, 700, a=fade(t, L[2] + 0.8), shadow=False)
    chip(c, 360, 800, 'Co-CEO: "more complex than that"', GOLD, pop(t, L[2] + 3.2), 26)
    source_v(c, t, 'Binance; TRM Labs')


def s_after(c, x):
    t, L = x.t, x.L
    specks(c, t, 83, 50)
    if t < L[1]:
        chip(c, 360, 215, 'Withdrawals paused', CORAL, pop(t, L[0] + 0.3), 32)
        g = ease(seg(t, L[0] + 2.0, L[0] + 3.5))
        x0, x1, y0 = 60, 660, 500
        c.text(360, 440, f'${F["amount_bn"]}B moved', 34, WHITE, 900, a=fade(t, L[0] + 1.5))
        c.rrect(x0, y0, x1, y0 + 80, 18, (255, 255, 255, 25), a=fade(t, L[0] + 1.5))
        fw = (x1 - x0) * F['frozen_bn'] / F['amount_bn'] * g
        if fw > 2:
            c.rrect(x0, y0, x0 + fw, y0 + 80, 18, SKY)
        c.icon('snowflake', 140, y0 + 40, 50, WHITE, a=g)
        c.text(360, 650, f'about ${F["frozen_bn"]:.0f}B frozen', 46, SKY, 900, a=fade(t, L[0] + 3))
        c.text(360, 705, 'with help from Tether and Circle', 26, WHITE, 800, a=fade(t, L[0] + 3.5))
        source_v(c, t, 'Binance; Tether; Circle')
        return
    if t < L[2]:
        c.icon('globe', 360, 400, 170, MUTED, a=fade(t, L[1]))
        c.text(360, 580, 'Investigators link it to', 32, WHITE, 800, a=fade(t, L[1] + 0.3))
        c.text(360, 630, 'North Korean hackers', 40, CORAL, 900, a=fade(t, L[1] + 0.6))
        k = pop(t, L[1] + 2.4)
        if k > 0:
            c.rrect(180, 700, 540, 770, 14, None, CORAL, 5, a=clamp(k))
            c.text(360, 735, 'NOT CONFIRMED', 36, CORAL, 900, a=clamp(k), shadow=False)
        source_v(c, t, 'TRM Labs, Chainalysis (analysts)')
        return
    if t < L[3]:
        c.icon('shield-check', 360, 420, 200, MINT, a=fade(t, L[2]))
        c.text(360, 610, 'Binance says it will', 32, WHITE, 800, a=fade(t, L[2] + 0.3))
        c.text(360, 660, 'cover customer losses', 40, MINT, 900, a=fade(t, L[2] + 0.6))
        c.text(360, 710, 'from its own funds', 28, WHITE, 800, a=fade(t, L[2] + 0.9))
        source_v(c, t, 'Binance')
        return
    c.icon('bitcoin', 300, 430, 190, GOLD, a=fade(t, L[3]))
    c.icon('trending-down', 470, 470, 110, CORAL, a=fade(t, L[3] + 0.4), stroke=2.5)
    c.text(360, 640, 'Bitcoin briefly fell', 34, WHITE, 800, a=fade(t, L[3] + 0.3))
    c.text(360, 700, f'below ${F["btc_below"]:,}', 56, CORAL, 900, a=fade(t, L[3] + 0.6))
    source_v(c, t, 'CoinDesk, The Block (Oct 29)')


B63 = '{$6.3 billion|six point three billion dollars}'
SHORT = [
    dict(draw=s_hook, vertical=True, lines=[
        f"In about {F['minutes']} minutes, hackers drained around {B63} from Binance, the world's biggest crypto "
        "exchange.",
        f"It's the biggest crypto theft ever recorded. The old record, the Bybit hack in {F['bybit_year']}, was "
        "about {$1.5 billion|one point five billion dollars}. This one is roughly four times bigger.",
    ], sfx=lambda L: [(L[0] + 0.6, 'pop'), (L[0] + 0.3, 'whoosh'), (L[1] + 0.4, 'pop'), (L[1] + 2.0, 'pop'),
                      (L[1] + 3.6, 'ding')]),
    dict(draw=s_how, vertical=True, lines=[
        "The money came out of Binance's hot wallets. Those are the online wallets an exchange uses to pay out "
        "withdrawals.",
        f"It moved across about {F['chains']} different blockchains, almost all at once.",
        "Binance says it started with a hacked engineer's laptop. But its co-CEO says the attack was more complex "
        "than that.",
    ], sfx=lambda L: [(L[1], 'whoosh'), (L[2] + 0.8, 'down'), (L[2] + 3.2, 'pop')]),
    dict(draw=s_after, vertical=True, lines=[
        "Within hours, Binance paused withdrawals, and companies including Tether and Circle helped freeze about "
        "{$3 billion|three billion dollars} of the moved coins.",
        "Blockchain investigators link the attack to North Korean hackers. That has not been officially confirmed.",
        "Binance says customers will not lose money. It promised to cover the losses from its own funds.",
        f"And bitcoin briefly fell below ${F['btc_below']:,} that night.",
    ], sfx=lambda L: [(L[0] + 0.3, 'pop'), (L[0] + 3.0, 'ding'), (L[1] + 2.4, 'down'), (L[3] + 0.4, 'down')]),
    end_card("We'll break down exactly how it happened. Follow Coin Theory for the full story.",
             tag='Follow for the full story'),
]
SHORTS = {'ep07_short_hack': SHORT}


def check_numbers():
    script = ' '.join(l for sc in SHORT for l in sc['lines'])
    lo, hi = min(F['estimates_bn']), max(F['estimates_bn'])
    assert lo <= F['amount_bn'] <= hi and F['amount_bn'] == 6.3, 'use Binance\'s own figure, inside the range'
    assert round(F['amount_bn'] / F['bybit_bn']) == 4 and 'roughly four times' in script
    assert F['frozen_bn'] < F['amount_bn'] and 'about {$3 billion' in script
    assert f"about {F['minutes']} minutes" in script and f"about {F['chains']} different blockchains" in script
    assert 'not been officially confirmed' in script, 'the North Korea link must be flagged as unconfirmed'
    assert 'below $77,000' in script and F['btc_below'] == 77000
    assert 'briefly' in script, 'the bitcoin drop was a brief dip'
    print('numbers check: OK')


if __name__ == '__main__':
    check_numbers()
    if '--stills' in sys.argv:
        previews([], SHORTS, os.path.join(BUILD, 'previews'))
        sys.exit()
    os.makedirs(BUILD, exist_ok=True)
    build(SHORT, os.path.join(OUT, 'ep07_short_hack.mp4'), os.path.join(BUILD, 'ep07_short_hack'), layout='short')
