"""Daily Short Nov 26 (from ep14): you own Nvidia through an S&P 500 fund. Data: channel/data/ep14.json (SSGA SPY
holdings as of 24-Nov-2026: NVDA 6.05%, top 10 holdings 36.96%; Yahoo Finance closes: NVDA 239.24 on 2026-10-06 ->
149.30 on 2026-11-25 = -37.6%; S&P 500 7,818.93 -> 7,182.78 = -8.1%)."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
CH = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, CH)
import engine as E
d = json.load(open(os.path.join(CH, 'data', 'ep14.json')))
w = {h['ticker']: h['weight'] for h in d['spy_top10']}
c = {k: dict(v) for k, v in d['closes'].items()}
nv = (c['nvda']['2026-11-25'] / c['nvda']['2026-10-06'] - 1) * 100
sp = (c['sp500']['2026-11-25'] / c['sp500']['2026-10-06'] - 1) * 100
top10 = sum(h['weight'] for h in d['spy_top10'])
assert round(w['NVDA'], 2) == 6.05 and round(nv, 1) == -37.6 and round(sp, 1) == -8.1 and round(top10) == 37
LINES = [
    "!You own Nvidia. Even if you never bought a single share.",
    "Got a {401(k)|four-oh-one-k} in an {S&P|S and P} 500 fund? Out of every $100, about $6 is Nvidia.",
    "And $37 sits in just its ten biggest holdings.",
    "Since its October peak, Nvidia has fallen 37.6%.",
    "That one stock took roughly two dollars out of every hundred in the fund.",
    "The whole {S&P|S and P} 500 is down about 8%.",
    "Did you know you owned it? Yes or no. Full breakdown on Coin Theory.",
]
GAP = 0.3
os.makedirs(os.path.join(HERE, 'vo'), exist_ok=True)
t, out, voice = 0.5, [], []
for i, ln in enumerate(LINES):
    drama = ln.startswith('!')
    toks = E.parse_line(ln.lstrip('!'))
    p = os.path.join(HERE, 'vo', f'{i}.npy')
    a = np.load(p) if os.path.exists(p) else E.speak(toks, exag=0.7 if drama else None)
    np.save(p, a)
    words, cov = E.align(toks, E.word_times(a), len(a) / E.SR)
    out.append(dict(text=' '.join(dd for dd, _ in toks), start=t, dur=len(a) / E.SR,
                    words=[dict(w=x['w'], s=t + x['s'], e=t + x['e']) for x in words]))
    voice.append((t, a)); t += len(a) / E.SR + GAP
total = t + 1.2
v = np.zeros(int(total * E.SR), np.float32)
for st, a in voice:
    E.place(v, a, st)
np.save(os.path.join(HERE, 'voice.npy'), v)
hop = E.SR // 30
env = np.array([np.sqrt(np.mean(v[i * hop:(i + 1) * hop] ** 2)) if i * hop < len(v) else 0 for i in range(int(total * 30) + 1)])
json.dump(dict(total=total, lines=out, mouth=[round(float(x), 3) for x in np.minimum(1, env / env.max() * 1.8)]),
          open(os.path.join(HERE, 'timeline.json'), 'w'), indent=1)
print('total', round(total, 2), [round(l['start'], 2) for l in out])
