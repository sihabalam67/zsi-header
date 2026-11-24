"""Voice + timings for the character demo Short (numbers: BLS average prices via ep13_groceries data)."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import engine as E

LINES = [
    "!This bag of coffee cost $4.17 in 2020.",
    "Today? $9.25.",
    "That's 122 percent more. Way more than beef, eggs, or bread.",
    "Beef is up 74 percent. Eggs, 59. Bread, 38.",
    "And your paycheck? Up 34 percent.",
    "So your morning coffee is running away from your pay.",
    "Follow Coin Theory for one money fact a day.",
]
GAP = 0.35
os.makedirs(os.path.join(HERE, 'vo'), exist_ok=True)
t, out, voice = 0.6, [], []
for i, ln in enumerate(LINES):
    drama = ln.startswith('!')
    toks = E.parse_line(ln.lstrip('!'))
    p = os.path.join(HERE, 'vo', f'{i}.npy')
    if os.path.exists(p):
        a = np.load(p)
    else:
        a = E.speak(toks, exag=0.7 if drama else None); np.save(p, a)
    words, cov = E.align(toks, E.word_times(a), len(a) / E.SR)
    out.append(dict(text=' '.join(d for d, _ in toks), start=t, dur=len(a) / E.SR,
                    words=[dict(w=w['w'], s=t + w['s'], e=t + w['e']) for w in words]))
    voice.append((t, a))
    t += len(a) / E.SR + GAP
total = t + 1.4
v = np.zeros(int(total * E.SR), np.float32)
for st, a in voice:
    E.place(v, a, st)
np.save(os.path.join(HERE, 'voice.npy'), v)
json.dump(dict(total=total, lines=out), open(os.path.join(HERE, 'timeline.json'), 'w'), indent=1)
print('total', round(total, 2), [round(l['start'], 2) for l in out])
