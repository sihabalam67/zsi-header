#!/usr/bin/env python3
"""Thumbnails for episode 5 (two variants for A/B testing). Writes channel/out/ep05_thumb_[ab].png."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wk2_art import *  # noqa: E402,F401,F403
from ep05_jobs import office  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')


def variant_a():
    c = Canvas((30, 18, 34), (80, 24, 40))
    c.circle(330, 430, 270, (248, 113, 113, 40))
    office(c, 330, 690, 1.65, lit=0.35)
    c.text(910, 170, '60,000', 150, CORAL, 900, stroke=9)
    c.text(910, 300, 'BUYOUTS', 104, WHITE, 900, stroke=8)
    penny(c, 900, 540, 90, 0.0, 'shocked', look=(-1, -0.3), bounce=False, arms=(200, -20))
    return c


def variant_b():
    c = Canvas((14, 22, 40), (30, 42, 78))
    c.text(640, 110, 'NOBODY\'S FIRED.', 92, WHITE, 900, stroke=8)
    c.text(640, 225, 'NOBODY\'S HIRED.', 92, GOLD, 900, stroke=8)
    c.icon('trending-down', 420, 470, 240, CORAL, stroke=3.5)
    penny(c, 900, 520, 100, 0.0, 'worried', look=(-1, 0), bounce=False)
    return c


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for name, fn in (('a', variant_a), ('b', variant_b)):
        fn().frame().resize((1280, 720), Image.LANCZOS).save(os.path.join(OUT, f'ep05_thumb_{name}.png'))
    print('ok')
