"""Episode 7 (long): the Binance hack. Built from confirmed facts only (FACTS in ep07_binance.py, each sourced).

    python3 channel/ep07_long.py [--hook-only] [--stills]

The opening uses a Google Flow clip made by the channel owner (assets/flow/binance_vault_clip.mp4) under our own
narration, captions and graphics; its own audio is not used.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from wk2_art import *  # noqa: E402,F401,F403
from engine import build  # noqa: E402
from ep07_binance import F, check_numbers  # noqa: E402

OUT = os.path.join(HERE, 'out')
BUILD = os.path.join(HERE, 'build', 'ep07_long')
CLIP = os.path.join(HERE, 'assets', 'flow', 'binance_vault_clip.mp4')
BOOM = 2.55 / 0.72  # when the vault door blows open (clip played at 0.72x speed)


def s_hook(c, x):
    """Over the Flow clip: the number lands the moment the vault blows."""
    t, L = x.t, x.L
    k = pop(t, BOOM)
    if k > 0:
        c.text(640, 300, f'${F["amount_bn"]} BILLION', int(120 * (0.6 + 0.4 * clamp(k))), GOLD, 900, a=clamp(k),
               stroke=8)
    k2 = pop(t, BOOM + 1.6)
    if k2 > 0:
        c.rrect(420, 370, 860, 440, 34, CORAL, a=clamp(k2))
        c.text(640, 405, f'GONE IN ABOUT {F["minutes"]} MINUTES', 30, INK, 900, a=clamp(k2), shadow=False)
    if len(L) > 1 and t > L[1]:
        penny(c, 1120, 600, 70, t, 'shocked', look=(-1, -0.3), talk=x.talk(), a=fade(t, L[1]))


SCENES = [
    dict(draw=s_hook, bg_video=CLIP, bg_speed=0.72, lead=0.3, gap=0.3, tail=0.6, cam=(1.0, 1.1), lines=[
        f"!{{$6.3 billion|Six point three billion dollars}}. Gone, in about {F['minutes']} minutes.",
        "This is the biggest crypto theft in history. Here's exactly how it happened, and what it means for "
        "anyone who keeps money on an exchange.",
    ], punch=lambda L: [BOOM, BOOM + 1.6], sfx=lambda L: [(BOOM, 'down'), (BOOM + 1.6, 'pop')]),
]

if __name__ == '__main__':
    check_numbers()
    os.makedirs(BUILD, exist_ok=True)
    if '--hook-only' in sys.argv:
        build(SCENES[:1], os.path.join(OUT, 'ep07_hook_test.mp4'), BUILD, layout='long')
        sys.exit()
