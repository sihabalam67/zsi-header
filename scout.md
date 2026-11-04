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

## 2026-11-04 test run
Source: https://trustmrr.com/api/ai/discovery → `fastestGrowingStartups` (25). All 25 .md pages opened (HTTP 200) on 2026-11-04 ~08:45 UTC. Note: the list changes during the day; Peeklens dropped out and Scalereach.ai came in since the setup check.

### Prospo (`prospo`)
- TrustMRR: https://trustmrr.com/startup/prospo · md: https://trustmrr.com/startup/prospo.md
- Site: https://prospo.io/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-03T11:53:21.982Z
- Revenue section: 24 hours $0.00 / 7 days $0.00 / 30 days $4,801 / 3 months $4,805 / 12 months $4,805 / All time $4,805
- Snapshot line: $4,801
- Daily (last 30): paid days 2/30 · biggest day $4,800.00 on 2026-10-26 = 100% of daily total
- Monthly timeline: 2026-10 $4,805
- MRR / active subscriptions: $0.00 / 0
- Pricing (founder text): Starter $29/mo, Pro $99/mo, Agency $199/mo. 7-day free trial, no card required.
- Channels (TrustMRR): SEO, LinkedIn, Instagram, X / Twitter, Product Hunt
- Founder X followers: 28

### Anonymous startup (`stealth-company-41`)
- TrustMRR: https://trustmrr.com/startup/stealth-company-41 · md: https://trustmrr.com/startup/stealth-company-41.md
- Site: none listed | stealthMode: true
- Payment provider: Stripe (API key) | last synced 2026-11-03T11:28:33.577Z
- Revenue section: 24 hours $0.00 / 7 days $0.00 / 30 days $2,004 / 3 months $2,012 / 12 months $2,012 / All time $2,012
- Snapshot line: $2,004
- Daily (last 30): paid days 2/30 · biggest day $2,000.00 on 2026-10-27 = 100% of daily total
- Monthly timeline: 2026-08 $4.00 · 2026-09 $4.00 · 2026-10 $2,004
- MRR / active subscriptions: $4.00 / 1
- Pricing (founder text): not shown
- Channels (TrustMRR): empty
- Founder X followers: 511

### Deepnia (`deepnia`)
- TrustMRR: https://trustmrr.com/startup/deepnia · md: https://trustmrr.com/startup/deepnia.md
- Site: https://deepnia.com/ | stealthMode: false
- Payment provider: Whop (API key) | last synced 2026-11-04T00:45:40.014Z
- Revenue section: 24 hours $24.00 / 7 days $254 / 30 days $691 / 3 months $693 / 12 months $693 / All time $693
- Snapshot line: $691
- Daily (last 30): paid days 14/30 · biggest day $322.00 on 2026-10-28 = 47% of daily total
- Monthly timeline: 2026-09 $2.00 · 2026-10 $580 · 2026-11 $111
- MRR / active subscriptions: $224 / 21
- Pricing (founder text): Credits: 10 credits for $3.50, 50 credits for $10.80, 100 credits for $17.00, 500 credits for $71.00; Pro and Business subscriptions available.
- Channels (TrustMRR): empty
- Founder X followers: 4,808

### Next Level Builders (`next-level-builders`)
- TrustMRR: https://trustmrr.com/startup/next-level-builders · md: https://trustmrr.com/startup/next-level-builders.md
- Site: https://nextlevelbuilder.io/ | stealthMode: false
- Payment provider: Polar (API key) | last synced 2026-11-03T20:26:50.352Z
- Revenue section: 24 hours $0.00 / 7 days $2,463 / 30 days $2,472 / 3 months $2,814 / 12 months $8,608 / All time $17,311
- Snapshot line: $2,472
- Daily (last 30): paid days 3/30 · biggest day $2,292.00 on 2026-11-01 = 93% of daily total
- Monthly timeline: 2026-08 $479 · 2026-09 $9.00 · 2026-10 $181 · 2026-11 $2,292
- MRR / active subscriptions: $758 / 28
- Pricing (founder text): Premium: $39/month billed annually at $468/year, VIP: $79/month billed annually at $948/year
- Channels (TrustMRR): empty
- Founder X followers: 3,486

