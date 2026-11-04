# Scout log

## 2026-11-04 test run (3 of 25: BasinCheck, ECOMSTATEMENT.COM, DevOps Daily)
Source: https://trustmrr.com/api/ai/discovery → `fastestGrowingStartups` (25 entries, 3 with stealthMode: true). The .md pages were fetched on 2026-11-04.

### BasinCheck (`basincheck`)
- TrustMRR: https://trustmrr.com/startup/basincheck · md: https://trustmrr.com/startup/basincheck.md
- Site: https://basincheck.com/ | stealthMode: false
- Payment provider: Stripe (API key) | **API key expired 2026-10-23**, revenue last synced 2026-10-23
- Revenue section: 24h $0.00 / 7d $0.00 / 30d **$2.98** / 3mo $2,643 / 12mo $5,579 / all-time $5,579
- Snapshot line: $2,226. **MISMATCH:** the snapshot is stale, and the Revenue table says $2.98.
- Daily (last 30): paid days 1/30 · biggest day $2.98 on 2026-10-20 = 100% of 30d
- Monthly timeline: 2026-07 $405 · 2026-08 $405 · 2026-09 $2,235 · 2026-10 $2.98
- MRR / active subscriptions: $895 / 5 (snapshot, stale sync)
- Pricing (founder text): Starter $125/mo, Standard $250/mo, Pro $500/mo
- Channels (TrustMRR): empty
- Founder X followers: 132

### ECOMSTATEMENT.COM (`ecomstatement-com`)
- TrustMRR: https://trustmrr.com/startup/ecomstatement-com · md: https://trustmrr.com/startup/ecomstatement-com.md
- Site: https://ecomstatement.com/ | stealthMode: false
- Payment provider: Stripe (API key) | revenue last synced 2026-11-03
- Revenue section: 24h $0.00 / 7d $1,112 / 30d **$3,304** / 3mo $3,432 / 12mo $3,883 / all-time $3,883
- Snapshot line: $3,304 (matches)
- Daily (last 30): paid days 6/30 (10-19 $29, 10-21 $842, 10-23 $35.38, 10-24 $1,120, 10-26 $164, 10-27 $1,112) · biggest day $1,120 on 2026-10-24 = 34% of 30d
- Monthly timeline: 2026-07 $64.38 · 2026-08 $64.38 · 2026-09 $64.38 · 2026-10 $3,304
- MRR / active subscriptions: not shown
- Pricing (founder text): free trial; Small $29/mo, Starter $49/mo, Unlimited $99/mo; yearly options
- Channels (TrustMRR): empty
- Founder X followers: 175

### DevOps Daily (`devops-daily`)
- TrustMRR: https://trustmrr.com/startup/devops-daily · md: https://trustmrr.com/startup/devops-daily.md
- Site: https://devops-daily.com/ | stealthMode: false
- Payment provider: Stripe (API key) | revenue last synced 2026-11-03
- Revenue section: 24h $0.00 / 7d $19.00 / 30d **$3,619** / 3mo $11,147 / 12mo $22,157 / all-time $22,157
- Snapshot line: $3,619 (matches; the discovery JSON said $3,628)
- Daily (last 30): paid days 4/30 · biggest day **$3,500 on 2026-10-17 = 97% of 30d**
- Monthly timeline: 2026-07 $5,500 · 2026-08 $3,010 · 2026-09 $4,519 · 2026-10 $3,628
- MRR / active subscriptions: not shown
- Pricing (founder text): Free, $0 forever. Revenue likely comes from sponsorships (not verified).
- Channels (TrustMRR): Blog, Newsletter, Content marketing, SEO, Facebook, LinkedIn, Threads, X / Twitter, Google Ads, Email marketing, Forums, Referral program, Affiliate, Press & PR
- Founder X followers: 1,595

### Test-run takeaways (the Checker would do this tonight)
- BasinCheck: **killed.** The Revenue table shows $2.98 for 30 days. The $2,226 is a stale snapshot from an expired key.
- ECOMSTATEMENT.COM: in range ($3,304). Only 6 paid days, and three ~$1k days look like a few large customers. It would survive, but with a low paid-days score.
- DevOps Daily: in range ($3,619), but 97% came on one day. That's the "one lucky day" pattern. It would survive the filter and get flagged hard in the Final check.
