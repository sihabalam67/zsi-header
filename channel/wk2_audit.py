#!/usr/bin/env python3
"""Audit narration with Whisper: per-line word coverage from align() (target >= 0.95), plus loudness of renders.

    python3 channel/wk2_audit.py ep03_gas ep04_fed
"""
import hashlib
import importlib
import os
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def audit(mod_name):
    mod = importlib.import_module(mod_name)
    ep = mod_name.split('_')[0]
    low, total, n = [], 0.0, 0
    for si, sc in enumerate(mod.SCENES):
        for text in sc['lines']:
            toks = engine.parse_line(text)
            spoken = ' '.join(sp for _, sp in toks)
            vid = engine.VOICE if engine.VOICE_ENGINE == 'kokoro' else engine.VOICE_ENGINE
            key = hashlib.md5(f'{vid}|{spoken}'.encode()).hexdigest()[:12]
            a = np.load(os.path.join(HERE, 'build', ep, f'vo_{key}.npy'))
            _, cov = engine.align(toks, engine.word_times(a), len(a) / engine.SR)
            total, n = total + cov, n + 1
            if cov < 0.95:
                low.append((si, round(cov, 3), text))
    print(f'{mod_name}: {n} lines, mean coverage {total / n:.3f}, below 0.95: {len(low)}')
    for row in low:
        print('  ', row)


def loudness(path):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', path, '-af', 'ebur128=peak=true', '-f', 'null', '-'],
                       capture_output=True, text=True).stderr
    summary = r[r.rfind('Summary:'):]
    li = [l.strip() for l in summary.splitlines() if l.strip().startswith(('I:', 'Peak:'))]
    print(f'{os.path.basename(path)}: {" | ".join(li)}')


if __name__ == '__main__':
    for name in sys.argv[1:]:
        audit(name)
    for f in sorted(os.listdir(os.path.join(HERE, 'out'))):
        if f.endswith('.mp4') and f.startswith(tuple(a.split('_')[0] for a in sys.argv[1:])):
            loudness(os.path.join(HERE, 'out', f))
