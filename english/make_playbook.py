"""Builds english/English_Channel_Playbook.pdf: the research and a complete build spec for the English-learning
story channel, written so any LLM with a coding tool can produce the videos with free tools only.

    python3 english/make_playbook.py
"""
import json
import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (KeepTogether, PageBreak, Paragraph, Preformatted, SimpleDocTemplate, Spacer, Table,
                                TableStyle)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'English_Channel_Playbook.pdf')
TEAL = colors.HexColor('#147878')
ORANGE = colors.HexColor('#E87828')

ss = getSampleStyleSheet()
H1 = ParagraphStyle('h1', parent=ss['Heading1'], fontSize=17, textColor=TEAL, spaceBefore=6, spaceAfter=8)
H2 = ParagraphStyle('h2', parent=ss['Heading2'], fontSize=12.5, textColor=colors.HexColor('#263040'), spaceBefore=8,
                    spaceAfter=4)
B = ParagraphStyle('b', parent=ss['BodyText'], fontSize=9.6, leading=13.2, alignment=TA_LEFT, spaceAfter=4)
BL = ParagraphStyle('bl', parent=B, leftIndent=12, bulletIndent=2, spaceAfter=2)
SM = ParagraphStyle('sm', parent=B, fontSize=8.2, leading=10.6)
CELL = ParagraphStyle('cell', parent=B, fontSize=8, leading=10, spaceAfter=0)
CELLB = ParagraphStyle('cellb', parent=CELL, fontName='Helvetica-Bold')
CODE = ParagraphStyle('code', fontName='Courier', fontSize=6.6, leading=8.1, leftIndent=4)
TITLE = ParagraphStyle('t', parent=ss['Title'], fontSize=24, textColor=TEAL, spaceAfter=6)

story = []


def h1(t):
    story.append(Paragraph(t, H1))


def h2(t):
    story.append(Paragraph(t, H2))


def p(t, st=B):
    story.append(Paragraph(t, st))


def bullets(items):
    for it in items:
        story.append(Paragraph(it, BL, bulletText='-'))


def table(rows, widths, head=True):
    data = [[Paragraph(str(c), CELLB if (head and i == 0) else CELL) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1 if head else 0)
    st = [('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#C8C8C8')), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
          ('LEFTPADDING', (0, 0), (-1, -1), 4), ('RIGHTPADDING', (0, 0), (-1, -1), 4),
          ('TOPPADDING', (0, 0), (-1, -1), 2.5), ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5)]
    if head:
        st.append(('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E3F1F1')))
    t.setStyle(TableStyle(st))
    story.append(t)
    story.append(Spacer(1, 6))


def code(text):
    story.append(Preformatted(text, CODE))
    story.append(Spacer(1, 6))


# ------------------------------------------------------------------- cover --
story.append(Spacer(1, 1.2 * inch))
story.append(Paragraph('English-Learning Story Channel', TITLE))
p('<b>Research and complete build specification</b>', ParagraphStyle('s', parent=B, fontSize=14, leading=18))
story.append(Spacer(1, 10))
p('Prepared November 10, 2026. Goal: reach the YouTube Partner Program (monetization) as fast as possible with a '
  'new channel of slow-English listening stories for adult learners.')
p('<b>How to use this document.</b> Give the whole PDF to any AI coding assistant (Claude, ChatGPT, Gemini or '
  'similar) and ask it to follow Sections 6 to 12. Everything uses free tools: Python, Pillow, ffmpeg and an '
  'open-source text-to-speech model. No paid video generator (such as Higgsfield) is needed. Appendix B contains a '
  'complete, working video builder; Appendix C contains a ready prompt for writing new stories.')
