#!/usr/bin/env python3
"""Download FRED series into channel/data/<ID>.csv (free, no API key).

    python3 channel/fetch_data.py JTSLDL UNRATE CPIAUCSL ...

Re-download before each new episode so the numbers are current. Series used by an already-published episode can
change in later releases, so keep its guards passing or save a dated copy (e.g. MORTGAGE30US_wk2.csv).
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
for sid in sys.argv[1:]:
    path = os.path.join(HERE, 'data', f'{sid}.csv')
    r = subprocess.run(['curl', '-sS', '-f', '-m', '60', '-o', path,
                        f'https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}'], capture_output=True, text=True)
    if r.returncode:
        print(f'{sid}: FAILED {r.stderr.strip()[:120]}')
        continue
    last = open(path).read().strip().splitlines()[-1]
    print(f'{sid}: latest {last}')
