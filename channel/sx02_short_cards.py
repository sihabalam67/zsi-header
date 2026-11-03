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


def s_statement(c, x):  # phone with the card statement and its minimum-payment warning
    i, u = beat(x, len(x.L))
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
    if i == 0 and u > 1.6:  # push in on the warning box so its text is readable on a phone
        z = fx.lerp(1.0, 1.75, fx.ease(fx.clamp((u - 1.6) / 0.7))) + 0.04 * max(0.0, u - 2.3)
        fx.zoom_canvas(c, z, 360, 655)  # header goes off the top, clear of the logo
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


HOOK2 = os.path.join(GEN, 'card_hook2.mp4')


def hook_frame(cv):
    """Frame 0 of the hook clip, so the last frame of the Short loops straight into the first."""
    from engine import clip_frame, cover
    cv.img.paste(cover(clip_frame(HOOK2, 0), cv.img.size[0], cv.img.size[1]))


def s_end(c, x):  # totals on paper, then the comment question, then glass breaks back into the hook
    i, u = beat(x, 2)
    if i == 0:
        return fx.paper_cutout(c, u, [('MINIMUM ONLY', 34), (f'${M.MIN["interest"]:,.0f}', 56), ('in interest', 30)],
                               [('$200 A MONTH', 34), (f'${M.FIX["interest"]:,.0f}', 56), ('in interest', 30)], 'VS')

    def question(cv):
        cv.rrect(0, 0, 720, 1280, 0, (14, 18, 30))
        pulse = 1 + 0.06 * math.sin(u * 6)
        fx.title(cv, 'EVER PAID\nONLY THE\nMINIMUM?', 330, int(104 * pulse), GOLD, 1)
        for j, (lab, col) in enumerate((('YES', CORAL), ('NO', MINT))):  # easy yes/no answer = more comments
            k = fx.clamp(fx.pop(u, 0.4 + j * 0.25, 0.3))
            bx = 230 + j * 260
            cv.rrect(bx - 105, 700 - 52 * k, bx + 105, 700 + 52 * k, 26, col)
            cv.text(bx, 700, lab, int(64 * k) + 1, INK, 400, family='Anton', shadow=False)
        cv.text(360, 830 + 8 * math.sin(u * 4), 'comment below', 34, WHITE, 900)
    brk = x.dur - x.L[1] - 0.95
    if u < brk:
        return question(c)
    fx.frame_break(c, u - brk + 0.5, x.t, question, hook_frame)  # shatter at the end, landing on frame 0


S = dict(vertical=True, lead=0.1, gap=0.15, captions=True, cap_y=1060)
SCENES = [
    dict(S, draw=none, bg_video=HOOK2, bg_speed=1.0, lead=0.05, lines=[
        f"!Paying only the minimum on a five thousand dollar credit card? That's {round(YRS_MIN)} years.",
    ], punch=lambda L: [5 / 30], sfx=lambda L: [(5 / 30, 'hit'), (16 / 30, 'pop')]),
    dict(S, draw=s_statement, lines=[
        "Your statement even warns you, because the minimum is mostly interest.",
    ], sfx=lambda L: [(L[0] + 0.2, 'whoosh'), (L[0] + 1.2, 'down'), (L[0] + 1.6, 'whoosh')]),
    dict(S, draw=none, bg_video=SPLIT, bg_speed=1.3, cap_y=1150, lines=[
        f"Your first payment is about {PAY:.0f} dollars. {INT:.0f} of it is interest.",
    ], sfx=lambda L: [(18 / 39, 'pop'), (44 / 39, 'pop'), (74 / 39, 'hit')]),
    dict(S, draw=none, bg_video=RACE, bg_speed=1.5, cap_y=1150, tail=0.9, lines=[  # 19 YEARS lands on "The minimum? 19"
        f"!Pay two hundred a month instead: gone in under three years. The minimum? {round(YRS_MIN)}.",
    ], sfx=lambda L: [(2.3 / 1.5, 'ding'), (6.4 / 1.5 - 1.0, 'riser'), (6.4 / 1.5, 'hit')]),
    dict(S, draw=s_end, tail=1.0, cam=(1.0, 1.0), lines=[  # no camera drift: its last frame must equal frame 0
        f"That's ${M.MIN['interest']:,.0f} in interest, versus ${M.FIX['interest']:,.0f}.",
        "Have you ever paid only the minimum? Yes or no, in the comments.",
    ], sfx=lambda L: [(L[0] + 0.1, 'pop'), (L[0] + 0.7, 'hit'), (L[1] + 0.1, 'whoosh'), (L[1] + 0.5, 'pop'),
                      (L[1] + 0.75, 'pop')]),
]


def check_numbers():
    script = ' '.join(l for sc in SCENES for l in sc['lines'])
    assert abs(M.APR - 0.2119) < 1e-6 and round(APR) == 21
    assert round(YRS_MIN) == 19 and '19 years' in script and YRS_FIX < 3 and 'under three years' in script
    assert round(PAY) == 138 and round(INT) == 88 and round(PAY - INT) == 50 and 'about 138 dollars' in script and 'Yes or no' in script
    assert round(M.MIN['interest']) == 7782 and round(M.FIX['interest']) == 1655
    assert '$7,782' in script and '$1,655' in script
    for p in (HOOK2, SPLIT, RACE):
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