story.append(Spacer(1, 14))
table([['Section', 'Contents'],
       ['1', 'Monetization rules (official)'], ['2', 'Why this niche: measured research'],
       ['3', 'Competitor teardown: 8 new channels'], ['4', 'The three winning formats and our choice'],
       ['5', 'Channel identity and audience'], ['6', 'Episode blueprint'], ['7', 'Story-writing rules'],
       ['8', 'Visual specification'], ['9', 'Voice and audio'], ['10', 'Illustrations (free)'],
       ['11', 'Build pipeline'], ['12', 'Titles, descriptions, thumbnails, Shorts'],
       ['13', 'Upload plan, pass marks and 30-day test'], ['14', 'Policy and safety rules'], ['15', 'Sources'],
       ['A-C', 'Story file example, full builder code, story-writing prompt']], [0.7 * inch, 5.6 * inch])
story.append(PageBreak())

# --------------------------------------------------------------- 1. rules --
h1('1. Monetization rules (official)')
p('From YouTube Help, "YouTube Partner Program overview and eligibility" (read November 10, 2026). A channel can '
  'apply for ad revenue sharing when it reaches either threshold:')
bullets(['<b>1,000 subscribers + 4,000 valid public watch hours in the last 12 months</b>, or',
         '<b>1,000 subscribers + 10 million valid public Shorts views in the last 90 days.</b>',
         'Watch hours from Shorts in the Shorts feed do <b>not</b> count toward the 4,000 hours. Only long videos '
         '(and Shorts watched outside the Shorts feed) count.',
         'YouTube notes updated YPP terms starting February 1, 2027; creators must accept them in YouTube Studio by '
         'January 31, 2027. Check the help page again before applying.'])
p('<b>The real risk is the review, not the numbers.</b> Since July 2025 the "repetitious content" rule is called '
  '"inauthentic content": mass-produced, repetitive or templated videos are not eligible for monetization, even when '
  'a channel meets the thresholds. Using AI tools is allowed; what gets refused is content that looks '
  'interchangeable. Every design choice below is made so each episode is clearly original: original stories, '
  'recurring characters, our own art style, and real teaching in every video.')
p('<b>What this means for strategy.</b> 4,000 hours is about 240,000 minutes. A 30-minute lesson watched for 8 '
  'minutes on average reaches that with roughly 30,000 views. That is why this plan is built on long videos (25 to 35 '
  'minutes) with Shorts only as trailers.')

# ------------------------------------------------------------ 2. research --
h1('2. Why this niche: measured research')
p('Most "best niche" articles online are marketing for paid tools. Instead we measured YouTube directly with the '
  'YouTube Data API on November 10, 2026: for each niche, the 50 most-viewed long videos (over 20 minutes) published '
  'in the last 60 days, and how many came from channels <b>under 8 months old</b>. A high count means new channels '
  'can still break in.')
table([['Niche (search term)', 'New-channel videos in top 50', 'Median views of top 50', 'Verdict'],
       ['learn english through story', '25 / 50', '97,307', 'Chosen'],
       ['english listening practice podcast', '15 / 50', '253,693', 'Chosen (same audience)'],
       ['betrayal revenge story', '30 / 50', '224,305', 'No: mostly recaps of copyrighted dramas'],
       ['stoicism philosophy', '25 / 50', '55,149', 'No: templated, high review risk'],
       ['carl jung psychology', '16 / 50', '155,898', 'No: flooded with AI-voice clones'],
       ['how it\'s made factory process', '9 / 50', '452,405', 'No: needs other people\'s footage'],
       ['personal finance explained', '8 / 50', '50,163', 'No: our current channel; weak results'],
       ['history to fall asleep to', '7 / 50', '193,382', 'No: viewers now reject AI narration'],
       ['geography documentary countries', '6 / 12', '22,848', 'No: low demand'],
       ['true crime documentary', '4 / 50', '1,886,013', 'No: closed to new channels, legal risk'],
       ['science to fall asleep to', '3 / 50', '104,227', 'No'],
       ['ai tools tutorial for beginners', '2 / 50', '298,187', 'No: closed to new channels']],
      [2.0 * inch, 1.3 * inch, 1.2 * inch, 2.0 * inch])
