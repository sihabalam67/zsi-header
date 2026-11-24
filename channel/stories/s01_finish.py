"""Finish story #1 after the voice is done: render frames in parallel, mix audio, encode.
    python3 channel/stories/s01_finish.py            # full render -> channel/out/s01_grandpa.mp4"""
import json
import os
import subprocess
import sys

import numpy as np
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import engine as E  # noqa: E402

B = os.path.join(HERE, 'build', 's01')
tl = json.load(open(os.path.join(B, 'timeline.json')))
total, nfr = tl['total'], int(tl['total'] * 30)
fr = os.path.join(B, 'frames')
# 1) frames, 4 workers
W = 4
procs = [subprocess.Popen(['node', os.path.join(HERE, 's01', 'rec.js'), os.path.join(B, 'timeline.json'), 'full', fr,
                           str(nfr * i // W), str(nfr * (i + 1) // W)]) for i in range(W)]
for p in procs:
    p.wait()
# 2) audio: voice + music + sfx on story beats
v = np.load(os.path.join(B, 'voice.npy'))
mus = E.music(total, os.path.join(B, 'music.wav'), tempo=96, seed=11)
fx = np.zeros(int(total * E.SR), np.float32)
for s in tl['scenes']:
    E.place(fx, E.sfx('pop'), max(0, s['start']) + 0.05)
    for ln in s['lines']:
        if ln['who'] == 'N':
            E.place(fx, E.sfx('ding'), ln['start'])
out = E.master(v, mus, fx, total)
sf.write(os.path.join(B, 'mix.wav'), out, E.SR)
# 3) encode
dst = os.path.join(os.path.dirname(HERE), 'out', 's01_grandpa.mp4')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', '30', '-i', os.path.join(fr, '%06d.jpg'), '-i',
                os.path.join(B, 'mix.wav'), '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p',
                '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', dst], check=True)
# 4) captions .srt from word timings
def ts(x):
    return f'{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int(x * 1000 % 1000):03d}'
n, rows = 1, []
for s in tl['scenes']:
    for ln in s['lines']:
        ws = ln['words']
        for i in range(0, len(ws), 7):
            ch = ws[i:i + 7]
            rows.append(f"{n}\n{ts(ch[0]['s'])} --> {ts(ch[-1]['e'] + .1)}\n{' '.join(w['w'] for w in ch)}\n")
            n += 1
open(os.path.join(os.path.dirname(HERE), 'out', 's01_grandpa.en.srt'), 'w').write('\n'.join(rows))
print('done', dst, round(total / 60, 2), 'min')
