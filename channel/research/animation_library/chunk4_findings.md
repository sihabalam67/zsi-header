# Chunk 4 findings (140 prompts, 0xcodez → zigapoto)

Caveat: about 45% of this chunk is just the author's tweet ("go all out", "made with Remotion"), and a few files are cut off in the source (pradeepxkapoor, humzaakhalid, tkz-aiart, gkxspace, johnmckeownn, shengtang). The craft detail comes from about 20 long prompts: dzhohola/hicallmechai/okapi/thegrootdev (one family), twoclipping, everestchris6, ik-builds, tanabe-fragm, dotey, astrothewizard, mochi-agi, thewevr, 0xcodez, wangyinrec.

Ratings: **Fit** = how well it suits Coin Theory money explainers; **Feas** = how feasible it is in our stack (frame-deterministic PIL/SVG/Canvas/Three.js via Playwright, offline, no paid assets). Both are 1-5.

## 1. STYLE FAMILIES

**A. Paper / marker "handmade" motion graphics**: a warm paper canvas, ink-black kinetic type, marker notes that draw themselves on, hard switches between light and dark.
- Techniques: "paper-light canvas, marker notes that draw on, real physics, huge kinetic type, hard light/dark switches, a new idea every 1.5–2 s, a sound on every hit". Kinetic type in Anton; handwriting in Caveat, drawn with stroke-dashoffset. 4-token palette (canvas/ink/accent1/accent2). Dark mode is a charcoal that matches the palette. Squash/stretch, onion skin, smear frames, follow-through. "One primary move per transition; no generic push/slide". The music drops out on the dark switch and slams back on the logo (ik-builds). "Efficient code-drawn textures if expensive watercolor effects make rendering impractical" (thewevr). Paper cut-out shadow theatre, 9:16, audio made in code (x4b47x).
- Best: ik-builds-585923, x4b47x-034026, thewevr-681887, helloshiva0801-438284
- Tech: GSAP/HyperFrames, SVG, Canvas. **Fit 5 / Feas 5.** This is the best house style for Penny: cheap, warm, and readable.

**B. Kinetic-type SaaS launch / "showreel" motion graphics**: big words, cursor, UI cards, beat-cut, Apple-ish.
- Techniques: 128 BPM, 8 bars, one bar per section (1.875 s), "every move lands on the beat" (ai9app). 12–15 compositions per 30 s, each lasting 1.4–3.5 s. Frame one is a finished picture. Big words enter from opposite sides and reveal the next scene (everestchris6). GSAP card timings: 280 ms cards, 220 ms title, 160 ms metadata, 60 ms stagger, with Playwright frame-stepping to catch overshoot (fleyta88). The 15-second arc "started → what I did → numbers that grew → what's still missing → one line on what's next" (lemcosmos).
- Best: everestchris6-399895, ai9app-989009, fleyta88-443662, lemcosmos-535145. The many "go all out" clones (ceowinkz, gouthamjay8, hsanat, techtactician, miskinho) add no technique.
- Tech: GSAP/Remotion, SVG/CSS. **Fit 4 / Feas 5.** Use it for hooks, stat slams and the "3 reasons" sections.

**C. Single-shape UI morph (Dribbble loop)**: one element never cuts and morphs from button to loader to player to slider to chart to toast. Warm-gray canvas, black and white plus one accent, a cursor drives everything.
- Techniques: Geist font. "Springs everywhere, a tiny overshoot at most". Closed-form spring step responses, summed per target change so the motion stays a pure function of t. The two edges of the tab indicator ride different springs so the leading edge stretches. Direct-manipulation drags that spring back from the release point. Beat grid from numpy at 120 BPM over 7 bars. 4 subframes per frame blended with ffmpeg tmix for motion blur. Last frame equals first frame. The nightshift variant (twoclipping): every morph glides 0.8 s on cubic-bezier(.45,0,.15,1) and the camera zoom rides the same curve. iOS glass (a pre-blurred photo clipped to the shape, then a tint and a gradient rim). Goo split/merge (blur plus alpha threshold). An iris opening through the period of the wordmark. A clock chip 11:42 PM → 6:59 AM. A counter to 200/200. "$48,200 counts up, the line draws."
- Best: twoclipping-747965, dzhohola-249003 (= hicallmechai, okapi-fukugyo), thegrootdev-966114 (Poké Ball morph)
- Tech: Canvas/DOM with seek(t). **Fit 4 / Feas 4.** Ideal for "your paycheck, beat by beat": a coin morphs into a pay stub, then a tax slice, then a 401(k) bar.

