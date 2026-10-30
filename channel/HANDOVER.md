# Handover for the next Claude session (Coin Theory channel)

Read this first when the user says "upload week 1", "week 2", "set up weekly autopilot", or similar.

## What exists
- `studio/`: free toolkit. Run `bash studio/setup.sh` if `python3 studio/check.py` fails.
- `channel/engine.py`: the video engine (Penny the coin mascot, captions aligned to the script,
  Kokoro voice `af_heart`, FluidSynth music, -14 LUFS master, crossfades, vertical Shorts).
- `channel/ep01_inflation.py`, `channel/ep02_housing.py`: episodes. Each has a number guard
  (`check_numbers()`) that blocks rendering if the narration disagrees with `channel/data/*.csv` (FRED).
- `channel/out/`: rendered videos, thumbnails, `.en.srt` captions, `*_chapters.txt`, and upload kits
  (`*.upload.md` for humans, `*.upload.json` manifests for `youtube/upload.py`). Rebuild kits with
  `python3 channel/make_kits.py`.
- `channel/WEEK1.md`: posting schedule. `channel/PLAN.md`: channel plan and the next topics.
- `youtube/upload.py` (upload one manifest), `youtube/stats.py` (read-only analytics report).

## YouTube access
The user stored `YT_CLIENT_ID`, `YT_CLIENT_SECRET` and `YT_REFRESH_TOKEN` as environment variables.
Never print, log, commit or echo their values. Check that they exist with `[ -n "$YT_REFRESH_TOKEN" ]`.
The OAuth app is "In production" (tokens don't expire weekly). The API project is not yet audited,
so YouTube locks API uploads to **private**: upload private and tell the user which day to switch
each video to Public (see WEEK1.md). Custom thumbnails need the channel's phone verification (done).

## Status (Oct 29, 2026)
- Weeks 1 and 2 (16 videos) are uploaded and scheduled via `publishAt` (2:00 PM ET). IDs: `channel/out/video_ids.json`,
  playlists: `channel/out/playlists.json`. See `WEEK1.md`, `WEEK2.md`, and the checklist artifact linked in WEEK2.md.
- Week 2 episodes: `ep03_gas.py`, `ep04_fed.py` (shared art in `wk2_art.py`, audit in `wk2_audit.py`).
- Render resumably after an interruption: `RESUME=1 python3 channel/ep0N_*.py`.
- Automation (scheduled tasks firing into the Claude session): daily 2:07 PM ET runs `youtube/daily.py`
  (launch comments + replies; Thursdays also analytics and next week's videos), and 8:43 PM ET a reply round.
  The API can't pin comments or set a Short's Related video; the user does those two by hand.
- Launch order changed Oct 29 after `youtube/trends.py` showed gas prices far ahead in demand: Gas (Oct 30),
  Fed (Nov 2), Housing (Nov 6), Inflation (Nov 9). Run trends.py on Thursdays to pick topics.
- From week 3 on, new videos use the upgraded defaults: Chatterbox voice (Whisper-checked per line, falls back
  to Kokoro) and AUDIO_STYLE=upgrade (GeneralUser GS soundfont + Kenney CC0 effects). Weeks 1-2 were
  made with VOICE_ENGINE=kokoro AUDIO_STYLE=classic; use those to re-render them identically.
- Next: ep05 "How banks create money out of thin air" (promised at the end of ep04).

## "upload week 1"
1. `pip install google-api-python-client google-auth` if needed.
2. Dry-run every manifest: `python3 youtube/upload.py channel/out/<name>.upload.json --dry-run`.
3. Upload in schedule order: ep01_inflation, ep01_short_prices, ep01_short_wages,
   ep01_short_rule70, ep02_housing, ep02_short_price, ep02_short_payment, ep02_short_supply.
   Quota is about 6 uploads per day (1,600 units each of 10,000); if quota runs out, report it and
   continue the next day.
4. Report each video's link and remind the user of the steps only they can do: "Test & compare"
   thumbnail B for the long videos, end screens, Shorts "Related video" links, and switching to Public.

## Standards (the user asked for no compromises)
- Original script, art and characters only; never copy other creators' content.
- Every number must come from data in `channel/data` and pass a guard; cite sources in descriptions.
- Audit narration with Whisper (`align()` coverage >= 0.95, or explain each gap); check frames and
  loudness before delivering.
- Long videos should aim for 8-10 minutes from episode 3 on (mid-roll ads).