### DevOps Daily (`devops-daily`)
- TrustMRR: https://trustmrr.com/startup/devops-daily · md: https://trustmrr.com/startup/devops-daily.md
- Site: https://devops-daily.com/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-03T16:23:25.482Z
- Revenue section: 24 hours $0.00 / 7 days $19.00 / 30 days $3,619 / 3 months $11,147 / 12 months $22,157 / All time $22,157
- Snapshot line: $3,619
- Daily (last 30): paid days 4/30 · biggest day $3,500.00 on 2026-10-17 = 97% of daily total
- Monthly timeline: 2026-07 $5,500 · 2026-08 $3,010 · 2026-09 $4,519 · 2026-10 $3,628
- MRR / active subscriptions: $91.00 / 5
- Pricing (founder text): Free: $0 forever
- Channels (TrustMRR): Blog, Newsletter, Content marketing, SEO, Facebook, LinkedIn, Threads, X / Twitter, Google Ads, Email marketing, Forums, Referral program, Affiliate, Press & PR
- Founder X followers: 1,595

### BasinCheck (`basincheck`)
- TrustMRR: https://trustmrr.com/startup/basincheck · md: https://trustmrr.com/startup/basincheck.md
- Site: https://basincheck.com/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-10-23T09:13:26.204Z | **Primary payment provider API credential: Stripe API key expired at 2026-10-23T15:12:56.767Z**
- Revenue section: 24 hours $0.00 / 7 days $0.00 / 30 days $2.98 / 3 months $2,643 / 12 months $5,579 / All time $5,579
- Snapshot line: $2,226 **MISMATCH** (Revenue table says $2.98; the table wins)
- Daily (last 30): paid days 1/30 · biggest day $2.98 on 2026-10-20 = 100% of daily total
- Monthly timeline: 2026-07 $405 · 2026-08 $405 · 2026-09 $2,235 · 2026-10 $2.98
- MRR / active subscriptions: $895 / 5
- Pricing (founder text): Starter: $125/mo, Standard: $250/mo, Pro: $500/mo
- Channels (TrustMRR): empty
- Founder X followers: 132

### lumabar (`lumabar`)
- TrustMRR: https://trustmrr.com/startup/lumabar · md: https://trustmrr.com/startup/lumabar.md
- Site: https://lumabar.xyz/ | stealthMode: false
- Payment provider: Polar (API key) | last synced 2026-11-04T00:23:57.530Z
- Revenue section: 24 hours $834 / 7 days $1,828 / 30 days $2,519 / 3 months $2,537 / 12 months $2,537 / All time $2,537
- Snapshot line: $2,519
- Daily (last 30): paid days 22/30 · biggest day $858.00 on 2026-11-03 = 34% of daily total
- Monthly timeline: 2026-09 $0.00 · 2026-10 $1,228 · 2026-11 $1,309
- MRR / active subscriptions: $0.00 / 0
- Pricing (founder text): $5.99 one-time (no subscription)
- Channels (TrustMRR): Reddit
- Founder X followers: 35

### bytemail (`bytemail`)
- TrustMRR: https://trustmrr.com/startup/bytemail · md: https://trustmrr.com/startup/bytemail.md
- Site: https://bytemailapp.com/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-03T12:09:27.088Z
- Revenue section: 24 hours $299 / 7 days $8,312 / 30 days $23,817 / 3 months $24,055 / 12 months $24,055 / All time $24,055
- Snapshot line: $23,817
- Daily (last 30): paid days 29/30 · biggest day $3,316.00 on 2026-10-14 = 14% of daily total
- Monthly timeline: 2026-09 $238 · 2026-10 $23,099 · 2026-11 $719
- MRR / active subscriptions: $343 / 90
- Pricing (founder text): One-time payment: $19
- Channels (TrustMRR): empty
- Founder X followers: 5,364

