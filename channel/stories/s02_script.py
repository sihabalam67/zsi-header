"""Story #2 narration: "Same Salary. 10 Years Later, One Is Broke." Every number comes from s02_numbers.N.
A line prefix sets who talks on screen: J| Jay, S| Sam, A| Ava, H| Hank; none = Penny.
A '!' after the prefix (or at the start) = dramatic read.
Model note: Sam's raises are not in his 401(k) number (same $300/month all 10 years, nothing Apr-Aug 2020)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from s02_numbers import N  # noqa: E402

TITLE = "Same Salary. 10 Years Later, One Is Broke."


def m(v):
    return f'${round(v):,}'


CAR = N['car_pay'] * 72 - N['car_interest']        # the $40,000 car
CARD = N['card_total'] - N['card_interest']        # the $6,000 vacation balance

SCENES = [
    dict(id='open', chapter='Midnight, 2026', lines=[
        "!Midnight. Pouring rain. 2026.",
        "Behind Jay, a tow truck is dragging his shiny car away.",
        "J|Sam. Buddy. I need to ask you something.",
        "S|Jay, it's midnight. Is that your car?",
        "J|Technically, it's the bank's car. It always was.",
        "Ten years ago, these two started the same job, on the same day, for the same salary.",
        f"Today, one of them has {m(N['now'])}. The other one is about to ask for it.",
        "It all came down to one little box, on one boring form.",
        "I'm Penny. These guys are made up. Every number is real. Let's go back to 2016.",
    ]),
    dict(id='y2016', chapter='2016: the boring form', lines=[
        f"First day at Bluebird Logistics. Two new hires. Same desk. Same salary: {m(N['salary'])} a year.",
        "J|Jay. Twenty-five. Fun guy. Eight thousand followers on Instagram.",
        "S|Sam. Also twenty-five. Eight followers. Four of them are my mom.",
        "Enter Hank from HR. Tie from 1987. Mug: World's Okayest Boss.",
        "H|Gentlemen! Behold, the most exciting paper in America!",
        "H|!The 401(k) form!",
        "J|Hank, you just made this whole room older.",
        "H|Put in six percent of your pay, and the company adds half that. Free money, boys!",
        f"For Sam: {m(N['own'])} a month from his paycheck, plus {m(N['match'])} free from the company.",
        "Sam checks the box.",
        "J|Retirement? Hank, I'm twenty-five. I'm retiring the day I win the lottery.",
        "Jay crumples his form, shoots at the trash can, and misses.",
        "H|I'll keep that one on file. Just in case.",
        f"Nobody knew it yet, but the free money from that box would grow to {m(N['match_now'])} all by itself.",
    ]),
    dict(id='car', chapter='The red car', lines=[
        "First paycheck. Jay walks straight into a car dealership.",
        "J|I'll take the red one. The one that looks fast even when it's parked.",
        f"Price: {m(CAR)}. At the going loan rate, about {N['car_rate']} percent, that's {m(N['car_pay'])} a month. "
        "For six years.",
        f"Plus {m(N['car_interest'])} in interest, just for borrowing.",
        "J|Six years? I'll be thirty-one! That's basically ancient.",
        "Monday, the whole office crowds the parking lot.",
        "A|Okay, Jay. That car is ridiculous. I love it.",
        "Sam drives a beige 2009 sedan. One hubcap. A door that only opens from the outside.",
        "S|It's got character. Mostly rust. But character.",
        "That's Ava, from accounting. Smart, sharp, and she calls everything exactly like it is.",
        "A|Sam, is your car making that noise on purpose?",
        "S|It's... singing. It's happy to see you.",
        "J|Ava! Need a ride? Heated seats.",
        "And Ava climbs in. Into Jay's car.",
        "S|Well. There goes my chance.",
        "But a car payment lasts a lot longer than a car ride.",
    ]),
    dict(id='insta', chapter='Living for the likes', lines=[
        "Jay's Instagram becomes a travel magazine. Cancun. Vegas. A yacht he definitely doesn't own.",
        "J|Living my best life! Hashtag blessed!",
        f"Every trip goes on the credit card. Soon, the balance is {m(CARD)}.",
        "J|Sam, come to Miami! Don't be Boring Sam!",
        "S|Can't. Big weekend. I'm alphabetizing my spices.",
        "S|Also, I'm starting a savings account. The Bad Day Fund.",
        "J|You named a bank account. That's the most Sam thing ever.",
        f"Here's the trap. The card only asks for a small minimum. About {m(N['card_first_min'])} a month.",
        "J|That's nothing! That's like two brunches!",
        f"But at today's average card rate, about {N['card_apr']:.0f} percent, paying only the minimum on {m(CARD)} "
        f"takes {N['card_years']} years.",
        f"!And costs {m(N['card_interest'])} in interest. More than the trips themselves.",
        "About twenty-one years, for a tan that lasted a week.",
        "At the office party, Ava finds Sam at the snack table.",
        "A|Jay took me to a fancy dinner. He talked about his car for an hour. Then his card got declined.",
        "S|Oof. Is that why you're holding eleven mini sandwiches?",
        "A|They're free. And you're the only honest guy in this building.",
        "A|So. Are you going to ask me out, or do I need Hank to give you a form?",
        "First date: Sam's old sedan. Sam runs around to open her door. Every time.",
        "A|This is the most romantic broken car I've ever seen.",
        "Life was good. But a storm was coming.",
    ]),
    dict(id='y2020', chapter='2020: the red button', lines=[
        f"February 2020. Sam has put {m(N['paid_2020'])} into his 401(k). It's worth about {m(N['peak_2020'])}.",
        "S|Jay! Look! It grew!",
        "J|That's fake money, bro. You can't drive it. You can't post it.",
        "!Then March 2020. A virus. The whole world shuts down.",
        "Hank shuffles in with a stack of envelopes.",
        "H|Boys... I'm so sorry. It's not you. It's everybody.",
        "Same job. Same day. Both laid off.",
        f"And on March 23rd, Sam's account hits {m(N['low_2020'])}. More than ten thousand dollars, gone in one month.",
        "Every TV channel says it. Get out. Sell.",
        "Sam's finger hovers over one big red button. SELL.",
        "S|!If I sell right now, at least I keep twenty thousand...",
        "Does he press it? Stay with me, because that one tap is worth tens of thousands of dollars.",
        "And if you like money stories like this, hit subscribe, so you don't miss the next one.",
    ]),
    dict(id='couch', chapter='The couch', lines=[
        "J|!Zero savings. And my car payment is due Friday.",
        "J|Hey, buddy. Quick question. How do you feel about roommates?",
        "Jay moves onto Sam's couch. Two suitcases, a ring light, and a protein shaker.",
        "Sam looks at the red button. Then puts the phone face down.",
        "S|The companies in this fund didn't vanish. People still buy groceries. I'm not selling.",
        "He pauses his contributions until he finds work, and lives on the Bad Day Fund. And beans.",
        "J|Bro. We've had beans nine nights in a row.",
        "S|Ten. Tonight is also bean night.",
        "!Then Sam finds Jay's card bill on the counter.",
        "S|You're still paying the minimum? You'll be paying for Miami when you're forty-five.",
        "J|!You think you're better than me? Mister Spreadsheet. Mister Beans.",
        "S|I think you're my best friend. And I think you're drowning.",
        "J|!At least I actually lived a little!",
        "Jay grabs his ring light, and slams the door.",
        "Best friends since day one. Gone, with one slam.",
    ]),
    dict(id='creep', chapter='Raises and rings', lines=[
        "Late summer 2020. Both get rehired.",
        "And the market? By August, a brand new record. Sam never sold, so he never missed the bounce back.",
        "They get the same raises. Jay's go to a bigger apartment, and a newer, bigger car, with a bigger payment.",
        "J|A raise means upgrade, baby! It's literally in the name!",
        "That's lifestyle creep. Pay goes up, spending goes up faster.",
        f"Sam kept his same {m(N['own'])} a month going into the 401(k), same as day one. His raises went into savings.",
        "And next to the old sedan, Sam gets down on one knee.",
        "A|Yes! Obviously yes. Get up, your knee is in a puddle.",
        "A fancy wedding costs about as much as Jay's car.",
        "S|I mean... I could take it out of the 401(k)...",
        "A|Sam. If you touch that account, I'm marrying Hank.",
        "H|I'm free on weekends!",
        "So: a small one. Backyard, string lights, tacos. The 401(k) stays untouched.",
        "S|Should we invite Jay?",
        "A|You haven't talked in years. Your call.",
        "Sam stares at the empty line on the list. Then, one rainy night, somebody knocks.",
    ]),
    dict(id='reveal', chapter='The ask', lines=[
        "Midnight. Rain. The tow truck pulls away.",
        "J|They took the car. My card is maxed. Rent is due. I need ten thousand dollars. I'll pay you back. Probably.",
        "S|Come inside. You're dripping on my welcome mat.",
        "Sam opens his laptop, and turns it around.",
        f"!{m(N['now'])}.",
        "J|!What? How? We made the same money! You drive a car with no hubcaps!",
        "S|One hubcap. Let me show you.",
        f"S|I put in {m(N['own_paid'])} of my own money. Same three hundred a month, whenever I had a job.",
        f"S|The company added {m(N['match_paid'])}. Free. From the box you threw at the trash can.",
        "S|And the market did the rest. Even after the night I almost hit the red button.",
        "J|So that little box...",
        "S|That little box.",
    ]),
    dict(id='ending', chapter='The best man', lines=[
        "Sam hands him a piece of paper. Not a check.",
        "J|What is this?",
        "S|I called Hank. He kept your crumpled form from 2016. This is the 2026 edition.",
        "S|No cash. But a plan. Check the box. Pay way more than the minimum. Cheaper car. And start a Bad Day Fund.",
        "J|You're giving me homework? At midnight?",
        "S|Bean night rules.",
        "Jay laughs. Picks up the pen. And checks the box.",
        "Three months later. String lights. Tacos. And a best man in a very shiny suit.",
        "J|To the most boring man I know. Who was right. About everything. Don't tell him I said that.",
        "A|Too late. I'm recording.",
        "H|I'm not crying. The salsa is spicy.",
        "Three lessons. One: if your job offers a free match, check the box.",
        "Two: minimum payments and giant car payments quietly eat a good salary.",
        "Three: when the market crashes, don't press the red button.",
        "Jay and Sam are made up, and so are their choices. The rates and market returns are real, before fees and "
        "taxes. This is education, not financial advice.",
        "Now tell me in one word: are you Jay, or Sam?",
        "And send this to a friend who still thinks retirement is a problem for later.",
        "I'm Penny. Subscribe for more money stories, and I'll see you next time.",
    ]),
]

assert N['now'] == 126766 and N['match_now'] == 42255 and N['own'] == 300 and N['match'] == 150
assert CAR == 40000 and CARD == 6000 and N['car_pay'] == 637 and round(N['card_apr']) == 22
assert 20.5 < N['card_years'] < 21 and N['card_interest'] > CARD and N['peak_2020'] - N['low_2020'] > 10000
assert 20000 < N['low_2020'] < 21000 and N['own_paid'] + N['match_paid'] == N['paid'] and N['card_first_min'] == 172

if __name__ == '__main__':
    words = sum(len(ln.split('|')[-1].split()) for s in SCENES for ln in s['lines'])
    talk = sum(1 for s in SCENES for ln in s['lines'] if '|' in ln)
    total = sum(len(s['lines']) for s in SCENES)
    print('words', words, 'lines', total, 'character lines', talk)
    for s in SCENES:
        print(f"  {s['id']:8s} {sum(len(ln.split('|')[-1].split()) for ln in s['lines'])}")
    print('max words/line', max(len(ln.split('|')[-1].split()) for s in SCENES for ln in s['lines']))
