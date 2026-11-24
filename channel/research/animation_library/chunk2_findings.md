# Chunk 2 findings: 140 prompts, adapted for Coin Theory

About 45% of these prompts are short tweets that just say "Opus 5.5 + Remotion" or one-liners like "go all out" (e.g. 0xlangeai, alex-leiro, ambiguous-ai, goldiez2599, sudo-kiran, zheke, xamfonos). They give almost no craft signal. All of the useful craft detail sits in about 20 long prompts: techhalla-498547, gdgtify-989608, twoclipping-402193, twoclipping-762046, 0xnicc0-516612, op7418-814408, koushikde-937635, howdevelop-733090, nft-chen-068069, zacxbt-944604, egeberkina-949521, froessell-562325, zhu185178-255661, oab10don-457273 and the aichrislee series.

Fit and Feasibility scores are on a 1-5 scale.

---

## 1. STYLE FAMILIES

### A. One-shape spring-morph UI ("one continuous take")
- **Look:** a single rounded rectangle morphs from a button into a loader, a player, a chart and a toast. It sits on a warm off-white stage, a cursor drives every change, there are no cuts, and the last frame equals the first.
- **Palette and fonts:** stage #f3f3f0 to #e3e3de, app world #121212, one accent (#1ed760). Geist or Inter. Soft layered shadows that grow with the shape's height.
- **Motion:** closed-form spring step responses, "a tiny overshoot at most". Morphs glide 0.8 s on cubic-bezier(.45,0,.15,1), and the camera zoom rides the same curve. Content dissolves in the back half of each glide.
- **Beat:** 120 BPM, "something happens on every beat", 7 bars = 28 beats = 14 s.
- **Craft details:**
  - The two edges of a tab indicator ride different springs, so the leading edge stretches ahead.
  - The volume slider rubber-bands past max.
  - Text inside a morph gets its own clip and its own enter/exit timing.
- **Banned:** crossfades, gradients on UI, particles, glows.
- **Best examples:** twoclipping-402193, twoclipping-762046, 0xnicc0-516612, yankis0x-174321 (sanjeevn72-151834 is a truncated copy).
- **Tech:** single HTML, seek(t), Playwright, 4 subframes blended with ffmpeg tmix.
- **Fit 4 / Feasibility 5.** It is perfect for a "banking app" segment: a paycheck pill splits into tax, 401(k) and rent chips, then the balance chart draws itself. It matches our window.frame(t) pipeline exactly.

### B. Poster-style kinetic typography / bumper
- **Look:** a street poster that moves. Huge condensed type slams onto a strict 3-colour palette, with print misregistration on impact frames.
- **techhalla-498547 palette:** bg #0A0A0A, magenta #FF2BD6, acid green #B8FF00, white #F5F5F5.
- **techhalla-498547 fonts:** Archivo Black for display (tracking −40 to −80), Syne ExtraBold for secondary lines, IBM Plex Mono for the 18-character "crumbs".
- **techhalla-498547 motion:**
  - Per-glyph spring on y, opacity and blur, staggered by 1/16 note (125 ms at 120 BPM).
  - A seeded Fisher–Yates letter scramble that snaps onto the beat.
  - A mask wipe that uses the outgoing word's outlines.
  - Camera limited to a punch-in (1.0→1.08) and smash-pans on beats.
  - Micro-breath on the final hold (scale 1.000→1.012→1.000).
- **gdgtify-989608 (JFK film):**
  - Palette: midnight #080D23, warm white #FFF4DD, coral #FF654F, blue #6685FF.
  - Type: a grotesque, plus an italic for the emphasised word.
  - Holds: 700 ms reading holds. "No word may begin its ornamental travel before its reading hold finishes."
  - Text height: active text at least 64 px in a 1080 frame.
  - Camera: only three moves (pullback, roll, velocity match), "each with a rhetorical purpose".
  - Curves: arc-length sampling.
- **nft-chen-068069 #13:** 120 BPM, one word per beat, orange on black, and "the last hammer" line.
- **Best examples:** techhalla-498547, gdgtify-989608, koushikde-937635, nft-chen-068069.
- **Tech:** Canvas/SVG, seek(t).
- **Fit 5 / Feasibility 5.** Use it for hooks ("YOUR RENT ISN'T HIGH / YOUR PAYCHECK IS LOW"), stat slams and Short openers.

