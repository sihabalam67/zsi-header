"""Standalone Short: the credit card minimum-payment trap. First Short built with all three engines:
Remotion (3D card hook, payment split), Manim (payoff race chart) and channel/fx.py, composited by engine.py.

    python3 channel/cards_math.py            # numbers -> assets/gen/sx02/payoff.json
    (Remotion: npx remotion render CardHook / PaymentSplit in /home/user/video-tools/remotion/coin-video;
     Manim: manim -qh --resolution 1080,1920 channel/manim/payoff_race.py PayoffRace)
    python3 channel/sx02_short_cards.py [--stills]

Facts: $5,000 at the average credit card rate (Fed G.19 via ep04: 21.19%); minimum = interest + 1% of the balance with
a $25 floor, a formula many card agreements use; the CARD Act (2009) requires statements to show how long paying only
the minimum takes. check_numbers() ties every spoken number to cards_math.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from wk2_art import *  # noqa: E402,F401,F403
from engine import build, still  # noqa: E402
import fx  # noqa: E402
import cards_math as M  # noqa: E402

OUT = os.path.join(HERE, 'out')
BUILD = os.path.join(HERE, 'build', 'sx02_short_cards')
GEN = os.path.join(HERE, 'assets', 'gen', 'sx02')
HOOK, SPLIT, RACE = (os.path.join(GEN, f) for f in ('card_hook.mp4', 'payment_split.mp4', 'payoff_race.mp4'))
PAY, INT = M.MIN['first']
YRS_MIN, YRS_FIX = M.MIN['months'] / 12, M.FIX['months'] / 12
APR = M.APR * 100


def beat(x, n):
    t, L = x.t, x.L
    i = max([j for j in range(n) if t >= L[j] - 0.12] or [0])
    return i, t - L[i]


def none(c, x):
    pass


def s_statement(c, x):  # phone with the card statement, then the minimum-payment formula
    i, u = beat(x, 2)
    c.rrect(0, 0, 720, 1280, 0, (14, 18, 30))

    def screen(cv, x0, y0, x1, y1):
        cx = (x0 + x1) / 2
        cv.rrect(x0, y0 + 50, x1, y0 + 130, 0, (60, 30, 90))
        cv.text(cx, y0 + 90, 'CARD STATEMENT', 24, WHITE, 900, shadow=False)
        cv.text(x0 + 24, y0 + 175, 'New balance', 18, (90, 96, 110), 700, anchor='lm', shadow=False)
        cv.text(x1 - 24, y0 + 175, '$5,000.00', 20, (20, 24, 32), 900, anchor='rm', shadow=False)
        cv.text(x0 + 24, y0 + 220, 'Minimum payment', 18, (90, 96, 110), 700, anchor='lm', shadow=False)
        cv.text(x1 - 24, y0 + 220, f'${PAY:,.2f}', 20, (20, 24, 32), 900, anchor='rm', shadow=False)
        k = fx.pop(u if i == 0 else 9, 1.2, 0.35)
        if k > 0:  # the CARD Act warning box
            cv.rrect(x0 + 16, y0 + 270, x1 - 16, y0 + 470, 14, (255, 240, 240), (220, 60, 60), 4, a=fx.clamp(k))
            cv.text(cx, y0 + 300, 'MINIMUM PAYMENT WARNING', 19, (200, 40, 40), 900, a=fx.clamp(k), shadow=False)
            cv.text(cx, y0 + 345, 'If you make only the', 19, (40, 40, 50), 700, a=fx.clamp(k), shadow=False)
            cv.text(cx, y0 + 372, 'minimum payment, you will', 19, (40, 40, 50), 700, a=fx.clamp(k), shadow=False)
            cv.text(cx, y0 + 399, 'pay it off in about', 19, (40, 40, 50), 700, a=fx.clamp(k), shadow=False)
            cv.text(cx, y0 + 438, f'{round(YRS_MIN)} YEARS', 34, (200, 40, 40), 900, a=fx.clamp(k), shadow=False)
    lift = fx.ease_out(fx.clamp(u / 0.5)) if i == 0 else 1
    s = 1.15
    fx.phone(c, 360, fx.lerp(1500, 620, lift), s, screen)
    if i == 0 and u > 2.6:  # a bouncing arrow points at the warning while it's read
        k = fx.pop(u, 2.6, 0.3)
        bob = 14 * math.sin((u - 2.6) * 7)
        c.icon('arrow-left', 640 + bob, 640, 90 * fx.clamp(k), CORAL, stroke=3)
    if i == 1:  # the formula pops in under the shrunken phone
        for j, (txt, col) in enumerate(((f'INTEREST (${INT:.0f})', CORAL), ('+ 1% OF BALANCE ($50)', MINT))):
            k = fx.pop(u, 0.6 + j * 0.9, 0.35)
            if k > 0:
                c.rrect(90, 770 + j * 92, 630, 842 + j * 92, 20, col, a=fx.clamp(k))  # stickers over the phone
                c.text(360, 806 + j * 92, txt, 36, INK, 400, family='Anton', a=fx.clamp(k), shadow=False)


def s_totals(c, x):  # paper cutouts: total interest, then the last line
    i, u = beat(x, 2)
    if i == 0:
        return fx.paper_cutout(c, u, [('MINIMUM ONLY', 34), (f'${M.MIN["interest"]:,.0f}', 56), ('in interest', 30)],
                               [('$200 A MONTH', 34), (f'${M.FIX["interest"]:,.0f}', 56), ('in interest', 30)], 'VS')
    fx.checklist_pop(c, u, ['Same card', 'Same $5,000', 'Different payment'], 0.55, 'THE ONLY DIFFERENCE')


S = dict(vertical=True, lead=0.1, gap=0.15, captions=True, cap_y=1060)
SCENES = [
    dict(S, draw=none, bg_video=HOOK, bg_speed=0.62, cam=(1.0, 1.04), lines=[
        f"!If you only pay the minimum on a five thousand dollar credit card, it takes about {round(YRS_MIN)} years "
        "to pay off.",
    ], punch=lambda L: [62 / 30 / 0.62], sfx=lambda L: [(0.0, 'whoosh'), (62 / 30 / 0.62, 'down')]),
    dict(S, draw=s_statement, lines=[
        "Your statement even warns you. By law, it has to show how long minimum payments take.",
        "That's because the minimum is often just the interest, plus one percent of the balance.",
    ], sfx=lambda L: [(L[0] + 0.2, 'whoosh'), (L[0] + 1.2, 'down'), (L[1] + 0.6, 'pop'), (L[1] + 1.5, 'pop')]),
    dict(S, draw=none, bg_video=SPLIT, bg_speed=0.75, cap_y=1150, lines=[
        f"At about {round(APR)} percent, your first {PAY:.0f} dollar payment? {INT:.0f} dollars is interest. "
        f"Only {PAY - INT:.0f} dollars pays down what you owe.",
    ], sfx=lambda L: [(18 / 30 / 0.75, 'pop'), (44 / 30 / 0.75, 'pop'), (74 / 30 / 0.75, 'down')]),
    dict(S, draw=none, bg_video=RACE, bg_speed=1.5, cap_y=1150, tail=0.9, lines=[  # 19 YEARS lands on "The minimum? 19"
        f"!Now pay two hundred a month instead. It's gone in under three years. The minimum? {round(YRS_MIN)}.",
    ], sfx=lambda L: [(2.3 / 1.5, 'ding'), (6.4 / 1.5, 'down')]),
    dict(S, draw=s_totals, tail=0.4, lines=[
        f"Total interest paying the minimum: ${M.MIN['interest']:,.0f}. Paying two hundred a month: "
        f"${M.FIX['interest']:,.0f}.",
        "Same card. Same debt. The only difference is the payment.",
    ], sfx=lambda L: [(L[0] + 0.1, 'pop'), (L[0] + 0.7, 'pop'), (L[1] + 0.2, 'ding'), (L[1] + 0.75, 'ding'),
                      (L[1] + 1.3, 'ding')]),
]


def check_numbers():
    script = ' '.join(l for sc in SCENES for l in sc['lines'])
    assert abs(M.APR - 0.2119) < 1e-6 and round(APR) == 21 and '21 percent' in script
    assert round(YRS_MIN) == 19 and '19 years' in script and YRS_FIX < 3 and 'under three years' in script
    assert round(PAY) == 138 and round(INT) == 88 and round(PAY - INT) == 50 and '138 dollar' in script
    assert round(M.MIN['interest']) == 7782 and round(M.FIX['interest']) == 1655
    assert '$7,782' in script and '$1,655' in script
    for p in (HOOK, SPLIT, RACE):
        assert os.path.exists(p), p
    print(f'numbers check: OK  min {M.MIN["months"]} mo / ${M.MIN["interest"]:,.0f}; $200 {M.FIX["months"]} mo / '
          f'${M.FIX["interest"]:,.0f}; first payment ${PAY:.2f} (${INT:.2f} interest)')


if __name__ == '__main__':
    check_numbers()
    os.makedirs(BUILD, exist_ok=True)
    if '--stills' in sys.argv:
        out = os.path.join(BUILD, 'stills')
        os.makedirs(out, exist_ok=True)
        for si, sc in enumerate(SCENES):
            starts = [0.1 + 3.2 * j for j in range(len(sc['lines']))]
            for j in range(len(sc['lines'])):
                for du in (1.0, 3.0):
                    still(sc, starts[j] + du, os.path.join(out, f's{si}_{j}_{du}.png'), starts=starts, layout='short')
        print('stills in', out)
        sys.exit()
    build(SCENES, os.path.join(OUT, 'sx02_short_cards.mp4'), BUILD, layout='short', loop=True)
