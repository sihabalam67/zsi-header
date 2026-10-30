# Faceless YouTube Channel Playbook (how Coin Theory is made)

Copy this whole file into a new AI chat and add your own topic at the bottom. Everything here is free and open
source. It describes the full system: tools, folder layout, how each video is made, how it is uploaded and
scheduled, the daily and weekly routine, the quality checklist, and the mistakes to avoid.

Important: a plain chat can't run programs, render videos or upload to YouTube. You need an AI that can run code on a
computer (a coding agent with a terminal, or you running the scripts it writes). The AI writes and runs the code;
you do only the few clicks YouTube doesn't allow apps to do.

---

## 1. What the channel is

- Faceless, animated explainer channel. A cartoon mascot (ours is "Penny", a coin) explains a trending topic with
  simple animated drawings, charts and big captions. AI voice narration. No camera, no face, no stock footage.
- Format per week: 2 long videos (8+ minutes) + 6 Shorts (under 60 s, made from the same research).
- Every number comes from official public data and is checked by code before rendering. Sources are cited on
  screen and in the description. Original script, original art. Marked as AI-voiced (YouTube "altered or synthetic
  content" = yes). Not made for kids. Education only, never personal advice.
- Topics are picked by search demand: what people are searching and watching right now in the niche.

## 2. Free tool stack

| Job | Tool (license) |
|---|---|
| Language | Python 3 |
| Drawing every frame | Pillow (PIL), numpy; shapes, text, icons drawn in code |
| Icons | Lucide SVG icons (ISC), rendered with cairosvg |
| Fonts | Poppins, Montserrat, Anton, Bebas Neue (Google Fonts, OFL) |
| Charts and data | pandas; data downloaded as CSV from FRED (St. Louis Fed) or any official source for your topic |
| Voice | Chatterbox TTS (MIT) as main voice; Kokoro TTS (Apache-2.0, voice "af_heart") as backup |
| Voice check + captions timing | faster-whisper (transcribes each line; words are matched to the script to time captions) |
| Music | Original MIDI generated in code, played with FluidSynth + GeneralUser GS soundfont (free) |
| Sound effects | Kenney CC0 audio packs (pop, ding, whoosh, tick) |
| Loudness | pyloudnorm, normalize to -14 LUFS, peak limiter so true peak stays under 0 dB |
| Video encode | ffmpeg (H.264, CRF 16-17, AAC 256k, +faststart) |
| YouTube automation | YouTube Data API v3 + YouTube Analytics API (google-api-python-client, google-auth-oauthlib) |
| Calendar reminders | Google Calendar (optional) |

Install (Linux): `apt-get install ffmpeg fluidsynth sox libcairo2-dev` then
`pip install kokoro-onnx soundfile faster-whisper pyloudnorm pydub scipy numpy pandas pillow cairosvg pretty_midi
google-api-python-client google-auth-oauthlib` and Chatterbox in its own virtual environment (`pip install
chatterbox-tts`, CPU torch is fine, it's just slower).

## 3. Folder layout

```
channel/
  engine.py          the video engine (drawing helpers, voice, captions, music, mixing, rendering)
  art.py             shared drawings for the channel (mascot, cards, charts, icons rows, end card)
  epNN_topic.py      one file per episode: data, number checks, scenes, Shorts
  vshorts.py         vertical versions of Shorts scenes
  thumb_epNN.py      thumbnails (A and B versions for YouTube's thumbnail test)
  make_kits.py       titles, descriptions, tags, chapters for every video -> channel/out/<name>.upload.json
  fetch_data.py      downloads data series as CSV into channel/data/
  data/              CSV data (keep a frozen copy per episode so old videos stay reproducible)
  out/               rendered videos (not in git), captions .srt, thumbnails, kits, video_ids.json, playlists.json
  SCHEDULE.md        the source of truth: which video goes live on which day
youtube/
  upload.py          upload one video from its kit (private + scheduled), thumbnail, captions
  publish_batch.py   upload a whole week from plan.json, schedule 2 PM local, playlists, links, launch questions
  replace_short.py   swap an uploaded, still-scheduled video for a re-rendered file (same day, same playlist spot)
  daily.py           post launch comments when videos go public, list and answer viewer comments
  stats.py           views, watch time, average % viewed, subscribers, traffic sources, countries
  trends.py          what's trending: recent videos on given keywords ranked by views per day
  qa.py              read-only check of every uploaded video against its kit and the schedule
```

## 4. How one episode is made (step by step)

1. **Pick the topic.** Run `trends.py "<keywords>" --days 7` for several candidate topics. Pick the one with the most
   views per day for recent videos and that you can explain with real data. Lead the title with a concrete number.
2. **Get the data.** Download official data series (CSV). Compute every number the script will say.
3. **Write the episode file.** At the top: load data, compute numbers. Then `check_numbers()` with asserts, e.g.
   "the script says 'more than double' only if peak/low > 2", "the month named in the script is the month in the
   data". The build refuses to run if any check fails. This is what keeps the channel trustworthy.
4. **Write scenes.** Each scene is a dict:
   `dict(draw=function, chapter='Chapter title', lines=['narration line 1', 'line 2', ...], sfx=lambda L: [(L[1], 'pop')])`.
   The draw function gets the time `t` and the start time of each narration line `L[i]`, so animations happen exactly
   when a line is spoken ("By May, it hit $4.50" -> the pump price counts up at L[1]). Numbers in lines are written
   with digits; the engine converts them to spoken words for the voice ("$4.50" -> "four dollars and fifty cents").
5. **Shorts.** Pick the 2-3 most surprising moments. Draw them natively vertical (720 x 1280 canvas, content between
   y=180 and y=900, captions near y=960, keep the bottom 20% empty because YouTube's buttons cover it, text size 28+,
   chart labels 24+). End with the mascot end card "Full story on <channel>".
6. **Preview.** Render stills of every scene (`--stills`), including each Shorts frame as it will look on a phone.
   Look at every one: overlaps, cut-off text, anything too small to read on a phone.
7. **Render.** The engine: voices each line (Chatterbox, checked by Whisper; retries up to 5 times; falls back to
   the backup voice with a loud warning), times captions word by word, draws every frame at 3840 x 2160, downsizes to
   2560 x 1440 for long videos (YouTube gives 1440p uploads its sharper encode) or 1080 x 1920 for Shorts, adds music
   that ducks under the voice, sound effects, crossfades, masters to -14 LUFS, writes the .srt captions and chapters.
8. **Audit.** Whisper re-checks that every line was spoken correctly; loudness and length are checked.
9. **Thumbnails.** Two versions (A and B) per long video, 1280 x 720, under 2 MB: one huge number, the mascot with
   an emotion, 3-5 words max.
10. **Kit.** Title (under 100 characters, number first), description (hook, what you'll learn, chapters, sources,
    "education only, not financial advice", "narrated with an AI voice"), tags (under 500 characters), category
    "Education", language, not made for kids, synthetic media = yes.

## 5. Upload, schedule and launch

- **API setup (one time):** Google Cloud project -> enable YouTube Data API v3 and YouTube Analytics API -> OAuth
  client (Desktop) -> publish the consent screen to "In production" (otherwise tokens expire weekly) -> run a login
  script once to get a refresh token. Keep YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN as secret environment
  variables. Never paste them into a chat, log or file.
- Apps that Google hasn't audited can only upload **private** videos, but **scheduled publishing still works**:
  upload private with `publishAt` and YouTube makes it public at that time.
- `publish_batch.py plan.json` uploads the week's videos: long videos first, then Shorts with a "Watch the full
  video" link to their long video; schedules each at 2:00 PM New York time on its day (daylight saving handled);
  creates/updates a playlist per topic series; adds "Previous episode" and "Full series" links to long descriptions;
  saves IDs. Then `qa.py` must say NO PROBLEMS.
- **Quota:** the API gives 10,000 units a day; one upload costs about 1,600 (plus captions 400). So about 5 uploads
  a day. It resets at midnight Pacific. Plan uploads days ahead.
- **Daily automation (scheduled task):**
  - 2:07 PM: `daily.py` posts a question as the first comment on each long video that just went public, and a
    "Watch the full video" link on each Short; lists unanswered comments; the AI replies to each (short, warm,
    specific, facts only from the video, no personal advice, skip spam).
  - 8:43 PM: another reply round.
  - It also notices follow-up questions in threads already answered and comments YouTube held for review.
- **Weekly (Thursday):** `stats.py` + `trends.py` -> short report -> make next week's batch (2 long + 6 Shorts),
  publish, check, update the schedule and reminders.

## 6. What you still do by hand (YouTube doesn't allow apps)

- Pin the question comment on each long video right after it goes public (open video -> the comment's ⋮ -> Pin).
- End screen on each long video (Studio -> video -> End screen -> add "Best for viewer" video + Subscribe).
- Thumbnail test (Studio -> video -> Test & compare -> upload thumbnail A and B).
- Optional: a Short's "Related video" link to its long video, if your account has it.
- Optional: heart good comments.

## 7. Quality checklist (every video, every time)

- Every number in the script is computed from data and asserted in `check_numbers()`. Date-based lookups, never
  "the 13th value from the end" (missing months shift it).
- Long videos 8:00+ when the material supports it (mid-roll ads need 8 minutes), never padded.
- 1440p for long videos, 1080 x 1920 vertical for Shorts, 30 fps.
- -14 LUFS loudness, true peak under 0 dB (limit samples at about -1.9 dBFS, because AAC encoding adds about 1 dB).
- Every voice line verified by Whisper (at least 90% of words recognized); no mixed voices in one video.
- Captions uploaded (.srt), chapters in the description (first at 0:00, at least 3, each 10+ seconds).
- No `<` or `>` in titles or descriptions (YouTube rejects them).
- Look at the previews of every scene before rendering; look at a contact sheet of the final file after.
- Sources on screen and in the description. "Not financial advice." AI voice disclosed.

## 8. Bugs we hit (avoid them)

- **Phantom white boxes:** an easing function returned 0.0000000000000002 instead of 0 before an element's start
  time, and drawing a fully transparent shape made the drawing library fall back to solid white. Result: empty white
  outlines on screen for seconds. Fix: return exactly 0 before start, and skip any shape whose fill and outline are
  both fully transparent.
- **Shorts that were just the 16:9 video in a strip** used a third of the phone screen. Draw Shorts natively
  vertical.
- **Wrong 12-month comparisons** when a month of data was missing. Use dates, not positions.
- **Voice process printing to the same pipe as its answers** broke the voice worker. Send library chatter to stderr.
- **Killing processes by name pattern** also killed the shell running the command. Kill by process ID.
- **Brand-new playlists** are "not found" for a few seconds after creation; retry with a pause.
- **Read-after-write** on the API can be stale for a few seconds; wait before verifying.
- **Comments can't be posted on private/scheduled videos**; post them after the video goes public.
- **YouTube can't replace a video file**; to fix a scheduled video, upload a new copy with the same publish time,
  put it in the same playlist position, verify it's scheduled, then delete the old copy.

## 9. Growth habits that matter

- Topic = what people are searching this week, explained with real numbers better than anyone else.
- Title and thumbnail carry one concrete, surprising number. Test two thumbnails.
- First 5 seconds state the surprising fact and the question the video answers.
- Shorts every day, each pointing to the long video. Long videos in series playlists. Every long video ends by
  teasing the next one.
- Reply to every comment early; pin a question that's easy to answer.
- Turn on YouTube's auto-dubbing so one video reaches other languages.
- Read the weekly numbers (average % viewed, traffic sources) and make more of what works.

---

## Prompt to start a new channel

> You are my YouTube production engineer. Build and run the system described above for a new faceless channel about
> **[YOUR TOPIC]** for **[YOUR AUDIENCE, COUNTRY, LANGUAGE]**. Mascot idea: **[YOUR MASCOT]**. Brand colors:
> **[COLORS]**. Use only free, open-source tools and official/public data sources for this topic, and cite them.
> Start by: (1) researching which subtopics people search most right now, (2) proposing the first 2 long videos and
> 6 Shorts with titles that lead with a concrete number, (3) setting up the engine and rendering episode 1 with a
> number-checking function, previews of every scene, and the full quality checklist. Never print or store my API
> secrets in chat. Ask me only for things that need my accounts or clicks, and give those to me as step-by-step
> instructions.
