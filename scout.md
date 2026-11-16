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

### Checker notes 2026-11-04 (TEST)
Re-opened all 9 in-range .md pages around 09:00 UTC; every 30-day figure matched the Revenue table. All 9 sites opened (HTTP 200).
**Killed:**
- 3 Anonymous startups (stealth-company-41, hugo-mobile-app-04, anonymous-startup-80).
- bytemail: $23,817 is over the $20k cap.
- BasinCheck: $2.98 in the Revenue table; the $2,226 snapshot is stale because the key expired.
- Qoest: $771, and stale since March because the key expired.
- 10 others under $1k: Deepnia, Workel, CossyVita, Skillmaxing, Kiiwi, 2FA Authenticator, VinoVeo, WRTune, FormBeep, slidelabs.

**Scores** (paid days / growth / fit with code+design+content / demand / sell alone):
- lumabar 5/3/5/3/5 = **21**. 22 paid days; $1,228 in Oct, then $1,309 in the first 3 days of Nov. A desktop app I could build. $5.99 one-time, sold through Reddit.
- Scalereach.ai 4/4/3/4/4 = **19**. 17 paid days; $847 in Oct, then $1,022 in Nov. 91 subscriptions. Video infrastructure is heavy, and the category is crowded.
- DevOps Daily 1/4/4/3/2 = 14. Steady $3–5.5k a month since May, but it arrives in single big payments (sponsorship-shaped), and that needs sales.
- Bidder iQ 2/2/3/3/4 = 14. Lumpy months; needs auction data.
- Printotr Aı 2/1/4/3/4 = 14. 68% came on one day ($800).
- Prospo 1/1/4/3/3 = 12. $4,800 came on one day (100%), likely one deal.
- ECOMSTATEMENT 2/1/3/2/3 = 11. Flat $64 a month, then three ~$1k days.
- Intentsly 1/1/3/3/2 = 10. $7,291 on one day (99%), after months at $97.
- Next Level Builders 1/1/2/3/2 = 9. 93% on one day; depends on the founder's 3.5k-follower audience.

**WHY THIS COULD FAIL**
- **lumabar:** only 2 months old. Nov 3 alone was $858 (about 140 sales), probably one Reddit post going viral, and that may not repeat. The current price is a 63%-off launch price. Free rivals exist (TaskbarX, Seelen UI), and Microsoft could ship the features itself.
- **Scalereach.ai:** competes with big, well-funded tools like Opus Clip. Video processing costs eat the margin. GetApp and Capterra show 0 real user reviews, so the demand evidence is the category's, not this product's.

## 2026-11-05 run
Source: https://trustmrr.com/api/ai/discovery → `fastestGrowingStartups` (25). All 25 .md pages opened (HTTP 200) on 2026-11-05 ~01:00 ET. New since yesterday's test run: 1418-technologies-llc, cliputils, inxanity-labs, peeklens, vedicastrolab. Gone since then: cossyvita, formbeep, scalereach, slidelabs-net, wrtune-for-openwrt.

### Prospo (`prospo`)
- TrustMRR: https://trustmrr.com/startup/prospo · md: https://trustmrr.com/startup/prospo.md
- Site: https://prospo.io/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-04T11:52:57.125Z
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
- Payment provider: Stripe (API key) | last synced 2026-11-05T05:21:23.437Z
- Revenue section: 24 hours $0.00 / 7 days $0.00 / 30 days $2,004 / 3 months $2,012 / 12 months $2,012 / All time $2,012
- Snapshot line: $2,004
- Daily (last 30): paid days 2/30 · biggest day $2,000.00 on 2026-10-27 = 100% of daily total
- Monthly timeline: 2026-08 $4.00 · 2026-09 $4.00 · 2026-10 $2,004
- MRR / active subscriptions: $4.00 / 1
- Pricing (founder text): not shown
- Channels (TrustMRR): empty
- Founder X followers: 511

### ClipUtils (`cliputils`)
- TrustMRR: https://trustmrr.com/startup/cliputils · md: https://trustmrr.com/startup/cliputils.md
- Site: https://cliputils.com/ | stealthMode: false
- Payment provider: Dodo Payments (API key) | last synced 2026-11-05T00:44:35.618Z
- Revenue section: 24 hours $2.09 / 7 days $135 / 30 days $409 / 3 months $410 / 12 months $410 / All time $410
- Snapshot line: $409
- Daily (last 30): paid days 26/30 · biggest day $98.89 on 2026-10-21 = 24% of daily total
- Monthly timeline: 2026-10 $394 · 2026-11 $15.71
- MRR / active subscriptions: $333 / 29
- Pricing (founder text): Freemium business model. Free online tools with opportunities for monetization through premium subscriptions, sponsored placements and advertising.
- Channels (TrustMRR): SEO, Content marketing
- Founder X followers: 7,801

### Deepnia (`deepnia`)
- TrustMRR: https://trustmrr.com/startup/deepnia · md: https://trustmrr.com/startup/deepnia.md
- Site: https://deepnia.com/ | stealthMode: false
- Payment provider: Whop (API key) | last synced 2026-11-05T00:35:59.885Z
- Revenue section: 24 hours $34.00 / 7 days $253 / 30 days $725 / 3 months $727 / 12 months $727 / All time $727
- Snapshot line: $725
- Daily (last 30): paid days 15/30 · biggest day $322.00 on 2026-10-28 = 44% of daily total
- Monthly timeline: 2026-09 $2.00 · 2026-10 $580 · 2026-11 $145
- MRR / active subscriptions: $259 / 25
- Pricing (founder text): Credits: 10 credits for $3.50, 50 credits for $10.80, 100 credits for $17.00, 500 credits for $71.00; Pro and Business subscriptions available.
- Channels (TrustMRR): empty
- Founder X followers: 4,808

### Next Level Builders (`next-level-builders`)
- TrustMRR: https://trustmrr.com/startup/next-level-builders · md: https://trustmrr.com/startup/next-level-builders.md
- Site: https://nextlevelbuilder.io/ | stealthMode: false
- Payment provider: Polar (API key) | last synced 2026-11-05T02:26:01.711Z
- Revenue section: 24 hours $257 / 7 days $2,721 / 30 days $2,730 / 3 months $3,071 / 12 months $8,637 / All time $17,568
- Snapshot line: $2,730
- Daily (last 30): paid days 4/30 · biggest day $2,292.00 on 2026-11-01 = 84% of daily total
- Monthly timeline: 2026-08 $479 · 2026-09 $9.00 · 2026-10 $181 · 2026-11 $2,549
- MRR / active subscriptions: $728 / 28
- Pricing (founder text): Premium: $39/month billed annually at $468/year, VIP: $79/month billed annually at $948/year
- Channels (TrustMRR): empty
- Founder X followers: 3,485

### DevOps Daily (`devops-daily`)
- TrustMRR: https://trustmrr.com/startup/devops-daily · md: https://trustmrr.com/startup/devops-daily.md
- Site: https://devops-daily.com/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-04T22:18:43.588Z
- Revenue section: 24 hours $0.00 / 7 days $9.50 / 30 days $3,628 / 3 months $11,157 / 12 months $22,166 / All time $22,166
- Snapshot line: $3,628
- Daily (last 30): paid days 5/30 · biggest day $3,500.00 on 2026-10-17 = 96% of daily total
- Monthly timeline: 2026-08 $3,010 · 2026-09 $4,519 · 2026-10 $3,628 · 2026-11 $9.50
- MRR / active subscriptions: $91.00 / 5
- Pricing (founder text): Free: $0 forever
- Channels (TrustMRR): Blog, Newsletter, Content marketing, SEO, Facebook, LinkedIn, Threads, X / Twitter, Google Ads, Email marketing, Forums, Referral program, Affiliate, Press & PR
- Founder X followers: 1,596

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
- Founder X followers: 134

### lumabar (`lumabar`)
- TrustMRR: https://trustmrr.com/startup/lumabar · md: https://trustmrr.com/startup/lumabar.md
- Site: https://lumabar.xyz/ | stealthMode: false
- Payment provider: Polar (API key) | last synced 2026-11-05T00:14:58.729Z
- Revenue section: 24 hours $281 / 7 days $1,993 / 30 days $2,806 / 3 months $2,824 / 12 months $2,824 / All time $2,824
- Snapshot line: $2,806
- Daily (last 30): paid days 22/30 · biggest day $858.00 on 2026-11-03 = 31% of daily total
- Monthly timeline: 2026-09 $0.00 · 2026-10 $1,228 · 2026-11 $1,596
- MRR / active subscriptions: $0.00 / 0
- Pricing (founder text): $5.99 one-time (no subscription)
- Channels (TrustMRR): Reddit
- Founder X followers: 37

### bytemail (`bytemail`)
- TrustMRR: https://trustmrr.com/startup/bytemail · md: https://trustmrr.com/startup/bytemail.md
- Site: https://bytemailapp.com/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-05T00:00:57.820Z
- Revenue section: 24 hours $576 / 7 days $7,186 / 30 days $24,595 / 3 months $24,833 / 12 months $24,833 / All time $24,833
- Snapshot line: $24,595
- Daily (last 30): paid days 29/30 · biggest day $3,316.00 on 2026-10-14 = 14% of daily total
- Monthly timeline: 2026-09 $238 · 2026-10 $23,099 · 2026-11 $1,496
- MRR / active subscriptions: $415 / 109
- Pricing (founder text): One-time payment: $19
- Channels (TrustMRR): empty
- Founder X followers: 5,369

