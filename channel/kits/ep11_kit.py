"""Write channel/out/ep11_vix.upload.json from the script's numbers and the rendered chapters."""
import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
import ep11_vix as e  # noqa: E402

chapters = open(os.path.join(HERE, 'out', 'ep11_chapters.txt')).read().strip()
desc = (
    f"Wall Street's fear index, the Cboe Volatility Index (VIX), closed at {e.V_NOW:.2f} on Nov 20, 2026, up from "
    f"{e.V_AT_REC:.2f} on Oct 6, the day the S&P 500 set its record. The S&P 500 fell {e.STREAK} days in a row to "
    f"{e.SP_NOW:,.2f}, {abs(e.SP_DD):.1f}% below that record. We explain what the VIX measures, how rare readings "
    f"like this are (30+ on about {e.SHARE30:.0f}% of days since 1990), and what the S&P 500 did after each of the "
    f"{len(e.PAST)} times since 1990 that the VIX first closed above 30: higher a month later {e.UP1} of {len(e.F1)} "
    f"times, higher a year later {e.UP12} of {len(e.F12)} times (median {e.MED12:+.0f}%), with 2008 as the big "
    f"exception.\n\n{chapters}\n\n"
    "Sources: Yahoo Finance daily closes for the Cboe Volatility Index (^VIX, from 1990), the S&P 500 (^GSPC) and the "
    "Nasdaq Composite (^IXIC), saved Nov 20, 2026 after the close. FRED (Federal Reserve Bank of St. Louis): DGS10 "
    "(10-year Treasury yield), CPIAUCSL (CPI). Spike and return statistics are our calculations, prices only (no "
    "dividends). A 'first spike' is the first close at 30 or higher after at least 60 trading days below 30.\n\n"
    "Watch next: Stocks fell 6 days in a row. Is a crash coming? https://youtu.be/lmXODEAxdJc\n\n"
    "This video is for education only and is not financial advice. Past performance does not guarantee future "
    "results.\nOriginal script and animation. Narrated with an AI voice.")
kit = {
    'video': 'channel/out/ep11_vix.mp4',
    'title': f"Wall Street's Fear Index Just {e.DOUBLED.title()}. What Happens Next?",
    'description': desc,
    'tags': ['vix', 'vix explained', 'fear index', 'what is the vix', 'stock market volatility', 'stock market today',
             'stock market crash', 'stock market correction', 's&p 500', 'cboe volatility index', 'stock market 2026',
             'is a crash coming', 'coin theory', 'money explained', 'personal finance'],
    'categoryId': 27,
    'thumbnail': 'channel/out/thumbs/ep11_vix_b.jpg',
    'captions': 'channel/out/ep11_vix.en.srt',
    'privacy': 'private',
    'madeForKids': False,
    'syntheticMedia': False,
    'language': 'en',
}
json.dump(kit, open(os.path.join(HERE, 'out', 'ep11_vix.upload.json'), 'w'), indent=1)
print(kit['title'], len(desc), 'chars')
