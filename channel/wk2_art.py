"""Shared drawings and scene helpers for week 2 (episodes 3 and 4). All art is original, drawn in code."""
import os

import pandas as pd

from engine import *  # noqa: F401,F403

HERE = os.path.dirname(os.path.abspath(__file__))


def series(name):
    d = pd.read_csv(os.path.join(HERE, 'data', f'{name}.csv'))
    d.columns = ['date', 'v']
    d['date'] = pd.to_datetime(d['date'])
    d['v'] = pd.to_numeric(d['v'], errors='coerce')
    return d.dropna().set_index('date')['v']


def decimal_year(idx):
    return [d.year + (d.dayofyear - 1) / 366 for d in idx]


# ----------------------------------------------------------------- objects --
def gas_pump(c, x, y, s, price=None, a=1.0, color=CORAL):
    """Cartoon fuel pump; (x, y) is the middle of its base."""
    w, h = 150 * s, 260 * s
    c.rrect(x - w / 2, y - h, x + w / 2, y, 16 * s, color, mix(color, INK, 0.4), 4 * s, a)
    c.rrect(x - w / 2 + 16 * s, y - h + 22 * s, x + w / 2 - 16 * s, y - h + 102 * s, 10 * s, INK, None, 0, a)
    if price is not None:
        c.text(x, y - h + 62 * s, price, int(34 * s), GOLD, 900, a=a, shadow=False, family='Poppins')
    c.rrect(x - w / 2 + 26 * s, y - h + 124 * s, x + w / 2 - 26 * s, y - h + 150 * s, 6 * s,
            mix(color, WHITE, 0.4), a=a)
    c.rrect(x - w / 2 - 14 * s, y - 14 * s, x + w / 2 + 14 * s, y + 8 * s, 6 * s, mix(color, INK, 0.5), a=a)
    hx = x + w / 2
    c.line([(hx, y - h + 140 * s), (hx + 50 * s, y - h + 170 * s), (hx + 50 * s, y - 70 * s)], INK, 7 * s, a)
    c.rrect(hx + 36 * s, y - 110 * s, hx + 64 * s, y - 50 * s, 6 * s, (60, 66, 88), a=a)


def barrel(c, x, y, s, label=None, a=1.0, color=(70, 82, 110)):
    """Oil barrel; (x, y) is the middle of its base."""
    w, h = 110 * s, 150 * s
    c.rrect(x - w / 2, y - h, x + w / 2, y, 14 * s, color, mix(color, INK, 0.4), 4 * s, a)
    for f in (0.22, 0.78):
        c.line([(x - w / 2, y - h * f), (x + w / 2, y - h * f)], mix(color, INK, 0.45), 5 * s, a)
    c.ellipse(x, y - h, w / 2, 12 * s, mix(color, WHITE, 0.15), mix(color, INK, 0.4), 3 * s, a)
    c.icon('droplet', x, y - h * 0.5, 50 * s, GOLD, a=a, stroke=2.5)
    if label:
        c.text(x, y + 28 * s, label, int(22 * s), WHITE, 800, a=a)


def tanker(c, x, y, s, a=1.0, color=(200, 70, 70), t=0.0):
    """Oil tanker ship, side view; (x, y) is the waterline centre."""
    bob = math.sin(t * 2.0 + x * 0.01) * 3 * s
    y = y + bob
    hull = [(x - 170 * s, y - 40 * s), (x + 150 * s, y - 40 * s), (x + 185 * s, y - 5 * s),
            (x + 160 * s, y + 20 * s), (x - 160 * s, y + 20 * s)]
    c.poly(hull, color, mix(color, INK, 0.45), 3 * s, a)
    c.rrect(x - 160 * s, y - 52 * s, x + 130 * s, y - 40 * s, 3 * s, mix(color, INK, 0.25), a=a)
    c.rrect(x - 150 * s, y - 110 * s, x - 90 * s, y - 52 * s, 6 * s, CREAM, mix(CREAM, INK, 0.3), 2 * s, a)
    c.rrect(x - 136 * s, y - 132 * s, x - 118 * s, y - 110 * s, 3 * s, (60, 66, 88), a=a)
    for i in range(3):
        cx = x - 50 * s + i * 65 * s
        c.ellipse(cx, y - 56 * s, 24 * s, 8 * s, mix(color, WHITE, 0.3), a=a)