### Peeklens (`peeklens`)
- TrustMRR: https://trustmrr.com/startup/peeklens · md: https://trustmrr.com/startup/peeklens.md
- Site: https://www.medcytes.com/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-04T22:41:46.966Z
- Revenue section: 24 hours $7,500 / 7 days $12,500 / 30 days $12,500 / 3 months $12,629 / 12 months $15,154 / All time $15,154
- Snapshot line: $12,500
- Daily (last 30): paid days 2/30 · biggest day $7,500.00 on 2026-11-04 = 60% of daily total
- Monthly timeline: 2026-06 $2,525 · 2026-09 $129 · 2026-10 $5,000 · 2026-11 $7,500
- MRR / active subscriptions: $0.00 / 0
- Pricing (founder text): not shown
- Channels (TrustMRR): empty
- Founder X followers: 0

### Qoest (`qoest`)
- TrustMRR: https://trustmrr.com/startup/qoest · md: https://trustmrr.com/startup/qoest.md
- Site: https://qoest.lemonsqueezy.com/ | stealthMode: false
- Payment provider: Lemon Squeezy (API key) | last synced 2026-03-19T21:12:53.542Z | **Primary payment provider API credential: Lemon Squeezy API key expired; expiration time unavailable**
- Revenue section: 24 hours $0.00 / 7 days $0.00 / 30 days $771 / 3 months $0.00 / 12 months $1,710 / All time $3,520
- Snapshot line: $771 **STALE:** last synced 2026-03-19 and the key has expired, so this figure is from March
- Daily (last 30): paid days 0/30
- Monthly timeline: 2025-12 $309 · 2026-01 $321 · 2026-02 $337 · 2026-03 $434
- MRR / active subscriptions: $4,274 / 20
- Pricing (founder text): $1.00 - $1,499.00
- Channels (TrustMRR): empty
- Founder X followers: 395

### Vedic Astro Lab (`vedicastrolab`)
- TrustMRR: https://trustmrr.com/startup/vedicastrolab · md: https://trustmrr.com/startup/vedicastrolab.md
- Site: https://vedicastrolab.com/ | stealthMode: false
- Payment provider: razorpay (API key) | last synced 2026-11-05T00:47:35.698Z
- Revenue section: 24 hours $0.89 / 7 days $25.83 / 30 days $174 / 3 months $176 / 12 months $176 / All time $176
- Snapshot line: $174
- Daily (last 30): paid days 28/30 · biggest day $62.30 on 2026-10-20 = 36% of daily total
- Monthly timeline: 2026-10 $159 · 2026-11 $16.68
- MRR / active subscriptions: $0.00 / 0
- Pricing (founder text): 60 seconds of free chat daily; pay-as-you-go minutes after that with no subscription or auto-renewal. Purchased minutes never expire; voice calls are paid.
- Channels (TrustMRR): SEO
- Founder X followers: 0

### Workel (`workel`)
- TrustMRR: https://trustmrr.com/startup/workel · md: https://trustmrr.com/startup/workel.md
- Site: https://workel.com/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-04T23:41:56.209Z
- Revenue section: 24 hours $0.00 / 7 days $99.00 / 30 days $99.00 / 3 months $110 / 12 months $222 / All time $242
- Snapshot line: $99.00
- Daily (last 30): paid days 1/30 · biggest day $99.00 on 2026-10-30 = 100% of daily total
- Monthly timeline: 2026-07 $18.00 · 2026-08 $26.00 · 2026-09 $1.20 · 2026-10 $99.00
- MRR / active subscriptions: $10.00 / 1
- Pricing (founder text): Free plan for an unlimited time
- Channels (TrustMRR): empty
- Founder X followers: 65

### Anonymous startup (`hugo-mobile-app-04`)
- TrustMRR: https://trustmrr.com/startup/hugo-mobile-app-04 · md: https://trustmrr.com/startup/hugo-mobile-app-04.md
- Site: none listed | stealthMode: true
- Payment provider: RevenueCat (API key) | last synced 2026-11-05T00:06:30.759Z
- Revenue section: 24 hours $0.00 / 7 days $0.74 / 30 days $10.13 / 3 months $20.59 / 12 months $36.57 / All time $36.57
- Snapshot line: $10.13
- Daily (last 30): paid days 29/30 · biggest day $5.15 on 2026-10-29 = 51% of daily total
- Monthly timeline: 2026-08 $10.33 · 2026-09 $0.02 · 2026-10 $9.70 · 2026-11 $0.54
- MRR / active subscriptions: $0.00 / 0
- Pricing (founder text): not shown
- Channels (TrustMRR): empty
- Founder X followers: 597

### Intentsly (`intentsly`)
- TrustMRR: https://trustmrr.com/startup/intentsly · md: https://trustmrr.com/startup/intentsly.md
- Site: https://intentsly.com/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-04T21:49:43.541Z
- Revenue section: 24 hours $0.00 / 7 days $0.00 / 30 days $7,388 / 3 months $7,582 / 12 months $7,936 / All time $11,091
- Snapshot line: $7,388
- Daily (last 30): paid days 2/30 · biggest day $7,291.00 on 2026-10-19 = 99% of daily total
- Monthly timeline: 2026-07 $97.00 · 2026-08 $97.00 · 2026-09 $97.00 · 2026-10 $7,388
- MRR / active subscriptions: $0.00 / 0
- Pricing (founder text): $97/mo
- Channels (TrustMRR): empty
- Founder X followers: 2,169

### INXANITY Labs — Browser Gaming & AI Modding Platform (`inxanity-labs`)
- TrustMRR: https://trustmrr.com/startup/inxanity-labs · md: https://trustmrr.com/startup/inxanity-labs.md
- Site: https://inxanitylabs.com/ | stealthMode: false
- Payment provider: Whop (API key) | last synced 2026-11-05T00:34:33.318Z
- Revenue section: 24 hours $0.00 / 7 days $143 / 30 days $1,450 / 3 months $1,470 / 12 months $1,470 / All time $1,470
- Snapshot line: $1,450
- Daily (last 30): paid days 17/30 · biggest day $286.00 on 2026-10-09 = 20% of daily total
- Monthly timeline: 2026-10 $1,367 · 2026-11 $103
- MRR / active subscriptions: $973 / 48
- Pricing (founder text): Games: free, ad-supported. Launcher + Discord community: $19.99/mo, cancel anytime. Not yet built: mobile ads, sponsored placements, ad optimization.
- Channels (TrustMRR): TikTok, X / Twitter, Instagram, SEO
- Founder X followers: 710

### Printotr Aı (`printotr-a`)
- TrustMRR: https://trustmrr.com/startup/printotr-a · md: https://trustmrr.com/startup/printotr-a.md
- Site: https://printotr.com.tr/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-04T21:57:12.750Z
- Revenue section: 24 hours $0.00 / 7 days $1,015 / 30 days $1,183 / 3 months $1,357 / 12 months $5,784 / All time $9,311
- Snapshot line: $1,183
- Daily (last 30): paid days 5/30 · biggest day $800.00 on 2026-10-29 = 68% of daily total
- Monthly timeline: 2026-08 $156 · 2026-09 $17.99 · 2026-10 $1,033 · 2026-11 $150
- MRR / active subscriptions: $150 / 1
- Pricing (founder text): Starter: $17.99, Pro: $39.99, Studio: $79.99 (one-time payment)
- Channels (TrustMRR): empty
- Founder X followers: 0

### Bidder iQ (`bidder-iq`)
- TrustMRR: https://trustmrr.com/startup/bidder-iq · md: https://trustmrr.com/startup/bidder-iq.md
- Site: https://bidderiq.com/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-04T20:14:30.356Z
- Revenue section: 24 hours $0.00 / 7 days $0.00 / 30 days $2,040 / 3 months $2,209 / 12 months $8,840 / All time $13,748
- Snapshot line: $2,040
- Daily (last 30): paid days 8/30 · biggest day $876.00 on 2026-10-10 = 43% of daily total
- Monthly timeline: 2026-07 $618 · 2026-08 $132 · 2026-09 $37.00 · 2026-10 $2,052
- MRR / active subscriptions: $0.00 / 0
- Pricing (founder text): $396/year
- Channels (TrustMRR): empty
- Founder X followers: 285

### 1418 Technologies LLC (`1418-technologies-llc`)
- TrustMRR: https://trustmrr.com/startup/1418-technologies-llc · md: https://trustmrr.com/startup/1418-technologies-llc.md
- Site: https://1418tech.com/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-04T22:32:50.323Z
- Revenue section: 24 hours $1,500 / 7 days $1,500 / 30 days $3,533 / 3 months $5,659 / 12 months $18,272 / All time $22,517
- Snapshot line: $3,563
- Daily (last 30): paid days 3/30 · biggest day $2,000.00 on 2026-10-10 = 57% of daily total
- Monthly timeline: 2026-08 $2,063 · 2026-09 $2,063 · 2026-10 $2,063 · 2026-11 $1,500
- MRR / active subscriptions: $63.00 / 2
- Pricing (founder text): not shown
- Channels (TrustMRR): empty
- Founder X followers: 11

