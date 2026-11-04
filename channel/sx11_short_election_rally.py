"""News Short (Nov 4, 2026): the day after the midterms the Dow jumped; why; and the $11.9B price tag of the election.

    python3 channel/fetch_sx11.py                  # after the 4 PM ET close -> data/sx11_market.json
    python3 channel/sx11_short_election_rally.py [--stills]

Facts (check_numbers() recomputes everything from the files):
- Dow (^DJI) and S&P 500 (^GSPC) closes Nov 3 vs Nov 4, 2026 and the last bigger % day ("best day since"), Yahoo Finance.
- Total 2026 midterm spending projected at $11.9 billion, the most for any midterm (OpenSecrets, via Spectrum News /
  Al Jazeera, Nov 1-2, 2026). US population 343,105,000 (Census via FRED POPTHM, Sept 2026) -> about $35 per person.
- Why: analysts said removing election uncertainty lifted stocks (CNN, CNBC, Nov 4, 2026).
Nonpartisan: no parties, no candidates. History line reuses sx10 (19 of 19 midterms since 1950 up a year later).
Real footage: Canva stock (owner's Canva Teams licence), assets/footage/canva_h/cash_count_hands.mp4.
"""
import datetime as dt
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from wk2_art import *  # noqa: E402,F401,F403
from engine import build, still  # noqa: E402
import fx  # noqa: E402

OUT = os.path.join(HERE, 'out')
BUILD = os.path.join(HERE, 'build', 'sx11_short_election_rally')
CLIP = os.path.join(HERE, 'assets', 'footage', 'canva_h', 'cash_count_hands.mp4')
M = json.load(open(os.path.join(HERE, 'data', 'sx11_market.json')))
DOW, SP = M['dow'], M['sp500']
PTS = int(round(DOW['points'] / 10.0) * 10)  # spoken/printed to the nearest 10 points
SINCE = dt.date.fromisoformat(DOW['best_since'])
SINCE_TXT = SINCE.strftime('%B %Y')
SPEND_B = 11.9
POP = 343_105_000
PER = SPEND_B * 1e9 / POP


def hook_overlay(c, u):
    c.rrect(0, 0, 720, 1280, 0, (8, 10, 20, 150))
    c.text(360, 240, 'THE DAY AFTER THE MIDTERMS', 36, WHITE, 900)
    s = 1.0 + 0.06 * max(0.0, 1 - abs(u - 0.15) / 0.15) if u < 0.3 else 1.0
    fx.title(c, f'+{PTS:,}', 470, int(170 * s), MINT, 1, stroke=8)
    c.rrect(160, 640, 560, 720, 36, MINT)
    c.text(360, 680, 'DOW POINTS', 48, INK, 400, family='Anton', shadow=False)


def s_hook(c, x):
    hook_overlay(c, max(0.0, x.t - x.L[0]))


def s_since(c, x):  # a calendar flips back month by month to the last bigger day
    u = x.t - x.L[0]
    c.rrect(0, 0, 720, 1280, 0, (14, 18, 30))
    c.text(360, 230, 'BEST DOW DAY SINCE', 44, WHITE, 900, a=fade(u, 0))
    months = []
    d = dt.date(2026, 11, 1)
    while (d.year, d.month) >= (SINCE.year, SINCE.month):
        months.append(d.strftime('%b %Y').upper())
        d = (d.replace(day=1) - dt.timedelta(days=1)).replace(day=1)
    k = ease(fx.clamp((u - 0.3) / 1.8))
    i = min(len(months) - 1, int(k * (len(months) - 1) + 0.0001))
    c.rrect(160, 380, 560, 780, 30, WHITE)
    c.rrect(160, 380, 560, 470, 30, CORAL)
    c.rrect(160, 440, 560, 470, 0, CORAL)
    mon, yr = months[i].split()
    c.text(360, 425, yr, 40, WHITE, 900, shadow=False)
    c.text(360, 620, mon, 150, INK, 400, family='Anton', shadow=False)
    kp = fx.pop(u, 2.3, 0.3)
    if kp > 0:
        c.rrect(170, 860, 550, 940, 36, GOLD, a=fx.clamp(kp))
        c.text(360, 900, f'+{DOW["pct"]:.1f}% IN ONE DAY', 40, INK, 400, family='Anton', a=fx.clamp(kp), shadow=False)


