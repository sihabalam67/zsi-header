# What works on Coin Theory (updated Nov 21, 2026 from `python3 youtube/learn.py`)

Every new video must beat the previous ones. Before writing a script, run `python3 youtube/learn.py`, read this
file, and write down in the episode docstring the 3 specific things this video does better than the last one.
After each video's first 3 days, add its numbers to the table below and update the rules.

## Scorecard (long videos, lifetime; API has no impressions/CTR, so "first 3 days" stands in for click pull)
| Video | Views | First 3 days | Watch min | Avg view | Kept at 30 s / 1 min / 2 min | Main traffic |
|---|---|---|---|---|---|---|
| Gold Fell 23% From Its Record. What Happened? | 1,545 | 1,359 | 2,113 | 2.8 min (35%) | 66% / 51% / 43% | suggested 1,423 min, browse/home 626 min |
| Microsoft Just Offered 60,000 Buyouts... | 132 | 93 | 67 | 1.9 min | 74% / 53% / 38% | browse |
| The Fed Just Raised Rates... | 29 | 18 | 36 | 1.8 min | 50% / 35% / 25% | suggested |
| Stocks Rose 18 Times Out of 18 After Midterms... | 112 | 77 | 30 | 0.9 min | 48% / 31% / 17% | browse |
| Why Is Gas So Expensive Right Now? | 21 | 10 | 15 | 1.2 min | 46% / 31% / 15% | search |
| Only 1 Dollar in 10 Is Cash (Banks) | 21 | 2 | 1 | 0.3 min | - | search |
| Stocks Fell 6 Days in a Row. Is a Crash Coming? | 218 | 167 | 209 | 3.1 min (38%) | 68% / 57% / 45% | browse |
| Fear Index Hits 37. What Happens Next? | 71 | 46 | 115 | 4.0 min (49%) | 73% / 64% / 55% | search, browse |
| The Nasdaq's Worst Week Since 2020. Now What? | 288 | 221 | 551 | 3.6 min (44%) | 75% / 61% / 53% | suggested 127, browse 83 |
Long-video watch hours, all time: ~59 of 4,000 (Nov 23).

## Progress check (Nov 23)
- Retention got much better with the daily format: the last 3 videos hold 68-75% at 30 s and 3.1-4.0 min on
  average (gold: 65% and 2.8 min). Pass mark "over 3 min average" met by all three.
- Clicks are still the weak spot: 71-288 views vs gold's 1,357 in 3 days. Thumbnails were changed to bright
  photos on Nov 21; titles shortened. Next: broader, everyday topics (see topic lesson) to raise clicks.
- Missed Nov 22 and Nov 23 videos: the session was down and the daily run didn't fire on time.

## What the winner did that the others didn't
1. **Thumbnail: bright, real photo of one recognizable thing (gold bars) + 2 huge words with one number
   ("GOLD -23%").** Our Nov 19-21 thumbnails were dark abstract chart lines: much less to click on.
2. **Title: short (45 characters), [thing] + [dramatic number] + "What happened?"** Longer titles (55-74 chars)
   did worse.
3. **Topic with a huge audience** (gold in 2026), not a niche policy topic (Fed mechanics, bank reserves).
4. **Hook held people:** 66% still watching at 30 s vs 46-50% for the weak ones.
5. **YouTube pushed it through suggested videos and the home feed**, not search and not our Shorts. That only
   happens when people click and keep watching.

## Topic lesson from the scout (Nov 21)
- "Your 401(k) Is Down 10%. Here's What History Says Comes Next." from a channel with 279 subscribers: ~52,000
  views/day. Same data story as our Nov 21 video, framed around the viewer's own money. Frame topics as "your
  401(k) / paycheck / rent / groceries", never index jargon ("S&P 500 correction", "VIX").
- Highest demand this week (English, views/day of recent videos): stock market crash ~255k, gold price ~137k,
  AI bubble ~78k, Black Friday ~59k, recession ~48k, car prices ~38k, bitcoin crash ~36k, Social Security ~30k.
  Big channels own the top of "stock market crash" and "gold price"; small channels are winning car prices,
  housing, grocery prices, credit card debt, rent and 401(k) angles.

## Ideas taken from the awesome-opus5-5-videos prompt library (703 code-animation prompts, Nov 24)
- "Something happens on every beat": top motion pieces change the frame on a fixed rhythm (often a 120 BPM grid,
  i.e. every 0.5 s). Our pace check allows 6 s; aim for a visible change every 2-3 s in the intro and every 4-5 s
  after.
- Real data, real objects, no placeholders: the best explainers show the actual thing (a receipt, a store shelf,
  a phone app) rather than abstract boxes. Our Thanksgiving receipt scene is this idea.
- Distinct visual identity per piece (hand-drawn pencil, storybook character, black-stage product film): we now
  A/B test templates (newsroom / paper / bold) instead of one fixed look.

## Where every video loses people
- The biggest drops are in the first 10-30 seconds, on every video. The intro is the weakest part.
- Second drop: the first chapter change (~1 min) when the video switches from the hook to background.

