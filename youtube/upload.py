#!/usr/bin/env python3
"""Upload a video (plus thumbnail and captions) described by a JSON manifest.

    python3 youtube/upload.py channel/out/ep01_upload.json            # upload
    python3 youtube/upload.py channel/out/ep01_upload.json --dry-run  # validate only

Credentials come from the environment: YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN
(see youtube/login.py). Videos uploaded by a new, unaudited API project are locked to
private by YouTube until the project passes Google's free audit, so everything uploads
as private (or scheduled with publishAt once audited) and you flip it to public in Studio.

Manifest fields: video, title, description, tags, categoryId, thumbnail, captions,
privacy ("private" | "unlisted" | "public"), publishAt (RFC 3339, optional),
madeForKids (bool), syntheticMedia (bool), language.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def client():
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    missing = [k for k in ('YT_CLIENT_ID', 'YT_CLIENT_SECRET', 'YT_REFRESH_TOKEN') if not os.environ.get(k)]
    if missing:
        sys.exit(f'Missing environment secrets: {", ".join(missing)} (see youtube/login.py)')
    creds = Credentials(None, refresh_token=os.environ['YT_REFRESH_TOKEN'],
                        client_id=os.environ['YT_CLIENT_ID'], client_secret=os.environ['YT_CLIENT_SECRET'],
                        token_uri='https://oauth2.googleapis.com/token')
    return build('youtube', 'v3', credentials=creds, cache_discovery=False)


def path(p):
    return p if os.path.isabs(p) else os.path.join(ROOT, p)


def validate(m):
    errors = []
    for key in ('video', 'title', 'description'):
        if not m.get(key):
            errors.append(f'missing {key}')
    for key in ('video', 'thumbnail', 'captions'):
        if m.get(key) and not os.path.exists(path(m[key])):
            errors.append(f'{key} file not found: {m[key]}')
    for key in ('title', 'description'):
        if '<' in m.get(key, '') or '>' in m.get(key, ''):
            errors.append(f'{key} contains < or > (YouTube rejects them)')
    if len(m.get('title', '')) > 100:
        errors.append('title over 100 characters')
    if len(m.get('description', '').encode()) > 5000:
        errors.append('description over 5000 bytes')
    if len(','.join(m.get('tags', []))) > 500:
        errors.append('tags over 500 characters total')
    if m.get('thumbnail') and os.path.getsize(path(m['thumbnail'])) > 2 * 1024 * 1024:
        errors.append('thumbnail over 2 MB')
    return errors


def upload(m):
    from googleapiclient.http import MediaFileUpload
    yt = client()
    status = {'privacyStatus': m.get('privacy', 'private'), 'selfDeclaredMadeForKids': m.get('madeForKids', False),
              'containsSyntheticMedia': m.get('syntheticMedia', True)}
    if m.get('publishAt'):
        status.update(privacyStatus='private', publishAt=m['publishAt'])
    body = {'snippet': {'title': m['title'], 'description': m['description'], 'tags': m.get('tags', []),
                        'categoryId': str(m.get('categoryId', 27)), 'defaultLanguage': m.get('language', 'en'),
                        'defaultAudioLanguage': m.get('language', 'en')},
            'status': status}
    req = yt.videos().insert(part='snippet,status', body=body,
                             media_body=MediaFileUpload(path(m['video']), chunksize=8 * 1024 * 1024, resumable=True))
    resp = None
    while resp is None:
        st, resp = req.next_chunk()
        if st:
            print(f'  uploading {st.progress() * 100:.0f}%', flush=True)
    vid = resp['id']
    print('uploaded: https://youtu.be/' + vid)
    if m.get('thumbnail'):
        try:
            yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(path(m['thumbnail']))).execute()
            print('thumbnail set')
        except Exception as e:  # custom thumbnails need a phone-verified channel
            print('thumbnail skipped:', e)
    if m.get('captions'):
        yt.captions().insert(part='snippet', body={'snippet': {'videoId': vid, 'language': m.get('language', 'en'),
                                                               'name': 'English', 'isDraft': False}},
                             media_body=MediaFileUpload(path(m['captions']))).execute()
        print('captions added')
    return vid


if __name__ == '__main__':
    manifest = json.load(open(sys.argv[1]))
    errs = validate(manifest)
    if errs:
        sys.exit('manifest problems: ' + '; '.join(errs))
    print('manifest OK:', manifest['title'])
    if '--dry-run' not in sys.argv:
        upload(manifest)