p('<b>Why English learning wins for fast monetization:</b>')
bullets(['Half of the top videos come from channels a few months old, so new channels still get recommended.',
         'Viewers watch for a long time on purpose (they are practising listening), which builds watch hours fast.',
         'Learners subscribe to follow a series level by level.',
         'An AI voice is an advantage here: learners want slow, perfectly clear speech.',
         'The audience is worldwide (hundreds of millions of English learners), not one country.',
         'The format (text, one illustration, voice) is cheap to produce with free code.'])

# ---------------------------------------------------------- 3. teardown --
h1('3. Competitor teardown: 8 new channels')
p('Measured from each channel\'s full upload list (YouTube Data API, November 10, 2026). "Long" means 5 minutes or '
  'more.')
table([['Channel', 'Created', 'Subs', 'Long videos / week', 'Median length', 'Median views', 'Format'],
       ['Family Life English', 'Jun 2026', '164,000', '7.0', '45 min', '282,092', '3D cartoon family, A2'],
       ['Henry Daily English', 'Aug 2026', '50,700', '6.2', '45 min', '122,484', '3D cartoon family, A2'],
       ['Family Story English', 'May 2026', '48,000', '3.5', '33 min', '118,751', '3D cartoon family, A1-A2'],
       ['Calm English Story', 'Apr 2026', '68,100', '3.0', '22 min', '12,406', 'Calm listening + shadowing'],
       ['English Speaking Coach II', 'Aug 2026', '19,300', '5.5', '48 min', '13,653', 'Two-host podcast, B1-B2'],
       ['English StoryShow', 'Aug 2026', '6,240', '1.3', '18 min', '27,584', 'Text + one illustration'],
       ['English In Sound', 'Sep 2026', '5,560', '4.8', '22 min', '1,016', 'Talk-style listening'],
       ['Nana English Story', 'Jun 2026', '4,990', '5.3', '32 min', '6,730', '3D cartoon family, A2']],
      [1.35 * inch, 0.6 * inch, 0.6 * inch, 0.75 * inch, 0.7 * inch, 0.7 * inch, 1.6 * inch])
p('<b>What the winners have in common:</b>')
bullets(['A level label everywhere: "A2", "B1-B2", "for beginners".',
         'The words "Slow English" or "English Listening" in every title.',
         'A story hook in the title with a cliffhanger: "Henry Ran Away... Then He Climbed Out the Window!"',
         'Recurring named characters (Henry, Lily, Grace, Leo) so viewers come back.',
         'Long videos (25 to 60 minutes) and frequent uploads (3 to 7 a week).',
         'Bright, emotional thumbnails: a character with a big reaction plus 2 to 5 large words.',
         'Several reached 50,000+ views on one of their first 1 to 15 videos.'])
p('<b>Warning sign.</b> Several 3D-cartoon channels use the <i>same</i> character name ("Henry") and nearly identical '
  'thumbnails. That is exactly the pattern YouTube\'s "inauthentic content" review targets. Our channel must look and '
  'sound like nobody else.')

# ------------------------------------------------------------ 4. formats --
h1('4. The three winning formats and our choice')
table([['', 'A. 3D cartoon family', 'B. Story text + illustration', 'C. Two-host podcast'],
       ['What it looks like', 'Animated-looking 3D kids and parents, emoji titles',
        'The story text on screen, the spoken sentence highlighted, one illustration per chapter',
        'Two illustrated hosts talking about everyday topics'],
       ['Typical length', '30-45 min', '18-35 min', '40-60 min'],
       ['Uploads needed', '4-7 a week', '1-3 a week', '4-6 a week'],
       ['Audience', 'Beginners; looks like kids content', 'Adult beginners A2-B1', 'Intermediate B1-B2'],
       ['Review risk', 'High (identical channels)', 'Low-medium if original', 'Medium'],
       ['Fits free tools', 'Hard (needs many 3D images)', 'Yes', 'Yes (two voices)']],
      [1.1 * inch, 1.75 * inch, 1.85 * inch, 1.8 * inch])
