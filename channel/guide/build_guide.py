"""Generate the Coin Theory checklist page from the upload results.

    python3 channel/guide/build_guide.py   # writes channel/guide/coin-theory-checklist.html

Publish it to the existing artifact https://claude.ai/artifact/QpErtvBZgo9XZvtmFaG4Hp (same URL). Add new videos to
SCHED, LONGS and QUESTIONS, and their day sections in main().
"""
import base64
import html
import json
import os
import subprocess

S = os.path.dirname(os.path.abspath(__file__))
REPO = '/home/user/zsi-header'
OUTD = os.path.join(REPO, 'channel', 'out')
RAW = 'https://github.com/sihabalam67/zsi-header/raw/claude/remake-video-claude-code-ds9btu/channel/out'
IDS = json.load(open(os.path.join(OUTD, 'video_ids.json')))

# (name, day label, date text, long?)
SCHED = [
    ('ep03_gas', 'Fri Oct 30', True), ('ep03_short_jump', 'Fri Oct 30', False),
    ('ep03_short_barrel', 'Sat Oct 31', False), ('ep03_short_feathers', 'Sun Nov 1', False),
    ('ep04_fed', 'Mon Nov 2', True), ('ep04_short_cards', 'Mon Nov 2', False),
    ('ep04_short_savings', 'Tue Nov 3', False), ('ep04_short_why', 'Wed Nov 4', False),
    ('ep05_jobs', 'Thu Nov 5', True), ('ep05_short_layoffs', 'Thu Nov 5', False),
    ('ep02_housing', 'Fri Nov 6', True), ('ep02_short_price', 'Fri Nov 6', False),
    ('ep02_short_payment', 'Sat Nov 7', False), ('ep02_short_supply', 'Sun Nov 8', False),
    ('ep01_inflation', 'Mon Nov 9', True), ('ep01_short_prices', 'Mon Nov 9', False),
    ('ep01_short_wages', 'Tue Nov 10', False), ('ep01_short_rule70', 'Wed Nov 11', False),
    ('ep05_short_hiring', 'Thu Nov 12', False),
]
LONGS = {'ep01': 'ep01_inflation', 'ep02': 'ep02_housing', 'ep03': 'ep03_gas', 'ep04': 'ep04_fed', 'ep05': 'ep05_jobs'}
M = {n: json.load(open(os.path.join(OUTD, f'{n}.upload.json'))) for n, _, _ in SCHED}


def title(n):
    return M[n]['title'].replace(' #shorts', '')


def dur(n):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0',
                          os.path.join(OUTD, f'{n}.mp4')], capture_output=True, text=True).stdout
    return float(out)


def mmss(sec):
    sec = int(sec)
    return f'{sec // 60}:{sec % 60:02d}'


def e(s):
    return html.escape(s, quote=True)


def ui(s):
    return f'<span class="ui">{e(s)}</span>'


def b(s):
    return f'<b>{e(s)}</b>'


def step(sid, head, body, clock=None, sub=None):
    c = f'<span class="clock">{e(clock)}</span>' if clock else ''
    sb = f'<span class="clock">{e(sub)}</span>' if sub else ''
    return (f'<div class="step" data-id="{sid}"><div class="step-h"><input type="checkbox" id="{sid}">'
            f'<label for="{sid}">{c}<h3>{e(head)}</h3>{sb}</label></div>{body}</div>')


def ol(items):
    return '<ol class="do">' + ''.join(f'<li>{i}</li>' for i in items) + '</ol>'


def day(when, t, length, h2, steps, note=None):
    n = f'<p class="if">{note}</p>' if note else ''
    hh = f'<h2>{e(h2)}</h2>' if h2 else ''
    return (f'<section class="day"><div class="when"><span class="d">{e(when)}</span><span class="t">{e(t)}</span>'
            f'<span class="len">{e(length)}</span></div><div class="body">{hh}{n}{"".join(steps)}</div></section>')


def copyline(cid, text):
    return (f'<div class="copyline"><span id="{cid}">{e(text)}</span>'
            f'<button class="btn" data-copy="{cid}">Copy</button></div>')


def thumb_data(ep):
    return 'data:image/png;base64,' + base64.b64encode(open(os.path.join(OUTD, f'{ep}_thumb_b.png'), 'rb').read()).decode()


