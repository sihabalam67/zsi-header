#!/usr/bin/env python3
"""Coin Theory, episode 5 (bonus): Microsoft's 60,000 buyouts and what the job data really says.

Data (FRED): JTSLDL (layoffs and discharges), JTSQUL (quits), JTSJOL (job openings), JTSHIR (hires rate), all from
BLS JOLTS; ICSA (initial jobless claims, Dept. of Labor); USINFO (information-sector jobs), PAYEMS, UNEMPLOY,
UEMPMEAN, UNRATE (BLS). Microsoft facts are from news reports cited in the description. check_numbers() refuses to
render if the narration disagrees with the data.

    python3 channel/ep05_jobs.py [--stills] [--no-short] [--shorts-only]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wk2_art import *  # noqa: E402,F401,F403

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
BUILD = os.path.join(HERE, 'build', 'ep05')

LAY = series('JTSLDL')
QUIT = series('JTSQUL')
OPEN = series('JTSJOL')
HIRE = series('JTSHIR')
CLAIMS = series('ICSA')
INFO = series('USINFO')
PAY = series('PAYEMS')
UNEMP = series('UNEMPLOY')
WEEKS = series('UEMPMEAN')
UNRATE = series('UNRATE')
HEALTH = series('CES6562000001')
MANUF = series('MANEMP')
SAHM = series('SAHMREALTIME')
FED = series('DFEDTARU')

L_NOW, L_AT = LAY.iloc[-1], LAY.index[-1]
L19 = LAY['2019'].mean()
L_MAX, L_MAX_AT = LAY.max(), LAY.idxmax()
RATE_NOW = L_NOW / PAY[L_AT] * 100
RATE19 = (LAY['2019'] / PAY['2019']).mean() * 100
C_NOW, C_AT = CLAIMS.iloc[-1], CLAIMS.index[-1]
C19 = CLAIMS['2019'].mean()
O_NOW, O_PEAK, O_PEAK_AT = OPEN.iloc[-1], OPEN.max(), OPEN.idxmax()
RATIO = (OPEN / UNEMP).dropna()
R_NOW, R_PEAK = RATIO.iloc[-1], RATIO.max()
H_NOW, H19 = HIRE.iloc[-1], HIRE['2019'].mean()
W_NOW, W19 = WEEKS.iloc[-1], WEEKS['2019'].mean()
Q_NOW, Q_PEAK, Q_PEAK_AT = QUIT.iloc[-1], QUIT.max(), QUIT.idxmax()
I_NOW = INFO.iloc[-1]
I_PEAK, I_PEAK_AT = INFO['2015':].max(), INFO['2015':].idxmax()
I_DROP = (I_PEAK - I_NOW) * 1000
I_PCT = (I_PEAK - I_NOW) / I_PEAK * 100
P_AT = PAY.index[-1]
YA = P_AT - pd.DateOffset(years=1)
P_CHG = (PAY[P_AT] - PAY[YA]) * 1000
P19 = (PAY['2019-12-01'] - PAY['2018-12-01']) * 1000 / 12
H_CHG = (HEALTH[P_AT] - HEALTH[YA]) * 1000
I_CHG = (INFO[P_AT] - INFO[YA]) * 1000
M_CHG = (MANUF[P_AT] - MANUF[YA]) * 1000
U_NOW, U19 = UNRATE.iloc[-1], UNRATE['2019'].mean()
S_NOW = SAHM.iloc[-1]
N_HIKES = int((FED['2022-01-01':'2023-12-31'].diff() > 0).sum())
LAY_X, LAY_Y = decimal_year(LAY.index), [min(v, 4.2) for v in LAY.values / 1000]  # Mar 2020 spike capped
OPEN_X, OPEN_Y = decimal_year(OPEN.index), list(OPEN.values / 1000)
INFO_X, INFO_Y = decimal_year(INFO['2015':].index), list(INFO['2015':].values / 1000)


def mil(v):
    return f'{v / 1000:.2f} million'


def office(c, x, y, s, a=1.0, lit=0.6):
    """Cartoon office tower; (x, y) is the base centre."""
    w, h = 220 * s, 360 * s
    c.rrect(x - w / 2, y - h, x + w / 2, y, 10 * s, (70, 90, 130), mix((70, 90, 130), INK, 0.4), 3 * s, a)
    for r in range(7):
        for k in range(4):
            on = ((r * 7 + k * 3) % 5) / 4 < lit
            c.rrect(x - w / 2 + 20 * s + k * 48 * s, y - h + 22 * s + r * 46 * s, x - w / 2 + 52 * s + k * 48 * s,
                    y - h + 50 * s + r * 46 * s, 4 * s, (255, 220, 120) if on else (40, 52, 80), a=a)
    c.rrect(x - 26 * s, y - 60 * s, x + 26 * s, y, 4 * s, (40, 52, 80), a=a)


# ------------------------------------------------------------------ scenes --
def s_hook(c, x):
    t, L = x.t, x.L
    specks(c, t, 71)
    office(c, 780, 600, 1.25, a=fade(t, 0.1))
    n = int(ease(seg(t, L[0] + 0.8, L[0] + 3.2)) * 60000)
    if n:
        c.rrect(930, 140, 1240, 260, 20, (14, 22, 40, 230), CORAL, 3)
        c.text(1085, 185, f'{n:,}', 52, CORAL, 900)
        c.text(1085, 235, 'buyout offers', 20, WHITE, 800)
    if t > L[0] + 3.5:
        chip(c, 1085, 300, '~1 in 4 Microsoft employees', GOLD, pop(t, L[0] + 3.5), 18)
    if t > L[2]:
        c.icon('search', 1080, 470, 110 * pop(t, L[2] + 0.3), SKY, stroke=3)
    penny(c, 260, 470, 62, t, 'shocked' if L[0] + 3 < t < L[2] else 'happy', look=(1, 0), talk=x.talk())


def s_title(c, x):
    t = x.t
    specks(c, t, 72, 60)
    k = ease_out(seg(t, 0.1, 0.7))
    c.text(640, 240 - 20 * (1 - k), '60,000 BUYOUTS', 84, CORAL, 900, a=k)
    c.text(640, 340 - 20 * (1 - k), 'Are layoffs really rising?', 50, WHITE, 900, a=k)
    c.text(640, 660, 'COIN THEORY', 22, MUTED, 800, a=fade(t, 0.8))


def s_buyout(c, x):
    t, L = x.t, x.L
    specks(c, t, 73)
    if t < L[2]:
        for i, (head, ic, col, sub, at) in enumerate((('LAYOFF', 'user-minus', CORAL, 'company decides', 0.3),
                                                      ('BUYOUT', 'hand-coins', MINT, 'you choose, and get paid',
                                                       L[1]))):
            k = pop(t, at)
            if k <= 0:
                continue
            cx = 360 + i * 560
            c.rrect(cx - 230, 150, cx + 230, 520, 24, (255, 255, 255, 14), col, 3, a=clamp(k))
            c.text(cx, 200, head, 40, col, 900, a=clamp(k))
            c.icon(ic, cx, 320, 120 * k, col, stroke=2.5)
            c.text(cx, 450, sub, 26, WHITE, 800, a=clamp(k))
        return
    if t < L[4]:
        c.text(640, 90, 'Microsoft\'s offer', 36, WHITE, 900, a=fade(t, L[2]))
        rows = (('users', 'VP level and below'), ('globe', 'US, Canada, India, UK'),
                ('calendar-clock', 'Decide by early December'))
        icon_row(c, t, rows, L[2] + 0.2, max(1.0, L[3] - L[2]), y=300, color=SKY)
        if t > L[3]:
            chip(c, 640, 560, '2nd buyout this year: earlier one, 30%+ of ~8,750 took it', GOLD, pop(t, L[3] + 0.3),
                 18)
        return
    if t < L[5]:
        c.icon('server', 420, 330, 170, GOLD, a=fade(t, L[4]))
        c.icon('arrow-right', 640, 330, 70, MUTED, a=fade(t, L[4] + 0.6))
        c.icon('users', 860, 330, 170, CORAL, a=fade(t, L[4] + 1.2))
        c.text(420, 480, 'AI spending up', 26, GOLD, 900, a=fade(t, L[4] + 0.3))
        c.text(860, 480, 'headcount down', 26, CORAL, 900, a=fade(t, L[4] + 1.4))
        return
    c.text(640, 110, 'How many usually accept?', 34, WHITE, 900, a=fade(t, L[5]))
    k = pop(t, L[5] + 0.6)
    for i in range(100):
        cx, cy = 290 + (i % 20) * 36, 220 + (i // 20) * 62
        took = i < 5
        person(c, cx, cy + 40, 0.28 * k, MINT if took else (90, 100, 125), t, i, 'happy', a=clamp(k))
    chip(c, 640, 590, 'Similar programs: about 3-5% said yes', MINT, pop(t, L[5] + 2), 22)


def s_layoffs(c, x):
    t, L = x.t, x.L
    c.text(640, 60, 'Layoffs and discharges per month, US (millions)', 30, WHITE, 800, a=fade(t, 0))
    k = ease(seg(t, L[0] + 0.5, L[1] + 2))
    px, py = line_chart(c, (150, 120, 1150, 530), LAY_X, LAY_Y, (2001, LAY_X[-1] + 0.2), (0, 4), k, CORAL,
                        xticks=range(2002, 2027, 4), yticks=range(0, 5), yfmt='{:.0f}M', a=fade(t, 0.1), width=3)
    if t > L[3] - 0.5:
        c.text(px(2020.2), 140, f'Mar 2020: {L_MAX / 1000:.1f}M (off the chart)', 18, CORAL, 800,
               a=fade(t, L[3] - 0.3))
    for xx, v, lab, col, at in ((2019.5, L19 / 1000, f'2019 avg: {L19 / 1000:.2f}M', GOLD, L[2] + 1),
                                (LAY_X[-1], L_NOW / 1000, f'now: {L_NOW / 1000:.2f}M', MINT, L[1] + 2)):
        kk = pop(t, at)
        if kk > 0:
            c.circle(px(xx), py(v), 9 * kk, col, WHITE, 2)
            bx = min(max(px(xx) - 60, 230), 1020)
            c.rrect(bx - 95, py(v) - 70, bx + 95, py(v) - 32, 14, col, a=clamp(kk))
            c.text(bx, py(v) - 51, lab, 19, INK, 800, a=clamp(kk), shadow=False)
    if t > L[2] + 3:
        chip(c, 640, 590, f'Share of all jobs: {RATE_NOW:.1f}% now vs {RATE19:.1f}% in 2019', GOLD,
             pop(t, L[2] + 3.3), 20)
    source(c, t, 'BLS JOLTS (JTSLDL), payrolls (PAYEMS) via FRED') if t < L[2] + 3 else None


def s_claims(c, x):
    t, L = x.t, x.L
    specks(c, t, 74)
    c.icon('clipboard-list', 260, 330, 170, SKY, a=fade(t, 0))
    c.text(260, 470, 'new jobless claims', 22, SKY, 800, a=fade(t, 0.3))
    if t > L[1]:
        compare_bars(c, t, (('2019 weekly avg', C19 / 1000, GOLD), ('last week', C_NOW / 1000, MINT)), L[1] + 0.3,
                     2.5, 300, lambda v: f'{v:.0f}K', box=(520, 160, 1180, 500))
    if t > L[2]:
        chip(c, 850, 590, 'No sign of mass layoffs (yet)', MINT, pop(t, L[2] + 0.3), 22)
    source(c, t, 'US Dept. of Labor initial claims (ICSA) via FRED') if t < L[2] else None


def s_hiring(c, x):
    t, L = x.t, x.L
    if t < L[3]:
        c.text(640, 60, 'Job openings, US (millions)', 30, WHITE, 800, a=fade(t, 0))
        k = ease(seg(t, L[1], L[1] + 3))
        px, py = line_chart(c, (150, 120, 1150, 530), OPEN_X, OPEN_Y, (2001, OPEN_X[-1] + 0.2), (0, 14), k, SKY,
                            xticks=range(2002, 2027, 4), yticks=range(0, 15, 2), yfmt='{:.0f}M', a=fade(t, 0.1),
                            width=3)
        for xx, v, lab, col, at in ((OPEN_X[OPEN_Y.index(O_PEAK / 1000)], O_PEAK / 1000, f'Mar 2022: {O_PEAK / 1000:.1f}M',
                                     GOLD, L[1] + 2), (OPEN_X[-1], O_NOW / 1000, f'now: {O_NOW / 1000:.1f}M', CORAL,
                                                       L[1] + 4)):
            kk = pop(t, at)
            if kk > 0:
                c.circle(px(xx), py(v), 9 * kk, col, WHITE, 2)
                bx = min(max(px(xx) - 60, 230), 1020)
                c.rrect(bx - 90, py(v) - 66, bx + 90, py(v) - 28, 14, col, a=clamp(kk))
                c.text(bx, py(v) - 47, lab, 19, INK, 800, a=clamp(kk), shadow=False)
        if t > L[2]:
            chip(c, 640, 590, f'Open jobs per unemployed person: {R_PEAK:.0f} then, {R_NOW:.0f} now', GOLD,
                 pop(t, L[2] + 0.3), 20)
        source(c, t, 'BLS JOLTS (JTSJOL), unemployed (UNEMPLOY) via FRED') if t < L[2] else None
        return
    specks(c, t, 75)
    c.text(640, 90, 'A low-hire, low-fire job market', 34, WHITE, 900, a=fade(t, L[3]))
    compare_bars(c, t, (('hiring rate 2019', H19, GOLD), ('hiring rate now', H_NOW, CORAL)), L[3] + 0.3, 2.0, 5,
                 lambda v: f'{v:.1f}%', box=(150, 170, 620, 500))
    if t > L[5]:
        compare_bars(c, t, (('weeks to find work 2019', W19, GOLD), ('now', W_NOW, CORAL)), L[5] + 0.3, 2.0, 30,
                     lambda v: f'{v:.0f} wks', box=(680, 170, 1150, 500))
    source(c, t, 'BLS JOLTS hires rate (JTSHIR), mean weeks unemployed (UEMPMEAN) via FRED')


def s_quits(c, x):
    t, L = x.t, x.L
    specks(c, t, 76)
    c.icon('door-open', 300, 320, 180, GOLD, a=fade(t, 0))
    compare_bars(c, t, (('Apr 2022 (record)', Q_PEAK / 1000, GOLD), ('now', Q_NOW / 1000, SKY)), L[0] + 2, 3.0, 5,
                 lambda v: f'{v:.1f}M', box=(560, 160, 1160, 500))
    c.text(860, 110, 'People quitting per month', 28, WHITE, 900, a=fade(t, 0.2))
    if t > L[2]:
        chip(c, 640, 590, '"The great stay"', SKY, pop(t, L[2] + 0.3), 24)
    source(c, t, 'BLS JOLTS quits (JTSQUL) via FRED') if t < L[2] else None


def s_tech(c, x):
    t, L = x.t, x.L
    if t < L[3]:
        c.text(640, 60, 'Information-sector jobs: software, telecom, media (millions)', 28, WHITE, 800, a=fade(t, 0))
        k = ease(seg(t, L[0] + 1, L[1] + 3))
        px, py = line_chart(c, (150, 120, 1150, 530), INFO_X, INFO_Y, (2015, INFO_X[-1] + 0.1), (2.6, 3.2), k, SKY,
                            xticks=range(2015, 2027, 2), yticks=(2.6, 2.8, 3.0, 3.2), yfmt='{:.1f}M', a=fade(t, 0.1),
                            width=4)
        for xx, v, lab, col, at in ((decimal_year([I_PEAK_AT])[0], I_PEAK / 1000, f'Nov 2022: {I_PEAK / 1000:.2f}M',
                                     GOLD, L[1] + 1), (INFO_X[-1], I_NOW / 1000, f'now: {I_NOW / 1000:.2f}M', CORAL,
                                                       L[1] + 3)):
            kk = pop(t, at)
            if kk > 0:
                c.circle(px(xx), py(v), 9 * kk, col, WHITE, 2)
                bx = min(max(px(xx) - 60, 230), 1020)
                c.rrect(bx - 95, py(v) - 66, bx + 95, py(v) - 28, 14, col, a=clamp(kk))
                c.text(bx, py(v) - 47, lab, 19, INK, 800, a=clamp(kk), shadow=False)
        if t > L[2]:
            chip(c, 640, 590, f'-{I_DROP:,.0f} jobs (-{I_PCT:.0f}%)', CORAL, pop(t, L[2] + 0.3), 24)
        source(c, t, 'BLS information-sector employment (USINFO) via FRED') if t < L[2] else None
        return
    specks(c, t, 77)
    c.icon('bot', 380, 320, 170, SKY, a=fade(t, L[3]))
    c.icon('server', 640, 320, 140, GOLD, a=fade(t, L[3] + 0.6))
    c.icon('users', 900, 320, 170, MINT, a=fade(t, L[3] + 1.2))
    if t > L[4]:
        chip(c, 640, 520, 'Microsoft: "not replacing workers with AI agents"', SKY, pop(t, L[4] + 0.3), 20)


def s_past(c, x):
    t, L = x.t, x.L
    specks(c, t, 80)
    steps = (('rocket', '2021-22\nhiring frenzy'), ('door-open', 'record\nquitting'), ('percent', f'{N_HIKES} Fed\nrate hikes'),
             ('snowflake', 'hiring\ncools'))
    icon_row(c, t, steps, 0.3, x.E[-1] - 0.5, y=300)


def s_who(c, x):
    t, L = x.t, x.L
    specks(c, t, 81)
    if t < L[2]:
        c.text(640, 90, 'Jobs added, last 12 months vs 2019 pace', 32, WHITE, 900, a=fade(t, 0))
        compare_bars(c, t, (('per month, 2019', P19 / 1000, GOLD), ('per month, now', P_CHG / 12000, CORAL)),
                     L[1] - 0.3, 2.0, 200, lambda v: f'{v:.0f}K', box=(300, 170, 980, 520))
        source(c, t, 'BLS payrolls (PAYEMS) via FRED')
        return
    c.text(640, 90, 'Change in jobs over the last 12 months', 32, WHITE, 900, a=fade(t, L[2]))
    items = (('All jobs', P_CHG / 1000, GOLD), ('Health care', H_CHG / 1000, MINT), ('Manufacturing', M_CHG / 1000, SKY),
             ('Information', I_CHG / 1000, CORAL))
    x0, x1, y0, y1 = 200, 1080, 170, 520
    zero = y0 + (y1 - y0) * 600 / 800
    c.line([(x0, zero), (x1, zero)], (255, 255, 255, 90), 2)
    for i, (lab, v, col) in enumerate(items):
        at = L[2] + 0.3 + i * 0.9
        g = ease(seg(t, at, at + 1))
        if t < at:
            continue
        bx = x0 + i * (x1 - x0) / 4 + 30
        h = (y1 - y0) * v / 800 * g
        c.rrect(bx, min(zero, zero - h), bx + 160, max(zero, zero - h), 10, col)
        c.text(bx + 80, (zero - h - 26) if v > 0 else (zero - h + 26), f'{v * g:+,.0f}K', 26, col, 900)
        c.text(bx + 80, y1 + 36, lab, 20, WHITE, 800)
    source(c, t, 'BLS payrolls (PAYEMS, CES6562000001, MANEMP, USINFO) via FRED')


def s_watch(c, x):
    t, L = x.t, x.L
    specks(c, t, 82)
    c.text(640, 80, 'Two numbers to watch', 36, WHITE, 900, a=fade(t, 0))
    if t > L[1]:
        dial(c, 400, 380, 150, round(C_NOW / 1000), 400, f'weekly claims: {C_NOW / 1000:.0f}K', a=fade(t, L[1]),
             color=MINT)
        chip(c, 400, 520, 'warning zone: ~300K+', CORAL, pop(t, L[1] + 2), 18)
    if t > L[2]:
        dial(c, 880, 380, 150, max(S_NOW, 0.01), 1.0, f'Sahm rule: {S_NOW:.2f}', a=fade(t, L[2]), color=MINT)
        chip(c, 880, 520, 'recession signal: 0.50', CORAL, pop(t, L[3]), 18)
    source(c, t, 'Dept. of Labor (ICSA); Sahm rule recession indicator (SAHMREALTIME) via FRED')


def s_you(c, x):
    t, L = x.t, x.L
    specks(c, t, 78)
    c.text(640, 80, 'What the data suggests for you', 36, WHITE, 900, a=fade(t, 0))
    items = (('piggy-bank', '3-6 months\nemergency fund'), ('handshake', 'Line up the\nnext job first'),
             ('graduation-cap', 'Learn AI tools\nin your field'), ('scale', 'Buyout? Do\nthe math first'))
    icon_row(c, t, items, L[1] - 0.3, x.E[-1] - L[1], y=300)
    if t > x.E[-1] - 1:
        chip(c, 640, 590, 'Education only - not financial advice', MUTED, pop(t, x.E[-1] - 0.7), 18)


def s_outro(c, x):
    t, L = x.t, x.L
    specks(c, t, 79, 50)
    penny(c, 260, 380, 76, t, 'happy', look=(1, 0), talk=x.talk(), wave=t > x.E[-1])
    if t < L[2]:
        office(c, 820, 560, 1.0, a=fade(t, 0.2), lit=0.4)
    if t > L[2]:
        k = ease_out(seg(t, L[2], L[2] + 0.6))
        c.text(400, 560, 'COIN THEORY', 30, GOLD, 900, anchor='lm', a=k)
        c.text(400, 595, 'money, explained with real data', 18, MUTED, 600, anchor='lm', a=k)
    if t > x.E[-1]:
        c.rrect(560, 150, 1200, 510, 20, (255, 255, 255, 10), (255, 255, 255, 40), 2, a=fade(t, x.E[-1], 0.8))


SCENES = [
    dict(draw=s_hook, chapter='Intro: 60,000 buyouts', cam=(1.0, 1.05), lines=[
        "This week, Microsoft offered buyouts to about 60,000 employees. That's roughly a quarter of its entire "
        "workforce.",
        "Headlines are full of layoffs and artificial intelligence. So, is your job in danger?",
        "Let's skip the panic and look at the government's own numbers, because they tell a very different story "
        "than the headlines.",
        "And stick around, because one industry is still hiring like crazy, and it's probably not the one you'd "
        "guess.",
    ], sfx=lambda L: [(L[0] + 0.8, 'whoosh'), (L[0] + 3.5, 'pop'), (L[2] + 0.3, 'ding')]),
    dict(draw=s_title, lines=[], min=3.2, captions=False, trans='fadeblack', sfx=lambda L: [(0.2, 'ding')]),
    dict(draw=s_buyout, chapter='Buyout vs layoff', trans='fadeblack', lines=[
        "First, a buyout is not a layoff. In a layoff, the company decides you're leaving.",
        "A buyout is an offer. The company pays you to leave voluntarily, usually with severance based on how long "
        "you've worked there. Long-time employees usually get the biggest checks.",
        "Microsoft's offer goes to staff at the vice president level and below in the US, Canada, India, and the "
        "UK, and they have until early December to decide.",
        "It's actually Microsoft's second buyout this year. According to reports, an earlier offer went to "
        "employees near retirement age, and more than 30% of the roughly 8,750 people who were eligible took it.",
        "Microsoft is spending heavily on artificial intelligence infrastructure, and says it wants to control "
        "headcount while avoiding layoffs.",
        "And here's a surprising detail. At other big tech companies with similar programs, only about 3 to 5% of "
        "people said yes. The downside for companies is that the people most likely to take the money are often "
        "the ones who can easily find another job.",
    ], sfx=lambda L: [(0.3, 'pop'), (L[1], 'pop'), (L[5] + 2, 'ding')]),
    dict(draw=s_layoffs, chapter='Are layoffs really rising?', cam=(1.0, 1.04), lines=[
        "So, are layoffs really surging across America? This is the official count, from a monthly survey of about "
        "21,000 employers run by the Bureau of Labor Statistics.",
        f"In August, US employers laid off or discharged about {mil(L_NOW)} workers.",
        f"That sounds like a lot, until you compare it. In 2019, before the pandemic, the average was about "
        f"{mil(L19)} a month. As a share of all jobs, it's about {RATE_NOW:.0f}% a month now, compared with "
        f"{RATE19:.1f}% in 2019.",
        f"And remember March 2020? Almost {L_MAX / 1e3:.0f} million people were laid off in a single month. Today "
        "is nowhere near that.",
    ], sfx=lambda L: [(L[1] + 2, 'pop'), (L[2] + 1, 'pop'), (L[2] + 3.3, 'ding')]),
    dict(draw=s_claims, chapter='The weekly warning sign', lines=[
        "Economists also watch a faster signal: new claims for unemployment benefits, reported every single week.",
        f"Last week, about {round(C_NOW, -3):,.0f} people filed a new claim. In 2019, the weekly average was about "
        f"{round(C19, -3):,.0f}.",
        "If mass layoffs were spreading across the country, this number would be shooting up. So far, it isn't.",
        f"The unemployment rate says the same thing. It's {U_NOW}%, a little higher than the {U19:.1f}% average of "
        "2019, but still low by historical standards.",
    ], sfx=lambda L: [(L[1] + 0.3, 'pop'), (L[2] + 0.3, 'ding')]),
    dict(draw=s_past, chapter='How we got here', lines=[
        "To understand today, rewind to 2021 and 2022. After the pandemic, companies couldn't hire fast enough.",
        "Job openings hit record highs, and a record number of people quit for better pay. Some called it the "
        "great resignation.",
        f"Then the Federal Reserve raised interest rates {N_HIKES} times to fight inflation. Borrowing got "
        "expensive, companies slowed down, and hiring cooled off.",
        "That's exactly what higher rates are designed to do, and it's a big reason the job market feels so "
        "different today.",
    ]),
    dict(draw=s_hiring, chapter='The real problem: hiring', cam=(1.0, 1.04), lines=[
        "So if layoffs are low, why does the job market feel so scary? Because the big change isn't firing. It's "
        "hiring.",
        f"In March 2022, there were about {O_PEAK / 1000:.1f} million open jobs in America. Now there are about "
        f"{O_NOW / 1000:.1f} million.",
        f"Back then, there were {R_PEAK:.0f} open jobs for every unemployed person. Now there's about {R_NOW:.0f}.",
        f"And companies are hiring slowly. In August, only {H_NOW:.1f}% of workers were new hires, compared with "
        f"{H19:.1f}% in 2019.",
        "Economists call this a low-hire, low-fire job market. If you have a job, it's fairly safe. But if you lose "
        "one, finding the next one takes longer.",
        f"The average unemployed person has now been looking for about {W_NOW:.0f} weeks, compared with about "
        f"{W19:.0f} weeks in 2019.",
    ], sfx=lambda L: [(L[1] + 2, 'pop'), (L[1] + 4, 'down'), (L[2] + 0.3, 'ding'), (L[5] + 0.3, 'pop')]),
    dict(draw=s_quits, chapter='The great stay', lines=[
        f"You can see the nervousness in another number: how many people quit. In April 2022, a record "
        f"{Q_PEAK / 1000:.1f} million Americans quit their jobs in a single month.",
        f"Now it's about {Q_NOW / 1000:.1f} million. People aren't leaving, because they're not sure they'll find "
        "something better.",
        "Some people call it the great stay. Fewer people quitting also means fewer openings for everyone else.",
    ], sfx=lambda L: [(L[0] + 2, 'pop'), (L[2] + 0.3, 'ding')]),
    dict(draw=s_tech, chapter='Tech jobs and AI', cam=(1.0, 1.04), lines=[
        "Now, the tech industry. The government's information sector, which includes software publishers, "
        "telecom, and media, shows the pressure clearly.",
        f"It peaked at about {I_PEAK / 1000:.2f} million jobs in November 2022. Today it's about "
        f"{I_NOW / 1000:.2f} million.",
        f"That's about {round(I_DROP, -3):,.0f} fewer jobs, or roughly {I_PCT:.0f}%.",
        "Many tech companies say they hired too fast during the pandemic, and now they're shifting money toward "
        "artificial intelligence, like the giant data centers Microsoft is building.",
        "So is AI replacing these workers? Microsoft says it is not replacing them with AI agents. But the "
        "pressure to cut costs while spending billions on AI is very real.",
    ], sfx=lambda L: [(L[1] + 1, 'pop'), (L[1] + 3, 'down'), (L[2] + 0.3, 'pop')]),
    dict(draw=s_who, chapter='Who is still hiring?', lines=[
        "So who is still hiring? First, the big picture.",
        f"Over the past 12 months, the US economy added about {round(P_CHG, -3):,.0f} jobs in total. That's about "
        f"{round(P_CHG / 12, -3):,.0f} a month. In 2019, it was about {round(P19, -3):,.0f} a month.",
        f"Now the surprise. Health care alone added about {round(H_CHG, -3):,.0f} jobs. That's more than the entire "
        "economy added overall, which means many other industries actually shrank.",
        f"The information sector lost about {round(-I_CHG, -3):,.0f} jobs over the same period, while manufacturing "
        "barely moved. Hospitals, clinics, and home health care are where the hiring is.",
    ], sfx=lambda L: [(L[1], 'pop'), (L[2] + 1.2, 'ding')]),
    dict(draw=s_watch, chapter='Two numbers to watch', lines=[
        "So how will you know if things are really getting worse? Watch two numbers.",
        f"The first is weekly jobless claims. It's about {round(C_NOW / 1000):.0f} thousand now. Many economists treat "
        "a steady climb toward 300 thousand as a warning sign.",
        f"The second is the Sahm rule, a recession signal created by economist Claudia Sahm. It compares the "
        f"recent unemployment rate with its low over the past year. Right now, it reads {S_NOW:.2f}.",
        "When it reaches 0.5, a recession has usually already started. Today, it's nowhere close.",
    ], sfx=lambda L: [(L[1] + 2, 'pop'), (L[3], 'ding')]),
    dict(draw=s_you, chapter='What this means for you', lines=[
        "So what does this mean for you? Here's what the data suggests.",
        "One: in a low-hire market, an emergency fund matters more, because a job search can take longer. Many "
        "experts suggest three to six months of expenses.",
        "Two: if you're thinking about quitting, line up the next job first.",
        "Three: keep your skills current. Learning to use AI tools in your own field can make you more valuable, "
        "not less.",
        "And four: if you're ever offered a buyout, compare the severance with how long a job search might take in "
        "your field, and talk to a professional before you decide.",
        "And five: if you're ever laid off, file for unemployment benefits right away. Rules differ by state, and "
        "taking a voluntary buyout can affect whether you qualify, so check with your state first.",
    ]),
    dict(draw=s_outro, chapter='Recap', tail=12, cam=(1.0, 1.02), lines=[
        "So, layoffs are not surging. The real story is a job market where hiring has slowed way down, and tech is "
        "feeling it the most.",
        "Microsoft's buyout is a sign of the times: big companies are pouring money into AI and trimming almost "
        "everywhere else.",
        "Next time: how banks create money out of thin air. Subscribe to Coin Theory so you don't miss it.",
    ], sfx=lambda L: [(L[2], 'pop')]),
]

SHORTS = {
    'ep05_short_layoffs': [SCENES[3], end_card("So what's really happening to jobs? Full story on Coin Theory.")],
    'ep05_short_hiring': [SCENES[6], end_card("Microsoft just offered 60,000 buyouts. Full story on Coin Theory.")],
}


def check_numbers():
    script = ' '.join(l for sc in SCENES for l in sc['lines'])
    assert L_AT.strftime('%Y-%m') == '2026-08' and 'In August' in script
    assert L_NOW < L19 and RATE_NOW < RATE19, (L_NOW, L19, RATE_NOW, RATE19)
    assert L_MAX_AT.strftime('%Y-%m') == '2020-03' and 12.5e3 < L_MAX < 13.5e3 and 'Almost 13 million' in script
    assert C_NOW < C19 and C_AT.year == 2026, (C_NOW, C19)
    assert O_PEAK_AT.strftime('%Y-%m') == '2022-03' and 'In March 2022' in script
    assert round(R_PEAK) == 2 and round(R_NOW) == 1, (R_PEAK, R_NOW)
    assert H_NOW < H19 and HIRE.index[-1].strftime('%Y-%m') == '2026-08'
    assert W_NOW > W19 and WEEKS.index[-1].year == 2026
    assert Q_PEAK_AT.strftime('%Y-%m') == '2022-04' and Q_PEAK == QUIT.max() and 'a record' in script
    assert I_PEAK_AT.strftime('%Y-%m') == '2022-11' and I_NOW < I_PEAK
    assert P_CHG < 12 * P19 and H_CHG > P_CHG and I_CHG < 0 and abs(M_CHG) < 100e3, (P_CHG, P19, H_CHG, I_CHG, M_CHG)
    assert U_NOW > U19 and U_NOW < UNRATE.mean() and 'low by historical standards' in script
    assert SAHM.index[-1].strftime('%Y-%m') == '2026-09' and S_NOW < 0.5 and N_HIKES == 11
    assert C_NOW < 300000
    assert 'about 60,000' in script and 'roughly a quarter' in script and '3 to 5%' in script
    print('numbers check: OK')
    print(f'  layoffs {L_NOW} vs 2019 {L19:.0f}; rate {RATE_NOW:.2f}% vs {RATE19:.2f}%; max {L_MAX} {L_MAX_AT.date()}; '
          f'claims {C_NOW:.0f} vs {C19:.0f}; openings {O_PEAK}->{O_NOW}; ratio {R_PEAK:.2f}->{R_NOW:.2f}; hires '
          f'{H_NOW} vs {H19:.2f}; weeks {W_NOW} vs {W19:.1f}; quits {Q_PEAK}->{Q_NOW}; info {I_PEAK}->{I_NOW} '
          f'(-{I_DROP:.0f}, {I_PCT:.1f}%)')


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    check_numbers()
    if '--stills' in sys.argv:
        os.makedirs(BUILD, exist_ok=True)
        for i, sc in enumerate(SCENES):
            n = max(1, len(sc['lines']))
            still(sc, 0.5 + 4 * n + 1, os.path.join(BUILD, f'still_{i:02d}.png'))
        sys.exit()
    if '--shorts-only' not in sys.argv:
        total, chapters = build(SCENES, os.path.join(OUT, 'ep05_jobs.mp4'), BUILD,
                                srt_path=os.path.join(OUT, 'ep05_jobs.en.srt'))
        with open(os.path.join(OUT, 'ep05_chapters.txt'), 'w') as f:
            for at, name in chapters:
                f.write(f'{fmt_time(at)} {name}\n')
        print(open(os.path.join(OUT, 'ep05_chapters.txt')).read())
    if '--no-short' not in sys.argv:
        for name, scenes in SHORTS.items():
            build(scenes, os.path.join(OUT, f'{name}.mp4'), os.path.join(BUILD, name), layout='short')
