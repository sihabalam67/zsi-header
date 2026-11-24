# Trend Report: Animated money stories and everyday-money explainers · Nov 24, 2026

Made for Coin Theory with the `trend-report`, `script-breakdown` and `title-formulas` skills, run in their **Without TubeLab** mode.

- **Top finding:** "Get rich on a low salary" stories won hardest. Three small channels made 33x to 482x their median views with it, and two of them used the same 1904 Japanese notebook method (Kakeibo).
- **Sample:** 389 videos at 3x or more their channel's median, from 108 channels, published Nov 24, 2025 to Nov 24, 2026. About 40 of them are English everyday-money videos. The rest were Hindi, kids' cartoons, Minecraft, anime recaps or AI-tutorial videos.

## How this was made, and what is lost without TubeLab

- **Searches:** 10 YouTube Data API searches, ordered by views, from the last 12 months, US and English. The queries were "animated money story", "personal finance story animation", "rich vs poor animation money", "inflation explained animation", "compound interest story", "frugal millionaire story", "401k explained simply", "grocery prices why", "why everything is so expensive explained" and "how money works animated".
- **Baseline:** for 182 channels with 5K to 3M subscribers, we read their last 50 uploads. We dropped Shorts (3 minutes or less) and kept the 30 most recent long videos. 108 channels had at least 8 of them. Ratio = views ÷ that channel's median views.
- **Quota used:** about 1,373 units (1,000 for searches, 9 for channel reads, 364 for upload reads).
- **Transcripts:** YouTube auto-captions through yt-dlp worked for 9 videos. NerdWallet's video was blocked by YouTube's "confirm you're not a bot" check, so its beats come from the description's chapters.
- **Thumbnails:** all 8 winners' `mqdefault.jpg` images loaded and were viewed.
- **What is lost:**
  - We could only test channels these 10 searches surfaced, so this is not a full outlier index.
  - The search ranks by views, so it surfaces bigger channels first.
  - We have no trending-formula index, so we have no video counts, growth or click triggers for each formula. The formulas below are proven only by the outliers we found.
  - We have no audience age or income data.
  - Ratios use the median of the last 30 long uploads, not a channel's lifetime average. Very new uploads have a low ratio only because they are new.

## Trending Videos

### 1. [The Japanese Art of Becoming Rich on a Low Salary | A Story About Quiet Wealth](https://www.youtube.com/watch?v=5IcV9Rw0u-c)

