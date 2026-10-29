#!/usr/bin/env python3
"""Smoke-test every studio tool and print a pass/fail table."""
import glob
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
MODELS = os.path.join(HERE, 'models')
results = []


def check(name, fn):
    try:
        detail = fn() or ''
        results.append((True, name, detail))
    except Exception as e:  # report and keep going
        results.append((False, name, f'{type(e).__name__}: {e}'[:90]))


def tool(cmd):
    return lambda: shutil.which(cmd) or (_ for _ in ()).throw(FileNotFoundError(cmd))


def kokoro():
    from kokoro_onnx import Kokoro
    k = Kokoro(f'{MODELS}/kokoro-v1.0.onnx', f'{MODELS}/voices-v1.0.bin')
    s, sr = k.create('Testing.', voice='am_michael', lang='en-us')
    return f'{len(s) / sr:.1f}s audio'


def piper():
    out = tempfile.mktemp(suffix='.wav')
    subprocess.run([sys.executable, '-m', 'piper', '-m', f'{MODELS}/en_US-norman-medium.onnx', '-f', out],
                   input=b'Testing.', check=True, capture_output=True)
    return 'norman voice ok'


def whisper():
    from faster_whisper import WhisperModel
    WhisperModel('base.en', device='cpu', compute_type='int8', download_root=f'{MODELS}/whisper')
    return 'base.en loaded'


def soundfont():
    sf = '/usr/share/sounds/sf2/FluidR3_GM.sf2'
    if not os.path.exists(sf):
        raise FileNotFoundError(sf)
    return 'FluidR3_GM'


def imports(*mods):
    def f():
        for m in mods:
            __import__(m)
        return ', '.join(mods)
    return f


def fonts():
    from PIL import ImageFont
    fs = glob.glob(os.path.join(HERE, 'assets/fonts/*.ttf'))
    for f in fs:
        ImageFont.truetype(f, 20)
    return f'{len(fs)} fonts'


def icons():
    n = len(glob.glob(os.path.join(HERE, 'assets/icons/lucide/*.svg')))
    if not n:
        raise FileNotFoundError('lucide icons')
    return f'{n} icons'


check('ffmpeg', tool('ffmpeg'))
check('fluidsynth', tool('fluidsynth'))
check('sox', tool('sox'))
check('soundfont', soundfont)
check('voice: Kokoro', kokoro)
check('voice: Piper', piper)
check('speech-to-text: Whisper', whisper)
check('audio tools', imports('noisereduce', 'pyloudnorm', 'pydub', 'soundfile', 'scipy'))
check('graphics', imports('PIL', 'skia', 'cairosvg', 'matplotlib', 'manim'))
check('music', imports('pretty_midi'))
check('data', imports('pandas', 'yfinance'))
check('youtube upload', imports('googleapiclient', 'google_auth_oauthlib'))
check('fonts', fonts)
check('icons', icons)

for ok, name, detail in results:
    print(f"{'PASS' if ok else 'FAIL'}  {name:26} {detail}")
sys.exit(0 if all(ok for ok, _, _ in results) else 1)
