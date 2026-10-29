#!/usr/bin/env python3
"""ONE-TIME login. Run this on YOUR OWN computer (not in the cloud session).

It opens your browser, you approve access to your YouTube channel, and it prints a
refresh token. Store the three values it prints as secrets in the cloud environment
settings: YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN. Never paste them in chat.

Setup (about 10 minutes, free):
  1. https://console.cloud.google.com -> create a project (e.g. "coin-theory").
  2. APIs & Services -> Library -> enable "YouTube Data API v3" AND "YouTube Analytics API".
  3. APIs & Services -> OAuth consent screen -> External, add your own Google account
     under "Test users".
  4. APIs & Services -> Credentials -> Create credentials -> OAuth client ID ->
     Application type "Desktop app" -> download the JSON as client_secret.json
     next to this file.
  5. pip install google-auth-oauthlib
     python3 login.py
"""
import json
import os

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/youtube.upload',
          'https://www.googleapis.com/auth/youtube.force-ssl',        # captions, thumbnails, video settings
          'https://www.googleapis.com/auth/yt-analytics.readonly']    # read views, retention, CTR (read-only)

here = os.path.dirname(os.path.abspath(__file__))
flow = InstalledAppFlow.from_client_secrets_file(os.path.join(here, 'client_secret.json'), SCOPES)
creds = flow.run_local_server(port=0, access_type='offline', prompt='consent')
info = json.load(open(os.path.join(here, 'client_secret.json')))
info = info.get('installed') or info.get('web')
print('\nAdd these three as secrets in the cloud environment settings (not in chat):\n')
print('YT_CLIENT_ID     =', info['client_id'])
print('YT_CLIENT_SECRET =', info['client_secret'])
print('YT_REFRESH_TOKEN =', creds.refresh_token)
