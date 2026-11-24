# Format test: which kind of video do people follow? (started Nov 24, 2026)

Owner's order: mix different types of video and let the numbers decide. Every video gets a `format` in
channel/out/styles.json; `python3 youtube/learn.py` prints "By FORMAT" (first-3-day views, % still watching at
30 s, average view, new subscribers). Rotate so no format runs twice in a row; after ~3 videos per format, give
more slots to the winners and drop the losers (decided in the Thursday report).

| # | Format | What it is | Proof it can work | Ours so far |
|---|---|---|---|---|
| 1 | news explainer | today's money headline explained (market drop, Fed, gold) | Gold 1,602 views (our best) | ep01-ep13 |
| 2 | family parable story | made-up family, real numbers, a money lesson | Will & Wisdom 482x | s01, s02 |
| 3 | mystery story | a hidden fortune / a puzzle solved over the video | "hidden millionaire" stories 1-4M | s03 |
| 4 | **superpower "What if" story** | POV ("you") story with an impossible power that reveals real money data | ConChaser 2.46M views, 23x its normal | **next: s04 (Dec 2)** |
| 5 | true history story | a real money event told like a thriller | "Why your coins have ridges" 1.6M on a 650-sub channel | s05 Newton vs the Counterfeiter |
| 6 | explained like you're five | one confusing money thing made simple with jars and toys | ELI5 channel 97x | idea bank #3, #10 |
| 7 | why it costs $N now | an everyday bill broken down like a receipt | NerdWallet 126x | idea bank #2, #5 |

Rules for every format: originality gate (tools/originality.py), story bible for stories, the child test for
thumbnails, real sourced numbers (a superpower is fiction; the numbers it reveals are not).
