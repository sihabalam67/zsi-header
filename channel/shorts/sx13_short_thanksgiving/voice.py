"""Thanksgiving Short (Nov 25, 2026). Numbers: American Farm Bureau Federation, 41st annual Thanksgiving dinner
survey (news release 'Cost of Thanksgiving Dinner Increases, Remains Below 2022 Record High', fb.org, Nov 2026):
classic dinner for 10 = $58.63 (~$5.86/person), +6% vs 2025, $5.42 below the 2022 record $64.05; 16-lb turkey
$23.68 (+10.1%); cranberries +8.8%, whole milk +8.6%, dinner rolls +7%; veggie tray -3.7%, pie crusts -2.7%,
frozen peas -2%. The 12 items sum to $58.63 (asserted below)."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import engine as E
ITEMS = [('16-lb turkey', 23.68), ('Pumpkin pie mix', 4.24), ('Sweet potatoes', 4.20), ('Gallon of milk', 4.05),
         ('Stuffing mix', 3.91), ('Misc. ingredients', 3.84), ('Dinner rolls', 3.81), ('Pie crusts', 3.28),
         ('Cranberries', 2.48), ('Frozen peas', 1.99), ('Whipping cream', 1.84), ('Veggie tray', 1.31)]
assert round(sum(p for _, p in ITEMS), 2) == 58.63
LINES = [
    "!Thanksgiving dinner for ten people, this year: $58.63.",
    "That's about $5.86 a plate.",
    "The turkey is the big one: $23.68, up ten percent.",
    "Cranberries, milk and dinner rolls went up too.",
    "But the veggie tray, the pie crusts and the peas got a little cheaper.",
    "And the whole feast is still $5.42 below the record from 2022.",
    "Happy Thanksgiving from Coin Theory. Which dish would you never skip?",
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
    out.append(dict(text=' '.join(d for d, _ in toks), start=t, dur=len(a) / E.SR,
                    words=[dict(w=w['w'], s=t + w['s'], e=t + w['e']) for w in words]))
    voice.append((t, a)); t += len(a) / E.SR + GAP
total = t + 1.2
v = np.zeros(int(total * E.SR), np.float32)
for st, a in voice:
    E.place(v, a, st)
np.save(os.path.join(HERE, 'voice.npy'), v)
hop = E.SR // 30
env = np.array([np.sqrt(np.mean(v[i * hop:(i + 1) * hop] ** 2)) if i * hop < len(v) else 0 for i in range(int(total * 30) + 1)])
json.dump(dict(total=total, lines=out, items=ITEMS, mouth=[round(float(x), 3) for x in np.minimum(1, env / env.max() * 1.8)]),
          open(os.path.join(HERE, 'timeline.json'), 'w'), indent=1)
print('total', round(total, 2), [round(l['start'], 2) for l in out])