**D. Storybook character explainer (Kurzgesagt / Pixar-lite)**: a personified protagonist, gags, real numbers, burned-in captions.
- Techniques: "Give the photon a personality". "One strong formal idea per scene". Simulate the real thing ("random walk should be an actual random walk"). Real numbers, honest about uncertainty. Onomatopoeia, callbacks, a parallel timeline ("what was happening on Earth"). Music changes per scene and ducks under the VO. SFX on every bounce, pop, whoosh and ding. Captions because people watch sound-off (astrothewizard). A STORYBOARD.md listing time, picture, text and transition per scene, plus free local TTS (henrygsing). Rig lesson from doubleunplussed: a jittery mouth circle reads as a bug, so use expressions instead of fake lip-sync, and avoid hand-to-face poses that look like errors.
- Best: astrothewizard-618782, henrygsing-050247, kamstudiolabs-877996, doubleunplussed-181894
- Tech: Canvas. **Fit 5 / Feas 4.** This is Penny's long-form backbone.

**E. Hand-drawn crayon / whiteboard / painting-by-cursor**
- Techniques: "Crayon texture on every surface: grainy strokes, wobbly outlines, paper tooth". "One timeline drives both" music and picture. Lights and camera follow the music. `?t=90` to jump anywhere (0xcodez). A whiteboard explainer drawn by hand (tak3sh8). A replay of a cursor painting the picture stroke by stroke (ehsanik).
- Best: 0xcodez-474136, tak3sh8-441895, ehsanik-162993
- Tech: Canvas 2D. **Fit 4 / Feas 5.** Whiteboard math works for APR and compound interest.

**F. Real-object process / "recipe" explainer**: ingredients physically go in, with measurements labelled as they land.
- Techniques: White Russian from empty glass to finished drink, each ingredient and measurement shown as it goes in, 30 s (sarut0bisasuke). Simulated everyday spending at the grocery store, gas station and restaurant, 9:16, JS + Playwright + FFmpeg only (felipemoller). Trucks, forklifts and chutes in a watchable warehouse sim (konstantinsaifo). An F1 pit stop with an 8-person crew (rubenssoto).
- Best: felipemoller-936736, sarut0bisasuke-069973, konstantinsaifo-169107
- Tech: Canvas/SVG (Three.js for the pit stop). **Fit 5 / Feas 5.** Shows a pay stub or grocery cart being "assembled".

**G. Infinite zoom / scale dive**
- Techniques: a fingertip to atoms, 1× → 1,000,000×, in one HTML file (curieuxexplorer). A data center → server → card → transistor → silicon atom (btc5887899, mdaman010).
- Best: curieuxexplorer-408141, btc5887899-288258
- Tech: Canvas/Three.js. **Fit 4 / Feas 4.** Hook idea: zoom into a $6 latte receipt down to the 11¢ of coffee beans.

**H. 3D exploded / turntable product**
- Techniques: the Explode button slides every part apart with its own label, and hovering lights up a part with one line on its job (aichrislee). A turbofan with a short caption for each stage (0xspikez). everestchris6 3D rules: camera between 35 and 55°, a soft key light from one side plus a rim light behind, labels as HTML positioned from the 3D scene every frame, measured background pixels matched to the brand colour, "no floating parts…no flat black glass".
- Best: aichrislee-922082, 0xspikez-483865, eyadnour-172216 (QR repair explainer)
- Tech: Three.js. **Fit 3 / Feas 3.** Good for an exploded credit card chip, a gold bar assay, or an ATM.

