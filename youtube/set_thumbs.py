#!/usr/bin/env python3
"""Set the chosen v3 thumbnail on every video and record it in its upload kit.

    python3 youtube/set_thumbs.py [--dry-run]
Choice per video (A = shock number, B = curiosity word, C = face + "you" question). Long videos start on A; the
owner can run YouTube Studio's Test & Compare with all three (out/thumbs/<name>_[abc].jpg).
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'youtube'))
os.chdir(ROOT)
from googleapiclient.http import MediaFileUpload  # noqa: E402
from upload import client  # noqa: E402

CHOICE = {
    'ep01_short_prices': 'c', 'ep01_short_rule70': 'c', 'ep01_short_wages': 'c', 'ep02_short_payment': 'c',
    'ep02_short_price': 'c', 'ep02_short_supply': 'a', 'ep03_short_barrel': 'c', 'ep03_short_feathers': 'c',
    'ep03_short_jump': 'a', 'ep04_short_cards': 'c', 'ep04_short_savings': 'c', 'ep04_short_why': 'a',
    'ep05_short_hiring': 'c', 'ep05_short_layoffs': 'a', 'ep06_short_banks': 'a', 'ep07_short_hack': 'a',
    'ep08_short_midterms': 'a', 'sx01_short_compound': 'c', 'sx02_short_cards': 'c', 'sx03_short_1962': 'a',
    'sx04_short_middle': 'b', 'sx10_short_midterm_stocks': 'a', 'sx11_short_election_rally': 'a', 'sx12_short_hens': 'a',
    'ep01_inflation': 'a', 'ep02_housing': 'a', 'ep03_gas': 'a', 'ep04_fed': 'a', 'ep05_jobs': 'a',
    'ep07_binance_long': 'a', 'ep08_midterms': 'a',
}

if __name__ == '__main__':
    dry = '--dry-run' in sys.argv
    ids = json.load(open('channel/out/video_ids.json'))
    yt = None if dry else client()
    for name, v in CHOICE.items():
        img = f'channel/out/thumbs/{name}_{v}.jpg'
        assert os.path.exists(img) and os.path.getsize(img) < 2_000_000, img
        vid = ids[name]
        if not dry:
            yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(img, mimetype='image/jpeg')).execute()
            kit = f'channel/out/{name}.upload.json'
            k = json.load(open(kit))
            k['thumbnail'] = img
            json.dump(k, open(kit, 'w'), indent=1)
        print('set' if not dry else 'would set', name, vid, img)
