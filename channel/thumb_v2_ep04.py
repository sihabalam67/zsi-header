#!/usr/bin/env python3
"""v2 thumbnails for episode 4 (A/B pair) in the thumbkit style. Writes channel/out/ep04_thumb_v2[ab].png."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wk2_art import *  # noqa: E402,F401,F403
from thumbkit import Thumb, squint  # noqa: E402
from ep04_fed import CC_NOW  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')


def variant_a():
    th = Thumb(('#ff8a1f', '#a3101f'), center=(0.33, 0.5))
    th.layer(lambda c: c.icon('flame', 330, 330, 520, (255, 214, 64), stroke=2.4), outline=0, shadow=False,
             glow=(255, 190, 40), glow_size=60)
    th.layer(lambda c: card(c, 330, 420, 2.0, color=SKY), outline=12, glow=(255, 236, 160), tilt=-9,
             pivot=(330, 420))
    th.text(930, 120, 'YOUR CARD', 92, color=(255, 220, 64), stroke=10)
    th.text(925, 320, f'{CC_NOW:.0f}%', 270, color=WHITE, stroke=16, glow=(255, 60, 40))
    th.layer(lambda c: penny(c, 1010, 590, 120, 0.0, 'shocked', look=(-1, -0.4), bounce=False, arms=(210, -30)),
             outline=10, glow=(255, 240, 160))
    return th


def variant_b():
    th = Thumb(('#2ec5ff', '#0b1d5c'), center=(0.32, 0.45))
    th.layer(lambda c: fed_building(c, 300, 660, 1.45), outline=10, glow=(160, 230, 255))
    th.layer(lambda c: c.icon('trending-up', 470, 330, 430, CORAL, stroke=3.8), outline=12, glow=(255, 90, 70),
             shadow=True)
    th.text(920, 150, 'RATES UP', 118, color=WHITE, stroke=12)
    th.text(905, 300, 'YOUR MONEY?', 84, color=(255, 214, 64), stroke=10, tilt=-4)
    th.layer(lambda c: penny(c, 1000, 570, 125, 0.0, 'worried', look=(-1, -0.3), bounce=False, arms=(200, -20)),
             outline=10, glow=(255, 240, 160))
    return th


def variant_c():
    """Real photo: the Fed's Eccles Building (public domain, Federal Reserve; see assets/photos/SOURCES.md)."""
    th = Thumb.photo(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'photos', 'fed_eccles.jpg'),
                     focus=(0.42, 0.55), zoom=1.25, vignette=0.6)
    th.layer(lambda c: c.icon('trending-up', 560, 300, 520, CORAL, stroke=4.2), outline=14, glow=(255, 70, 50),
             glow_size=50)
    th.text(330, 110, 'RATES UP', 130, color=WHITE, stroke=13)
    th.text(980, 560, f'{CC_NOW:.0f}%', 220, color=(255, 214, 64), stroke=15, glow=(255, 60, 40), tilt=6)
    th.text(980, 680, 'on your card', 60, color=WHITE, stroke=9)
    th.layer(lambda c: penny(c, 1110, 250, 115, 0.0, 'shocked', look=(-1, 0.2), bounce=False, arms=(200, -20)),
             outline=10, glow=(255, 240, 160))
    return th


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    paths = [variant_a().save(os.path.join(OUT, 'ep04_thumb_v2a.png')),
             variant_b().save(os.path.join(OUT, 'ep04_thumb_v2b.png')),
             variant_c().save(os.path.join(OUT, 'ep04_thumb_v2c.png'))]
    print('ok', paths)