### C. Generic "showreel / SaaS launch" motion graphics
- **Look:** a dark graphite canvas with luminous gradients, UI fragments, kinetic code and fast cuts.
- **What the prompts asked for:** "hook in the first second", "every transition should visually demonstrate a feature" (howdevelop-733090), "break screenshots into components/icons so we can animate those" (ho-ba-761062), and the story must "work muted".
- **howdevelop-733090 details:**
  - 9:16-safe central area inside a 16:9 frame.
  - Second-by-second sequence with on-screen copy for each beat.
  - Accuracy guardrails.
  - "Inspect the rendered result and fix clipped text."
- **Examples:** howdevelop-733090, ho-ba-761062, reflex-cloud-304046, jhylee95-452427, plus about 30 vague ones (deeprajo1, essjaykay755, prasenx, onewaysidewalks…).
- **Fit 3 / Feasibility 5.** The look is generic. Borrow only the safe-area rule and the "transition = demonstration" rule.

### D. Interactive 3D exploded-view / cutaway
- **Look:** a realistic object (heart, lens, watch, jet engine, phone, cannon). The camera orbits, an Explode button slides every part apart along an axis, and each part gets a name label with a dashed leader line. Hovering a part highlights it and shows one line about what it does.
- **Template sentence:** "the parts you never get to see … Explode button … every part slides apart … snaps back together."
- **thebuggeddev-482912** adds live orthographic "technical drawings".
- **Best examples:** aichrislee-476025 (watch), aichrislee-479847 (jet engine), nft-chen-068069 #6 (phone), thebuggeddev-482912.
- **Tech:** Three.js with procedural geometry and no assets.
- **Fit 4 / Feasibility 4.** Candidates: "what's inside a credit card / ATM / gas pump / gold bar assay". Drive the explode with t instead of a click.

### E. Cinematic science / data simulation
- **Look:** an "Apple-quality interactive science visualization turned into a cinematic motion-design video".
- **egeberkina-949521 (earthquake):** a cross-section where stress builds, stress zones glow and a live seismograph reacts. Then the fault slips, waves radiate, and the camera cuts up to a shaking city and back down for the aftershocks. "Reveal something new every few seconds." Minimal type and dynamic labels.
- **Related:** haribuilds-007643 (Point Nemo data story), thesethian-384517 (one-shot flight through five future "stops"), kisaka-ki-859326 (debris deposition map).
- **nft-chen-068069 recipes:**
  - #3 scale comparison: true radii, smooth pull-out, punchline number.
  - #11 Kurzgesagt-style paper fold: "big numbers, thickness ×2, camera zooms regularly until the end".
- **Fit 5 / Feasibility 4.** A stock crash works as an earthquake (pressure builds, slip, aftershocks). Compound interest works as the paper fold. Inflation works as a scale comparison.

### F. Hand-drawn / doodle / storybook / collage / paper
- **Look:** marker or crayon lines that wobble (line boil), paper grain, warm and narrative, minimal text.
- **nft-chen-068069 #4 whiteboard:** black marker drawn stroke by stroke, red only for the key point, satisfaction particles that "grow bigger each time".
- **nft-chen-068069 #8 picture book:** crayon line plus pencil fill, jittering lines, the tail swinging to the beat, paper texture.
- **nft-chen-068069 #10 antique map:** parchment, faint ink roads, a vermilion route drawn in one stroke with distance labels, ending in a seal stamp.
- **nft-chen-068069 #1 coloured shadow puppets:** warm backlight and jointed puppets.
- **Others:**
  - songkeys-384673: origami/doodle, "no spoken language … poetic".
  - n01ennn-597182: a hand-drawn agent story that ends on heart eyes and a green check.
  - tomandrieu96707-875264: whimsical hand-drawn collage.
  - x7mdnet-157811: Vox-style with Canvas-generated paper textures.
  - nofollowers2023-974928: paper cut-out characters.
- **Best examples:** nft-chen-068069, songkeys-384673, n01ennn-597182, tomandrieu96707-875264.
- **Tech:** Canvas/SVG.
- **Fit 5 / Feasibility 4.** This is the natural home for Penny, e.g. a storybook "history of money" or an antique-map gold route.