def s_sp(c, x):
    u = x.t - x.L[0]
    c.rrect(0, 0, 720, 1280, 0, (14, 18, 30))
    c.text(360, 300, 'S&P 500', 56, WHITE, 900, a=fade(u, 0))
    k = ease(fx.clamp((u - 0.1) / 1.0))
    fx.title(c, f'+{SP["pct"] * k:.1f}%', 560, 210, MINT, 1, stroke=8)
    ks = fx.pop(u, 1.4, 0.3)
    if ks > 0:
        c.text(360, 780, 'in a single day', 40, MUTED, 800, a=fx.clamp(ks))


def s_why(c, x):  # question marks everywhere, then they get wiped away
    u = x.t - x.L[0]
    c.rrect(0, 0, 720, 1280, 0, (14, 18, 30))
    import random
    rnd = random.Random(4)
    wipe = fx.clamp((u - 2.2) / 0.5)
    for i in range(14):
        k = fx.pop(u, 0.1 + i * 0.1, 0.25)
        if k > 0 and wipe < 1:
            x0, y0 = rnd.uniform(80, 640), rnd.uniform(260, 1000)
            c.text(x0 + 700 * wipe, y0, '?', int(rnd.uniform(70, 150) * fx.clamp(k)), CORAL, 400, family='Anton',
                   a=1 - wipe)
    c.text(360, 200, 'WALL STREET HATES', 46, WHITE, 900, a=fade(u, 0))
    kc = fx.pop(u, 2.5, 0.3)
    if kc > 0:
        fx.title(c, 'NOT\nKNOWING', 560, 150, GOLD, kc)
        c.rrect(140, 860, 580, 940, 36, MINT, a=fx.clamp(fx.pop(u, 3.2, 0.3)))
        c.text(360, 900, 'NOW THE GUESSING STOPS', 34, INK, 400, family='Anton', a=fx.clamp(fx.pop(u, 3.2, 0.3)),
               shadow=False)
    fx.zoom_canvas(c, 1.01 + 0.01 * max(0.0, u), 360, 600)


def s_cost(c, x):  # the price tag of the election, then per person
    u = x.t - x.L[0]
    c.rrect(0, 0, 720, 1280, 0, (14, 18, 30))
    c.text(360, 210, 'MOST EXPENSIVE MIDTERM EVER', 36, WHITE, 900, a=fade(u, 0))
    k = ease(fx.clamp((u - 0.1) / 1.2))
    fx.title(c, f'${SPEND_B * k:.1f}B', 400, 170, GOLD, 1, stroke=8)
    for i in range(int(12 * k)):  # a growing stack of bills
        bill(c, 360 + (i % 2) * 14 - 7, 770 - i * 12, 280, '100')
    kp = fx.pop(u, 4.4, 0.35)
    if kp > 0:
        c.rrect(110, 860, 610, 1000, 34, MINT, a=fx.clamp(kp))
        c.text(360, 900, f'ABOUT ${PER:.0f}', 64, INK, 400, family='Anton', a=fx.clamp(kp), shadow=False)
        c.text(360, 960, 'for every person in America', 28, INK, 800, a=fx.clamp(kp), shadow=False)
    c.text(360, 1030, 'projection: OpenSecrets', 24, MUTED, 800, a=fade(u, 0.5))
    fx.zoom_canvas(c, 1.01 + 0.012 * max(0.0, u), 360, 560)  # slow push so it never sits still


def hook_frame(cv):
    from engine import clip_frame, cover
    cv.img.paste(cover(clip_frame(CLIP, 0), cv.img.size[0], cv.img.size[1]))
    hook_overlay(cv, 0.0)


