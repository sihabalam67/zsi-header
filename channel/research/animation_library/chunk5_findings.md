# Chunk 5 findings: 140 prompts (0xrathi … zakisbuilding)

How to read this chunk: about 45% of these files are only the post text, with no real prompt ("made this in Remotion, wow"), or a single line such as "make a dynamic 15-second motion graphics video that shows what an incredible motion designer you are". About 20 prompts are long, structured and full of craft detail, and nearly all the useful material comes from them. Ratings are **Fit** (fit for Coin Theory money explainers) and **Feas** (how feasible in our offline, frame-deterministic Python/PIL + Playwright HTML/SVG/Three.js stack), each 1-5.

---

## 1. STYLE FAMILIES

### A. "One shape, never cut": morphing UI motion (Dribbble style)
**Look:** A warm-gray or off-white stage with black and white UI and one accent color. A single element morphs through 8-12 states (button → loader → check → slider → chart → toast), a cursor drives every change, and screen-studio camera zooms make each state fill the frame. The video loops.
**Techniques:**
- Palettes: warm gray plus #FD9543 accent; stage #f3f3f0→#e3e3de with dark world #121212 and #1ed760; warm off-white with one orange accent. Fonts: Geist, or Archivo (wdth 125, wt 800) for wordmarks.
- Motion: springs with "a tiny overshoot at most". Morphs take 0.8s on cubic-bezier(.45,0,.15,1), and the camera zoom uses the same curve.
- Sliders "stretch past max" and rubber-band. A tab indicator or toggle knob has its leading and trailing edges on different springs, so it stretches like liquid.
- Goo merges use blur + alpha threshold. Floods fill the frame and contract into the next scene. An iris-blade transition has 6 blades.
- Timing: 120 BPM, 7 bars or 54 beats, "something on every beat".
**Best:** nezbuilds-294391, annacher-433425, rossaxbt-312793, twoclipping-496100 (also threeaus-886343, diamai-157697, annacher-152174)
**Tech:** HTML/SVG/CSS computed inside `seek(t)`, Playwright, ffmpeg tmix
**Fit 4 / Feas 5.** This is close to our `window.frame(t)` engine already. Money UI maps onto it directly: paycheck stub, budget slider, 401(k) toggle, chart.

### B. Premium dark-stage product film (timestamped timeline)
**Look:** A near-black rounded "stage" covering about 80% of the canvas, set on an atmospheric gradient. White type, gray secondary text, one brand green. Album art or UI cards slide, expand and converge. A persistent player bar ties the shots together.
**Techniques:**
- Second-by-second timeline, about one idea per second.
- Match-position transitions, masked vertical text reveals, perspective tilt that settles to frontal.
- Critically damped springs, motion blur only during the fastest zoom.
- "Outgoing titles must disappear before incoming titles occupy the same space."
- Banned: particles, lens flares, camera shake. Uses 3-5 temporal subframes.
**Best:** brainextends-606193, raphaelaubryy-687877, aschapmann-724497, cipherwrk-451155
**Tech:** HTML/SVG, seek(t)
**Fit 4 / Feas 5.** Use the persistent-bar idea as a "wallet HUD" that stays on screen through a whole segment.

### C. Kinetic / architectural typography
**Look:** Words carry the whole frame. Letterforms act as structure: a word works as a lintel, a support or a floor. Editorial serif, heavy grotesque and mono.
**Techniques:**
- Palette #102820 bg / #F4E9D5 paper / #F2B544 accent. That is money green, cream and gold.
- High-contrast serif for the speech, heavy grotesque for "load-bearing" words, monospace for timing marks.
- Cues come from phrases, not a dance beat. "At least one 400ms moment of absolute stillness."
- Critically damped settling, with elastic deformation on only one element (the baseline).
- Real glyph paths for deformation. Transitions between unrelated words use occlusion, not path interpolation.
- render(0)=render(20) for a seamless loop.
- Other variants: a pitch-black 120 BPM grid (noah-z-zhang-765393) and an Evangelion title-card lyric video (kurahu-capten-054506).
**Best:** gdgtify-929495, noah-z-zhang-765393, kurahu-capten-054506, rohanpaul-ai-500542
**Tech:** SVG/Canvas
**Fit 5 / Feas 4.** Ideal for hooks, thesis lines and outros ("Rent ate the raise"). Glyph-path deformation takes extra work (opentype.js or fontTools).

