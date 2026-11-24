# Chunk 1 findings: 138 prompts (0xevinho … zhang-baoqing)

Caveat: about 45 of the 138 are "PARTIAL" (the author posted a tweet, not the prompt) or one-liners ("make a dynamic 15-second motion graphics video… go all out"). Those show *what* people found impressive, not *how* it was made. The craft detail is concentrated in roughly 20 long prompts: daniel-haida, demonugc, flxrnc, verbove, rossaxbt, twoclipping x2, notdwd x2, gdgtify, agioyaz, majidmanzarpour, okazaky, niegramotny, superalesha and ulyssexbt. Ratings: **Fit** = suits Coin Theory money explainers; **Feas** = doable in our stack (deterministic PIL, or a Playwright `frame(t)` page, offline, no paid assets).

## 1. STYLE FAMILIES

**A. Premium fintech product film (dark navy + warm gold)**: restrained, Apple/Stripe-like. Dark metal, gold accents, crisp UI, object-driven transitions.
- Techniques (daniel-haida-636937):
  - Palette: bg #0c0f1a; surfaces #111525/#131722/#1a2032; gold #e8b84b, highlight #f5d07a, depth #9b6d18; text #e8eaf2/#f6f4eb, secondary #8b93b5; positive #34d399; negative #f87171 only where it means something.
  - Fonts: Plus Jakarta Sans, with JetBrains Mono for money figures.
  - Ease `cubic-bezier(0.16,1,0.3,1)`; overshoot under 2%; staggered arrivals.
  - Cut at 115–120 BPM. Story arc CHAOS → CONTROL → CLARITY → BRAND.
  - Transitions: "a receipt becomes a booking", "a chart line becomes a connector", "financial number → amount in invoice".
  - Look: soft gold rim light, a specular sweep, a restrained vignette, optional grain.
  - Long banned list: no particle spam, constant zoom, bouncing UI, crossfades or glitch.
- Best: daniel-haida-636937, notdwd-998633, twoclipping-000267.
- Tech: Remotion/React, SVG/CSS, frame-driven.
- **Fit 5 / Feas 5.** The gold palette is almost exactly Coin Theory's brand.

**B. Single-shape UI morph loop (Dribbble spring motion)**: one rounded shape that never cuts. It morphs button → loader → check → player → slider → chart → toast while a cursor drives it. Warm-gray or off-white canvas, black/white plus one accent.
- Techniques:
  - Closed-form spring step responses. When a value changes target several times, sum one spring per change, so it stays a pure function of time.
  - Tab-indicator edges ride different springs so the leading edge stretches.
  - Content swaps with a 12px blur over 0.15s. Content enters after its container starts morphing and leaves before the next morph.
  - Springs: shape damping 0.72 / settle 0.35s; camera damping 1.0 / settle 0.6s.
  - 0.5s beat grid (120 BPM, "something happens on every beat").
  - Counter rolls "F 000 → F 840"; word swaps roll vertically.
  - Last frame equals the first, so it loops. Loop the cursor with `t - 14*floor(t/14)`.
  - 4–6 subframes averaged for motion blur.
- Best: demonugc-525162, flxrnc-251921, verbove-268381, cgclick-497325.
- Tech: one HTML file, Canvas/SVG, `seek(t)`/`renderAt(t)`.
- **Fit 4** (banking-app, paycheck and 401(k) UI Shorts) **/ Feas 5.**

**C. "Connecting dot" minimal motion design**: off-white, near-black, one vivid orange dot. The dot threads every scene: UI toggle → dot over an "i" → spring graph → filling circle → halftone field → end card.
- Techniques (rossaxbt-707651):
  - Draw the graph from the same spring function that moves the dot.
  - One shape morphs circle → rotating square → pill.
  - Words orbit the dot, then scatter into a halftone grid whose dot sizes respond to the hero dot.
  - Bans gradients, glows, particle bursts, and "motion that isn't connected to an element already on screen".
