# Chunk 3 findings (139 prompts) — for Coin Theory

Note on the data: about 60% of the prompts in this chunk are one-liners or tweet captions ("make a slick video for X, go all out", "Opus built this game"). They tell us only the genre. The useful craft is in roughly 15 long, structured prompts (heyiamnick, morse/sanjeevn72, twoclipping, ultimaxbt, gdgtify, tanabe-fragm, agioyaz, jake11moran, kopert0x, woojinrad, stokebuilder, l3d1c, iamtanzil, eric-khun, groundcontrol). Several files are cut off mid-prompt in the source data (heyiamnick, gdgtify, byaiden-vu, koldo2k, op7418, artless101, jasondainter, johncodunayo).

Ratings: **Fit** = how well it suits money explainers; **Feas** = how practical it is in our stack (frame-deterministic PIL/SVG/Canvas/Three.js via Playwright, offline, no paid assets). Both are 1-5.

---

## 1. STYLE FAMILIES

### A. Beat-grid kinetic typography / "one-take morph" showreel
**Look:** Flat 2D graphics where one line or shape keeps turning into the next thing (text, then a shape, a chart, a gear, a dashboard). There are no cuts, and something happens on every beat.
**Techniques:**
- Timing: 120 BPM with "something happens on every beat". Moves start 0.05 s before their beat so they land on it. 15 bars of 2 s each.
- Easing: a critically damped spring, `1-(1+wt)e^(-wt)` with w = 12–40, so nothing passes its target. Exponential ease-in/out for wipes.
- Scene changes: a hard-edged shape floods the frame, or a single horizontal scan line wipes it.
- The last frame equals the first, so it loops.
- Corner labels such as "FIG. 07 — GEAR" and "BEAT 27/60".
- Counters roll up ("120 BPM, 60 BEATS, 1800 FRAMES, 0 CUTS").
- A bar chart whose baseline bends into a ring.
- Type: Geist only, weight 900 for big words and 600–800 for labels at 24–28 px, tracked 0.14–0.3 em.
- Palette: cream #EDE6D5, blueprint #1B3ED2, cyan #45F0DD, black #07080A, graphite #16161A.
- Safe margin: nothing at rest within 150 px of the sides or 90 px of the top and bottom.
- tanabe-fragm adds:
  - zero constant-speed motion
  - overlapping scene moves
  - a 0.3–0.5 s "tame" (wind-up) before each highlight
  - "every paused frame must work as a still"
  - at most 3–4 colours and 2 typefaces
  - a storyboard table in 0.5 s steps
**Best:** heyiamnick-119558, tanabe-fragm-706979, gdgtify-393073, lukasersil-726495.
**Tech:** Canvas/SVG, closed-form springs.
**Fit 5 / Feas 5.** This is our whole grammar for charts and stat reveals.

