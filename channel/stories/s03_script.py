"""Story #3 narration: "The Poorest Man in Town Left $2 Million. How?" Every number comes from s03_numbers.N.
A line prefix sets who talks on screen: W| Walter (flashbacks, notebook, receipts, card), L| Lily, D| Derek,
K| Ms. Kowalski; none = Penny. A '!' after the prefix (or at the start) = dramatic read.
Governing visual rule: the brass key / box 467 never leaves the story (slid across, turned, opened, its 467
envelopes counted, its card read, its notebook read in court).
Model note: $300 on the first trading day of every month Jan 1988-Nov 2026 (467 envelopes) into an S&P 500 index
fund with dividends, plus $5,000 from the storm jar at the 2002, 2009 and 2020 lows. Before fees and taxes.
Walter decides during Black Monday week (Oct 1987); his first envelope goes in January 1988."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from s03_numbers import N  # noqa: E402

TITLE = "The Poorest Man in Town Left $2 Million. How?"


def m(v):
    return f'${round(v):,}'


CRASH_PCT = abs(float(N['black_monday']))

SCENES = [
    dict(id='open', chapter='The will', lines=[
        "!A tiny law office. Folding chairs. A will, and one sentence.",
        "K|I leave everything I own to the town library and the children's hospital.",
        f"K|!The total: {m(N['now'])}.",
        "D|!Two million? Walter? Walter ate soup for dinner. Every single night!",
        "L|His coat was held together with safety pins. Eleven of them. I counted.",
        "Walter was the school janitor. Same mop, same coat, same car.",
        "L|!So how? How does a janitor leave two million dollars?",
        "Ms. Kowalski slides a tiny brass key across the table. Toward Lily.",
        "K|He left you something else.",
        "I'm Penny. These people are made up. Every number is real. Let's go back one week.",
    ]),
    dict(id='lily', chapter='Lily and the soup', lines=[
        "Meet Lily. Twenty-eight. Rent due. Three maxed-out credit cards.",
        "L|I call them my three little dragons. They're sleeping. Please don't wake them.",
        "Every Sunday, Lily brought soup next door. To Walter.",
        "L|Honestly? I felt sorry for him.",
        "Flashback. Walter, in the safety-pin coat.",
        "W|Soup again? You know I make soup every night, right?",
        "L|Then why do you always take mine?",
        "W|Yours has chicken in it. Mine has opinions.",
        "On his shelf, a jar of coins labeled: Storm Jar.",
        "L|What's the jar for, Walter?",
        "W|Storms. Obviously. Eat your soup.",
        "Then, last Tuesday, nobody answered Walter's door.",
        "Back at the will reading, the door bangs open.",
        "D|!Nobody reads anything without me! Derek. Cousin. Closest living family.",
        "L|You visited him once. Christmas, 2011.",
        "D|And I brought a fruit basket. That's love.",
        "K|You're sitting in my chair, Derek.",
        "D|That money belongs to family. And whatever that little key opens? Also mine.",
        "Lily turns the key over. Stamped on the back: Box 467.",
        "What does a man with eleven safety pins keep in a bank vault?",
    ]),
    dict(id='box', chapter='Box 467', lines=[
        "Next morning. The vault. Derek tags along, uninvited.",
        "D|I'm here to supervise. As family.",
        "K|You're here because somebody said the word vault.",
        "!And the lid opens.",
        "One: a worn notebook. On the cover, in pencil: Walter's Rules.",
        "Two: a yellowed newspaper. October 20th, 1987. The headline: STOCKS CRASH.",
        "Three: a fat stack of envelopes.",
        "Four: a birthday card. Sealed. With one name on it.",
        "L|!That's... my name.",
        "D|Why keep a forty-year-old newspaper? Was he collecting bad news?",
        "L|And why is there a card for me? From nineteen ninety-eight?",
        "The notebook's first line:",
        "W|Read the envelopes first. The card goes last. Patience, kid. That's the whole trick.",
        "L|He's bossing me around. From a notebook.",
        "K|He was a very organized man.",
        "The answer to two million dollars is in this box. Lily opens the first envelope.",
    ]),
    dict(id='envelopes', chapter='Clue 1: the envelopes', lines=[
        "Each one holds a bank receipt. And the same number.",
        "L|Three hundred dollars. January 1988. Three hundred. February. Three hundred. March...",
        "Into an index fund: one basket of America's five hundred biggest companies.",
        f"{N['months']} envelopes. Not one month missed.",
        f"L|{N['months']}! Box 467! He picked the box number on purpose!",
        "K|Of course he did. That's very Walter.",
        "One from 1995 has a note:",
        "W|Car died on the highway today. Took the bus home. Envelope still goes in.",
        "D|Three hundred a month? I spend that on... actually, I don't know what on.",
        "K|That's usually the problem.",
        f"!Add them all up: {m(N['paid_monthly'])}.",
        "L|That's a lot of soup money. But it's not two million dollars.",
        "D|See? Missing money! Very suspicious. I smell a lawsuit.",
        "K|You smell my coffee.",
        "So where did the rest come from? The next clue was yellowing in that box.",
    ]),
    dict(id='crash', chapter='Clue 2: the newspaper', lines=[
        "The newspaper. October 20th, 1987.",
        f"The day before, Black Monday, the stock market fell {CRASH_PCT} percent. In one single day.",
        "Everyone panicked. In the margin, in pencil:",
        "W|Everybody's selling. So the stores are having a sale. I'm going shopping.",
        "That week, Walter opened his account. First envelope: January 1988.",
        "L|He started investing... during a crash?",
        "K|Turn the page. There's more.",
        "Taped inside: three receipts. Five thousand dollars each, on three terrible days.",
        "The 2002 crash. The 2009 crisis. The 2020 shutdown.",
        "L|!The Storm Jar! He said it was for storms. I thought he was joking!",
        "On the 2009 receipt, one line:",
        "W|Everyone thinks I'm crazy. Good. Crazy people get the best prices.",
        f"That 2002 five thousand is worth {m(N['c2002'])} today. The 2009 one: {m(N['c2009'])}.",
        f"Even the 2020 one: {m(N['c2020'])}.",
        "D|So he bought when everyone was scared? That's actually smart. I hate it.",
        "Three storms. Fifteen thousand dollars. Still nowhere near two million.",
        "Then Lily finds a pencil chart in the notebook.",
        "If you like money mysteries, subscribe, so you don't miss the next one.",
    ]),
    dict(id='growth', chapter='Clue 3: the slow part', lines=[
        "Every ten years, Walter wrote down his balance.",
        f"1996, after nine years: {m(N['v1996'])}.",
        "W|Nine years of soup. Feels like nothing's happening. Keep going.",
        f"2006: {m(N['v2006'])}.",
        "W|Car still runs. Coat still works. Keep going.",
        f"2016, almost twenty-nine years in: {m(N['v2016'])}.",
        "L|Half a million. Amazing. But still not two million.",
        f"!Then the last ten years. That {m(N['v2016'])} grew more than four times bigger.",
        f"{N['last10_share']} percent of all the money appeared in the final ten years.",
        f"L|{N['last10_share']} percent? At the very end?",
        "K|That's compounding. Your money earns money. Then that money earns money too.",
        "W|It's a snowball. For years you're just pushing snow. Then one day it rolls by itself.",
        "D|Forty years to get rich, and he never spent it? That's not genius. That's crazy.",
        "L|Or maybe it's both?",
        "Derek marches straight to the courthouse. With a lawyer he found on a bus bench.",
    ]),
    dict(id='contest', chapter="Derek's Friday", lines=[
        "Monday. A court letter lands on Ms. Kowalski's desk.",
        "K|Derek is contesting the will. He says Walter wasn't of sound mind.",
        "D|!Nobody sane lives like that! Soup every night? Safety pins? With millions in the bank?",
        "D|He was clearly confused. And I was clearly his favorite cousin.",
        "L|You were his only cousin.",
        "D|Which makes me the favorite. That's math.",
        "K|Hearing's Friday, nine a.m. If the judge agrees, the will could be thrown out.",
        "L|And then who gets the money?",
        "K|Most likely the closest family. Derek.",
        "D|I'm thinking a boat. A big one. I'll name it after Walter. The Soup.",
        "Four days until Friday. And one thing in that box is still sealed.",
        "L|The card.",
    ]),
    dict(id='card', chapter='The card', lines=[
        "That night, on Walter's front step, Lily opens the card. June 1st, 1998.",
        "W|Dear Lily. Today you were born, right next door. Your mom let me hold you.",
        "W|You grabbed one of my safety pins, and you would not let go.",
        "L|The safety pins...",
        "W|So today I bought you one thousand dollars of my fund. Don't touch it. Let it grow up with you.",
        "A receipt slides out. And this year's statement.",
        f"!Twenty-eight years later, that one thousand is worth {m(N['gift'])}.",
        "L|!He planted this the day I was born.",
        "A sticky note, in newer ink:",
        "W|P.S. You brought me soup. I planted you a tree. Fair trade.",
        "L|I thought I was the one helping him. Sunday soup. Out of pity.",
        "L|He was helping me the whole time.",
        "And on the back:",
        "W|If Derek makes trouble, read him page one.",
    ]),
    dict(id='friday', chapter='Friday, 9 a.m.', lines=[
        "Friday. Courtroom Two. Derek wears sunglasses indoors. And a captain's hat.",
        "D|I'm dressing for the life I'm about to have.",
        "K|Your Honor, here are Walter's own words. Page one.",
        "W|Walter's Rules. One: pay yourself first. Three hundred, every month, before anything else.",
        "W|Two: when the world panics, go shopping. Keep a storm jar.",
        "W|Three: don't touch it. Time does the heavy lifting.",
        "W|Four: a coat with safety pins is still a coat. Buy freedom, not stuff.",
        "W|Five: when I'm gone, it goes to the library and the hospital. They were good to me.",
        "The judge flips through the envelopes. Then takes off her glasses.",
        "A man who never missed a month in thirty-nine years? Very sound mind.",
        "!The will stands.",
        "D|!So I get nothing?",
        "K|Not nothing. Walter left you one item.",
        "A garment bag. The coat. Eleven safety pins.",
        "W|For Derek. It's warm. It's paid for. And it'll teach you more than money would.",
        "Derek puts it on. One safety pin pops. He catches it.",
        "D|...It does have nice pockets.",
    ]),
    dict(id='ending', chapter="Lily's envelope", lines=[
        "Outside, kids run up the library steps.",
        "L|Walter wasn't poor. He wasn't saving to look rich. He was saving to be free.",
        "That night: dragon number three. And the kitchen scissors.",
        "!Snip.",
        "L|One dragon down. Two to go. And next month, three hundred dollars. In an envelope.",
        "And a new jar on her shelf: Storm Jar.",
        "Sounds like a movie? Real people have done this.",
        "In 2014, a Vermont janitor left about eight million dollars, much of it to his town's library and hospital.",
        "Walter, Lily and Derek are made up, and so are their choices. The market returns are real, before fees and "
        "taxes.",
        "Past results don't promise the future. This is education, not financial advice.",
        "Now tell me in one word: could you live like Walter for ten years? Yes or no?",
        "L|I'd say yes. But I'm keeping the chicken in my soup.",
        "And send this to a friend who thinks small money doesn't matter.",
        "I'm Penny. See you next time.",
    ]),
]

assert N['now'] == 2032554 and N['monthly'] == 300 and N['months'] == 467 and N['paid_monthly'] == 140100
assert N['paid'] == 155100 and N['v2016'] == 479188 and N['last10_share'] == 76 and N['now'] > 4 * N['v2016']
assert N['c2002'] == 73299 and N['c2009'] == 74227 and N['c2020'] == 17827 and N['gift'] == 11063
assert CRASH_PCT == 20.5 and N['v1996'] < N['v2006'] < N['v2016'] and 400000 < N['v2016'] < 600000
assert N['c2002'] < N['c2009'] and 11000 < N['gift'] < 12000

if __name__ == '__main__':
    words = sum(len(ln.split('|')[-1].split()) for s in SCENES for ln in s['lines'])
    talk = sum(1 for s in SCENES for ln in s['lines'] if '|' in ln)
    total = sum(len(s['lines']) for s in SCENES)
    print('words', words, 'lines', total, 'character lines', talk)
    for s in SCENES:
        print(f"  {s['id']:10s} {sum(len(ln.split('|')[-1].split()) for ln in s['lines'])}")
    print('max words/line', max(len(ln.split('|')[-1].split()) for s in SCENES for ln in s['lines']))