p('<b>Choice: Format B</b>, with two upgrades from Format A that drive views: a story hook with a cliffhanger in '
  'every title, and recurring characters. Later, once the channel grows, add Format C as a second series for B1-B2 '
  'learners.')

# ----------------------------------------------------------- 5. identity --
h1('5. Channel identity and audience')
bullets(['<b>Audience:</b> adults learning English (levels A2 to B1), worldwide. Biggest groups: India, Pakistan, '
         'Bangladesh, Indonesia, Vietnam, Brazil, Mexico, Turkey, the Middle East and Europe. Age 18 to 45.',
         '<b>Promise:</b> "Understand real English by listening to stories about real adult life."',
         '<b>Recurring cast:</b> Maya (27, moved to a new country, works in a cafe), Daniel (her coworker), Mrs. '
         'Patel (the cafe owner), Leo (Maya\'s younger brother, still at home). Real adult problems: jobs, money, '
         'apartments, friendships, family calls, first dates, mistakes at work.',
         '<b>Name ideas</b> (check that the name is free on YouTube before creating): "Maya\'s English Stories", '
         '"Slow English with Maya", "Story English Daily".',
         '<b>Look:</b> warm hand-painted storybook illustrations (gouache style), cream paper background, teal and '
         'orange accents. Nobody else in the niche uses this look.',
         '<b>Set "Made for kids" to NO</b> in YouTube Studio: the audience is adults. Avoid kid-centric plots.'])

# ------------------------------------------------------------- 6. episode --
h1('6. Episode blueprint')
p('Target: 25 to 35 minutes, 3,000 to 4,500 words of story at about 110 to 120 words per minute (slow speech).')
table([['Part', 'Length', 'What happens'],
       ['Opening', '15-25 s', 'Level badge and title. Voice: "Today\'s story is for A2 learners. Listen, read along, '
        'and answer one question at the end." No long intro.'],
       ['Chapters 1-6', '4-5 min each', 'One illustration per chapter. 4 to 6 paragraphs per chapter, 3 to 5 sentences '
        'per paragraph. The sentence being spoken is highlighted; earlier sentences turn grey.'],
       ['Cliffhangers', 'end of each chapter', 'Each chapter ends with a small question or surprise so viewers keep '
        'watching ("But when she opened the box, it was empty.").'],
       ['Key words', '1-2 min', '6 to 10 words or phrases from the story, each with a simple meaning, spoken slowly.'],
       ['Quiz', '30-45 s', '1 to 3 multiple-choice questions, a 3-second pause, then the answer.'],
       ['Ending', '10 s', 'One sentence of recap, a comment prompt ("Write one sentence about your first job in the '
        'comments"), and the next story\'s title.']],
      [1.0 * inch, 1.0 * inch, 4.5 * inch])
p('<b>Why comments matter:</b> asking learners to practise by writing one sentence turns the comment section into '
  'a study tool, which raises engagement and signals an original, interactive channel.')

# -------------------------------------------------------------- 7. writing --
h1('7. Story-writing rules')
bullets(['Use common words only (CEFR A2: about the 1,500 to 2,000 most common English words). Introduce at most 8 '
         'new words per story, and explain each in the Key words section.',
         'Sentences of 6 to 12 words. One idea per sentence. Mostly present simple and past simple.',
         'Write in the first person ("I") for A2 stories; it feels personal and is easy to follow.',
         'Real adult situations with a clear problem, a turning point and a warm ending.',
         'Repeat key words 3 to 5 times across the story so learners hear them in context.',
         'Dialogue in short lines with quotation marks; the narrator says who is speaking.',
         'Never copy existing stories, books, films or characters. Never use real people or brands.',
         'Every story must be different in plot, setting or lesson; no fill-in-the-blank templates.'])
