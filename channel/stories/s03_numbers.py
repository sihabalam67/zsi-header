"""Numbers for story #3 "The Poorest Man in Town Left $2 Million. How?" Hypothetical saver, real market data.
Walter: $300/month into an S&P 500 index fund with dividends reinvested (Yahoo ^SP500TR, before fees/taxes) from
Jan 1988 to Nov 2026, plus $5,000 at each of three crash lows (Oct 9 2002, Mar 9 2009, Mar 23 2020).
Lily's gift: $1,000 on Jun 1 1998. Black Monday from ^GSPC daily closes. Run: python3 channel/stories/s03_numbers.py"""
import os
import pandas as pd

D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
tr = pd.read_csv(os.path.join(D, 'SP500TR_daily.csv'), parse_dates=['date']).set_index('date')['close']
gs = pd.read_csv(os.path.join(D, 'GSPC_daily.csv'), parse_dates=['date']).set_index('date')['close']
NOW = tr.index[-1]
CRASH = {'2002-10-09': 5000, '2009-03-09': 5000, '2020-03-23': 5000}
first = lambda d: tr.loc[d:].index[0]  # noqa: E731

u, months, snaps = 0.0, 0, {}
for m in pd.date_range('1988-01-01', NOW, freq='MS'):
    d = first(m)
    u += 300 / tr[d]
    months += 1
    for b, a in CRASH.items():
        if first(b).year == d.year and first(b).month == d.month:
            u += a / tr[first(b)]
    if m.month == 11 and m.year in (1996, 2006, 2016):
        snaps[m.year] = round(u * tr[d])
N = dict(monthly=300, months=months, paid_monthly=300 * months, paid=300 * months + 15000, now=round(u * tr[NOW]),
         v1996=snaps[1996], v2006=snaps[2006], v2016=snaps[2016])
N['last10_share'] = round(100 * (N['now'] - N['v2016']) / N['now'])
for k, d in zip(('c2002', 'c2009', 'c2020'), CRASH):
    N[k] = round(5000 * tr[NOW] / tr[first(d)])
N['gift'] = round(1000 * tr[NOW] / tr[first('1998-06-01')])
N['black_monday'] = round(100 * (gs['1987-10-19'] / gs['1987-10-16'] - 1), 1)

if __name__ == '__main__':
    print(NOW.date(), N)
    assert N['now'] == 2032554 and N['v2016'] == 479188 and N['gift'] == 11063 and N['black_monday'] == -20.5, N
    assert N['last10_share'] == 76 and N['months'] == 467, N