### Anonymous startup (`hugo-mobile-app-04`)
- TrustMRR: https://trustmrr.com/startup/hugo-mobile-app-04 · md: https://trustmrr.com/startup/hugo-mobile-app-04.md
- Site: none listed | stealthMode: true
- Payment provider: RevenueCat (API key) | last synced 2026-11-04T06:15:03.954Z
- Revenue section: 24 hours $0.01 / 7 days $5.88 / 30 days $10.14 / 3 months $20.58 / 12 months $36.56 / All time $36.56
- Snapshot line: $10.14
- Daily (last 30): paid days 30/30 · biggest day $5.15 on 2026-10-29 = 51% of daily total
- Monthly timeline: 2026-08 $10.33 · 2026-09 $0.02 · 2026-10 $9.70 · 2026-11 $0.53
- MRR / active subscriptions: $0.00 / 0
- Pricing (founder text): not shown
- Channels (TrustMRR): empty
- Founder X followers: 597

### Qoest (`qoest`)
- TrustMRR: https://trustmrr.com/startup/qoest · md: https://trustmrr.com/startup/qoest.md
- Site: https://qoest.lemonsqueezy.com/ | stealthMode: false
- Payment provider: Lemon Squeezy (API key) | last synced 2026-03-19T21:12:53.542Z | **Primary payment provider API credential: Lemon Squeezy API key expired; expiration time unavailable**
- Revenue section: 24 hours $0.00 / 7 days $0.00 / 30 days $771 / 3 months $0.00 / 12 months $1,710 / All time $3,520
- Snapshot line: $771 **STALE:** last synced 2026-03-19 and the key has expired, so this 30-day figure is from March, not now
- Daily (last 30): paid days 0/30
- Monthly timeline: 2025-12 $309 · 2026-01 $321 · 2026-02 $337 · 2026-03 $434
- MRR / active subscriptions: $4,274 / 20
- Pricing (founder text): $1.00 - $1,499.00
- Channels (TrustMRR): empty
- Founder X followers: 395

### Workel (`workel`)
- TrustMRR: https://trustmrr.com/startup/workel · md: https://trustmrr.com/startup/workel.md
- Site: https://workel.com/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-03T23:49:17.347Z
- Revenue section: 24 hours $0.00 / 7 days $99.00 / 30 days $99.00 / 3 months $110 / 12 months $232 / All time $242
- Snapshot line: $99.00
- Daily (last 30): paid days 1/30 · biggest day $99.00 on 2026-10-30 = 100% of daily total
- Monthly timeline: 2026-07 $18.00 · 2026-08 $26.00 · 2026-09 $1.20 · 2026-10 $99.00
- MRR / active subscriptions: $10.00 / 1
- Pricing (founder text): Free plan for an unlimited time
- Channels (TrustMRR): empty
- Founder X followers: 65

### Intentsly (`intentsly`)
- TrustMRR: https://trustmrr.com/startup/intentsly · md: https://trustmrr.com/startup/intentsly.md
- Site: https://intentsly.com/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-03T15:53:22.906Z
- Revenue section: 24 hours $0.00 / 7 days $0.00 / 30 days $7,388 / 3 months $7,582 / 12 months $7,936 / All time $11,091
- Snapshot line: $7,388
- Daily (last 30): paid days 2/30 · biggest day $7,291.00 on 2026-10-19 = 99% of daily total
- Monthly timeline: 2026-07 $97.00 · 2026-08 $97.00 · 2026-09 $97.00 · 2026-10 $7,388
- MRR / active subscriptions: $0.00 / 0
- Pricing (founder text): $97/mo
- Channels (TrustMRR): empty
- Founder X followers: 2,166