h2('30 starting story ideas (original)')
ideas = ['My First Day at Work in a New Country', 'The Wrong Bus and the Kind Stranger', 'I Lost My Phone on the Train',
         'Renting My First Apartment Alone', 'The Coffee I Made for the Wrong Customer', 'A Phone Call from My Mother',
         'My First Paycheck', 'The Job Interview I Almost Missed', 'Cooking Dinner for My New Friends',
         'The Neighbour Who Never Smiled', 'I Said Yes to Everything for One Week', 'The Day the Cafe Lost Power',
         'Learning to Ride a Bike at Twenty-Seven', 'My Brother Visits Me', 'A Mistake on My First Big Order',
         'The Lost Wallet with a Note Inside', 'My First Snow', 'Saving Money for One Big Dream',
         'The Doctor\'s Appointment in English', 'When My Boss Asked Me to Lead', 'A Weekend Without My Phone',
         'The Old Man and the Library Book', 'I Opened a Bank Account', 'The Birthday Nobody Remembered',
         'Moving Day in the Rain', 'My First Online Date', 'The Fire Alarm at Midnight', 'Teaching My Friend to Cook',
         'A Letter I Wrote to My Future Self', 'One Year in a New Country']
table([[f'{i + 1}. {ideas[i]}', f'{i + 16}. {ideas[i + 15]}'] for i in range(15)], [3.25 * inch, 3.25 * inch],
      head=False)

# --------------------------------------------------------------- 8. visual --
h1('8. Visual specification')
table([['Item', 'Value'],
       ['Video size', '1920 x 1080, 30 fps, H.264 (libx264, CRF 20), AAC 192 kbps'],
       ['Background', 'Cream paper #FAF5EB'],
       ['Text colour', 'Ink #262A34; already-read sentences grey #969696'],
       ['Highlight', 'Current sentence on a rounded yellow bar #FFDD78'],
       ['Accents', 'Teal #147878 (level badge, key words), orange #E87828 (progress bar)'],
       ['Fonts (free, Google Fonts)', 'Story text: Nunito Bold 52 px. Chapter titles: DM Serif Display 62 px. '
        'Labels: Poppins Bold 30-34 px.'],
       ['Layout', 'Top-left: level badge (e.g. "A2") and "SLOW ENGLISH STORY". Below: chapter title. Left column '
        '(1080 px wide): the current paragraph. Right: the chapter illustration, 640 x 800 px, rounded corners 36 px, '
        'white frame and soft shadow. Bottom: a thin progress bar across the full width.'],
       ['Motion', 'The frame changes only when the spoken sentence changes. This keeps rendering fast (a 30-minute '
        'video in minutes) and is easy to read. Optional: a slow 3% zoom on the illustration during each chapter.'],
       ['Key words screen', 'Rows of word and meaning; the row being spoken is highlighted yellow.'],
       ['Quiz screen', 'Question at top, options A/B/C in white rows; the correct one turns green after the pause.']],
      [1.5 * inch, 5.0 * inch])

# ---------------------------------------------------------------- 9. audio --
h1('9. Voice and audio')
bullets(['<b>Free voice:</b> Kokoro TTS (open-source, Apache 2.0), run locally with the <font face="Courier">'
         'kokoro-onnx</font> Python package. Model files: <font face="Courier">kokoro-v1.0.onnx</font> and '
         '<font face="Courier">voices-v1.0.bin</font> from the kokoro-onnx GitHub releases page. Works on CPU.',
         '<b>Recommended voices:</b> af_heart (warm female, US), am_michael (male, US), bf_emma (female, UK). Use one '
         'narrator per series for consistency.',
         '<b>Speed:</b> 0.80 to 0.85 for A2 stories (slower than normal speech), 0.95 for B1-B2.',
         '<b>Pauses:</b> 0.55 s after each sentence, 1.1 s after each paragraph, 0.8 s after chapter titles, 3 s before '
         'a quiz answer.',
         '<b>Generate one sentence at a time.</b> That gives exact timing for highlighting, with no speech-to-text '
         'alignment needed.',
         '<b>Loudness:</b> normalise the final mix to -14 LUFS with ffmpeg <font face="Courier">loudnorm=I=-14:'
         'TP=-1.5:LRA=11</font>.',
         '<b>Music:</b> none, or a very quiet royalty-free bed from the YouTube Audio Library at -30 dB. Learners '
         'prefer a clean voice.',
         '<b>Better voices later:</b> a stronger local model on a GPU computer (for example the open-source '
         'VoiceStudio or Chatterbox) can replace Kokoro without changing anything else.'])

