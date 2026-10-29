#!/usr/bin/env python3
"""Read-only channel report: per-video views, watch time, average view %, and subscribers gained.

    python3 youtube/stats.py [days]     # default: last 28 days
Uses the same YT_* environment secrets as upload.py.
"""
import datetime as dt
import sys

from upload import client


def main(days=28):
    from googleapiclient.discovery import build
    yt = client()
    creds = yt._http.credentials
    ya = build('youtubeAnalytics', 'v2', credentials=creds, cache_discovery=False)
    end = dt.date.today()
    start = end - dt.timedelta(days=days)
    rep = ya.reports().query(ids='channel==MINE', startDate=str(start), endDate=str(end),
                             metrics='views,estimatedMinutesWatched,averageViewPercentage,subscribersGained',
                             dimensions='video', sort='-views', maxResults=50).execute()
    rows = rep.get('rows', [])
    ids = [r[0] for r in rows]
    titles = {}
    if ids:
        for item in yt.videos().list(part='snippet', id=','.join(ids)).execute().get('items', []):
            titles[item['id']] = item['snippet']['title']
    print(f'Last {days} days ({start} to {end})')
    print(f"{'views':>8} {'minutes':>8} {'avg %':>6} {'subs':>5}  title")
    for vid, views, mins, avg, subs in rows:
        print(f'{views:>8} {mins:>8} {avg:>5.0f}% {subs:>5}  {titles.get(vid, vid)}')


if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 28)
