#!/usr/bin/env python3
"""Daily launch helper: post launch comments when videos go public, list new viewer comments, reply to one.

    python3 youtube/daily.py                 # check launches, post due comments, list unanswered viewer comments
    python3 youtube/daily.py --reply ID TEXT # reply (as the channel) to the comment thread ID

Long videos get the question from channel/out/launch_comments.json; each Short gets a link to its long video.
YouTube's API can't pin comments or set a Short's "Related video", so those stay manual. Comments can only be
posted once a video is public. Progress is kept in channel/out/automation_log.json, so re-running is safe.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'youtube'))
from upload import client  # noqa: E402

OUT = os.path.join(ROOT, 'channel', 'out')
IDS = json.load(open(os.path.join(OUT, 'video_ids.json')))
QUESTIONS = json.load(open(os.path.join(OUT, 'launch_comments.json')))
LOG_PATH = os.path.join(OUT, 'automation_log.json')
LOG = json.load(open(LOG_PATH)) if os.path.exists(LOG_PATH) else {'commented': {}, 'replied': []}


def long_of(name):
    ep = name.split('_')[0]
    return next(n for n in IDS if n.startswith(ep) and '_short_' not in n)


def save():
    json.dump(LOG, open(LOG_PATH, 'w'), indent=1)


def post(yt, channel, vid, text):
    r = yt.commentThreads().insert(part='snippet', body={'snippet': {
        'channelId': channel, 'videoId': vid, 'topLevelComment': {'snippet': {'textOriginal': text}}}}).execute()
    return r['id']


def main():
    yt = client()
    channel = yt.channels().list(part='id', mine=True).execute()['items'][0]['id']
    if sys.argv[1:2] == ['--reply']:
        thread, text = sys.argv[2], ' '.join(sys.argv[3:])
        r = yt.comments().insert(part='snippet', body={'snippet': {'parentId': thread, 'textOriginal': text}}).execute()
        LOG['replied'].append(thread)
        save()
        print('replied', r['id'])
        return
    names = {v: k for k, v in IDS.items()}
    status = {}
    for i in range(0, len(IDS), 50):
        chunk = list(IDS.values())[i:i + 50]
        for v in yt.videos().list(part='status,statistics', id=','.join(chunk)).execute()['items']:
            status[names[v['id']]] = v
    public = [n for n in IDS if status[n]['status']['privacyStatus'] == 'public']
    for n in IDS:
        st = status[n]['status']
        print(f"{n:22s} {st['privacyStatus']:8s} {st.get('publishAt', '')[:16]:16s} "
              f"views={status[n].get('statistics', {}).get('viewCount', '0')}")
    for n in public:
        if n in LOG['commented']:
            continue
        text = QUESTIONS.get(n) or f"Watch the full video here: https://youtu.be/{IDS[long_of(n)]}"
        try:
            LOG['commented'][n] = post(yt, channel, IDS[n], text)
            save()
            print(f'POSTED launch comment on {n}: {text}')
        except Exception as e:
            print(f'could not comment on {n}: {str(e)[:200]}')
    print('\nUNANSWERED VIEWER COMMENTS')
    for n in public:
        try:
            threads = yt.commentThreads().list(part='snippet', videoId=IDS[n], maxResults=50,
                                               order='time').execute().get('items', [])
        except Exception as e:
            print(f'  ({n}: {str(e)[:120]})')
            continue
        for th in threads:
            top = th['snippet']['topLevelComment']['snippet']
            if top.get('authorChannelId', {}).get('value') == channel or th['id'] in LOG['replied']:
                continue
            print(f"  [{n}] thread={th['id']} by {top.get('authorDisplayName')}: {top.get('textOriginal')[:300]}")


if __name__ == '__main__':
    main()
