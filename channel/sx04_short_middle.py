"""Standalone Short: are you middle class? (10/10 rules; thumbnail made in Canva first: out/sx04_thumb.png).

    python3 channel/sx04_short_middle.py [--stills]

Facts:
- Pew Research Center, "Are you in the American middle class?" (Sept 16, 2024), 2022 American Community Survey data:
  middle income = two-thirds to double the national median household income, incomes scaled to a 3-person
  household; for 3 people about $56,600 to $169,800 (2022 dollars); adults: 52% middle, 28% lower, 19% upper income.
- Census Bureau median household income 2025: $87,460 (FRED MEHOINUSA646N).
The opening photo is the Canva-generated image used for the thumbnail (assets/gen/sx04/canva_thumb.png).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from wk2_art import *  # noqa: E402,F401,F403
from engine import build, still  # noqa: E402
import fx  # noqa: E402

OUT = os.path.join(HERE, 'out')
BUILD = os.path.join(HERE, 'build', 'sx04_short_middle')
HOUSE = os.path.join(HERE, 'assets', 'gen', 'sx04', 'canva_thumb.png')

PEW = dict(lo=56600, hi=169800, mid=52, lower=28, upper=19, year=2022)
MED = series('MEHOINUSA646N')
MED_NOW, MED_YEAR = float(MED.iloc[-1]), MED.index[-1].year


def hook(c, u):
    fx.photo(c, HOUSE, 1.0 + 0.03 * u, (0.27, 0.5), sat=1.1, dark=0.35)  # the house half of the Canva image
    c.rrect(0, 0, 720, 1280, 0, (0, 0, 0, 70))
    k = fx.pop(u, 0.12, 0.3)
    if k > 0:
        fx.title(c, f'{PEW["mid"]}%', 420, 230, GOLD, k, stroke=8)
        c.rrect(60, 560, 660, 630, 34, WHITE, a=fx.clamp(fx.pop(u, 0.45)))
        c.text(360, 595, 'of US adults are middle class', 30, INK, 900, a=fx.clamp(fx.pop(u, 0.45)), shadow=False)


def s_hook(c, x):
    hook(c, max(0.0, x.t - x.L[0]))


def money_k(v):
    return f'${v / 1000:.0f}K'


def s_range(c, x):  # line 1: the definition as two chips; line 2: the band grows on an income line
    t, L = x.t, x.L
    u = t - L[0]
    c.rrect(0, 0, 720, 1280, 0, (14, 18, 30))
    c.text(360, 250, 'Middle class (household of 3)', 34, WHITE, 900, a=fade(u, 0))
    if t < L[1] - 0.1:
        for j, (txt, col, at) in enumerate((('2/3 of the median', MINT, 0.9), ('up to 2x the median', GOLD, 2.4))):
            k = fx.pop(u, at, 0.35)
            if k > 0:
                c.rrect(110, 470 + j * 140, 610, 570 + j * 140, 30, col, a=fx.clamp(k))
                c.text(360, 520 + j * 140, txt, 46, INK, 400, family='Anton', a=fx.clamp(k), shadow=False)
        return
    v1 = t - L[1]
    x0, x1, y = 70, 650, 600
    vmax = 250000

    def px(v):
        return x0 + (x1 - x0) * v / vmax
    c.line([(x0, y), (x1, y)], (255, 255, 255, 120), 6)
    for v in (0, 50000, 100000, 150000, 200000, 250000):
        c.line([(px(v), y - 14), (px(v), y + 14)], (255, 255, 255, 120), 3)
        c.text(px(v), y + 50, money_k(v), 22, MUTED, 800, shadow=False)
    g = ease(seg(v1, 0.2, 1.2))
    if g > 0:
        mid = (PEW['lo'] + PEW['hi']) / 2
        a, b = mid - (mid - PEW['lo']) * g, mid + (PEW['hi'] - mid) * g
        c.rrect(px(a), y - 40, px(b), y + 40, 16, MINT + (200,))
    for v, at in ((PEW['lo'], 1.0), (PEW['hi'], 2.4)):
        k = fx.pop(v1, at, 0.35)
        if k > 0:
            c.text(px(v), y - 100, f'${v:,}', int(42 * (0.7 + 0.3 * fx.clamp(k))), GOLD, 400, family='Anton',
                   a=fx.clamp(k))
    if v1 > 3.4:
        chip(c, 360, 800, f'Pew Research Center ({PEW["year"]} data)', SKY, pop(v1, 3.4), 26)


def s_split(c, x):  # the adult population split into lower / middle / upper income
    u = x.t - x.L[0]
    c.rrect(0, 0, 720, 1280, 0, (14, 18, 30))
    c.text(360, 220, 'US adults by household income', 34, WHITE, 900, a=fade(u, 0))
    parts = (('LOWER', PEW['lower'], CORAL, 0.1), ('MIDDLE', PEW['mid'], MINT, 0.6), ('UPPER', PEW['upper'], GOLD, 1.9))  # bottom-up
    y0, y1 = 300, 900
    total = sum(p[1] for p in parts)
    y = y1
    for lab, v, col, at in (parts[0], parts[1], parts[2]):
        h = (y1 - y0) * v / total
        g = ease(seg(u, at, at + 0.6))
        if g > 0:
            c.rrect(170, y - h * g, 550, y, 14, col)
            if g > 0.6:
                c.text(360, y - h / 2, f'{lab}  {v}%', 44, INK, 400, family='Anton', shadow=False)
        y -= h


def s_median(c, x):
    u = x.t - x.L[0]
    fx.digital_zoom(c, u, round(MED_NOW), f'typical household, {MED_YEAR}')


def s_end(c, x):  # the yes/no question, then glass breaks back into the hook's first frame
    u = x.t - x.L[0]

    def question(cv):
        cv.rrect(0, 0, 720, 1280, 0, (14, 18, 30))
        pulse = 1 + 0.06 * math.sin(u * 6)
        fx.title(cv, 'ARE YOU\nMIDDLE\nCLASS?', 330, int(110 * pulse), GOLD, 1)
        for j, (lab, col) in enumerate((('YES', MINT), ('NO', CORAL))):
            k = fx.clamp(fx.pop(u, 0.4 + j * 0.25, 0.3))
            bx = 230 + j * 260
            cv.rrect(bx - 105, 740 - 52 * k, bx + 105, 740 + 52 * k, 26, col)
            cv.text(bx, 740, lab, int(64 * k) + 1, INK, 400, family='Anton', shadow=False)
        cv.text(360, 870 + 8 * math.sin(u * 4), 'comment below', 34, WHITE, 900)
    brk = x.dur - x.L[0] - 0.95
    if u < brk:
        return question(c)
    fx.frame_break(c, u - brk + 0.5, x.t, question, lambda cv: hook(cv, 0.0))


S = dict(vertical=True, lead=0.1, gap=0.15, captions=True, cap_y=1080)
SCENES = [
    dict(S, draw=s_hook, lead=0.05, lines=[
        f"!Only about half of American adults are middle class. {PEW['mid']} percent.",
    ], punch=lambda L: [0.12], sfx=lambda L: [(0.12, 'hit'), (0.45, 'pop')]),
    dict(S, draw=s_range, lines=[
        "Pew Research's definition: two-thirds to double the median income.",
        f"For a household of three, that's ${PEW['lo']:,} to ${PEW['hi']:,}.",
    ], sfx=lambda L: [(L[0] + 0.9, 'pop'), (L[0] + 2.4, 'pop'), (L[1] + 0.2, 'whoosh'), (L[1] + 1.0, 'pop'),
                      (L[1] + 2.4, 'pop'), (L[1] + 3.4, 'pop')]),
    dict(S, draw=s_split, lines=[
        f"{PEW['lower']} percent are lower income. {PEW['upper']} percent are upper income.",
    ], sfx=lambda L: [(L[0] + 0.1, 'pop'), (L[0] + 0.6, 'pop'), (L[0] + 1.9, 'hit')]),
    dict(S, draw=s_median, lines=[
        f"And the typical US household now earns about {round(MED_NOW / 1000)} thousand dollars a year.",
    ], sfx=lambda L: [(L[0] + 1.0, 'riser'), (L[0] + 2.0, 'hit')]),
    dict(S, draw=s_end, tail=1.0, cam=(1.0, 1.0), lines=[
        "So, are you middle class? Yes or no, in the comments.",
    ], sfx=lambda L: [(L[0] + 0.4, 'pop'), (L[0] + 0.65, 'pop')]),
]


def check_numbers():
    script = ' '.join(l for sc in SCENES for l in sc['lines'])
    assert PEW['lower'] + PEW['mid'] + PEW['upper'] in (99, 100, 101)
    assert '52 percent' in script and '28 percent' in script and '19 percent' in script
    assert '$56,600 to $169,800' in script
    assert MED_YEAR == 2025 and round(MED_NOW) == 87460 and 'about 87 thousand' in script and 'Yes or no' in script
    assert os.path.exists(HOUSE)
    print(f'numbers check: OK  Pew {PEW}; Census median {MED_YEAR}: ${MED_NOW:,.0f}')


if __name__ == '__main__':
    check_numbers()
    os.makedirs(BUILD, exist_ok=True)
    if '--stills' in sys.argv:
        out = os.path.join(BUILD, 'stills')
        os.makedirs(out, exist_ok=True)
        for si, sc in enumerate(SCENES):
            for du in (0.3, 2.5, 5.0):
                still(sc, 0.1 + du, os.path.join(out, f's{si}_{du}.png'), starts=[0.1], layout='short')
        print('stills in', out)
        sys.exit()
    build(SCENES, os.path.join(OUT, 'sx04_short_middle.mp4'), BUILD, layout='short', loop=True)
