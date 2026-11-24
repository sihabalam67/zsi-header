# Coin Theory Style Playbook: how every video should look and move

Built Nov 24, 2026 from a full read of all 703 prompts in github.com/yihui-dev/awesome-opus5-5-videos (viral
code-animated videos). Five agents read every prompt; their notes are in `channel/research/animation_library/`
(chunk1-5_findings.md, with example slugs; `index.json` links each slug to its original post).
**Use this file every day, at step 3 of DAILY_PRODUCTION.md, before writing the script.**

What the library taught us, in one paragraph: the videos people loved were not the "go all out" one-liners (about
45% of the library; they made generic tech reels). They came from about 100 specific briefs. These briefs had one
governing visual idea, exact numbers (hex colors, seconds, BPM, spring constants), a **banned list**, a time-coded
storyboard with locked words, real data only, and a rule to look at stills and fix them before the final render.
The motion rules repeat everywhere:
- something changes on every beat;
- nothing ever freezes (slow push-in on every hold);
- springs instead of linear moves;
- squash and stretch;
- numbers that count up;
- one hero object carries the whole film.

---

## 1. Our 13 style families (pick 1 main family per video, plus 2-4 "devices" from others)

| # | Family | The look | Best library examples | Fit / Feasibility |
|---|---|---|---|---|
| 1 | **Gold Desk** | Premium dark navy + warm gold fintech film. Crisp charts and UI, objects turn into the next scene (a chart line becomes a receipt edge). Restrained. | daniel-haida-636937, notdwd-998633, brainextends-606193 | 5/5 |
| 2 | **Paper & Marker** | Warm paper, ink-black huge kinetic type, marker notes that draw on, pencil "boil", hatching, grain. | ik-builds-585923, heyiamnick-119558, twoclipping-041659 | 5/5 |
| 3 | **Penny Storybook** | Character-led explainer (Kurzgesagt-lite): Penny has goals, gags and reactions; real numbers; burned-in captions. | astrothewizard-618782, superalesha-970412, jakubantowski-020905, byaiden-vu-755862 | 5/4 |
| 4 | **Poster Slam** | 3-color street-poster type that slams onto the beat, print misregistration on impacts, per-letter springs. | techhalla-498547, gdgtify-929495, nft-chen-068069 | 5/5 |
| 5 | **One-Shape Money Morph** | One rounded shape never cuts: paycheck pill → tax slice → 401(k) toggle → chart → "$143 left" toast. Cursor-driven, loops. | twoclipping-402193, nezbuilds-294391, rossaxbt-312793, 0xnicc0-516612 | 4/5 |
| 6 | **Money Machine** | The mechanism *is* the argument: number wheels, buckets, dominoes 1.5x bigger each, gates. Every moving part is a real operation. | gdgtify-393073, parkerrex-701462, techartist-697078 | 5/5 |
| 7 | **Coins as Data** | Real data as countable objects: "1 coin = $1 billion" pours into jars; tiles re-form into a chart; clinks are synced to collisions. | rneayan-417829, tanabe-fragm-322001, nischalsharma-587738 | 5/4 |
| 8 | **Loot Reveal** | Game "reward" juice. The chest charges up and bursts. Tiers go green → blue → purple → gold, coins fly along curves into a balance that bumps, and a "▲ +$3,000" count-up lands. | op7418-814408, op7418-818226 | 5/4 |
| 9 | **Receipt & Recipe** | A real object assembles item by item with live counters: a receipt prints, a cart fills, or a "gallon of gas" glass fills layer by layer with labelled amounts. | felipemoller-936736, ror-fly-880547, sarut0bisasuke-069973 | 5/5 |
| 10 | **Timeline Slam / Era Chronicle** | Years spring and slam onto a timeline while line art draws; each era has its own art style; year-counter HUD; a seal stamp between chapters. | rpa-dake-593915, dotey-927166, notdwd-998633 | 5/5 |
| 11 | **Crash Quake** | A cinematic science sim used as a metaphor. Stress builds at a fault line, a seismograph acts as the price chart, then the slip, then aftershocks. | egeberkina-949521 | 5/4 |
| 12 | **Follow the Dollar** | Continuous zoom or exploded view. Zoom from your $7 receipt down to the 18¢ the farmer gets, or explode a house into what your rent pays for. | acoramaa-053577, curieuxexplorer-016717, aichrislee-938609, techartist-021472 | 5/4 (2D zoom), 3D is slower |
| 13 | **Pixel Quest** | 8/16-bit game. "Compound Interest QUEST": inflation is a monster chasing you, and impulse buys are pits to jump. | 0xpai-eth-635565, zacxbt-944604 | 3-4/5 |

