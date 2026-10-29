# Studio toolkit

Everything used to make the channel's videos. All tools are free and open source,
and licensed for commercial use (a monetized YouTube channel).

```bash
bash studio/setup.sh     # install / repair everything (~5 min first time)
python3 studio/check.py  # health check
```

Cloud sessions start fresh, so run `setup.sh` at the start of a session, or paste
`bash studio/setup.sh` into the environment's **Setup script** setting so it runs automatically.

| Job | Tool | License |
|---|---|---|
| Narration (main) | [Kokoro](https://github.com/thewh1teagle/kokoro-onnx) TTS, 50+ voices | Apache-2.0 / MIT |
| Narration (backup) | [Piper](https://github.com/OHF-Voice/piper1-gpl): `norman` (public domain), `joe` (CC0) | GPL-3.0 tool; voices PD/CC0 |
| Word-timed captions, transcribe your own recordings | [faster-whisper](https://github.com/SYSTRAN/faster-whisper) `base.en` | MIT |
| Clean up a phone recording | noisereduce, sox | MIT, GPL |
| Loudness to YouTube standard (-14 LUFS) | pyloudnorm, ffmpeg loudnorm | MIT, LGPL |
| Music with real instruments | pretty_midi + FluidSynth + FluidR3_GM soundfont | MIT, LGPL, MIT |
| 2D animation | Pillow, skia-python (antialiased vector drawing) | HPND, BSD-3 |
| Math / chart animation | manim Community | MIT |
| Charts | matplotlib | PSF-style |
| SVG icons → images | cairosvg + [Lucide](https://lucide.dev) icons (1,500+) | LGPL, ISC |
| Fonts | Poppins, Montserrat, Nunito, Anton, Bebas Neue | SIL OFL 1.1 |
| Data | FRED (US economic data, CSV, no key), World Bank API, yfinance | free public data |
| Encoding | ffmpeg (H.264 / AAC) | LGPL/GPL |
| Upload to YouTube (optional) | google-api-python-client | Apache-2.0 |

Models download to `studio/models/` (git-ignored, ~600 MB).
Fonts and icons are committed in `studio/assets/` (both licenses allow redistribution).
