"""Short from story #1 (Grandpa's $1,000): the cookie-jar money vs the planted money. Numbers from
channel/stories/s01_numbers.py (FRED CPI-U Nov 1996 -> latest; Yahoo ^SP500TR total return, Nov 25 1996 -> latest)."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), 'stories'))
import engine as E
from s01_numbers import N
assert N['jar_buys'] == 470 and N['now'] == 16368, N

LINES = [
    "!One thousand dollars, hidden in a cookie jar since 1996.",
    "Thirty years later, every bill is still there.",
    f"Yet at today's prices, that stack only buys what ${N['jar_buys']} used to.",
    "A sneaky mouse called inflation ate more than half of it, and never left a single bite mark.",
    "His sister planted the same thousand dollars in the stock market instead.",
    f"!Today, hers is worth ${N['now']:,}.",
    "Which grandkid are you? The whole story is on Coin Theory now.",
]
GAP = 0.32
os.makedirs(os.path.join(HERE, 'vo'), exist_ok=True)
t, out, voice = 0.5, [], []
for i, ln in enumerate(LINES):
    drama = ln.startswith('!')
    toks = E.parse_line(ln.lstrip('!'))
    p = os.path.join(HERE, 'vo', f'{i}.npy')
    a = np.load(p) if os.path.exists(p) else E.speak(toks, exag=0.7 if drama else None)
    np.save(p, a)
    words, cov = E.align(toks, E.word_times(a), len(a) / E.SR)
    out.append(dict(text=' '.join(d for d, _ in toks), start=t, dur=len(a) / E.SR,
                    words=[dict(w=w['w'], s=t + w['s'], e=t + w['e']) for w in words]))
    voice.append((t, a)); t += len(a) / E.SR + GAP
total = t + 1.2
v = np.zeros(int(total * E.SR), np.float32)
for st, a in voice:
    E.place(v, a, st)
np.save(os.path.join(HERE, 'voice.npy'), v)
json.dump(dict(total=total, lines=out), open(os.path.join(HERE, 'timeline.json'), 'w'), indent=1)
print('total', round(total, 2), [round(l['start'], 2) for l in out])