- notdwd-766641 is in the same family: off-white, ink and one orange. A 12-frame filmstrip of a ball's bounce (squash on contact, stretch mid-air) stamps in one frame per beat. "Arrive fast, land soft (cover 12–19% of remaining distance per frame)." "Nothing ever freezes (slow push on every hold)." Stagger 2–4 frames; blur only on fast moves.
- Best: rossaxbt-707651, notdwd-766641.
- **Fit 5** (swap the dot for a gold coin, i.e. Penny) **/ Feas 5.**

**D. Kinetic / typographic explainer**: words are the visuals; the type field reacts physically to meaning.
- Techniques:
  - gdgtify-130294: bg #102820, letters #F4E9D5, field lines #F2B544. Serif for speech, heavy grotesque for "load-bearing words", monospace for gauges. Words get roles (WAIT is a repelling plate, letters lean away; FLOOR flattens into a plane). Rotate whole glyphs analytically, never morph paths. Particles are atmosphere only, hash-seeded. "Hold absolute stillness for at least 400ms".
  - nakazakifam-831964: a NextCore-style psychology explainer, type and code only, switching to a different drawing style every few seconds.
  - niirajrshah-163739: big year, one line per moment.
- Best: gdgtify-130294, nakazakifam-831964, niirajrshah-163739.
- Tech: SVG/Canvas.
- **Fit 4** (hooks, the "1971: gold standard ends" timeline) **/ Feas 5.**

**E. Paper / handmade storybook textures**: grain, collage, chalk, graphite, ink line.
- Techniques:
  - superalesha-970412: a 6.5-minute short drawn entirely in canvas, with a different medium per scene: torn-paper collage, chalk on black paper, tissue paper underwater, sand on a light table, pop-up book. A recurring motif (the "short, short, long" knock) drives both story and music.
  - obydulme-052905: procedural paper grain, graphite hatching, paint reveal, felt-piano soundtrack.
  - paripune-657175: "one unbroken line draws the whole story; it traces every object, the image fills in, and the line flows on."
  - twoclipping-041659: off-white paper, black, one red, one yellow, Geist. Grain on everything, soft vignette. "A camera that never rests: slow handheld float + slow push inside every scene." No hard cuts ("each handoff starts on the exact last frame of the scene before"). Ink blots swallow the page; brush strokes sweep through.
  - mattbean-917572 and abderrahmen-g-899031: "drawing style" and hand-drawn input images.
- Best: superalesha-970412, twoclipping-041659, paripune-657175, obydulme-052905.
- **Fit 5** (warm and friendly for groceries and rent) **/ Feas 4** (grain, hatching and line-draw are easy in PIL or Canvas).

**F. Data-as-physical-objects simulation**: real data rendered as countable things, with sound tied to physics.
- Techniques:
  - rneayan-417829: "1 marble = 1 million people", 8,144 marbles from real 2024 data, every clink synced to a simulated collision.
  - apoorvjain25-945542: soundtrack synthesized from the same bounce data ("every bounce you see is a click you hear"); real travel times.
  - ulyssexbt-205279: FFT of its own mix drives the equalizer bars.
  - michaelzsguo-782312: sand animation telling 250 years of US history.
- Best: rneayan-417829, apoorvjain25-945542, michaelzsguo-782312.
- Tech: Canvas plus a deterministic physics precompute.
- **Fit 5** ("1 coin = $1B", jars of coins for national debt, piles for income deciles) **/ Feas 4.** Pre-simulate the physics with a fixed timestep and cache positions so frames stay deterministic.