### CossyVita (`cossyvita`)
- TrustMRR: https://trustmrr.com/startup/cossyvita · md: https://trustmrr.com/startup/cossyvita.md
- Site: https://www.cossyvita.com/en | stealthMode: false
- Payment provider: RevenueCat (API key) | last synced 2026-11-04T00:36:53.582Z
- Revenue section: 24 hours $1.60 / 7 days $6.21 / 30 days $80.93 / 3 months $82.16 / 12 months $82.16 / All time $82.16
- Snapshot line: $80.93
- Daily (last 30): paid days 16/30 · biggest day $29.25 on 2026-10-19 = 36% of daily total
- Monthly timeline: 2026-08 $0.00 · 2026-09 $1.23 · 2026-10 $76.33 · 2026-11 $4.60
- MRR / active subscriptions: $32.54 / 24
- Pricing (founder text): Freemium model with limited free product analyses. Premium monthly and annual subscriptions unlock advanced features and higher analysis limits. One-t
- Channels (TrustMRR): Instagram, TikTok, Google Ads
- Founder X followers: 0

### Printotr Aı (`printotr-a`)
- TrustMRR: https://trustmrr.com/startup/printotr-a · md: https://trustmrr.com/startup/printotr-a.md
- Site: https://printotr.com.tr/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-03T16:01:10.665Z
- Revenue section: 24 hours $0.00 / 7 days $1,015 / 30 days $1,183 / 3 months $1,357 / 12 months $5,784 / All time $9,311
- Snapshot line: $1,183
- Daily (last 30): paid days 5/30 · biggest day $800.00 on 2026-10-29 = 68% of daily total
- Monthly timeline: 2026-08 $156 · 2026-09 $17.99 · 2026-10 $1,033 · 2026-11 $150
- MRR / active subscriptions: $150 / 1
- Pricing (founder text): Starter: $17.99, Pro: $39.99, Studio: $79.99 (one-time payment)
- Channels (TrustMRR): empty
- Founder X followers: 0

### Anonymous startup (`anonymous-startup-80`)
- TrustMRR: https://trustmrr.com/startup/anonymous-startup-80 · md: https://trustmrr.com/startup/anonymous-startup-80.md
- Site: none listed | stealthMode: true
- Payment provider: Superwall (API key) | last synced 2026-11-04T00:56:02.607Z
- Revenue section: 24 hours $1.57 / 7 days $208 / 30 days $637 / 3 months $648 / 12 months $648 / All time $648
- Snapshot line: $637
- Daily (last 30): paid days 28/30 · biggest day $54.83 on 2026-10-19 = 9% of daily total
- Monthly timeline: 2026-08 $0.00 · 2026-09 $10.11 · 2026-10 $556 · 2026-11 $81.29
- MRR / active subscriptions: $516 / 408
- Pricing (founder text): not shown
- Channels (TrustMRR): empty
- Founder X followers: 0

### Bidder iQ (`bidder-iq`)
- TrustMRR: https://trustmrr.com/startup/bidder-iq · md: https://trustmrr.com/startup/bidder-iq.md
- Site: https://bidderiq.com/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-03T14:15:03.271Z
- Revenue section: 24 hours $0.00 / 7 days $0.00 / 30 days $2,052 / 3 months $2,221 / 12 months $8,840 / All time $13,748
- Snapshot line: $2,052
- Daily (last 30): paid days 9/30 · biggest day $876.00 on 2026-10-10 = 43% of daily total
- Monthly timeline: 2026-07 $618 · 2026-08 $132 · 2026-09 $37.00 · 2026-10 $2,052
- MRR / active subscriptions: $0.00 / 0
- Pricing (founder text): $396/year
- Channels (TrustMRR): empty
- Founder X followers: 285

### Skillmaxing (`skillmaxing`)
- TrustMRR: https://trustmrr.com/startup/skillmaxing · md: https://trustmrr.com/startup/skillmaxing.md
- Site: https://skillmaxing.in/ | stealthMode: false
- Payment provider: Dodo Payments (API key) | last synced 2026-10-17T06:21:07.762Z | **Primary payment provider API credential: Dodo Payments API key expired at 2026-10-17T12:20:41.641Z**
- Revenue section: 24 hours $0.00 / 7 days $0.00 / 30 days $456 / 3 months $465 / 12 months $465 / All time $465
- Snapshot line: $456
- Daily (last 30): paid days 0/30
- Monthly timeline: 2026-09 $465
- MRR / active subscriptions: $15.64 / 3
- Pricing (founder text): not shown
- Channels (TrustMRR): empty
- Founder X followers: 56

