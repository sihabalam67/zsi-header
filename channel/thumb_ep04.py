#!/usr/bin/env python3
"""Thumbnails for episode 4 (two variants for A/B testing). Writes channel/out/ep04_thumb_[ab].png."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wk2_art import *  # noqa: E402,F401,F403
from ep04_fed import CC_NOW, S_NOW  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')


def variant_a():
    c = Canvas((20, 28, 54), (70, 22, 40))
    fed_building(c, 380, 640, 1.5)
    c.icon('arrow-up', 760, 260, 260, CORAL, stroke=3.5)
    c.text(1040, 200, 'RATES', 110, WHITE, 900, stroke=8)
    c.text(1040, 330, 'UP', 150, CORAL, 900, stroke=9)
    penny(c, 1040, 560, 80, 0.0, 'shocked', look=(-1, -0.3), bounce=False, arms=(200, -20))
    return c


def variant_b():
    c = Canvas((14, 22, 40), (30, 42, 78))
    c.text(640, 110, 'YOUR CARD:', 92, WHITE, 900, stroke=8)
    card(c, 330, 420, 1.6, color=SKY)
    c.circle(860, 420, 170, CORAL, WHITE, 8)
    c.text(860, 400, f'{CC_NOW:.0f}%', 110, WHITE, 900, shadow=False)
    c.text(860, 485, 'interest', 30, WHITE, 800, shadow=False)
    penny(c, 1150, 540, 80, 0.0, 'worried', look=(-1, 0), bounce=False)
    return c


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for name, fn in (('a', variant_a), ('b', variant_b)):
        fn().frame().resize((1280, 720), Image.LANCZOS).save(os.path.join(OUT, f'ep04_thumb_{name}.png'))
    print('ok')
