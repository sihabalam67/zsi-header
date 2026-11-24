"""Voice + timeline for story #1: per-line narration (cached), word timings, lip-sync envelope -> stories/build/s01/."""
import hashlib
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import engine as E  # noqa: E402
from s01_script import SCENES  # noqa: E402

B = os.path.join(HERE, 'build', 's01')
os.makedirs(os.path.join(B, 'vo'), exist_ok=True)
GAP, SCENE_GAP, FPS = 0.32, 0.9, 30
t, voice, scenes = 1.0, [], []
for si, sc in enumerate(SCENES):
    s_start = t
    lines = []
    for li, raw in enumerate(sc['lines']):
        who, text = (raw.split('|', 1) if '|' in raw[:3] else ('P', raw))
        drama = text.startswith('!')
        text = text.lstrip('!')
        toks = E.parse_line(text)
        key = f'{si:02d}_{li:02d}_' + hashlib.md5(text.encode()).hexdigest()[:10]
        p = os.path.join(B, 'vo', key + '.npy')
        if os.path.exists(p):
            a = np.load(p)
        else:
            a = E.speak(toks, exag=0.7 if drama else None)
            np.save(p, a)
        words, cov = E.align(toks, E.word_times(a), len(a) / E.SR)
        lines.append(dict(who=who, text=' '.join(d for d, _ in toks), start=round(t, 3), dur=round(len(a) / E.SR, 3),
                          words=[dict(w=w['w'], s=round(t + w['s'], 3), e=round(t + w['e'], 3)) for w in words]))
        voice.append((t, a))
        t += len(a) / E.SR + GAP
    t += SCENE_GAP
    scenes.append(dict(id=sc['id'], chapter=sc['chapter'], start=round(s_start - (0.5 if si else 1.0), 3),
                       end=round(t - SCENE_GAP * 0.5, 3), lines=lines))
total = t + 1.5
v = np.zeros(int(total * E.SR), np.float32)
for st, a in voice:
    E.place(v, a, st)
np.save(os.path.join(B, 'voice.npy'), v)
hop = E.SR // FPS
env = np.array([np.sqrt(np.mean(v[i * hop:(i + 1) * hop] ** 2)) if i * hop < len(v) else 0 for i in range(int(total * FPS) + 1)])
env = np.minimum(1, env / env.max() * 1.8)
json.dump(dict(total=round(total, 3), fps=FPS, scenes=scenes, mouth=[round(float(x), 3) for x in env]),
          open(os.path.join(B, 'timeline.json'), 'w'))
with open(os.path.join(B, 'chapters.txt'), 'w') as fh:
    for s in scenes:
        st = max(0, s['start'])
        fh.write(f"{int(st // 60)}:{int(st % 60):02d} {s['chapter']}\n")
print('total', round(total, 1), 's =', round(total / 60, 2), 'min;', [(s['id'], s['start']) for s in scenes])