### Kiiwi (`kiiwi`)
- TrustMRR: https://trustmrr.com/startup/kiiwi · md: https://trustmrr.com/startup/kiiwi.md
- Site: https://kiiwi.app/ | stealthMode: false
- Payment provider: Dodo Payments (API key) | last synced 2026-11-03T18:15:09.686Z
- Revenue section: 24 hours $0.00 / 7 days $34.45 / 30 days $504 / 3 months $513 / 12 months $513 / All time $513
- Snapshot line: $504
- Daily (last 30): paid days 19/30 · biggest day $153.00 on 2026-10-08 = 30% of daily total
- Monthly timeline: 2026-09 $5.62 · 2026-10 $500 · 2026-11 $8.14
- MRR / active subscriptions: $0.00 / 0
- Pricing (founder text): $4.99 one-time, 2 Macs, 14-day money-back guarantee, lifetime updates
- Channels (TrustMRR): X / Twitter, Threads
- Founder X followers: 407

### ECOMSTATEMENT.COM (`ecomstatement-com`)
- TrustMRR: https://trustmrr.com/startup/ecomstatement-com · md: https://trustmrr.com/startup/ecomstatement-com.md
- Site: https://ecomstatement.com/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-03T14:58:00.852Z
- Revenue section: 24 hours $0.00 / 7 days $1,112 / 30 days $3,304 / 3 months $3,432 / 12 months $3,883 / All time $3,883
- Snapshot line: $3,304
- Daily (last 30): paid days 6/30 · biggest day $1,120.00 on 2026-10-24 = 34% of daily total
- Monthly timeline: 2026-07 $64.38 · 2026-08 $64.38 · 2026-09 $64.38 · 2026-10 $3,304
- MRR / active subscriptions: $1,149 / 2
- Pricing (founder text): Free trial, Small: $29/month, Starter: $49/month, Unlimited: $99/month, with yearly options available.
- Channels (TrustMRR): empty
- Founder X followers: 175

### 2FA Authenticator (`2fa-authenticator`)
- TrustMRR: https://trustmrr.com/startup/2fa-authenticator · md: https://trustmrr.com/startup/2fa-authenticator.md
- Site: https://www.authenticator.sh/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-04T00:28:06.685Z
- Revenue section: 24 hours $24.99 / 7 days $64.86 / 30 days $299 / 3 months $305 / 12 months $305 / All time $305
- Snapshot line: $299
- Daily (last 30): paid days 11/30 · biggest day $88.00 on 2026-10-12 = 29% of daily total
- Monthly timeline: 2026-10 $280 · 2026-11 $24.99
- MRR / active subscriptions: $6.66 / 7
- Pricing (founder text): Free to install. Paid cloud backup.
- Channels (TrustMRR): SEO, YouTube, TikTok, Product Hunt
- Founder X followers: 0

### VinoVeo (`vinoveo`)
- TrustMRR: https://trustmrr.com/startup/vinoveo · md: https://trustmrr.com/startup/vinoveo.md
- Site: https://vinoveo.com/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-04T02:25:17.511Z
- Revenue section: 24 hours $0.00 / 7 days $0.00 / 30 days $67.91 / 3 months $141 / 12 months $1,158 / All time $2,062
- Snapshot line: $67.91
- Daily (last 30): paid days 1/30 · biggest day $67.91 on 2026-10-21 = 100% of daily total
- Monthly timeline: 2026-07 $1.38 · 2026-08 $130 · 2026-09 $1.41 · 2026-10 $67.91
- MRR / active subscriptions: $79.62 / 17
- Pricing (founder text): 50€ annual subscription
- Channels (TrustMRR): empty
- Founder X followers: 1