### G. Cartoon game "reward reveal" (juice)
- **Source:** op7418-814408, the richest craft prompt in the chunk.
- **Look:**
  - Saturated toon shading (MeshToonMaterial with a 3-4 step ramp).
  - A uniform dark outline #1A1033 from post-process normal+depth edge detection, not the inverted-hull trick.
  - Chubby titles in Titan One / Lilita One with black stroke and drop shadow, slammed in letter by letter with rebound.
  - The colour tier upgrades green → blue → purple → gold.
- **Five-phase choreography:**
  1. Idle bob with a periodic "tap me" shake.
  2. Upgrade: the object jumps, spins, and squashes on landing.
  3. Charge (~1 s): shaking intensifies, light leaks from the seams, particles suck inward, pitch rises, then a final squash.
  4. Burst: additive bloom ≤0.8, screen shake, camera push, triple-stroke shockwaves (wide/faint, medium, thin/bright), coins and gems, confetti used only once.
  5. Reveal: cards fly out on an arc and land with overshoot, numbers roll up with "▲+value", and coins fly along Bézier curves into the top-right balance, which bumps on each arrival.
- **Light rules:** god-rays are 5-7 blurred beams in a fan. The background uses conic gradients with 2-3 layers at different speeds. The glow sits behind the hero and never in front of it.
- **froessell-562325 "camera juice":** a tiny shake on light hits, a 50-100 ms hit-stop on big ones, a zoom impulse on pile-ups, never continuous shaking. Every impact combines physics + particles + audio + camera + score popup.
- **Fit 5 / Feasibility 4.** Coins flying into a balance is literally our domain: 401(k) match unlocks, tax refund chest, paycheck day.

### H. Retro pixel / 16-bit
- **zacxbt-944604 recipe:**
  - 128×96 logical canvas, integer upscale, imageSmoothingEnabled = false.
  - Fixed 24-colour palette.
  - Procedural sprite built from rects.
  - Pose parameters eased, then quantised to an 8-12 fps feel.
  - 1-2 px screen shake.
  - Particles step through palette indices (white → magic colour → dark).
  - 1 px rim light from the light source.
- **Other examples:** nft-chen-068069 #7 (16-bit idiom with hard cuts every ~1.6 s), hoyoyoda-543147 (Chuseok pixel scene), plus the pixel games opener-ai, dmowlin, rehan-shei, waseemkhalo and tonnusos.
- **Fit 3 / Feasibility 5.** Use it for "1980 vs today prices" flashbacks, an "8-bit Penny" Short, or a "level up your credit score" bit.

### I. Beat-synced machines / music visualisers
- **Examples:**
  - kamstudiolabs-440893: "every note comes from a visible collision".
  - gorden-sun-797351: a ball falls through a 3D scene, bounces, lights objects on the beat, "with humour".
  - riyadbkhsh-300736: 605 billboards lighting up on the beat.
  - oab10don-457273:
    - BPM measured as 137.
    - Every dip lands within ±0.5 frame of the kick.
    - Material swaps on the downbeat (chrome → gold → hologram → voxel).
    - A final hit freezes everyone.
  - acoramaa-248467: the kick opens plates, bass pushes the lens, and the eye goes quiet in the breakdown before blowing open on the drop.
  - iniyanai-856596: real switch clicks used as the beat.
- **Fit 3 / Feasibility 4.** A Plinko of coins showing "where $100 of your paycheck goes" makes a great Short.

### J. Math / flat infographic / isometric flow / timeline
- **nft-chen-068069 recipes:**
  - #9 3Blue1Brown: dark ground, a circle cut into 8/16/32 sectors that are really rearranged into a rectangle, formula built term by term.
  - #2 isometric 2.5D parcel-sorting flow: numbered step labels, two lines merging into one, "clean, followable".
  - #12 flat MG: pure-colour geometry, no strokes, two-tone lighting.
  - #15 horizontal timeline: the camera pushes along the axis, nodes scale and light up, big year plus one line.
- **Others:** eleanorina-653042 (Manim, 3b1b explainer with TTS), goofyninjaaa-315331 (2D floor plan synced with a 3D room, collision warnings).
- **Fit 5 / Feasibility 5.** These are our core explainer segments: isometric "how a grocery price is built" supply chain, a timeline of gold prices, and 3b1b-style "why 7% doubles in 10 years".