**G. Classroom explainer (Manim-ish / diagrammatic)**: a concept made visual step by step, often with a cutaway.
- Examples:
  - linearuncle-971663: Manim derivative plus edge-tts; "easy to understand, with examples, thought-provoking".
  - anirockshady-032809: gradient descent; Volcanic Orange, Cyan and a grey gradient; fade in/out.
  - miguel07code-091611: Fourier series.
  - blueoctopusai-270222: how the First-and-10 yellow line works.
  - stewchan2-369810: how backlinks work.
  - rashadmirza404-020971: optogenetics, "scientifically accurate".
  - konstantinsaifo-501736: "take apart" an engine, follow the oxygen and methane.
  - theparuchh-013286: a watch that disassembles as you scroll while it keeps running.
  - michaelraspuzzi-740595: "hook creates a curiosity gap for real-world application… switch up scenes".
  - ldataengineer-823010: P(doom) through analogy ("Would you board a plane with a 10% crash risk?").
- Best: linearuncle-971663, konstantinsaifo-501736, ldataengineer-823010, michaelraspuzzi-740595.
- **Fit 5** (exploded paycheck, "follow the dollar" through a 401(k)) **/ Feas 4–5.**

**H. Documentary / archival brand film**:
- notdwd-998633:
  - Cold open on a public-domain clip playing in a glowing CRT, with word-by-word captions.
  - Old web pages strobe one per frame; a counter "ticks EVERY frame up to today's scale".
  - The only saturated colour is one hero object (a 3D embossed button); everything else is white, silver, cream and archival black.
  - Film finish in numpy: fresh grain per frame, halation, vignette about 0.65x at the corners, 1px edge-clamped chroma fringe, 24fps.
  - Captions of 7 words or fewer, one text layer at a time.
  - Glitch lasts only 1–2 frames on a real cut, always with a click.
  - Duck the music -18dB under the narrator; -14 LUFS.
- linke1427832-343079: documentary-trailer history of AI with a synthesized score, "cut the visuals to the music".
- jdverolme-302685: 1-minute history of AI.
- Best: notdwd-998633, linke1427832-343079.
- **Fit 4** (1929 / 2008 crash, gold history) **/ Feas 4.** Prelinger archival footage is free.

**I. Cinematic Three.js metaphor scenes**:
- agioyaz-986461: a cathedral window gets filled by grey cubes engraved with "busy / efficiency / urgent / deadline", flying in faster and faster until it is dark. One block falls out, a coloured shaft of light enters, then the blocks chain-release into a stained-glass floor projection. Cold achromatic first half, jewel red/blue/gold second half. Mincho text fades in and out. Every 1/30s stepped exactly.
- zeezomb-726206: a glass and gold-leaf mosaic whose tiles lift, flip and click back; figures are flocks of tiles.
- cryptowluha-060792 and mrkindey-267498: a house growing from pencil lines → massing → detail → finished; scrubbable stages, X-ray, explode, section cut.
- llama3dstudio-918962: fried chicken procedure, all procedural.
- Others: eigeorguy (snow globe), curieuxexplorer-272483 (Taj Mahal), sayan-shanky-868515 (inside a data centre), dan-proggg-274533 (pagoda built joint by joint).
- Best: agioyaz-986461, zeezomb-726206, mrkindey-267498, cryptowluha-060792.
- **Fit 4** (gold-leaf mosaic for gold, house build-up for rent and mortgage costs) **/ Feas 3.** WebGL works headless via `--use-angle=swiftshader` (notdwd-998633), but it is slow.

**J. Character / cartoon storytelling**:
- jackfriks-338762: a 9:16 pig sending love notes, with sound effects and an app tease at the end.
- superalesha-970412: a mouse in a red scarf.
- chrisjdimarco-524106: a procedural samurai doing poses in one spot.
- majidmanzarpour-927543 (pixel wizard rig): parameterized pose (staff angle, arm raise, head tilt, robe sway), quantized to 8–12fps.
- mtvneo-819281: "personify yourself".
- kloss-xyz-941143: 9:16 "brain rot", chaotic.
- Anime battles: ishuagra02-922825, fanfulladev-063524 (Pokémon FireRed-style intro), ryzoft-887481 ("80s/90s cartoon"), rafiroutes-596199.
- Best: jackfriks-338762, superalesha-970412, majidmanzarpour-927543.
- **Fit 5** (Penny-led Shorts) **/ Feas 4.**

