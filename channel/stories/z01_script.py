"""ZSI.Ai investor presentation (played in person to 10+ investors). Two presenters, like business partners:
F| = female presenter, N| = male presenter. Plan: investor/zsi/SCRIPT.md + MASTER_PROMPT.md (Gold Desk style).
Every number is the live calculator's default proposal value (re-captured Nov 25, 2026 after the owner's update: GoldenMark Money customers 100/700/7,000/12,000/20,000 and ZSI PAY fee 0.8%, investor/zsi/research/).
Each product explanation stays under 20 seconds (owner rule). Owner decisions Nov 24: GoldenMark Money uses the
calculator's $0.65 price; SaaS = businesses pay $75/month to use the five platforms; no raise amount or valuation."""

TITLE = "ZSI.Ai: Seven Products, Four Revenue Streams"

SCENES = [
    dict(id='open', chapter='ZSI.Ai', lines=[
        "F|Seven products you can open in your browser today.",
        "N|Four separate ways they make money.",
        "F|This is ZSI dot A I.",
    ]),
    dict(id='kabab', chapter='Kabab King', lines=[
        "N|First, Kabab King: a complete restaurant platform.",
        "N|Guests browse the menu, order for pickup or delivery, reserve a table, and book catering for weddings and events, all online.",
    ]),
    dict(id='store', chapter='GoldenMark Store', lines=[
        "F|GoldenMark Store is a full online shop: product categories, featured deals, search, a cart, and order tracking.",
    ]),
    dict(id='marry', chapter='USA Marry', lines=[
        "N|USA Marry is a Muslim marriage and matchmaking platform.",
        "N|Members create a profile, search for compatible partners, message securely, and choose a membership plan.",
    ]),
    dict(id='print', chapter='DG Print 24', lines=[
        "F|DG Print 24 is online printing. Pick a product, from business cards to posters, upload your artwork, and track the order to your door.",
    ]),
    dict(id='limo', chapter='RPC LIMO', lines=[
        "N|RPC LIMO books luxury limos and chauffeurs in more than three hundred cities: by the hour, per ride, or round trip, with apps for riders and drivers.",
    ]),
    dict(id='saas', chapter='Five SaaS platforms', lines=[
        "F|Together, these are our five SaaS platforms.",
        "F|SaaS means software as a service: businesses pay us a monthly subscription to use the platform, instead of building their own.",
    ]),
    dict(id='gmm', chapter='GoldenMark Money', lines=[
        "N|GoldenMark Money lets any business print checks on its own printer, email eChecks, and pay a whole batch of vendors at once, right from the browser.",
    ]),
    dict(id='zsipay', chapter='ZSI PAY', lines=[
        "F|And ZSI PAY. Restaurants and online shops process their online sales through ZSI PAY, and we keep eight tenths of one percent of every sale.",
        "N|That's eight dollars on every thousand.",
    ]),
    dict(id='terms', chapter='How it makes money', lines=[
        "N|Now, how it makes money. Three words first.",
        "F|Revenue: all the money customers pay us. Expenses: what we spend to run each business. And the bottom line: revenue minus expenses, the money we keep.",
        "N|Everything you'll see is a five-year projection from our live calculator, based on its assumptions. It's a plan, not a guarantee.",
    ]),
    dict(id='saas_model', chapter='Stream 1: SaaS', lines=[
        "F|Stream one: SaaS. Each subscription pays seventy-five dollars a month, plus a five-hundred-dollar setup fee. That's fourteen hundred dollars in its first year.",
        "N|The plan adds three hundred new subscriptions in Year 1, rising to twelve hundred fifty in Year 5, even after one in ten customers cancels each year.",
    ]),
    dict(id='saas_num', chapter='Stream 1: SaaS', lines=[
        "F|Revenue grows from two hundred eighty-five thousand dollars in Year 1 to over three point one million in Year 5.",
        "N|And that's after every cost: sales staff, marketing, development, hosting and card fees. Profit before tax: over five million dollars across five years, and profitable from the very first year.",
    ]),
    dict(id='gmm_model', chapter='Stream 2: GoldenMark Money', lines=[
        "N|Stream two: GoldenMark Money. A business pays sixty-five cents per digital check. No monthly fee, no setup fee.",
        "F|Our cost is two cents. So we keep sixty-three cents of every check.",
    ]),
    dict(id='gmm_num', chapter='Stream 2: GoldenMark Money', lines=[
        "N|As customers grow from one hundred businesses to twenty thousand, revenue rises from seventy-eight thousand dollars to nineteen and a half million a year.",
        "F|Over five years: thirty-eight point six million in revenue, and thirty-seven point one million left after check costs and marketing.",
    ]),
    dict(id='pay_num', chapter='Stream 3: ZSI PAY', lines=[
        "F|Stream three: ZSI PAY. The plan adds sixty restaurants and one hundred twenty online shops every year.",
        "N|By Year 5 that's nine hundred merchants, and seven hundred twenty million dollars in sales processed over five years.",
        "F|Our eight tenths of a percent becomes about two point one million dollars a year, and five point seven six million over five years.",
    ]),
    dict(id='misc', chapter='Stream 4: Miscellaneous', lines=[
        "N|Stream four is a bonus. While selling our products, the sales team wins outside projects: about five a year, at ten thousand dollars each.",
        "N|Half goes to development, so one hundred twenty-five thousand dollars net over five years.",
    ]),
    dict(id='combined', chapter='All four together', lines=[
        "F|Now put all four together.",
        "N|Revenue grows from six hundred forty-three thousand dollars in Year 1 to twenty-four point eight million in Year 5. That's over two million dollars every month.",
        "F|Fifty-two point four million dollars over five years.",
    ]),
    dict(id='bottom', chapter='The bottom line', lines=[
        "N|The bottom line rises from about three hundred thirty-one thousand dollars to twenty-three point two million a year.",
        "F|And the profit margin, the share of revenue we keep, climbs from about fifty-one percent to ninety-three.",
        "N|One shared team sells and runs all seven products, and its costs are already counted under SaaS. So GoldenMark Money only adds its check costs and marketing, and ZSI PAY needs no extra team.",
    ]),
    dict(id='why', chapter='Why invest', lines=[
        "F|So, why invest?",
        "N|Seven real, working products and four ways to earn, so we never depend on just one.",
        "F|Revenue that comes back every month.",
        "N|High margins: a check that sells for sixty-five cents costs us two.",
        "F|Fast growth: from six hundred forty-three thousand to twenty-four point eight million dollars a year.",
        "N|Profit from Year 1 in SaaS.",
        "F|And full transparency.",
    ]),
    dict(id='close', chapter='Test it yourself', lines=[
        "N|Don't just take our word for it. Open the live calculator, change any assumption, and test the numbers yourself.",
        "F|ZSI dot A I. Seven products. Four revenue streams. One platform, built to grow.",
        "N|Thank you. We'd love to take your questions.",
    ]),
]

if __name__ == '__main__':
    import re
    words = sum(len(re.sub(r'^[A-Z]\|', '', l).split()) for s in SCENES for l in s['lines'])
    print(len(SCENES), 'scenes', words, 'words', round(words / 150, 1), 'min')
