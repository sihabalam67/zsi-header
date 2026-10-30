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
    'ep03_gas': dict(
        titles=['Why Is Gas So Expensive Right Now? (2026 Oil Shock Explained)',
                'Gas Went From $2.78 to $4.50. Here\'s Why.',
                'The Strait of Hormuz Crisis and Your Gas Bill, Explained'],
        hook="In January, a gallon of regular gas cost about $2.78. By May it hit $4.50, and it's still around $4.27. "
             "So where is all that money going, and when will it come down?",
        summary="Penny the coin explains the 2026 gas price spike with real data: the Strait of Hormuz and the war "
                "with Iran, how oil more than doubled, how a barrel becomes a gallon (and what you pay for), why "
                "America's own oil doesn't protect you, past oil shocks since 1990, why prices rise like rockets and "
                "fall like feathers, how diesel pushes up food and everything else, what it costs your family, and "
                "what could bring prices down.",
        sources="Gasoline and diesel prices (EIA: GASREGW, GASDESW), WTI crude (EIA: DCOILWTICO), CPI and energy CPI "
                "(BLS: CPIAUCSL, CPIENGSL), retrieved from FRED, Federal Reserve Bank of St. Louis, through October "
                "2026. Strait of Hormuz share of world oil: EIA, World Oil Transit Chokepoints. First-quarter oil "
                "price jump and production cuts: EIA, Today in Energy (April 2026). War timeline and tanker "
                "attacks: CNN (March 9 and October 8, 2026). Federal gas tax: 18.4 cents per gallon (US Federal "
                "Highway Administration). US as top oil producer: EIA.",
        tags=['gas prices', 'why is gas so expensive', 'gas prices 2026', 'oil prices', 'strait of hormuz',
              'iran war oil', 'oil shock', 'gas prices explained', 'diesel prices', 'inflation 2026',
              'rockets and feathers', 'cost of living'],
        thumb='ep03_thumb_a.png'),
    'ep04_fed': dict(
        titles=['The Fed Just Raised Rates. What It Means for Your Money',
                'Fed Rate Hike 2026 Explained: Credit Cards, Mortgages, Savings',
                'Your Credit Card Now Charges 21%. Here\'s Why.'],
        hook="On September 17, 2026, the Federal Reserve raised interest rates for the first time in more than "
             "three years. Here's exactly what that means for your credit card, your mortgage, your car loan and "
             "your savings.",
        summary="Penny the coin explains the Fed's 2026 rate hike with real data: what the Fed actually controls, "
                "the rate rollercoaster since 2022, why an oil shock pushed the Fed to act, the split October vote, "
                "what happens to credit card rates (now over 21%), mortgages and car loans, why the average savings "
                "account still pays almost nothing, a simple rate-hike checklist, and what could happen next.",
        sources="Fed funds target range (DFEDTARU, DFEDTARL), bank prime loan rate (DPRIME), credit card plan rates "
                "(TERMCBCCALLNS) and 48-month new car loan rates (TERMCBAUTO48NS) from the Federal Reserve; 30-year "
                "mortgage rate (Freddie Mac, MORTGAGE30US); national savings rate (FDIC, SNDR); CPI and unemployment "
                "(BLS); retrieved from FRED, Federal Reserve Bank of St. Louis, through October 2026. October 28 "
                "vote: Federal Reserve FOMC statement, October 28, 2026. Deposit insurance: FDIC.",
        tags=['fed rate hike', 'federal reserve', 'interest rates', 'fed raises rates', 'fed rate hike 2026',
              'credit card interest', 'mortgage rates', 'savings account interest', 'high yield savings',
              'inflation 2026', 'what the fed rate hike means for you', 'prime rate'],
        thumb='ep04_thumb_a.png'),
    'ep05_jobs': dict(
        titles=['Microsoft Just Offered 60,000 Buyouts. Are Layoffs Really Rising?',
                'Nobody\'s Getting Fired. Nobody\'s Getting Hired. (2026 Job Market)',
                '60,000 Buyouts at Microsoft: What the Job Data Really Says'],
        hook="Microsoft just offered buyouts to about 60,000 employees, roughly a quarter of its workforce. So are "
             "layoffs really surging? The government's own data tells a very different story.",
        summary="Penny the coin breaks down the job market with official data: what a buyout is (and why so few "
                "people take one), whether layoffs are really rising, weekly jobless claims, how we got here, the "
                "real problem (hiring has slowed way down), the great stay, tech jobs and AI, which industry is "
                "still hiring, two numbers to watch for a recession, and what it all means for you.",
        sources="Layoffs and discharges, quits, job openings and hires rate (BLS JOLTS: JTSLDL, JTSQUL, JTSJOL, "
                "JTSHIR); initial jobless claims (US Dept. of Labor: ICSA); payrolls by industry (BLS: PAYEMS, "
                "CES6562000001, MANEMP, USINFO); unemployment (BLS: UNRATE, UNEMPLOY, UEMPMEAN); Sahm rule "
                "recession indicator (SAHMREALTIME); Fed funds target (DFEDTARU); retrieved from FRED, Federal "
                "Reserve Bank of St. Louis, through October 2026. Microsoft buyouts: CNBC, TechCrunch, Deadline and "
                "Fortune reports, October 26-28, 2026.",
        tags=['microsoft layoffs', 'microsoft buyouts', 'layoffs 2026', 'job market 2026', 'are layoffs rising',
              'hiring freeze', 'jobs report', 'unemployment', 'ai jobs', 'tech layoffs', 'sahm rule', 'recession'],
        thumb='ep05_thumb_a.png'),
}

SHORTS = {
    'ep01_short_prices': ('Bread, eggs, coffee, gas: 1980 vs today #shorts', 'ep01_inflation'),
    'ep01_short_wages': ('Why your raise doesn\'t feel like a raise #shorts', 'ep01_inflation'),
    'ep01_short_rule70': ('The rule of 70: how fast your money loses value #shorts', 'ep01_inflation'),
    'ep02_short_price': ('A house cost $23,000 in 1970. Now? #shorts', 'ep02_housing'),
    'ep02_short_payment': ('Same house, $876 more per month #shorts', 'ep02_housing'),
    'ep02_short_supply': ('America stopped building homes #shorts', 'ep02_housing'),
    'ep03_short_jump': ('Gas went from $2.78 to $4.50 in 4 months #shorts', 'ep03_gas'),
    'ep03_short_barrel': ('What you really pay for in a gallon of gas #shorts', 'ep03_gas'),
    'ep03_short_feathers': ('Why gas prices rise fast but fall slow #shorts', 'ep03_gas'),
    'ep04_short_cards': ('Your credit card now charges over 21% #shorts', 'ep04_fed'),
    'ep04_short_savings': ('Your savings pay 0.38%. Inflation is 3.7%. #shorts', 'ep04_fed'),
    'ep04_short_why': ('Why the Fed raises rates when gas gets expensive #shorts', 'ep04_fed'),
    'ep05_short_layoffs': ('Layoffs are LOWER than in 2019. Here is the proof #shorts', 'ep05_jobs'),
    'ep05_short_hiring': ('The job market\'s real problem: nobody is hiring #shorts', 'ep05_jobs'),
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
