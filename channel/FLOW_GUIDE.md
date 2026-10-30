# Google Flow: how we use it (owner makes, Claude finishes)

The owner has Google AI Pro and makes images and video clips in Google Flow (labs.google/flow) from prompts Claude
writes. Claude never logs into the owner's Google account; the owner sends the files in the chat and Claude adds
narration, numbers, captions, Penny, sound and checks. Every Flow asset is logged in assets/photos/SOURCES.md.

## What Claude asks for, per long video (one brief, sent the day the video is planned)
- 2 thumbnail images, two different scenarios (usually: a fictional reaction face, and a dramatic object/scene).
- 1-3 clips of 1-10 s for the moments that matter most: the opening hook (always), a big reveal, the ending.
- Optional, for big stories: a 20-60 s "cinematic sequence" built by extending clips (see Extend below).
Per Short: only when a real-looking scene beats our animation (news, disasters, heists); vertical 9:16.

## The modes the owner uses (names can shift slightly in Flow's menus)
1. Text to Video: paste the prompt, pick 16:9 (long videos) or 9:16 (Shorts), generate, pick the best take.
2. Frames to Video: upload a start image (and optionally an end image) so the clip starts/ends exactly there.
   Use it to start a clip from a thumbnail image so the video and thumbnail match.
3. Ingredients to Video: upload reference images (e.g. assets/brand/penny_ref.png) so a character or object looks
   the same in every clip. Use it whenever Penny appears in a Flow clip.
4. Extend (in Scenebuilder): continue a clip from its last frame with a new prompt, 8 s at a time. Chain 2-6 of
   these for a seamless 16-48 s sequence. Download each piece (or the whole scene) and send them in order.

## Prompt rules Claude follows
- Always end with: no text, no letters, no numbers, no logos, no brand names, no real or famous people.
- Say the aspect ratio, camera move, lighting, mood, colours, and where empty space for text must be.
- Fictional people only, never anyone real; no logos (Flow draws them badly and trademarks are a risk).
- For chained clips: one prompt per 8 s piece, each starting with "Continue the same shot:" and describing only
  what changes, so the scene stays consistent.

## How Claude uses the files
- Images: thumbkit.Thumb.photo(...) adds text, Penny, glow, outline; squint test at phone size.
- Clips: a scene with bg_video=path (or a list of paths, played back to back) and bg_speed (slow motion so the
  clip covers the narration; the camera keeps pushing so nothing freezes). The clip's own audio is never used.
  16:9 clips in Shorts are centre-cropped to fill 9:16, never stretched.
- YouTube disclosure: every upload is marked "altered or synthetic content" (realistic AI scenes require it).

## If assets don't arrive in time
Claude builds the scene with our own animation and a thumbnail from public-domain photos, so a launch never slips.