QUESTIONS = {
    'ep01': 'What did a loaf of bread cost where you grew up, and what year was it? I read every answer.',
    'ep02': 'How old were you (or your parents) when you bought a first home, and what did it cost? Or are you '
            'still waiting?',
    'ep03': 'What are you paying for a gallon of gas right now, and in which state? Let\'s map it in the comments.',
    'ep04': 'Have you noticed your credit card rate or your savings rate change this year? Tell me which one.',
    'ep05': "Has your company frozen hiring, or offered buyouts this year? Tell me your industry, and I'll read every answer.",
}
SHORTS_OF = {ep: [n for n, _, lg in SCHED if n.startswith(ep) and not lg] for ep in LONGS}


def yt(n):
    return f'https://youtu.be/{IDS[n]}'


def launch_day(ep, when, prefix):
    long_n = LONGS[ep]
    lt = title(long_n)
    first_short = SHORTS_OF[ep][0]
    steps = [
        step(f'{prefix}1', 'Check that it\'s live', ol([
            f'Open <a href="https://studio.youtube.com" target="_blank" rel="noopener">studio.youtube.com</a> → '
            f'{ui("Content")}.',
            f'{b(lt)} and {b(title(first_short))} should say {b("Public")} in the Visibility column. If it still '
            f'says Scheduled, wait 5 minutes and refresh the page.']), clock='2:05 PM'),
        step(f'{prefix}2', 'Pin my question comment', ol([
            'At 2:07 PM I post this question on the video for you (don\'t post it yourself, or it shows twice):'
            + copyline(f'q{ep}', QUESTIONS[ep]),
            f'After 2:10 PM, open the video: <a href="{yt(long_n)}" target="_blank" rel="noopener">{yt(long_n)}</a> '
            f'and scroll down to {b("Comments")}. On the phone app, tap the comments box under the video.',
            f'Find that comment, click the three dots <b>⋮</b> on its right → {ui("Pin")} → {ui("Pin")} again to '
            'confirm.']), clock='2:10 PM',
            sub='YouTube does not let apps pin comments, so this one click is yours.'),
        step(f'{prefix}3', f'(Optional) Link the Shorts to the long video', ol([
            f'Only if you see {ui("Related video")}; YouTube is still rolling it out. Each Short\'s description '
            'already links to the full video, so skipping this is fine.',
            f'Studio → {ui("Content")} → {ui("Shorts")} tab.',
            f'Move your mouse over {b(title(SHORTS_OF[ep][0]))} and click the <b>pencil</b> icon '
            f'({ui("Details")}).',
            f'Scroll down to {ui("Related video")} and click the box.',
            f'A list of your videos opens. Click {b(lt)}.',
            f'Click the blue {ui("Save")} button at the top right.',
            'Do the same for ' + ' and '.join(b(title(n)) for n in SHORTS_OF[ep][1:]) +
            '. They are still Scheduled; you can still change them.']), clock='2:10 PM',
            sub='This adds a tappable link on each Short that sends viewers to the full video.'),
        step(f'{prefix}4', '(Optional) Heart comments', f'<p>I reply to comments for you at 2:07 PM and 8:43 PM. '
             f'Apps can\'t give hearts, so if you have a minute, open Studio → {ui("Comments")} and tap the '
             f'<b>heart</b> on good ones. Please don\'t reply to the same comments yourself; it would show two '
             f'answers.</p>', clock='evening, 2 min'),
    ]
    return day(when, '2:05 PM', 'about 15 min', f'{lt} goes live', steps,
               'At <b>2:00 PM</b> the video goes public by itself. You don\'t need to do anything at 2:00.')


def check_day(n, when, sid):
    return day(when, '2:05 PM', '2 min, optional', None, [step(sid, '(Optional) Peek at today\'s Short', ol([
        f'Studio → {ui("Content")} → {ui("Shorts")}. {b(title(n))} should say {b("Public")}. I check this too '
        'and message you if it isn\'t.',
        f'Comment replies are automatic. If you like, tap the <b>heart</b> on good comments in '
        f'{ui("Comments")}.']))])


def analytics_day(when, eps, sid):
    names = ' and '.join(b(title(LONGS[ep])) for ep in eps)
    return day(when, '7:00 PM', 'about 15 min', 'Take screenshots for next week', [step(sid,
        'Screenshot the analytics of this week\'s long videos',
        '<p>How to take a screenshot: on <b>Windows</b>, press <b>Windows key + Shift + S</b> and drag a box. On a '
        '<b>Mac</b>, press <b>Cmd + Shift + 4</b> and drag a box; the picture lands on your Desktop.</p>' + ol([
            f'Studio → {ui("Content")} → {ui("Videos")}. Move your mouse over the video and click the '
            f'<b>bar-chart</b> icon ({ui("Analytics")}).',
            f'Take a screenshot of the {ui("Overview")} tab.',
            f'Click {ui("Reach")}. Take a screenshot that shows <b>impressions click-through rate</b> and '
            f'<b>traffic sources</b>.',
            f'Click {ui("Engagement")}. Take a screenshot of the <b>audience retention</b> graph.',
            f'Do this for {names}.',
            'Come back to the Claude chat, attach the screenshots, and type <b>next week</b>.']) +
        '<p class="if">If the tabs have different names, take a screenshot of every tab.</p>')])