Low value for us (don't use as a main style): generic SaaS "showreel" reels, shader/demoscene art, glitch VJ
(only a 1-2 frame crash stinger), heavy 3D dioramas (slow without a GPU), games.

How the families map to the engine's A/B looks (`STYLE`):
- `newsroom` ≈ Gold Desk
- `paper` ≈ Paper & Marker / Penny Storybook
- `bold` ≈ Poster Slam

Families 5-13 are **devices**: whole scenes that can sit inside any look.

---

## 2. Topic → style: decide in 2 minutes

| Today's topic | Main family (look) | Hook device (0-25 s) | Body devices (pick 2-4) | Payoff / outro device |
|---|---|---|---|---|
| Stocks fall / crash / fear index | Gold Desk (`newsroom`) | Poster Slam ("6 DAYS DOWN") | Crash Quake; Timeline Slam (1929/1987/2008/2020); Coins as Data (who owns stocks) | Money Machine (what history says next) |
| Grocery / food / everyday prices | Paper & Marker (`paper`) | Receipt prints, total counts up | Follow the Dollar (receipt → farm); Money Machine (how inflation compounds); Penny reactions | Penny Storybook (what you can do) |
| Gold / silver / bitcoin price | Gold Desk | Coins as Data (gold bar tiles fly apart) | Timeline Slam (gold since 1971); Coins as Data (central banks' piles); Crash Quake for drops | Loot Reveal ("if you'd bought in 2000") |
| Paycheck / taxes / raise / jobs | One-Shape Morph on `paper` | Poster Slam ("RENT ATE THE RAISE") | One-Shape Morph (pay stub splits); Receipt & Recipe; Money Machine (tax brackets) | Loot Reveal gag ("your raise… 3%") |
| 401(k) / retirement / compound interest | Paper & Marker or Gold Desk | Money Machine (dominoes 1.5x each) | Slider-to-chart (rossaxbt); Loot Reveal (employer match); Follow the Dollar (into the fund) | Money Machine (1.07^n wheels) |
| Rent / housing / mortgage | Paper & Marker | Follow the Dollar (rent check zooms into the house) | Exploded house with cost labels; Coins as Data (rent vs. pay); Timeline (prices since 1970) | Emotional "light returns" outro |
| Credit cards / debt / national debt | Poster Slam (`bold`) | Coins as Data (1 coin = $1B pours) | Money Machine (interest snowball); Receipt (minimum payment trap) | "Blocks seal the window, one is removed, gold light enters" (agioyaz) |
| Gas / energy | Paper & Marker | Receipt & Recipe ("the recipe of a $4.29 gallon") | Follow the Dollar (crude → refinery → truck → pump, isometric) | Money Machine |
| Holidays / Black Friday / spending | Penny Storybook | Penny with a cart, the total ticks up | Receipt & Recipe; Pixel Quest (impulse-buy pits) | Loot Reveal (what you saved) |
| Social Security / policy / Fed | Gold Desk | Poster Slam (the one number) | Money Machine (how it works); Timeline Slam; One-Shape Morph (your check) | Penny Storybook (what it means for you) |
| **Shorts (any topic)** | Penny Storybook / Paper | Poster Slam in the first 1 s, shock number first | One device only, a new visual every 1.5-2 s | Loop seam (last frame = first) + Follow tap |

When unsure: Paper & Marker + Penny for household money, Gold Desk for markets. Then follow the A/B rotation in
DAILY_PRODUCTION.md for the look, and pick devices from this table.

---

## 3. Structure of a long video (8-10 min) using the devices

1. **0-3 s:** shock number as a Poster Slam or a real object close-up. Something new every 2-3 s for 15 s.
2. **3-25 s:** the payoff promise and an open loop. No definitions yet.
3. **First chapter (to about 1:30), the most dramatic device:** Crash Quake, Coins pour, Loot burst. Every
   video loses the most viewers here, so this is where the best device goes.
4. **Body chapters:** switch device every chapter. Never more than 60 s on one device without a reveal, a
   question or a surprising number. Alternate fast and slow chapters.
5. **History chapter:** Timeline Slam, with a seal-stamp transition and a drum hit.
6. **Recap:** a One-Shape Morph that walks through the 3 numbers.
7. **Outro:** an emotional device plus Penny's Subscribe/Follow tap. End on a still frame of 1.2 s.

**Persistent anchor:** one element stays across the whole video so it feels like one film. Use either Penny
(she reacts in a corner) or a "wallet HUD" pill (`$ left this month`) at the bottom.

---

## 4. House craft rules (apply all of them; `channel/motion/kit.js` implements them)

1. **Every frame is a pure function of t.** No timers, no unseeded random, no state carried between frames.
   `window.frame(t)` in HTML, `draw(c, x)` in PIL.
2. **Springs, not linear moves:** critically damped `1-(1+wt)e^(-wt)` with w = 12-40. When a value retargets,
   **sum one spring per change**. Use tiny overshoot at most, except on Penny.
3. **Beat grid:** 120 BPM = 0.5 s. Something happens on every beat in the hook, then every 2 beats. Moves
   start 0.05 s before the beat so they land on it. Cut on downbeats.
4. **Never a dead frame:** a 1.03-1.07 slow push-in on every hold. At most ~1 s of near-frozen screen per 30 s.
   The exception is one planned 400 ms freeze before a punchline.
5. **Arrive fast, land soft;** text lands slowly enough to read, then leaves fast. 700 ms reading hold before
   any decorative motion on a word.
6. **Text rises through a mask line**; nothing pops in from nowhere. Outgoing text leaves before incoming text
   takes its place. Never text on top of text.
7. **Numbers count up** in tabular figures, digits roll only while moving, then settle hard. Pop a
   "▲ +value" after.
8. **Squash & stretch + anticipation:** a 0.3-0.5 s wind-up before every big reveal. Squash on landing,
   stretch in the air. Secondary motion: Penny's blink, breathing, sweat drop.
9. **Camera:** at most 3 purposeful moves per scene: push-in, punch-in 1.0→1.08 on a beat, smash-pan. Zoom
   is interpolated in log space. Never zoom in and out back to back. Camera juice is a 50-100 ms hit-stop on
   big hits and a tiny shake on light ones, never continuous shake.
10. **Transitions are objects:** the thing in front becomes the next scene, as in a shared-element handoff, a
    color flood or an iris. Floods overscale past the corners in ~0.3 s. No plain crossfades.
11. **One hero color:** everything else is calmer, and gold/Penny is the only fully saturated thing.
    3-4 colors and 2 typefaces per video. The glow goes behind the hero, never over it.
12. **Texture pass:** light grain (fresh per frame), soft vignette; on paper, pencil boil (wobble phase
    stepped 8x/s, double stroke).
13. **Motion blur** only on fast moves: 4 subframes averaged (ffmpeg `tmix`). Counters read the frame's t, not
    the subframe's.
14. **Sound is choreography:** a soft SFX for every element that appears and silence otherwise. Place SFX
    by their measured peak. Duck music −18 dB under voice; master at −14 LUFS. Optionally drop the music out for a
    beat before the drop.
15. **Shorts:** 9:16 safe zone (captions measured in the real font, nothing under the right-side buttons or
    the bottom 300 px). The first frame is already a finished picture. Last frame = first frame (loop).

**Banned (copy this list into every brief):** generic purple/neon tech gradients, rockets, lens flares,
particle spam, constant camera shake, plain crossfades, bouncy easing on UI, corner "FIG." labels or fake HUD
numbers, text over text, holds over 1 s without motion, made-up numbers, real people, logos, clip-art.

---

## 5. The daily creative brief (write this into the episode docstring before any code)

```
<inputs>      topic, the 3-5 sourced numbers (from check_numbers), title, length, Long or Short
<direction>   main family + look (STYLE), hero object, one governing visual rule ("the receipt never leaves
              the screen"), palette hexes, 2 fonts, BANNED list (section 4)
<structure>   time-coded storyboard: per chapter = device, the on-screen words (locked), the beat it lands on
<build>       engine (PIL scenes / HTML frame(t) via Playwright), springs, beat grid, subframes yes/no
<gotchas>     anything learned last time (overlaps, caption band y>=620, numbers checked)
<start>       render stills for every scene → contact sheet → critique like a harsh motion director → fix the
              3 worst problems → full render
```

## 6. Quality gate (before publishing)

- [ ] Contact sheet: one still per scene plus one per second of the first 15 s. Check for no overlaps and no
      clipped text; contrast is at least 4.5:1.
- [ ] Pace: no still frame over 0.5 s in the hook; pace_report has no warnings.
- [ ] First sentence = the shock number; a new visual every 2-3 s for 15 s.
- [ ] Every on-screen number traces to the data (check_numbers asserts).
- [ ] Would a non-investor smile or say "whoa" at least once a minute? If a chapter has no such moment, add a
      device.

## 7. Learning loop

Record each video in `channel/out/styles.json` as `{"epNN_slug": {"look": "paper", "family": "Paper & Marker",
"devices": ["Receipt & Recipe", "Crash Quake"]}}`. `python3 youtube/learn.py` compares looks **and**
devices (first-3-day views, % kept at 30 s, average view). Every Thursday, move devices up or down this playbook
based on that table. A device that holds viewers moves into more topics; one that loses them is dropped.
