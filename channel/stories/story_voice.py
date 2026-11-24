"""Voice + timeline for a story video: Penny (narrator) uses the channel voice (Chatterbox via engine.speak); each
character gets their own Kokoro voice so they sound like different people. Cached per line (stable md5 keys).
    python3 channel/stories/story_voice.py s02"""
import hashlib
import importlib
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import engine as E  # noqa: E402

SID = sys.argv[1]
SCENES = importlib.import_module(f'{SID}_script').SCENES
VOICES = {  # who -> (kokoro voice, speed)
    'J': ('am_puck', 1.08), 'S': ('am_michael', 1.0), 'A': ('af_bella', 1.04), 'H': ('am_santa', 0.95),
    'G': ('bm_george', 0.95), 'M': ('af_nicole', 1.05), 'B': ('am_echo', 1.05), 'R': ('af_sky', 1.04),
}
_k = None


def kokoro(text, voice, speed):
    global _k
    if _k is None:
        from kokoro_onnx import Kokoro
        _k = Kokoro(os.path.join(E.MODELS, 'kokoro-v1.0.onnx'), os.path.join(E.MODELS, 'voices-v1.0.bin'))
    s, sr = _k.create(text, voice=voice, speed=speed, lang='en-us')
    n = int(len(s) * E.SR / sr)
    return np.interp(np.linspace(0, len(s) - 1, n), np.arange(len(s)), s).astype(np.float32)


B = os.path.join(HERE, 'build', SID)
os.makedirs(os.path.join(B, 'vo'), exist_ok=True)
GAP, SCENE_GAP, FPS = 0.28, 0.9, 30
t, voice, scenes = 1.0, [], []
for si, sc in enumerate(SCENES):
    s_start, lines = t, []
    for li, raw in enumerate(sc['lines']):
        who, text = (raw.split('|', 1) if '|' in raw[:3] else ('P', raw))
        drama = text.startswith('!')
        text = text.lstrip('!')
        toks = E.parse_line(text)
        spoken = ' '.join(sp for _, sp in toks)
        key = f'{si:02d}_{li:02d}_{who}_' + hashlib.md5(spoken.encode()).hexdigest()[:10]
        p = os.path.join(B, 'vo', key + '.npy')
        if os.path.exists(p):
            a = np.load(p)
        else:
            a = E.speak(toks, exag=0.7 if drama else None) if who == 'P' or who not in VOICES else kokoro(spoken, *VOICES[who])
            if who in VOICES:
                a = a / (np.abs(a).max() + 1e-6) * 0.9
            np.save(p, a)
        words, cov = E.align(toks, E.word_times(a), len(a) / E.SR)
        lines.append(dict(who=who, text=' '.join(d for d, _ in toks), start=round(t, 3), dur=round(len(a) / E.SR, 3),
                          words=[dict(w=w['w'], s=round(t + w['s'], 3), e=round(t + w['e'], 3)) for w in words]))
        voice.append((t, a))
        t += len(a) / E.SR + (GAP if who != 'P' else GAP + .05)
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
print('total', round(total, 1), 's =', round(total / 60, 2), 'min')