**K. Retro pixel art**:
- majidmanzarpour-927543:
  - Logical canvas of 128x96, integer-scaled, `imageSmoothingEnabled=false`.
  - Fixed palette of about 24 hex colours; no anti-aliasing, gradients or shadowBlur.
  - State machine IDLE → CHARGE → CAST (1–2px screen shake) → RECOVER.
  - Particles step through palette indices white → magic colour → dark.
  - 1px rim light from the gem.
- twoclipping-041659 pixel objects:
  - 16x16 hand-placed grid per object, extruded down-right with a bevel and a contact shadow.
  - Pixel morph pairs the cells of object A with the cells of object B.
- Also 0xevinho-436195, aisongman-461057, sciencedegens-843325, flxrnc-251921 (pixel mascot).
- **Fit 3** (good for "video-game economics" or nostalgic price comparisons) **/ Feas 5** in PIL.

**L. Beat-cut SaaS hype reel ("go all out")**: about 30 prompts (0xfemyn, amol909s, astrodevil, melvynx, kmasiff, kingokings, fractadev, julianpscheid, federicoaltepo1, teleboost, humzaakhalid, slvdev, vahidf24, yuyudora, charumitradubey…).
- humzaakhalid-537875 lists the stock toolkit: "motion blur, glow, camera hits, HUD details, seamless transitions, kinetic type, terminal UI, particles, cinematic logo finale", palette #3D40FE.
- charumitradubey-328233 explicitly bans "generic AI visuals, rockets, purple gradients".
- **Fit 2** (the look is too SaaS) **/ Feas 5.** Mine it for transitions, not for style.

**M. Live broadcast / HUD overlay**: abyssalld-602690 is a launch broadcast with "nine cameras, a clock that actually moves, Max-q on the overlay like a real feed".
- **Fit 4** (a "LIVE: market crash" ticker, a gas-pump readout) **/ Feas 4.**

**N. Generative spectacle and games** (low relevance):
- Fireworks and particles: fornyapayzeka-795431, zhang-baoqing-920413.
- Poster breaking its frame: pankajkumar-dev-718609 and sahilvermaai-189237.
- Games: niegramotny-197521, dreyk0o0-165270, arixxbt-292438, 0xsolty-735200, curieuxexplorer-519730 and others.
- **Fit 1–2.** "Poster breaks its frame" could work as a hook for a price tag escaping a receipt.

## 2. REUSABLE TECHNIQUES

