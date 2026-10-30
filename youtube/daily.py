#!/usr/bin/env python3
"""Daily launch helper: post launch comments when videos go public, list new viewer comments, reply to one.

    python3 youtube/daily.py                 # check launches, post due comments, list unanswered viewer comments
    python3 youtube/daily.py --reply ID TEXT # reply (as the channel) to the comment thread ID
    python3 youtube/daily.py --reply ID TEXT --for CID  # same, answering viewer reply CID inside that thread

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
    return next(n for n in IDS if n.startswith(ep + '_') and '_short_' not in n)


def save():
    json.dump(LOG, open(LOG_PATH, 'w'), indent=1)


def post(yt, channel, vid, text):
    r = yt.commentThreads().insert(part='snippet', body={'snippet': {
        'channelId': channel, 'videoId': vid, 'topLevelComment': {'snippet': {'textOriginal': text}}}}).execute()
    return r['id']


def author(c):
    return c['snippet'].get('authorChannelId', {}).get('value')


def text(c):
    sn = c['snippet']
    return sn.get('textOriginal') or sn.get('textDisplay') or ''


def all_threads(yt, vid, **kw):
    items, token = [], None
    while True:
        r = yt.commentThreads().list(part='snippet', videoId=vid, maxResults=100, textFormat='plainText',
                                     pageToken=token, **kw).execute()
        items += r.get('items', [])
        token = r.get('nextPageToken')
        if not token:
            return items


def main():
    yt = client()
    channel = yt.channels().list(part='id', mine=True).execute()['items'][0]['id']
    if sys.argv[1:2] == ['--reply']:
        args = sys.argv[2:]
        target = None
        if '--for' in args:
            i = args.index('--for')
            target = args[i + 1]
            del args[i:i + 2]
        thread, msg = args[0], ' '.join(args[1:])
        if target:  # @mention the viewer so YouTube notifies them of the answer
            who = yt.comments().list(part='snippet', id=target).execute()['items'][0]['snippet']['authorDisplayName']
            if who and not msg.startswith(who):
                msg = f'{who} {msg}'
        r = yt.comments().insert(part='snippet', body={'snippet': {'parentId': thread, 'textOriginal': msg}}).execute()
        LOG['replied'].append(target or thread)
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
        if n in QUESTIONS:
            msg = QUESTIONS[n]
        elif '_short_' in n:
            msg = f"Watch the full video here: https://youtu.be/{IDS[long_of(n)]}"
        else:  # a long video without a written question still gets a real conversation starter
            msg = "What surprised you most in this video? Tell me in the comments, I read every one."
            print(f'NOTE: no launch question for {n}; add one to channel/out/launch_comments.json')
        try:
            LOG['commented'][n] = post(yt, channel, IDS[n], msg)
            save()
            print(f'POSTED launch comment on {n}: {msg}')
        except Exception as e:
            print(f'could not comment on {n}: {str(e)[:200]}')
    print('\nUNANSWERED VIEWER COMMENTS')
    held = []
    for n in public:
        try:
            threads = all_threads(yt, IDS[n])
            held += [(n, th) for th in all_threads(yt, IDS[n], moderationStatus='heldForReview')]
        except Exception as e:
            print(f'  ({n}: {str(e)[:120]})')
            continue
        for th in threads:
            # a viewer message needs an answer unless we logged a reply to it or the channel spoke after it
            msgs = [th['snippet']['topLevelComment']]
            if th['snippet'].get('totalReplyCount'):
                msgs += yt.comments().list(part='snippet', parentId=th['id'], maxResults=100,
                                           textFormat='plainText').execute()['items']
            msgs.sort(key=lambda c: c['snippet']['publishedAt'])
            ours = [c for c in msgs if author(c) == channel]
            for c in msgs:
                if author(c) == channel or c['id'] in LOG['replied']:
                    continue
                name, at = c['snippet'].get('authorDisplayName', ''), c['snippet']['publishedAt']
                # answered by hand in Studio: a later channel reply that @mentions them, or any channel reply to
                # a viewer's own top-level comment
                later = [o for o in ours if o['snippet']['publishedAt'] > at]
                if any(name and name in text(o) for o in later) or (c['id'] == th['id'] and later):
                    continue
                where = f"thread={th['id']}" + ('' if c['id'] == th['id'] else f" --for {c['id']}")
                print(f"  [{n}] {where} by {c['snippet'].get('authorDisplayName')}: {text(c)[:300]}")
    if held:
        print('\nHELD FOR REVIEW (YouTube hid these; approve or remove them in Studio > Comments > Held for review)')
        for n, th in held:
            c = th['snippet']['topLevelComment']
            print(f"  [{n}] by {c['snippet'].get('authorDisplayName')}: {text(c)[:200]}")


if __name__ == '__main__':
    main()