**I. 3D cinematic diorama / world**
- Techniques: a tile mosaic of about 190k instanced tiles that resolves into the ad's final frame. A hard sun from the top left. A homemade bokeh DOF whose aperture closes over time. Letter tiles start in the background colour and then flip left to right. Never put the overhead camera exactly vertical (tanabe-fragm). Also a Ghibli sunset dogfight (nft-chen), a procedural manor with a day/night window switch (thusatharan), and Middle-earth (earthwalkerx17).
- Best: tanabe-fragm-322001, thusatharan-433543, nft-chen-350878
- **Fit 2–3 / Feas 2–3.** Too heavy, except the mosaic reveal idea: coins tiling into a $ figure.

**J. Retro pixel / 8-bit / perler bead**
- Techniques: "Compound Interest QUEST". Impulse spending is a trap to jump over, inflation is a monster that chases you, and the stat that levels up is patience. 8-bit music (0xpai-eth). "Hand-drawn character animation from a top-tier 16-bit studio, not scaled-down vector" (gkxspace). Perler beads with holes, ironed into white-bordered stickers on graph paper, karaoke subs (hahazwei). Another World polygon style with data under 250 KB (gandamu).
- Best: 0xpai-eth-635565, gkxspace-923139, hahazwei-425483, pluginplay-472343
- Tech: Canvas pixel. **Fit 4 / Feas 5.** Great for Shorts and gamified savings.

**K. Period / cultural illustration chronicle**: era-specific art styles carry a history timeline.
- Techniques: two styles alternate, line art on rice paper and gold on black. Each scroll has one main colour plus a motif that evolves by era. One big calligraphic keyword per shot. A HUD with a red seal (top left), the dynasty name set vertically (right), and a scroll ruler plus year counter (bottom). Seal-stamp and drum-hit transitions between scrolls. BPM speeds up with the era. "Lock the beat grid and the shot list before rendering" (dotey). A rotating Greek vase tells the story as the vase turns (perezalexa23). A Renaissance naturalist's manuscript with a MIDI score written in Python (recorder theme, harpsichord random walk that gets denser each bar, 2 s bars) and FluidSynth for the sound (wangyinrec). Also risograph (rneayan), comic book (madpencil), sumi-e (pradeepxkapoor).
- Best: dotey-927166, perezalexa23-414045, wangyinrec-532344
- Tech: Canvas/SVG. **Fit 5 / Feas 4.** "History of money": shells → coins → paper → gold standard → Bitcoin, each era with its own art style.

**L. Data/timeline "story of X"**
- Techniques: monetary history driven by real Bitcoin block data (bradmillscan). "bang, bang, boom, whoa" capability progression (nummanali). Twitter → X in 30 s (tejasthange3). A learning curve with milestone captions, "Game 1: dies at 128 … Game 98,299" (redp314). A 7-minute repo explainer with chapters (what, map, life of a query, abstractions, real trace) (deedydas).
- Best: bradmillscan-839974, deedydas-407965, redp314-642106
- **Fit 5 / Feas 5.** The chapter template maps straight onto 8–10 min videos.

**M. Listicle slideshow synced to TTS (yukkuri / 2ch style)**
- Techniques: 5 structured items, each fact checked against the official help pages, images drawn in code, scenes switched to the second against the voice (claudecode-ut).
- **Fit 4 / Feas 5.** "5 grocery tricks" format.

**N. 2.5D parallax stills plus expressive subtitles (horror)**
- Techniques: 9 stills given depth in Three.js with a camera move. Whisper subtitles typed one character at a time, set vertically. Shouted subtitles shake harder the louder the line. VO acting tags like [whispering] (mochi-agi).
- **Fit 3 / Feas 4.** Useful as a dread sting for a "stock crash" cold open.