def video_rows():
    rows = []
    for n, d, lg in SCHED:
        kind = '<b>Long:</b> ' if lg else 'Short: '
        rows.append(f'<tr><td class="t">{e(d)}, 2:00 PM</td><td>{kind}{e(title(n))}</td>'
                    f'<td><a href="{yt(n)}" target="_blank" rel="noopener">{IDS[n]}</a></td></tr>')
    return ''.join(rows)


def setup_section():
    thumbs = ''.join(
        f'<figure><img src="{thumb_data(ep)}" alt="Thumbnail B for {e(title(LONGS[ep]))}"><figcaption>'
        f'<a href="{RAW}/{ep}_thumb_b.png" target="_blank" rel="noopener">{ep}_thumb_b.png</a> · '
        f'{e(title(LONGS[ep]))}</figcaption></figure>' for ep in LONGS)
    ends = ''.join(f'<li>{b(title(LONGS[ep]))}: the video is {mmss(dur(LONGS[ep]))} long, so type '
                   f'<b>{mmss(dur(LONGS[ep]) - 15)}</b>.</li>' for ep in LONGS)
    steps = [
        step('s1', '1. Open YouTube Studio', ol([
            'On your computer, open Chrome and go to <a href="https://studio.youtube.com" target="_blank" '
            'rel="noopener">studio.youtube.com</a>.',
            'If it asks you to sign in, use the Google account that owns the Coin Theory channel.',
            f'Click your round profile picture at the <b>top right</b> and check that it says <b>Coin Theory</b>. '
            f'If not, click {ui("Switch account")} and pick Coin Theory.',
            f'On the left, click {ui("Content")}. The tabs at the top are {ui("Videos")} (your 5 long videos) and '
            f'{ui("Shorts")} (your 14 Shorts).'])),
        step('s2', '2. One-minute check: is anything locked?', ol([
            f'In the {ui("Videos")} tab, look at the {ui("Visibility")} column. Every video should say '
            f'<b>Scheduled</b> with a date. I set those for you.',
            f'Click the word <b>Scheduled</b> on {b(title("ep01_inflation"))}.']) +
            '<p class="if"><b>If a box opens with the date and time:</b> good. Press <b>Esc</b> and go to step 3.</p>'
            '<p class="if"><b>If you see a lock, the word "locked" or "restricted", or nothing opens:</b> YouTube has '
            'locked uploads from my app. Go to <a href="#planb">Plan B</a> at the bottom, then come back to step 3.</p>',
            sub='YouTube may lock uploads from apps it hasn\'t reviewed yet. This tells you if that happened.'),
        step('s3', '3. Thumbnail test (5 long videos)', '<p>Save these 5 pictures to your <b>Desktop</b>: click each '
             f'link, then right-click the picture → {ui("Save image as…")} → <b>Desktop</b> → {ui("Save")}.</p>'
             f'<div class="thumbs">{thumbs}</div>' + ol([
                 f'{ui("Content")} → {ui("Videos")} → <b>pencil</b> on the first long video.',
                 f'Scroll down to {ui("Thumbnail")}. Thumbnail A is already there (I uploaded it). You may have done this step already.',
                 f'Click {ui("Test & compare")} next to the thumbnail. If you don\'t see it, click the three dots '
                 f'<b>⋮</b> on the thumbnail.',
                 'A window opens with thumbnail A in the first slot. Click the empty slot with the <b>+</b>, open '
                 'your <b>Desktop</b>, and pick the matching <b>_thumb_b.png</b> file.',
                 f'Click {ui("Done")}, then {ui("Save")} at the top right.',
                 'Repeat for the other long videos.']) +
             '<p class="if"><b>If Test &amp; compare is grey or missing</b> while a video is scheduled, do it right '
             'after that video goes public (Fri Oct 30, Mon Nov 2, Fri Nov 6, Mon Nov 9 at 2:05 PM).</p>',
             sub='YouTube shows each viewer one of two covers and keeps the one that gets more watch time.'),
        step('s4', '4. End screens (5 long videos)', ol([
            'Open the Details page (<b>pencil</b>) of a long video.',
            f'In the right column, click {ui("End screen")}.',
            f'On the left, click the template that shows <b>1 video + 1 subscribe</b>.',
            f'Click the video box in the preview and choose {ui("Best for viewer")}.',
            'Click each box and type the start time below into its <b>start time</b> field under the preview, so '
            'the boxes show for the last 15 seconds:<ul>' + ends + '</ul>',
            f'Click {ui("Save")} at the top right. Repeat for each long video.']),
            sub='These are the "watch next" and "subscribe" boxes at the end.'),
    ]
    return day('Fri Oct 30', '10:00 AM', 'about 30 min, one sitting', 'One-time setup', steps,
               'It\'s in your Google Calendar. Try to finish before 2 PM, when the first video goes live. If you can\'t, do it later the same day; it still works.')


