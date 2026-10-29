#!/usr/bin/env python3
"""Thumbnails for episode 1 (two variants for A/B testing). Writes channel/out/ep01_thumb_[ab].png."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import *  # noqa: E402,F401,F403

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')


def variant_a():
    c = Canvas((20, 28, 54), (44, 20, 60))
    c.circle(300, 380, 260, (255, 196, 61, 40))
    penny(c, 300, 360, 150, 0.0, 'shocked', look=(1, 0), bounce=False, arms=(200, -20))
    bill(c, 760, 230, 300, '100')
    c.line([(760, 330), (760, 420)], WHITE, 10)
    c.poly([(730, 410), (790, 410), (760, 450)], WHITE)
    bill(c, 760, 500, 120, '100', tint=0.5)
    c.text(1090, 230, '$100', 110, WHITE, 900, stroke=8)
    c.text(1090, 500, '$12', 130, CORAL, 900, stroke=8)
    c.text(1090, 590, 'SINCE 1970', 34, GOLD, 900, stroke=5)
    return c


def variant_b():
    c = Canvas((14, 22, 40), (30, 42, 78))
    c.text(640, 140, 'WHERE DID', 100, WHITE, 900, stroke=8)
    c.text(640, 260, 'MY $88 GO?', 120, GOLD, 900, stroke=8)
    penny(c, 330, 520, 110, 0.0, 'shocked', look=(1, -0.3), bounce=False)
    bill(c, 860, 520, 330, '100', tint=0.2)
    c.circle(1050, 450, 70, CORAL, WHITE, 6)
    c.text(1050, 452, '-88%', 40, WHITE, 900, shadow=False)
    return c


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for name, fn in (('a', variant_a), ('b', variant_b)):
        fn().frame().resize((1280, 720), Image.LANCZOS).save(os.path.join(OUT, f'ep01_thumb_{name}.png'))
    print('ok')
