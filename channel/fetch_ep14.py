#!/usr/bin/env python3
"""Data for ep14 (Nvidia's crash and your 401(k)): Yahoo Finance daily closes for NVDA, ^GSPC, ^NDX, SPY and the
SPDR S&P 500 ETF (SPY) daily holdings file from State Street (ssga.com). Saves channel/data/ep14.json."""
import datetime as dt
import io
import json
import os
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'data', 'ep14.json')
UA = {'User-Agent': 'Mozilla/5.0'}


def series(sym):
    req = urllib.request.Request(f'https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range=1y&interval=1d', headers=UA)
    r = json.load(urllib.request.urlopen(req, timeout=40))['chart']['result'][0]
    return [(str(dt.datetime.fromtimestamp(t, dt.UTC).date()), round(c, 2)) for t, c in
            zip(r['timestamp'], r['indicators']['quote'][0]['close']) if c]


out = {'fetched': dt.datetime.now(dt.UTC).isoformat(timespec='seconds'), 'closes': {}}
for name, sym in (('nvda', 'NVDA'), ('sp500', '%5EGSPC'), ('ndx', '%5ENDX'), ('spy', 'SPY')):
    out['closes'][name] = series(sym)
req = urllib.request.Request('https://www.ssga.com/us/en/intermediary/library-content/products/fund-data/etfs/us/holdings-daily-us-en-spy.xlsx', headers=UA)
raw = urllib.request.urlopen(req, timeout=60).read()
open(os.path.join(HERE, 'data', 'spy_holdings.xlsx'), 'wb').write(raw)
import openpyxl
ws = openpyxl.load_workbook(io.BytesIO(raw), read_only=True).active
rows = [[c for c in r] for r in ws.iter_rows(values_only=True)]
hdr = next(i for i, r in enumerate(rows) if r and 'Weight' in [str(x) for x in r])
cols = [str(x) for x in rows[hdr]]
asof = [r for r in rows[:hdr] if r and any('As of' in str(x) for x in r if x)]
hold = []
for r in rows[hdr + 1:]:
    if not r or r[cols.index('Weight')] in (None, ''):
        continue
    hold.append(dict(name=r[cols.index('Name')], ticker=r[cols.index('Ticker')], weight=float(r[cols.index('Weight')])))
hold.sort(key=lambda h: -h['weight'])
out['spy_asof'] = ' '.join(str(x) for x in asof[0] if x) if asof else ''
out['spy_top10'] = hold[:10]
out['spy_count'] = len(hold)
json.dump(out, open(OUT, 'w'), indent=1)
c = {k: dict(v) for k, v in out['closes'].items()}
print('asof', out['spy_asof'], 'holdings', len(hold))
for h in hold[:10]: print(f"  {h['ticker']:6s} {h['weight']:.2f}  {h['name']}")
print('top10 sum', round(sum(h['weight'] for h in hold[:10]), 2))
for k in c:
    v = out['closes'][k]; mx = max(v, key=lambda x: x[1]); print(k, 'last', v[-1], 'max', mx, 'dd', round((v[-1][1] / mx[1] - 1) * 100, 1))