### K. Step-by-step recipe with live counters
- **Examples:** ror-fly-880547 (empty glass to finished cocktail, ingredients and measurements animate in as they pour), n01ennn-597182 (Haiku White Russian: "live counters and a checklist"), retropunkai-277590 (history of the Sphere from bare architecture to finished venue).
- **Fit 5 / Feasibility 5.** Use it for a grocery cart or receipt that builds item by item while the total counts up, or for building a paycheck.

### L. Cinematic 3D worlds / dioramas
- **Examples:**
  - alexalbert-274839: 1906 Market St, every building traced to a source.
  - mdaman010-610173: procedural Middle-earth with an orchestral score.
  - filicroval-168898: voxel capybara.
  - truenyl-447745: BotW look.
  - ishuagra02-678129: particle-speck illustration with ribbon motion strokes.
  - youwareai-300653: castle above clouds.
  - blitast-studio-257328: the whole thing is ~200 KB.
- **Fit 2-3 / Feasibility 3.** Voxel or particle cities could suit "rent in 5 cities" B-roll, but they cost a lot of effort.

### M. Character shorts from code
- **Examples:**
  - gmgmgm1545-245507: a mechanical hermit crab chases a light and finds it was in its own claw all along (a twist ending).
  - uinerd-635877: the last "Prost!" as the lights go out.
  - generussai-904308: "adult-swim cartoon, quick cuts, cute but badass characters".
  - nemtudo-614053: "make a funny video".
  - supremebeme-306746: brainrot.
  - henkpoley-761980: a deliberately terrible reel (anti-pattern humour).
- **Fit 4 / Feasibility 4.** These are Penny mini-stories built on twist structure.

### N. Other textures
- **Examples:**
  - johnsavage-ai-427263: film grain + CRT retro-futurism.
  - nft-chen-068069 #14: B/W manga panels with halftone and one red, hard cuts between panels.
  - akakuma0219-658335: found-tape handheld POV horror.
  - zhu185178-255661: 2.5D anime previz. It relies on AI images and Real-ESRGAN, so it is not feasible for us, but its compositor ideas are: depth parallax, bokeh, rack focus, light bands sweeping a face, "on twos" pose timing.
- **Comic panels: Fit 4 / Feasibility 5.** Use them for "the day the market crashed" in red-accent manga.

### O. Narrated pipeline / Shorts factory
- **Examples:**
  - tetsu-tetsu333-576886: TTS split into 32 phrases so captions and UI appear the instant they are spoken; BGM ducks under the voice.
  - tarunyadav9761-053244: word-level kinetic captions, 3D perspective tilts plus springs.
  - jiro-aicompany-487818: "top 5" Shorts; the script is structured into 5 items with headings, facts are checked against official docs, and each item's image is drawn in code and switched to the second to match the voice length.
  - signalz-jp-918002: ffmpeg check against YouTube specs before upload.
  - palashbagchi11-389221: landscape and portrait versions from one source.
- **Fit 5 / Feasibility 5.** This is a process template for our TTS videos.

---

## 2. REUSABLE TECHNIQUES

### Determinism and rendering
- **Pure seek(t):** every frame is a pure function of time. No CSS transitions or timers, deterministic out-of-order seeks, and window.frame(n) for n = 0…N at t = n/60. (gdgtify-989608, techhalla-498547, yankis0x-174321)
- **Stacked closed-form springs:** a value that changes target many times is the sum of one closed-form spring per change, so it stays pure. (0xnicc0-516612, twoclipping-402193)
- **Motion blur:** render 4 subframes per frame and blend them with ffmpeg tmix. 14 s × 60 fps × 4 = 3,360 renders. (techhalla-498547, yankis0x-174321)
- **Arc-length sampling:** gives even spacing along curves. Blend position and tangent continuously when leaving a path, with no teleport. (gdgtify-989608)
- **Separate transforms:** keep the camera transform separate from glyph orientation. Counter-rotate the active phrase during a camera roll so it stays readable. (gdgtify-989608)
- **Typing from time:** characters shown = floor(progress × length), and the caret blinks only when idle. (0xnicc0-516612)
- **Seeded randomness only:** seeded letter scramble (Fisher–Yates per glyph) that snaps on the beat, and no runtime randomness. (techhalla-498547)

