"""Story math for sx12 "Same $100, four friends" (an original take on the classic $100-and-hens parable).

Real data: US average price of a dozen grade A large eggs, BLS series APU0000708111 (FRED): Sept 2026 $2.27, 2025
average $4.25 (the bird-flu shortage). US CPI (CPIAUCSL) for the jar's loss to inflation. When bird flu reaches a farm,
the whole flock is culled (USDA APHIS policy).
Story assumptions (said on screen as "story math"): a laying hen costs $25, lays 20 dozen eggs a year, and costs $15 a
year to feed; eggs sell at the BLS average price; Friend 4 borrows $400 at 12% a year. No taxes or labour.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wk2_art import series  # noqa: E402

EGGS = series('APU0000708111')
PRICE = round(float(EGGS.iloc[-1]), 2)          # $ per dozen, latest month
PRICE_DATE = EGGS.index[-1]
PRICE_2025 = round(float(EGGS['2025'].mean()), 2)
CPI = series('CPIAUCSL')
INFL = float(CPI.iloc[-1] / CPI.iloc[-13] - 1)   # last 12 months

HEN, DOZEN_YR, FEED_YR = 25.0, 20.0, 15.0
LOAN, RATE = 400.0, 0.12
PROFIT_YR = DOZEN_YR * PRICE - FEED_YR           # per hen per year
PROFIT_MO = PROFIT_YR / 12


def run(months=12, flu_month=None):
    """Return each friend's net worth after `months`; with flu_month, every hen dies at the end of that month."""
    out = {}
    # 1. The jar: $100 cash, loses value to inflation.
    out['jar'] = dict(cash=100.0, hens=0, debt=0.0, real=100.0 / (1 + INFL) ** (months / 12))
    # 2. Buys 4 hens, keeps the egg money.
    # 3. Buys 4 hens and reinvests every month (whole hens only).
    # 4. Borrows $400 to buy 20 hens, pays interest monthly.
    for key, hens0, debt in (('keeper', 4, 0.0), ('reinvest', 4, 0.0), ('borrow', 20, LOAN)):
        hens, cash, alive = hens0, 0.0, True
        for m in range(1, months + 1):
            if alive:
                cash += hens * PROFIT_MO
            cash -= debt * RATE / 12
            if key == 'reinvest' and alive:
                buy = int(cash // HEN)
                hens += buy
                cash -= buy * HEN
            if flu_month and m == flu_month:
                alive, hens = False, 0
        out[key] = dict(cash=cash, hens=hens, debt=debt, net=hens * HEN + cash - debt)
    out['jar']['net'] = out['jar']['cash']
    return out


GOOD = run()
FLU = run(flu_month=6)

if __name__ == '__main__':
    print(f'eggs ${PRICE}/dozen ({PRICE_DATE:%b %Y}); 2025 avg ${PRICE_2025}; inflation {INFL:.1%}; '
          f'profit/hen/yr ${PROFIT_YR:.2f}')
    for name, r in (('good year', GOOD), ('bird flu in month 6', FLU)):
        print(name)
        for k, v in r.items():
            print(f"  {k:9s} net ${v['net']:8.2f}  hens {v['hens']:3d}  cash ${v['cash']:8.2f}  debt ${v['debt']:.0f}"
                  + (f"  real ${v['real']:.2f}" if 'real' in v else ''))