## Rules for the next video (apply every one, every day)
1. **Thumbnail (v4, Nov 24, owner: "the thumbnail is the main part"):** made with `channel/thumbs4/` (specs.json +
   `node channel/thumbs4/render.js channel/thumbs4/specs.json <name>`). Learned from the 30 most-viewed money videos of
   the last 4 months: (a) a BIG emotional face, 30-50% of the frame: for us Penny, shocked, hands up, sweat, shock
   lines, white sticker outline; (b) a mini-story in the picture: old price tag crossed out → red arrow → new price,
   red candles stepping down, a fear gauge in the red, a crashing chart; (c) 2-5 words, one in a red box, yellow/white
   with thick black outline; (d) high contrast, saturated, sunburst or photo background, dark vignette; (e) never reuse
   the same background on two videos; (f) the viewer must understand the topic from the picture alone. Check the
   thumbnail at 320x180 (phone size) before shipping. Nov 24: new v4 thumbnails set on ep10-ep13; compare their
   views/day before vs after on Nov 27.
   Old rule (still true for the background): bright photo-real background (Canva AI image: one object or scene, no text, no logos, no real
   people) + max 3 words incl. one number, high contrast, warm colors. Never a dark abstract chart again.
1b. **Thumbnails = 3 bets, one title (Nov 24, owner: "almost looking same and not good").** The two-worlds split
   (crying loser vs cheering winner) was used 3 times in a row and is RETIRED as a default. Every long video now
   follows the `youtube-packaging` skill (.claude/skills/youtube-packaging) + `.claude/references/thumbnail-principles.md`:
   one locked title x 3 thumbnail bets, each a DIFFERENT lever (number lead / object-curiosity / face-reaction) and a
   DIFFERENT background color. Each bet: ONE big positive face (head fills ~60% of the height, no tears/no sad
   faces), ONE hook, max 3 words that never repeat the title, bright saturated `rays` background, must read at
   120 px wide. Upload bet A by API; B and C go to the owner for Studio Test & Compare. Log the winner per lever
   here. Example: out/thumbs/s03_janitor_A/B/C.jpg (specs s03_janitor_A/B/C).
   CHANNEL GRID RULE (owner's screenshot, Nov 24: "why all 4 look same"): viewers see thumbnails as a stack on the
   channel page, so the LIVE bet is chosen to differ from the 3 newer/older neighbours in lever, background color
   AND face side (alternate left/right). Never make the same letter (A) live for every video. Before uploading, stack
   the last 4 live thumbnails vertically at 480 px wide and look at it like the channel page.
   PRE-CLICK PSYCHOLOGY (Nov 24, thumbnail-expert agent briefs from the installed skills): every live thumbnail
   opens ONE gap only the video closes, each with a different trigger: hidden item ("ONE ITEM DOUBLED" + ? tag),
   dramatic irony (happy kid, mouse eating his "TOTALLY SAFE" jar), identity reversal ("BORING" crossed out, "WON"),
   forbidden secret (glowing open vault, "BOX 467"). Live set = <name>_X specs. Log which trigger wins.
   OWNER STANDING ORDER (Nov 24): ALWAYS follow and take suggestions from the two installed repos (youtube-skills,
   youtube-packaging) via the thumbnail-expert agent (.claude/agents/thumbnail-expert.md), and every thumbnail must
   pass the CHILD TEST: a small child can say what it's about in one second = one big face + one object everyone
   knows + money VISIBLE (coins/cash) + max 3 everyday words. No codes ("BOX 467"), jargon (401k) or word games.
   KEEP THE BOTTOM-RIGHT CORNER EMPTY (x > 1450, y > 850 on 1920x1080): YouTube's duration badge covers it (owner's
   phone screenshot, Nov 24: the $126,766 / $16,368 / $132.50 tags were hidden). Titles: checked with yt-title-optimizer
   (40-60 chars, one number, positive outcome framing, no words shared with the thumbnail).
2. **Title:** under 50 characters; one big number; curiosity ("What happened?", "Why?", "Now what?").
3. **First 15 seconds:** say the most surprising fact in the first sentence, show a new visual every 2-3 s, no
   long first sentence, and promise the payoff ("by the end, you'll know ..."). Keep the full intro under 25 s.
4. **First minute:** go straight to the most interesting part (the crash day, the big chart), not definitions.
   Definitions come later, in one line.
5. **Open loops:** tease the best stat early ("and one number from 1987 that surprised me, in a minute").
6. **Topic choice:** the biggest money story that a general audience is searching today; prefer famous assets
   and household money (stocks crash, gold, housing, gas, paychecks) over policy mechanics.
7. **Length:** 8-10 min (mid-roll ads need 8:00+), but never pad: if retention data shows a dull section, cut it.
8. **Every 3 days:** re-run learn.py on the newest videos; if a title or thumbnail underperforms its peers in the
   first 3 days, change it (titles and thumbnails can be changed after upload).

- 2026-11-24 daily check: no new long video today (ep13 Groceries 12 PM + Coffee Short 2 PM were already scheduled).
  Every long video still loses its biggest share at 0:05-0:15 (the intro line), even the best one (Gold, 1,602 views,
  65% at 30 s). Next videos: open on the picture of the payoff, not on the number read aloud; first line under 8 words.
  Best traffic = SUBSCRIBER + RELATED_VIDEO (Gold 926 + 602): topics next to big news videos win.