### Anonymous startup (`anonymous-startup-80`)
- TrustMRR: https://trustmrr.com/startup/anonymous-startup-80 · md: https://trustmrr.com/startup/anonymous-startup-80.md
- Site: none listed | stealthMode: true
- Payment provider: Superwall (API key) | last synced 2026-11-05T00:46:03.589Z
- Revenue section: 24 hours $0.00 / 7 days $193 / 30 days $665 / 3 months $678 / 12 months $678 / All time $678
- Snapshot line: $665
- Daily (last 30): paid days 27/30 · biggest day $54.83 on 2026-10-19 = 8% of daily total
- Monthly timeline: 2026-08 $0.00 · 2026-09 $10.11 · 2026-10 $556 · 2026-11 $112
- MRR / active subscriptions: $525 / 416
- Pricing (founder text): not shown
- Channels (TrustMRR): empty
- Founder X followers: 0

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
- Payment provider: Dodo Payments (API key) | last synced 2026-11-05T00:06:29.268Z
- Revenue section: 24 hours $6.99 / 7 days $41.44 / 30 days $511 / 3 months $520 / 12 months $520 / All time $520
- Snapshot line: $511
- Daily (last 30): paid days 19/30 · biggest day $153.00 on 2026-10-08 = 30% of daily total
- Monthly timeline: 2026-09 $5.62 · 2026-10 $500 · 2026-11 $15.13
- MRR / active subscriptions: $0.00 / 0
- Pricing (founder text): $4.99 one-time, 2 Macs, 14-day money-back guarantee, lifetime updates
- Channels (TrustMRR): X / Twitter, Threads
- Founder X followers: 409

### ECOMSTATEMENT.COM (`ecomstatement-com`)
- TrustMRR: https://trustmrr.com/startup/ecomstatement-com · md: https://trustmrr.com/startup/ecomstatement-com.md
- Site: https://ecomstatement.com/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-05T02:56:06.019Z
- Revenue section: 24 hours $0.00 / 7 days $0.00 / 30 days $3,304 / 3 months $3,432 / 12 months $3,883 / All time $3,883
- Snapshot line: $3,304
- Daily (last 30): paid days 6/30 · biggest day $1,120.00 on 2026-10-24 = 34% of daily total
- Monthly timeline: 2026-07 $64.38 · 2026-08 $64.38 · 2026-09 $64.38 · 2026-10 $3,304
- MRR / active subscriptions: $1,155 / 2
- Pricing (founder text): Free trial, Small: $29/month, Starter: $49/month, Unlimited: $99/month, with yearly options available.
- Channels (TrustMRR): empty
- Founder X followers: 175

### 2FA Authenticator (`2fa-authenticator`)
- TrustMRR: https://trustmrr.com/startup/2fa-authenticator · md: https://trustmrr.com/startup/2fa-authenticator.md
- Site: https://www.authenticator.sh/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-05T00:19:00.341Z
- Revenue section: 24 hours $0.00 / 7 days $39.87 / 30 days $299 / 3 months $305 / 12 months $305 / All time $305
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
- Payment provider: Stripe (API key) | last synced 2026-11-05T02:24:32.949Z
- Revenue section: 24 hours $0.00 / 7 days $0.00 / 30 days $67.91 / 3 months $141 / 12 months $1,158 / All time $2,062
- Snapshot line: $67.91
- Daily (last 30): paid days 1/30 · biggest day $67.91 on 2026-10-21 = 100% of daily total
- Monthly timeline: 2026-07 $1.38 · 2026-08 $130 · 2026-09 $1.41 · 2026-10 $67.91
- MRR / active subscriptions: $79.73 / 17
- Pricing (founder text): 50€ annual subscription
- Channels (TrustMRR): empty
- Founder X followers: 1



### Checker notes 2026-11-05
Re-opened all 11 in-range .md pages around 03:00 ET; every 30-day figure matched the Scout run, and all 11 sites opened (HTTP 200).
**Killed (14):**
- 3 Anonymous startups (stealth-company-41, hugo-mobile-app-04, anonymous-startup-80).
- bytemail: $24,595 is over the $20k cap.
- BasinCheck ($2.98), Qoest ($771, stale since March) and Skillmaxing ($456): expired payment keys, and out of range anyway.
- Under $1k: ClipUtils ($409), Deepnia ($725), Vedic Astro Lab ($174), Workel ($99), Kiiwi ($511), 2FA Authenticator ($299), VinoVeo ($68).
- Watch list: ClipUtils (26/30 paid days) and Vedic Astro Lab (28/30) are paid almost daily but are still small. If they cross $1k, they're strong candidates.

**Scores** (paid days / growth / fit with code+design+content / demand / sell alone):
- lumabar 5/4/5/3/5 = **22 STEAL-READY**. Up from 21: November is already $1,596 after 4 days, more than all of October ($1,228).
- INXANITY Labs 4/2/2/3/3 = 14. 17 paid days, but daily sales fell from $200–286 (Oct 9–11) to about $20 a day since mid-October. The founder's "~$150/day in ads" claim is not checked revenue and isn't counted.
- DevOps Daily 1/4/4/3/2 = 14. Unchanged. 96% came on one day (sponsorship-shaped).
- Bidder iQ 2/2/3/3/4 = 14. 8 paid days now.
- Printotr Aı 2/1/4/3/4 = 14. 68% came on one $800 day.
- Prospo 1/1/4/3/3 = 12. One $4,800 payment.
- ECOMSTATEMENT 2/1/3/2/3 = 11.
- Intentsly 1/1/3/3/2 = 10. One $7,291 payment. A web listing claims "$203k MRR", which contradicts the Revenue table and is ignored.
- Next Level Builders 1/1/2/3/2 = 9. 84% came on Nov 1 ($2,292). It depends on the founder's 3.5k X followers and on coaching.
- 1418 Technologies 1/3/2/2/1 = 9. A steady ~$2k a month since July looks like one client retainer for ML services: consulting, not a product.
- Peeklens 1/1/1/2/1 = 6. Two payments ($5,000 and $7,500) for B2B medical writing. The site is medcytes.com, not "Peeklens", so the name and the site don't match.

**WHY THIS COULD FAIL**
- **lumabar:** only 2 months old. Nov 3 alone was $858, probably one viral post. The current price is a launch discount. Free rivals exist (TaskbarX, Seelen UI), and Microsoft could ship the features itself.
- **INXANITY Labs:** the catalog is built on decompiled browser games and game mods, so one copyright takedown could end it. Sales are already fading after the launch week.

## 2026-11-09 run (weekly)
Source: https://trustmrr.com/api/ai/discovery → `fastestGrowingStartups` (25). All 25 .md pages opened (HTTP 200) on 2026-11-09 ~08:50 ET. New since 2026-11-05: autodm, drafterplus, morphy, scalereach, slidelabs-net, storystitch, swarmpane, taskdesk. Gone: 2fa-authenticator, bytemail, inxanity-labs, kiiwi, printotr-a, vedicastrolab, vinoveo, workel.

### Prospo (`prospo`)
- TrustMRR: https://trustmrr.com/startup/prospo · md: https://trustmrr.com/startup/prospo.md
- Site: https://prospo.io/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-09T11:44:27.012Z
- Revenue section: 24 hours $0.00 / 7 days $0.00 / 30 days $4,801 / 3 months $4,805 / 12 months $4,805 / All time $4,805
- Snapshot line: $4,801
- Daily (last 30): paid days 2/30 · biggest day $4,800.00 on 2026-10-26 = 100% of daily total
- Monthly timeline: 2026-10 $4,805
- MRR / active subscriptions: $0.00 / 0
- Pricing (founder text): Starter $29/mo, Pro $99/mo, Agency $199/mo. 7-day free trial, no card required.
- Channels (TrustMRR): SEO, LinkedIn, Instagram, X / Twitter, Product Hunt
- Founder X followers: 29

### Anonymous startup (`stealth-company-41`)
- TrustMRR: https://trustmrr.com/startup/stealth-company-41 · md: https://trustmrr.com/startup/stealth-company-41.md
- Site: none listed | stealthMode: true
- Payment provider: Stripe (API key) | last synced 2026-11-09T11:20:53.745Z
- Revenue section: 24 hours $0.00 / 7 days $0.00 / 30 days $2,004 / 3 months $2,012 / 12 months $2,012 / All time $2,012
- Snapshot line: $2,004
- Daily (last 30): paid days 2/30 · biggest day $2,000.00 on 2026-10-27 = 100% of daily total
- Monthly timeline: 2026-08 $4.00 · 2026-09 $4.00 · 2026-10 $2,004
- MRR / active subscriptions: $4.00 / 1
- Pricing (founder text): not shown
- Channels (TrustMRR): empty
- Founder X followers: 519

### Deepnia (`deepnia`)
- TrustMRR: https://trustmrr.com/startup/deepnia · md: https://trustmrr.com/startup/deepnia.md
- Site: https://deepnia.com/ | stealthMode: false
- Payment provider: Whop (API key) | last synced 2026-11-09T12:35:02.402Z
- Revenue section: 24 hours $1.50 / 7 days $254 / 30 days $893 / 3 months $895 / 12 months $895 / All time $895
- Snapshot line: $893
- Daily (last 30): paid days 20/30 · biggest day $322.00 on 2026-10-28 = 36% of daily total
- Monthly timeline: 2026-09 $2.00 · 2026-10 $580 · 2026-11 $313
- MRR / active subscriptions: $409 / 34
- Pricing (founder text): Credits: 10 credits for $3.50, 50 credits for $10.80, 100 credits for $17.00, 500 credits for $71.00; Pro and Business subscriptions available.
- Channels (TrustMRR): empty
- Founder X followers: 4,808