# -------------------------------------------------------------- 10. images --
h1('10. Illustrations (free)')
bullets(['One illustration per chapter (5 to 6 per video), plus one for the thumbnail.',
         '<b>Free options:</b> Canva\'s AI image generator (included with a Canva account), or an open-source model on '
         'a GPU computer (for example FLUX.1 schnell, Apache 2.0, or Stable Diffusion XL) via ComfyUI or the '
         'diffusers Python library.',
         '<b>Keep the characters consistent:</b> write a fixed character description and paste it into every '
         'prompt. Keep the same style words in every prompt.',
         'Portrait shape (4:5), main character in the centre, no text in the image.'])
h2('Prompt template')
code('Warm hand-painted storybook illustration, soft gouache texture, muted teal and warm orange palette.\n'
     '[CHARACTER: A fictional young woman in her late twenties with shoulder-length dark hair, wearing a\n'
     'mustard-yellow coat and a green scarf.] [SCENE: what happens in this chapter, the place, time of day,\n'
     'her emotion.] Vertical composition, the character in the centre. No text, no letters, no numbers,\n'
     'no logos, no brand names, no real or famous people.')

# ------------------------------------------------------------ 11. pipeline --
h1('11. Build pipeline')
p('Install (Python 3.10 or newer, ffmpeg on the PATH):')
code('pip install kokoro-onnx soundfile numpy pillow\n'
     '# download kokoro-v1.0.onnx and voices-v1.0.bin into a models/ folder\n'
     '# download the fonts Nunito, DM Serif Display and Poppins (Google Fonts) into a fonts/ folder')
p('Steps for every episode:')
bullets(['1. Write the story as a JSON file in the format of Appendix A (use the prompt in Appendix C).',
         '2. Check the English level: every sentence 12 words or fewer, new words listed in "words".',
         '3. Make the chapter illustrations (Section 10) and save them as PNG files; put their paths in the JSON.',
         '4. Run the builder in Appendix B with <font face="Courier">--stills</font> and look at the preview images: '
         'no text overflow, the picture fits, the highlight is on the right sentence.',
         '5. Run the builder without <font face="Courier">--stills</font>. It voices every sentence, draws one frame '
         'per sentence, holds each frame for exactly its audio length (ffmpeg concat with durations), and writes '
         'the MP4.',
         '6. Check the MP4: plays to the end without errors, loudness about -14 LUFS, length as planned.',
         '7. Make the thumbnail (Section 12), write the title and description, upload.'])
p('How the builder works: each "beat" is one spoken sentence plus the frame shown while it plays. It builds a list '
  'of beats (chapter title, every sentence, each key word, the quiz), generates the audio for each beat, saves one PNG '
  'per beat, writes an ffmpeg concat list with each PNG\'s duration, and muxes the joined audio. A 30-minute video '
  'needs about 400 frames instead of 54,000, so it renders in minutes on any computer.')

# ------------------------------------------------------------ 12. packaging --
h1('12. Titles, descriptions, thumbnails, Shorts')
h2('Title pattern (60 to 90 characters)')
code('{Character} {problem}... Then {surprise}! | Slow English Listening Story (A2)\n'
     'Example: Maya Lost Her Keys on Her First Day... Then a Stranger Helped! | Slow English Story (A2)')
bullets(['Always include "Slow English" or "English Listening" and the level.',
         'One emotional hook and a cliffhanger. No false promises: the story must contain what the title says.'])
