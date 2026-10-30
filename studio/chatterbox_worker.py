"""Chatterbox TTS worker (run with the voicelab venv's python). Reads JSON lines {"text", "seed", "out"} on stdin,
writes a mono WAV to "out" and answers with a JSON line {"ok": true} or {"error": "..."}.

Chatterbox (Resemble AI) is MIT-licensed. It runs on CPU at roughly 3-4x real time.
"""
import json
import sys

OUT = sys.stdout
sys.stdout = sys.stderr  # library chatter goes to stderr; only JSON answers go to OUT
import torch  # noqa: E402
import torchaudio  # noqa: E402
from chatterbox.tts import ChatterboxTTS  # noqa: E402

model = ChatterboxTTS.from_pretrained(device='cuda' if torch.cuda.is_available() else 'cpu')
print(json.dumps({'ready': True, 'sr': model.sr}), file=OUT, flush=True)
for line in sys.stdin:
    try:
        job = json.loads(line)
        torch.manual_seed(int(job.get('seed', 0)))
        wav = model.generate(job['text'], exaggeration=float(job.get('exaggeration', 0.6)),
                             cfg_weight=float(job.get('cfg', 0.4)))
        torchaudio.save(job['out'], wav, model.sr)
        print(json.dumps({'ok': True}), file=OUT, flush=True)
    except Exception as e:  # keep serving; the caller falls back to Kokoro
        print(json.dumps({'error': str(e)[:300]}), file=OUT, flush=True)