### ClipUtils (`cliputils`)
- TrustMRR: https://trustmrr.com/startup/cliputils · md: https://trustmrr.com/startup/cliputils.md
- Site: https://cliputils.com/ | stealthMode: false
- Payment provider: Dodo Payments (API key) | last synced 2026-11-09T12:43:05.971Z
- Revenue section: 24 hours $38.40 / 7 days $205 / 30 days $603 / 3 months $605 / 12 months $605 / All time $605
- Snapshot line: $603
- Daily (last 30): paid days 30/30 · biggest day $98.89 on 2026-10-21 = 16% of daily total
- Monthly timeline: 2026-10 $394 · 2026-11 $210
- MRR / active subscriptions: $379 / 49
- Pricing (founder text): Freemium business model. Free online tools with opportunities for monetization through premium subscriptions, sponsored placements and advertising.
- Channels (TrustMRR): SEO, Content marketing
- Founder X followers: 7,801

### Next Level Builders (`next-level-builders`)
- TrustMRR: https://trustmrr.com/startup/next-level-builders · md: https://trustmrr.com/startup/next-level-builders.md
- Site: https://nextlevelbuilder.io/ | stealthMode: false
- Payment provider: Polar (API key) | last synced 2026-11-09T08:26:00.107Z
- Revenue section: 24 hours $0.00 / 7 days $267 / 30 days $2,740 / 3 months $3,081 / 12 months $8,647 / All time $17,578
- Snapshot line: $2,740
- Daily (last 30): paid days 5/30 · biggest day $2,292.00 on 2026-11-01 = 84% of daily total
- Monthly timeline: 2026-08 $479 · 2026-09 $9.00 · 2026-10 $181 · 2026-11 $2,559
- MRR / active subscriptions: $747 / 29
- Pricing (founder text): Premium: $39/month billed annually at $468/year, VIP: $79/month billed annually at $948/year
- Channels (TrustMRR): empty
- Founder X followers: 3,486

### swarmpane (`swarmpane`)
- TrustMRR: https://trustmrr.com/startup/swarmpane · md: https://trustmrr.com/startup/swarmpane.md
- Site: https://swarmpane.com/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-09T06:32:27.525Z
- Revenue section: 24 hours $1.00 / 7 days $51.10 / 30 days $564 / 3 months $566 / 12 months $566 / All time $566
- Snapshot line: $564
- Daily (last 30): paid days 23/30 · biggest day $307.00 on 2026-10-30 = 54% of daily total
- Monthly timeline: 2026-10 $515 · 2026-11 $51.10
- MRR / active subscriptions: $237 / 10
- Pricing (founder text): not shown
- Channels (TrustMRR): SEO, X / Twitter
- Founder X followers: 1,613

### DevOps Daily (`devops-daily`)
- TrustMRR: https://trustmrr.com/startup/devops-daily · md: https://trustmrr.com/startup/devops-daily.md
- Site: https://devops-daily.com/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-09T10:18:15.116Z
- Revenue section: 24 hours $0.00 / 7 days $9.50 / 30 days $3,628 / 3 months $11,157 / 12 months $22,166 / All time $22,166
- Snapshot line: $3,628
- Daily (last 30): paid days 5/30 · biggest day $3,500.00 on 2026-10-17 = 96% of daily total
- Monthly timeline: 2026-08 $3,010 · 2026-09 $4,519 · 2026-10 $3,628 · 2026-11 $9.50
- MRR / active subscriptions: $91.00 / 5
- Pricing (founder text): Free: $0 forever
- Channels (TrustMRR): Blog, Newsletter, Content marketing, SEO, Facebook, LinkedIn, Threads, X / Twitter, Google Ads, Email marketing, Forums, Referral program, Affiliate, Press & PR
- Founder X followers: 1,595

### Morphy (`morphy`)
- TrustMRR: https://trustmrr.com/startup/morphy · md: https://trustmrr.com/startup/morphy.md
- Site: https://www.appmorphy.com/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-09T12:37:31.445Z
- Revenue section: 24 hours $9.00 / 7 days $57.06 / 30 days $950 / 3 months $955 / 12 months $955 / All time $955
- Snapshot line: $950
- Daily (last 30): paid days 23/30 · biggest day $206.00 on 2026-10-28 = 22% of daily total
- Monthly timeline: 2026-10 $889 · 2026-11 $66.06
- MRR / active subscriptions: $471 / 67
- Pricing (founder text): Free plan. Pro $9/month (limited spots, then $14). Lifetime $99 (limited spots, then $299)
- Channels (TrustMRR): Instagram, TikTok, Discord, YouTube
- Founder X followers: 22

### lumabar (`lumabar`)
- TrustMRR: https://trustmrr.com/startup/lumabar · md: https://trustmrr.com/startup/lumabar.md
- Site: https://lumabar.xyz/ | stealthMode: false
- Payment provider: Polar (API key) | last synced 2026-11-09T12:13:57.592Z
- Revenue section: 24 hours $820 / 7 days $3,206 / 30 days $4,506 / 3 months $4,530 / 12 months $4,530 / All time $4,530
- Snapshot line: $4,506
- Daily (last 30): paid days 26/30 · biggest day $858.00 on 2026-11-03 = 19% of daily total
- Monthly timeline: 2026-09 $0.00 · 2026-10 $1,228 · 2026-11 $3,303
- MRR / active subscriptions: $0.00 / 0
- Pricing (founder text): $5.99 one-time (no subscription)
- Channels (TrustMRR): Reddit
- Founder X followers: 38

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
- Founder X followers: 135

### Peeklens (`peeklens`)
- TrustMRR: https://trustmrr.com/startup/peeklens · md: https://trustmrr.com/startup/peeklens.md
- Site: https://www.medcytes.com/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-09T10:41:18.365Z
- Revenue section: 24 hours $0.00 / 7 days $7,500 / 30 days $12,500 / 3 months $12,629 / 12 months $15,154 / All time $15,154
- Snapshot line: $12,500
- Daily (last 30): paid days 2/30 · biggest day $7,500.00 on 2026-11-04 = 60% of daily total
- Monthly timeline: 2026-06 $2,525 · 2026-09 $129 · 2026-10 $5,000 · 2026-11 $7,500
- MRR / active subscriptions: $0.00 / 0
- Pricing (founder text): not shown
- Channels (TrustMRR): empty
- Founder X followers: 0

### StoryStitch (`storystitch`)
- TrustMRR: https://trustmrr.com/startup/storystitch · md: https://trustmrr.com/startup/storystitch.md
- Site: https://storystitch.ai/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-09T11:05:51.325Z
- Revenue section: 24 hours $114 / 7 days $114 / 30 days $114 / 3 months $115 / 12 months $115 / All time $115
- Snapshot line: $114
- Daily (last 30): paid days 1/30 · biggest day $114.00 on 2026-11-09 = 100% of daily total
- Monthly timeline: 2026-10 $1.32 · 2026-11 $114
- MRR / active subscriptions: $0.00 / 0
- Pricing (founder text): Free preview; £14.99 one-time per book (Production Unlock + ebook); Creator Studio £19/mo; Studio Pro £49/mo; audiobook and print quoted at checkout
- Channels (TrustMRR): X / Twitter, Instagram
- Founder X followers: 0

### Qoest (`qoest`)
- TrustMRR: https://trustmrr.com/startup/qoest · md: https://trustmrr.com/startup/qoest.md
- Site: https://qoest.lemonsqueezy.com/ | stealthMode: false
- Payment provider: Lemon Squeezy (API key) | last synced 2026-03-19T21:12:53.542Z | **Primary payment provider API credential: Lemon Squeezy API key expired; expiration time unavailable**
- Revenue section: 24 hours $0.00 / 7 days $0.00 / 30 days $771 / 3 months $0.00 / 12 months $1,710 / All time $3,520
- Snapshot line: $771 **STALE:** last synced 2026-03-19 and the key has expired, so this figure is from March
- Daily (last 30): paid days 0/30
- Monthly timeline: 2025-12 $309 · 2026-01 $321 · 2026-02 $337 · 2026-03 $434
- MRR / active subscriptions: $4,274 / 20
- Pricing (founder text): $1.00 - $1,499.00
- Channels (TrustMRR): empty
- Founder X followers: 395

### Intentsly (`intentsly`)
- TrustMRR: https://trustmrr.com/startup/intentsly · md: https://trustmrr.com/startup/intentsly.md
- Site: https://intentsly.com/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-09T09:49:39.989Z
- Revenue section: 24 hours $0.00 / 7 days $0.00 / 30 days $7,388 / 3 months $7,582 / 12 months $7,936 / All time $11,091
- Snapshot line: $7,388
- Daily (last 30): paid days 2/30 · biggest day $7,291.00 on 2026-10-19 = 99% of daily total
- Monthly timeline: 2026-07 $97.00 · 2026-08 $97.00 · 2026-09 $97.00 · 2026-10 $7,388
- MRR / active subscriptions: $0.00 / 0
- Pricing (founder text): $97/mo
- Channels (TrustMRR): empty
- Founder X followers: 2,184