### D. Hand-drawn / paper collage / paper puppet
**Look:**
- Whimsical cut-paper collage, "walking paper puppet" characters.
- Paper that folds, grain, "painted swaps".
- Pencil line drawing that builds up and is then painted with color and finished with gold leaf (shunshu-944719).
- Cardboard and paper textures with cinematic post-processing (jrayon-054015).
**Techniques:**
- Line draw-on first, then color fill, then "point gold" as the last accent.
- Grain overlay. Paper-fold geometry ("work out how the paper had to fold").
- Soft shadows instead of line boil: "Abandon line boiling; use hand-written vector gradients, soft shadows, night-sky glows" (ayi-ainotes-933194).
**Best:** shunshu32385143-944719, vignesh-rav-417649, jamee-now-583635, hakimieiqbal-762926 (also so-ainsight-225926)
**Tech:** SVG/Canvas/Three.js
**Fit 5 / Feas 4.** A warm, human look for grocery, rent and paycheck stories. Paper grain and drop shadows are trivial in PIL.

### E. Storybook / cartoon character short
**Look:**
- A small character with a clear action arc: steps, charges up, runs, impact.
- Silent-film shorts where "sound tells half the story".
- A life-cycle loop: childhood → 9-5 → family → old age → loop.
- Cuphead-style cartoons and comedic "fights".
**Techniques:**
- Every action synced to piano or harp notes frame by frame.
- A cursive title flips and "lands as a decimal point", then confetti.
- An anchor character feature, such as the cat's eyes that watch, blink on the beat and land on the logo (leowenai-125931).
**Best:** ayi-ainotes-933194, loicrambo-980558, kamstudiolabs-100086, leowenai-125931 (also xanderwow-a-597063, kadaliao-048854, taylorbereiter-189192)
**Tech:** SVG/Canvas, Web Audio
**Fit 5 / Feas 4.** This is the home for Penny. The "decimal point landing" gag is made for a money channel.