- **Pure `seek(t)`**: no timers, no Math.random (use a seeded hash per id and t), no carried state, and `?t=` freezes a frame (flxrnc-251921, notdwd-998633, demonugc-525162). Our `window.frame(t)` already matches this.
- **Closed-form springs, summed per retarget**, so a value that changes target repeatedly stays deterministic (demonugc-525162, verbove-268381). Use damping 0.72 / settle 0.35s for objects and 1.0 / 0.6s for the camera (flxrnc-251921).
- **Camera settles slower than the subject** and starts on the beat (flxrnc-251921).
- **Two-edge spring stretch**: the leading edge rides a faster spring, which makes indicators and coins smear (demonugc-525162).
- **Exponential approach "arrive fast, land soft"**: cover 12–19% of the remaining distance per frame (notdwd-766641).
- **Never a dead hold**: a slow push-in on every hold plus a handheld float (notdwd-766641, twoclipping-041659). Counterpoint: one deliberate 400ms absolute freeze for a punchline (gdgtify-130294).
- **Squash and stretch**: squash on contact, stretch mid-air, real arcs (notdwd-766641). Penny's landings.
- **Motion blur by subframe averaging**: 3–8 subframes per frame (t-1/240, t, t+1/240), blended with ffmpeg `tmix` or numpy (twoclipping-000267, verbove-268381).
- **Beat grid from analysis**: numpy tempo and beat grid calibrated to real kicks; every cut on a downbeat; place each SFX by its *measured peak*, not its file start (twoclipping-000267, demonugc-525162). 120 BPM = 0.5s grid.
- **One still per beat as a contact sheet before the full render**, then critique "like a harsh motion director" and fix the 3 worst problems (notdwd-766641, verbove-268381, niirajrshah-163739, ulyssexbt-205279). This is a QA loop for our pipeline.
- **Object-driven transitions / shared geometry**: chart line → document edge, number → invoice amount, receipt → booking (daniel-haida-636937). Measure element positions at runtime for match cuts (twoclipping-000267).
- **Scene handoff on the exact last frame**: draw the outgoing scene under the transition, and let a flood finish before the next scene starts (twoclipping-041659).
- **Never fade black straight into the accent**: move an accent element between states instead (verbove-268381, flxrnc-251921).
- **Content blur-swap**: 12px blur plus fade over 0.15s, and draw-on starts after the blur-in (flxrnc-251921).
- **Counters that run on the global clock**, so they keep ticking through cutaways; tabular numerals and a fixed unit label; "if a counter freezes, the render is broken" (notdwd-998633). Ideal for the national debt or a price clock.
- **Word-by-word captions**: grey → white over 0.2s on TTS word timestamps, 7 words or fewer, one text layer at a time (notdwd-998633). Typed captions behind a block cursor, key word underlined in red as it is spoken (twoclipping-041659).
- **Film finish pass**: fresh grain per frame, halation, about 0.65x corner vignette, 1px edge-clamped chroma fringe (notdwd-998633). Easy in numpy after PIL.
- **One saturated hero object**: everything else desaturated, and colour arrives on the drop (notdwd-998633). Make Penny's or gold's the only saturated colour.
- **Cold → warm colour arc for the emotional turn**: achromatic grey first, jewel red/blue/gold later (agioyaz-986461).
- **Data-sonification**: one click per bounce or collision, and FFT bars from the real mix (apoorvjain25-945542, rneayan-417829, ulyssexbt-205279).
- **Pixel-sprite pipeline**: logical low resolution, integer scale, fixed palette, pose parameters quantized to 8–12fps, palette-index particle ageing (majidmanzarpour-927543). 3D extruded pixel objects plus a cell-pair morph (twoclipping-041659).
- **Fall-through-a-mask zoom**: scale a silhouette mask on a cubed curve until it fills the frame, with the inner scene zooming less for parallax (twoclipping-041659). Use it to fall into a coin or a piggy bank.
- **Rolling number / word swaps vertically** (flxrnc-251921). Counter "F 000 → F 840" style for prices.
- **Glitch discipline**: 1–2 frames, only on a real cut, always with a click; readable text stays at least 8 clean frames (notdwd-998633).
- **Gotchas**: no `will-change` on camera-scaled text; no opacity or filter on preserve-3d elements, fade the wrapper instead (demonugc-525162, twoclipping-000267).
- **Mixing**: narrator 10–15dB over the music, -18dB duck while speaking, -14 LUFS (notdwd-998633, okazaky-084783).
- **Make the loop seamless** for Shorts replays: last frame = first frame, cursor position and speed included (demonugc-525162, rossaxbt-707651).

## 3. PROMPT PATTERNS

