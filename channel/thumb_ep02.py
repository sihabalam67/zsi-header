#!/usr/bin/env python3
"""Thumbnails for episode 2 (two variants for A/B testing). Writes channel/out/ep02_thumb_[ab].png."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import *  # noqa: E402,F401,F403
from ep02_housing import P1970, P_NOW, SHARE_NOW, house  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')


def variant_a():
    c = Canvas((20, 28, 54), (60, 22, 40))
    c.circle(340, 430, 260, (248, 113, 113, 40))
    house(c, 340, 600, 2.0, lit=1)
    penny(c, 600, 520, 80, 0.0, 'shocked', look=(-1, -0.3), bounce=False, arms=(200, -20))
    c.text(1000, 200, f'${round(P1970 / 1000)}K', 120, MINT, 900, stroke=8)
    c.line([(1000, 290), (1000, 360)], WHITE, 12)
    c.poly([(965, 350), (1035, 350), (1000, 395)], WHITE)
    c.text(1000, 480, f'${round(P_NOW / 1000)}K', 150, CORAL, 900, stroke=9)
    return c


def variant_b():
    c = Canvas((14, 22, 40), (30, 42, 78))
    c.text(640, 130, 'WHY CAN\'T', 96, WHITE, 900, stroke=8)
    c.text(640, 245, 'ANYONE BUY A HOUSE?', 84, GOLD, 900, stroke=8)
    house(c, 380, 640, 1.6, roof=(120, 120, 140))
    c.icon('lock', 380, 470, 90, CORAL, stroke=3)
    penny(c, 760, 560, 90, 0.0, 'worried', look=(-1, 0), bounce=False)
    c.circle(1040, 470, 110, CORAL, WHITE, 6)
    c.text(1040, 445, f'{SHARE_NOW:.0f}%', 64, WHITE, 900, shadow=False)
    c.text(1040, 505, 'of your pay', 22, WHITE, 800, shadow=False)
    return c


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for name, fn in (('a', variant_a), ('b', variant_b)):
        fn().frame().resize((1280, 720), Image.LANCZOS).save(os.path.join(OUT, f'ep02_thumb_{name}.png'))
    print('ok')
