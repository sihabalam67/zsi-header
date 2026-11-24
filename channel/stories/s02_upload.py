"""Write channel/out/s02_salary.upload.json and channel/plans/s02.json after the render."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from s02_numbers import N  # noqa: E402

OUT = os.path.join(os.path.dirname(HERE), 'out')
chap = open(os.path.join(HERE, 'build', 's02', 'chapters.txt')).read().strip().splitlines()
chap[0] = '0:00 ' + chap[0].split(' ', 1)[1]
growth = N['now'] - N['paid']
desc = f"""Jay and Sam started the same job, on the same day, for the same salary. Ten years later, one of them has ${N['now']:,}. The other is standing at his door at midnight, asking for help. It came down to one little box on one boring form. A money story about friendship, car payments, credit cards, a layoff, a wedding... and the red SELL button.

{chr(10).join(chap)}

The real numbers behind the story:
- Sam puts 6% of a $60,000 salary ($300/month) into his 401(k); the company adds half ($150/month). Invested in the S&P 500 with dividends from Feb 2016 to Nov 2026 (paused Apr-Aug 2020 while laid off): ${N['own_paid']:,} of his money + ${N['match_paid']:,} free match = ${N['now']:,} (before fees and taxes). The free match alone grew to ${N['match_now']:,}.
- March 23, 2020: the account fell to ${N['low_2020']:,} from about ${N['peak_2020']:,} in February.
- Jay's $40,000 car at the 2017 average new-car loan rate ({N['car_rate']}%), 72 months: ${N['car_pay']}/month, ${N['car_interest']:,} interest.
- A $6,000 card balance at today's average card rate ({N['card_apr']}%), paying only the minimum (interest + 1%): {N['card_years']} years and ${N['card_interest']:,} in interest.

Are you Jay or Sam? Tell me in one word.

Data: S&P 500 Total Return index (Yahoo Finance ^SP500TR); Federal Reserve G.19 via FRED (TERMCBCCINTNS card APR, TERMCBAUTO48NS new-car loan rate).

Jay, Sam and their choices are made up; the rates and market returns are real. Past results don't promise future returns. Education only, not financial advice.
Original story, characters and animation. Voices are AI."""
json.dump(dict(video='channel/out/s02_salary.mp4', title="Same Salary. 10 Years Later, One Is Broke.", description=desc,
               tags=['money story', '401k match', 'lifestyle creep', 'credit card debt', 'car payment', 'same salary different life',
                     'personal finance', 'saving vs spending', 'investing for beginners', 'coin theory'],
               categoryId=27, privacy='private', madeForKids=False, syntheticMedia=False, language='en',
               thumbnail='channel/out/thumbs/s02_salary_v5.jpg', captions='channel/out/s02_salary.en.srt'),
          open(os.path.join(OUT, 's02_salary.upload.json'), 'w'), indent=1)
json.dump({'videos': {'s02_salary': '2026-11-27T12:00'},
           'playlists': {'s02': ['Money Stories', 'Family-friendly money stories with real numbers.']},
           'launch_questions': {'s02_salary': 'One word: are you Jay or Sam?'}},
          open(os.path.join(os.path.dirname(HERE), 'plans', 's02.json'), 'w'), indent=1)
print(len(desc), 'chars;', chap)
