"""Write channel/out/s03_janitor.upload.json and channel/plans/s02.json after the render."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from s03_numbers import N  # noqa: E402

OUT = os.path.join(os.path.dirname(HERE), 'out')
chap = open(os.path.join(HERE, 'build', 's03', 'chapters.txt')).read().strip().splitlines()
chap[0] = '0:00 ' + chap[0].split(' ', 1)[1]
desc = f"""Walter was the school janitor. Same mop, same coat with eleven safety pins, soup every night. When he died, his will left ${N['now']:,} to the town library and the children's hospital. How? His neighbor Lily gets a key to box 467, and inside are the clues: a notebook, a 1987 crash newspaper, 467 envelopes, and a birthday card with her name on it. A money mystery for the whole family.

{chr(10).join(chap)}

The real numbers behind the story:
- ${N['monthly']} every month from Jan 1988 to Nov 2026 ({N['months']} months, ${N['paid_monthly']:,}) into an S&P 500 index fund with dividends reinvested, plus $5,000 at each of three crash lows: Oct 9, 2002 (now ${N['c2002']:,}), Mar 9, 2009 (now ${N['c2009']:,}) and Mar 23, 2020 (now ${N['c2020']:,}). Total put in ${N['paid']:,}; worth ${N['now']:,} on Nov 23, 2026 (before fees and taxes).
- Balance in Nov 1996: ${N['v1996']:,}; Nov 2006: ${N['v2006']:,}; Nov 2016: ${N['v2016']:,}. {N['last10_share']}% of the money appeared in the last 10 years.
- Black Monday, Oct 19, 1987: the S&P 500 fell {abs(N['black_monday'])}% in one day.
- $1,000 invested on June 1, 1998 is worth ${N['gift']:,} today.
- Real people have done this: in 2014 a Vermont janitor left about $8 million, much of it to his town's library and hospital (widely reported in 2015).

Could you live like Walter for 10 years? Yes or no?

Data: S&P 500 Total Return index (Yahoo Finance ^SP500TR); S&P 500 daily closes (Yahoo Finance ^GSPC).

Walter, Lily and Derek are made up; the market returns are real. Past results don't promise future returns. Education only, not financial advice.
Original story, characters and animation. Voices are AI."""
json.dump(dict(video='channel/out/s03_janitor.mp4', title="The Poorest Man in Town Left $2 Million. How?", description=desc,
               tags=['money story', 'millionaire next door', 'janitor millionaire', 'index fund', 'compound interest', 'dollar cost averaging',
                     'black monday 1987', 'investing for beginners', 'money mystery', 'coin theory'],
               categoryId=27, privacy='private', madeForKids=False, syntheticMedia=False, language='en',
               thumbnail='channel/out/thumbs/s03_janitor_v5.jpg', captions='channel/out/s03_janitor.en.srt'),
          open(os.path.join(OUT, 's03_janitor.upload.json'), 'w'), indent=1)
json.dump({'videos': {'s03_janitor': '2026-11-29T12:00'},
           'playlists': {'s03': ['Money Stories', 'Family-friendly money stories with real numbers.']},
           'launch_questions': {'s03_janitor': 'Could you live like Walter for 10 years? Yes or no?'}},
          open(os.path.join(os.path.dirname(HERE), 'plans', 's03.json'), 'w'), indent=1)
print(len(desc), 'chars;', chap)
