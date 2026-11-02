"""Standalone Short: "Banks create money out of thin air". All 18 motion effects from channel/fx.py, one per beat.

    python3 channel/ep06_short_banks.py [--stills]

Facts (checked in check_numbers):
- Bank of England, "Money creation in the modern economy", Quarterly Bulletin 2014 Q1: commercial banks create
  most money by making loans; repaying a loan destroys money; bank deposits were 97% of UK broad money.
- Federal Reserve: reserve requirement ratios cut to 0% effective March 26, 2020 (announced March 15, 2020).
- FRED: currency in circulation (WCURCIR, weekly, $ millions) vs the M2 money supply (M2SL, $ billions).
Photos: channel/assets/photos/ep06s (public domain / CC0, logged in SOURCES.md). Everything else is drawn in code;
the bank app, chat, headlines and magazine are made up.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from wk2_art import *  # noqa: E402,F401,F403
from engine import build, still  # noqa: E402
import fx  # noqa: E402

OUT = os.path.join(HERE, 'out')
BUILD = os.path.join(HERE, 'build', 'ep06_short_banks')
PH = os.path.join(HERE, 'assets', 'photos', 'ep06s')
CASH, VAULT, BANK, HOUSES = (os.path.join(PH, f) for f in ('cash.jpg', 'vault.png', 'bank.jpg', 'houses.jpg'))
CASH_F = (0.83, 0.72)  # the US $50 stacks (keeps the one non-US note out of frame)

CUR = series('WCURCIR')          # $ millions, weekly
M2 = series('M2SL')              # $ billions, monthly
CASH_BN = CUR.iloc[-1] / 1000
M2_BN = M2.iloc[-1]
CASH_SHARE = CASH_BN / M2_BN     # about 0.106: roughly 1 dollar in 10
M2_1960 = M2[M2.index.year == 1960].mean()
M2Y = M2[M2.index.year >= 1960]
XS, YS = [d.year + (d.month - 1) / 12 for d in M2Y.index], [v / 1000 for v in M2Y.values]
BOE_DEPOSITS = 97                # % of UK broad money held as bank deposits (Bank of England, 2014)
LOAN = 300000


def hook(c, u):
    fx.snap_zoom(c, u, CASH, "YOUR BANK\nDOESN'T LEND\nYOUR MONEY", CASH_F)


def loop_frame(c):
    """The exact first frame, so the Short loops seamlessly."""
    hook(c, 0.0)


def beat(x, n):
    """Index of the active narration line and seconds since it started."""
    t, L = x.t, x.L
    i = max([j for j in range(n) if t >= L[j] - 0.12] or [0])
    return i, t - L[i]


def s_open(c, x):  # 1 snap zoom, 2 headline storm, 3 zoom through cut
    i, u = beat(x, 3)
    if i == 0 or x.t < x.L[0]:
        return hook(c, max(0.0, x.t - x.L[0]))
    if i == 1:
        return fx.headline_storm(c, u, ['WHERE DOES\nMONEY COME FROM?', 'BANKS CREATE\nMONEY?', 'NEW MONEY,\nEVERY DAY',
                                        'THE LOAN\nMYSTERY', "IT'S NOT\nYOUR SAVINGS", 'OUT OF\nTHIN AIR?',
                                        'WHO PRINTS\nYOUR DOLLARS?'])
    fx.zoom_through(c, u, x.dur - x.L[2], VAULT, '$', (0.82, 0.55), 'HERE IS HOW')


def s_loan(c, x):  # 4 phone mockup, 5 chat takeover, 6 green screen
    i, u = beat(x, 3)
    if i == 0:
        return fx.phone_mockup(c, u + 0.12, LOAN, CASH)
    if i == 1:
        return fx.chat_takeover(c, u, [('where did the bank\nget $300k?', 'l'), ('from other people\'s\nsavings?', 'l'),
                                       ('nope', 'r'), ('then from where??', 'l'), ('watch', 'r')], step=0.6)
    fx.green_screen(c, u, x.t)


def s_new(c, x):  # 7 digital zoom, 8 paper cutout, 9 magazine cover
    i, u = beat(x, 3)
    if i == 0:
        return fx.digital_zoom(c, u, LOAN, 'brand-new money')
    if i == 1:
        return fx.paper_cutout(c, u, [('YOUR LOAN', 44), ('you owe the bank', 26), ('$300,000', 52)],
                               [('YOUR DEPOSIT', 44), ('the bank owes you', 26), ('$300,000', 52)], '+')
    fx.magazine_cover(c, u, BANK, 'MONEY', '"Banks create money\nby making loans"',
                      'BANK OF ENGLAND, 2014', (0.5, 0.45))


def s_size(c, x):  # 10 liquid glass, 11 orbit, 12 growth curve
    i, u = beat(x, 3)
    if i == 0:
        return fx.liquid_glass(c, u, CASH, [(f'{BOE_DEPOSITS}%', 'of UK money = bank deposits', GOLD),
                                            (f'{100 - BOE_DEPOSITS}%', 'is cash', WHITE)], CASH_F)
    if i == 1:
        return fx.orbit(c, u, '~1 IN 10', f'US dollars is cash (${CASH_BN / 1000:.2f}T of ${M2_BN / 1000:.1f}T)')
    fx.growth_curve(c, u, XS, YS, f'${M2_BN / 1000:.1f}T', f'${M2_1960 / 1000:.1f}T in 1960', 2.4)


def s_limits(c, x):  # 13 frame escape, 14 checklist pop, 15 checklist tally
    i, u = beat(x, 3)
    if i == 0:
        def inside(cv, x0, y0, x1, y1):
            cv.rrect(x0, y0, x1, y1, 0, (14, 18, 30))
            pts = [(x0 + (x1 - x0) * k / 40, y1 - 30 - (y1 - y0 - 80) * (k / 40) ** 2.2) for k in range(41)]
            cv.line(pts, MINT, 8)
        return fx.frame_escape(c, u, x.t, inside, 'WHAT STOPS\nTHEM?')
    if i == 1:
        return fx.checklist_pop(c, u, ['Must be paid back', 'Capital rules',
                                       'Interest rates'], 0.8, 'THE LIMITS')
    fx.checklist_tally(c, u, 10, 0, 'US reserve requirement', 'MARCH 2020')


def s_end(c, x):  # 16 b-roll overlay, 17 zoom portal, 18 frame break (back to the first frame)
    i, u = beat(x, 3)
    if i == 0:
        return fx.broll_overlay(c, u, HOUSES, 'PAY OFF A LOAN...', 'THE MONEY\nDISAPPEARS', (0.72, 0.45))

    def full_video(cv):
        cv.rrect(0, 0, 720, 1280, 0, (20, 26, 44))
        fx.photo(cv, BANK, 1.1, (0.5, 0.4), box=(0, 0, 720, 1280), dark=0.45)
        fx.title(cv, 'HOW BANKS\nCREATE\nMONEY', 420, 110, GOLD, 1)
        cv.text(360, 820, 'FULL VIDEO ON THE CHANNEL', 30, WHITE, 900)
    if i == 1:
        return fx.zoom_portal(c, u, full_video, 'THE FULL STORY')
    fx.frame_break(c, u, x.t, full_video, loop_frame)


S = dict(vertical=True, lead=0.1, gap=0.15, captions=True, cap_y=1060)
SCENES = [
    dict(S, draw=s_open, lines=[
        "!Your bank doesn't lend out your money.",
        "It creates brand-new money. Out of thin air.",
        "Here's how.",
    ], punch=lambda L: [0.05], sfx=lambda L: [(0.0, 'down'), (L[1], 'whoosh'), (L[2], 'whoosh')]),
    dict(S, draw=s_loan, lines=[
        "Say you get a three hundred thousand dollar mortgage.",
        "The bank doesn't take that money from someone else's savings.",
        "It just types the number into your account.",
    ], sfx=lambda L: [(L[0] + 1.9, 'ding'), (L[1], 'pop'), (L[1] + 1.2, 'pop'), (L[1] + 2.4, 'pop'),
                      (L[2] + 0.4, 'whoosh')]),
    dict(S, draw=s_new, lines=[
        "!A new deposit appears. That's new money.",
        "Your loan and your deposit are created at the same moment.",
        "Don't take my word for it. The Bank of England said it in 2014.",
    ], punch=lambda L: [L[0] + 1.6], sfx=lambda L: [(L[0] + 1.6, 'ding'), (L[1] + 0.1, 'pop'), (L[1] + 0.7, 'pop'),
                                                    (L[2] + 0.1, 'down')]),
    dict(S, draw=s_size, lines=[
        f"In Britain, about {BOE_DEPOSITS}% of money is bank deposits, not cash.",
        "In America, only about one in ten dollars is actual cash.",
        "That's why the money supply just keeps growing.",
    ], sfx=lambda L: [(L[0] + 0.3, 'pop'), (L[0] + 1.2, 'pop'), (L[1] + 0.6, 'ding'), (L[2] + 2.4, 'ding')]),
    dict(S, draw=s_limits, lines=[
        "So what stops banks from making money forever?",
        "Three things: people have to pay it back, banks need enough capital, and interest rates.",
        "And the old rule to keep cash in reserve? Since March 2020, it's zero.",
    ], punch=lambda L: [L[2] + 1.9], sfx=lambda L: [(L[0] + 0.9, 'pop'), (L[1] + 0.5, 'ding'), (L[1] + 1.3, 'ding'),
                                                    (L[1] + 2.1, 'ding'), (L[2] + 1.9, 'down')]),
    dict(S, draw=s_end, tail=0.3, lines=[
        "!And when you pay off a loan, that money disappears.",
        "The full story is in our video on how banks create money.",
        "So no, your money was never sitting in the vault.",
    ], sfx=lambda L: [(L[0] + 1.4, 'down'), (L[1] + 0.1, 'whoosh'), (L[2] + 0.5, 'down')]),
]


def check_numbers():
    script = ' '.join(l for sc in SCENES for l in sc['lines'])
    assert 0.09 < CASH_SHARE < 0.115 and 'one in ten dollars' in script, CASH_SHARE
    assert BOE_DEPOSITS == 97 and '97%' in script and 'Bank of England said it in 2014' in script
    assert 'Since March 2020' in script and 'zero' in script
    assert M2_BN / M2_1960 > 50
    print(f'numbers check: OK  cash ${CASH_BN:,.0f}B / M2 ${M2_BN:,.0f}B = {CASH_SHARE:.1%};  '
          f'M2 1960 ${M2_1960:,.0f}B -> {M2.index[-1]:%b %Y}; cash as of {CUR.index[-1]:%b %d %Y}')


if __name__ == '__main__':
    check_numbers()
    os.makedirs(BUILD, exist_ok=True)
    if '--stills' in sys.argv:
        out = os.path.join(BUILD, 'stills')
        os.makedirs(out, exist_ok=True)
        for si, sc in enumerate(SCENES):
            starts = [0.1 + 3.2 * j for j in range(3)]
            for j in range(3):
                for du in (0.6, 1.8, 2.9):
                    still(sc, starts[j] + du, os.path.join(out, f's{si}_{j}_{du}.png'), starts=starts, layout='short')
        print('stills in', out)
        sys.exit()
    build(SCENES, os.path.join(OUT, 'ep06_short_banks.mp4'), BUILD, layout='short', loop=True)
