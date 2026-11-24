"""Finish story #1 after the voice is done: render frames in parallel, mix audio, encode.
    python3 channel/stories/s01_finish.py            # full render -> channel/out/s01_grandpa.mp4"""
import json
import os
import subprocess
import sys

import numpy as np
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
OUTNAMES = {'s01': 's01_grandpa', 's02': 's02_salary', 's03': 's03_janitor', 'z01': 'zsi_investor'}
sys.path.insert(0, os.path.dirname(HERE))
import engine as E  # noqa: E402

SID = sys.argv[1] if len(sys.argv) > 1 else 's01'
B = os.path.join(HERE, 'build', SID)
OUTNAME = OUTNAMES[SID]
tl = json.load(open(os.path.join(B, 'timeline.json')))
total, nfr = tl['total'], int(tl['total'] * 30)
# 1) video in 4 parallel segments, frames streamed straight into ffmpeg
W = 4
SCRATCH = os.environ.get('STORY_SCRATCH', B)  # big temporary files (segments, music, mix) can live in RAM (/dev/shm)
os.makedirs(SCRATCH, exist_ok=True)
segs = [os.path.join(SCRATCH, f'seg{i}.mp4') for i in range(W)]
procs = [subprocess.Popen(['node', os.path.join(HERE, SID, 'rec.js'), os.path.join(B, 'timeline.json'), 'pipe', segs[i],
                           str(nfr * i // W), str(nfr * (i + 1) // W)]) for i in range(W)]
for p in procs:
    p.wait()
open(os.path.join(SCRATCH, 'segs.txt'), 'w').write(''.join(f"file '{s}'\n" for s in segs))
# 2) audio: voice + music + sfx on story beats
v = np.load(os.path.join(B, 'voice.npy'))
mus = E.music(total, os.path.join(SCRATCH, 'music.wav'), tempo=84 if SID.startswith('z') else 96, seed=11)
fx = np.zeros(int(total * E.SR), np.float32)
for s in tl['scenes']:
    E.place(fx, E.sfx('pop'), max(0, s['start']) + 0.05)
    for ln in s['lines']:
        if ln['who'] == 'N' and not SID.startswith('z'):  # z01: N is the male presenter, not a sound cue
            E.place(fx, E.sfx('ding'), ln['start'])
out = E.master(v, mus, fx, total)
sf.write(os.path.join(SCRATCH, 'mix.wav'), out, E.SR)
# 3) encode
dst = os.path.join(os.path.dirname(HERE), 'out', OUTNAME + '.mp4')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', os.path.join(SCRATCH, 'segs.txt'), '-i',
                os.path.join(SCRATCH, 'mix.wav'), '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
                '-shortest', '-movflags', '+faststart', dst], check=True)
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
open(os.path.join(os.path.dirname(HERE), 'out', OUTNAME + '.en.srt'), 'w').write('\n'.join(rows))
print('done', dst, round(total / 60, 2), 'min')
