#!/usr/bin/env python3
"""Thumbnails for episode 3 (two variants for A/B testing). Writes channel/out/ep03_thumb_[ab].png."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wk2_art import *  # noqa: E402,F401,F403
from ep03_gas import G_LOW, G_PEAK  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')


def variant_a():
    c = Canvas((30, 18, 30), (80, 24, 34))
    c.circle(360, 420, 280, (248, 113, 113, 45))
    gas_pump(c, 360, 660, 2.1, f'${G_PEAK:.2f}')
    penny(c, 700, 520, 90, 0.0, 'shocked', look=(-1, -0.3), bounce=False, arms=(200, -20))
    c.text(1030, 210, f'${G_LOW:.2f}', 110, MINT, 900, stroke=8)
    c.line([(1030, 300), (1030, 360)], WHITE, 12)
    c.poly([(995, 350), (1065, 350), (1030, 395)], WHITE)
    c.text(1030, 480, f'${G_PEAK:.2f}', 140, CORAL, 900, stroke=9)
    return c


def variant_b():
    c = Canvas((14, 22, 40), (30, 42, 78))
    c.text(640, 120, 'WHY IS GAS', 100, WHITE, 900, stroke=8)
    c.text(640, 235, 'SO EXPENSIVE?', 96, CORAL, 900, stroke=8)
    tanker(c, 420, 560, 1.15)
    waves(c, 600, 0.0, a=0.8)
    c.line([(300, 380), (540, 560)], CORAL, 22)
    c.line([(540, 380), (300, 560)], CORAL, 22)
    penny(c, 980, 520, 95, 0.0, 'worried', look=(-1, 0), bounce=False)
    return c


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for name, fn in (('a', variant_a), ('b', variant_b)):
        fn().frame().resize((1280, 720), Image.LANCZOS).save(os.path.join(OUT, f'ep03_thumb_{name}.png'))
    print('ok')
