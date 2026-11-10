"""English-learning story videos (format B in channel/RESET_PLAN.md): the story text on screen beside one
illustration, a slow clear voice, the sentence being read highlighted, key words and a short quiz.

    python3 english/story.py english/stories/ep01_sample.json [--stills]

A story file is JSON: {"name", "level", "title", "voice", "speed", "chapters": [{"title", "image", "paragraphs":
[[sentence, ...], ...]}], "words": [[word, meaning], ...], "quiz": {"q", "options", "answer"}}.
Each sentence is voiced on its own (Kokoro, local, free), so timings are exact and nothing needs aligning.
The picture changes only when the highlighted sentence changes, so each state is drawn once and held: a 30-minute
video renders in a few minutes.
"""
import json
import os
import subprocess
import sys

import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FONTS = os.path.join(ROOT, 'studio', 'assets', 'fonts')
MODELS = os.path.join(ROOT, 'studio', 'models')
W, H, SR, FPS = 1920, 1080, 44100, 30
PAPER, INK, GREY, TEAL, ORANGE, MARK = (250, 245, 235), (38, 42, 52), (150, 150, 150), (20, 120, 120), (232, 120, 40), \
    (255, 221, 120)
_fonts = {}
_kokoro = None


def font(name, size):
    if (name, size) not in _fonts:
        _fonts[(name, size)] = ImageFont.truetype(os.path.join(FONTS, name), size)
    return _fonts[(name, size)]


def say(text, voice, speed):
    """One sentence -> float32 audio at SR."""
    global _kokoro
    if _kokoro is None:
        from kokoro_onnx import Kokoro
        _kokoro = Kokoro(os.path.join(MODELS, 'kokoro-v1.0.onnx'), os.path.join(MODELS, 'voices-v1.0.bin'))
    s, sr = _kokoro.create(text, voice=voice, speed=speed, lang='en-us')
    n = int(len(s) * SR / sr)
    a = np.interp(np.linspace(0, len(s) - 1, n), np.arange(len(s)), s).astype(np.float32)
    return a / max(1e-6, np.abs(a).max()) * 0.85


def wrap(d, text, f, maxw):
    lines, cur = [], ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    return lines + [cur] if cur else lines


def base(story, chapter, progress):
    im = Image.new('RGB', (W, H), PAPER)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((70, 50, 250, 110), 30, TEAL)
    d.text((160, 80), story['level'], font=font('Poppins-700.ttf', 34), fill='white', anchor='mm')
    d.text((280, 80), 'SLOW ENGLISH STORY', font=font('Poppins-700.ttf', 30), fill=TEAL, anchor='lm')
    d.text((70, 170), chapter['title'], font=font('DMSerif-400.ttf', 62), fill=INK, anchor='lm')
    d.rounded_rectangle((70, H - 46, W - 70, H - 34), 6, (228, 220, 205))
    d.rounded_rectangle((70, H - 46, 70 + (W - 140) * progress, H - 34), 6, ORANGE)
    if chapter.get('image') and os.path.exists(os.path.join(ROOT, chapter['image'])):
        pic = Image.open(os.path.join(ROOT, chapter['image'])).convert('RGB')
        bw, bh = 640, 800
        s = max(bw / pic.width, bh / pic.height)
        pic = pic.resize((int(pic.width * s) + 1, int(pic.height * s) + 1), Image.LANCZOS)
        x0, y0 = (pic.width - bw) // 2, (pic.height - bh) // 2
        pic = pic.crop((x0, y0, x0 + bw, y0 + bh))
        mask = Image.new('L', (bw, bh), 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, bw, bh), 36, 255)
        d.rounded_rectangle((W - 70 - bw - 8 + 14, 150 - 8 + 14, W - 70 + 8 + 14, 150 + bh + 8 + 14), 44, (225, 215, 198))
        d.rounded_rectangle((W - 70 - bw - 8, 150 - 8, W - 70 + 8, 150 + bh + 8), 44, 'white')
        im.paste(pic, (W - 70 - bw, 150), mask)
    return im


def page(story, chapter, para, active, progress):
    """One paragraph on screen; sentence `active` is marked, earlier ones grey, later ones dark."""
    im = base(story, chapter, progress)
    d = ImageDraw.Draw(im)
    f = font('Nunito-700.ttf', 52)
    x0, y, maxw, lh = 70, 260, 1080, 78
    for si, sent in enumerate(para):
        for ln in wrap(d, sent, f, maxw):
            if si == active:
                d.rounded_rectangle((x0 - 14, y - 4, x0 + d.textlength(ln, font=f) + 14, y + lh - 10), 14, MARK)
            d.text((x0, y), ln, font=f, fill=INK if si >= active else GREY)
            y += lh
        y += 14
    return im