[![](https://i.ytimg.com/vi/5IcV9Rw0u-c/mqdefault.jpg)](https://www.youtube.com/watch?v=5IcV9Rw0u-c)

- [Will & Wisdom](https://www.youtube.com/@thewillwisdom) · 20.2K subs · May 25, 2026 · 17.7 min · faceless, illustrated, narrated
- **Views:** 905,163 | **482X Outlier** (channel median 1,877) · 16,628 likes · 743 comments
- **Hook:** `Imagine two men standing in the rain. The first man is holding a massive bucket, but the bucket has a hundred holes in the bottom.`
- **Title formula:** `The [Culture] Art of [Becoming Rich] on a [Low Salary] | A Story About [Theme]`.
- **Thumbnail:** a warm illustrated man in a kimono writes in a notebook at a low table. The text says "Become Rich On Low Salary" in yellow and white, with kanji on the wall. It shows a calm, doable promise and no chart.
- **Why it worked:** *it promises wealth without a raise, it is set in a calm and foreign place, and it is one simple method the viewer can start tonight.*

### 2. [Why You Can't Leave the House For Under $100 | NerdWallet](https://www.youtube.com/watch?v=knOpgZm8oSk)

[![](https://i.ytimg.com/vi/knOpgZm8oSk/mqdefault.jpg)](https://www.youtube.com/watch?v=knOpgZm8oSk)

- [NerdWallet](https://www.youtube.com/@nerdwallet) · 306K subs · Oct 20, 2026 · 8.5 min · **host on camera, not faceless**
- **Views:** 306,841 | **126X Outlier** (median 2,437 across 12 long uploads; the channel posts mostly Shorts)
- **Hook:** no transcript, because YouTube's bot check blocked the caption request. The description opens with: "The cost of living, lifestyle creep, and the rising cost of socializing are making an ordinary day out surprisingly expensive. We track a $100 afternoon in New York City…"
- **Title formula:** `Why You Can't [Ordinary Thing] For Under $[Number]`.
- **Thumbnail:** a puzzled woman shrugs next to "IT'S NOT THE $7 COFFEE", with "NOT" in red. The thumbnail argues against the title's obvious answer.
- **Why it worked:** *everyone has felt this exact price. The thumbnail then denies the cliché answer, so the viewer has to click to learn the real one.*

### 3. [The $5,000 Trump Dividend Isn't What You Think – Explained Like You're Five](https://www.youtube.com/watch?v=y6J1acI_Xm0)

[![](https://i.ytimg.com/vi/y6J1acI_Xm0/mqdefault.jpg)](https://www.youtube.com/watch?v=y6J1acI_Xm0)

- [Explaining Economics Like You're Five](https://www.youtube.com/@explainingeconlikeyourefive) · 18.6K subs · Oct 16, 2026 · 11.0 min · faceless, cartoon explainer
- **Views:** 86,855 | **97X Outlier** (median 891)
- **Hook:** `Every adult citizen gets $5,000 if Republicans keep control of Congress. That's the promise and it has a lot of people asking how it would actually work.`
- **Title formula:** `The $[Number] [Thing in the News] Isn't What You Think – Explained Like You're Five`.
- **Thumbnail:** a cartoon Capitol and a "$5,000 PROPOSED" check behind a padlock, with a red arrow and "THE CATCH" across the top. It uses one number, one object and one word that opens a question.
- **Why it worked:** *a big personal number from the news, a promise to explain it simply and fairly, and the hint of a catch.*

### 4. [How AI Became More Expensive Than The Workers It Replaced](https://www.youtube.com/watch?v=cfaZZPjA3g0)

[![](https://i.ytimg.com/vi/cfaZZPjA3g0/mqdefault.jpg)](https://www.youtube.com/watch?v=cfaZZPjA3g0)

- [Economy Media](https://www.youtube.com/@economymedia) · 141K subs · Jul 2, 2026 · 11.3 min · faceless, news clips with narration
- **Views:** 4,003,870 | **57.5X Outlier** (median 69,675)
- **Hook:** `In 2022, chat GPT was released to the market and since then the growth of AI has been impressive.`
- **Title formula:** `How [Thing] Became More Expensive Than [What It Replaced]`. The same channel also has "How AI Is Making Everything More Expensive", at 18.9X.
- **Thumbnail:** a stressed man rubs his head in front of a Google sign, with "Back To Human Workers" on a red bar. It shows a reversal the viewer did not expect.
- **Why it worked:** *a reversal of what everyone assumed, told as a story about jobs and money.*

### 5. [If You're Earning a Low Salary, Watch This and Thank Me Later Powerful Story](https://www.youtube.com/watch?v=UnsT0ARtT5Y)

[![](https://i.ytimg.com/vi/UnsT0ARtT5Y/mqdefault.jpg)](https://www.youtube.com/watch?v=UnsT0ARtT5Y)

- [The Journey Within](https://www.youtube.com/@thejourneywithin-yt) · 36.2K subs · Jul 11, 2026 · 16.8 min · faceless, illustrated story
- **Views:** 928,244 | **43X Outlier** (median 21,549) · 36,479 likes · 1,242 comments
- **Hook:** `Let me ask you one question. Have you ever received your salary, looked at your bank account a week later, and wondered, "Where did all my money go?"`
- **Title formula:** `If You're [Painful Situation], Watch This [Payoff Phrase]`.
- **Thumbnail:** a young man writes in a notebook at night, with cash and a calculator on the desk, and "BECOME RICH ON LOW SALARY". The text is **the same as #1's thumbnail**, on a different channel.
- **Why it worked:** *the viewer sees their own payday in the first sentence, and a named everyman (Michael, a supermarket attendant) carries the lesson.*

**Runners-up that back the patterns:**

| Video | Channel (subs) | Views | Ratio | Date |
|---|---|---:|---:|---|
| [The Japanese Art of Getting Rich on an Ordinary Salary](https://www.youtube.com/watch?v=IwgtXRzh9W4) | [Bille Finance](https://www.youtube.com/@bille_finance) (27.6K) | 311,923 | 33.5X | Sep 10, 2026 |
| [A Day in the Life of a Quiet Millionaire](https://www.youtube.com/watch?v=ne_ZlaNw1M4) | [Bille Finance](https://www.youtube.com/@bille_finance) | 215,007 | 23.1X | Jul 29, 2026 |
| [The Japanese Art of Building Wealth With Almost Nothing](https://www.youtube.com/watch?v=rhSrp3S7XQY) | [Will & Wisdom](https://www.youtube.com/@thewillwisdom) | 149,630 | 79.7X | Jun 29, 2026 |
| [The Japanese Money Method That Forces You to Save](https://www.youtube.com/watch?v=vUkFfDYdwZU) | [Will & Wisdom](https://www.youtube.com/@thewillwisdom) | 96,853 | 51.6X | May 5, 2026 |
| [Macroeconomics Made Simple (Understand the Economy in One Video)](https://www.youtube.com/watch?v=xmdBlkrkTN4) | [Martik Finance](https://www.youtube.com/@martikfinance) (107K) | 616,931 | 25.7X | Feb 8, 2026 |
| [What If You Could See Everyone's Future Wealth?](https://www.youtube.com/watch?v=DK4EOHCrVvM) | [ConChaser](https://www.youtube.com/@conchaser) (34.4K) | 2,460,081 | 23.1X | Oct 25, 2026 |
| [Once You Understand MONEY, You'll Stop Saving It [PART #1]](https://www.youtube.com/watch?v=mnuOZcmoGD8) | [LITTLE BIT BETTER](https://www.youtube.com/@littlebitbetter7) (1.45M) | 4,028,581 | 17.7X | May 3, 2026 |
| [Once You Understand Economics, You Can't Be MANIPULATED Anymore [PART #10]](https://www.youtube.com/watch?v=zxVoCw3P1Gc) | [LITTLE BIT BETTER](https://www.youtube.com/@littlebitbetter7) | 4,532,940 | 19.9X | Mar 1, 2026 |
| [12 WORST Grocery Stores You Should NEVER BUY Steak At All cost](https://www.youtube.com/watch?v=R3yqib_wsAY) | [Consumer Watch](https://www.youtube.com/@consumerwatch-y3r) (14.9K) | 815,704 | 47.7X | Oct 25, 2026 |

**Left out:**
- Hindi and Urdu videos, even where the language tag said English.
- Kids' cartoons, Minecraft and anime recaps.
- AI-tutorial channels.
- Dr. Dicle's CFA lecture batch, where ratios of 15x to 19x come from a median of 243 views.
- A Rich vs Poor sketch channel with a sketch audience.

## Script Breakdowns (top 3)

### [The Japanese Art of Becoming Rich on a Low Salary](https://www.youtube.com/watch?v=5IcV9Rw0u-c) · [Will & Wisdom](https://www.youtube.com/@thewillwisdom) · 905K views, 482X, 17.7 min

- **Hook (0:00 to 0:30):** "Imagine two men standing in the rain. The first man is holding a massive bucket, but the bucket has a hundred holes in the bottom. The rain pours in. He is making a lot of money, but it pours out just as fast. At the end of the storm, his bucket is empty. He is exhausted, stressed, and broke. The second man is holding a small cup, but his cup is solid steel. No holes."
- **What it does:** one picture holds the whole thesis: income is the rain, and habits are the holes.
- **Against a weak video:** [How Samurai Trained Their Mind to Never Give Up](https://www.youtube.com/watch?v=9UJ1TEMUIQ0) · 0.10X · it opens with an equally vivid cliff scene, but it has no money and no personal stake for the viewer.

| Time | Beat | What happens |
|---|---|---|
| [0:00](https://www.youtube.com/watch?v=5IcV9Rw0u-c&t=0s) | hook | The bucket with holes vs the steel cup in the rain |
| [0:59](https://www.youtube.com/watch?v=5IcV9Rw0u-c&t=59s) | stakes | "We are obsessed with income… you just speed up the flow of waste" |
| [1:24](https://www.youtube.com/watch?v=5IcV9Rw0u-c&t=84s) | proof | 1904, Hani Motoko invents Kakeibo; households save "up to 35%" |
| [2:06](https://www.youtube.com/watch?v=5IcV9Rw0u-c&t=126s) | promise | "We are going to show you how to patch the holes in your bucket" |
| [2:25](https://www.youtube.com/watch?v=5IcV9Rw0u-c&t=145s) | open loop | "The trap of invisible money": tap-to-pay and the "pain of paying" |
| [4:16](https://www.youtube.com/watch?v=5IcV9Rw0u-c&t=256s) | mini-payoff | Four questions; "$3,000 income, save $500 first, live on $2,500" |
| [6:04](https://www.youtube.com/watch?v=5IcV9Rw0u-c&t=364s) | mini-payoff | Four spending buckets; "that is an autopsy… Kakeibo is a daily checkup" |
| [8:14](https://www.youtube.com/watch?v=5IcV9Rw0u-c&t=494s) | mini-payoff | Cash envelopes: "An empty envelope cannot buy a beer" |
| [9:43](https://www.youtube.com/watch?v=5IcV9Rw0u-c&t=583s) | re-hook | The 30-day wish list: "90% of the time, the urge will be gone" |
| [11:03](https://www.youtube.com/watch?v=5IcV9Rw0u-c&t=663s) | re-hook | Mottainai: "Repairing a shirt is an act of rebellion" |
| [12:12](https://www.youtube.com/watch?v=5IcV9Rw0u-c&t=732s) | mini-payoff | Monthly review: "Why did I spend $200 on Uber Eats?" |
| [13:35](https://www.youtube.com/watch?v=5IcV9Rw0u-c&t=815s) | payoff | "Man A makes $200,000 and spends $200,000… Man B makes $50,000, spends $30,000" |
| [15:18](https://www.youtube.com/watch?v=5IcV9Rw0u-c&t=918s) | payoff | "The ledger proves you are a liar. Align your spending with your soul." |
| [16:21](https://www.youtube.com/watch?v=5IcV9Rw0u-c&t=981s) | call to action | 7-day challenge; "Confess your guilty pleasure expense in the comments" |

### [Why You Can't Leave the House For Under $100](https://www.youtube.com/watch?v=knOpgZm8oSk) · [NerdWallet](https://www.youtube.com/@nerdwallet) · 307K views, 126X, 8.5 min

- **Hook:** we could not get it. YouTube's bot check blocked the transcript, so these beats come from the description and chapters. The beat types are inferred from the chapter titles.
- **What it does:** it starts by tracking one real $100 afternoon in New York City, which is a concrete receipt rather than an abstract "cost of living" claim.
- **Against a weak video:** [First Time Home Buyers: 5 Things You NEED To Know Before You Buy](https://www.youtube.com/watch?v=0PfEPz_jEyI) · 0.24X · a generic how-to list with no price you have felt and no myth to break.

| Time | Beat | Chapter |
|---|---|---|
| [0:00](https://www.youtube.com/watch?v=knOpgZm8oSk&t=0s) | hook | Why Does Leaving the House Cost $100? (tracked afternoon in NYC) |
| [2:02](https://www.youtube.com/watch?v=knOpgZm8oSk&t=122s) | stakes | Is Social Spending Really Optional? |
| [2:34](https://www.youtube.com/watch?v=knOpgZm8oSk&t=154s) | proof | Third Places: Why Affordable Hangouts Are Disappearing |
| [3:43](https://www.youtube.com/watch?v=knOpgZm8oSk&t=223s) | re-hook | The Access Economy: Paying for Community |
| [5:22](https://www.youtube.com/watch?v=knOpgZm8oSk&t=322s) | mini-payoff | Why Socializing Has Become So Expensive |
| [6:19](https://www.youtube.com/watch?v=knOpgZm8oSk&t=379s) | payoff | Saving Money vs. Having a Social Life |
| [7:08](https://www.youtube.com/watch?v=knOpgZm8oSk&t=428s) | mini-payoff | Is Your Gym Membership Actually Worth It? |
| [7:46](https://www.youtube.com/watch?v=knOpgZm8oSk&t=466s) | payoff | Is Lifestyle Creep Really Keeping You Poor? (then the newsletter call to action) |

### [The $5,000 Trump Dividend Isn't What You Think](https://www.youtube.com/watch?v=y6J1acI_Xm0) · [Explaining Economics Like You're Five](https://www.youtube.com/@explainingeconlikeyourefive) · 87K views, 97X, 11.0 min

- **Hook (0:00 to 0:23):** "Every adult citizen gets $5,000 if Republicans keep control of Congress. That's the promise and it has a lot of people asking how it would actually work. Today, I'll explain how the $5,000 Trump dividend would actually work to you like you're 5 years old. No sides taken here. We'll look at what supporters say, what critics say, where the money would come from, and what has to happen for it to become real."
- **What it does:** it states the money promise, then sets the rules: simple, fair, and four questions answered.
- **Against a weak video:** [What Happens If You Get Sent to COLLECTIONS](https://www.youtube.com/watch?v=7bR4PYISS7c) · 0.28X · it has a good scene-style hook, but no news peg and no number the viewer hopes to receive. It is also only 12 days old, so its ratio may still rise.

| Time | Beat | What happens |
|---|---|---|
| [0:00](https://www.youtube.com/watch?v=y6J1acI_Xm0&t=0s) | hook | "Every adult citizen gets $5,000 if…" |
| [0:09](https://www.youtube.com/watch?v=y6J1acI_Xm0&t=9s) | promise | Explained like you're five, "no sides taken", the four questions |
| [0:58](https://www.youtube.com/watch?v=y6J1acI_Xm0&t=58s) | stakes | "Right now, it's a promise, not a law" |
| [1:22](https://www.youtube.com/watch?v=y6J1acI_Xm0&t=82s) | mini-payoff | The government's money is a kitchen jar: taxes, tariffs and "the credit card" |
| [2:38](https://www.youtube.com/watch?v=y6J1acI_Xm0&t=158s) | proof | "245 million adults… about 1.2 trillion"; 2,700 years at $1M a day |
| [3:15](https://www.youtube.com/watch?v=y6J1acI_Xm0&t=195s) | mini-payoff | How a bill becomes a check: "both parents have to agree" |
| [4:35](https://www.youtube.com/watch?v=y6J1acI_Xm0&t=275s) | re-hook | "Wait, has the government actually done this before?" ($1,200, $600, $1,400; Alaska) |
| [5:51](https://www.youtube.com/watch?v=y6J1acI_Xm0&t=351s) | proof | What supporters say, then what critics say |
| [7:00](https://www.youtube.com/watch?v=y6J1acI_Xm0&t=420s) | open loop | "The inflation question, which is a little tricky": the lemonade stand |
| [8:14](https://www.youtube.com/watch?v=y6J1acI_Xm0&t=494s) | payoff | Kitchen-table math: "two $5,000 checks would be $10,000" |
| [9:14](https://www.youtube.com/watch?v=y6J1acI_Xm0&t=554s) | payoff | Six steps that must happen in order |
| [9:56](https://www.youtube.com/watch?v=y6J1acI_Xm0&t=596s) | mini-payoff | Scam warning: "Anyone asking you for a fee… is not the government" |
| [10:22](https://www.youtube.com/watch?v=y6J1acI_Xm0&t=622s) | call to action | Recap; "hold off on buying that fancy couch" |

**Other hooks, quoted word for word:**
- [Bille Finance, 33.5X](https://www.youtube.com/watch?v=IwgtXRzh9W4): "You wake up at 6:10 in a one-bedroom apartment… You make $54,000 a year… You have $312,000… Your manager earns $190,000 a year and owes $41,000."
- [ConChaser, 23X](https://www.youtube.com/watch?v=DK4EOHCrVvM): "Sir, you dropped this. You bend down to pick up a $5 bill. The homeless man turns around, and that's when you see it, floating above his head. $8,742,619,300."
- [LITTLE BIT BETTER, 17.7X](https://www.youtube.com/watch?v=mnuOZcmoGD8): "Nobody teaches you the truth about money." It then turns to the stone money of Yap in 1903.

### Shared layout (it appears in 4 of the 5 scripted winners)

Hook: a concrete scene with a number (0:00) → Promise: what you'll learn, plus a fairness or simplicity contract (0:10 to 2:00) → Origin or proof: a dated piece of history or a big number made small (1:00 to 3:00) → 4 to 7 named mini-chapters, each with one dollar example (every 60 to 120 seconds) → a re-hook question in the second half ("Has this happened before?", "Why did I spend $200 on Uber Eats?") → Payoff: household math with two people side by side → Call to action: a small challenge plus a comment prompt.

## Winning Patterns

- **Topics:** saving on an ordinary salary, why ordinary life costs so much, explaining a money headline, and a hidden net worth.
- **Hooks:** they open with a **scene** ("Imagine two men…", "You wake up at 6:10…") or **a number the viewer wants** ("$5,000"). They then **contrast two people** (income vs wealth) and **date a source** ("In 1904…").
- **Triggers:** relief, because you don't need a raise (#1, #5, Bille). Outrage at prices (#2, #4). Hope of free money with suspicion of a catch (#3). Envy and curiosity (ConChaser).

### Five recurring title formulas, with proof

These are proven only by outliers in this niche. TubeLab was not used, so there are no counts from across YouTube.

| # | Formula | Proof (ratio) |
|---|---|---|
| 1 | `The [Culture] [Art/Method] of [Getting Rich] on a [Low/Ordinary] Salary` | [Will & Wisdom 482X](https://www.youtube.com/watch?v=5IcV9Rw0u-c), [79.7X](https://www.youtube.com/watch?v=rhSrp3S7XQY), [51.6X](https://www.youtube.com/watch?v=vUkFfDYdwZU), [46X](https://www.youtube.com/watch?v=3NoyEhrOfeQ); [Bille Finance 33.5X](https://www.youtube.com/watch?v=IwgtXRzh9W4). That is 2 channels; the "rich on a low salary" promise also appears on a third, [The Journey Within 43X](https://www.youtube.com/watch?v=UnsT0ARtT5Y). |
| 2 | `Why [Everyday Thing] Costs [$N] Now` / `How [X] Became More Expensive Than [Y]` | [NerdWallet 126X](https://www.youtube.com/watch?v=knOpgZm8oSk); [Economy Media 57.5X](https://www.youtube.com/watch?v=cfaZZPjA3g0) and [18.9X](https://www.youtube.com/watch?v=JlmLdvCM-ZI) |
| 3 | `The $[N] [Headline] Isn't What You Think – Explained Like You're Five` / `[Topic] Made Simple` | [ELI5 97X](https://www.youtube.com/watch?v=y6J1acI_Xm0); [Martik Finance 25.7X](https://www.youtube.com/watch?v=xmdBlkrkTN4) |
| 4 | `Once You Understand [MONEY TOPIC], You'll [Never/Stop] [Common Habit]` | [LITTLE BIT BETTER 17.7X](https://www.youtube.com/watch?v=mnuOZcmoGD8), [19.9X](https://www.youtube.com/watch?v=zxVoCw3P1Gc), [8.9X](https://www.youtube.com/watch?v=C8KULYii7NY). One channel only, so it is a series format to test. |
| 5 | `What If You Could See Everyone's [Money Secret]?` / `[A Day in the Life / POV] of a [Quiet Millionaire]` | [ConChaser 23.1X](https://www.youtube.com/watch?v=DK4EOHCrVvM); [Bille Finance 23.1X](https://www.youtube.com/watch?v=ne_ZlaNw1M4) and [6.7X](https://www.youtube.com/watch?v=EgQ0zlFWjRg) |

Shared title traits:
- A dollar figure or "salary" in the first 40 characters.
- A promise of relief or a myth to break.
- Thumbnail text of 3 to 5 words that does not repeat the title, such as "IT'S NOT THE $7 COFFEE" or "THE CATCH".

### Five changes for our story scripts and explainers

1. **Open on a scene or a personal number, never on the topic.** Start the first line with a picture ("Imagine two men…", "You wake up at 6:10…") or a dollar figure the viewer feels ("$5,000", "$100"). In the first 15 seconds, show two people with the same problem and different outcomes. Our gold video held 66% at 30 seconds; every winner opens this way.
2. **Make a promise and set the rules by 0:20.** Say the four questions you will answer and add "no sides taken" or "explained simply". ELI5 does this in 20 seconds. Cut "like and subscribe" before the story starts; The Journey Within does it there and still won, but none of the others do.
3. **Build in named chapters with one dollar example each, every 60 to 120 seconds.** Put a re-hook question in the back half ("Has this happened before?"). Name the chapters in the description, as NerdWallet and Economy Media do. Our scripts should not run for more than about 2 minutes without a new chapter card.
4. **Make them longer.** The story winners run 16 to 19 minutes and the explainers run 8.5 to 11.3. Our long videos average about 8 minutes, and we now keep 3 to 4 minutes on average. Make the everyday explainers 10 to 12 minutes and test one 14 to 16 minute story each week. Add length only as new chapters, never as padding.
5. **End at the kitchen table, then give a small challenge.** Turn the macro number into one household's math, such as "two checks = $10,000" or "Man A vs Man B". Then add a warning or habit for the viewer to try and one comment prompt ("Confess your guilty-pleasure expense"; that video drew 743 comments). Cite every number on screen from BLS, the Fed, the IRS or USDA.

## Video Ideas for Coin Theory

Each idea gives its source for the numbers. No outlier's title is copied; each keeps the shape and changes the topic.

1. **The $5 Notebook That Beat a $190K Salary**
   - A story of two coworkers, one using a Kakeibo-style ledger (formula 1, 482X and 33.5X). The numbers come from BLS Consumer Expenditure Survey shares.
   - Opening line: `Two coworkers. One earns $54,000, the other earns $190,000. Only one of them can quit at 50.`
2. **Why a Night Out Now Costs $100**
   - An animated receipt of an ordinary evening for a family of two (formula 2, NerdWallet 126X). The numbers come from BLS CPI for food away from home, admission tickets and transit since 2020.
   - Opening line: `Dinner, a movie, and a ride home. In 2019 that was $[X, from CPI]. Tonight it's $100. Here's where the difference went.`
3. **Grocery Prices, Explained Like You're Five**
   - A kitchen-jar explainer of where a $100 grocery bill goes (formula 3, ELI5 97X). The numbers come from the USDA ERS Food Dollar series and BLS CPI food at home.
   - Opening line: `You hand the cashier $100. Only a small slice of it ever reaches a farmer. Let's follow the rest.`
4. **What If You Could See Everyone's Savings?**
   - Numbers float over people's heads, and the rich-looking neighbor has the smallest one (formula 5, ConChaser 23X). The numbers come from the Fed's SHED report on emergency savings and the Survey of Consumer Finances medians by age.
   - Opening line: `The man in the new truck has $412 over his head. The woman at the bus stop has $186,000.` (These are story numbers; anchor the real ones to SHED and SCF.)
5. **The $7 Coffee Isn't Why You're Broke**
   - A myth-buster with real household math (the NerdWallet thumbnail, 126X, and formula 3). The numbers come from BLS Consumer Expenditure shares for housing, transport and food against coffee.
   - Opening line: `Skip a $7 coffee every day for a year and you save $2,555. Now look at what your rent did.`
6. **Once You Understand Inflation, You'll Stop Hiding Cash**
   - An animated story: Grandma's coffee can of cash, 2015 to 2026 (formula 4, LITTLE BIT BETTER 17.7X). The numbers come from the BLS CPI inflation calculator against a high-yield savings rate.
   - Opening line: `In 2015, Grandma hid $10,000 in a coffee can. It's all still there. It just buys a lot less.`
7. **A Day in the Life of a $60K Millionaire**
   - Second-person story, from a 6 a.m. alarm to the 401(k) statement (formula 5, Bille Finance 23.1X). The numbers come from IRS 401(k) limits and Vanguard's "How America Saves" match data.
   - Opening line: `You make $60,000. You drive a 2014 Corolla. And on Tuesday, your 401(k) crossed seven figures.`
8. **Why Everything Costs More After a Tariff**
   - A family story that follows one imported item from the port to the shelf (formula 2, Economy Media 57.5X; "tariffs" is also a high-demand scout topic). The numbers come from the BLS import price index and CPI for the item.
   - Opening line: `This $30 toaster crossed an ocean, paid a toll at the border, and you paid that toll too.`
9. **The $5 Allowance That Became $40,000**
   - A family-friendly compound interest story, from a parent and kid to age 30 (formula 1's "rich on little" promise). The numbers come from historical S&P 500 total returns, and the math is shown on screen.
   - Opening line: `Two kids get the same $5 a week from age 5. At 30, one has a drawer of receipts. The other has about $25,000.`
   - Math check: $260 a year for 25 years at 10% a year comes to about $25,600. Show the rate as an assumption on screen.
10. **Your 401(k), Explained Like You're Five**
    - A jar-and-match explainer for first-job viewers aged 23 to 30 (formula 3, ELI5 97X, plus our scout's 401(k) topic at about 52K views a day). The numbers come from IRS 2026 contribution limits and Vanguard's average employer match.
    - Opening line: `Your boss is offering you free money, and a lot of people say no without knowing it. Here's how it works.`

**Before using these:**
- Check every statistic against its named source before it goes in a script.
- Do not promise our channel these multiples. A small channel's 482X proves the format works, not that we will get the same result.
- Check the "Japanese method" angle for saturation first. Two channels already run it, so put our own twist on it, such as an American family or the real BLS budget.
