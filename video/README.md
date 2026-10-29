# Second Chances

An original ~2:40 animated explainer about how immunotherapy changed late-stage cancer,
made entirely with code in Claude Code. Inspired by the *topic* of Kurzgesagt's
"How I Survived Late-Stage Cancer"; the script, characters and art here are original.

- **Animation:** Python + Pillow, drawn frame by frame (`render.py`)
- **Voiceover:** [Piper TTS](https://github.com/OHF-Voice/piper1-gpl), free and offline.
  The default voice `norman` is public domain; `VOICE=joe` (CC0) also works.
- **Music:** composed procedurally with numpy
- **Encoding:** ffmpeg

```bash
pip install piper-tts pillow numpy
python3 video/render.py            # -> video/second_chances.mp4 (about 4 min on 4 cores)
VOICE=joe python3 video/render.py
```

For education only, not medical advice.