h2('Description template')
code('Improve your English listening with a slow, easy story for A2 learners.\n'
     'In this story: {one-sentence summary without the ending}.\n\n'
     'Key words: {word} ({meaning}), {word} ({meaning}), ...\n\n'
     '0:00 Introduction\n0:20 Chapter 1: {title}\n... (one line per chapter, from the builder\'s timings)\n'
     '{mm:ss} Key words\n{mm:ss} Quiz\n\n'
     'Practise: write one sentence about {topic} in the comments.\n'
     'Next story: {next title}\n\n#learnenglish #englishlistening #slowenglish')
h2('Thumbnail (1280 x 720)')
bullets(['The chapter illustration that shows the strongest emotion, cropped wide, on the left two-thirds.',
         '2 to 5 huge words (the hook, e.g. "SHE LOST EVERYTHING?") on the right, white text with a dark outline.',
         'Level badge "A2" in a corner and the words "Slow English". Test 3 versions with YouTube\'s Test &amp; Compare.'])
h2('Shorts (2 to 3 a week)')
bullets(['Vertical 1080 x 1920, 20 to 45 seconds: one useful phrase from the latest story ("take a deep breath"), '
         'the scene, the meaning, one example sentence, and "Full story on the channel".',
         'Shorts bring subscribers; the long videos bring watch hours. Always link the Short to its long video.'])

# --------------------------------------------------------------- 13. plan --
h1('13. Upload plan, pass marks and 30-day test')
table([['Week', 'Long videos', 'Shorts', 'Focus'],
       ['1', '3 (Mon, Wed, Fri)', '3', 'Launch: stories 1-3, one playlist "A2 Stories"'],
       ['2', '3', '3', 'Check retention graphs; fix the first 30 seconds if viewers drop early'],
       ['3', '4', '3', 'Double the topics that worked (characters, situations)'],
       ['4', '4-5', '3', 'Add a B1 story; decide on the podcast format (C)']],
      [0.6 * inch, 1.4 * inch, 0.7 * inch, 3.8 * inch])
p('<b>Pass marks for every long video</b> (YouTube Studio, after 7 days):')
table([['Measure', 'Pass mark', 'If it misses'],
       ['Average view duration', 'over 4 minutes', 'Shorten the intro, make chapter 1 more dramatic'],
       ['Click-through rate', 'over 4%', 'New thumbnail and title test'],
       ['Subscribers per 100 views', '1 or more', 'Stronger series hook: "Maya\'s story continues next week"'],
       ['Comments', 'some practice sentences', 'Make the comment prompt easier']],
      [1.8 * inch, 1.5 * inch, 3.2 * inch])
p('<b>Decision rule:</b> after 30 days, keep the format if at least 3 videos pass the view-duration and '
  'subscriber marks. If none do, change one big thing (format, level or voice) rather than making more of the same.')
p('<b>Daily 10 minutes (owner):</b> reply to comments on the channel, and share a new story where English learners '
  'meet (for example language-learning communities and groups that allow it). Never spam.')

# ------------------------------------------------------------- 14. policy --
h1('14. Policy and safety rules')
bullets(['No buying views, subscribers or comments; no bots; no sub-for-sub. These can get the channel terminated.',
         'Original stories, characters and illustrations only. No copyrighted characters, books, films or music.',
         'No real or famous people and no logos or brands in images or stories.',
         'Every video must be different and teach something (key words, quiz). No near-duplicate uploads.',
         'AI disclosure: YouTube requires the "altered or synthetic content" label for realistic content that could '
         'be mistaken for real people or events. Clearly illustrated stories normally do not need it; when in doubt, '
         'turn it on (it does not reduce reach or monetization).',
         'Made for kids: NO (adult learners).'])

