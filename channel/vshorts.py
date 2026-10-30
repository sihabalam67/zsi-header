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


def mark(c, t, px, py, xx, v, lab, col, at, above=True, lo=200, hi=560):
    """Dot on a chart point with a value label in a pill, kept inside the frame."""
    kk = pop(t, at)
    if kk <= 0:
        return
    c.circle(px(xx), py(v), 12 * kk, col, WHITE, 3)
    bx = min(max(px(xx), lo), hi)
    y = py(v) - 57 if above else py(v) + 57
    w = max(170, len(lab) * 17 + 40)
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


VERTICAL = {
    'ep03_short_jump': [v03_hook, v03_oil],
    'ep03_short_barrel': [v03_barrel],
    'ep03_short_feathers': [v03_feathers],
}


def scenes_for(name):
    """The original Short's scenes with their drawings swapped for the vertical versions (end card is shared)."""
    out = []
    draws = iter(VERTICAL[name])
    for sc in E.SHORTS[name]:
        if sc.get('vertical'):
            out.append(sc)
            continue
        sc = {k: v for k, v in sc.items() if k not in ('focus', '_crop')}
        out.append(dict(sc, draw=next(draws), vertical=True))
    return out


if __name__ == '__main__':
    scenes = scenes_for(NAME)
    build_dir = os.path.join(HERE, 'build', EPN, NAME)
    os.makedirs(build_dir, exist_ok=True)
    if '--stills' in sys.argv:
        previews([], {NAME: scenes}, os.path.join(HERE, 'build', EPN, 'vshorts'))
        sys.exit()
    build(scenes, os.path.join(HERE, 'out', f'{NAME}.mp4'), build_dir, layout='short')