def s_end(c, x):
    u = x.t - x.L[0]

    def question(cv):
        cv.rrect(0, 0, 720, 1280, 0, (14, 18, 30))
        cv.text(360, 250, 'STOCKS 1 YEAR AFTER MIDTERMS:', 30, WHITE, 900)
        cv.text(360, 300, '19 OF 19 HIGHER SINCE 1950', 30, MINT, 900)
        pulse = 1 + 0.06 * math.sin(u * 6)
        fx.title(cv, '20 FOR\n20?', 480, int(140 * pulse), GOLD, 1)
        for j, (lab, col) in enumerate((('YES', MINT), ('NO', CORAL))):
            kk = fx.clamp(fx.pop(u, 0.4 + j * 0.25, 0.3))
            bx = 230 + j * 260
            cv.rrect(bx - 105, 760 - 52 * kk, bx + 105, 760 + 52 * kk, 26, col)
            cv.text(bx, 760, lab, int(64 * kk) + 1, INK, 400, family='Anton', shadow=False)
        cv.text(360, 880 + 8 * math.sin(u * 4), 'comment below', 34, WHITE, 900)
    brk = x.dur - x.L[0] - 0.95
    if u < brk:
        return question(c)
    fx.frame_break(c, u - brk + 0.5, x.t, question, hook_frame)


S = dict(vertical=True, lead=0.1, gap=0.15, captions=True, cap_y=1080)
SCENES = [
    dict(S, draw=s_hook, bg_video=CLIP, bg_speed=1.0, lead=0.05, lines=[
        f"!The day after the midterms, the Dow jumped {PTS:,} points.",
    ], punch=lambda L: [0.12], sfx=lambda L: [(0.12, 'hit')]),
    dict(S, draw=s_since, lines=[
        f"That's its best day since {SINCE_TXT}.",
    ], sfx=lambda L: [(L[0] + 0.3, 'tick'), (L[0] + 2.3, 'hit')]),
    dict(S, draw=s_sp, lines=[
        f"The S&P 500 climbed {SP['pct']:.1f} percent in a single day.",
    ], sfx=lambda L: [(L[0] + 0.1, 'riser'), (L[0] + 1.1, 'pop')]),
    dict(S, draw=s_why, lines=[
        "Why? Wall Street hates not knowing. Once the votes are counted, the guessing stops.",
    ], sfx=lambda L: [(L[0] + 0.1, 'pop'), (L[0] + 2.2, 'whoosh'), (L[0] + 2.5, 'hit')]),
    dict(S, draw=s_cost, lines=[
        f"And this midterm is projected to cost {SPEND_B} billion dollars, the most ever. "
        f"That's about {PER:.0f} dollars for every person in America.",
    ], sfx=lambda L: [(L[0] + 0.1, 'riser'), (L[0] + 1.2, 'hit'), (L[0] + 4.4, 'pop')]),
    dict(S, draw=s_end, tail=1.0, cam=(1.0, 1.0), lines=[
        "Stocks were higher a year after all 19 midterms since 1950. 20 for 20? Yes or no.",
    ], sfx=lambda L: [(L[0] + 0.4, 'pop'), (L[0] + 0.65, 'pop')]),
]


def check_numbers():
    script = ' '.join(l for sc in SCENES for l in sc['lines'])
    assert DOW['close_nov4'] > DOW['close_nov3'] and DOW['pct'] > 0 and SP['pct'] > 0
    assert abs(DOW['points'] - (DOW['close_nov4'] - DOW['close_nov3'])) < 0.05
    assert f'{PTS:,} points' in script and SINCE_TXT in script and f"{SP['pct']:.1f} percent" in script
    assert round(PER) == 35 and 'about 35 dollars' in script and '11.9 billion' in script
    sx10 = os.path.join(HERE, 'data', 'SP500_midterms.csv')
    assert sum(1 for _ in open(sx10)) - 1 == 19 and '19 midterms since 1950' in script
    assert os.path.exists(CLIP)
    print(f'numbers check: OK  Dow +{DOW["points"]:.0f} ({DOW["pct"]}%), best since {SINCE_TXT}; '
          f'S&P +{SP["pct"]}%; ${SPEND_B}B / {POP:,} = ${PER:.2f} per person; data fetched {DOW["fetched"]}')


if __name__ == '__main__':
    check_numbers()
    os.makedirs(BUILD, exist_ok=True)
    if '--stills' in sys.argv:
        out = os.path.join(BUILD, 'stills')
        os.makedirs(out, exist_ok=True)
        for si, sc in enumerate(SCENES):
            for du in (0.0, 1.5, 3.5):
                still(sc, 0.1 + du, os.path.join(out, f's{si}_{du}.png'), starts=[0.1], layout='short')
        print('stills in', out)
        sys.exit()
    build(SCENES, os.path.join(OUT, 'sx11_short_election_rally.mp4'), BUILD, layout='short', loop=True)