### AutoDM (`autodm`)
- TrustMRR: https://trustmrr.com/startup/autodm · md: https://trustmrr.com/startup/autodm.md
- Site: https://autodm.live/ | stealthMode: false
- Payment provider: razorpay (API key), Dodo Payments (API key) | last synced 2026-11-09T12:45:36.264Z
- Revenue section: 24 hours $19.99 / 7 days $22.58 / 30 days $36.70 / 3 months $37.21 / 12 months $37.21 / All time $37.21
- Snapshot line: $36.70
- Daily (last 30): paid days 9/30 · biggest day $19.99 on 2026-11-09 = 54% of daily total
- Monthly timeline: 2026-09 $0.52 · 2026-10 $14.12 · 2026-11 $22.58
- MRR / active subscriptions: $0.00 / 0
- Pricing (founder text): Free Forever: $0 with 3,000 replies per month; Creator Pro: $1.99/month or $19.99/year for unlimited replies. One-time pass also available.
- Channels (TrustMRR): empty
- Founder X followers: 295

### Bidder iQ (`bidder-iq`)
- TrustMRR: https://trustmrr.com/startup/bidder-iq · md: https://trustmrr.com/startup/bidder-iq.md
- Site: https://bidderiq.com/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-09T08:14:28.528Z
- Revenue section: 24 hours $288 / 7 days $396 / 30 days $2,424 / 3 months $2,593 / 12 months $9,128 / All time $14,144
- Snapshot line: $2,436
- Daily (last 30): paid days 10/30 · biggest day $288.00 on 2026-10-11 = 18% of daily total
- Monthly timeline: 2026-08 $132 · 2026-09 $37.00 · 2026-10 $2,052 · 2026-11 $396
- MRR / active subscriptions: $0.00 / 0
- Pricing (founder text): $396/year
- Channels (TrustMRR): empty
- Founder X followers: 285

### 1418 Technologies LLC (`1418-technologies-llc`)
- TrustMRR: https://trustmrr.com/startup/1418-technologies-llc · md: https://trustmrr.com/startup/1418-technologies-llc.md
- Site: https://1418tech.com/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-09T10:32:20.276Z
- Revenue section: 24 hours $0.00 / 7 days $1,530 / 30 days $3,563 / 3 months $5,689 / 12 months $18,247 / All time $22,547
- Snapshot line: $3,563
- Daily (last 30): paid days 3/30 · biggest day $1,500.00 on 2026-11-04 = 96% of daily total
- Monthly timeline: 2026-08 $2,063 · 2026-09 $2,063 · 2026-10 $2,063 · 2026-11 $1,530
- MRR / active subscriptions: $63.00 / 2
- Pricing (founder text): not shown
- Channels (TrustMRR): empty
- Founder X followers: 10

### Anonymous startup (`hugo-mobile-app-04`)
- TrustMRR: https://trustmrr.com/startup/hugo-mobile-app-04 · md: https://trustmrr.com/startup/hugo-mobile-app-04.md
- Site: none listed | stealthMode: true
- Payment provider: RevenueCat (API key) | last synced 2026-11-09T12:05:31.154Z
- Revenue section: 24 hours $0.29 / 7 days $5.67 / 30 days $15.42 / 3 months $26.04 / 12 months $42.02 / All time $42.02
- Snapshot line: $15.42
- Daily (last 30): paid days 30/30 · biggest day $5.15 on 2026-10-29 = 33% of daily total
- Monthly timeline: 2026-08 $10.33 · 2026-09 $0.02 · 2026-10 $9.71 · 2026-11 $5.98
- MRR / active subscriptions: $0.00 / 0
- Pricing (founder text): not shown
- Channels (TrustMRR): empty
- Founder X followers: 596

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

### ECOMSTATEMENT.COM (`ecomstatement-com`)
- TrustMRR: https://trustmrr.com/startup/ecomstatement-com · md: https://trustmrr.com/startup/ecomstatement-com.md
- Site: https://ecomstatement.com/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-09T08:56:03.293Z
- Revenue section: 24 hours $0.00 / 7 days $0.00 / 30 days $3,304 / 3 months $3,432 / 12 months $3,883 / All time $3,883
- Snapshot line: $3,304
- Daily (last 30): paid days 6/30 · biggest day $1,120.00 on 2026-10-24 = 34% of daily total
- Monthly timeline: 2026-07 $64.38 · 2026-08 $64.38 · 2026-09 $64.38 · 2026-10 $3,304
- MRR / active subscriptions: $1,146 / 2
- Pricing (founder text): Free trial, Small: $29/month, Starter: $49/month, Unlimited: $99/month, with yearly options available.
- Channels (TrustMRR): empty
- Founder X followers: 176

### Scalereach.ai (`scalereach`)
- TrustMRR: https://trustmrr.com/startup/scalereach · md: https://trustmrr.com/startup/scalereach.md
- Site: http://scalereach.ai/ | stealthMode: false
- Payment provider: Dodo Payments (API key) | last synced 2026-11-09T06:43:57.440Z
- Revenue section: 24 hours $207 / 7 days $1,840 / 30 days $2,943 / 3 months $3,017 / 12 months $3,183 / All time $3,183
- Snapshot line: $2,943
- Daily (last 30): paid days 19/30 · biggest day $438.00 on 2026-11-03 = 15% of daily total
- Monthly timeline: 2026-08 $12.00 · 2026-09 $14.69 · 2026-10 $847 · 2026-11 $2,155
- MRR / active subscriptions: $2,059 / 124
- Pricing (founder text): Pro $18/mo or $12.50/mo annual (400 min/mo), Agency $99/mo or $49/mo annual (5,000 min/mo)
- Channels (TrustMRR): Instagram, Reddit, TikTok
- Founder X followers: 0

### DaFreeAi (`drafterplus`)
- TrustMRR: https://trustmrr.com/startup/drafterplus · md: https://trustmrr.com/startup/drafterplus.md
- Site: https://www.dafreeai.site/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-09T11:46:29.396Z
- Revenue section: 24 hours $5.56 / 7 days $49.18 / 30 days $256 / 3 months $284 / 12 months $526 / All time $674
- Snapshot line: $256
- Daily (last 30): paid days 8/30 · biggest day $128.00 on 2026-11-01 = 50% of daily total
- Monthly timeline: 2026-07 $13.36 · 2026-08 $23.23 · 2026-10 $83.70 · 2026-11 $177
- MRR / active subscriptions: $116 / 4
- Pricing (founder text): Free: 50 credits, Upgrade for more credits & limits
- Channels (TrustMRR): TikTok, X / Twitter, Discord
- Founder X followers: 5

### Anonymous startup (`anonymous-startup-80`)
- TrustMRR: https://trustmrr.com/startup/anonymous-startup-80 · md: https://trustmrr.com/startup/anonymous-startup-80.md
- Site: none listed | stealthMode: true
- Payment provider: Superwall (API key) | last synced 2026-11-09T06:44:54.646Z
- Revenue section: 24 hours $2.63 / 7 days $213 / 30 days $809 / 3 months $828 / 12 months $828 / All time $828
- Snapshot line: $809
- Daily (last 30): paid days 30/30 · biggest day $55.61 on 2026-11-08 = 7% of daily total
- Monthly timeline: 2026-08 $0.00 · 2026-09 $10.11 · 2026-10 $556 · 2026-11 $261
- MRR / active subscriptions: $643 / 504
- Pricing (founder text): not shown
- Channels (TrustMRR): empty
- Founder X followers: 0

### Taskdesk (`taskdesk`)
- TrustMRR: https://trustmrr.com/startup/taskdesk · md: https://trustmrr.com/startup/taskdesk.md
- Site: https://www.taskdesk.it/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-09T10:16:14.250Z
- Revenue section: 24 hours $0.00 / 7 days $0.00 / 30 days $48.06 / 3 months $49.18 / 12 months $49.18 / All time $49.18
- Snapshot line: $48.06
- Daily (last 30): paid days 1/30 · biggest day $48.06 on 2026-10-16 = 100% of daily total
- Monthly timeline: 2026-10 $49.18
- MRR / active subscriptions: $39.27 / 2
- Pricing (founder text): Starter: €35/mese, Team: €60/mese, Business: €100/mese, Enterprise: Su misura
- Channels (TrustMRR): empty
- Founder X followers: 0

### slidelabs.net (`slidelabs-net`)
- TrustMRR: https://trustmrr.com/startup/slidelabs-net · md: https://trustmrr.com/startup/slidelabs-net.md
- Site: https://slidelabs.net/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-09T10:42:17.035Z
- Revenue section: 24 hours $0.00 / 7 days $0.00 / 30 days $250 / 3 months $376 / 12 months $459 / All time $459
- Snapshot line: $250
- Daily (last 30): paid days 1/30 · biggest day $250.00 on 2026-10-28 = 100% of daily total
- Monthly timeline: 2026-07 $65.00 · 2026-08 $12.00 · 2026-09 $114 · 2026-10 $250
- MRR / active subscriptions: $0.00 / 0
- Pricing (founder text): Free: $0, Basic: $6 one-time, Pro: $29 one-time, Max: $108 one-time
- Channels (TrustMRR): Facebook, Threads, TikTok, TikTok Ads
- Founder X followers: 503

### Checker notes 2026-11-09 (weekly)
**No new winners this week.** All 10 businesses in the $1k–$20k range with live payment keys are already in `list.md`: lumabar, Scalereach.ai, Prospo, Next Level Builders, DevOps Daily, Peeklens, Intentsly, Bidder iQ, 1418 Technologies, ECOMSTATEMENT. Under the weekly rule they don't go on top again.
**Killed:**
- 3 Anonymous startups (stealth-company-41, hugo-mobile-app-04, anonymous-startup-80).
- Expired keys: BasinCheck, Qoest (stale since March), Skillmaxing.
- Under $1k: Deepnia, ClipUtils, swarmpane, Morphy, StoryStitch, AutoDM, DaFreeAi, Taskdesk, slidelabs.net.