# ------------------------------------------------------------ 15. sources --
h1('15. Sources')
bullets(['YouTube Help, "YouTube Partner Program overview and eligibility", support.google.com/youtube/answer/72851 '
         '(read Nov 10, 2026).',
         'Niche and channel measurements: YouTube Data API v3 (search, videos, channels, playlistItems), queried '
         'Nov 10, 2026; top 50 long videos per search term published in the previous 60 days.',
         'nofacetube.com, "YouTube\'s inauthentic content policy for faceless channels".',
         'TubeBuddy blog, "YouTube AI demonetization: the new rule hitting entire channels".',
         '404 Media, "AI-generated \'Boring History\' videos are flooding YouTube" (2025).',
         'Kokoro TTS (Apache 2.0) and the kokoro-onnx package; Google Fonts (Nunito, DM Serif Display, Poppins, all '
         'SIL Open Font License).'])
p('Note: channel numbers change daily. Re-measure before relying on them.', SM)

# ----------------------------------------------------------- appendices --
story.append(PageBreak())
h1('Appendix A: story file format (JSON)')
p('One file per episode. "paragraphs" is a list of paragraphs; each paragraph is a list of sentences. "image" is '
  'the path of the chapter illustration. A full episode has 5 to 6 chapters; this example shows one.')
code(json.dumps(json.load(open(os.path.join(HERE, 'stories', 'ep01_sample.json'))), indent=1, ensure_ascii=False))

story.append(PageBreak())
h1('Appendix B: complete video builder (Python)')
p('Save as <font face="Courier">story.py</font>. Adjust the FONTS and MODELS folder paths at the top to where you '
  'put the fonts and Kokoro model files. Run <font face="Courier">python3 story.py my_story.json --stills</font> to '
  'preview, then without --stills to render.')
code(open(os.path.join(HERE, 'story.py')).read())

story.append(PageBreak())
h1('Appendix C: prompt for writing a new story')
p('Paste this into any LLM, replacing the parts in braces. Review the result before building.')
code('''You are writing an original listening story for adult English learners at CEFR level {A2}.
Title: {title}. Main character: Maya, 27, who moved to a new country and works in a small cafe.
Other recurring characters you may use: Daniel (coworker), Mrs. Patel (cafe owner), Leo (Maya's brother).

Rules:
- 3,000 to 4,000 words in 6 chapters. Each chapter 4 to 6 paragraphs; each paragraph 3 to 5 sentences.
- Every sentence 6 to 12 words. Common words only. Mostly present simple and past simple. First person ("I").
- A real adult problem, a turning point, and a warm ending. End every chapter with a small surprise.
- Repeat each new word 3 to 5 times. Choose 6 to 10 key words or phrases and give a very simple meaning for each.
- Write one multiple-choice quiz question with 3 options about the story, and say which option is correct.
- Completely original: no existing stories, books, films, real people, brands or copyrighted characters.
- For each chapter, write one image description: the scene, the place, the time of day, Maya's emotion.

Output only valid JSON in exactly this format:
{"name": "{file_name}", "level": "A2", "title": "...", "voice": "af_heart", "speed": 0.82,
 "chapters": [{"title": "Chapter 1: ...", "image": "art/{file_name}_ch1.png", "image_prompt": "...",
               "paragraphs": [["sentence", "sentence"], ["sentence"]]}],
 "words": [["word", "simple meaning"]],
 "quiz": {"q": "...", "options": ["...", "...", "..."], "answer": 0}}''')


def footer(c, d):
    c.saveState()
    c.setFont('Helvetica', 7.5)
    c.setFillColor(colors.HexColor('#888888'))
    c.drawString(0.75 * inch, 0.5 * inch, 'English-Learning Story Channel: research and build specification')
    c.drawRightString(letter[0] - 0.75 * inch, 0.5 * inch, f'Page {d.page}')
    c.restoreState()


doc = SimpleDocTemplate(OUT, pagesize=letter, leftMargin=0.75 * inch, rightMargin=0.75 * inch, topMargin=0.7 * inch,
                        bottomMargin=0.75 * inch, title='English-Learning Story Channel: Research and Build Spec',
                        author='Coin Theory studio')
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print('wrote', OUT)
