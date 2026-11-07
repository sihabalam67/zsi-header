# Laptop setup for Claude (Coin Theory)

The owner's laptop (MSI Cyborg 15, RTX 5050 8 GB, Windows) runs the GPU work; the cloud session runs the channel
(scheduling, uploads, comments; the YouTube keys live only there). Both share work through this GitHub repo.

## Rules (same as the cloud)
- Free path only: no paid API keys (no MuAPI, no DataForSEO, no ElevenLabs), buy nothing, no Pro tiers.
- Never upload or post anything; the cloud session publishes after review.
- No real or famous people, no logos in AI images or video.
- Read each installer's page or README before running it. Ask the owner before anything needing admin rights.
- Don't delete the owner's files without asking.

## Install (tools folder: C:\coin-tools)
1. VoiceStudio (voice, AGPL-3.0): Windows installer from https://github.com/debpalash/VoiceStudio/releases/latest,
   choose NVIDIA CUDA.
2. AppFlowy (notes, AGPL-3.0): installer from https://github.com/AppFlowy-IO/AppFlowy/releases, use it offline.
3. Open Generative AI (MIT): https://github.com/Anil-matcha/Open-Generative-AI/releases/download/v2.0.0/Open.Generative.AI.Setup.2.0.0.exe
   (unsigned: SmartScreen "More info, Run anyway"). Never enter a MuAPI key.
   Wan2GP for free local video: needs Git + Python 3.11, then
   `git clone https://github.com/deepbeepmeep/Wan2GP` into C:\coin-tools, run `install.bat`,
   then in the app: Settings > Local Models > Wan2GP > pick that folder.
4. OpenSEO: skip (needs a paid DataForSEO key).

## First test (after install)
- VoiceStudio: read the first two lines of `channel/sx05_short_five_a_day.py` SCENES in a clear, warm US English
  voice; save WAV to `channel/assets/laptop/voice_test.wav`.
- Wan2GP: an 8 s vertical (9:16) clip: "coins dropping into a glass jar on a wooden table, soft morning light,
  cinematic, no text, no logos, no people"; save to `channel/assets/laptop/wan_test.mp4`.
- `channel/assets/` is git-ignored, so commit the files with `git add -f` (keep each under 50 MB) and push to the
  current branch; the cloud session reviews them.
