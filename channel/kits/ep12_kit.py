"""Write channel/out/ep12_week.upload.json from the script's numbers and the rendered chapters."""
import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
import ep12_week as e  # noqa: E402

chapters = open(os.path.join(HERE, 'out', 'ep12_chapters.txt')).read().strip()
desc = (
    f"The Nasdaq Composite fell {abs(e.NDQ_WK):.1f}% in the week to Nov 20, 2026, its worst week since "
    f"{e.NDQ_WK_SINCE:%B %Y}. The S&P 500 fell {abs(e.SP_WK):.1f}%, its worst week since {e.SP_WK_SINCE:%B %Y}, and "
    f"closed at {e.SP_NOW:,.2f}: {abs(e.SP_DD):.1f}% below its Oct 6 record, which makes it a correction. We go "
    f"through the week day by day, why stocks fell (bond yields over 5%, {e.INFL:.1f}% inflation, the Fed's "
    f"September hike, the tech unwind, a fear index at {e.V_NOW:.0f}), where the money went (gold "
    f"{e.GOLD_WK:+.1f}%, bitcoin {e.BTC_WK:+.1f}%, Treasuries up), and every S&P 500 correction since 1950: "
    f"{e.N_CORR} of them, {e.N_STOP} stopped before a bear market, and a year after first hitting -10% the index "
    f"was higher {e.UP12} of {e.N12} times (median {e.MED12:+.0f}%).\n\n{chapters}\n\n"
    "Sources: Yahoo Finance daily closes for the S&P 500 (^GSPC), Nasdaq Composite (^IXIC), Dow Jones Industrial "
    "Average (^DJI), Cboe VIX (^VIX), COMEX gold futures (GC=F), bitcoin (BTC-USD) and the U.S. dollar index "
    "(DX-Y.NYB), through Nov 20, 2026. FRED (Federal Reserve Bank of St. Louis): DGS10, DFEDTARU/DFEDTARL, "
    "CPIAUCSL, MORTGAGE30US (Freddie Mac). Correction statistics are our calculations from S&P 500 closes since "
    "1950, prices only (no dividends): a correction is a close 10% or more below the prior record, finished at the "
    "next record.\n\n"
    "Watch next: the fear index explained https://youtu.be/f8OkPpAPeRg\n\n"
    "This video is for education only and is not financial advice. Past performance does not guarantee future "
    "results.\nOriginal script and animation. Narrated with an AI voice.")
kit = {
    'video': 'channel/out/ep12_week.mp4',
    'title': "The Nasdaq's Worst Week Since 2020. What Happens After a Correction?",
    'description': desc,
    'tags': ['stock market correction', 'what happens after a stock market correction', 'nasdaq worst week',
             'stock market crash', 'stock market today', 'stock market this week', 's&p 500 correction',
             'bear market', 'is a crash coming', 'stock market 2026', 'gold price', 'bitcoin price', 'vix',
             'coin theory', 'money explained', 'personal finance'],
    'categoryId': 27,
    'thumbnail': 'channel/out/thumbs/ep12_week_a.jpg',
    'captions': 'channel/out/ep12_week.en.srt',
    'privacy': 'private',
    'madeForKids': False,
    'syntheticMedia': False,
    'language': 'en',
}
json.dump(kit, open(os.path.join(HERE, 'out', 'ep12_week.upload.json'), 'w'), indent=1)
print(kit['title'], len(desc), 'chars')