def waves(c, y, t, color=(96, 165, 250), a=0.35, x0=0, x1=W):
    pts = [(xx, y + math.sin(xx * 0.03 + t * 2) * 5) for xx in range(int(x0), int(x1) + 1, 8)]
    c.line(pts, color, 3, a)


def strait_map(c, k_block, t, a=1.0, ships=0.0):
    """Stylised map of the Persian Gulf and the Strait of Hormuz (not to scale)."""
    sea = (36, 76, 130)
    c.rrect(80, 110, 1200, 575, 28, sea, None, 0, a)
    land = (196, 170, 120)
    # Iran (north and east)
    c.poly([(80, 110), (1200, 110), (1200, 300), (1010, 330), (860, 300), (700, 250), (520, 220), (330, 190),
            (180, 170), (80, 180)], land, mix(land, INK, 0.4), 3, a)
    # Arabian Peninsula (south and west)
    c.poly([(80, 330), (240, 340), (420, 395), (600, 440), (760, 455), (860, 420), (900, 360), (950, 380),
            (980, 450), (1060, 500), (1200, 530), (1200, 575), (80, 575)], mix(land, (255, 220, 160), 0.2),
           mix(land, INK, 0.4), 3, a)
    c.text(640, 160, 'IRAN', 28, INK, 900, a=a * 0.8, shadow=False)
    c.text(420, 520, 'SAUDI ARABIA', 24, INK, 900, a=a * 0.8, shadow=False)
    c.text(1100, 555, 'OMAN', 20, INK, 900, a=a * 0.8, shadow=False)
    c.text(470, 365, 'Persian Gulf', 22, (200, 225, 255), 700, a=a * 0.9, shadow=False)
    c.text(1085, 490, 'to the world', 18, (200, 225, 255), 700, a=a * 0.9, shadow=False)
    # the strait
    c.circle(930, 345, 46, None, GOLD, 4, a=a * (0.6 + 0.4 * math.sin(t * 4) ** 2))
    c.text(930, 270, 'Strait of Hormuz', 22, GOLD, 900, a=a)
    # tankers moving through
    n = 5
    for i in range(n):
        f = ((t * 0.08 + i / n) % 1.0)
        if f < 0.5:
            px, py = lerp(380, 930, f / 0.5), lerp(300, 345, f / 0.5)
        else:
            px, py = lerp(930, 1160, (f - 0.5) / 0.5), lerp(345, 470, (f - 0.5) / 0.5)
        stop = k_block > 0 and px > 860
        if stop:
            continue
        tanker(c, px, py, 0.16, a=a * ships, t=t)
    if k_block > 0:
        c.line([(905, 320), (955, 370)], CORAL, 10, a * clamp(k_block))
        c.line([(955, 320), (905, 370)], CORAL, 10, a * clamp(k_block))


def fed_building(c, x, y, s, a=1.0, color=CREAM):
    """Classical bank building (the Fed); (x, y) is the base centre."""
    w = 360 * s
    c.rrect(x - w / 2 - 20 * s, y - 24 * s, x + w / 2 + 20 * s, y, 4 * s, mix(color, INK, 0.15), a=a)
    for i in range(6):
        cx = x - w / 2 + 30 * s + i * (w - 60 * s) / 5
        c.rrect(cx - 14 * s, y - 190 * s, cx + 14 * s, y - 24 * s, 4 * s, color, mix(color, INK, 0.3), 2 * s, a)
    c.rrect(x - w / 2 - 10 * s, y - 214 * s, x + w / 2 + 10 * s, y - 190 * s, 4 * s, mix(color, INK, 0.1), a=a)
    c.poly([(x - w / 2 - 20 * s, y - 214 * s), (x, y - 300 * s), (x + w / 2 + 20 * s, y - 214 * s)], color,
           mix(color, INK, 0.3), 3 * s, a)
    c.text(x, y - 245 * s, 'THE FED', int(24 * s), INK, 900, a=a, shadow=False)


def card(c, x, y, s, a=1.0, color=SKY, label='CREDIT'):
    w, h = 300 * s, 190 * s
    c.rrect(x - w / 2, y - h / 2, x + w / 2, y + h / 2, 18 * s, color, mix(color, INK, 0.4), 3 * s, a)
    c.rrect(x - w / 2, y - h / 2 + 38 * s, x + w / 2, y - h / 2 + 72 * s, 0, mix(color, INK, 0.5), a=a)
    c.rrect(x - w / 2 + 24 * s, y + 4 * s, x - w / 2 + 84 * s, y + 46 * s, 6 * s, GOLD, a=a)
    c.text(x + w / 2 - 20 * s, y + h / 2 - 26 * s, label, int(18 * s), WHITE, 800, anchor='rm', a=a,
           shadow=False)


