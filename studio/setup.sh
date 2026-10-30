#!/usr/bin/env bash
# One-command setup for the video studio. Safe to re-run; skips what's present.
# Everything installed here is free and open source (see studio/README.md).
set -euo pipefail
cd "$(dirname "$0")"
MODELS="$PWD/models"
mkdir -p "$MODELS"

echo "== system packages"
if ! command -v fluidsynth >/dev/null || ! command -v sox >/dev/null; then
  apt-get update -qq
  apt-get install -y -qq ffmpeg fluidsynth fluid-soundfont-gm sox libcairo2-dev libpango1.0-dev pkg-config
fi

echo "== python packages"
pip install -q piper-tts kokoro-onnx soundfile faster-whisper noisereduce pyloudnorm pydub audioop-lts \
  scipy numpy pandas pillow matplotlib skia-python cairosvg pretty_midi yfinance \
  google-api-python-client google-auth-oauthlib 2>&1 | grep -iE "^error" || true

# manim needs `srt`, whose sdist won't build against Debian's patched setuptools;
# build its wheel in a clean venv instead.
if ! python3 -c "import manim" 2>/dev/null; then
  tmp=$(mktemp -d)
  python3 -m venv "$tmp/venv"
  "$tmp/venv/bin/pip" -q wheel srt -w "$tmp/wheels"
  pip install -q "$tmp"/wheels/srt-*.whl
  pip install -q manim
  rm -rf "$tmp"
fi

echo "== voice models"
K=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
for f in kokoro-v1.0.onnx voices-v1.0.bin; do
  [ -f "$MODELS/$f" ] || curl -sSfL "$K/$f" -o "$MODELS/$f"
done
for v in en_US-norman-medium en_US-joe-medium; do
  [ -f "$MODELS/$v.onnx" ] || python3 -m piper.download_voices --download-dir "$MODELS" "$v"
done

echo "== music soundfont (GeneralUser GS, free incl. commercial use)"
if [ ! -f "$MODELS/GeneralUser-GS.sf2" ]; then
  tmp=$(mktemp -d); git clone -q --depth 1 https://github.com/mrbumpy409/GeneralUser-GS "$tmp/gu"
  cp "$tmp/gu/GeneralUser-GS.sf2" "$MODELS/"; rm -rf "$tmp"
fi

echo "== expressive voice (Chatterbox, MIT) in its own venv"
VL=/home/user/voicelab
if [ ! -x "$VL/venv/bin/python" ] || ! "$VL/venv/bin/python" -c "import chatterbox" 2>/dev/null; then
  mkdir -p "$VL" && python3 -m venv "$VL/venv"
  "$VL/venv/bin/pip" -q install --upgrade pip
  "$VL/venv/bin/pip" -q install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
  "$VL/venv/bin/pip" -q install chatterbox-tts
fi

echo "== speech recognition model"
python3 -c "from faster_whisper import WhisperModel; WhisperModel('base.en', device='cpu', compute_type='int8', download_root='$MODELS/whisper')" 2>&1 | grep -v HF_TOKEN || true

echo "== check"
python3 check.py
