"""Thumbnail toolkit (v2): the pro look. Bright light-burst backgrounds, subjects drawn on their own layer and given
a thick white outline, a coloured glow and a drop shadow, optional tilt, and huge stroked text.

    from thumbkit import Thumb
    th = Thumb(('#ff3d2e', '#ffb02e'))                  # burst colours: centre, edge
    th.layer(lambda c: card(c, 640, 360, 2.0), outline=10, glow=(255, 220, 120), tilt=-8)
    th.text(980, 380, '21%', 260, color=WHITE, stroke=14)
    th.save('out/ep04_thumb_v2a.png')

Rules (the 'squint test'): one subject, one emotion, 2-4 words, readable at 160 px wide, no text that repeats the title.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageChops, ImageDraw, ImageFilter  # noqa: E402
from engine import Canvas, K, W, H, font  # noqa: E402

TW, TH = int(W * K), int(H * K)  # drawn at 3840 x 2160, saved at 1280 x 720


def hexrgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


class Thumb:
    def __init__(self, burst=('#ff4d2e', '#7a0f1f'), center=(0.5, 0.45), rays=18):
        c0, c1 = (hexrgb(x) if isinstance(x, str) else x for x in burst)
        cx, cy = center[0] * TW, center[1] * TH
        yy, xx = [a.astype('float32') for a in __import__('numpy').mgrid[0:TH // 4, 0:TW // 4]]
        import numpy as np
        r = np.sqrt((xx * 4 - cx) ** 2 + (yy * 4 - cy) ** 2) / math.hypot(TW, TH) * 1.6
        r = np.clip(r, 0, 1)[..., None]
        bg = (np.array(c0) * (1 - r) + np.array(c1) * r).astype('uint8')
        img = Image.fromarray(bg, 'RGB').resize((TW, TH), Image.BICUBIC)
        if rays:  # soft light rays from the centre
            ray = Image.new('L', (TW, TH), 0)
            d = ImageDraw.Draw(ray)
            for i in range(rays):
                a0 = 2 * math.pi * i / rays
                a1 = a0 + math.pi / rays * 0.55
                R = TW * 1.2
                d.polygon([(cx, cy), (cx + R * math.cos(a0), cy + R * math.sin(a0)),
                           (cx + R * math.cos(a1), cy + R * math.sin(a1))], fill=38)
            ray = ray.filter(ImageFilter.GaussianBlur(TW // 120))
            img = Image.composite(Image.new('RGB', (TW, TH), (255, 255, 255)), img, ray)
        self.img = img.convert('RGBA')

    def layer(self, draw, outline=10, outline_color=(255, 255, 255), glow=None, glow_size=40, shadow=True,
              tilt=0, pivot=None):
        """Draw `draw(canvas)` on its own transparent layer (logical 1280x720 coordinates), then add effects."""
        lay = Image.new('RGBA', (TW, TH), (0, 0, 0, 0))
        c = Canvas(img=lay, k=K)
        draw(c)
        if tilt:
            lay = lay.rotate(tilt, resample=Image.BICUBIC,
                             center=None if pivot is None else (pivot[0] * K, pivot[1] * K))
        a = lay.getchannel('A')
        if shadow:
            sh = a.filter(ImageFilter.GaussianBlur(18 * K / 3)).point(lambda v: int(v * 0.55))
            self.img.paste((0, 0, 0, 255), (int(10 * K), int(14 * K)), sh)
        if glow:
            g = a.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(glow_size * K / 3))
            g = g.point(lambda v: min(255, int(v * 1.6)))
            self.img.paste(tuple(glow) + (255,), (0, 0), g)
        if outline:
            o = a
            n = max(3, int(outline * K / 3) | 1)
            for _ in range(3):
                o = o.filter(ImageFilter.MaxFilter(n if n <= 15 else 15))
            o = o.filter(ImageFilter.GaussianBlur(1))
            self.img.paste(tuple(outline_color) + (255,), (0, 0), o)
        self.img.alpha_composite(lay)

    def text(self, x, y, s, size, color=(255, 255, 255), stroke=12, stroke_color=(20, 16, 30), glow=None,
             tilt=0, anchor='mm', weight=900):
        def draw(c):
            c.text(x, y, s, size, color, weight, anchor=anchor, shadow=False, stroke=stroke, stroke_fill=stroke_color)
        self.layer(draw, outline=0, glow=glow, glow_size=26, shadow=True, tilt=tilt, pivot=(x, y))

    def save(self, path):
        self.img.convert('RGB').resize((1280, 720), Image.LANCZOS).save(path)
        return path


def squint(paths, out):
    """Side-by-side preview of thumbnails at real phone feed size (about 320 px wide) and full size."""
    ims = [Image.open(p).convert('RGB') for p in paths]
    small = [im.resize((320, 180), Image.LANCZOS) for im in ims]
    sheet = Image.new('RGB', (640 * len(ims) + 10 * (len(ims) - 1), 360 + 200), (255, 255, 255))
    for i, im in enumerate(ims):
        sheet.paste(im.resize((640, 360), Image.LANCZOS), (i * 650, 0))
        sheet.paste(small[i], (i * 650 + 160, 370))
    sheet.save(out)
    return out
