"""Manim scene for the sx02 Short: two balances racing to zero (vertical 1080x1920, no LaTeX).

    manim -qh --resolution 1080,1920 --fps 30 channel/manim/payoff_race.py PayoffRace
Reads channel/assets/gen/sx02/payoff.json (written by channel/cards_math.py).
"""
import json
import os

from manim import (Scene, Axes, VMobject, Text, Dot, VGroup, Create, FadeIn, Write, GrowFromCenter, Flash,
                   ValueTracker, always_redraw, config, UP, DOWN, LEFT, RIGHT, UR, rate_functions, linear)

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, '..', 'assets', 'gen', 'sx02', 'payoff.json')))
config.frame_width = 9
config.frame_height = 16
config.background_color = '#0e1220'
MINT, CORAL, GOLD, MUTED = '#34d399', '#f87171', '#fbbf24', '#94a3b8'
FONT = 'Poppins'


class PayoffRace(Scene):
    def construct(self):
        ax = Axes(x_range=[0, 20, 5], y_range=[0, 5000, 1000], x_length=7.6, y_length=8.4,
                  axis_config={'color': MUTED, 'stroke_width': 3, 'include_tip': False}
                  ).shift(UP * 0.6 + RIGHT * 0.35)
        ticks = VGroup(*[Text(str(v), font=FONT, font_size=26, color=MUTED).next_to(ax.c2p(v, 0), DOWN, buff=0.2)
                         for v in (0, 5, 10, 15, 20)],
                       *[Text(f'${v // 1000}K', font=FONT, font_size=24, color=MUTED).next_to(ax.c2p(0, v), LEFT, buff=0.15)
                         for v in (1000, 2000, 3000, 4000, 5000)])  # plain Text: no LaTeX needed
        xl = Text('years', font=FONT, font_size=30, color=MUTED).next_to(ax.x_axis, DOWN, buff=0.75)
        yl = Text('balance ($)', font=FONT, font_size=30, color=MUTED).next_to(ax, UP, buff=0.35).align_to(ax, LEFT)
        self.play(Create(ax), FadeIn(ticks), FadeIn(xl), FadeIn(yl), run_time=0.8)

        def curve(path, color):
            pts = [ax.c2p(i / 12, v) for i, v in enumerate(path)]
            m = VMobject(stroke_color=color, stroke_width=10)
            m.set_points_smoothly(pts)
            return m

        fix = curve(D['fix']['path'], MINT)
        mn = curve(D['min']['path'], CORAL)
        yf, ym = D['fix']['months'] / 12, D['min']['months'] / 12
        T = ValueTracker(0.001)  # one clock in years drives both lines, so they race fairly

        def part(src, total, color):
            return always_redraw(lambda: VMobject(stroke_color=color, stroke_width=10).pointwise_become_partial(
                src, 0, min(1.0, max(1e-3, T.get_value() / total))))
        lf, lm = part(fix, yf, MINT), part(mn, ym, CORAL)
        hf = always_redraw(lambda: Dot(lf.get_end(), radius=0.14, color=MINT))  # always at the tip of the line
        hm = always_redraw(lambda: Dot(lm.get_end(), radius=0.14, color=CORAL))
        lab_f = Text('$200 a month', font=FONT, font_size=40, color=MINT, weight='BOLD').move_to(ax.c2p(11, 4500))
        lab_m = Text('minimum only', font=FONT, font_size=40, color=CORAL, weight='BOLD').move_to(ax.c2p(11, 3800))
        self.play(FadeIn(lab_f), FadeIn(lab_m), run_time=0.4)
        self.add(lf, lm, hf, hm)
        self.play(T.animate.set_value(yf), run_time=1.5, rate_func=linear)
        done = Text(f"{yf:.1f} YEARS", font='Anton', font_size=72, color=MINT).move_to(ax.c2p(8.6, 650))
        self.play(GrowFromCenter(done), Flash(ax.c2p(yf, 0), color=MINT), run_time=0.5)
        self.play(T.animate.set_value(ym), run_time=3.0, rate_func=rate_functions.ease_in_out_sine)
        yrs = Text(f"{ym:.0f} YEARS", font='Anton', font_size=110, color=CORAL).move_to(ax.c2p(12.6, 2500))
        self.play(GrowFromCenter(yrs), Flash(ax.c2p(ym, 0), color=CORAL), run_time=0.5)
        self.wait(1.4)
