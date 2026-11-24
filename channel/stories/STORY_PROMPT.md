# Coin Theory master story prompt (v1, Nov 24, 2026)

Our own prompt for every story video. It combines the strongest prompts from the awesome-opus5-5-videos library
(slugs in brackets, notes in channel/research/animation_library/) with the owner's feedback on stories #1 and #2.
The writer agent (.claude/agents/story-writer.md) writes the script. This prompt drives the visuals, sound and
QA. Fill in every `{…}` and keep it in the episode docstring.

```
<inputs>
  story: {one-line premise}   numbers: channel/stories/sNN_numbers.py (N[...] only, asserted)
  cast: {codes, names, one personality line each, cast.js colors}   length: 8.5-9.5 min, 16:9 + one 9:16 Short
</inputs>

<direction>
  One governing visual rule [gdgtify-989608 "the baseline is a trajectory"; rossaxbt-707651 "one dot threads every
  scene"]: {e.g. "the 401(k) form never leaves the story: it is checked, crumpled, kept, returned"}.
  Look: Penny Storybook on warm paper; ONE saturated hero color per scene (gold = money that grows, red = debt)
  [notdwd-998633]; cold blue-gray world for the losing path, warm gold world for the winning path (scenes only; thumbnails follow LEARNINGS 1b).
  Characters are actors, not stickers [astrothewizard-618782 "give it a personality"; jakubantowski-020905 felt
  blob]: blink, breathe, look at whoever speaks, react within 0.3 s (gasp, laugh, nod), squash on landings.
  MOTION LIMITS (owner feedback Nov 24): calm, readable motion. Talking = slow head nod (<= 2.5 deg) + one hand
  gesture; idle sway <= 0.5 deg; never jitter; shakes only on a real impact, <= 0.3 s, <= 6 px [froessell-562325
  camera juice: "a tiny shake on light hits, hit-stop on big ones, never continuous"].
  Camera: push in to the speaker (1.12x) on dialogue, wide on narration; one slow push per hold (1.03) so no frame
  is dead [twoclipping-041659]; punch-in 1.0→1.08 only on reveals [techhalla-498547].
  Voices: Penny = channel narrator; each character = Chatterbox cloned from its own reference
  (stories/voices/*.wav), expressiveness per character (EXAG in story_voice.py). Natural pace, no shouting.
  BANNED: generic tech gradients, particle spam, constant shake, crossfades, text on text, holds over 1 s without
  motion, made-up numbers, real people or logos, clip-art, robotic monotone delivery.
</direction>

<structure>  (one row per chapter; every chapter ends on a hook)
  time | device | what moves | locked on-screen words | sfx | hook line
  0:00 cold open in the middle of the crisis + the central question (Penny: "Let's go back to …")
  every ~60 s: reveal / reversal / ticking clock / cliffhanger [egeberkina-949521 "reveal something new every
  few seconds, pressure builds before release"]
  big-number reveals use Loot Reveal juice [op7418-814408]: 1 s charge (shake grows, light leaks), burst
  (3-stroke shockwave, glow BEHIND the subject), count-up with ▲+value, coins fly along Béziers into the balance
  money-as-objects beats use Coins as Data [rneayan-417829] and Receipt & Recipe [felipemoller-936736]
  history beats use Timeline Slam with a year HUD + seal-stamp transition [rpa-dake-593915, dotey-927166]
  the choice beat uses One-Shape Morph [twoclipping-402193]: the paycheck pill splits into its parts
  mid-video subscribe ask right after the first big cliffhanger; comment question + share line at the end
</structure>

<build>
  HTML page with window.frame(t) rendered by Playwright, streamed into ffmpeg in 4 parallel segments
  (stories/story_finish.py). channel/motion/kit.js (springs, beat grid, countUp, coinsTo, shockwave, maskRise,
  grain), motion/cast.js (rig + acts), motion/penny.js. Closed-form springs only; seeded randomness only
  [demonugc-525162]. Beat grid 120 BPM: cuts and reveals land on beats; sfx placed by measured peak [twoclipping-000267].
  Music ducks under voice; -14 LUFS.
</build>

<gotchas>
  - Characters' gestures read talk > 0 for the whole line (smoothed mouth, never 0 inside a line) or they flicker.
  - Labels never cover faces; captions own y >= 880; keep 150 px side margins.
  - Cache voice by md5(text) (Python hash() is random per run).
  - Every number on screen comes from N[...] and is asserted; the honesty line is in the last chapter.
</gotchas>

<start>
  1 script (story-writer) → 2 numbers asserted → 3 voices → 4 one still per line → contact sheet → critique "like a
  harsh motion director", fix the 3 worst problems [notdwd-766641] → 5 full render → frames every 20 s → 6 ship.
  Quality bar [everestchris6-399895]: <= 1 s frozen per 30 s, no still > 0.5 s in the first 15 s, text contrast
  >= 4.5:1, nothing flies through text.
</start>
```

## Ideas queued for the next stories (from the library)
- **Loot-chest reveal** for the big number (op7418): the 401(k) jar charges and bursts into coins that fly into
  the scoreboard.
- **Crash Quake** (egeberkina): a 2008/2020 crash as an earthquake cross-section with a seismograph price line.
- **Paper-fold doubling** (nft-chen #11): compound interest as a sheet folded again and again until it reaches the moon.
- **Follow the dollar zoom** (acoramaa/curieuxexplorer): from a $7 coffee receipt into the farm, the truck and the rent.
- **Era chronicle** (dotey): the history of the dollar with a different art style per era and a seal stamp per
  chapter.
