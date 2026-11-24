"""Numbers for story #1 (Grandpa's $1,000 test). Data: data/SP500TR_daily.csv (Yahoo ^SP500TR, S&P 500 total return,
dividends reinvested, before fees/taxes) and data/CPIAUCSL.csv (FRED CPI-U). Run: python3 channel/stories/s01_numbers.py"""
import os
import pandas as pd

D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
tr = pd.read_csv(os.path.join(D, 'SP500TR_daily.csv'), parse_dates=['date']).set_index('date')['close']
cpi = pd.read_csv(os.path.join(D, 'CPIAUCSL.csv'), parse_dates=['observation_date']).set_index('observation_date').iloc[:, 0]
START = tr.loc['1996-11-25':].index[0]
NOW = tr.index[-1]


def val(d):
    return 1000 * tr[d] / tr[START]


N = dict(now=round(val(NOW)), d2000_peak=round(val('2000-09-01')), d2002_low=round(val('2002-10-09')),
         d2007_peak=round(val('2007-10-09')), d2009_low=round(val('2009-03-09')), d2020_peak=round(val('2020-02-19')),
         d2020_low=round(val('2020-03-23')), record=round(val(tr[START:].idxmax())),
         jar_buys=round(1000 * cpi['1996-11-01'] / cpi.iloc[-1]), need_today=round(1000 * cpi.iloc[-1] / cpi['1996-11-01']))
units = paid = 0
for m in pd.date_range('2007-10-01', NOW, freq='MS'):
    d = tr.loc[m:].index[0]
    units += 100 / tr[d]
    paid += 100
    if d <= pd.Timestamp('2009-03-09'):
        N['dca_2009_paid'], N['dca_2009_worth'] = paid, round(units * tr['2009-03-09'])
N['dca_paid'], N['dca_now'] = paid, round(units * tr[NOW])

if __name__ == '__main__':
    print(START.date(), NOW.date(), N)
    assert N['now'] == 16368 and N['jar_buys'] == 470 and N['d2009_low'] == 1103 and N['dca_now'] == 100324, N