- **Tagged sections `<inputs> <direction> <structure> <build> <gotchas> <start>`**, a shared template (demonugc, flxrnc, rossaxbt, twoclipping x2, notdwd-998633, verbove). It separates taste, timeline, engineering and known pitfalls. Example: "Ask me for the inputs, then show me the state list on the beat grid before you write any code."
- **Numbers instead of adjectives.** Example: "Use hex codes, seconds, damping ratios and pixel sizes instead of adjectives." (flxrnc-251921)
- **Explicit banned lists** do a lot of the quality work. Example: "Banned: shockwave rings, particle bursts, RGB split, camera shake, lens flares, neon glows, grid floors…" (twoclipping-000267). Another: "NOT: cyberpunk, crypto, neon, gaming, generic AI purple" (daniel-haida-636937).
- **Timestamped storyboards with one idea per block.** Examples: "0.00–1.20 BLACK / NAVY. A tiny warm-gold glint appears." (daniel-haida-636937) and "10 bars at 120 BPM, 2 seconds each." (twoclipping-000267)
- **A mandatory visual self-review loop.** Examples: "Show me 5 stills first… critique them like a harsh motion director, fix the 3 worst problems, then render." (notdwd-766641) and "Do not declare success because the code compiles. The deliverable is the FILM." (daniel-haida-636937)
- **Restraint and quality-bar framing.** Examples: "I would rather have 3 extraordinary visual moments than 10 mediocre feature animations." (daniel-haida-636937) and "If the button isn't the most memorable thing in the film, start over." (notdwd-998633)
- One-liners ("go all out", "like it's your showreel") also went viral, but they leave the look to chance and produce generic SaaS reels. For a channel with a consistent brand, use the long structured form.

## 4. TOP 10 FOR COIN THEORY

1. **daniel-haida-636937**: adopt it as the channel's master style guide (navy and gold, Jakarta and Mono, object-driven transitions). Paycheck explainer: "the gross-pay number becomes the first deduction line". All long-video chart segments.
2. **rneayan-417829**: "1 coin = $1B" physics drops for national debt, gold reserves by country, or who owns US stocks, with clinks synced. Hook or Short.
3. **notdwd-766641**: Penny bounce with squash and stretch, plus the "arrive fast, land soft" rules, as the channel intro sting and Shorts opener; "every price is a frame" flipbook of grocery prices by year.
4. **rossaxbt-707651**: a gold dot (Penny) threads every scene and traces a spring graph that overshoots to "+7%/yr". Compound interest / 401(k) explainer and loopable Short.
5. **demonugc-525162 / verbove-268381**: single-shape morph: paycheck pill → tax loader → 401(k) toggle → growth chart → "Deposit received" toast. A 30s Short on "what happens to your paycheck".
6. **twoclipping-041659**: paper, red and yellow with pixel objects on a turning ring (the coin flips with sparks). "What $100 buys in 1990 vs 2026" hook; typed captions with the key word underlined in red.
7. **notdwd-998633**: archival CRT cold open, counters ticking every frame, word-by-word captions, film grain. Stock-crash episodes (1929/1987/2008) and gold history; one saturated gold object.
8. **michaelzsguo-782312 + superalesha-970412**: multi-medium storybook (sand, torn paper, chalk) for long-form history segments: history of the dollar, inflation since 1913, Penny's story arc.
9. **agioyaz-986461**: words like "rent / subscriptions / interest" fly in and block a window until it goes dark, then removing one lets gold light in. Emotional outro on budgeting and debt payoff; a cold-to-gold colour arc. Do it in 2D to stay feasible.
10. **mrkindey-267498 / cryptowluha-060792**: a house builds in stages (sketch → frame → systems → finished) with each layer labelled by its cost share. Rent vs. buy and "where your mortgage payment goes"; explode or X-ray for hidden costs.

Honorable mentions:
- konstantinsaifo-501736: a "take apart" cutaway; follow a dollar through a 401(k).
- abyssalld-602690: a live-broadcast HUD for a market-crash "live feed".
- gdgtify-130294: field-reactive typography for hook lines such as "We were told to wait".
- ldataengineer-823010: analogy-led hooks ("Would you board a plane with a 10% crash risk?" maps to "would you buy a stock with…").
