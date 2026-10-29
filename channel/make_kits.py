#!/usr/bin/env python3
"""Build upload kits (human-readable .md + uploader manifest .json) for every finished video in channel/out."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
DISCLAIMER = ('This video is for education only and is not financial advice.\n'
              'Original script, characters and animation. Narrated with an AI voice.')
COMMON_TAGS = ['coin theory', 'economics explained', 'money explained', 'personal finance', 'animated explainer']

VIDEOS = {
    'ep01_inflation': dict(
        titles=['Where Did Your $100 Go? (Inflation Explained)', 'Your $100 Is Now Worth $12. Here\'s Why.',
                'Why Your Money Slowly Melts: Inflation Explained With Real Data'],
        hook="In 1970, $100 under a mattress would buy only about $12 worth of stuff today. So where did the other "
             "$88 go?",
        summary="Penny the coin explains inflation with real government data: how prices are measured, what bread, "
                "eggs, coffee and gas cost in 1980 vs today, why prices rise, how the Fed fights back with interest "
                "rates, why the target is 2% instead of zero, who wins and who loses, why your pay barely beat "
                "inflation since 1973, and the rule of 70.",
        sources="US Bureau of Labor Statistics (CPI-U, average prices, average hourly earnings) and Federal Reserve "
                "(Fed funds rate), retrieved from FRED, Federal Reserve Bank of St. Louis, through September 2026.",
        tags=['inflation', 'inflation explained', 'what is inflation', 'consumer price index', 'cpi',
              'why are prices rising', 'purchasing power', 'federal reserve', 'interest rates', 'rule of 70',
              'real wages', 'deflation', 'cost of living'],
        thumb='ep01_thumb_a.png'),
    'ep02_housing': dict(
        titles=['Why Houses Got So Expensive', 'Houses Cost $23,000 in 1970. Now $393,000. What Happened?',
                'Why Can\'t Anyone Afford a House? (Explained With Real Data)'],
        hook="In 1970, the typical new American home sold for about $23,000. Today it's about $393,000, almost twice "
             "as expensive even after inflation.",
        summary="Penny the coin breaks down the housing crisis with real data: how many years of income a home "
                "costs, why America stopped building enough homes, how zoning rules block new housing, how mortgage "
                "rates pushed prices up and then made payments jump, whether it was easier in 1984, who wins and "
                "loses, and what would actually help.",
        sources="Median sales price of new houses (Census/HUD), median household income (Census), housing starts "
                "(Census), 30-year mortgage rate (Freddie Mac), CPI (BLS), retrieved from FRED, Federal Reserve "
                "Bank of St. Louis.",
        tags=['housing crisis', 'why are houses so expensive', 'housing market', 'home prices', 'mortgage rates',
              'housing affordability', 'zoning', 'housing shortage', 'first time home buyer', 'real estate'],
        thumb='ep02_thumb_a.png'),
}

SHORTS = {
    'ep01_short_prices': ('Bread, eggs, coffee, gas: 1980 vs today #shorts', 'ep01_inflation'),
    'ep01_short_wages': ('Why your raise doesn\'t feel like a raise #shorts', 'ep01_inflation'),
    'ep01_short_rule70': ('The rule of 70: how fast your money loses value #shorts', 'ep01_inflation'),
    'ep02_short_price': ('A house cost $23,000 in 1970. Now? #shorts', 'ep02_housing'),
    'ep02_short_payment': ('Same house, $876 more per month #shorts', 'ep02_housing'),
    'ep02_short_supply': ('America stopped building homes #shorts', 'ep02_housing'),
}


def main():
    for name, v in VIDEOS.items():
        video = os.path.join(OUT, f'{name}.mp4')
        if not os.path.exists(video):
            continue
        ep = name.split('_')[0]
        chapters = open(os.path.join(OUT, f'{ep}_chapters.txt')).read().strip()
        desc = f"{v['hook']}\n\n{v['summary']}\n\n{chapters}\n\nData: {v['sources']}\n\n{DISCLAIMER}"
        manifest = dict(video=f'channel/out/{name}.mp4', title=v['titles'][0], description=desc,
                        tags=v['tags'] + COMMON_TAGS, categoryId=27, thumbnail=f"channel/out/{v['thumb']}",
                        captions=f'channel/out/{name}.en.srt', privacy='private', madeForKids=False,
                        syntheticMedia=True, language='en')
        json.dump(manifest, open(os.path.join(OUT, f'{name}.upload.json'), 'w'), indent=2)
        alt = '\n'.join(f'{i}. {t}' for i, t in enumerate(v['titles'], 1))
        md = (f"# Upload kit: {name}\n\n**Title options** (1 is the default):\n{alt}\n\n"
              f"**Thumbnails:** {ep}_thumb_a.png (default), {ep}_thumb_b.png. Use Studio's \"Test & compare\".\n\n"
              f"**Description:**\n\n{desc}\n\n**Tags:** {', '.join(manifest['tags'])}\n\n"
              f"**Captions:** {name}.en.srt (English)\n\n**Settings:** Education category; Not made for kids; "
              f"Altered or synthetic content: Yes (AI narrator voice); add end screen (latest video + subscribe) "
              f"over the final 15 seconds.\n")
        open(os.path.join(OUT, f'{name}.upload.md'), 'w').write(md)
        print('kit:', name)
    for name, (title, parent) in SHORTS.items():
        if not os.path.exists(os.path.join(OUT, f'{name}.mp4')):
            continue
        desc = (f"{VIDEOS[parent]['hook']}\nFull video on the Coin Theory channel.\n\n"
                f"Data: {VIDEOS[parent]['sources']}\n\n{DISCLAIMER}")
        manifest = dict(video=f'channel/out/{name}.mp4', title=title, description=desc,
                        tags=VIDEOS[parent]['tags'][:6] + ['shorts'], categoryId=27, privacy='private',
                        madeForKids=False, syntheticMedia=True, language='en')
        json.dump(manifest, open(os.path.join(OUT, f'{name}.upload.json'), 'w'), indent=2)
        print('kit:', name)


if __name__ == '__main__':
    main()
