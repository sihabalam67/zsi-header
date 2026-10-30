#!/usr/bin/env python3
"""Swap an uploaded (still private, scheduled) video for a re-rendered file, keeping its day and place.

    python3 youtube/replace_short.py ep03_short_jump [--dry-run]

YouTube can't replace a video's file, so this uploads channel/out/<name>.mp4 with the same kit and the same
publishAt as the live copy, puts it at the old copy's position in the episode playlist, checks it is scheduled,
then deletes the old copy and updates channel/out/video_ids.json and channel/SCHEDULE.md. Refuses to touch a video
that is already public (that would lose its views and comments).
"""
import json
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'youtube'))
os.chdir(ROOT)
from upload import client, upload, validate  # noqa: E402

OUT = 'channel/out'


def main():
    name, dry = sys.argv[1], '--dry-run' in sys.argv
    ids = json.load(open(f'{OUT}/video_ids.json'))
    old = ids[name]
    yt = client()
    pend_path = f'{OUT}/replaced.json'  # name -> old id, kept until the old copy is deleted
    pend = json.load(open(pend_path)) if os.path.exists(pend_path) else {}
    if name in pend:  # an earlier run uploaded the new copy but didn't finish; just finish it
        finish(yt, name, pend[name], ids[name], pend, pend_path)
        return
    items = yt.videos().list(part='status', id=old).execute()['items']
    if not items:
        sys.exit(f'{name}: old video {old} not found on YouTube')
    st = items[0]['status']
    if st['privacyStatus'] != 'private' or not st.get('publishAt'):
        sys.exit(f'{name}: {old} is {st["privacyStatus"]} (publishAt {st.get("publishAt")}); only scheduled videos '
                 'can be swapped')
    m = json.load(open(f'{OUT}/{name}.upload.json'))
    m['publishAt'] = st['publishAt']
    if '_short_' in name:
        ep = name.split('_')[0]
        parent = next((n for n in ids if n.startswith(ep + '_') and '_short_' not in n), None)
        if parent:
            m['description'] = m['description'].replace(
                'Full video on the Coin Theory channel.', f'Watch the full video: https://youtu.be/{ids[parent]}')
    errs = validate(m)
    if errs:
        sys.exit(f'{name}: {errs}')
    pls = json.load(open(f'{OUT}/playlists.json'))
    where = None  # (playlist id, playlist item id, position) of the old copy
    for pid in pls.values():
        for it in yt.playlistItems().list(part='snippet', playlistId=pid, maxResults=50).execute()['items']:
            if it['snippet']['resourceId']['videoId'] == old:
                where = (pid, it['id'], it['snippet']['position'])
    print(f'{name}: replace {old} (publishAt {m["publishAt"]}, playlist {where})')
    if dry:
        return
    new = upload(m)
    ids[name] = new
    pend[name] = old
    json.dump(ids, open(f'{OUT}/video_ids.json', 'w'), indent=1)  # save at once so a crash can't lose the new id
    json.dump(pend, open(pend_path, 'w'), indent=1)
    if where:
        for attempt in range(6):
            try:
                yt.playlistItems().insert(part='snippet', body={'snippet': {
                    'playlistId': where[0], 'position': where[2],
                    'resourceId': {'kind': 'youtube#video', 'videoId': new}}}).execute()
                break
            except Exception as e:
                print('  playlist retry:', str(e)[-80:])
                time.sleep(8 * (attempt + 1))
        try:  # else a "[Deleted video]" entry stays behind; finish() double-checks via ensure_playlist
            yt.playlistItems().delete(id=where[1]).execute()
        except Exception as e:
            print('  old playlist entry not removed yet:', str(e)[-80:])
    finish(yt, name, old, new, pend, pend_path, m['publishAt'])


def ensure_playlist(yt, old, new):
    """Put `new` where `old` sits in its playlist (if it isn't there yet) and drop old's entry."""
    for pid in json.load(open(f'{OUT}/playlists.json')).values():
        items = yt.playlistItems().list(part='snippet', playlistId=pid, maxResults=50).execute()['items']
        olds = [i for i in items if i['snippet']['resourceId']['videoId'] == old]
        if not olds:
            continue
        if not any(i['snippet']['resourceId']['videoId'] == new for i in items):
            yt.playlistItems().insert(part='snippet', body={'snippet': {
                'playlistId': pid, 'position': olds[0]['snippet']['position'],
                'resourceId': {'kind': 'youtube#video', 'videoId': new}}}).execute()
        for i in olds:
            try:
                yt.playlistItems().delete(id=i['id']).execute()
            except Exception as e:  # already gone (the playlist list can lag a few seconds)
                print('  playlist entry already gone:', str(e)[-60:])


def finish(yt, name, old, new, pend, pend_path, publish_at=None):
    if yt.videos().list(part='id', id=old).execute()['items']:
        ensure_playlist(yt, old, new)  # a run cut short (quota, crash) may have skipped the playlist step
    for attempt in range(6):
        time.sleep(5)
        got = yt.videos().list(part='status', id=new).execute()['items']
        if got and got[0]['status'].get('publishAt') and publish_at in (None, got[0]['status']['publishAt']):
            break
    else:
        sys.exit(f'{name}: new upload {new} is not showing as scheduled yet; old {old} kept. Re-run to finish.')
    if yt.videos().list(part='id', id=old).execute()['items']:
        yt.videos().delete(id=old).execute()
    sched = 'channel/SCHEDULE.md'
    s = open(sched).read()
    open(sched, 'w').write(s.replace(old, new))
    del pend[name]
    json.dump(pend, open(pend_path, 'w'), indent=1)
    print(f'{name}: now https://youtu.be/{new} (old {old} deleted)')


if __name__ == '__main__':
    main()
