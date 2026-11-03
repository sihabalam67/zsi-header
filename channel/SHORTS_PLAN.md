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
10/10 rules (owner, Nov 3; sx02 v2 is the reference):
1. Payoff first: the shocking number is on screen AND spoken in the first 0.5 s (no build-up, no intro).
2. Under 35 s when possible; every beat earns its place; no scene longer than ~7 s; nothing static > 4 s.
3. One number per beat, shown big; the explanation never outruns the visuals.
4. End on a comment question tied to the viewer ("How long would yours take?").
5. Seamless loop: the last frame is frame 0 of the hook (fx.frame_break into the hook's first frame, end-scene
   cam=(1.0, 1.0)), so replays count.
6. Bright, high-contrast palette; grade eq=saturation=1.35; captions clear of every graphic.
If a topic's facts can't be confirmed, skip it and take the next one. Breaking money news beats the list.

| Day | Status | Topic | Key facts to confirm |
|---|---|---|---|
| Tue Nov 3 | live 5 PM | sx01 compound interest: start at 25 vs 35 | math (done) |
| Wed Nov 4 | live 5 PM | sx02 the credit card minimum-payment trap | $5,000 at the average card rate (ep04 CC_NOW 21.19%), minimum = interest + 1% of balance ($25 floor; a formula many card agreements use, no CFPB source found): about 19 years and $7,782 interest vs $200/month: under 3 years, $1,655 |
| Thu Nov 5 | live 5 PM | ep06 banks create money | done |
| Fri Nov 6 | to build | sx03 what $100 from 1970 buys today | CPIAUCSL in channel/data |
| Sat Nov 7 | to build | sx04 are you middle class? the real median income | MEHOINUSA646N in channel/data; Pew's middle-income definition (2/3 to 2x median) |
| Sun Nov 8 | to build | sx05 $5 a day: what it becomes | math: 10, 20, 30 years at an example rate; say "example, not a promise" |
| Mon Nov 9 | to build | sx06 why your paycheck shrinks: where taxes go | IRS / SSA 2026 rates (FICA 7.65%) |
| Tue Nov 10 | to build | sx07 the 50/30/20 budget in 40 seconds | median income example |
| Wed Nov 11 | to build | sx08 how a credit score is calculated | FICO's published weights (35/30/15/10/10) |
| Thu Nov 12 | to build | sx09 inflation: why prices never go back down | CPI data |
