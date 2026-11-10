# Reset plan (Nov 10, 2026). Goal: YouTube monetization as fast as possible

Owner's decision (Nov 10): run two channels. Coin Theory gets one more month with a fixed, smaller scope; a new
English-learning story channel gets most of the production time. This file replaces the "2 Shorts every day" rule
and the weekly "2 long + 6 Shorts" batch in HANDOVER.md and SHORTS_PLAN.md.

## Why the first plan failed (28 days to Nov 10: ~2,800 views, ~6 watch hours, 1 subscriber)
- Shorts were tested mostly in Japan (756 views, ~3 s each); only 95 US views. Newest Shorts get 1-13 views.
- Long videos lose viewers in 15-75 s; only long videos count toward the 4,000 hours.
- Text cards + AI voice look like every other faceless finance channel: no reason to subscribe.
- Nine topics in two weeks; no outside traffic (1 external view).
- We optimized correctness and polish, and kept adding volume after the data said viewers were not staying.
- What did work: search and suggested viewers watched ~1.5 min each; timely explainers earned the most minutes.

## Coin Theory: one month, fixed scope (decision day: Thu Dec 10)
- 2 long videos a week, each answering one money question people are searching that week (check demand with
  youtube/trends.py first; pick questions small channels can rank for). No daily Shorts; 2-3 Shorts a week that
  point to that week's long video. Videos already scheduled through Nov 18 run as they are.
- Every long video: the answer in the first 30 s; real footage/photos, fewer text cards; the title is the searched
  question; 3 thumbnails in Test & Compare.
- Owner: ~10 min a day answering one Reddit/Quora question with the video linked where allowed.
- Keep after Dec 10 only if the new long videos average over 3 min watched and at least 1 subscriber per 100 views.
  Otherwise stop and move everything to the English channel.

## New channel: English-learning stories (the main bet)
Measured with the YouTube API on Nov 10 (top 50 long videos of the last 60 days per niche, share from channels
under 8 months old): "learn english through story" 25/50, "english listening practice podcast" 15/50; finance 8/50.
Three formats win:
- A. 3D-cartoon family stories, A2, 30-45 min, 4-7 videos a week (118k-282k median views). Many near-identical
  channels (the same "Henry" on three of them): highest "mass-produced" risk, and looks like kids' content.
- B. "Learn English with stories": the story text on screen beside one illustration, slow clear voice, adult
  first-person stories. English StoryShow: 12 videos in 63 days, 1.3 a week, 6,240 subs, 99k views on video 1,
  303k on "Poor Boy to Successful Man" (26 min).
- C. Two-host "podcast" for A2-B2, 40-60 min (English Speaking Coach II: 19,300 subs in 95 days).
We start with B: it fits our tools (text + voice + illustration), needs the fewest uploads, and is for adults.
Our own angle so it is not a copy: original stories about real adult life (work, money, moving abroad), recurring
characters, our own art style, and real teaching in every video (level label, key words, a short quiz).
- Voice: AI voice is fine here (learners want slow, clear speech); better voices come from the owner's laptop
  (VoiceStudio) once Claude is set up there (channel/LAPTOP_SETUP.md).
- Pass marks per video: over 3 min average view, CTR over 4%, 1 subscriber per 100 views. Miss = change the format.
- Needs from the owner: create the channel; add its upload token as the environment secret YT2_REFRESH_TOKEN.

## Rules that stay
No bought views/subscribers, bots or sub-for-sub. Original scripts and art. Every fact sourced. No real people or
logos in AI images. Uploads private with publishAt. Nothing deleted without the owner's OK.
