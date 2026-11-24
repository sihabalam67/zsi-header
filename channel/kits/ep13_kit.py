"""Write channel/out/ep13_groceries.upload.json from the script's numbers and the rendered chapters."""
import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
import ep13_groceries as e  # noqa: E402

chapters = open(os.path.join(HERE, 'out', 'ep13_chapters.txt')).read().strip()
P = e.PRICES
desc = (
    f"U.S. grocery prices (CPI food at home) are up {e.FOOD_UP:.1f}% since January 2020, and this year's classic "
    f"Thanksgiving dinner for 10 costs ${e.DINNER_TOTAL:.2f}, more than 6% above last year, with the 16-lb turkey up "
    f"10%, per the American Farm Bureau. Coffee is up {P['Coffee']['up']:.0f}% (${P['Coffee']['then']:.2f} to "
    f"${P['Coffee']['now']:.2f} a pound), ground beef {P['Ground beef']['up']:.0f}%, eggs {P['Eggs']['up']:.0f}% "
    f"after peaking at ${P['Eggs']['peak']:.2f} a dozen. We look at why food costs more (fuel, labor, packaging: "
    f"under 6 cents of each grocery dollar reaches the farm), groceries vs your other bills, and whether pay kept up "
    f"(average hourly pay +{e.PAY_UP:.1f}%).\n\n{chapters}\n\n"
    "Sources: BLS consumer price indexes and average prices via FRED (CUSR0000SAF11, CPIAUCSL, CUSR0000SEFV, "
    "CUSR0000SEHA, CUSR0000SEHF01, CUSR0000SETA02, APU0000717311, APU0000703112, APU0000708111, APU0000702111, "
    "APU0000709112, APU0000711211), BLS average hourly earnings (CES0500000003), EIA weekly gas price (GASREGW), "
    "Federal Reserve G.19 credit card rate (TERMCBCCINTNS); American Farm Bureau Federation 2026 Thanksgiving dinner "
    "survey (Nov 18, 2026). Data through October 2026 unless noted. The $150-a-week cart and $500 card balance are "
    "worked examples.\n\n"
    "Watch next: what the stock market drop means for you https://youtu.be/w8y0rEUenp4\n\n"
    "This video is for education only and is not financial advice.\nOriginal script and animation; AI-generated "
    "photos (no real people or brands). Narrated with an AI voice.")
kit = {
    'video': 'channel/out/ep13_groceries.mp4',
    'title': 'Your Groceries Cost 32% More. Why?',
    'description': desc,
    'tags': ['grocery prices', 'why are groceries so expensive', 'thanksgiving dinner cost 2026', 'food prices',
             'grocery prices 2026', 'coffee prices', 'beef prices', 'egg prices', 'inflation', 'cost of living',
             'thanksgiving 2026', 'black friday', 'credit card interest', 'save money on groceries', 'coin theory',
             'money explained', 'personal finance'],
    'categoryId': 27,
    'thumbnail': 'channel/out/thumbs/ep13_groceries_a.jpg',
    'captions': 'channel/out/ep13_groceries.en.srt',
    'privacy': 'private',
    'madeForKids': False,
    'syntheticMedia': False,
    'language': 'en',
}
json.dump(kit, open(os.path.join(HERE, 'out', 'ep13_groceries.upload.json'), 'w'), indent=1)
print(kit['title'], len(desc), 'chars')
