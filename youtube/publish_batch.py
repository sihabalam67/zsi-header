#!/usr/bin/env python3
"""Upload and schedule a batch of finished videos, then wire them into playlists. Resumable and safe to re-run.

    python3 youtube/publish_batch.py plan.json [--dry-run]

plan.json maps each kit name (channel/out/<name>.upload.json) to its launch day, plus playlist info:
    {"videos": {"ep06_banks": "2026-11-13", "ep06_short_x": "2026-11-13", ...},
     "playlists": {"ep06": ["Banking, Explained", "How money is created ..."]},
     "launch_questions": {"ep06_banks": "Question to post as the launch comment"},
     "links": {"ep06_banks": ["Previous episode", "ep05_jobs"]}}

"links" (optional) adds a "<label>: <title> <link>" line to a long video's description; the target can be any video in
video_ids.json. Every long video also gets a "Full series: <playlist link>" line.

Every video goes public at 2:00 PM New York time on its day (daylight saving handled). Shorts get a "Watch the full
video" link to their episode's long video in the description. IDs go to channel/out/video_ids.json, playlists to
channel/out/playlists.json and questions to channel/out/launch_comments.json.
"""
import datetime as dt
import json
import os
import sys
import time
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'youtube'))
os.chdir(ROOT)
from upload import client, upload, validate  # noqa: E402

OUT = 'channel/out'
NY = ZoneInfo('America/New_York')


def publish_at(day):
    """'YYYY-MM-DD' goes live at 2:00 PM New York; 'YYYY-MM-DDTHH:MM' at that New York time (breaking news)."""
    d, _, hm = day.partition('T')
    t = dt.time.fromisoformat(hm) if hm else dt.time(14, 0)
    local = dt.datetime.combine(dt.date.fromisoformat(d), t, tzinfo=NY)
    return local.astimezone(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def is_short(name):
    return '_short_' in name


def probe(path):
    """(seconds, width, height) of a video file."""
    import subprocess
    out = subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                                   'stream=width,height:format=duration', '-of', 'json', path])
    j = json.loads(out)
    return float(j['format']['duration']), j['streams'][0]['width'], j['streams'][0]['height']


def long_of(name, names):
    ep = name.split('_')[0]
    return next((n for n in names if n.startswith(ep + '_') and '_short_' not in n), None)


def link_up(yt, plan, ep, ids, playlist_id, longs):
    """Append the episode links and the series playlist to each long video's description (once)."""
    for name in longs:
        sn = yt.videos().list(part='snippet', id=ids[name]).execute()['items'][0]['snippet']
        if 'Full series:' in sn['description']:
            continue
        add = '\n'
        if name in plan.get('links', {}):
            label, target = plan['links'][name]
            t = yt.videos().list(part='snippet', id=ids[target]).execute()['items'][0]['snippet']['title']
            add += f"\n{label}: {t} https://youtu.be/{ids[target]}"
        add += f"\nFull series: https://www.youtube.com/playlist?list={playlist_id}"
        sn['description'] += add
        yt.videos().update(part='snippet', body={'id': ids[name], 'snippet': {
            k: sn[k] for k in ('title', 'description', 'tags', 'categoryId', 'defaultLanguage', 'defaultAudioLanguage')
            if k in sn}}).execute()
        print('  linked', name)


def main():
    plan = json.load(open(sys.argv[1]))
    dry = '--dry-run' in sys.argv
    ids = json.load(open(f'{OUT}/video_ids.json'))
    videos = plan['videos']
    # long videos first, so Shorts can link to them
    order = sorted(videos, key=lambda n: ('_short_' in n, videos[n], n))
    for name in order:
        m = json.load(open(f'{OUT}/{name}.upload.json'))
        m['publishAt'] = publish_at(videos[name])
        errs = validate(m)
        if errs:
            sys.exit(f'{name}: {errs}')
        secs, w, h = probe(m['video'])
        if is_short(name) and (w, h) != (1080, 1920):
            sys.exit(f'{name}: Shorts must be 1080x1920, got {w}x{h}')
        if not is_short(name) and h < 1440:
            print(f'  WARNING: {name} is {w}x{h}; render at 1440p (engine default) for YouTube\'s sharper encode')
        if not is_short(name) and secs < 480:
            print(f'  WARNING: {name} is {secs / 60:.1f} min; mid-roll ads need 8:00+ (fine only if the material is done)')
        if is_short(name) and secs > 180:
            sys.exit(f'{name}: {secs:.0f}s is too long for a Short (3 min max)')
        print(f"{name}: {m['title']} -> {m['publishAt']}" + (' (already uploaded)' if name in ids else ''))
        if dry or name in ids:
            continue
        if '_short_' in name:
            parent = long_of(name, list(ids) + list(videos))
            if parent and parent not in ids:
                sys.exit(f'{name}: upload its long video {parent} first')
            if parent:  # a standalone (news) Short keeps its own description
                m['description'] = m['description'].replace(
                    'Full video on the Coin Theory channel.', f'Watch the full video: https://youtu.be/{ids[parent]}')
        ids[name] = upload(m)
        json.dump(ids, open(f'{OUT}/video_ids.json', 'w'), indent=1)
    if dry:
        return
    yt = client()
    pls = json.load(open(f'{OUT}/playlists.json'))
    for ep, (title, desc) in plan.get('playlists', {}).items():
        if title not in pls:
            pls[title] = yt.playlists().insert(part='snippet,status', body={
                'snippet': {'title': title, 'description': desc + ' Education only, not financial advice.',
                            'defaultLanguage': 'en'}, 'status': {'privacyStatus': 'public'}}).execute()['id']
            json.dump(pls, open(f'{OUT}/playlists.json', 'w'), indent=1)
            time.sleep(15)  # a brand-new playlist is briefly not found
        have = {i['snippet']['resourceId']['videoId'] for i in yt.playlistItems().list(
            part='snippet', playlistId=pls[title], maxResults=50).execute().get('items', [])}
        for name in order:
            if not name.startswith(ep + '_') or ids[name] in have:
                continue
            for attempt in range(6):
                try:
                    yt.playlistItems().insert(part='snippet', body={'snippet': {
                        'playlistId': pls[title], 'resourceId': {'kind': 'youtube#video', 'videoId': ids[name]}}}).execute()
                    break
                except Exception as e:
                    print('  playlist retry:', str(e)[-80:])
                    time.sleep(8 * (attempt + 1))
        print('playlist', title, pls[title])
        link_up(yt, plan, ep, ids, pls[title], [n for n in order if n.startswith(ep + '_') and not is_short(n)])
    q = json.load(open(f'{OUT}/launch_comments.json'))
    q.update(plan.get('launch_questions', {}))
    json.dump(q, open(f'{OUT}/launch_comments.json', 'w'), indent=1)
    missing = [n for n in videos if '_short_' not in n and n not in q]
    if missing:
        print('WARNING: no launch question for', missing)
    time.sleep(10)  # YouTube can briefly return stale status after uploads
    for v in yt.videos().list(part='status', id=','.join(ids[n] for n in order)).execute()['items']:
        print(v['id'], v['status']['privacyStatus'], v['status'].get('publishAt'))


if __name__ == '__main__':
    main()
