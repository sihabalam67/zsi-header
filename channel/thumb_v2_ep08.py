#!/usr/bin/env python3
"""Thumbnails for ep08 (midterms) on the owner's Google Flow images. Writes out/ep08_thumb_[ab].png."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wk2_art import *  # noqa: E402,F401,F403
from thumbkit import Thumb, squint  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
FLOW = os.path.join(HERE, 'assets', 'flow', 'ep08')


def variant_a():
    """The dome bursting with light under a green arrow; the claim on the right."""
    th = Thumb.photo(os.path.join(FLOW, 'img6.jpg'), focus=(0.5, 0.5), saturation=1.15, contrast=1.1, vignette=0.3)
    th.text(985, 200, '18 / 18', 190, color=(255, 214, 64), stroke=15, glow=(80, 255, 140))
    th.text(985, 365, 'STOCKS AFTER', 72, color=WHITE, stroke=10)
    th.text(985, 450, 'MIDTERMS', 92, color=(90, 255, 150), stroke=11, glow=(40, 200, 90))
    return th


def variant_b():
    """Fictional amazed woman at her laptop (left); the number on the right."""
    th = Thumb.photo(os.path.join(FLOW, 'img1.jpg'), focus=(0.38, 0.5), zoom=1.08, saturation=1.1, contrast=1.08,
                     vignette=0.3)
    th.text(990, 190, '18 FOR 18', 120, color=(255, 214, 64), stroke=13, glow=(255, 140, 40))
    th.text(990, 330, 'after every', 64, color=WHITE, stroke=9)
    th.text(990, 420, 'MIDTERM', 110, color=(90, 255, 150), stroke=12, glow=(40, 200, 90), tilt=-3)
    th.layer(lambda c: penny(c, 1130, 590, 85, 0.0, 'shocked', look=(-1, -0.2), bounce=False, arms=(200, -20)),
             outline=8, glow=(255, 240, 160))
    return th


if __name__ == '__main__':
    paths = [variant_a().save(os.path.join(OUT, 'ep08_thumb_a.png')),
             variant_b().save(os.path.join(OUT, 'ep08_thumb_b.png'))]
    squint(paths, '/tmp/claude-0/-home-user-zsi-header/135a45f0-ab71-57a7-80ce-da145bb199c8/scratchpad/qa/sv/thumb_ep08.png')
    print('ok')
