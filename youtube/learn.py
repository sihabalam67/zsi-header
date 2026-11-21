#!/usr/bin/env python3
"""What worked and what didn't: a scorecard of every long video, so each new video can be better than the last.

    python3 youtube/learn.py            # prints the scorecard, writes channel/out/learn.json

For each long video (from channel/out/video_ids.json, names without '_short_'):
- lifetime views and likes (Data API), and since publish (Analytics API): watch minutes, average view duration,
  average % viewed, subscribers gained, views in the first 3 days;
- where its views came from (traffic sources: suggested, browse, search, Shorts, ...);
- its audience retention curve: share of viewers still watching at 30 s, 1 min, 2 min, halfway, and the three
  steepest drops, matched to the video's chapters (channel/out/<ep>_chapters.txt) so we know which part lost people.
Impressions and click-through rate are not in the API (Studio only), so views in the first days stand in for the
title/thumbnail pull. Read-only; uses the same YT_* secrets as upload.py.
"""
import datetime as dt
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from upload import client  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'channel', 'out')


def chapters_for(name):
    ep = name.split('_')[0]
    for p in (os.path.join(OUT, f'{ep}_chapters.txt'), os.path.join(OUT, f'{name}_chapters.txt')):
        if os.path.exists(p):
            res = []
            for line in open(p):
                m = re.match(r'(\d+):(\d+)\s+(.*)', line.strip())
                if m:
                    res.append((int(m.group(1)) * 60 + int(m.group(2)), m.group(3)))
            return res
    return []


def chapter_at(chs, sec):
    name = None
    for at, n in chs:
        if sec >= at:
            name = n
    return name


def iso_seconds(d):
    m = re.fullmatch(r'P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', d)
    days, h, mi, s = (int(x or 0) for x in m.groups())
    return days * 86400 + h * 3600 + mi * 60 + s


def main():
    from googleapiclient.discovery import build
    yt = client()
    ya = build('youtubeAnalytics', 'v2', credentials=yt._http.credentials, cache_discovery=False)
    ids = json.load(open(os.path.join(OUT, 'video_ids.json')))
    longs = {n: v for n, v in ids.items() if '_short_' not in n and not n.startswith('sx')}
    meta = {}
    vids = list(longs.values())
    for i in range(0, len(vids), 50):
        for it in yt.videos().list(part='snippet,statistics,contentDetails,status', id=','.join(vids[i:i + 50])).execute()['items']:
            meta[it['id']] = it
    today = dt.date.today()
    rows = []
    for name, vid in longs.items():
        m = meta.get(vid)
        if not m or m['status'].get('privacyStatus') != 'public':
            continue
        pub = dt.date.fromisoformat(m['snippet']['publishedAt'][:10])
        if m['status'].get('publishAt'):
            pub = dt.date.fromisoformat(m['status']['publishAt'][:10])
        dur = iso_seconds(m['contentDetails']['duration'])
        base = dict(ids='channel==MINE', startDate=str(pub), endDate=str(today), filters=f'video=={vid}')
        r = (ya.reports().query(metrics='views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,'
                                       'subscribersGained,likes', **base).execute().get('rows') or [[0] * 6])[0]
        first3 = (ya.reports().query(metrics='views', **dict(base, endDate=str(min(today, pub + dt.timedelta(days=2))))
                                    ).execute().get('rows') or [[0]])[0][0]
        src = ya.reports().query(metrics='views,estimatedMinutesWatched', dimensions='insightTrafficSourceType',
                                 sort='-views', **base).execute().get('rows', [])
        ret = ya.reports().query(metrics='audienceWatchRatio', dimensions='elapsedVideoTimeRatio',
                                 **dict(base, filters=f'video=={vid};audienceType==ORGANIC')).execute().get('rows', [])
        curve = [(x * dur, y) for x, y in ret]

        def at(sec):
            pts = [y for s, y in curve if s <= sec]
            return round(pts[-1] * 100) if pts else None
        drops = sorted(((curve[i][1] - curve[i + 1][1], curve[i][0]) for i in range(len(curve) - 1)), reverse=True)
        chs = chapters_for(name)
        top_drops = [(round(d * 100, 1), round(s), chapter_at(chs, s)) for d, s in drops[:4] if s > 5][:3]
        rows.append(dict(name=name, id=vid, title=m['snippet']['title'], published=str(pub), days=(today - pub).days,
                         duration=dur, views_lifetime=int(m['statistics'].get('viewCount', 0)), views=r[0],
                         minutes=r[1], avg_view_s=r[2], avg_pct=round(r[3]), subs=r[4], likes=r[5], first3=first3,
                         sources={k: v for k, v, _ in src}, minutes_by_source={k: mm for k, _, mm in src},
                         kept_30s=at(30), kept_60s=at(60), kept_120s=at(120), kept_half=at(dur / 2),
                         drops=top_drops))
    rows.sort(key=lambda r: -r['minutes'])
    json.dump(rows, open(os.path.join(OUT, 'learn.json'), 'w'), indent=1)
    print(f"{'min':>5} {'views':>6} {'3day':>5} {'avg':>5} {'%':>3} {'30s':>4} {'1m':>4} {'2m':>4} {'subs':>4}  title")
    for r in rows:
        print(f"{r['minutes']:>5} {r['views_lifetime']:>6} {r['first3']:>5} {r['avg_view_s'] / 60:>4.1f}m {r['avg_pct']:>3}"
              f" {r['kept_30s'] or 0:>3}% {r['kept_60s'] or 0:>3}% {r['kept_120s'] or 0:>3}% {r['subs']:>4}  {r['title'][:70]}")
        top = sorted(r['sources'].items(), key=lambda kv: -kv[1])[:3]
        print(f"{'':>40}sources: {', '.join(f'{k} {v}' for k, v in top)}")
        if r['drops']:
            print(f"{'':>40}biggest drops: " + '; '.join(f'-{d}% at {s // 60}:{s % 60:02d} ({c})' for d, s, c in r['drops']))
    hours = sum(r['minutes'] for r in rows) / 60
    print(f'\nlong-video watch hours, all time: {hours:.1f} of 4,000')


if __name__ == '__main__':
    main()