**Three closest new ones** (all missed only because they're under $1k):
- **ClipUtils**: $603, paid **30/30** days (Dodo Payments). 28+ online video, audio and image tools, freemium. The steadiest payer on the list.
- **Morphy**: $950, paid 23/30 days (Stripe). A desktop canvas for running AI coding agents side by side. Pro $9/mo, lifetime $99. October $889, November $66 so far, so it's fading after launch.
- **Deepnia**: $893, paid 20/30 days (Whop). AI social media posting with credit packs. The founder says most revenue goes through an unlisted gateway; that's not checked, so it doesn't count.

**Updates on already-listed winners** (not re-added):
- **lumabar**: $4,506 in 30 days (up from $2,806), paid **26/30** days. The biggest day is now only 19% of the month, and November is $3,303 after 9 days. Still the #1 pick and getting stronger.
- **Scalereach.ai**: $2,943 (up from $1,837), paid 19/30 days. November is $2,155 after 9 days. Climbing.

## 2026-11-16 run (weekly)
Source: https://trustmrr.com/api/ai/discovery → `fastestGrowingStartups` (25). All 25 .md pages opened (HTTP 200) on 2026-11-16 ~08:50 ET. New since 2026-11-09: antwork, arazio, chart-scanner-ai, formbold, hothelia, mafia-ia-premium-acceso-de-por-vida, naughty, pawr, reception, scribekit, startup-11350e2a5296, tapnoise, trustqr, useless-ads. Gone: 1418-technologies-llc, anonymous-startup-80, autodm, basincheck, bidder-iq, devops-daily, drafterplus, hugo-mobile-app-04, morphy, peeklens, skillmaxing, slidelabs-net, swarmpane, taskdesk.

### Mafia IA Premium — Acceso de por vida (`mafia-ia-premium-acceso-de-por-vida`)
- TrustMRR: https://trustmrr.com/startup/mafia-ia-premium-acceso-de-por-vida · md: https://trustmrr.com/startup/mafia-ia-premium-acceso-de-por-vida.md
- Site: https://mafiaia.com/ | stealthMode: false
- Payment provider: Creem (API key) | last synced 2026-11-16T12:42:03.077Z
- Revenue section: 24 hours $0.00 / 7 days $164 / 30 days $8,529 / 3 months $8,530 / 12 months $8,531 / All time $8,531
- Snapshot line: $8,529
- Daily (last 30): paid days 17/30 · biggest day $3,195.00 on 2026-10-23 = 37% of daily total
- Monthly timeline: 2026-08 $0.93 · 2026-10 $7,142 · 2026-11 $1,388
- MRR / active subscriptions: $0.00 / 0
- Pricing (founder text): €149 one-time payment for lifetime access; includes future updates. Some prompts are free.
- Channels (TrustMRR): Newsletter, Instagram, LinkedIn, Facebook, Threads, YouTube
- Founder X followers: 3,782

### Prospo (`prospo`)
- TrustMRR: https://trustmrr.com/startup/prospo · md: https://trustmrr.com/startup/prospo.md
- Site: https://prospo.io/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-15T17:41:55.077Z
- Revenue section: 24 hours $0.00 / 7 days $0.00 / 30 days $9,601 / 3 months $9,605 / 12 months $9,605 / All time $9,605
- Snapshot line: $9,601
- Daily (last 30): paid days 3/30 · biggest day $4,800.00 on 2026-10-26 = 50% of daily total
- Monthly timeline: 2026-10 $4,805 · 2026-11 $4,800
- MRR / active subscriptions: $0.00 / 0
- Pricing (founder text): Starter $29/mo, Pro $99/mo, Agency $199/mo. 7-day free trial, no card required.
- Channels (TrustMRR): SEO, LinkedIn, Instagram, X / Twitter, Product Hunt
- Founder X followers: 29

### Anonymous startup (`stealth-company-41`)
- TrustMRR: https://trustmrr.com/startup/stealth-company-41 · md: https://trustmrr.com/startup/stealth-company-41.md
- Site: none listed | stealthMode: true
- Payment provider: Stripe (API key) | last synced 2026-11-16T11:18:54.833Z
- Revenue section: 24 hours $0.00 / 7 days $504 / 30 days $2,504 / 3 months $2,512 / 12 months $2,516 / All time $2,516
- Snapshot line: $2,504
- Daily (last 30): paid days 3/30 · biggest day $2,000.00 on 2026-10-27 = 80% of daily total
- Monthly timeline: 2026-08 $4.00 · 2026-09 $4.00 · 2026-10 $2,004 · 2026-11 $504
- MRR / active subscriptions: $504 / 3
- Pricing (founder text): not shown
- Channels (TrustMRR): empty
- Founder X followers: 532

### TrustQR (`trustqr`)
- TrustMRR: https://trustmrr.com/startup/trustqr · md: https://trustmrr.com/startup/trustqr.md
- Site: https://trustqr.org/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-16T10:27:45.568Z
- Revenue section: 24 hours $0.00 / 7 days $600 / 30 days $1,470 / 3 months $1,474 / 12 months $1,997 / All time $2,636
- Snapshot line: $1,470
- Daily (last 30): paid days 5/30 · biggest day $600.00 on 2026-11-09 = 41% of daily total
- Monthly timeline: 2026-07 $3.00 · 2026-08 $1.00 · 2026-10 $873 · 2026-11 $600
- MRR / active subscriptions: $0.00 / 0
- Pricing (founder text): Explore Transparent Pricing
- Channels (TrustMRR): SEO, LinkedIn
- Founder X followers: 0

### Deepnia (`deepnia`)
- TrustMRR: https://trustmrr.com/startup/deepnia · md: https://trustmrr.com/startup/deepnia.md
- Site: https://deepnia.com/ | stealthMode: false
- Payment provider: Whop (API key) | last synced 2026-11-16T12:31:02.948Z
- Revenue section: 24 hours $0.00 / 7 days $85.50 / 30 days $979 / 3 months $981 / 12 months $981 / All time $981
- Snapshot line: $979
- Daily (last 30): paid days 26/30 · biggest day $322.00 on 2026-10-28 = 33% of daily total
- Monthly timeline: 2026-09 $2.00 · 2026-10 $580 · 2026-11 $399
- MRR / active subscriptions: $492 / 43
- Pricing (founder text): Credits: 10 credits for $3.50, 50 credits for $10.80, 100 credits for $17.00, 500 credits for $71.00; Pro and Business subscriptions available.
- Channels (TrustMRR): empty
- Founder X followers: 4,808

### Chart Scanner AI (`chart-scanner-ai`)
- TrustMRR: https://trustmrr.com/startup/chart-scanner-ai · md: https://trustmrr.com/startup/chart-scanner-ai.md
- Site: https://chartscannerai.com/ | stealthMode: false
- Payment provider: RevenueCat (API key) | last synced 2026-11-16T06:49:29.861Z
- Revenue section: 24 hours $8.04 / 7 days $839 / 30 days $3,588 / 3 months $3,595 / 12 months $3,595 / All time $3,595
- Snapshot line: $3,588
- Daily (last 30): paid days 30/30 · biggest day $252.00 on 2026-10-24 = 7% of daily total
- Monthly timeline: 2026-09 $0.00 · 2026-10 $1,826 · 2026-11 $1,770
- MRR / active subscriptions: $2,981 / 114
- Pricing (founder text): $7.99 weekly / $44.99 6 months
- Channels (TrustMRR): TikTok
- Founder X followers: 0

### pawr (`pawr`)
- TrustMRR: https://trustmrr.com/startup/pawr · md: https://trustmrr.com/startup/pawr.md
- Site: https://pawr.link/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-16T10:12:44.517Z
- Revenue section: 24 hours $0.00 / 7 days $2,400 / 30 days $2,484 / 3 months $2,496 / 12 months $2,632 / All time $3,429
- Snapshot line: $2,484
- Daily (last 30): paid days 4/30 · biggest day $2,400.00 on 2026-11-13 = 97% of daily total
- Monthly timeline: 2026-08 $6.00 · 2026-09 $6.00 · 2026-10 $54.00 · 2026-11 $2,436
- MRR / active subscriptions: $40.00 / 6
- Pricing (founder text): $6/mo, $4/mo when paid yearly
- Channels (TrustMRR): empty
- Founder X followers: 1,872

### lumabar (`lumabar`)
- TrustMRR: https://trustmrr.com/startup/lumabar · md: https://trustmrr.com/startup/lumabar.md
- Site: https://lumabar.xyz/ | stealthMode: false
- Payment provider: Polar (API key) | last synced 2026-11-16T06:10:27.763Z
- Revenue section: 24 hours $3,465 / 7 days $7,520 / 30 days $12,015 / 3 months $12,051 / 12 months $12,051 / All time $12,051
- Snapshot line: $12,015
- Daily (last 30): paid days 30/30 · biggest day $3,919.00 on 2026-11-15 = 33% of daily total
- Monthly timeline: 2026-09 $0.00 · 2026-10 $1,228 · 2026-11 $10,823
- MRR / active subscriptions: $0.00 / 0
- Pricing (founder text): $5.99 one-time (no subscription)
- Channels (TrustMRR): Reddit
- Founder X followers: 87

### Free Contact Form to Email API for Modern Websites (`formbold`)
- TrustMRR: https://trustmrr.com/startup/formbold · md: https://trustmrr.com/startup/formbold.md
- Site: https://formbold.com/ | stealthMode: false
- Payment provider: Paddle (API key) | last synced 2026-11-16T12:28:04.588Z
- Revenue section: 24 hours $6.00 / 7 days $44.70 / 30 days $666 / 3 months $668 / 12 months $668 / All time $668
- Snapshot line: $666
- Daily (last 30): paid days 22/30 · biggest day $206.00 on 2026-10-30 = 31% of daily total
- Monthly timeline: 2026-10 $572 · 2026-11 $95.70
- MRR / active subscriptions: $656 / 93
- Pricing (founder text): Free, Starter, Premium, Business plan
- Channels (TrustMRR): empty
- Founder X followers: 3,744

### Next Level Builders (`next-level-builders`)
- TrustMRR: https://trustmrr.com/startup/next-level-builders · md: https://trustmrr.com/startup/next-level-builders.md
- Site: https://nextlevelbuilder.io/ | stealthMode: false
- Payment provider: Polar (API key) | last synced 2026-11-16T08:25:58.809Z
- Revenue section: 24 hours $0.00 / 7 days $257 / 30 days $2,988 / 3 months $3,329 / 12 months $8,904 / All time $17,835
- Snapshot line: $2,988
- Daily (last 30): paid days 5/30 · biggest day $2,292.00 on 2026-11-01 = 77% of daily total
- Monthly timeline: 2026-08 $479 · 2026-09 $9.00 · 2026-10 $181 · 2026-11 $2,816
- MRR / active subscriptions: $718 / 29
- Pricing (founder text): Premium: $39/month billed annually at $468/year, VIP: $79/month billed annually at $948/year
- Channels (TrustMRR): empty
- Founder X followers: 3,494

### TapNoise (`tapnoise`)
- TrustMRR: https://trustmrr.com/startup/tapnoise · md: https://trustmrr.com/startup/tapnoise.md
- Site: https://tapnoise.com/ | stealthMode: false
- Payment provider: Dodo Payments (API key) | last synced 2026-11-16T12:27:32.166Z
- Revenue section: 24 hours $11.98 / 7 days $117 / 30 days $1,330 / 3 months $1,335 / 12 months $1,335 / All time $1,335
- Snapshot line: $1,330
- Daily (last 30): paid days 29/30 · biggest day $291.00 on 2026-10-19 = 22% of daily total
- Monthly timeline: 2026-10 $998 · 2026-11 $337
- MRR / active subscriptions: $0.00 / 0
- Pricing (founder text): One-time: Solo $14.99/1 Mac; Duo $20.99/2 Macs + tax. Limited launch from $5.99/$7.99. All updates included. No trial. 7-day refunds.
- Channels (TrustMRR): Blog, SEO, X / Twitter
- Founder X followers: 665

### Antwork (`antwork`)
- TrustMRR: https://trustmrr.com/startup/antwork · md: https://trustmrr.com/startup/antwork.md
- Site: https://antwork.io/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-16T09:31:08.657Z
- Revenue section: 24 hours $0.00 / 7 days $285 / 30 days $852 / 3 months $858 / 12 months $858 / All time $858
- Snapshot line: $852
- Daily (last 30): paid days 10/30 · biggest day $223.00 on 2026-11-04 = 26% of daily total
- Monthly timeline: 2026-10 $24.20 · 2026-11 $834
- MRR / active subscriptions: $245 / 13
- Pricing (founder text): Free: 2 accounts, 10 posts/mo. Pro $19 (5 accounts), Business $29 (10), Scale $39 (30), Agency $89 (100). Unlimited posts on paid plans, 7-day trial.
- Channels (TrustMRR): empty
- Founder X followers: 13

### Reception (`reception`)
- TrustMRR: https://trustmrr.com/startup/reception · md: https://trustmrr.com/startup/reception.md
- Site: https://reception.sh/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-16T12:28:04.770Z
- Revenue section: 24 hours $0.00 / 7 days $0.00 / 30 days $2,895 / 3 months $2,920 / 12 months $2,920 / All time $2,920
- Snapshot line: $2,895
- Daily (last 30): paid days 14/30 · biggest day $950.00 on 2026-10-29 = 33% of daily total
- Monthly timeline: 2026-10 $2,716 · 2026-11 $204
- MRR / active subscriptions: $1,017 / 44
- Pricing (founder text): $25 per month
- Channels (TrustMRR): empty
- Founder X followers: 19,057

### StoryStitch (`storystitch`)
- TrustMRR: https://trustmrr.com/startup/storystitch · md: https://trustmrr.com/startup/storystitch.md
- Site: https://storystitch.ai/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-15T17:04:17.481Z
- Revenue section: 24 hours $0.00 / 7 days $140 / 30 days $140 / 3 months $141 / 12 months $141 / All time $141
- Snapshot line: $140
- Daily (last 30): paid days 2/30 · biggest day $114.00 on 2026-11-09 = 81% of daily total
- Monthly timeline: 2026-10 $1.32 · 2026-11 $140
- MRR / active subscriptions: $0.00 / 0
- Pricing (founder text): Free preview; £14.99 one-time per book (Production Unlock + ebook); Creator Studio £19/mo; Studio Pro £49/mo; audiobook and print quoted at checkout
- Channels (TrustMRR): X / Twitter, Instagram
- Founder X followers: 0

### ScribeKit (`scribekit`)
- TrustMRR: https://trustmrr.com/startup/scribekit · md: https://trustmrr.com/startup/scribekit.md
- Site: https://www.trulyoffline.app/scribekit | stealthMode: false
- Payment provider: RevenueCat (API key) | last synced 2026-11-16T12:22:59.364Z
- Revenue section: 24 hours $0.00 / 7 days $99.77 / 30 days $195 / 3 months $197 / 12 months $197 / All time $197
- Snapshot line: $195
- Daily (last 30): paid days 14/30 · biggest day $44.64 on 2026-10-22 = 23% of daily total
- Monthly timeline: 2026-08 $0.00 · 2026-09 $0.00 · 2026-10 $65.13 · 2026-11 $132
- MRR / active subscriptions: $29.37 / 17
- Pricing (founder text): Free; Pro $1.99/month, $9.99/year (7-day trial) or $19.99 lifetime
- Channels (TrustMRR): App store optimization, Instagram, Threads, X / Twitter, YouTube, Forums, Hacker News, Word of mouth
- Founder X followers: 4

### Anonymous startup (`startup-11350e2a5296`)
- TrustMRR: https://trustmrr.com/startup/startup-11350e2a5296 · md: https://trustmrr.com/startup/startup-11350e2a5296.md
- Site: none listed | stealthMode: true
- Payment provider: Shopify (OAuth connection) | last synced 2026-11-16T07:50:32.127Z
- Revenue section: 24 hours $89.15 / 7 days $1,715 / 30 days $4,654 / 3 months $4,706 / 12 months $4,706 / All time $4,706
- Snapshot line: $4,654
- Daily (last 30): paid days 27/30 · biggest day $384.00 on 2026-11-11 = 8% of daily total
- Monthly timeline: 2026-10 $1,984 · 2026-11 $2,721
- MRR / active subscriptions: $0.00 / 0
- Pricing (founder text): not shown
- Channels (TrustMRR): empty
- Founder X followers: 0

### Qoest (`qoest`)
- TrustMRR: https://trustmrr.com/startup/qoest · md: https://trustmrr.com/startup/qoest.md
- Site: https://qoest.lemonsqueezy.com/ | stealthMode: false
- Payment provider: Lemon Squeezy (API key) | last synced 2026-03-19T21:12:53.542Z | **Primary payment provider API credential: Lemon Squeezy API key expired; expiration time unavailable**
- Revenue section: 24 hours $0.00 / 7 days $0.00 / 30 days $771 / 3 months $0.00 / 12 months $1,710 / All time $3,520
- Snapshot line: $771 **STALE:** last synced 2026-03-19 and the key has expired, so this figure is from March
- Daily (last 30): paid days 0/30
- Monthly timeline: 2025-12 $309 · 2026-01 $321 · 2026-02 $337 · 2026-03 $434
- MRR / active subscriptions: $4,274 / 20
- Pricing (founder text): $1.00 - $1,499.00
- Channels (TrustMRR): empty
- Founder X followers: 395

### Intentsly (`intentsly`)
- TrustMRR: https://trustmrr.com/startup/intentsly · md: https://trustmrr.com/startup/intentsly.md
- Site: https://intentsly.com/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-16T09:49:10.928Z
- Revenue section: 24 hours $0.00 / 7 days $0.00 / 30 days $7,388 / 3 months $7,582 / 12 months $7,936 / All time $11,091
- Snapshot line: $7,388
- Daily (last 30): paid days 2/30 · biggest day $7,291.00 on 2026-10-19 = 99% of daily total
- Monthly timeline: 2026-07 $97.00 · 2026-08 $97.00 · 2026-09 $97.00 · 2026-10 $7,388
- MRR / active subscriptions: $0.00 / 0
- Pricing (founder text): $97/mo
- Channels (TrustMRR): empty
- Founder X followers: 2,188

### Hothelia (`hothelia`)
- TrustMRR: https://trustmrr.com/startup/hothelia · md: https://trustmrr.com/startup/hothelia.md
- Site: https://hothelia.com/ | stealthMode: false
- Payment provider: Polar (API key) | last synced 2026-11-16T11:54:28.470Z
- Revenue section: 24 hours $0.00 / 7 days $71.00 / 30 days $71.00 / 3 months $72.00 / 12 months $72.00 / All time $72.00
- Snapshot line: $71.00
- Daily (last 30): paid days 1/30 · biggest day $71.00 on 2026-11-09 = 100% of daily total
- Monthly timeline: 2026-10 $1.00 · 2026-11 $71.00
- MRR / active subscriptions: $0.00 / 0
- Pricing (founder text): Plan Flex: $69/mo, Plan Basic: $99/mo, Plan Pro: $149/mo, Plan Enterprise: 8% commission
- Channels (TrustMRR): empty
- Founder X followers: 0

### Useless Ads (`useless-ads`)
- TrustMRR: https://trustmrr.com/startup/useless-ads · md: https://trustmrr.com/startup/useless-ads.md
- Site: https://uselessads.site/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-16T06:27:29.840Z
- Revenue section: 24 hours $0.00 / 7 days $3.96 / 30 days $91.54 / 3 months $93.02 / 12 months $93.02 / All time $93.02
- Snapshot line: $91.54
- Daily (last 30): paid days 13/30 · biggest day $46.16 on 2026-11-05 = 50% of daily total
- Monthly timeline: 2026-10 $25.80 · 2026-11 $67.22
- MRR / active subscriptions: $17.16 / 4
- Pricing (founder text): $0.99/week per ad. Optional logo +$0.49 and bold stroke +$0.49 one-time.
- Channels (TrustMRR): X / Twitter, LinkedIn, Reddit, Cold DM
- Founder X followers: 818

### Arazio For Mac (`arazio`)
- TrustMRR: https://trustmrr.com/startup/arazio · md: https://trustmrr.com/startup/arazio.md
- Site: https://arazioformac.com/ | stealthMode: false
- Payment provider: Dodo Payments (API key) | last synced 2026-11-16T11:48:57.924Z
- Revenue section: 24 hours $19.18 / 7 days $19.18 / 30 days $164 / 3 months $180 / 12 months $180 / All time $180
- Snapshot line: $164
- Daily (last 30): paid days 9/30 · biggest day $51.29 on 2026-10-18 = 31% of daily total
- Monthly timeline: 2026-09 $13.49 · 2026-10 $133 · 2026-11 $34.17
- MRR / active subscriptions: $0.00 / 0
- Pricing (founder text): 10$ lifetime , pricing varies for each country based on PPP
- Channels (TrustMRR): empty
- Founder X followers: 30

### ClipUtils (`cliputils`)
- TrustMRR: https://trustmrr.com/startup/cliputils · md: https://trustmrr.com/startup/cliputils.md
- Site: https://cliputils.com/ | stealthMode: false
- Payment provider: Dodo Payments (API key) | last synced 2026-11-15T18:39:35.737Z
- Revenue section: 24 hours $34.43 / 7 days $271 / 30 days $855 / 3 months $869 / 12 months $869 / All time $869
- Snapshot line: $855
- Daily (last 30): paid days 30/30 · biggest day $98.89 on 2026-10-21 = 12% of daily total
- Monthly timeline: 2026-10 $394 · 2026-11 $475
- MRR / active subscriptions: $399 / 67
- Pricing (founder text): Freemium business model. Free online tools with opportunities for monetization through premium subscriptions, sponsored placements and advertising.
- Channels (TrustMRR): SEO, Content marketing
- Founder X followers: 7,801

### WeNaughty (`naughty`)
- TrustMRR: https://trustmrr.com/startup/naughty · md: https://trustmrr.com/startup/naughty.md
- Site: https://apps.apple.com/us/app/dirty-truth-or-dare-wenaughty/id6817063947?uo=4 | stealthMode: false
- Payment provider: RevenueCat (API key) | last synced 2026-11-16T12:27:03.808Z
- Revenue section: 24 hours $8.20 / 7 days $183 / 30 days $531 / 3 months $539 / 12 months $539 / All time $539
- Snapshot line: $531
- Daily (last 30): paid days 28/30 · biggest day $55.26 on 2026-11-15 = 10% of daily total
- Monthly timeline: 2026-08 $0.00 · 2026-09 $0.00 · 2026-10 $153 · 2026-11 $386
- MRR / active subscriptions: $412 / 33
- Pricing (founder text): Free; VIP Weekly $3.99, VIP Annual $29.99, VIP Monthly $6.99
- Channels (TrustMRR): empty
- Founder X followers: 8,117

### Scalereach.ai (`scalereach`)
- TrustMRR: https://trustmrr.com/startup/scalereach · md: https://trustmrr.com/startup/scalereach.md
- Site: https://scalereach.ai/ | stealthMode: false
- Payment provider: Dodo Payments (API key) | last synced 2026-11-16T06:40:02.284Z
- Revenue section: 24 hours $1,567 / 7 days $3,697 / 30 days $6,585 / 3 months $6,714 / 12 months $6,880 / All time $6,880
- Snapshot line: $6,585
- Daily (last 30): paid days 24/30 · biggest day $1,855.00 on 2026-11-15 = 28% of daily total
- Monthly timeline: 2026-08 $12.00 · 2026-09 $14.69 · 2026-10 $847 · 2026-11 $5,852
- MRR / active subscriptions: $2,988 / 175
- Pricing (founder text): Pro $18/mo or $12.50/mo annual (400 min/mo), Agency $99/mo or $49/mo annual (5,000 min/mo)
- Channels (TrustMRR): Instagram, Reddit, TikTok
- Founder X followers: 0

### ECOMSTATEMENT.COM (`ecomstatement-com`)
- TrustMRR: https://trustmrr.com/startup/ecomstatement-com · md: https://trustmrr.com/startup/ecomstatement-com.md
- Site: https://ecomstatement.com/ | stealthMode: false
- Payment provider: Stripe (API key) | last synced 2026-11-16T08:55:33.157Z
- Revenue section: 24 hours $0.00 / 7 days $162 / 30 days $3,574 / 3 months $3,703 / 12 months $4,154 / All time $4,154
- Snapshot line: $3,574
- Daily (last 30): paid days 8/30 · biggest day $1,120.00 on 2026-10-24 = 31% of daily total
- Monthly timeline: 2026-08 $64.38 · 2026-09 $64.38 · 2026-10 $3,304 · 2026-11 $271
- MRR / active subscriptions: $1,131 / 2
- Pricing (founder text): Free trial, Small: $29/month, Starter: $49/month, Unlimited: $99/month, with yearly options available.
- Channels (TrustMRR): empty
- Founder X followers: 175

### Checker notes 2026-11-16 (weekly)
Re-opened the 6 new in-range .md pages; all 30-day figures matched, and all 6 sites opened (HTTP 200).
**New survivors (not in list.md before):** Chart Scanner AI, TapNoise, Reception, Mafia IA Premium, pawr, TrustQR.
**Already listed, not re-added:** lumabar, Scalereach.ai, Prospo, Next Level Builders, Intentsly, ECOMSTATEMENT.
**Killed:**
- 2 Anonymous startups (stealth-company-41; startup-11350e2a5296 at $4,654 with 27 paid days, but anonymous means out).
- Qoest: expired key, stale since March.
- Under $1k: Deepnia ($979, 26 paid days, almost there), ClipUtils ($855, 30/30), FormBold, Antwork, StoryStitch, ScribeKit, Hothelia, Useless Ads, Arazio, WeNaughty.

**Scores** (paid days / growth / fit with code+design+content / demand / sell alone):
- **Chart Scanner AI** 5/4/4/3/4 = **20 STEAL-READY**. Paid **30/30** days, biggest day only 7% of the month. 114 active subscriptions, $2,981 MRR. Oct $1,826; Nov $1,770 by the 16th. An iOS app: screenshot a chart and get an AI Long/Hold/Short reading. Founder has 0 X followers; channel is TikTok. Demand is scored 3 because the App Store shows only 1 rating, though dozens of copycat "chart AI" apps show the category sells.
- **TapNoise** 5/2/5/3/5 = **20 STEAL-READY**. Paid 29/30 days. A Mac menu-bar app for keyboard sounds plus "agent done" chimes for Claude Code and Codex. But Oct $998, then only $337 by Nov 16, so it's slowing. Tie with Chart Scanner: ranked second because Chart Scanner is steady **and** climbing, while TapNoise is steady but fading.
- Reception 3/2/4/3/2 = 14. In-app review and upsell SDK, $25/mo, 44 subscriptions. Oct $2,716, then $204 in November. The founder has 19,057 X followers, so growth likely rides the audience.
- Mafia IA Premium 4/1/4/2/2 = 13. A Spanish €149 lifetime AI-prompt and tool pack. Oct $7,142, then fading ($1,388 in November). Founder newsletter plus 3.8k X followers.
- pawr 1/1/4/3/3 = 12. A link-in-bio page at $6/mo; 97% of the month is one $2,400 day.
- TrustQR 2/1/2/2/1 = 8. B2B anti-counterfeit QR tags: physical product and sales-led.

**Updates on listed winners:** lumabar now **$12,015** in 30 days ($3,465 in the last 24h alone). Scalereach.ai **$6,585**. Both are still climbing fast.

**WHY THIS COULD FAIL**
- **Chart Scanner AI:** trading apps live close to "financial advice", so regulators or App Store review could hit it. The category is flooded with near-identical apps. $7.99/week subscriptions churn fast and usually need paid TikTok or Meta ads. Only 1 public rating, so buyer love is unproven.
- **TapNoise:** sales are already halving month over month. Free rivals exist (Klack-style apps, KeyBell, Tacque), and novelty apps fade.
