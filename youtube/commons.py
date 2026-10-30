#!/usr/bin/env python3
"""Find and download copyright-free photos (public domain or CC0 only) from Wikimedia Commons.

    python3 youtube/commons.py search "Eccles Federal Reserve building" [--min 1600]
    python3 youtube/commons.py get "File:Name.jpg" channel/assets/photos/fed.jpg

Every download is logged with its source page and license in channel/assets/photos/SOURCES.md.
"""
import json
import os
import re
import sys
import urllib.parse
import urllib.error
import urllib.request

API = 'https://commons.wikimedia.org/w/api.php'
UA = {'User-Agent': 'CoinTheoryBot/1.0 (educational YouTube channel; contact via channel)'}
FREE = re.compile(r'^(public domain|pd[- ].*|cc0.*|cc-zero)$', re.I)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def api(**p):
    import time
    p.update(format='json')
    req = urllib.request.Request(API + '?' + urllib.parse.urlencode(p), headers=UA)
    for attempt in range(5):
        try:
            return json.load(urllib.request.urlopen(req, timeout=30))
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            time.sleep(5 * (attempt + 1))  # Commons asks clients to slow down; be polite
    raise RuntimeError('Wikimedia Commons keeps rate-limiting; try again later')


def search(q, min_w=1600, n=40):
    r = api(action='query', generator='search', gsrsearch=f'{q} filetype:bitmap', gsrnamespace=6, gsrlimit=n,
            prop='imageinfo', iiprop='url|size|extmetadata')
    out = []
    for p in (r.get('query') or {}).get('pages', {}).values():
        ii = p['imageinfo'][0]
        lic = ii.get('extmetadata', {}).get('LicenseShortName', {}).get('value', '')
        if FREE.match(lic.strip()) and ii['width'] >= min_w:
            out.append((p['title'], ii['width'], ii['height'], lic, ii['url']))
    return out


def get(title, dest):
    r = api(action='query', titles=title, prop='imageinfo', iiprop='url|extmetadata', iiurlwidth=2560)
    ii = next(iter(r['query']['pages'].values()))['imageinfo'][0]  # thumburl: a 2560 px rendition, as Commons asks
    lic = ii['extmetadata'].get('LicenseShortName', {}).get('value', '')
    assert FREE.match(lic.strip()), f'not public domain / CC0: {lic}'
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    req = urllib.request.Request(ii.get('thumburl') or ii['url'], headers=UA)
    data = urllib.request.urlopen(req, timeout=60).read()
    open(dest, 'wb').write(data)
    page = 'https://commons.wikimedia.org/wiki/' + urllib.parse.quote(title.replace(' ', '_'))
    log = os.path.join(ROOT, 'channel', 'assets', 'photos', 'SOURCES.md')
    with open(log, 'a') as f:
        f.write(f'- {os.path.basename(dest)}: {page} ({lic})\n')
    print('saved', dest, lic)


if __name__ == '__main__':
    if sys.argv[1] == 'search':
        mw = int(sys.argv[sys.argv.index('--min') + 1]) if '--min' in sys.argv else 1600
        for t in search(sys.argv[2], mw):
            print(f'{t[1]}x{t[2]}  {t[3]:18s} {t[0]}')
    else:
        get(sys.argv[2], sys.argv[3])
