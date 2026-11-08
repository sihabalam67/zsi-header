"""Standalone Short (fx style): where a typical paycheck goes.

    python3 channel/sx06_short_paycheck.py [--stills]

Facts (check_numbers recomputes everything):
- Pay: BLS median usual weekly earnings, full-time wage and salary workers (FRED LES1252881500Q), latest quarter,
  x 52 weeks; paid every two weeks (26 paychecks).
- Federal income tax 2026 (IRS, Rev. Proc. 2025-32 / IRS newsroom, Oct 9 2025): single filer, standard deduction
  $16,100; 10% up to $12,400 of taxable income, 12% up to $50,400, 22% up to $105,700. No other deductions or
  credits; state and local taxes not included (said on screen).
- FICA: Social Security 6.2% (2026 wage base $184,500, SSA) + Medicare 1.45%, paid by the employee, and the same
  7.65% again by the employer.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from wk2_art import *  # noqa: E402,F401,F403
from engine import build, still  # noqa: E402
import fx  # noqa: E402

OUT = os.path.join(HERE, 'out')
BUILD = os.path.join(HERE, 'build', 'sx06_short_paycheck')
CASH = os.path.join(HERE, 'assets', 'photos', 'ep06s', 'cash.jpg')

WK = series('LES1252881500Q')
WEEK, WEEK_DATE = WK.iloc[-1], WK.index[-1]
GROSS = WEEK * 52
STD, B10, B12, B22 = 16100, 12400, 50400, 105700
SS_RATE, MED_RATE, WAGE_BASE = 0.062, 0.0145, 184500
TAXABLE = GROSS - STD
TAX = 0.10 * min(TAXABLE, B10) + 0.12 * max(0, min(TAXABLE, B12) - B10) + 0.22 * max(0, min(TAXABLE, B22) - B12)
SS, MED = SS_RATE * min(GROSS, WAGE_BASE), MED_RATE * GROSS
NET = GROSS - TAX - SS - MED
EMPLOYER = (SS_RATE + MED_RATE) * GROSS
COST = GROSS + EMPLOYER
EFF = TAX / GROSS
BRACKET = 12 if B10 < TAXABLE <= B12 else None
P_GROSS, P_SS, P_MED, P_NET = round(GROSS / 26), round(SS / 26), round(MED / 26), round(NET / 26)
P_TAX = P_GROSS - P_SS - P_MED - P_NET           # shown so the stub adds up exactly


def money(v):
    return f'${v:,.0f}'


def card(c, u, at, y, text, col=WHITE, fg=INK, size=40, w=520):
    kk = fx.pop(u, at, 0.3)
    if kk <= 0:
        return
    s = 0.7 + 0.3 * fx.clamp(kk)
    c.rrect(360 - w / 2 * s, y - 40 * s, 360 + w / 2 * s, y + 40 * s, 26, col, a=fx.clamp(kk))
    c.text(360, y, text, int(size * s), fg, 400, family='Anton', a=fx.clamp(kk), shadow=False)


def hook_draw(c, u):
    fx.photo(c, CASH, 1.15 - 0.04 * fx.clamp(u / 3), (0.83, 0.72), dark=0.55, sat=1.15)
    c.rrect(0, 0, 720, 1280, 0, (8, 10, 20, 140))
    s = 1.0 + 0.07 * max(0.0, 1 - abs(u - 0.15) / 0.15) if u < 0.3 else 1.0
    c.text(360, 300, 'YOUR JOB COSTS', 44, WHITE, 900)
    fx.title(c, money(COST), 400, int(120 * s), GOLD, 1, stroke=7)
    c.text(360, 560, 'YOU KEEP', 44, WHITE, 900)
    fx.title(c, money(NET), 660, int(120 * s), MINT, 1, stroke=7)
    k = fx.clamp(fx.pop(u, 1.4, 0.3))
    if k > 0:
        c.rrect(170, 800, 550, 860, 30, CORAL, a=k)
        c.text(360, 830, 'WHERE DID IT GO?', 36, WHITE, 400, family='Anton', a=k, shadow=False)
    if u > 0:
        fx.zoom_canvas(c, 1.01 + 0.012 * u, 360, 560)


def s_hook(c, x):
    hook_draw(c, max(0.0, x.t - x.L[0]))


def s_pay(c, x):  # the typical salary, counting up
    u = x.t - x.L[0]
    l1 = x.L[1] - x.L[0]
    c.rrect(0, 0, 720, 1280, 0, (14, 18, 30))
    c.text(360, 230, 'TYPICAL FULL-TIME WORKER', 34, WHITE, 900, a=fade(u, 0))
    v = WEEK * ease(fx.clamp((u - 0.4) / 1.2))
    fx.title(c, f'{money(v)} / WEEK', 380, 96, GOLD, 1, stroke=6)
    if u > l1:
        y = GROSS * ease(fx.clamp((u - l1 - 0.3) / 1.4))
        fx.title(c, f'{money(y)} / YEAR', 560, 96, MINT, 1, stroke=6)
    c.text(360, 700, f'median weekly pay, BLS, {WEEK_DATE:%b %Y} quarter', 22, MUTED, 800, a=fade(u, 0.6))
    fx.zoom_canvas(c, 1.01 + 0.008 * u, 360, 450)


def stub(c, u, rows, net_at=None, title='PAYCHECK: EVERY 2 WEEKS'):
    """A made-up pay stub; rows: (appear_at, label, amount_text, color)."""
    c.rrect(0, 0, 720, 1280, 0, (14, 18, 30))
    c.rrect(70, 200, 650, 860, 26, (240, 236, 226))
    c.text(360, 250, title, 30, INK, 900, shadow=False)
    c.line([(110, 290), (610, 290)], (180, 175, 165), 3)
    c.text(110, 340, 'Gross pay', 32, INK, 800, anchor='lm', shadow=False)
    c.text(610, 340, money(P_GROSS), 40, INK, 400, family='Anton', anchor='rm', shadow=False)
    for j, (at, lab, amt, col) in enumerate(rows):
        k = fx.clamp(fx.pop(u, at, 0.3))
        if k <= 0:
            continue
        y = 425 + j * 85
        dx = 40 * (1 - k)
        c.text(110 + dx, y, lab, 30, INK, 800, anchor='lm', a=k, shadow=False)
        c.text(610 + dx, y, amt, 40, col, 400, family='Anton', anchor='rm', a=k, shadow=False)
    if net_at is not None:
        k = fx.clamp(fx.pop(u, net_at, 0.3))
        if k > 0:
            c.line([(110, 680), (610, 680)], INK, 4)
            c.rrect(100, 705, 620, 830, 22, MINT, a=k)
            c.text(130, 767, 'TAKE-HOME', 34, INK, 900, anchor='lm', a=k, shadow=False)
            c.text(590, 767, money(P_NET), int(64 * (0.7 + 0.3 * k)), INK, 400, family='Anton', anchor='rm', a=k,
                   shadow=False)


def s_stub(c, x):
    u = x.t - x.L[0]
    l1 = x.L[1] - x.L[0]
    rows = [(l1 + 0.2, 'Social Security 6.2%', f'-{money(P_SS)}', CORAL),
            (l1 + 2.0, 'Medicare 1.45%', f'-{money(P_MED)}', CORAL),
            (l1 + 3.8, 'Federal income tax', f'-{money(P_TAX)}', CORAL)]
    stub(c, u, rows)
    if u < l1:
        card(c, u, 1.8, 930, 'THEN THE CUTS START', CORAL, WHITE, 40, 520)
    fx.zoom_canvas(c, 1.01 + 0.005 * u, 360, 530)


def s_net(c, x):
    u = x.t - x.L[0]
    rows = [(-1, 'Social Security 6.2%', f'-{money(P_SS)}', CORAL), (-1, 'Medicare 1.45%', f'-{money(P_MED)}', CORAL),
            (-1, 'Federal income tax', f'-{money(P_TAX)}', CORAL)]
    stub(c, u, rows, net_at=0.3)
    card(c, u, 2.4, 930, '+ STATE TAX IN MOST STATES', GOLD, INK, 34, 560)
    fx.zoom_canvas(c, 1.01 + 0.006 * u, 360, 600)


def s_bracket(c, x):  # 12% bracket, 8.6% paid: the first dollars are taxed less
    u = x.t - x.L[0]
    l1 = x.L[1] - x.L[0]
    c.rrect(0, 0, 720, 1280, 0, (14, 18, 30))
    if u < l1:
        c.text(360, 250, 'YOUR TAX BRACKET', 40, WHITE, 900, a=fade(u, 0))
        fx.title(c, f'{BRACKET}%', 380, 150, CORAL, fx.pop(u, 0.4), stroke=7)
        if u > 1.8:
            c.text(360, 560, 'BUT YOU PAY', 40, WHITE, 900, a=fade(u, 1.8))
            fx.title(c, f'{EFF * 100:.1f}%', 690, 150, MINT, fx.pop(u, 2.2), stroke=7)
            c.text(360, 830, 'of your pay in income tax', 30, WHITE, 800, a=fade(u, 2.2))
        fx.zoom_canvas(c, 1.01 + 0.012 * u, 360, 560)
        return
    tiers = [(STD, '0%', SKY, 'standard deduction'), (B10, '10%', MINT, 'first $12,400 taxed'),
             (TAXABLE - B10, '12%', GOLD, 'the rest')]
    tot = sum(v for v, *_ in tiers)
    y = 260
    for j, (v, rate, col, lab) in enumerate(tiers):
        k = ease(fx.clamp((u - l1 - 0.3 - j * 1.6) / 0.6))
        h = 620 * v / tot
        if k > 0:
            c.rrect(110, y, 110 + 500 * k, y + h - 8, 14, col)
            c.text(360, y + h / 2 - 18, f'{money(v)}', 38, INK, 400, family='Anton', a=k, shadow=False)
            c.text(360, y + h / 2 + 22, f'{rate}: {lab}', 22, INK, 900, a=k, shadow=False)
        y += h
    c.text(360, 200, f'{money(GROSS)} salary, taxed in layers', 32, WHITE, 900, a=fade(u, l1))
    fx.zoom_canvas(c, 1.01 + 0.012 * (u - l1), 360, 560)


def s_boss(c, x):
    u = x.t - x.L[0]
    c.rrect(0, 0, 720, 1280, 0, (14, 18, 30))
    c.text(360, 240, 'YOUR EMPLOYER ALSO PAYS', 36, WHITE, 900, a=fade(u, 0))
    fx.title(c, '+7.65%', 380, 130, GOLD, fx.pop(u, 0.5), stroke=7)
    k = fx.clamp(fx.pop(u, 2.0, 0.3))
    if k > 0:
        v = EMPLOYER * ease(fx.clamp((u - 2.0) / 1.0))
        c.rrect(110, 520, 610, 680, 30, (24, 30, 48), GOLD, 5, a=k)
        c.text(360, 600, f'{money(v)} / YEAR', 70, GOLD, 400, family='Anton', a=k)
    if u > 3.6:
        card(c, u, 3.6, 800, 'NEVER ON YOUR PAYCHECK', CORAL, WHITE, 40, 540)
    fx.zoom_canvas(c, 1.01 + 0.01 * u, 360, 500)


def s_end(c, x):
    u = x.t - x.L[0]

    def question(cv):
        cv.rrect(0, 0, 720, 1280, 0, (14, 18, 30))
        fx.title(cv, 'DID YOU\nKNOW THIS?', 330, int(100 * (1 + 0.04 * math.sin(u * 6))), GOLD, 1)
        for j, (txt, col) in enumerate((('YES', MINT), ('NO', CORAL))):
            kk = fx.clamp(fx.pop(u, 0.3 + j * 0.2, 0.3))
            bx = 230 + j * 260
            cv.rrect(bx - 110, 680 - 60 * kk, bx + 110, 680 + 60 * kk, 30, col)
            cv.text(bx, 680, txt, int(70 * kk) + 1, INK, 400, family='Anton', shadow=False)
        cv.text(360, 820 + 8 * math.sin(u * 4), 'tell me in the comments', 32, WHITE, 900)
    brk = x.dur - x.L[0] - 0.95
    if u < brk:
        return question(c)
    fx.frame_break(c, u - brk + 0.5, x.t, question, lambda cv: hook_draw(cv, 0.0))


S = dict(vertical=True, lead=0.1, gap=0.15, captions=True, cap_y=1080)
SCENES = [
    dict(S, draw=s_hook, lead=0.05, lines=[
        f"!Your job costs your boss about {round(COST / 1000)} thousand dollars. You keep about "
        f"{round(NET / 1000)} thousand. Here's where the rest goes.",
    ], punch=lambda L: [0.12], sfx=lambda L: [(0.12, 'hit'), (1.4, 'pop')]),
    dict(S, draw=s_pay, lines=[
        f"The typical full-time worker earns about {WEEK:,.0f} dollars a week.",
        f"That's {GROSS:,.0f} dollars a year.",
    ], sfx=lambda L: [(L[0] + 0.4, 'tick'), (L[0] + 1.6, 'ding'), (L[1] + 0.3, 'tick'), (L[1] + 1.7, 'ding')]),
    dict(S, draw=s_stub, lines=[
        f"Paid every two weeks: {P_GROSS:,} dollars. Then the cuts start.",
        f"Social Security: 6.2 percent. Medicare: 1.45. Federal income tax: about {P_TAX} dollars.",
    ], sfx=lambda L: [(L[0] + 1.8, 'down'), (L[1] + 0.2, 'pop'), (L[1] + 2.0, 'pop'), (L[1] + 3.8, 'pop')]),
    dict(S, draw=s_net, lines=[
        f"!Take-home: about {P_NET:,} dollars. Plus state tax in most states.",
    ], sfx=lambda L: [(L[0] + 0.3, 'hit'), (L[0] + 2.4, 'pop')]),
    dict(S, draw=s_bracket, lines=[
        f"The surprise? This worker is in the {BRACKET} percent bracket, but pays just {EFF * 100:.1f} percent "
        "in income tax.",
        f"The first {STD:,} dollars aren't taxed. The next {B10:,} pay just 10 percent.",
    ], sfx=lambda L: [(L[0] + 0.4, 'pop'), (L[0] + 2.2, 'hit'), (L[1] + 0.3, 'pop'), (L[1] + 1.9, 'pop'),
                      (L[1] + 3.5, 'pop')]),
    dict(S, draw=s_boss, lines=[
        f"!And your boss pays another 7.65 percent on top: about {EMPLOYER:,.0f} dollars a year you never see.",
    ], sfx=lambda L: [(L[0] + 0.5, 'hit'), (L[0] + 2.0, 'tick'), (L[0] + 3.0, 'ding'), (L[0] + 3.6, 'pop')]),
    dict(S, draw=s_end, tail=1.0, cam=(1.0, 1.0), lines=[
        "Did you know your boss pays that too? Yes or no?",
    ], sfx=lambda L: [(L[0] + 0.3, 'pop'), (L[0] + 0.5, 'pop')]),
]


def check_numbers():
    script = ' '.join(l for sc in SCENES for l in sc['lines'])
    assert WEEK == 1239 and WEEK_DATE.strftime('%Y-%m') == '2026-07' and GROSS == 64428
    assert TAXABLE == 48328 and BRACKET == 12 and round(TAX) == 5551 and round(EFF * 100, 1) == 8.6
    assert round(SS) == 3995 and round(MED) == 934 and round(NET) == 53948 and round(EMPLOYER) == 4929
    assert round(COST) == 69357 and GROSS < WAGE_BASE
    assert (P_GROSS, P_SS, P_MED, P_TAX, P_NET) == (2478, 154, 36, 213, 2075), (P_GROSS, P_SS, P_MED, P_TAX, P_NET)
    assert abs(P_TAX - TAX / 26) < 1
    for s in ('69 thousand', '54 thousand', '1,239 dollars a week', '64,428 dollars a year', '2,478 dollars',
              '6.2 percent', 'Medicare: 1.45', 'about 213 dollars', '2,075 dollars', '8.6 percent',
              '16,100 dollars', '12,400', '7.65 percent', '4,929 dollars', 'most states', '12 percent bracket'):
        assert s in script, s
    print(f'numbers check: OK  ${WEEK:,.0f}/wk ({WEEK_DATE:%b %Y}) = ${GROSS:,.0f}; tax ${TAX:,.0f} ({EFF:.1%}), '
          f'SS ${SS:,.0f}, Medicare ${MED:,.0f}, net ${NET:,.0f}; employer ${EMPLOYER:,.0f}, cost ${COST:,.0f}; '
          f'paycheck {P_GROSS} - {P_SS} - {P_MED} - {P_TAX} = {P_NET}')


if __name__ == '__main__':
    check_numbers()
    os.makedirs(BUILD, exist_ok=True)
    if '--stills' in sys.argv:
        out = os.path.join(BUILD, 'stills')
        os.makedirs(out, exist_ok=True)
        for si, sc in enumerate(SCENES):
            starts = [0.1 + 3.6 * j for j in range(len(sc['lines']))]
            for du in (0.0, 2.6, 4.6):
                still(sc, 0.1 + du, os.path.join(out, f's{si}_{du}.png'), starts=starts, layout='short')
        print('stills in', out)
        sys.exit()
    build(SCENES, os.path.join(OUT, 'sx06_short_paycheck.mp4'), BUILD, layout='short', loop=True)
