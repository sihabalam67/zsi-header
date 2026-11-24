"""Write channel/out/s01_grandpa.upload.json and channel/plans/s01.json after the render."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from s01_numbers import N  # noqa: E402

OUT = os.path.join(os.path.dirname(HERE), 'out')
chap = open(os.path.join(HERE, 'build', 's01', 'chapters.txt')).read().strip().splitlines()
chap[0] = '0:00 ' + chap[0].split(' ', 1)[1]
desc = f"""Thirty years ago, Grandpa Joe gave his three grandkids $1,000 each and one rule: come back in 30 years. Mia spent it. Ben hid it in a cookie jar. Rosie planted a "money tree": an index fund that owns America's 500 biggest companies. Who won? A money story for the whole family. The kids are made up; every number is real.

{chr(10).join(chap)}

The real numbers:
- $1,000 in the S&P 500 with dividends reinvested on Nov 25, 1996 was worth ${N['now']:,} on Nov 23, 2026 (before fees and taxes). Along the way it fell to ${N['d2002_low']:,} (Oct 2002), ${N['d2009_low']:,} (Mar 2009) and ${N['d2020_low']:,} (Mar 2020).
- Prices rose 2.13 times since Nov 1996 (CPI), so $1,000 in a jar now buys what ${N['jar_buys']} bought then.
- $100 a month from Oct 2007: ${N['dca_paid']:,} put in, worth ${N['dca_now']:,} today (it was ${N['dca_2009_worth']:,} on ${N['dca_2009_paid']:,} put in at the March 2009 low).

Which grandkid are you? Tell me in the comments.

Data: S&P 500 Total Return index (Yahoo Finance ^SP500TR); CPI-U, all items (U.S. Bureau of Labor Statistics via FRED, CPIAUCSL).

Past results don't promise future returns. This video is for education only and is not financial advice.
Original story, characters and animation. Narrated with an AI voice."""
json.dump(dict(video='channel/out/s01_grandpa.mp4', title="Grandpa Gave 3 Kids $1,000. Who Won?", description=desc,
               tags=['money story', 'compound interest', 'inflation explained', 'index fund', 'investing for beginners',
                     'money lesson for kids', 'family finance', 's&p 500', 'saving vs investing', 'coin theory'],
               categoryId=27, privacy='private', madeForKids=False, syntheticMedia=False, language='en',
               thumbnail='channel/out/thumbs/s01_grandpa_v4.jpg', captions='channel/out/s01_grandpa.en.srt'),
          open(os.path.join(OUT, 's01_grandpa.upload.json'), 'w'), indent=1)
json.dump({'videos': {'s01_grandpa': '2026-11-25T12:00'},
           'playlists': {'s01': ['Money Stories', 'Family-friendly money stories with real numbers.']},
           'launch_questions': {'s01_grandpa': 'Which grandkid are you: Mia, Ben, or Rosie?'}},
          open(os.path.join(os.path.dirname(HERE), 'plans', 's01.json'), 'w'), indent=1)
print(len(desc), 'chars;', chap)
