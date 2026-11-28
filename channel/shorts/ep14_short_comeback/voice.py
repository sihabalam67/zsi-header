"""Daily Short Nov 28 (from ep14): the comeback math. A loss of L% needs L/(100-L) to get back. Data: channel/data/ep14.json
(Yahoo Finance closes: NVDA 239.24 on 2026-10-06 -> 149.30 on 2026-11-25 = -37.6%, needs +60.2% to return)."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
CH = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, CH)
import engine as E
d = json.load(open(os.path.join(CH, 'data', 'ep14.json')))
c = {k: dict(v) for k, v in d['closes'].items()}
hi, lo = c['nvda']['2026-10-06'], c['nvda']['2026-11-25']
need = lambda L: L / (100 - L) * 100
assert (hi, lo) == (239.24, 149.30) and round((lo / hi - 1) * 100, 1) == -37.6 and round((hi / lo - 1) * 100, 1) == 60.2
assert round(need(10)) == 11 and round(need(50)) == 100 and round(need(80)) == 400
LINES = [
    "!Lose 50%, and you need 100% just to get even.",
    "Start with $100. Drop by half, and you're holding $50.",
    "To climb back to $100, that $50 has to double.",
    "That's why Nvidia's 37.6% fall is so hard to undo.",
    "From $149.30, it has to rise 60.2% to reach its October high of $239.24.",
    "The math is lopsided. Lose 10%, you need 11%. Lose 80%, you need 400%.",
    "So which hurts more: the drop, or the wait back? Tell me below.",
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
