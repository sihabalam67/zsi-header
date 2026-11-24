"""Story #1 narration: "Grandpa's $1,000 Test". Every number comes from s01_numbers.N (asserted there).
A line prefix sets who talks on screen: G| Grandpa, M| Mia, B| Ben, R| Rosie, N| Nickel the parrot; none = Penny.
A '!' after the prefix (or at the start) = dramatic read."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from s01_numbers import N  # noqa: E402

TITLE = "Grandpa Gave 3 Kids $1,000. Who Won?"


def m(v):
    return f'${v:,}'


SCENES = [
    dict(id='open', chapter='Thirty years later', lines=[
        "!Thirty years ago, a grandpa gave each of his three grandkids one thousand dollars.",
        "G|And one rule: come back in thirty years, and show me what you did with it.",
        f"Today is the day. One of them has {m(N['now'])}.",
        "One has a thousand dollars that is secretly worth less than half.",
        "And one has a closet full of old junk.",
        "By the end, you'll know which one you are, and the simple thing that made the winner win.",
        "I'm Penny, and this is a money story. The kids are made up. Every number is real.",
        "Let's go back to 1996.",
    ]),
    dict(id='y1996', chapter='1996: three envelopes', lines=[
        "November 1996. Grandpa Joe has a big white mustache, red suspenders, and the worst jokes in town.",
        "G|Why did the dollar go to school? To get a little more cents!",
        "His parrot, Nickel, has heard that joke four hundred times.",
        "Grandpa hands out three envelopes. Inside each one: one thousand dollars.",
        "Mia is twelve. Rosie is eleven. Ben is ten.",
        "G|Do whatever you want with it. Just come back in thirty years.",
        "N|Boring!",
        "Grandpa also writes a secret note, seals it in a fourth envelope, and locks it in his desk. We'll open it at the very end.",
    ]),
    dict(id='choices', chapter='Spend, save, or plant', lines=[
        "Mia spends hers that same afternoon. A virtual pet on a keychain, light-up sneakers, and a mountain of candy.",
        "Ben has a different plan. He puts every dollar in a cookie jar, and names it Fort Cookie.",
        "B|Nobody can steal from Fort Cookie. I will never, ever lose a single dollar.",
        "Rosie does something strange. She puts her money in a fund that owns a tiny slice of America's five hundred "
        "biggest companies.",
        "When those companies make money, a little comes back to her, and she plants it right back in.",
        "Grandpa calls it a money tree. Rosie plants it in his backyard, and it is very, very small.",
        "M|That's it? A stick?",
        "R|Just wait. Trees take time.",
        "Grandpa winks. Nickel yawns. And thirty years start ticking.",
    ]),
    dict(id='storm1', chapter='The first storm', lines=[
        f"For a few years, the tree grows fast. By September 2000, Rosie's thousand dollars has grown to "
        f"{m(N['d2000_peak'])}.",
        "Mia's virtual pet, meanwhile, has died. Eleven times.",
        "Then a storm hits. Lots of internet companies that everybody was excited about turn out to be worth "
        "almost nothing.",
        f"Stocks fall for two whole years. By October 2002, Rosie's tree is down to {m(N['d2002_low'])}.",
        "M|Told you. Money trees are scary.",
        "Ben pats Fort Cookie. Still one thousand dollars. Safe and sound.",
        "And for the first time, Nickel squawks it.",
        "N|!Don't chop the tree!",
        "Here's the thing about storms. Rosie's companies didn't disappear. People still bought food, shoes and medicine. The leaves fell, but the roots were fine.",
    ]),
    dict(id='storm2', chapter='The biggest storm', lines=[
        f"Rosie doesn't chop. Slowly, the tree grows back. By October 2007, it's worth {m(N['d2007_peak'])}.",
        "!Then comes the biggest storm in eighty years.",
        "Banks had lent too much money to people who couldn't pay it back, and the whole system started to crack.",
        "Every week, more leaves fall. Rosie watches her money blow away.",
        f"March 2009. Rosie has had her tree for twelve years. It's worth {m(N['d2009_low'])}.",
        f"That's just {m(N['d2009_low'] - 1000)} more than Ben's cookie jar.",
        f"B|Twelve years of worrying, for {N['d2009_low'] - 1000} dollars!",
        "Everybody on TV says the same thing: get out. Sell everything.",
        "!Rosie picks up the axe.",
        "Then the phone rings. It's Grandpa.",
        "G|Rosie. Storms end. But a tree you chop down never grows back.",
        "So, does she chop it? Stay with me, because the answer is worth thousands of dollars.",
        "And if you like money stories like this one, hit subscribe, so you don't miss the next one.",
    ]),
    dict(id='mouse', chapter='The sneaky mouse', lines=[
        "While Rosie's tree is getting hit by storms, something sneaky is happening inside Fort Cookie.",
        "Every bill is still there. One thousand dollars. Ben counts it every night.",
        "But a tiny mouse lives in the jar. Its name is Inflation.",
        "The Inflation Mouse never steals a bill. It nibbles something else: what the money can buy.",
        "In 1996, Ben's thousand dollars could fill a big shopping cart.",
        "Every year, prices go up a little. Milk, bread, shoes, movie tickets. Two or three percent a year doesn't "
        "sound like much.",
        "But year after year, the same thousand dollars fills a smaller and smaller cart.",
        "Nobody notices, because the number on the bills never changes. That's what makes the mouse so sneaky.",
        "By 2026, the mouse has nibbled so much that Ben's cart is less than half full.",
        "And Ben has no idea. He still sleeps right next to Fort Cookie, every single night.",
    ]),
    dict(id='storm3', chapter='The weird storm', lines=[
        f"Back to the tree. Rosie didn't chop it. By early 2020, it's worth {m(N['d2020_peak'])}.",
        "Then comes the weirdest storm of all. A virus. Schools close. Everybody stays home.",
        f"In about one month, the tree drops thirty-four percent, to {m(N['d2020_low'])}.",
        "This time, Rosie doesn't even look at the axe. She makes a cup of hot chocolate, and waits.",
        "N|Don't chop the tree!",
        "The storm passes faster than anyone expected. By August 2020, just five months later, the tree is back to a brand new record.",
        "People who chopped their trees in March missed the whole bounce back.",
    ]),
    dict(id='reunion', chapter='Reunion day', lines=[
        "November 2026. Thirty years later. Everybody is back at Grandpa's house.",
        "Grandpa sets up a big scoreboard. Mia goes first.",
        "She brings a box. A virtual pet, light-up sneakers, an old TV, three phones. None of them turn on.",
        "Well, one of them beeps. Mia's money score: zero dollars.",
        "Ben is next. He opens Fort Cookie, and counts. One thousand dollars. Every single bill.",
        "B|I told you. I never lost a dollar.",
        "Grandpa smiles, and pulls out a receipt. Prices have more than doubled since 1996.",
        f"!Ben's thousand dollars now buys only what {m(N['jar_buys'])} bought back then.",
        f"To buy what a thousand dollars bought in 1996, you'd need {m(N['need_today'])} today.",
        "B|I never lost a dollar... but I lost half my money?",
        "Then it's Rosie's turn. Grandpa checks the tree. Even during this month's market dip, it's worth...",
        f"!{m(N['now'])}.",
        "Sixteen times what she started with. And she never picked a hot stock. She never guessed when to sell.",
        "She just did one thing. The hardest thing. She didn't chop the tree.",
        "Grandpa gives her a high five. Nickel tries to count the coins on the tree, and gives up at forty-two.",
    ]),
    dict(id='mia', chapter="Mia's second chance", lines=[
        "M|Is it too late for me? I'm forty-two.",
        "Grandpa hands her one last envelope. It's a true story, about the unluckiest planter ever.",
        "In October 2007, this person started planting just one hundred dollars a month, right before the biggest "
        "storm in eighty years.",
        f"By March 2009, they had put in {m(N['dca_2009_paid'])}, and it was worth only {m(N['dca_2009_worth'])}. "
        "Terrible timing.",
        "But they kept planting. One hundred dollars, every single month, storm or no storm.",
        f"Today, they've put in {m(N['dca_paid'])}. And it's worth {m(N['dca_now'])}.",
        "The worst timing in history, and their money still grew more than four times.",
        "G|The best time to plant a tree was thirty years ago. The second best time is today.",
        "So Mia plants a seed. A very, very small one.",
        "N|Don't chop the tree!",
        "And Grandpa's secret note from 1996? At the bottom, it says one more thing: I'm proud of all three of you. Now go plant something.",
    ]),
    dict(id='lessons', chapter='Three lessons', lines=[
        "So here's what Grandpa's test teaches. Three things, simple enough for a ten-year-old.",
        "One. Money in a jar shrinks. The Inflation Mouse is always nibbling.",
        "Two. Planted money grows, but storms always come. Don't chop the tree.",
        "Three. Start small, start now, and keep planting.",
        "Rosie's fund is a real kind of fund: an index fund that owns the five hundred biggest US companies. These "
        "are its real past results, before fees and taxes.",
        "The past doesn't promise the future, and storms can last a long time. This is education, not financial "
        "advice.",
        "Now tell me in the comments: which grandkid are you? Mia, Ben, or Rosie?",
        "And send this to someone who still keeps a cookie jar.",
        "I'm Penny. Subscribe for more money stories, and I'll see you next time.",
    ]),
]

assert N['dca_now'] / N['dca_paid'] > 4 and N['jar_buys'] < 500 and round(N['now'] / 1000) == 16
assert abs(N['d2020_low'] / N['d2020_peak'] - 1 + 0.34) < 0.005

if __name__ == '__main__':
    words = sum(len(ln.split('|')[-1].split()) for s in SCENES for ln in s['lines'])
    print('words', words, 'lines', sum(len(s['lines']) for s in SCENES))
