# Daily production (owner's decision, Nov 19 2026)

The owner handed Coin Theory over completely: "the channel is yours, the one goal is monetization, don't ask me,
make same-day videos on what's live today, no week-ahead schedules." This file is the daily routine. It replaces the
"2 long videos a week" rule in RESET_PLAN.md (the English channel plan there still stands as a later option).

## Why this format (from our own data, Nov 19)
- Long video watch hours are the only path to the 4,000 hours. Shorts-feed views don't count, and our Shorts sent
  almost nobody to long videos (Banks: 5 views from ~200 Short views).
- The one long video that worked, "Gold Fell 23% From Its Record. What Happened?", was a timely question about a
  big money move: 1,343 views and 615 watch minutes in days, mostly from suggested videos and the home feed.
- So: one long video (8-10 min) every day about the biggest money story of that day, published the same day.

## Every day
0. **Learn first (mandatory).** `python3 youtube/learn.py`, then read channel/LEARNINGS.md. Compare the newest
   video with the best one (views in first 3 days, % still watching at 30 s / 1 min, average view, traffic).
   Write the 3 concrete improvements this video makes over the last one at the top of the new episode file, and
   update LEARNINGS.md with anything new. If a recent video's first 3 days are clearly below its peers, change its
   title or thumbnail (set_thumbs.py / the API) the same day.
1. **Pick the story with the topic-scout agent (by ~noon ET).** Spawn the `topic-scout` agent (.claude/agents/
   topic-scout.md); it measures demand with `youtube/scout.py` and returns the top 3 with titles. Pick the one with
   the widest everyday audience we can back with data. After drafting the script, spawn the `script-doctor` agent
   on it before the full render.
   (Old step, still valid:) WebSearch today's money news (markets, Fed, inflation, jobs, housing, gas,
   gold/crypto, a big IPO or layoff, a new law that changes paychecks or taxes). Check search demand with
   `python3 youtube/trends.py "<topic>" --days 3`. Choose the story most people are searching *today* that we can
   explain with real data. Title = the question people type ("Stocks Fell 6 Days in a Row. Is a Crash Coming?").
2. **Get the numbers.** Only from primary data we can download and recompute: Yahoo chart API (indexes, futures,
   stocks), FRED via `channel/fetch_data.py`, BLS/BEA/Treasury/Fed releases. If a fact can't be verified from a
   primary source or two major outlets, leave it out. Never invent; every number gets an assert in check_numbers.
3. **Pick the look and animation with channel/STYLE_PLAYBOOK.md** (built from all 703 prompts of the
   awesome-opus5-5-videos library): use the topic table to choose the main family + look and 2-4 devices (Crash
   Quake, Coins as Data, Receipt & Recipe, Loot Reveal, Money Machine, ...). Write the 6-part creative brief
   (inputs/direction/structure/build/gotchas/start, with the BANNED list) into the episode docstring. Device scenes
   can be HTML pages rendered with `window.frame(t)` + Playwright using `channel/motion/kit.js` (springs, beat grid,
   count-ups, coins-to-balance, shockwave, mask-rise text, grain); see `channel/demo_character/` for a full example
   with Penny. Record look, family and devices in channel/out/styles.json.
   **Then write `channel/epNN_<slug>.py`** using the newest episode as the template (ep10_stocks.py): 10-13 scenes,
   ~1,300-1,450 words (8-9 min). The answer in the first 30 s; a subscribe ask right after the hook's payoff and
   at the end; one question for the comments; "education only, not financial advice". Drawn charts are enough;
   no real people, no logos.
4. **Check and render.** `--check`, then `--stills` and look at every still (no overlaps; keep chips above y=600,
   the caption band starts at ~620). Then the full render (~30-40 min). Fix pace warnings with --only.
5. **Thumbnails.** Bright photo-real background (Canva generate-image: one object/scene, no text, no logos, no
   faces/real people; place it on a 1920x1080 page of design DAHZ5Imlf3g and export PNG), then a SPEC entry in
   thumbs_v3.py: max 3 words with one number. Never a dark abstract chart. Look at the sheet next to the gold
   thumbnail (our best) and only ship if it's as clickable.
6. **Publish the same day.** Write `channel/out/epNN_<slug>.upload.json` (title, description with chapters and
   sources, tags, thumbnail B for news, captions .srt, categoryId 27, not made for kids, language en) and a plan
   in `channel/plans/`, with the launch time in New York time: as soon as it's ready, at a whole hour, ideally
   12-7 PM ET. `python3 youtube/publish_batch.py channel/plans/<plan>.json`, then `python3 youtube/qa.py`.
   Add the other two thumbnails as Test & Compare options in Studio only if the API can't (it can't; skip).
7. **After it's live**: `python3 youtube/daily.py` posts the launch question; reply to every real comment
   (sourced facts only, never personal financial advice, skip abuse).
8. **Commit and push** everything except build files. Log the video in channel/out/LOG.md (date, title, id).

## Template A/B test (owner's request, Nov 24)
Each video uses one visual template, set at the top of the episode file BEFORE importing the engine:
`os.environ.setdefault('STYLE', 'paper')`. Templates: `newsroom` (dark navy data desk, Nov 19-24), `paper` (light
notebook, ink-dark text), `bold` (near-black stage, saturated accents). Rotate so every template gets at least 3
videos (next order: paper, bold, newsroom, ...); record the choice in channel/out/styles.json ({"epNN_slug": style})
when publishing. `python3 youtube/learn.py` prints a "By template" comparison (first-3-day views, % kept at 30 s,
average view). After 3+ videos each, use the winner most days and keep testing a challenger 1 day in 3. New
templates are welcome (ideas: hand-drawn pencil, storybook mascot, receipt/real-object close-ups, from the prompt
library github.com/yihui-dev/awesome-opus5-5-videos): add them to engine.py the same way.

## Lessons so far
- The narration runs faster than word count suggests: ~1,450 words gave 5.5 min. Aim for ~2,000 words and check
  the length with a pre-render before the final numbers are in; YouTube needs 8:00+ for mid-roll ads.
- For market stories, pre-render during the day, then refresh the data after the 4 PM close, rerun --check and
  re-render (voice is cached per line, so only changed lines are re-voiced). Update the title, thumbnail text and
  launch question to the closing numbers too (Nov 20: the VIX moved from 30 to 37 at the close).
- Never `pkill -f`; stop a render by its PID.

## Weekly (Thursday)
`python3 youtube/stats.py 28` -> channel/WEEKLY_REPORT.md: watch hours, subscribers, and per video average view
time and subscribers per 100 views. Double down on topics and title styles that hold viewers longest.

## Hard rules (unchanged)
No bought views/subscribers, bots, sub-for-sub, comment spam or misleading titles. No real people or logos in
AI images. Every number sourced and recomputed. Never personal financial advice. No spending money. Keep secrets
out of logs and git. Don't delete published videos.