### WRTune for OpenWRT (`wrtune-for-openwrt`)
- TrustMRR: https://trustmrr.com/startup/wrtune-for-openwrt · md: https://trustmrr.com/startup/wrtune-for-openwrt.md
- Site: https://apps.apple.com/app/id6758356103 | stealthMode: false
- Payment provider: RevenueCat (API key) | last synced 2026-11-03T21:23:46.282Z
- Revenue section: 24 hours $0.00 / 7 days $19.30 / 30 days $19.30 / 3 months $74.16 / 12 months $860 / All time $860
- Snapshot line: $19.30
- Daily (last 30): paid days 1/30 · biggest day $19.30 on 2026-11-02 = 100% of daily total
- Monthly timeline: 2026-08 $19.46 · 2026-09 $35.40 · 2026-10 $0.00 · 2026-11 $19.30
- MRR / active subscriptions: $6.49 / 4
- Pricing (founder text): Free · In‑App Purchases
- Channels (TrustMRR): empty
- Founder X followers: 19

### FormBeep (`formbeep`)
- TrustMRR: https://trustmrr.com/startup/formbeep · md: https://trustmrr.com/startup/formbeep.md
- Site: https://formbeep.com/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-04T00:29:38.373Z
- Revenue section: 24 hours $0.00 / 7 days $0.00 / 30 days $38.00 / 3 months $38.90 / 12 months $38.90 / All time $38.90
- Snapshot line: $38.00
- Daily (last 30): paid days 2/30 · biggest day $29.00 on 2026-10-07 = 76% of daily total
- Monthly timeline: 2026-09 $0.90 · 2026-10 $38.00
- MRR / active subscriptions: $38.00 / 2
- Pricing (founder text): Free: $0, Starter: $9/month, Pro: $29/month, Agency: $79/month
- Channels (TrustMRR): Blog, Content marketing, SEO, X / Twitter
- Founder X followers: 450

### slidelabs.net (`slidelabs-net`)
- TrustMRR: https://trustmrr.com/startup/slidelabs-net · md: https://trustmrr.com/startup/slidelabs-net.md
- Site: https://slidelabs.net/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-03T22:48:10.688Z
- Revenue section: 24 hours $0.00 / 7 days $250 / 30 days $250 / 3 months $376 / 12 months $459 / All time $459
- Snapshot line: $250
- Daily (last 30): paid days 1/30 · biggest day $250.00 on 2026-10-28 = 100% of daily total
- Monthly timeline: 2026-07 $65.00 · 2026-08 $12.00 · 2026-09 $114 · 2026-10 $250
- MRR / active subscriptions: $0.00 / 0
- Pricing (founder text): Free: $0, Basic: $6 one-time, Pro: $29 one-time, Max: $108 one-time
- Channels (TrustMRR): Facebook, Threads, TikTok, TikTok Ads
- Founder X followers: 503

### Scalereach.ai (`scalereach`)
- TrustMRR: https://trustmrr.com/startup/scalereach · md: https://trustmrr.com/startup/scalereach.md
- Site: http://scalereach.ai/ | stealthMode: false
- Payment provider: Dodo Payments (API key) | last synced 2026-11-04T06:54:57.382Z
- Revenue section: 24 hours $392 / 7 days $1,337 / 30 days $1,837 / 3 months $1,896 / 12 months $2,050 / All time $2,050
- Snapshot line: $1,837
- Daily (last 30): paid days 17/30 · biggest day $438.00 on 2026-11-03 = 24% of daily total
- Monthly timeline: 2026-08 $12.00 · 2026-09 $14.69 · 2026-10 $847 · 2026-11 $1,022
- MRR / active subscriptions: $1,558 / 91
- Pricing (founder text): Pro $18/mo or $12.50/mo annual (400 min/mo), Agency $99/mo or $49/mo annual (5,000 min/mo)
- Channels (TrustMRR): Instagram, Reddit, TikTok
- Founder X followers: 0

