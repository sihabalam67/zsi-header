#!/usr/bin/env python3
"""Fetch the day-after-midterm market move for sx11 into channel/data/sx11_market.json.

Dow (^DJI) and S&P 500 (^GSPC) daily closes from Yahoo Finance: Nov 3 2026 (election day) vs Nov 4 2026, plus the last
earlier day in the past year with a bigger % gain (for "best day since ..."). Run after the 4 PM ET close.
"""
import datetime as dt
import json
import os
import urllib.request

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'sx11_market.json')


def series(sym):
    req = urllib.request.Request(f'https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range=2y&interval=1d',
                                 headers={'User-Agent': 'Mozilla/5.0'})
    r = json.load(urllib.request.urlopen(req, timeout=40))['chart']['result'][0]
    rows = [(dt.datetime.fromtimestamp(t, dt.UTC).date(), c) for t, c in
            zip(r['timestamp'], r['indicators']['quote'][0]['close']) if c]
    return rows, r['meta']


out = {}
for name, sym in (('dow', '%5EDJI'), ('sp500', '%5EGSPC')):
    rows, meta = series(sym)
    d = {x: c for x, c in rows}
    a, b = d[dt.date(2026, 11, 3)], d[dt.date(2026, 11, 4)]
    pct = (b / a - 1) * 100
    since = None
    for i in range(len(rows) - 1, 0, -1):
        day, c = rows[i]
        if day >= dt.date(2026, 11, 4):
            continue
        if (c / rows[i - 1][1] - 1) * 100 >= pct:
            since = str(day)
            break
    out[name] = dict(close_nov3=round(a, 2), close_nov4=round(b, 2), points=round(b - a, 2), pct=round(pct, 2),
                     best_since=since, market_state=meta.get('marketState'),
                     fetched=dt.datetime.now(dt.UTC).isoformat(timespec='seconds'))
json.dump(out, open(OUT, 'w'), indent=1)
print(json.dumps(out, indent=1))