### Beat and audio
- **Beat grid:** 120 BPM, downbeat at t = 0, something on every beat for the first 16 beats and every other beat after. Measure beats with numpy and place each click or chime on its measured peak. (techhalla-498547, twoclipping-402193)
- **Loudness:** loudnorm to −14 LUFS and encode H.264 at CRF 16. (0xnicc0-516612)
- **Quiet intro, hard drop:** put the key "press" on the drop. (twoclipping-762046, kisalay-921896: "Quiet sadness for four seconds. Then the drop.")
- **Ducking:** lower the BGM under the voice, and split the TTS into phrases so on-screen text appears the instant each phrase is spoken. (tetsu-tetsu333-576886)

### Timing and pacing
- **Reading holds:** a 700 ms hold before decorative motion starts, and the final composition held completely still for 1.2 s. (gdgtify-989608)
- **One gesture per scene:** each gesture physically carries the camera into the next world, with no holds longer than 1 s. (twoclipping-762046)
- **Loop seam:** last frame = first frame, including cursor position and speed. (0xnicc0-516612, twoclipping-402193)
- **Steady reveals:** reveal something new every few seconds, and build pressure before the release. (egeberkina-949521)

### Camera
- **Limited moves:** punch-in 1.0→1.08 plus smash-pans on beats only, never random drift. Alternatively, three camera moves, each with a purpose. (techhalla-498547, gdgtify-989608)
- **Camera juice:** small shake on light hits, a 50-100 ms hit-stop freeze on big ones, a zoom impulse on the climax, never continuous shake. (froessell-562325)
- **Speed through spacing:** show acceleration by widening the spacing between trailing marks, not by shaking. (gdgtify-989608)

### Motion feel
- **Squash and stretch:** jump, spin, then squash on landing and rebound. During charge, shaking grows, particles are sucked in and pitch rises, then a final squash before the burst. (op7418-814408)
- **Number count-ups:** numbers roll up, then a "▲+value" pops. Reward cards fly out on an arc and land with overshoot and a wobble. (op7418-814408)
- **Coins into a balance:** coins fly along Bézier curves into a balance counter that bumps on each arrival. (op7418-814408) This is our signature move.
- **Two-spring edges:** the leading and trailing edges of an indicator ride different springs, so it stretches. The slider rubber-bands past max. (twoclipping-402193)
- **Swaps inside morphs:** text inside a morphing container gets its own clip and enter/exit timing; swap content with a short blur. (0xnicc0-516612, twoclipping-402193)
- **Per-glyph springs:** spring y, opacity and blur per glyph, staggered by a 1/16 note (125 ms). (techhalla-498547)
- **Mask transitions:** a mask wipe where the outgoing word's outlines reveal the incoming line. (techhalla-498547)
- **Goo dots:** three typing dots split, fly out into chat bubbles, then pour back into the middle one. (twoclipping-762046)
- **Pixel-art timing:** ease the pose parameters, then quantise to an 8-12 fps pixel feel. (zacxbt-944604)
- **Anime timing:** key poses "on twos", plus mesh-warp breathing and hair sway. (zhu185178-255661)

### Look and texture
- **Print misregistration:** duplicate the text layer ±2-4 px in two accent colours at 40% opacity, on impact frames only. (techhalla-498547)
- **Shockwaves and glow:** shockwaves drawn as three strokes (wide/faint, medium, thin/bright). Every spark has a low-alpha halo, and bloom is capped at 0.8 so the frame never whites out. (op7418-814408)
- **Hero lighting:** glow sits behind the hero and only spills from the edges. God-rays are 5-7 blurred beams. Backgrounds layer 2-3 conic gradients rotating at different speeds. (op7418-814408)
- **Toon outlines:** post-process outlines from normal + depth maps. Use a relaxed depth threshold and lean on normals, or diagonal surfaces get hatching artifacts. (op7418-814408)
- **Hand-drawn feel:** jittering crayon lines on paper texture, red used only for the key point, and a "satisfaction particle" that grows larger with each repetition. (nft-chen-068069)
- **Ending stamp:** a seal or stamp as the closing beat, e.g. on the antique map. (nft-chen-068069)
- **Restraint rules:** one accent colour carries every transition. "No corner labels, no fake HUD numbers." (koushikde-937635, 1littlecoder-914649)

### Production QA
- **Stills before the full render:** render one still per beat or per major moment and fix anything cramped, off-grid or low-contrast first. (0xnicc0-516612, techhalla-498547, gdgtify-989608, op7418-814408)
- **Self-check questions:** "Is the hero blocked by glow? Overexposed? Small text legible? Anything still jittering after settle?" (op7418-814408)