**O. Beat-synced music video / lyric type** (abhinavflac, davidshulmanfl, aijipusi with per-character lyric timing, anabology): **Fit 2 / Feas 3.** Borrow only the lyric-type ideas.

## 2. REUSABLE TECHNIQUES
- Pure-function frames: no clock, timers or unseeded RNG. Seam check: compare frame 0 with frame N pixel by pixel. A smoke test with 6 yes/no defect gates, including "text on text" (0xkarmi-129839).
- Closed-form springs summed per target change, so seek(t) stays pure (dzhohola-249003).
- Two-edge springs: the leading edge stretches ahead of the trailing edge on a sliding pill or highlight. Use it on a "budget category" tab (dzhohola-249003).
- Motion blur: 4 subframes per frame, blended with ffmpeg tmix (dzhohola, twoclipping). Counters must read the frame's t, not the subframe's, "or the digits smear" (twoclipping-747965).
- Ease a closing iris by area, not radius. A helper that sets globalAlpha must restore it. Never zoom the camera into an off-centre dot; open it instead (twoclipping-747965).
- Goo split/merge via blur plus alpha threshold: one result orb splits into 3 pills (twoclipping). Use it for a paycheck splitting into tax / rent / savings.
- Time-of-day clock chip plus a sky that relights from night to dawn, for "while you sleep" compounding (twoclipping).
- Count-up money figure while the line draws, with a hover tooltip following the line (twoclipping).
- One table of beat times drives every morph, "so retiming is one edit" (twoclipping). Analyze the beat grid with numpy, start on a downbeat, place SFX at measured peaks (dzhohola).
- The 120/128 BPM grid: one section per bar (1.875 s at 128 BPM), something happens on every beat (ai9app, dzhohola).
- "The thing in front becomes the transition": a title moves toward the camera while the next scene waits underneath. A carried object lands on the same pixels on both sides of a cut (everestchris6-399895).
- "Things land slowly enough to read, leave fast". Cut only when size, direction and subject match on both sides. Vary scale: close, wide, overhead, full-frame type (everestchris6).
- Quality metrics: no more than about 1 s of frozen screen per 30 s, no still longer than about 0.5 s, text contrast ≥ 4.5:1, nothing flies through other text (everestchris6).
- Handwriting via stroke-dashoffset in Caveat. Kinetic type in Anton. Smear frames and onion skin on fast moves (ik-builds-585923).
- Music arrangement as punctuation: the drums drop out while an object is airborne and slam back on the type and logo. Master to -14 LUFS / -2 dBTP, re-measured after the AAC encode (ik-builds).
- Seal-stamp impact transition plus a drum hit between chapters. A persistent HUD with a year counter and a timeline ruler (dotey-927166). Use it for "1971: Nixon closes the gold window".
- The BPM rises as the timeline approaches the present (dotey). Use it for inflation acceleration.
- Expressive subtitles: whispers appear one character at a time, shouts shake in proportion (mochi-agi-421448). Use it for "your rent… went up AGAIN".
- Crayon texture: grainy strokes, wobbly outlines and paper tooth on every surface (0xcodez-474136). One timeline drives audio and picture, and the page supports `?t=` seek.
- Simulate, don't depict: a real random walk, real numbers, honest uncertainty, onomatopoeia and callbacks (astrothewizard-618782). Use it for a real Monte Carlo of 401(k) outcomes.
- Mosaic reveal: tiles start in the background colour, the text tiles flip in last from left to right, and SFX get quieter with camera distance and merge into "rain" as the count grows (tanabe-fragm-322001).
- Labels as HTML/2D overlay projected from 3D each frame, never as text inside the 3D scene. Key light plus rim light (everestchris6).
- Explode toggle: parts slide apart with name labels and snap back (aichrislee-922082). Use it to explode a paycheck or a gas price into its components.
- Render one still per beat (or 6 key stills) before the full render, then contact sheets every 0.2 s around transitions (dzhohola, twoclipping, everestchris6).
- Python-written MIDI score (chords plus two leitmotifs) rendered with FluidSynth and a free GM soundfont, then loudnorm (wangyinrec-532344). This gives us zero-cost original music.