### F. Cartoon game "reward / loot reveal"
**Look:** A chunky toon 3D chest or medal with a heavy dark outline (#1A1033) and saturated colors. Tier colors escalate green → blue → purple → gold. Light rays, coins and gems burst out, and numbers roll up.
**Techniques:** five stages.
1. Idle bob with a periodic "tap me" shake.
2. Each level-up: jump, spin, then squash on landing and rebound.
3. About 1s charge: shaking intensifies, light leaks through the seams, particles are sucked inward, pitch rises, then a final squash.
4. Burst: bloom flash (screen blend, ≤0.8), shake, camera push, three-layer shockwaves (wide-faint / medium / thin-bright), spinning coins. Confetti only once, at the climax.
5. Reveal: cards arc out and settle with overshoot, numbers count up with a "▲+value" popup, coins fly along Béziers into the top-right balance, which bumps on each arrival.

Rendering and type details:
- Fonts: Titan One / Lilita One with black outline, letters "slam" in.
- Three.js MeshToonMaterial with a 3-4 step gradient. Outlines come from post-process normal + depth edge detection, not an inverted hull.
- Background rays: conic-gradient, 2-3 layers at different speeds.
- Glow sits behind the subject and only spills from its edges.
**Best:** op7418-818226, juancarlos17626-429530 (3D logo intro in chrome, gold, glass, clay or neon)
**Tech:** Three.js + Canvas2D particles + GSAP (port it to a seek(t) function)
**Fit 5 / Feas 4.** Penny or a piggy bank "leveling up" for employer match, a tax refund or compound-interest milestones. Best Short material in the chunk.

### G. 3Blue1Brown-style mechanism explainer
**Look:** A clean diagram where every frame is a pure function of time. Built around one core question, with a curiosity hook, a counter-intuitive point and an everyday analogy.
**Techniques:**
- Zoom across scales, "from the whole body down to a single molecule".
- A side-by-side comparison of scenarios on the same input (Healthy vs Type 1 vs Type 1 + insulin).
- A slider from INTACT to BROKEN, and "follow one molecule through the body".
**Best:** parkerrex-701462 (token bucket, canvas only), curieuxexplorer-016717, testlandblog-617500, cryptoxorz-359201 (also kureshirfan-386691, kloss-xyz-067876)
**Tech:** Canvas/SVG
**Fit 5 / Feas 5.** This is the core body format for 8-10 min videos.

### H. Physical machine / Rube Goldberg simulation
**Look:**
- A wooden board, brass toggles, glass marbles, warm studio light, a slow camera following "the busiest part".
- A domino cascade where each domino is 1.5× the previous one.
- A take-apart engine, and a stress heat-map with a crack that grows step by step.
**Best:** techartist-697078, godsboy7777-150194, stefanostraus-971191, chang-200908
**Tech:** Three.js (+Rapier). We would script it analytically for determinism.
**Fit 4 / Feas 3.** Dominoes growing 1.5× each step are a perfect picture of compound interest or inflation. Physics engines need baking.

### I. 3D object build / product turntable
**Look:** A LEGO-style step-by-step assembly, a can with painted labels, logo pieces that fly in and assemble, then a glint and letter-by-letter name.
**Best:** juancarlos17626-429530, sammmaing-702076, per-simmons-944727
**Tech:** Three.js
**Fit 3 / Feas 4.** Good for a channel ident (a gold coin assembling) and for "what's in a $5 burger" built piece by piece.

### J. Halftone / glitch / psychedelic VJ
**Look:**
- Halftone xerox print look.
- Beat-cut sticker cutouts with white borders.
- RGB split and band tearing on the beat, kaleidoscope, hue-rotate on the chorus.
- Huge difference-blend words that flash once per bar, plus film grain and scanlines.
**Techniques:**
- Effect intensity per song section: intro about 40%, verse 70%, chorus 100%.
- Tearing resets before the next beat. Never the same pose on two adjacent beats.
**Best:** pound75423-464968, leowenai-125931, yama-kiyo-134910, nonbiri-ai-110674
**Tech:** Canvas
**Fit 2 / Feas 5.** Use it only as a short "market panic / crash" stinger.

### K. Retro pixel / voxel
**Look:** A pixel history of human progress, a 3D pixel pelican crossing a bridge, Minecraft-style TNT and a "gold and diamond tower" with craters.
**Best:** xodud-rkd-160324, 0xverdao-776363, sadalbert10-856416
**Fit 3 / Feas 5.** A pixel "history of money" timeline would work. So would a gold tower blown up by TNT as a stock-crash Short.

### L. Generative shader art (demoscene, mosaic, ink)
**Look:**
- A chrome sphere that gains one Mandelbox level per hit and collapses into gold 3D letters.
- A glass and gold-leaf mosaic whose tiles "were never glued down" and lift, flip and re-form.
- A Qi Baishi ink painting with paper fibre.
**Best:** nischalsharma-587738, xanares-738984, youwareai-259061, jrayon-054015
**Fit 3 / Feas 3.** The gold mosaic suits a gold-price video: tiles re-form into a chart. Raymarching is expensive offline.

### M. Particle re-construction of footage (workflow)
**Look:** Source footage is rebuilt from dots, squares or glyphs, sized by depth and brightness.
**Techniques:**
- Show the original first, then transform it.
- Alternate fast and slow sections, and clash colors between adjacent cuts.
- Grade feedback by hit strength: a light nudge on every hit, some particles flying at camera on medium hits, a time-freeze orbit on only the one or two biggest hits.
**Best:** pluvio9yte-662953
**Fit 3 / Feas 4.** Example: a $100 bill rebuilt from tiny "$" glyphs.

### N. Generic SaaS launch / showreel and interactive games
Most of these are one-liners: ann-nnng, prasad-pilla, jayscambler, thilina-a, deedydas, chatgptastra, souravbhar871, nolkeeg, plus the games 0xrathi, ved-cj, nolit64, lexnlin, curieuxexplorer-772215.
- egawa-ai-design-092323 is the one useful structured example: deep green × gold, Mincho font, "calm and adult-oriented", 5 numbered message beats, frame review every 0.25s.
- wani-shola-459278 gives useful brand rules (listed in section 2).
**Fit 2 / Feas 3.**

---

## 2. REUSABLE TECHNIQUES

**Timing and motion math**
- **Closed-form springs, "a sum of springs".** A value that changes target several times is the sum of one spring step response per change, so it stays a pure function of t (nezbuilds-294391, twoclipping-496100). Port this directly to our Python engine.
- **Two-edge springs.** The leading and trailing edges of a pill or bar ride different spring constants, so it stretches ahead and catches up (annacher-433425). Use it for a highlight sweeping across a receipt line.
- **Rubber-band past max.** Drag a slider beyond its limit and it stretches, then springs back from where it was released (nezbuilds-294391, rossaxbt-312793). Use it for "budget overspent".
- **Same curve for morph and camera.** Morph and zoom share cubic-bezier(.45,0,.15,1) over 0.8s, so shape changes "feel almost invisible" (rossaxbt-312793).
- **Easing discipline.** Critically damped motion for settling. Elastic only on the one element whose whole job is to bend. One planned 400ms total stillness before the payoff (gdgtify-929495).
- **Squash and stretch with anticipation.** Jump, spin, squash on landing, rebound. Before a payoff, about 1s of building shake plus rising pitch, then a hard squash (op7418-818226).

**Reveals and counters**
- **Count-up with "▲+value" popup,** and coins that fly along Béziers into a balance which bumps on each arrival (op7418-818226).
- **Escalating tier color.** Green → blue → purple → gold, switching the main color, glow and background tint each level (op7418-818226). Use it for net-worth milestones.
- **Glow behind, never over.** Bloom spills only from the subject's edges. Flash uses screen blend at ≤0.8 and never full white. Shockwaves are three stroked rings: wide/faint, medium, thin/bright (op7418-818226).
- **Line-then-paint reveal.** Pencil line-art builds stroke by stroke, then is painted in, with gold accents last (shunshu32385143-944719).

**Transitions and continuity**
- **Flood transition.** A shape floods the frame and contracts into the next scene. It must overscale past the corners and take about 0.3s, or half the screen changes in one frame (twoclipping-496100).
- **Persistent anchor.** One element stays through the film: a player bar (brainextends-606193), cat's eyes that blink on the beat (leowenai-125931), or one orange circle as "the through-line and the cut" (threeaus-886343). Our version: Penny, or a running "$ left this month" pill.
- **Match-position handoffs.** The hero object keeps its identity and position across scenes. Element positions are measured at runtime (brainextends-606193, raphaelaubryy-687877).
- **Text hygiene.** Swapped text inside a morphing container needs its own enter/exit timing or mask. Outgoing titles leave before incoming ones arrive (nezbuilds-294391, brainextends-606193).
- **Seamless loop for Shorts.** Last frame = first frame, cursor position and speed included. render(0)=render(T) (annacher-433425, gdgtify-929495).

**Rendering and polish**
- **Subframe motion blur.** 3-4 subframes per frame (t−1/240, t, t+1/240), blended with `ffmpeg tmix` at 60fps. Stationary text stays sharp (raphaelaubryy-687877, brainextends-606193).
- **Paper / grain / scanline overlay** at low strength, with a fade-in from black (pound75423-464968, vignesh-rav-417649).
- **Fixed seeds everywhere.** Render a 5-6-step parameter sweep side by side and pick one (pluvio9yte-662953).

**Beat grid, sound and pacing**
- **120 BPM grid, beat ≈ integer frames.** At 60fps, 30 frames = 1 beat. Cuts land on downbeats, UI hits on beats, and the biggest move lands on the drop (raphaelaubryy-687877, nezbuilds-294391, alanschwegler-629665).
- **Measure the track with numpy.** Get BPM, the first downbeat, energy per bar and the drop, and start on a downbeat (diamai-157697).
- **SFX placed by measured peak, not file start.** Keep SFX quiet under the music and loudnorm to -14 LUFS (raphaelaubryy-687877). Alternative rule: "one soft sound effect for every element that appears and silence otherwise" (aschapmann-724497).
- **Effect intensity per section.** About 40% in the intro, 70% in the verse, 100% at the climax. Low-energy sections get quiet "breather" shots (pound75423-464968).
- **Fast-slow alternation.** Constant speed numbs viewers. Clash colors between adjacent cuts. End with a resolution such as particles growing into color blocks, or a return to the original (pluvio9yte-662953).
- **Brand rules.** Three colors, the site's own fonts, one idea per shot, centered key objects, "a rhythm that speeds up and slows down with the story" (wani-shola-459278).

**QA and anti-slop**
- **Self-QA passes.** Render one frame per beat first. Scan for single-frame pops (frame-difference spikes 3× their neighbours). Review a frame list every 0.25s. "Inspect eight representative frames" (twoclipping-496100, egawa-ai-design-092323, gdgtify-929495).
- **Anti-AI-slop bans.** No corner frames or corner text ("typical AI giveaways", souravbhar871-477361). No full stops in on-screen text (raphaelaubryy-687877). No particle bursts, lens flares or holds over 1s. "Make it less like a powerpoint" (leowenai-125931).

---

## 3. PROMPT PATTERNS

- **XML-sectioned brief.** The sections are `<inputs>` `<direction>` `<structure>` `<build>` `<gotchas>` `<start>`, and the strongest prompts all use this template (nezbuilds, annacher, rossaxbt, twoclipping, raphaelaubryy). Example: *"Ask me for the inputs, then show me the state list on the beat grid before you write any code."*
- **An explicit Banned list.** It names the clichés to avoid, not just the goals. Example: *"Banned: bouncy easing, particle bursts, glows, gradients on UI chrome, mismatched icon strokes, dead time, anything that looks like a template."*
- **A concrete second-by-second storyboard,** with the exact on-screen words and colors per beat (brainextends-606193, gdgtify-929495). Example: *"4.9–5.8 seconds: A compact search field appears. Type 'Glass Tides'."*
- **A governing visual metaphor or rule** that every scene obeys. Examples: *"Words have assigned architectural roles. WAIT is a lintel… FLOOR is a platform."* and *"Every scene is made out of the previous one: nothing fades, blurs or cuts."*
- **Engineering constraints that force determinism and quality.** Example: *"Every style is computed from time inside seek(t): no CSS transitions, no timers, no state between frames."* Pair them with known gotchas, e.g. *"No will-change on anything the camera scales."*
- **Self-review before delivery, plus blunt iterative notes.** Examples: *"render it, check the frames yourself and fix anything that overlaps, clips or feels rushed"* and *"Some parts too fast, some too slow. Only the key hits on the beat. Make it readable."* (elkrispis-872980)

---

## 4. TOP 10 FOR COIN THEORY

1. **gdgtify-929495.** Architectural kinetic type in green, cream and gold (#102820/#F4E9D5/#F2B544). **Hook/outro:** "Your raise… got eaten by rent". RENT works as a lintel pressing down on the sentence, and SAVINGS becomes the floor the final line stands on.
2. **op7418-818226.** Loot-box reveal with tier escalation and coins flying into a balance. **Short / payoff beat:** Penny "levels up" as the 401(k) employer match unlocks (green → gold), with a count-up "▲+$3,000".
3. **rossaxbt-312793.** A slider dragged past max rubber-bands into a green chart, and the knob becomes the final data point. **Chart segment:** "bump your 401(k) from 3% to 10%". The drag turns into a 30-year growth curve with the number counting up.
4. **twoclipping-496100 / nezbuilds-294391.** One black shape morphs through states (Ordered → Printing % → On its way → Delivered). **Short "Life of a paycheck":** a $2,000 pill shrinks through Taxes % → 401(k) → Rent → Groceries → $143 left, then loops.
5. **parkerrex-701462.** A token bucket in canvas, pure function of t. **Explainer:** emergency fund or envelope budgeting as a bucket that refills at the paycheck rate while bills drain it. The same model works for credit utilisation.
6. **techartist-697078.** Each domino is 1.5× the last, carrying the push from desk to room scale. **Hook for compound interest or inflation:** a $1 domino topples its way up to a house-sized one, with a year counter on each domino.
7. **curieuxexplorer-016717.** Whole-system to single-molecule zoom, with side-by-side scenarios and an INTACT→BROKEN slider. **Explainer:** "follow one dollar" from the Fed down to your grocery receipt. Compare No 401(k) / 401(k) / 401(k)+match on the same salary.
8. **brainextends-606193.** Timestamped dark-stage film with a persistent player bar. **Template for a long-video segment:** a persistent "wallet HUD" (balance, month progress) stays at the bottom while scenes change above it. Copy its timeline-prompt format as our scene spec.
9. **loicrambo-980558.** One person from childhood → 9-5 → family → old age, looping. **Short:** "Lifetime earnings in 30s". A paycheck stack grows and shrinks with each life stage, then loops back to a piggy bank.
10. **nischalsharma-587738 + shunshu32385143-944719.** Gold-leaf mosaic tiles that lift and re-form, and line-art that gets painted and gilded. **Gold-price video:** a gold bar's tiles fly apart and re-form into a 50-year price chart. The intro draws a coin in pencil, paints it, then gilds it. 0xverdao-776363 is the alternative: a gold and diamond tower blown by TNT for a "stock crash" Short.

**Honorable mentions:**
- kamstudiolabs-100086: a silent short where sound tells the story, for a no-narration Short.
- egawa-ai-design-092323: a calm green × gold "adult" tone with numbered beats.
- pluvio9yte-662953: the graded hit-feedback and fast-slow pacing rules.
- juancarlos17626-429530: a gold-material logo intro as the channel ident.