---

## 3. PROMPT PATTERNS

- **XML-ish sections.** The best prompts use `<inputs> <direction> <structure> <build> <gotchas> <start>` blocks, and the gotchas encode hard-won bugs. Example: "Text inside a morphing shape needs its own clip and separate enter/exit timing." (0xnicc0-516612)
- **A Banned list as important as the wishes.** Example: "Banned: crossfades, gradients on UI, particles, glows, bouncy easing, dead beats, anything that feels like a template." (0xnicc0-516612) Brand-specific variant: "No rockets, astronaut illustrations, starfield wallpaper, lens flares." (gdgtify-989608)
- **Time-coded storyboard with locked copy.** Each segment carries timestamps, an action and an on-screen line. Example: "0.0–2.5s COLD OPEN — 'STOP SCROLLING' slams in from below with spring overshoot." (techhalla-498547) Also howdevelop-733090 and zhu185178-255661.
- **One central visual metaphor stated as a rule.** Example: "The baseline of the sentence is a trajectory." (gdgtify-989608) And: "One shape tells the whole story." (0xnicc0-516612)
- **Required techniques written as engineering specs.** Example: "implement, don't approximate … Springs = closed-form step responses … Motion blur: render 4 subframes per frame." (techhalla-498547)
- **A built-in quality gate.** Example: "Inspect frames at 0, 3, 5, 7.5, 10.5, 13, 16, and 19 seconds." (gdgtify-989608) And: "inspect the rendered result, and fix any clipped text, weak transitions, mistimed beats." (howdevelop-733090)
- **Stakes framing helps a little.** Example: "Showreel stakes: if this is weak, you don't get hired." (techhalla-498547) The lazy versions ("go all out") produce generic reels.

---

## 4. TOP 10 FOR COIN THEORY

1. **op7418-814408** (reward-chest reveal). Shorts and long-form payoffs: "your 401(k) employer match" or "tax refund" as a loot chest that tiers up green → gold, with coins flying along Béziers into a balance counter. Penny can be the coin.
2. **techhalla-498547** (poster kinetic type). Hook for every long video and the first 3 s of Shorts, e.g. "GROCERIES AREN'T EXPENSIVE / SHRINKFLATION IS", with print misregistration on beats.
3. **twoclipping-402193 / 0xnicc0-516612** (one-shape morph). Paycheck explainer: a gross-pay pill morphs into tax, FICA, 401(k) and health chips, then into a net-pay toast and a bank-app chart. Loopable Short.
4. **egeberkina-949521** (earthquake sim). Stock crash segment: leverage and "stress" build at a fault, the slip is the crash, a seismograph acts as the price chart, and aftershocks follow.
5. **nft-chen-068069 #11** (paper-fold doubling). Compound interest / Rule of 72: big numbers, ×2 on every beat, the camera zooming regularly until the value dwarfs a skyscraper.
6. **ror-fly-880547 + n01ennn-597182 Haiku** (recipe with live counters). Grocery-price explainer: a receipt or cart builds item by item, a running total counts up, and a checklist ticks.
7. **gdgtify-989608** (trajectory typography). Emotional outro or quote card ("Compound interest is the eighth wonder…"), with reading holds, a single camera roll and a still final frame.
8. **nft-chen-068069 #2 + #10** (isometric flow + antique map route). "Why gas costs $4": crude to refinery to truck to pump with numbered step labels and a cost added at each step. Gold's journey from mine to vault on parchment with a vermilion route and a seal stamp.
9. **aichrislee-476025 / nft-chen-068069 #6** (exploded view). "What's actually inside a gold bar, credit card or ATM": layers slide apart along an axis with leader-line labels, driven by t.
10. **froessell-562325** camera-juice spec + **gmgmgm1545-245507** twist story. Penny mini-narratives for Shorts ("Penny chases the dream house… it was in her savings jar all along"), with hit-stop and a light shake on punchlines.

Honourable mentions:
- tetsu-tetsu333-576886 / jiro-aicompany-487818 for the TTS phrase-sync and "top 5" Shorts pipeline.
- zacxbt-944604 for an 8-bit "prices in 1985" flashback.
- nft-chen-068069 #14 for red-accent manga panels about the 2008 crash.