def dial(c, x, y, r, value, vmax, label, a=1.0, color=CORAL):
    """Half-circle gauge showing value/vmax."""
    c.arc(x, y, r, 180, 360, (255, 255, 255, 40), 18 * r / 120, a)
    end = 180 + 180 * clamp(value / vmax)
    if end > 181:
        c.arc(x, y, r, 180, end, color, 18 * r / 120, a)
    ang = math.radians(end)
    c.line([(x, y), (x + math.cos(ang) * r * 0.8, y + math.sin(ang) * r * 0.8)], WHITE, 6 * r / 120, a)
    c.circle(x, y, 10 * r / 120, WHITE, a=a)
    c.text(x, y + 40 * r / 120, label, int(24 * r / 120), WHITE, 800, a=a)


# ------------------------------------------------------------ scene helpers --
def source(c, t, text):
    c.text(1150, 600, 'Source: ' + text, 14, MUTED, 400, anchor='rm', a=fade(t, 1), shadow=False)


def chip(c, x, y, text, color, k, size=22, w=None):
    if k <= 0:
        return
    w = w or (len(text) * size * 0.58 + 40)
    c.rrect(x - w / 2, y - size * 1.05, x + w / 2, y + size * 1.05, size, color, a=clamp(k))
    c.text(x, y, text, size, INK, 800, a=clamp(k), shadow=False)


def icon_row(c, t, items, start, span, y=340, color=GOLD, size=70, x0=90, width=1100, ring=80, label_size=22):
    """Reveal up to 4 icon+label items one after another across [start, start+span]."""
    n = len(items)
    gapx = width / n
    lsize = label_size
    for i, (ic, label) in enumerate(items):
        k = pop(t, start + span * (0.05 + 0.85 * i / n))
        if k <= 0:
            continue
        cx = x0 + gapx * (i + 0.5)
        c.circle(cx, y, ring * k, (255, 255, 255, 18), color, 3, a=clamp(k))
        c.icon(ic, cx, y, size * k, color, a=clamp(k))
        for j, part in enumerate(label.split('\n')):
            c.text(cx, y + ring + 45 + j * lsize * 1.36, part, lsize, WHITE, 800, a=clamp(k))


def compare_bars(c, t, items, start, span, vmax, fmt, box=(240, 170, 1040, 530), value_size=34, label_size=20):
    """items: (label, value, color). Bars grow one after another."""
    x0, y0, x1, y1 = box
    n = len(items)
    bw = (x1 - x0) / n
    c.line([(x0, y1), (x1, y1)], (255, 255, 255, 90), 2)
    for i, (label, v, col) in enumerate(items):
        at = start + span * i / n
        g = ease(seg(t, at, at + 1.0))
        if t < at:
            continue
        bx = x0 + i * bw + bw * 0.2
        top = y1 - (y1 - y0) * v / vmax * g
        c.rrect(bx, top, bx + bw * 0.6, y1, 12, col)
        c.text(bx + bw * 0.3, top - value_size * 0.82, fmt(v * g), value_size, col, 900)
        c.text(bx + bw * 0.3, y1 + label_size * 1.4, label, label_size, WHITE, 800)


def end_card(line, tag='Full story on Coin Theory'):
    """Closing Shorts scene: Penny waves and points viewers to the full video (drawn vertically)."""
    def draw(c, x):
        specks(c, x.t, 30, 70)
        penny(c, 360, 520, 130, x.t, 'happy', wave=True, talk=x.talk())
        c.text(360, 790, tag, 42, GOLD, 900, a=fade(x.t, 0.3))
    return dict(draw=draw, lines=[line], tail=1.2, vertical=True)


def source_v(c, t, text):
    """Source line for a vertical Shorts scene, just above the captions."""
    c.text(c.w - 40, 900, 'Source: ' + text, 16, MUTED, 400, anchor='rm', a=fade(t, 1), shadow=False)


def fmt_time(sec):
    return f'{int(sec // 60)}:{int(sec % 60):02d}'
