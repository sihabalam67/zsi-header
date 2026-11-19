"""Write channel/out/ep10_stocks.upload.json from the script's numbers and the rendered chapters."""
import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
import ep10_stocks as e  # noqa: E402

chapters = open(os.path.join(HERE, 'out', 'ep10_chapters.txt')).read().strip()
desc = (
    f"The S&P 500 fell {e.STREAK} days in a row and closed at {e.SP_NOW:,.2f} on Nov 19, 2026: {abs(e.SP_DD):.1f}% "
    f"below its Oct 6 record of {e.SP_REC:,.2f}. The Nasdaq is {abs(e.NDQ_DD):.1f}% below its record (a correction) "
    f"and the Dow closed at {e.DOW_NOW:,.2f}, below 50,000 for the first time since June. Why: the 10-year Treasury "
    f"yield is {e.Y_NOW:.2f}%, inflation is {e.INFL:.1f}%, and the Fed raised rates in September. Then the history: "
    f"since 1950 the S&P 500 fell 8% or more from a record {e.N8} times, and {e.N20} of those became bear markets. "
    f"After {e.N6} six-day losing streaks, stocks were higher a year later {e.UP6} of {len(e.F12)} times.\n\n"
    f"{chapters}\n\n"
    "Sources: Yahoo Finance daily closes for the S&P 500 (^GSPC), Dow Jones Industrial Average (^DJI) and Nasdaq "
    "Composite (^IXIC), saved Nov 19, 2026 after the close. FRED (Federal Reserve Bank of St. Louis): DGS10 (10-year "
    "Treasury yield), DFEDTARU/DFEDTARL (Fed target range), CPIAUCSL (CPI). History statistics are our calculations "
    "from S&P 500 daily closes since 1950, prices only (no dividends).\n\n"
    "This video is for education only and is not financial advice. Past performance does not guarantee future "
    "results.\nOriginal script and animation. Narrated with an AI voice.")
kit = {
    'video': 'channel/out/ep10_stocks.mp4',
    'title': f'Stocks Fell {e.STREAK} Days in a Row. Is a Crash Coming?',
    'description': desc,
    'tags': ['stock market crash', 'is a stock market crash coming', 'stock market today', 'why is the stock market down',
             'stock market correction', 'nasdaq correction', 'dow below 50000', 's&p 500', 'bear market',
             'stock market 2026', '10 year treasury yield', 'inflation', 'federal reserve', 'should i sell my stocks',
             '401k', 'index fund', 'coin theory', 'money explained', 'personal finance'],
    'categoryId': 27,
    'thumbnail': 'channel/out/thumbs/ep10_stocks_b.jpg',
    'captions': 'channel/out/ep10_stocks.en.srt',
    'privacy': 'private',
    'madeForKids': False,
    'syntheticMedia': False,
    'language': 'en',
}
json.dump(kit, open(os.path.join(HERE, 'out', 'ep10_stocks.upload.json'), 'w'), indent=1)
print(kit['title'], len(desc), 'chars')