def plan_b():
    files = []
    for n, d, lg in SCHED:
        files.append([n + '.mp4', ('Long video' if lg else 'Short') + ', goes public ' + d])
        if lg:
            ep = n[:4]
            files += [[ep + '_thumb_a.png', 'Thumbnail A for ' + title(n)], [ep + '_thumb_b.png', 'Thumbnail B'],
                      [n + '.en.srt', 'Captions for ' + title(n)]]
    kits = [dict(when=d + ', 2:00 PM', file=n + '.mp4', title=M[n]['title'], description=M[n]['description'],
                 tags=', '.join(M[n]['tags'])) for n, d, _ in SCHED]
    return files, kits


PLAN_B_HTML = '''
<details id="planb">
  <summary>Plan B: only if step 2 showed a lock</summary>
  <div class="body">
    <p>If YouTube locked my uploads, they can't go public. You'll upload them yourself through Studio, and YouTube
    treats those uploads normally. It takes about 15 minutes per long video and 5 per Short. Do week 1 first; week 2
    can wait until Nov 5.</p>
    <div class="step" data-id="b1"><div class="step-h"><input type="checkbox" id="b1"><label for="b1"><h3>B1. Download the files</h3></label></div>
      <p>Click each link. Videos download straight away. For pictures and caption files, right-click the page → <span class="ui">Save as…</span>. Save everything to one folder on your Desktop.</p>
      <div class="tablebox"><table><tbody id="files"></tbody></table></div></div>
    <div class="step" data-id="b2"><div class="step-h"><input type="checkbox" id="b2"><label for="b2"><h3>B2. Delete the locked copies</h3></label></div>
      <ol class="do"><li>Studio → <span class="ui">Content</span>. Move your mouse over a locked video → three dots <b>⋮</b> → <span class="ui">Delete forever</span>.</li>
      <li>Tick the box, then click <span class="ui">Delete forever</span>. Repeat for each locked video.</li></ol></div>
    <div class="step" data-id="b3"><div class="step-h"><input type="checkbox" id="b3"><label for="b3"><h3>B3. Upload each video</h3></label></div>
      <ol class="do">
        <li>In Studio, click <span class="ui">Create</span> (camera with a +, top right) → <span class="ui">Upload videos</span> → <span class="ui">Select files</span>. Pick the .mp4 file.</li>
        <li><b>Details page:</b> use the Copy buttons below to paste the <b>Title</b> and <b>Description</b>.</li>
        <li>Long videos only: under <span class="ui">Thumbnail</span>, click <span class="ui">Upload file</span> and pick the <b>_thumb_a.png</b> file.</li>
        <li><span class="ui">Audience</span>: choose <b>No, it's not made for kids</b>.</li>
        <li>Click <span class="ui">Show more</span>. Set <b>Altered content</b> to <b>Yes</b>, paste the <b>Tags</b>, and set <b>Category</b> to <b>Education</b>. Click <span class="ui">Next</span>.</li>
        <li><b>Video elements</b> (long videos only): <span class="ui">Add subtitles</span> → <span class="ui">Upload file</span> → <span class="ui">With timing</span> → <span class="ui">Continue</span> → pick the <b>.en.srt</b> file → <span class="ui">Done</span>. Then <span class="ui">End screen</span> → <span class="ui">Add</span> and follow setup step 4. Click <span class="ui">Next</span>.</li>
        <li><b>Checks:</b> wait for "No issues found", then <span class="ui">Next</span>.</li>
        <li><b>Visibility:</b> <span class="ui">Schedule</span> → the date from the table at the top, <b>2:00 PM</b>, <b>New York / Eastern Time</b> → <span class="ui">Schedule</span>.</li>
      </ol>
      <p class="if">Your video links will be new, so open each video from Studio instead of using the links on this page. Tell me in the chat and I'll update the playlists and Short descriptions for you.</p>
      <div id="kits" style="display:flex;flex-direction:column;gap:12px"></div></div>
  </div>
</details>
'''


