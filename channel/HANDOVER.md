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
so YouTube locks API uploads to **private**; scheduled `publishAt` still makes them public on their day
(verified on all 19 videos). Custom thumbnails need the channel's phone verification (done).

## Status (Oct 30, 2026)
- New .mp4 renders are git-ignored (GitHub rejects files >100 MB); the uploaded copies on YouTube are the archive.
- Weekly toolchain (in order): `python3 channel/fetch_data.py <FRED IDs>` -> write `channel/epNN_*.py` with
  `check_numbers()` and native vertical Shorts scenes (`vertical=True`, see below) -> `--stills` (calls
  `engine.previews`: long stills plus every Shorts scene as a phone frame) and look at all of them -> render (1440p) -> `python3 channel/wk2_audit.py epNN_*` (Whisper and
  loudness; the build also warns if any line fell back to the backup voice) -> thumbnails (`thumb_epNN.py`) ->
  kit entries in `make_kits.py` -> `python3 youtube/publish_batch.py plan.json` (uploads, 2 PM New York with DST,
  playlists, Short links, launch questions, "links" + "Full series" lines on long videos; warns under 8:00 or
  below 1440p, refuses Shorts that aren't 1080x1920 or run over 3 min) ->
  `python3 youtube/qa.py` (read-only live check of every video vs kit and SCHEDULE.md; must say NO PROBLEMS) -> `python3 channel/guide/build_guide.py` and publish its HTML with
  `url=https://claude.ai/artifact/QpErtvBZgo9XZvtmFaG4Hp` (same page) -> calendar reminders -> update SCHEDULE.md.
- Current schedule: channel/SCHEDULE.md (19 videos, Oct 30 to Nov 12). ep05_jobs is the Microsoft buyouts bonus.
- `youtube/daily.py` lists every viewer message still unanswered (top-level, replies under our launch comments, and
  follow-ups in threads we already answered), plus comments YouTube held for review (tell the user; the API can't
  heart or approve). `--reply THREAD TEXT --for CID` @mentions that viewer so they get notified.
- Video upgrades (Oct 30): long videos render at 1440p by default (`RES=1080` for the old size) so YouTube serves
  its sharper VP9/AV1 encode; chart tick labels are 19 (was 16) for phone readability (`tick_size=`).
- Shorts must be drawn natively vertical from week 3 on: give each Short scene `vertical=True` and draw on a
  720 x 1280 canvas (`c.w`, `c.h`): content between y=180 and y=900, captions sit at y=960 (`cap_y=`), keep the
  bottom ~20% empty (YouTube's overlay), text 28+ and chart ticks `tick_size=24`. Reuse the long video's data and
  helpers (gas_pump, line_chart, chip, `source_v`...) at a bigger scale; `end_card` is already vertical. Preview with `still(scene, t, path, layout='short')`.
  Old-style 16:9 scenes in a Short still work: the engine now finds their content and enlarges it (content_box).
- Audio master: limiter ceiling 0.80 (-1.9 dBFS) so the AAC true peak stays under 0 dB (Gas renders peaked +0.2).
- `youtube/stats.py` adds traffic sources and countries; impressions/CTR are Studio-only (not in the API).
- Weeks 1 and 2 (16 videos) are uploaded and scheduled via `publishAt` (2:00 PM ET). IDs: `channel/out/video_ids.json`,
  playlists: `channel/out/playlists.json`. See `WEEK1.md`, `WEEK2.md`, and the checklist artifact linked in WEEK2.md.
- Week 2 episodes: `ep03_gas.py`, `ep04_fed.py` (shared art in `wk2_art.py`, audit in `wk2_audit.py`).
- Render resumably after an interruption: `RESUME=1 python3 channel/ep0N_*.py`.
- Automation (scheduled tasks firing into the Claude session): daily 2:07 PM ET runs `youtube/daily.py`
  (launch comments + replies; Thursdays also analytics and next week's videos), and 8:43 PM ET a reply round.
  The API can't pin comments or set a Short's Related video; the user does those two by hand.
- Launch order changed Oct 29 after `youtube/trends.py` showed gas prices far ahead in demand: Gas (Oct 30),
  Fed (Nov 2), Jobs (Nov 5), Inflation (Nov 6), Housing (Nov 9). Run trends.py on Thursdays to pick topics.
- From week 3 on, new videos use the upgraded defaults: Chatterbox voice (Whisper-checked per line, falls back
  to Kokoro) and AUDIO_STYLE=upgrade (GeneralUser GS soundfont + Kenney CC0 effects). Weeks 1-2 were
  made with VOICE_ENGINE=kokoro AUDIO_STYLE=classic; use those to re-render them identically.
- Next: ep05 "How banks create money out of thin air" (promised at the end of ep04).

## Monetization first (owner's #1 priority, Oct 30)
- Goal: YouTube Partner Program as fast as possible: 1,000 subscribers + 4,000 public watch hours in 12 months
  (long videos only; Shorts don't count toward hours), or 1,000 subscribers + 10M Shorts views in 90 days. Check
  YouTube's current numbers each month (a higher hours bar has been reported for 2027).
- So: long videos 10-15 min with high retention earn the hours; daily Shorts earn subscribers and feed the long
  videos (pinned "watch the full video" comment). Weekly report tracks: subs, public watch hours (12-month
  running), Shorts views (90 days), retention, CTR, and what to change.
- Every video: 10/10 rules (hook at 0 s, pace checker, punches, loops in Shorts), 2+ thumbnails tested, honest
  titles (no misleading claims: YouTube punishes them and viewers leave).

## Owner's Google Flow (images + 1-10 s clips) — see channel/FLOW_GUIDE.md
- For each long video, first send the owner ONE brief: 2 thumbnail image prompts (two scenarios) + 1-3 clip
  prompts (hook always; Extend chains for big moments; Ingredients with assets/brand/penny_ref.png when Penny
  appears). Write it to channel/briefs/epNN.md too. Owner sends files in chat; save to channel/assets/flow/epNN_*,
  log in assets/photos/SOURCES.md, use via thumbkit.Thumb.photo and scenes with bg_video/bg_speed.
- Never block a launch on Flow: if assets aren't there a day before, use own animation + public-domain photos
  (youtube/commons.py, PD/CC0 only).
- Standalone 10/10 Shorts live in channel/shorts_v2.py (render queue channel/v2_all.sh, swaps via
  youtube/auto_swap.py --v2). New Shorts are written there, never cut from long videos.

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