## 3. PROMPT PATTERNS
- **XML-sectioned briefs** (`<inputs> <direction> <structure> <build> <gotchas> <start>`). This is the most-copied format in the chunk (4 remixes). "Ask me for the inputs, then show me the state list on the beat grid before you write any code." (dzhohola)
- **A banned list next to the positive direction.** "Banned: bouncy easing, particle bursts, glows, gradients on UI chrome, mismatched icon strokes, dead time, anything that looks like a template." (dzhohola)
- **A numeric beat structure with an exact chain of states**: "120 BPM, 7 bars, something happens on every beat. Button → loader → check → dynamic island…" Timed seconds tables work too: "0〜3 one dark tile on the floor, camera skimming the floor" (tanabe-fragm).
- **Truth constraints.** "Nothing made up: every number and label on screen comes from the recordings." (bilimfili1) "facts file… is the only source for any number, name or claim" (everestchris6). Essential for money content.
- **A gotchas section with hard-won bugs**: "Counters read the frame's time, not the subframe's, or the digits smear." (twoclipping)
- **A quality bar plus an autonomous verification loop**: "Build verification loops: render stills of every scene and review them critically… Don't hand me a first draft." (astrothewizard) Also "the builder never judges its own work" (everestchris6).
- (Weak pattern) "Go all out / showreel for your CV" one-liners are everywhere but give no reusable direction. The specific briefs are the ones worth copying.

## 4. TOP 10 FOR COIN THEORY
1. **felipemoller-936736**: a 9:16 simulation of everyday spending at the grocery store, gas station and restaurant. Use it directly for Shorts on grocery and gas prices, with a running total ticker.
2. **0xpai-eth-635565**: Compound Interest QUEST, in pixel style. Use it for a 401(k)/compound-interest Short or a long-form interlude where an inflation monster chases Penny and impulse buys are pits.
3. **twoclipping-747965**: a morph/goo split, clock chip, count-up and line draw. Use it for the explainer segment "what happens to your paycheck overnight" (deposit → split into tax/rent/401(k) → morning balance).
4. **sarut0bisasuke-069973**: a pour-in recipe with measurements. Use it for an explainer on "the recipe of a $4.29 gallon of gas" or a paycheck: crude, refining, tax and margin pour into the glass with labelled amounts.
5. **astrothewizard-618782**: a storybook character with real numbers, gags and captions. Use it as the master brief template for 8–10 min Penny explainers (rent, gold).
6. **dotey-927166**: an era-styled chronicle with a year-counter HUD and stamp transitions. Use it for "History of the dollar / gold standard" long-form chapters.
7. **ik-builds-585923**: a paper canvas with marker notes and Anton kinetic type. Use it as the house style kit for hooks, chapter cards and Short intros.
8. **curieuxexplorer-408141**: an infinite zoom. Use it as the hook "zoom into your $7 burrito until you find the 18¢ the farmer gets".
9. **x4b47x-034026**: paper cut-out shadow theatre, 9:16 with code audio, on "what makes a place feel like home". Use it as an emotional rent/housing Short or a long-form outro.
10. **everestchris6-399895**: a production system (storyboard table, motion principles, facts file, critic loop, measured quality bar). Use it as the QA and prompting spec for every video. Not a look on its own.

Runners-up: dzhohola-249003 (a coin-morph channel bumper), bradmillscan-839974 (real-data monetary history), mochi-agi-421448 (a stock-crash cold open), tanabe-fragm-322001 (coins tiling into a price reveal).
