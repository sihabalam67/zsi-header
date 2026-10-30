#!/usr/bin/env python3
"""Read-only QA of every uploaded video against its kit and channel/SCHEDULE.md. Run after each publish_batch.py.

    python3 youtube/qa.py

Checks: private + scheduled at 2 PM New York on the SCHEDULE.md day, not made for kids, processed, title/description/
tags match the kit (ignoring the series links publish_batch adds), Shorts link their long video, custom thumbnail,
length, launch question, one playlist per episode, English captions serving, playlists public. Exits 1 on problems.
"""
import json, os, re, sys, datetime as dt
from zoneinfo import ZoneInfo
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT); sys.path.insert(0, 'youtube')
from upload import client
yt = client(); OUT = 'channel/out'
ids = json.load(open(f'{OUT}/video_ids.json')); pls = json.load(open(f'{OUT}/playlists.json'))
q = json.load(open(f'{OUT}/launch_comments.json'))
sched = {}
for line in open('channel/SCHEDULE.md'):
    m = re.match(r'\| (\w+ \w+ \d+) \| (\w+) \| .*\| https://youtu.be/(\S+) \|', line)
    if m: sched[m.group(3)] = m.group(1)
probs, warns = [], []
def P(*a): probs.append(' '.join(map(str, a)))
items = {}
vids = list(ids.values())
for i in range(0, len(vids), 50):
    for v in yt.videos().list(part='snippet,status,contentDetails,fileDetails,processingDetails,localizations', id=','.join(vids[i:i+50])).execute()['items']:
        items[v['id']] = v
names = {v: k for k, v in ids.items()}
inpl = {}
for t, pid in pls.items():
    for it in yt.playlistItems().list(part='snippet', playlistId=pid, maxResults=50).execute()['items']:
        inpl.setdefault(it['snippet']['resourceId']['videoId'], []).append(t)
NY = ZoneInfo('America/New_York')
def iso_secs(d):
    m = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', d); h, mi, s = (int(x or 0) for x in m.groups()); return h*3600+mi*60+s
rows = []
for n, vid in ids.items():
    v = items.get(vid)
    if not v: P(n, 'NOT FOUND on YouTube'); continue
    kit = json.load(open(f'{OUT}/{n}.upload.json'))
    sn, st, cd = v['snippet'], v['status'], v['contentDetails']
    if st['privacyStatus'] != 'private': P(n, 'privacy', st['privacyStatus'])
    pa = st.get('publishAt')
    if not pa: P(n, 'no publishAt')
    else:
        local = dt.datetime.fromisoformat(pa.replace('Z', '+00:00')).astimezone(NY)
        if (local.hour, local.minute) != (14, 0): P(n, 'publish not 2PM ET', local)
        want = sched.get(vid)
        if want and local.strftime('%a %b ') + str(local.day) != want: P(n, 'schedule mismatch', local.date(), 'vs SCHEDULE.md', want)
        if not want: P(n, 'not in SCHEDULE.md')
    if st.get('madeForKids') or st.get('selfDeclaredMadeForKids'): P(n, 'made for kids!')
    if st.get('uploadStatus') != 'processed': P(n, 'uploadStatus', st.get('uploadStatus'))
    if st.get('license') != 'youtube': P(n, 'license', st.get('license'))
    if not st.get('embeddable'): P(n, 'not embeddable')
    if sn['title'] != kit['title']: P(n, 'TITLE differs:\n   live:', sn['title'], '\n   kit: ', kit['title'])
    desc = sn['description']
    if '_short_' in n:
        parent = next(k for k in ids if k.startswith(n.split('_')[0] + '_') and '_short_' not in k)
        if f'https://youtu.be/{ids[parent]}' not in desc: P(n, 'Short missing full-video link')
    elif re.sub(r'\n\n(?:[^\n]+: [^\n]*https://youtu\.be/\S+\n)?Full series: \S+$', '', desc) != kit['description']:
        P(n, 'DESCRIPTION differs from kit')
    if set(sn.get('tags', [])) != set(kit.get('tags', [])): P(n, 'tags differ')
    if sn.get('categoryId') != '27': P(n, 'category', sn.get('categoryId'))
    if sn.get('defaultLanguage') != 'en' or sn.get('defaultAudioLanguage') != 'en': P(n, 'language', sn.get('defaultLanguage'), sn.get('defaultAudioLanguage'))
    th = sn.get('thumbnails', {})
    if '_short_' not in n and 'maxres' not in th: P(n, 'no maxres thumbnail (custom thumbnail may be missing)')
    dur = iso_secs(cd['duration'])
    if '_short_' in n and dur > 180: P(n, 'Short too long', dur)
    if '_short_' not in n and dur < 480: warns.append(f'{n}: {dur}s, under 8 min (no mid-roll ads)')
    if '_short_' not in n and 'Full series:' not in desc: P(n, 'no series/playlist link in description')
    if '_short_' not in n and n not in q: P(n, 'no launch question')
    ep = n.split('_')[0]
    if vid not in inpl: P(n, 'NOT in any playlist')
    elif len(inpl[vid]) > 1: P(n, 'in several playlists', inpl[vid])
    if '<' in desc or '>' in desc: P(n, 'angle bracket in description')
    rows.append((pa[:16] if pa else '', n, dur, cd.get('definition'), len(sn['title'])))
# captions on long videos
for n, vid in ids.items():
    if '_short_' in n: continue
    caps = yt.captions().list(part='snippet', videoId=vid).execute()['items']
    std = [c for c in caps if c['snippet']['trackKind'] == 'standard' and c['snippet']['language'] == 'en']
    if not std: P(n, 'no uploaded English captions')
    elif any(c['snippet'].get('status') != 'serving' for c in std): P(n, 'caption status', [c['snippet'].get('status') for c in std])
# playlist membership by episode
ep_pl = {}
for n, vid in ids.items():
    for t in inpl.get(vid, []): ep_pl.setdefault(n.split('_')[0], set()).add(t)
for ep, s in ep_pl.items():
    if len(s) != 1: P(ep, 'episode spread over playlists', s)
for t, pid in pls.items():
    p = yt.playlists().list(part='status,snippet', id=pid).execute()['items']
    if not p: P('playlist missing', t)
    elif p[0]['status']['privacyStatus'] != 'public': P('playlist', t, p[0]['status']['privacyStatus'])
ch = yt.channels().list(part='brandingSettings,status,statistics,snippet', mine=True).execute()['items'][0]
print('channel:', ch['snippet']['title'], ch['statistics'], 'madeForKids:', ch['status'].get('madeForKids'), 'longUploads:', ch['status'].get('longUploadsStatus'))
for r in sorted(rows): print(*r)
print('\nwarnings:', *warns, sep='\n  ')
print('\nPROBLEMS:' if probs else '\nNO PROBLEMS', *probs, sep='\n')
sys.exit(1 if probs else 0)
