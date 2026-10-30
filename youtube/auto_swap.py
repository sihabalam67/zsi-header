"""Watch channel/build/vshorts/render_all.log (written by channel/vshorts_all.sh); for each rendered Short, check the file and swap it on YouTube. Order = render order."""
import json, os, re, subprocess, sys, time, datetime as dt
from zoneinfo import ZoneInfo
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QA = os.path.join(ROOT, 'channel', 'build', 'vshorts')
V2 = '--v2' in sys.argv  # standalone Shorts from channel/shorts_v2.py: new lengths, own logs
LOG = f'{QA}/render_v2.log' if V2 else f'{QA}/render_all.log'
OUT = f'{QA}/auto_swap_v2.log' if V2 else f'{QA}/auto_swap.log'
sys.path.insert(0, f'{ROOT}/youtube')
os.chdir(ROOT)
from upload import client
done = set(l.split()[1] for l in open(OUT) if l.startswith('SWAPPED')) if os.path.exists(OUT) else set()
def log(msg):
    with open(OUT, 'a') as f: f.write(msg + '\n')
def live_secs(vid):
    d = client().videos().list(part='contentDetails', id=vid).execute()['items'][0]['contentDetails']['duration']
    m = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', d)
    return sum(int(x or 0) * k for x, k in zip(m.groups(), (3600, 60, 1)))
def check(name):
    p = f'{ROOT}/channel/out/{name}.mp4'
    j = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                                            'stream=width,height:format=duration', '-of', 'json', p]))
    w, h, secs = j['streams'][0]['width'], j['streams'][0]['height'], float(j['format']['duration'])
    lo = subprocess.run(['ffmpeg', '-nostats', '-i', p, '-af', 'ebur128=peak=true', '-f', 'null', '-'],
                        capture_output=True, text=True).stderr
    lufs = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', lo)[-1]); peak = float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS', lo)[-1])
    ids = json.load(open(f'{ROOT}/channel/out/video_ids.json'))
    old = live_secs(ids[name])
    errs = []
    if (w, h) != (1080, 1920): errs.append(f'size {w}x{h}')
    if abs(lufs + 14) > 1: errs.append(f'loudness {lufs}')
    if peak > 0: errs.append(f'peak {peak}')
    if not V2 and abs(secs - old) > 1.5: errs.append(f'length {secs:.1f}s vs scheduled {old}s')
    if V2 and not 20 <= secs <= 60: errs.append(f'length {secs:.1f}s outside 20-60 s')
    rlog = f'{QA}/r2_{name}.log'
    if V2 and os.path.exists(rlog) and re.search(r'backup voice|PACE WARNING|WARNING chatterbox', open(rlog).read()):
        errs.append('render warnings (backup voice or pace); see ' + rlog)
    return errs, f'{w}x{h} {secs:.1f}s {lufs} LUFS peak {peak}'
while True:
    lines = open(LOG).read().split('\n') if os.path.exists(LOG) else []
    for l in lines:
        if not l.startswith('OK '): continue
        name = l.split()[1]
        if name in done: continue
        errs, info = check(name)
        if errs:
            log(f'HELD {name}: {errs} ({info})'); done.add(name); continue
        r = subprocess.run(['python3', 'youtube/replace_short.py', name], capture_output=True, text=True)
        tail = (r.stdout + r.stderr).strip().splitlines()[-1:] or ['']
        if r.returncode == 0:
            log(f'SWAPPED {name} {info} | {tail[0]}'); done.add(name)
            sw = f'{ROOT}/channel/out/vshorts_swapped{"_v2" if V2 else ""}.json'
            d = json.load(open(sw)) if os.path.exists(sw) else []
            json.dump(sorted(set(d) | {name}), open(sw, 'w'), indent=1)
            subprocess.run(['git', 'add', 'channel/out/video_ids.json', 'channel/SCHEDULE.md', 'channel/out/replaced.json',
                            sw], cwd=ROOT)
            msg = (f'Swap in {"standalone 10/10" if V2 else "vertical"} {name}\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\n'
                   'Claude-Session: https://claude.ai/code/session_01KPBsdzhy6yaFbGMrWeQjjn')
            subprocess.run(['git', 'commit', '-qm', msg], cwd=ROOT)
            for _ in range(4):
                if subprocess.run(['git', 'push', '-q', '-u', 'origin', 'claude/remake-video-claude-code-ds9btu'], cwd=ROOT).returncode == 0:
                    break
                time.sleep(5)
        elif 'quota' in (r.stdout + r.stderr).lower():
            now = dt.datetime.now(ZoneInfo('America/Los_Angeles'))
            wake = (now + dt.timedelta(days=1)).replace(hour=0, minute=5, second=0)
            log(f'QUOTA reached at {name}; waiting until {wake.astimezone(ZoneInfo("America/New_York")):%H:%M} ET')
            time.sleep((wake - now).total_seconds())
            break
        else:
            log(f'ERROR {name}: {(r.stdout + r.stderr)[-400:]}'); done.add(name)
    if 'ALLDONE' in lines and all(l.split()[1] in done for l in lines if l.startswith(('OK ', 'FAIL '))):
        log('ALL SWAPS DONE'); break
    time.sleep(30)
