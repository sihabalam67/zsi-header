#!/usr/bin/env python3
"""Channel branding: profile picture (800x800), banner (2560x1440, text inside the 1546x423 safe area),
and a video watermark (150x150). Writes channel/out/brand_*.png."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import *  # noqa: E402,F401,F403

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')


def profile():
    c = Canvas((30, 42, 78), (14, 22, 40), k=800 / 1280 * 2)  # 1280-wide logical canvas -> 1600 px, cropped
    c.circle(640, 400, 330, (255, 196, 61, 30))
    penny(c, 640, 330, 150, 0.0, 'happy', bounce=False, arms=(40, 140))
    img = c.img.crop((int(240 * c.k), int(-40 * c.k) if False else 0, int(1040 * c.k), int(800 * c.k)))
    return img.resize((800, 800), Image.LANCZOS)


def banner():
    k = 2560 / 1280
    img = Image.new('RGB', (2560, 1440))
    c = Canvas(img=img, k=k)
    bg = gradient(BG1, BG2).resize((2560, 1440))
    img.paste(bg)
    specks(c, 3.0, 40, 90, amax=0.12)
    # safe area is the centre 1546x423 px -> logical x 253..1027, y 254..466
    penny(c, 350, 330, 58, 0.0, 'happy', bounce=False, arms=(40, 150))
    c.text(435, 335, 'COIN THEORY', 64, GOLD, 900, anchor='lm', stroke=3)
    c.text(437, 393, 'Money and the economy, explained with real data', 19, WHITE, 700, anchor='lm')
    c.text(437, 428, 'New videos every week', 17, MUTED, 600, anchor='lm')
    for i, (x, h) in enumerate(((70, 60), (110, 90), (150, 75), (190, 120), (230, 150))):
        c.rrect(x, 720 - h - 140, x + 28, 580, 6, (96, 165, 250, 70))
    for i, (x, h) in enumerate(((1050, 150), (1090, 120), (1130, 160), (1170, 200), (1210, 240))):
        c.rrect(x, 580 - h, x + 28, 580, 6, (52, 211, 153, 70))
    return img


def watermark():
    c = Canvas((14, 22, 40), (14, 22, 40), k=2)
    penny(c, 150, 130, 90, 0.0, 'happy', bounce=False)
    return c.img.crop((0, 0, 600, 600)).resize((150, 150), Image.LANCZOS)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    profile().save(os.path.join(OUT, 'brand_profile.png'))
    banner().save(os.path.join(OUT, 'brand_banner.png'))
    watermark().save(os.path.join(OUT, 'brand_watermark.png'))
    print('ok')