def card_words(story, upto, progress):
    im = base(story, dict(title='Key words'), progress)
    d = ImageDraw.Draw(im)
    for i, (w, m) in enumerate(story['words']):
        y = 290 + i * 150
        on = i == upto
        d.rounded_rectangle((70, y, W - 70, y + 120), 26, MARK if on else 'white')
        d.text((110, y + 60), w, font=font('Poppins-700.ttf', 52), fill=TEAL if i <= upto else GREY, anchor='lm')
        if i <= upto:
            d.text((620, y + 60), m, font=font('Nunito-700.ttf', 44), fill=INK, anchor='lm')
    return im


def card_quiz(story, show, progress):
    q = story['quiz']
    im = base(story, dict(title='Quick quiz'), progress)
    d = ImageDraw.Draw(im)
    d.text((70, 320), q['q'], font=font('Nunito-900.ttf', 60), fill=INK, anchor='lm')
    for i, o in enumerate(q['options']):
        y = 430 + i * 150
        right = show and i == q['answer']
        d.rounded_rectangle((70, y, W - 70, y + 120), 26, (190, 235, 200) if right else 'white')
        d.text((110, y + 60), f"{'ABC'[i]}.  {o}", font=font('Nunito-700.ttf', 50), fill=INK, anchor='lm')
        if right:
            d.text((W - 130, y + 60), 'correct', font=font('Poppins-700.ttf', 40), fill=TEAL, anchor='rm')
    return im


def build(path, stills=False):
    story = json.load(open(path))
    out_dir = os.path.join(HERE, 'build', story['name'])
    os.makedirs(out_dir, exist_ok=True)
    voice, speed = story.get('voice', 'af_heart'), story.get('speed', 0.85)
    # every beat: (text to speak, pause after, function drawing its frame given progress)
    beats = []
    for ch in story['chapters']:
        beats.append((ch['title'] + '.', 0.8, lambda p, ch=ch: page(story, ch, ch['paragraphs'][0], -1, p)))
        for para in ch['paragraphs']:
            for si, sent in enumerate(para):
                beats.append((sent, 0.55, lambda p, ch=ch, para=para, si=si: page(story, ch, para, si, p)))
            beats[-1] = (beats[-1][0], 1.1, beats[-1][2])
    if story.get('words'):
        beats.append(('Key words from this story.', 0.6, lambda p: card_words(story, -1, p)))
        for i, (w, m) in enumerate(story['words']):
            beats.append((f'{w}. {m}.', 0.9, lambda p, i=i: card_words(story, i, p)))
    if story.get('quiz'):
        q = story['quiz']
        beats.append((q['q'] + ' ' + ' '.join(f"{'ABC'[i]}: {o}." for i, o in enumerate(q['options'])), 3.0,
                      lambda p: card_quiz(story, False, p)))
        beats.append((f"The answer is {'ABC'[q['answer']]}: {q['options'][q['answer']]}.", 1.5,
                      lambda p: card_quiz(story, True, p)))
    if stills:
        for i in sorted({0, 2, len(beats) // 2, len(beats) - 4, len(beats) - 1}):
            beats[i][2](i / len(beats)).save(os.path.join(out_dir, f'still_{i:03d}.png'))
        print('stills in', out_dir)
        return
    audio, concat, t = [], [], 0.0
    lead = np.zeros(int(SR * 0.6), np.float32)
    audio.append(lead)
    for i, (text, pause, draw) in enumerate(beats):
        a = say(text, voice, speed)
        a = np.concatenate([a, np.zeros(int(SR * pause), np.float32)])
        dur = len(a) / SR + (0.6 if i == 0 else 0)
        fp = os.path.join(out_dir, f'f_{i:04d}.png')
        draw(i / len(beats)).save(fp)
        concat.append(f"file '{fp}'\nduration {dur:.3f}\n")
        audio.append(a)
        t += dur
    concat.append(f"file '{fp}'\n")
    open(os.path.join(out_dir, 'list.txt'), 'w').write(''.join(concat))
    sf.write(os.path.join(out_dir, 'voice.wav'), np.concatenate(audio), SR)
    out = os.path.join(HERE, 'out', story['name'] + '.mp4')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', os.path.join(out_dir, 'list.txt'),
                    '-i', os.path.join(out_dir, 'voice.wav'), '-vf', f'fps={FPS},format=yuv420p', '-c:v', 'libx264',
                    '-preset', 'medium', '-crf', '20', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-c:a', 'aac', '-b:a',
                    '192k', '-shortest', out], check=True)
    print(f'wrote {out}  {t / 60:.1f} min, {len(beats)} beats')


if __name__ == '__main__':
    build(sys.argv[1], '--stills' in sys.argv)
