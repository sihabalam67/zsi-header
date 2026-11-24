"""Numbers for story #2 "Same Salary. 10 Years Later, One Is Broke." Hypothetical choices, real market data and rates.
Data: data/SP500TR_daily.csv (S&P 500 total return, Yahoo ^SP500TR), FRED TERMCBCCINTNS (card APR, accounts assessed
interest), FRED TERMCBAUTO48NS (48-month new-car loan rate). Run: python3 channel/stories/s02_numbers.py"""
import os
import pandas as pd

D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
tr = pd.read_csv(os.path.join(D, 'SP500TR_daily.csv'), parse_dates=['date']).set_index('date')['close']
rd = lambda s: pd.read_csv(os.path.join(D, s + '.csv'), parse_dates=['observation_date']).set_index('observation_date').iloc[:, 0].dropna()  # noqa: E731
cc, auto = rd('TERMCBCCINTNS'), rd('TERMCBAUTO48NS')
NOW = tr.index[-1]
SKIP = (pd.Timestamp('2020-04-01'), pd.Timestamp('2020-08-01'))  # both laid off: no contributions Apr-Aug 2020


def dca(amount, start='2016-02-01', end=None, at=None):
    u = p = 0
    for m in pd.date_range(start, end or NOW, freq='MS'):
        if SKIP[0] <= m <= SKIP[1]:
            continue
        d = tr.loc[m:].index[0]
        u += amount / tr[d]
        p += amount
    return p, round(u * tr[at or NOW])


N = dict(salary=60000, own=300, match=150)  # Sam: 6% of $60k = $300/mo, employer adds 50% of it = $150/mo
N['paid'], N['now'] = dca(450)
N['own_paid'] = N['paid'] * 300 // 450
N['match_paid'], N['match_now'] = dca(150)
N['paid_2020'], N['peak_2020'] = dca(450, end='2020-02-01', at=pd.Timestamp('2020-02-19'))
_, N['low_2020'] = dca(450, end='2020-03-01', at=pd.Timestamp('2020-03-23'))
r = auto['2017'].mean() / 1200
N['car_rate'] = round(auto['2017'].mean(), 1)
N['car_pay'] = round(40000 * r / (1 - (1 + r) ** -72))
N['car_interest'] = round(N['car_pay'] * 72 - 40000)
apr = cc.iloc[-1] / 100
N['card_apr'] = round(cc.iloc[-1], 2)
b, m, tot = 6000.0, 0, 0.0
while b > .01:
    i = b * apr / 12
    pmt = min(max(25, i + b * .01), b + i)
    b, tot, m = b + i - pmt, tot + pmt, m + 1
N['card_years'], N['card_total'], N['card_interest'] = round(m / 12, 1), round(tot), round(tot - 6000)
N['card_first_min'] = round(6000 * apr / 12 + 60)

if __name__ == '__main__':
    print(NOW.date(), N)
    assert N['now'] == 126766 and N['match_now'] == 42255 and N['car_pay'] == 637 and N['card_interest'] == 10105, N
