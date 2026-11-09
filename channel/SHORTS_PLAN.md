# 5 PM Shorts plan (2 Shorts a day: the 2 PM schedule + one new fx-style Short at 5 PM ET)

Owner's rule (Nov 2, 2026): every day two Shorts. Every new Short is built like `channel/ep06_short_banks.py`
(the owner loved it): the `channel/fx.py` motion effects, one per beat; real public-domain photos via
`youtube/commons.py`; made-up apps, chats, headlines and magazines only; every number recomputed in
`check_numbers()` from data or a cited source; no PACE WARNINGs; loop=True; 35-59 s; look at the stills before
rendering and at frames after. Name files `sxNN_short_<topic>.py`, kits `sxNN_short_<topic>`, plan
`channel/plans/sxNN.json` with playlist "Money Basics, Explained", time `"YYYY-MM-DDT17:00"` and `"news": true`.
Advanced build (from sx02): Remotion pieces live in /home/user/video-tools/remotion/coin-video/src (CardTrap.tsx is the
example: springs, 3D, film grain, local fonts), Manim scenes in channel/manim (payoff_race.py: Text-only labels, no
LaTeX), rendered silent into channel/assets/gen/sxNN and used as bg_video scenes; check that each clip's key moment
fits inside its scene (bg_speed), add `eq=saturation=1.35`, and run kinocut `kino video-quality-check` (saturation
always flags on our dark design; everything else must pass). Run third-party tools via /home/user/video-tools/safe.
Canva (owner OK'd, Nov 3; sx04 is the example): make the thumbnail FIRST with Canva create-design (YouTube Thumbnail,
brief with the exact text), export PNG 1280x720, add Penny with thumbkit, squint-test; reuse its image as the
Short's opening so thumbnail and video match; set it via the kit's "thumbnail". Canva's stock library can't be
searched through the API; if the owner fills a "Coin Theory B-roll" design, export its pages as MP4.
HyperFrames (HeyGen, Apache 2.0, installed Nov 3 at /home/user/video-tools/hyperframes, CLI 0.9.8): HTML/GSAP video compositions with a 448-block catalog (finance money counter, bar-chart race, data charts, line graph, US maps, news ticker/lower thirds, 30+ transitions, chat/notification mock-ups). Run via ../safe npx hyperframes with HYPERFRAMES_TELEMETRY=0 DO_NOT_TRACK=1 PUPPETEER_EXECUTABLE_PATH=/opt/pw-browsers/chromium; render with --no-browser-gpu (WebGPU shader blocks won't work without a GPU). 5 s 1080p block renders in ~20 s. Restyle blocks to our dark navy/gold palette before use; render silent and use as bg_video scenes.
Thumbnails v3 (Nov 3, owner: quality first): every video gets 3 thumbnails in channel/thumbs_v3.py: A = shock number, B = curiosity word (+ red BREAKING bar on news), C = fictional shocked face + a 'you' question. Backgrounds: 2 Canva AI images per Short / 3 per long video (prompts in channel/thumb_prompts.json, no text/logos/real people), exported at full size through holder designs DAHZ5Imlf3g (9:16) / DAHZ5P7G4Nw (16:9) into assets/thumbsrc/ai/<name>_<n>.png; text only from verified numbers; check the sheet at phone size; set with youtube/set_thumbs.py (add the video to CHOICE). Long videos: owner runs Studio Test & Compare with all 3.
Colorfigures skill (installed Nov 5 in .claude/skills/colorfigures, MIT, April Zhu; credit 'Colorfigures' in the description when used): hand-inked isometric 3D figures with a See-through view of the real mechanism (ATM, gas pump, vault, card reader, printing press...). Output is one interactive HTML page; record it to video with channel/colorfigure_record.js (Playwright: turn with arrow keys, press the buttons, ?xr=1&labels=1), crop away the UI, use as a bg_video scene. Costs ~15-30 min and a lot of tokens per figure, so use it for long-video 'how it works' segments, not every Short.
Real footage (from sx03): public domain only: US government films or Prelinger Archives (archive.org advancedsearch,
check creator + licenseurl in /metadata; uploaders' PD marks on movies/TV are often wrong); no logos; show it with
fx.archival (framed panel + REAL FOOTAGE stamp); log it in assets/photos/SOURCES.md; footage files are git-ignored.
10/10 rules (owner, Nov 3; sx02 v2 is the reference):
1. Payoff first: the shocking number is on screen AND spoken in the first 0.5 s (no build-up, no intro).
2. Under 35 s when possible; every beat earns its place; no scene longer than ~7 s; nothing static > 4 s.
3. One number per beat, shown big; the explanation never outruns the visuals.
4. End on a comment question tied to the viewer ("How long would yours take?").
5. Seamless loop: the last frame is frame 0 of the hook (fx.frame_break into the hook's first frame, end-scene
   cam=(1.0, 1.0)), so replays count.
6. Bright, high-contrast palette; grade eq=saturation=1.35; captions clear of every graphic.
7. No scene over ~6 s; speed up a clip (bg_speed) instead of letting a slow chart hold the screen.
8. Small on-screen text (phone screens, documents) gets a push-in (fx.zoom_canvas) so it reads on a phone.
9. Sound design: 'hit' (bass hit) on every big number reveal, 'riser' 1 s before the biggest one, pops for items.
10. The comment question has an instant answer (yes/no or a choice), shown as tappable-looking chips.
11. Owner's own voice would beat the AI voice; if they send a voice-over, build around it.
If a topic's facts can't be confirmed, skip it and take the next one. Breaking money news beats the list.

| Day | Status | Topic | Key facts to confirm |
|---|---|---|---|
| Tue Nov 3 | live 5 PM | sx01 compound interest: start at 25 vs 35 | math (done) |
| Wed Nov 4 | live 5 PM | sx02 the credit card minimum-payment trap | $5,000 at the average card rate (ep04 CC_NOW 21.19%), minimum = interest + 1% of balance ($25 floor; a formula many card agreements use, no CFPB source found): about 19 years and $7,782 interest vs $200/month: under 3 years, $1,655 |
| Thu Nov 5 | live 5 PM | ep06 banks create money | done |
| Fri Nov 6 | live 5 PM | sx03 $100 in 1962 = $1,112 (real public-domain 1962 footage) | done |
| Sat Nov 7 | live 5 PM | sx04 are you middle class? (Pew 52%, $56,600-$169,800; Census median $87,460) | MEHOINUSA646N in channel/data; Pew's middle-income definition (2/3 to 2x median) |
| Wed Nov 4 | live 9 AM (extra) | sx10 stocks after every midterm since 1950: 19/19, avg +15.1% (S&P 500 daily closes, data/SP500_midterms.csv) | done |
| Sun Nov 8 | live 5 PM | sx05 $5 a day: $152/mo, put in $54,750, about $185,537 at an example 7% (10y $26K, 20y $79K, 40y $399K); owner's Canva sx05 clips | done |
| Mon Nov 9 | live 5 PM | sx06 paycheck: BLS median $1,239/wk = $64,428; IRS 2026 brackets (single, $16,100 std): tax $5,551 = 8.6% in the 12% bracket; FICA 7.65% + employer 7.65% ($4,929); keep $53,948 | done |
| Tue Nov 10 | live 5 PM | sx07 50/30/20 on the sx06 take-home ($4,496/mo): $2,248 / $1,349 / $899; $899 for 10y at an example 7% = $155,603 | done |
| Wed Nov 11 | to build | sx08 how a credit score is calculated | FICO's published weights (35/30/15/10/10) |
| Thu Nov 12 | to build | sx09 inflation: why prices never go back down | CPI data |
