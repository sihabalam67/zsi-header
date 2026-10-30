#!/usr/bin/env python3
"""Thumbnails for ep07 (the Binance hack) on the owner's Google Flow background. Writes out/ep07_thumb_[ab].png."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wk2_art import *  # noqa: E402,F401,F403
from thumbkit import Thumb, squint  # noqa: E402
from ep07_binance import F  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
BG = os.path.join(HERE, 'assets', 'flow', 'binance_vault.jpg')


def variant_a():
    th = Thumb.photo(BG, focus=(0.5, 0.5), zoom=1.0, saturation=1.15, contrast=1.1, vignette=0.35)
    th.text(930, 150, f'${F["amount_bn"]} BILLION', 98, color=(255, 214, 64), stroke=13, glow=(255, 120, 30))
    th.text(930, 270, f'GONE IN {F["minutes"]} MIN', 80, color=WHITE, stroke=11, tilt=-3)
    th.layer(lambda c: c.icon('arrow-left', 760, 470, 190, CORAL, stroke=4), outline=12, glow=(255, 70, 50))
    th.layer(lambda c: penny(c, 1090, 560, 125, 0.0, 'shocked', look=(-1, 0), bounce=False, arms=(200, -20)),
             outline=10, glow=(255, 240, 160))
    return th


def variant_b():
    th = Thumb.photo(BG, focus=(0.38, 0.55), zoom=1.25, saturation=1.2, contrast=1.15, vignette=0.45)
    th.text(900, 120, 'BIGGEST HACK', 92, color=WHITE, stroke=12)
    th.text(820, 235, 'EVER', 120, color=(255, 70, 50), stroke=12, glow=(255, 60, 40))
    th.text(960, 590, f'${F["amount_bn"]}B', 190, color=(255, 214, 64), stroke=15, glow=(255, 120, 30), tilt=5)
    th.layer(lambda c: penny(c, 1140, 370, 95, 0.0, 'shocked', look=(-1, 0.3), bounce=False, arms=(210, -30)),
             outline=9, glow=(255, 240, 160))
    return th


if __name__ == '__main__':
    paths = [variant_a().save(os.path.join(OUT, 'ep07_thumb_a.png')),
             variant_b().save(os.path.join(OUT, 'ep07_thumb_b.png'))]
    squint(paths, '/tmp/claude-0/-home-user-zsi-header/135a45f0-ab71-57a7-80ce-da145bb199c8/scratchpad/qa/sv/thumb_ep07.png')
    print('ok')
