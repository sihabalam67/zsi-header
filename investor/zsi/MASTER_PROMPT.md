# ZSI.Ai investor video: master prompt (v1, Nov 24, 2026)

Built from our animation prompt library (channel/STYLE_PLAYBOOK.md + channel/research/animation_library/) and the
same engine we use for Coin Theory stories (HTML page with window.frame(t), rendered frame-by-frame by Playwright,
streamed into ffmpeg; channel/motion/kit.js springs/count-ups; Chatterbox natural voice; -14 LUFS mix).

```
<inputs>
  goal: show investors 7 real products, 4 revenue streams, the 5-year numbers, and why to invest
  sources (only these): the live calculator (5 tabs, default proposal values) + the 6 live product websites +
    the owner's brief. Nothing invented: no team, customers, partners, raise amount or valuation.
  length: ~6 min, 16:9 1920x1080 30 fps
</inputs>

<direction>
  Main family: GOLD DESK [daniel-haida-636937, notdwd-998633, brainextends-606193]: premium deep navy + warm
  gold, crisp UI, restrained, one hero colour per scene. Stream colours from the calculator:
  SaaS #1D5C7A · GoldenMark Money #A8822A · ZSI PAY #C4502F · Miscellaneous #5B4B8A.
  Devices:
  - LIVE PRODUCT TOUR (our build): each real website in a clean browser frame, smooth eased scroll with a
    cursor, gold callout chips that pop on the feature the narrator names [twoclipping-041659 "one slow push per
    hold, no dead frame"].
  - RECEIPT & RECIPE [felipemoller-936736]: the GoldenMark check prints: price $0.65, cost $0.02, we keep $0.63.
  - COINS AS DATA [rneayan-417829]: ZSI PAY: a $1,000 sale flows through; $5 drops into the ZSI PAY jar.
  - MONEY MACHINE [gdgtify-393073]: SaaS subscriptions pipe in (300 → 1,250 a year), 10% leak out.
  - ONE-SHAPE MORPH [twoclipping-402193]: a single gold bar grows into the stacked 4-colour revenue chart.
  - Big-number reveals: count-up + soft glow, no confetti, no shake [restrained Loot Reveal].
  Type: Poppins 700/900 for numbers, clean sans for labels. Every term explained once in plain words.
  BANNED: fake UI, made-up numbers or claims, stock people, logos we don't own, shake, particle spam,
  crossfades longer than 0.4 s, text over text, holds over 1 s without motion.
</direction>

<structure>  see SCRIPT.md (scene table: time | visual | on-screen words | narration)

<build>
  investor/zsi/: capture.py (Playwright full-page captures of every site and calculator tab, 1440 wide @2x),
  page/ (_head.html, _helpers.js, _scenes.js → story.html), voice via channel/stories/story_voice.py pattern,
  finish via story_finish.py pattern. Every number on screen comes from numbers.py (asserted against the
  calculator text captured today). ZSI PAY scene = one self-contained scene function; when the live link
  arrives, add its capture and swap the scene without touching the rest.
</build>

<gotchas>
  - Calculator tabs are iframes (/saas/index.html etc.): capture those URLs directly.
  - GoldenMark Money's website lists eCheck tiers at $0.60 / $0.56 / $0.50; the calculator uses $0.65:
    narration says "the proposal assumes $0.65" (owner to confirm).
  - Say once: projections from the calculator's assumptions, not guarantees. Call the combined figure
    "bottom line", best case; say what each stream's bottom line includes.
  - Testimonial names on the websites are blurred/skipped (not our claims).
</gotchas>

<start>
  1 approve SCRIPT.md → 2 captures → 3 voice → 4 one still per scene → harsh review, fix top 3 →
  5 full render → frames every 20 s → 6 owner review.
</start>
```
