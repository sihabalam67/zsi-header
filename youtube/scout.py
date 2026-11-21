#!/usr/bin/env python3
"""Topic scout: how many ordinary people are watching a topic on YouTube right now, and can a small channel win it?

    python3 youtube/scout.py "thanksgiving dinner cost" "black friday deals" "social security 2027" ...
    python3 youtube/scout.py --default        # a broad list of everyday-money topics

For each topic (YouTube Data API search, last 7 days, long videos 4-20 min, US English):
- demand  = median views per day of the top 15 recent videos (how many people watch this topic now)
- top     = views/day of the best recent video (the ceiling)
- small   = how many of the top 15 come from channels with under 50k subscribers (can a small channel rank?)
- score   = demand x (1 + small/15): high demand and room for small channels both push it up
Prints topics ranked by score and writes channel/out/scout.json. Each topic costs ~101 quota units (10,000/day).
"""
import datetime as dt
import json
import os
import re
import statistics as st
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from upload import client  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT = ['stock market crash', 'gas prices', 'grocery prices', 'thanksgiving dinner cost', 'black friday deals',
           'social security increase', 'tax refund 2027', 'mortgage rates', 'rent prices', 'minimum wage increase',
           'credit card debt', 'layoffs 2026', 'gold price', 'bitcoin crash', 'recession 2026', 'egg prices',
           'car prices', 'student loans', 'tariffs prices', 'housing market crash']


def iso_seconds(d):
    m = re.fullmatch(r'P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', d)
    days, h, mi, s = (int(x or 0) for x in m.groups())
    return days * 86400 + h * 3600 + mi * 60 + s


def scout(yt, q, days=7):
    since = (dt.datetime.now(dt.UTC).replace(tzinfo=None) - dt.timedelta(days=days)).strftime('%Y-%m-%dT%H:%M:%SZ')
    r = yt.search().list(part='id', q=q, type='video', order='viewCount', publishedAfter=since, maxResults=50,
                         videoDuration='medium', relevanceLanguage='en', regionCode='US').execute()
    ids = [i['id']['videoId'] for i in r.get('items', [])]
    if not ids:
        return None
    vids = yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(ids)).execute()['items']
    chans = {v['snippet']['channelId'] for v in vids}
    subs = {}
    cl = list(chans)
    for i in range(0, len(cl), 50):
        for c in yt.channels().list(part='statistics', id=','.join(cl[i:i + 50])).execute()['items']:
            subs[c['id']] = int(c['statistics'].get('subscriberCount', 0) or 0)
    now = dt.datetime.now(dt.UTC).replace(tzinfo=None)
    rows = []
    for v in vids:
        age = max(0.5, (now - dt.datetime.strptime(v['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')).total_seconds() / 86400)
        vpd = int(v['statistics'].get('viewCount', 0)) / age
        rows.append(dict(title=v['snippet']['title'], channel=v['snippet']['channelTitle'],
                         subs=subs.get(v['snippet']['channelId'], 0), vpd=round(vpd),
                         minutes=round(iso_seconds(v['contentDetails']['duration']) / 60, 1)))
    rows = [x for x in rows if sum(c.isascii() for c in x['title']) / max(1, len(x['title'])) > 0.95]
    if not rows:
        return None
    rows.sort(key=lambda x: -x['vpd'])
    top = rows[:15]
    demand = st.median([x['vpd'] for x in top])
    small = sum(x['subs'] < 50000 for x in top)
    return dict(topic=q, demand=round(demand), top=top[0]['vpd'], small=small, score=round(demand * (1 + small / 15)),
                examples=top[:3])


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    topics = DEFAULT if ('--default' in sys.argv or not args) else args
    yt = client()
    res = []
    for q in topics:
        try:
            r = scout(yt, q)
        except Exception as e:  # quota or a transient error: keep going
            print(f'{q}: error {str(e)[:80]}')
            continue
        if r:
            res.append(r)
    res.sort(key=lambda r: -r['score'])
    json.dump(dict(date=str(dt.date.today()), results=res), open(os.path.join(ROOT, 'channel', 'out', 'scout.json'), 'w'),
              indent=1)
    print(f"{'score':>8} {'demand/day':>10} {'best/day':>9} {'small':>5}  topic")
    for r in res:
        print(f"{r['score']:>8} {r['demand']:>10} {r['top']:>9} {r['small']:>3}/15  {r['topic']}")
        for e in r['examples'][:2]:
            print(f"{'':>36}{e['vpd']:>8}/day  {e['subs']:>9} subs  {e['title'][:70]}")


if __name__ == '__main__':
    main()