def main():
    head = open(os.path.join(S, 'v2_head.html')).read()
    script = open(os.path.join(S, 'v2_script.html')).read()
    files, kits = plan_b()
    done = [
        'Uploaded all 19 videos (5 long, 14 Shorts) with English captions and thumbnail A. Weekly analytics are pulled automatically, so no screenshots needed.',
        'Scheduled every video to go public at <b>2:00 PM New York time</b> on its day.',
        'Made 5 playlists (Inflation, Housing, Gas prices, Interest rates, Jobs) and added each video, with "next episode" and series links in the descriptions.',
        'Added a "Watch the full video" link to every Short\'s description.',
        'Put every reminder below into your <b>Google Calendar</b>, with a link to this page.',
        'Posts launch comments and replies to viewers automatically every day. Made week 2 on the two most-searched money stories right now: the 2026 gas price spike and the Fed\'s '
        'rate hike. Every number comes from official data.',
    ]
    body = f'''<div class="wrap">
<header>
  <span class="eyebrow">Coin Theory · Oct 30 – Nov 12, 2026</span>
  <h1>Your launch, one click at a time</h1>
  <p class="lede">All times are <b>your time (New York, Eastern)</b>. Tick each box as you finish it. This page remembers your ticks in this browser.</p>
  <div class="progress"><div class="bar"><i id="bar"></i></div><span id="count">0 / 0</span></div>
</header>
<section class="panel"><h2>Already done for you</h2><ul class="donelist">{"".join(f"<li>{d}</li>" for d in done)}</ul>
<p class="if">What's left below is only what YouTube doesn't let apps do: thumbnail tests, end screens and pinning a comment. Everything else is optional.</p></section>
<div class="note"><strong>Before you start</strong><p>Use a <b>computer</b> (laptop or desktop) with Chrome. The YouTube phone app can't add end screens or test thumbnails. If a button has a slightly different name than here, click the closest match.</p></div>
<section class="panel"><h2>Your 19 videos</h2><div class="tablebox"><table><thead><tr><th>Goes public</th><th>Video</th><th>Link</th></tr></thead><tbody>{video_rows()}</tbody></table></div></section>
{setup_section()}
<h2 class="week">Week 1</h2>
{launch_day('ep03', 'Fri Oct 30', 'm')}
{check_day('ep03_short_barrel', 'Sat Oct 31', 't1')}
{check_day('ep03_short_feathers', 'Sun Nov 1', 'w1')}
{launch_day('ep04', 'Mon Nov 2', 'h')}
{check_day('ep04_short_savings', 'Tue Nov 3', 'f1')}
{check_day('ep04_short_why', 'Wed Nov 4', 'a1')}
{launch_day('ep05', 'Thu Nov 5', 'j')}
<h2 class="week">Week 2</h2>
{launch_day('ep02', 'Fri Nov 6', 'n')}
{check_day('ep02_short_payment', 'Sat Nov 7', 't2')}
{check_day('ep02_short_supply', 'Sun Nov 8', 'w2')}
{launch_day('ep01', 'Mon Nov 9', 'r')}
{check_day('ep01_short_wages', 'Tue Nov 10', 'f2')}
{check_day('ep01_short_rule70', 'Wed Nov 11', 'a2')}
{check_day('ep05_short_hiring', 'Thu Nov 12', 'j2')}
{PLAN_B_HTML}
</div>
'''
    extra_css = ('<style>.donelist{margin:0;padding-left:1.2em;display:flex;flex-direction:column;gap:6px}'
                 '.donelist li::marker{content:"✓  ";color:var(--done);font-weight:700}'
                 'h2.week{font-size:30px;padding-top:12px}.do ul{margin:6px 0 0;padding-left:1.2em}</style>\n')
    page = head.replace('<title>Coin Theory Launch Week</title>', '<title>Coin Theory Launch Plan</title>') \
        + extra_css + body + script.replace('__KITS__', json.dumps(kits).replace('</', '<\\/')) \
        .replace('__FILES__', json.dumps(files)).replace('__RAW__', RAW)
    open(os.path.join(S, 'coin-theory-checklist.html'), 'w').write(page)
    print('ok', len(page))


if __name__ == '__main__':
    main()
