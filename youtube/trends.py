#!/usr/bin/env python3
"""What's working right now: recent videos on our topics ranked by views per day (YouTube Data API, free quota).

    python3 youtube/trends.py                       # default money topics, last 14 days
    python3 youtube/trends.py "gas prices" "fed rate hike" --days 7 --shorts

Prints top videos with views/day, length, and title, plus title patterns (numbers, questions, length) among the
leaders. Uses only public metadata; nothing is downloaded. Each search costs 100 quota units of the daily 10,000.
"""
import datetime as dt
import re
import sys

from upload import client

DEFAULT = ['gas prices', 'fed rate hike', 'inflation explained', 'housing market', 'credit card interest',
           'recession 2026', 'mortgage rates', 'savings account interest']


def iso_seconds(d):
    m = re.fullmatch(r'P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', d)
    days, h, mi, s = (int(x or 0) for x in m.groups())
    return days * 86400 + h * 3600 + mi * 60 + s


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    days = int(sys.argv[sys.argv.index('--days') + 1]) if '--days' in sys.argv else 14
    if '--days' in sys.argv:
        args.remove(str(days))
    shorts = '--shorts' in sys.argv
    topics = args or DEFAULT
    yt = client()
    since = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days)).strftime('%Y-%m-%dT%H:%M:%SZ')
    seen, rows = set(), []
    for q in topics:
        res = yt.search().list(part='id', q=q, type='video', order='viewCount', publishedAfter=since,
                               regionCode='US', relevanceLanguage='en', maxResults=25,
                               videoDuration='short' if shorts else 'any').execute()
        ids = [i['id']['videoId'] for i in res.get('items', []) if i['id']['videoId'] not in seen]
        seen.update(ids)
        if not ids:
            continue
        for v in yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(ids)).execute()['items']:
            age = (dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(
                v['snippet']['publishedAt'].replace('Z', '+00:00'))).total_seconds() / 86400
            views = int(v['statistics'].get('viewCount', 0))
            t = v['snippet']['title']
            if '--en' in sys.argv and (re.search(r'[^\x00-\x7F\u2018-\u201f\u2026\u2013\u2014\U0001F000-\U0001FFFF\u2600-\u27BF\uFE0F]', t)
                                       or re.search(r'₹|\blakh|\bcrore|\bindia|\bsbi\b|\brupee', t, re.I)
                                       or v['snippet'].get('defaultAudioLanguage', 'en')[:2] not in ('en', '')):
                continue
            rows.append(dict(topic=q, title=v['snippet']['title'], channel=v['snippet']['channelTitle'],
                             vpd=views / max(age, 0.5), views=views, secs=iso_seconds(v['contentDetails']['duration']),
                             likes=int(v['statistics'].get('likeCount', 0)),
                             comments=int(v['statistics'].get('commentCount', 0)), id=v['id']))
    rows.sort(key=lambda r: -r['vpd'])
    print(f'Top recent videos (last {days} days, {"Shorts" if shorts else "all lengths"}), ranked by views/day\n')
    for r in rows[:30]:
        print(f"{r['vpd']:>10,.0f}/day {r['views']:>11,} views {r['secs'] // 60:>3}:{r['secs'] % 60:02d}  "
              f"[{r['topic']}] {r['title'][:90]}  ({r['channel']})")
    top = rows[:30]
    if top:
        num = sum(bool(re.search(r'\d', r['title'])) for r in top)
        qs = sum('?' in r['title'] for r in top)
        caps = sum(bool(re.search(r'\b[A-Z]{3,}\b', r['title'])) for r in top)
        avg_len = sum(len(r['title']) for r in top) / len(top)
        long_share = sum(r['secs'] >= 480 for r in top)
        print(f'\nPatterns in the top {len(top)}: {num} titles have a number, {qs} ask a question, {caps} use a '
              f'CAPS word; average title {avg_len:.0f} characters; {long_share} are 8+ minutes long.')
        by_topic = {}
        for r in rows:
            by_topic.setdefault(r['topic'], []).append(r['vpd'])
        print('\nDemand by topic (median views/day of its top results):')
        for t, v in sorted(by_topic.items(), key=lambda kv: -sorted(kv[1])[len(kv[1]) // 2]):
            print(f'  {sorted(v)[len(v) // 2]:>10,.0f}/day  {t}')


if __name__ == '__main__':
    main()