### B. Mechanism-as-explanation ("kinetic proof", diagram machine)
**Look:** An engraved or industrial machine whose moving parts *are* the argument: number wheels, belts, division gates, ramps.
**Techniques (gdgtify):**
- Palette: porcelain #F0EEE6, graphite #222522, industrial green #416B53, warning orange #E78636.
- Type: tabular monospace for all calculations, a heavy geometric grotesque for claims, a small technical serif for the conclusion.
- Rolling numerals only while something moves, then a sharp settle.
- One orange unit enters and changes 30030 to 30031, and that is "the decisive visual event".
- Six results laid out side by side so they can be compared at once.
- "Every mechanical action must correspond to an operation."
- LOCKED COPY plus a timed storyboard.
**Related:** adrianduta96 (a Rube-Goldberg music machine where every sound matches a visible movement, in ink black, cobalt and sunflower yellow); aimevzulari (Galileo's brachistochrone race in Canvas: straight ramp vs. circle vs. cycloid); drake5112 (network effects: "5x users = 27x connections" with a slider and narration).
**Best:** gdgtify-393073, adrianduta96-992248, aimevzulari-256293, drake5112-661428.
**Fit 5 / Feas 5.** Compound interest, inflation, 401(k) matching and tax brackets map directly onto this.

### C. Seamless product-launch / UI-morph film
**Look:** A warm white or gray canvas with black UI. One element morphs through states; a cursor clicks and drags; the camera pushes into whatever matters.
**Techniques:**
- morse/sanjeevn72:
  - one shape, never cut, morphing size, radius and colour; content swaps with a short blur
  - the two edges of the tab indicator ride different springs, so the leading edge stretches ahead
  - drags compute the value from the cursor and spring back on release
  - a camera zoom so each state fills the frame
  - banned: bouncy easing, particle bursts, glows, gradients on UI chrome
- ultimaxbt:
  - palette #f5f5f2 / #0e0e10 / lime #cdf24f / orange #ff6a2a / blue #2f6bff
  - an iridescent conic-gradient glow
  - one camera transform keyed by [t, zoom, x, y], with zoom interpolated in **log space**
  - "never zoom in and out consecutively"
  - shared-element handoffs: a lime flood carries the bubble's words; a button grows into the page
  - text rises from a mask line
- jake11moran: camera moves of 1.5–3 s on gentle ease-in-out, "half the speed you'd default to", plus motion blur and light film grain.
- khlaseek: a card scales from 30% to 100% while fading in, details slide in one after another, the graph line draws as a path, and a back glow rises.
**Best:** ultimaxbt-549714, morse-369333, jake11moran-414633, khlaseek-dsgner-877659.
**Tech:** HTML/CSS computed in `seek(t)`.
**Fit 4 / Feas 5.** Use it for "your banking app / 401(k) dashboard" segments.

### D. Loud poster / sticker collage / halftone
**Look:** Bold colour blocks, an op-art sunburst, die-cut stickers with white borders, stamps, tickets and grain. It has internet-brutalist energy.
**Techniques (twoclipping):**
- Palette: cobalt #2B3BFF, ink #0E0F1F, cream #F6E4C6, pink #FF7DC7, tangerine #FF5A1F.
- Type: Archivo 900 extra-condensed for names; Geist Mono for labels.
- The camera never stops: a slow 1.03–1.07 push on every scene.
- Nothing pops in; letters rise through a mask line.
- Patterns rotate continuously, not one notch per beat (that reads as stutter).
- Carousel glides of about 0.55 s; colour fades of about 0.35 s.
- A "NOW CASTING" stamp presses down on a beat; a ticket stub tears off; a MATCH % counts up.
- A sticker border made by dilating the alpha; a 3D box built from orthographic affine-mapped faces.
**Related:** stokebuilder (typewriter-tape labels, hand-drawn marks, halftone/manga print, a shared "style bible + component kit" for 50 inserts); anjmaxx (K-pop lyric typography, big text while the background is quiet, characters on the right and lyrics on the left).
**Best:** twoclipping-551116, stokebuilder-356793, anjmaxx-459455.
**Fit 4 / Feas 4.** Works for receipts, price tags, coupon stamps and a "SALE" sunburst on grocery or inflation hooks.

### E. Hand-drawn pencil / crayon / coloured-pencil storybook
**Look:** Paper grain, wobbly graphite lines, hatching fills, watercolour washes, and a warm, human feel.
**Techniques:**
- heyiamnick's paper ink:
  - resample lines and push them off true with slow sines whose phase changes 8×/s (the boil)
  - stroke twice: full width at 90%, then half width at 40% with more wobble
  - knock paper tooth out of the strokes, then multiply onto the paper
  - fills are diagonal hatching drawn one line at a time; big type is hatching clipped to the letter shapes
  - a 60 px blue grid at 13%, with every fifth line at 26%
- groundcontrol: a pencil style with "a little tasteful chromatic aberration" and pastiche, used for real weather data.
- woojinrad: 1080×1350 at 24 fps, 3 ideas each with a caption taken from the text, one simple original character, storyboard first.
- kopert0x: crayon and watercolour; one timeline drives the music and the picture; every note lights a city window.
- eric-khun: a fixed character spec (silhouette, ears, eye rings, chest mark), fast cuts and zooms, bilingual text.
- byaiden-vu: minimal black ink on cream, a monoline stickman inside a battery icon, a red drain line as the villain.
- dan-riverbendai: a one-line sketch drawn in real time, pastel, an old film look.
**Best:** heyiamnick-119558 (paper stage), woojinrad-455731, kopert0x-098349, byaiden-vu-755862.
**Tech:** Canvas 2D (it ports to PIL easily).
**Fit 5 / Feas 5.** It's warm, cheap to render and fits Penny well.

### F. Mascot / character comedy shorts
**Look:** A simple, characterful lead (box robot, stickman, felt blob, cat, moose) living inside a UI or object.
**Techniques:**
- heyiamnick's box mascot: body 76×54 units, arm stubs 24×16, legs 11×33, tall rounded eyes 8×14. It runs with alternate leg pairs, 6 steps/s, leaning 7°. It holds a pencil, takes the current ink's colour and is "never a fourth colour".
- jakubantowski felt blob: fuzzy felt, breathing, blinking, squash & stretch, a lagging beret (secondary motion), a subtle reaction to the cursor.
- flxrnc: a tiny film set, a live monitor, a slow blink into the lens.
- byaiden-vu: the antagonist is a UI element (the battery-drain line).
- jasondainter: stick figures who start as friends and escalate into a fight.
**Best:** jakubantowski-020905, byaiden-vu-755862, heyiamnick-119558, flxrnc-619627.
**Fit 5 / Feas 5.** Penny versus a villain UI element: the inflation line, the overdraft fee, the gas price sign.

### G. Powers-of-ten continuous zoom
**Look:** One unbroken dolly from the macro scale to the micro scale (desk, then CPU, then atom; or hillside, then universe), with a scale ruler on screen.
**Techniques:**
- acoramaa: "one continuous shot, no cuts" and a ruler on the right tracking scale from about 1 m down to about 2 nm.
- adomicael: a path from a phone through fibre and a data centre to a transistor, and back.
- aidinzeo: a self-similar zoom that loops at 300,000×.
**Best:** acoramaa-053577, kgonia7-746268, adomicael-707503, victortaelin-875778.
**Tech:** Three.js.
**Fit 4 / Feas 3.** Good for "follow your $5 latte" or "where your paycheck goes" (zoom from the payslip into tax, FICA, 401(k)). In 2D it can be done with nested scaled scenes in log-space zoom.

### H. 3D cutaway / exploded view / X-ray
**Look:** A realistic object you can take apart: parts slide out with labels, an X-ray reveals the insides.
**Techniques:**
- aichrislee: an Explode button where every part slides apart along an axis with a name label; hover lights a part and shows one line on what it does.
- techartist: staged construction (foundation, skeleton, systems, envelope, finished) plus an X-ray of plumbing and power.
- iamtanzil: a radial-gradient mask spotlight revealing the X-ray image under the exterior (radius 165, feather 45, `cubic-bezier(.16,1,.3,1)` word pull-up with a 0.08 s stagger).
- bthreeagency: a badge treated as a solid 3D object, with a gold-particle celebration, "fast and smooth, not bouncy".
- konstantinsaifo: a slider drives the plasma from 15M to 150M °C and a city lights up.
**Best:** aichrislee-938609, techartist-021472, iamtanzil-120030, konstantinsaifo-587629.
**Fit 5 / Feas 4.** Explode a house to show where rent goes (mortgage, tax, insurance, profit), a gas price breakdown, or a gold bar.

### I. Cinematic 3D light-and-metaphor film
**Look:** Moody 3D and volumetric light carrying an emotional metaphor.
**Techniques (agioyaz):**
- 1080×1920 at 30 fps, 37 s.
- Grey cubes engraved with words (BUSY, URGENT, KPI…) fly in faster and faster and seal a window.
- Total darkness and silence for 3 s.
- One block falls and dissolves into sparks; a single golden beam enters.
- The camera spirals up.
- Elegant serif lines fade quietly.
- Synthesized audio: an accelerating clock, a thud per block, then silence, then one bell, then a choir pad.
**Related:** itsolelehmann (four seasons outside a train window, "Grand Budapest Hotel style"); nathanwilbanks (fire whose sound is derived from per-frame brightness).
**Best:** agioyaz-397647, itsolelehmann-762215.
**Fit 3 / Feas 3.** Good as a Short emotional arc: bills sealing the window, one cancelled subscription, light returns.

### J. Data map / timeline history
**Look:** A light-theme map with moving agents, or neon year stamps on a timeline.
**Techniques:**
- milos-gis: a light theme; overview, then zoom into each quadrant; slow the animation when zoomed without stretching the total length.
- rpa-dake: neon years spring in with a 3D rotation and "slam" down, while SVG line art is added for each year's event. Their thesis: "history pacing is decided by the gaps between slammed scenes, not the amount of information".
- retropunkai: the architecture builds from a minimal shell to the finished venue.
- kewai: "talk-show wit + data-viz expert + director".
**Best:** rpa-dake-593915, milos-gis-317580, groundcontrol-230877.
**Fit 5 / Feas 5.** A history of gold, a timeline of stock crashes, a map of rent by city.

### K. Claymation / stop-motion look
**Look:** Clay or felt materials animated "on twos" (each pose held for 2 frames), with steam and a looping prop.
**Best:** wikiwayne-080350, wikiwayne-486055, nikolajankovic-616097, jakubantowski-020905.
**Tech:** Three.js (or Blender).
**Fit 4 / Feas 3.** Three.js with a matte material, noise displacement and stepped time (`t = floor(t*12)/12`) gives the look cheaply.

### L. Shader / demoscene / psychedelic abstract
Examples: monokern, gandamu, demitiyageekzen (a full WebGL2 sky, Karplus-Strong guzheng synthesis), argbeknwn, rneayan (oscilloscope), buildfastwithai-844291 (128 BPM audio-reactive ring), aidinzeo (Mandelbrot).
**Fit 2 / Feas 3.** Only useful as a transition flourish or a "market crash" glitch.

### M. Games / interactive playables
Examples: 0xchuckstock, hellovyom, kepochnik, itsjdraven, lisp-mi, codrops (arcade), agentgamesbot (pixel), boona11, mayuresh, smallhusk, mycodecoach (battle royale HUD), op7418 (gacha reward reveal).
**Fit 2 / Feas 2.** Exceptions:
- op7418's "loot-box / rank-up reward reveal" is a great *gag format* for "your raise arrived… it's 3%".
- mycodecoach's HUD elements (timer, players alive) could frame a "budget survival" bit.

### N. Prompt-only "go all out" product promos
Examples: robvjourney, roundtablespace, bizibeast, rammanq (AllInvestView, a finance product), meetarno, lepadev, wozu, sudo-kiran ×2, majorbaguette, cansincengiz, fumiyamizuguchi, ezshine, thegawdstiles, gonzalomacagno, maxalexweber, micheleharmonic, utsavchopra, plus Remotion/HyperFrames posts by allodev, t4k1ra, saxxyweb3, seri-nonnon, petert, bridgemindai, l3d1c, rishit30g, itsahmedharoon.
There is no style spec, so they're only informative as evidence that "showreel energy" prompts get attention. l3d1c's process notes are gold (see section 2).

---

## 2. REUSABLE TECHNIQUES

**Motion and easing**
- **Closed-form critically damped spring** `1-(1+wt)e^(-wt)`, w = 12–40, for every settle. Retargeting means summing one spring per target change, so it stays a pure function of t (heyiamnick, morse).
- **Two-edge spring stretch:** the leading and trailing edges of a highlight bar or pill ride different springs, so it stretches ahead like liquid. Use it for a progress bar or a "you are here" marker on a chart (morse).
- **Rolling digits only while moving, then a hard settle on the final value.** Count-ups for prices and percentages, using tabular monospace (gdgtify, twoclipping MATCH %, heyiamnick counters).
- **One decisive accent event:** a single unit in the warning colour (#E78636) changes the number. For example, "+$1" or "+0.25%" becomes the climax (gdgtify).
- **Anticipation / "tame":** a 0.3–0.5 s wind-up before every highlight; no constant-speed motion; overlap scene exits and entrances (tanabe-fragm).
- **Text rises through a mask line, letter by letter;** nothing "pops in" (twoclipping, ultimaxbt). Word pull-up: translateY 20 px, opacity 0→1, `cubic-bezier(.16,1,.3,1)`, 0.6 s, 0.08 s stagger (iamtanzil).
- **Secondary motion on the mascot:** a lagging hat/beret, breathing, blinks, squash & stretch on landing; run cycle at 6 steps/s with a 7° lean (jakubantowski, heyiamnick).

**Camera**
- **Single camera transform keyed [t, zoom, x, y], zoom interpolated in log space.** One eased move per scene, never in-then-out back to back, no reversing direction (ultimaxbt).
- **Constant slow push of 1.03–1.07 on every scene,** so the frame is never dead (twoclipping).
- **Slow cinematic moves of 1.5–3 s,** "half the speed you'd default to", with motion blur and film grain (jake11moran).
- **Locked "drafting-table" camera:** objects move, the camera never does. Use it for chart-heavy segments to keep them readable (heyiamnick).

**Transitions**
- **Shared-element handoffs:** a button grows into the next page, a colour floods out of an object and shrinks into another, a disc morphs into a phone. Do this inside the same camera transform or it jumps (ultimaxbt, twoclipping).
- **Hard-edged shape flood or a single scan-line wipe** between scenes instead of crossfades (heyiamnick).
- **Each stage's accent colour becomes the next stage's base** (blue pencil on paper, then blueprint blue), so colour carries continuity (heyiamnick).
- **Last frame = first frame** for looping Shorts, including cursor position and speed (morse, heyiamnick, twoclipping).

**Texture and look**
- **Pencil boil:** sine wobble with its phase stepped 8×/s, a double stroke (90% / 40%), paper-tooth knockout, multiply blend (heyiamnick).
- **Hatching fills drawn one line at a time;** hatching clipped to letter shapes for big numbers (heyiamnick).
- **Tasteful chromatic aberration plus pencil** (groundcontrol); **light film grain** (jake11moran, twoclipping).
- **Die-cut stickers:** dilate the alpha to get a white border, add a soft shadow, then a slow sway after they land (twoclipping).
- **Hologram ink:** scan-line fills on an 8 px pitch whose thickness follows how lit the surface is, and no blur halo (heyiamnick).
- **Iridescent conic-gradient glow** around the focus element, as an "AI magic" cue (ultimaxbt).
- **Stop-motion "on twos":** quantize time to 12 fps for the character while the camera stays smooth (wikiwayne).
- **X-ray spotlight mask:** a radial-gradient mask reveals the "inside" layer (iamtanzil). Use it to reveal hidden fees on a bill.

**Rendering and QA**
- **Motion blur via subframes:** render 4–8 subframes per frame and blend them with ffmpeg `tmix`. Use 8 for whips (morse, twoclipping, ultimaxbt).
- **Counters read the frame's time, not the subframe's** (twoclipping).
- **No `will-change` on anything the camera scales,** or text goes blurry (morse).
- **A pattern rotating one notch per beat reads as stutter:** rotate it continuously and pick speeds that loop cleanly (twoclipping).
- **A flood circle that has filled the screen should become a full-frame rect** (twoclipping).
- **Contact-sheet QA:** render about 20 stills tiled into one image before any video; render one frame per beat; scan for single-frame pops; measure "hard jumps per second" against a reference (l3d1c, morse, twoclipping).
- **Captions measured in the real font and shrunk to fit the 9:16 safe zone** so nothing hides under the TikTok/Shorts UI (l3d1c).
- **One codebase producing 30 s, 15 s and 6 s cuts in 16:9 and 9:16** as different scene lists (l3d1c).

**Sound**
- **120 BPM grid:** cuts land on the beat. Analyse the music with numpy and place every SFX by its measured peak; loudnorm to -14 LUFS (l3d1c, morse, twoclipping).
- **Every sound matches a visible movement:** 12 s of silence, then the machine plays (adrianduta96).
- **Silence before the reveal** (agioyaz, 11–14 s). **Per-frame data drives the sound,** e.g. fire brightness drives the crackle (nathanwilbanks). This could become a cash-register tick on each counter step.
- **Web Audio synthesis:** chord progression Am–F–C–G; each note lights a window (kopert0x); Karplus-Strong plucks (demitiyageekzen).

**Editorial**
- **Locked copy and a "never invent numbers" rule;** sync graphics to spoken words; leave breathing room between inserts (stokebuilder, gdgtify).
- **"Do not claim X" logic guardrails** in the prompt (gdgtify). This is critical for money accuracy.
- **Write a style bible and component kit first,** so 50 inserts look like one show (stokebuilder).

---

## 3. PROMPT PATTERNS

- **XML-ish sections: `<inputs> <direction> <structure> <build> <gotchas> <start>`.** The best prompts (morse, twoclipping, ultimaxbt, heyiamnick) separate taste, timeline, engineering and known pitfalls. Example: *"Every style is computed from time inside seek(t): no CSS transitions, no timers, no state carried between frames."*
- **Explicit Banned list.** It kills template looks more reliably than adjectives. Example: *"Banned: particle bursts, glows, lens flares, camera shake, RGB split, crossfades, generic gradients, bouncy easing…"*
- **A one-line concept, then a beat- or second-indexed storyboard.** Example: *"one pencil line gets promoted three times (graphite on paper, wire on a blueprint, light on black) and never leaves the screen."*
- **Exact numbers for everything:** hex codes, px sizes, spring constants, BPM, beat indices, durations. Example: *"Moves start 0.05 s before their beat so they land on it."*
- **Locked copy plus logic and fact guardrails.** Example: *"Do not claim that multiplying primes and adding one always produces a prime."* and *"Never invent facts, numbers or quotes."*
- **Self-review loop and staged approval.** Example: *"show me the beat map and 6 stills… before you render"*; *"Render one frame per beat before the full render. Fix anything off the grid."*

Vague "go all out / best of the best" prompts (sudo-kiran, robvjourney) gave no transferable craft. Specificity, not hype, is what drove quality.

---

## 4. TOP 10 FOR COIN THEORY

1. **heyiamnick-119558.** Our master style. Pencil-on-paper Penny segments, then a "blueprint" ink for the mechanics of a 401(k) or paycheck. Spring easing, a 120 BPM grid, a bar chart that bends into a ring. Use it for long-video chapter explainers and charts.
2. **gdgtify-393073.** A "kinetic proof" machine for compound interest or inflation. Wheels multiply 1.07ⁿ, a single orange "+1%" is the decisive event, tabular counters. Explainer core; also a looping Short.
3. **ultimaxbt-549714.** A one-take UI film with a log-space camera and shared-element handoffs. A "your banking app" scene (paycheck lands, then splits into rent, groceries and 401(k)). Mid-video explainer.
4. **twoclipping-551116.** A loud poster/sticker style with stamps and tickets. Grocery receipt hook: price stickers slap on, a "PRICE HIKE" stamp presses on the beat, a % counter. Hook / Short.
5. **byaiden-vu-755862.** Ink-on-cream stickman inside a battery icon fighting the drain line. Restyle as Penny inside a gas gauge or bank-balance bar fighting the red "inflation" line. A looping 9:16 Short.
6. **aichrislee-938609 + techartist-021472.** Exploded or staged house with labels. "Where your rent actually goes": a house explodes into mortgage, property tax, insurance, maintenance and landlord margin; an X-ray of a gas pump price. Explainer centrepiece.
7. **woojinrad-455731.** A 25 s coloured-pencil storybook with 3 ideas, captions taken from the text and one character, storyboard first. A template for turning an article into a Short (for example "3 things the Fed rate cut means for you").
8. **rpa-dake-593915.** Neon years spring-slam onto a timeline while line art is drawn. Gold price history, a timeline of stock crashes (1929, 1987, 2000, 2008, 2020). Chart/history segment.
9. **agioyaz-397647.** Words on blocks seal the light, then silence, then one block falls and a golden beam enters. Restyle with subscriptions or debt blocks (NETFLIX, OVERDRAFT FEE, BNPL…) sealing a window; cancel one and gold light floods in. Emotional Short or outro.
10. **acoramaa-053577 (with adomicael-707503).** A continuous zoom with a scale ruler. "Follow one dollar": zoom from the grocery receipt line into the egg carton, farm, feed and fuel cost, with a cost ruler instead of a length ruler. Hook for grocery-price videos.

**Honourable mentions:**
- jakubantowski-020905: secondary motion for Penny (breathing, blinks, a lagging hat).
- tanabe-fragm-706979: a QA checklist to paste into every prompt.
- l3d1c-632524: the multi-cut, 9:16 safe-zone and contact-sheet pipeline.
- op7418-021491: a gacha "reward reveal" gag for a 3% raise.
- drake5112-661428: a network-effect slider recast as "how fast compound interest grows".
