# Indoor Hunt Co.: plan from A to Z (5-day launch → 2-year business)

**Owner:** you (≈10 h/week). **Operator:** Claude (research, build, content, ads setup, reporting).
**Budget:** $500. **Market:** USA. **Model:** dropshipping (CJ US warehouse ships; you never touch stock).
**Store:** custom Next.js site on Vercel + Stripe + CJ API (already built: `store/`).

> **Honest frame.** Nobody can guarantee sales. What this plan guarantees is that every day goes on the
> things that produce sales, with clear numbers that decide stop / fix / scale. Most new stores fail at
> step 1 (no product–video fit). We'll find out in about 2 weeks for under $300 instead of after months.

---

## 1. The decisions (already made)

| Decision | Choice | Why |
|---|---|---|
| Niche | Indoor cat play | Cat videos spread well; light, cheap-to-ship products; no health claims needed |
| Hero product | **Locked on day 1 from CJ US stock** (see "Product lock" below) | The research favourite has open IP and stock questions |
| Brand | Indoor Hunt Co. (sub-niche brand, not a product brand) | A second or third product can be added without rebranding |
| Price | $24.99 single · $39.99 2-pack · $54.99 3-pack · $9.99 lure refill add-on | ~51–54% margin before ads; bundles raise order value |
| Shipping | Free over $29, else $4.99 · 5–7 business days from CJ US warehouse | Unit 2 unlocks free shipping |
| Platform | Own site (no Shopify fee) on Vercel free tier | $0/month fixed cost |
| Traffic | Organic TikTok + Instagram every day, plus small TikTok ads from day 3 | New accounts get little organic reach in week 1. Ads are what make a 5-day sale realistic |

### Product lock (day 1, needs your CJ account)
Sourcing research (24 Nov) found three problems with the original favourite, the reel fishing-rod toy:
- No confirmed US-warehouse, no-MOQ source. CJ search needs a logged-in account.
- **US patent 10,271,519 "Pet toy caster" (2019) claims a reel on a rod and may still be in force.**
- Competitors sell reel rods for $10–20.

So the hero is chosen on day 1, using your CJ API key, as **the first candidate below that passes every check**:

| Order | Candidate | Notes |
|---|---|---|
| 1 | "Cat TV" window bird feeder (suction-cup, clear acrylic) | Strong video (birds + cat watching), gift-friendly, no patent flag found. Must sell at ≥ $32.99 to clear margin |
| 2 | Telescopic teaser wand **without reel** + lure refill system | Avoids the reel patent claim. Cheaper, more crowded, so it wins on bundle + content |
| 3 | Reel fishing-rod toy | **Only** if the listing shows a licence or a patent attorney clears it (≈$300–500 opinion). Skipped by default |

**Checks:**
- In CJ **US** warehouse with ≥ 100 units
- US→US delivery ≤ 5 days
- Margin floor met after shipping and fees
- ≥ 4 real product photos/videos
- No brand names or patent marks on the listing

`store/lib/product.js` is swapped to the winner; the brand (Indoor Hunt Co.) and site stay the same.
The current site copy ("Reel Hunter Wand") is a placeholder until then.

### Budget ($500)
| Item | $ | Note |
|---|---|---|
| Domain | 15 | Yearly |
| CJ wallet top-up | 60 | Pays the supplier for the first orders; refilled from Stripe payouts |
| One test unit shipped to you | 15 | Optional but strongly advised: quality check + real "unboxing / cat playing" footage |
| Ads, launch week (days 3–5) | 75 | $25/day on 2–3 videos |
| Ads, weeks 2–3 (only behind proven videos) | 175 | Released only if the rules in §4 are met |
| Reserve | 160 | Refunds, chargebacks, cash-flow gap (Stripe pays out 2–7 days after a sale) |
| Stripe, Vercel, Resend, ManyChat | 0 | Free tiers |

### Unit economics (estimates until CJ quotes; update after day 1)
- Expected average order ≈ **$38** (mix of single / 2-pack / 3-pack, about 1 in 5 adding the refill).
- Product + supplier shipping + Stripe fees for that order ≈ **$18**.
- **Gross profit before ads ≈ $20/order**, so **break-even cost per sale from ads ≈ $20.**
- Target: get cost per sale under **$14** (≈30% profit after ads) before raising the budget.

---

## 2. The 5-day launch sprint (goal: first paid orders before day 6)

**Rule:** every hour you spend is on accounts and posting. Claude does everything else.

### Day 1: accounts + product locked
| You (≈90 min) | Claude |
|---|---|
| Create **Stripe** (ID + bank) | Lock the CJ US-warehouse listing: cost, ship time, variant IDs, photos |
| Create **CJ Dropshipping**, add $60 to wallet, create API key | Replace placeholder images with real product media; finalize page copy |
| Create **Resend** (free), **Instagram** + **TikTok** business accounts (same handle) | Deploy store to a free Vercel address for you to review |
| Choose domain (Claude suggests 3 available names) | Write 14 video scripts + captions (see §5) and generate the first 6 faceless clips |
| Order 1 test unit to your address (optional) | Set up profile bios, link-in-bio, profile images |

### Day 2: store goes live
| You (≈45 min) | Claude |
|---|---|
| Paste keys into Vercel (guided step by step), buy domain | Connect Stripe + CJ + email; set webhook + tracking cron |
| Approve "go live" | **Real end-to-end test order** (test card → CJ order created → cancelled) |
| Post first 2 videos (TikTok), 1 Reel (Instagram) | Policies, contact page, business address, launch checklist all green |
| Text 20 cat-owning friends the link (fastest real first sale) | Set up comment-to-DM: comment "LINK" and get the product link |

### Day 3: traffic on
| You (≈40 min) | Claude |
|---|---|
| Post 2–3 TikToks + 1 Reel; reply to every comment for 15 min | Build TikTok ad campaign: 3 videos × 1 ad group, $25/day, US, 25–54, pet interests + broad |
| Approve the ad spend | Install TikTok pixel + purchase event so ads optimise for sales |

### Day 4: read, cut, double down
| You (≈30 min) | Claude |
|---|---|
| Post, reply | Read ad + organic data: watch time, click rate, cost per click, add-to-carts |
| | Turn off the worst video; make 3 new versions of the best hook |
| | Fix page leaks (if clicks but no add-to-cart → page/price issue; if carts but no buy → checkout/shipping issue) |

### Day 5: first-sale push
| You (≈30 min) | Claude |
|---|---|
| Post, reply, share in 2–3 cat Facebook groups **where the rules allow promotion** | Launch offer: "free lure refill with any 2-pack this week" (real, time-boxed, honestly stated) |
| | Abandoned-checkout email (Stripe Checkout recovery) |
| | Day-5 report: sales, cost per sale, best video, decision for week 2 |

**What "success by day 5" looks like:** ≥1 real order from a stranger and a cost per click under $1.
Even with zero sales, the data tells us whether the problem is the video, the page or the product, and
week 2 fixes that one thing.

---

## 3. 2-year roadmap: stages move on numbers, not dates

| Stage | Typical timing | Goal | Move on when… | Main work |
|---|---|---|---|---|
| **0. Launch** | Days 1–5 | First sale | Store live + first stranger order | §2 sprint |
| **1. Validate** | Weeks 2–4 | Find a winning video + offer | 30 orders and cost per sale < $20 for 7 days | 3 new videos/day, kill losers in 48 h, page tweaks, reviews from first buyers |
| **2. Profitable** | Months 2–3 | Steady profit | 10+ orders/day at cost per sale < $14 for 14 days | Raise ads 20% every 3 days while profitable; email flows (welcome, post-purchase, win-back); real customer photos and reviews |
| **3. Small brand** | Months 4–6 | $15–40k revenue/month | 3 products selling, repeat rate > 15% | Add products 2 and 3 (window "cat TV" bird feeder for winter, then a cool-mist grooming brush or a silvervine add-on); move to a multi-product store (Medusa from your list); TikTok Shop + affiliate creators; part-time VA for support |
| **4. Own the margin** | Months 7–12 | 35–45% margin | Hero sells > 600 units/month | Branded packaging via CJ, bulk stock in CJ US warehouse or a 3PL; Meta + Google Shopping ads; Hyperswitch if a second payment processor is needed; LLC + bookkeeping |
| **5. Expand** | Year 2 | $80–150k revenue/month | Each new channel profitable on its own | Amazon / Walmart via a multi-channel tool, Canada/UK, 8–12 product cat line, subscription refills (lures and silvervine), wholesale to pet boutiques |

**Money path (illustrative, not a promise):**
- Month 3: ~$8k revenue, ~$1.5k profit.
- Month 6: ~$30k revenue, ~$6k profit.
- Month 12: ~$80k revenue, ~$20k profit.
- Month 24: ~$150k revenue, ~$40k profit.

Two years of profit on that path is roughly $250–400k. $500k is the stretch case and needs stage 4 margins plus a second hit product.

---

## 4. Decision rules (so nothing is decided on feelings)

**Ads**
- A new ad gets $20–30 before judging it.
- Kill it if, after 1.5× break-even spend (~$30), it has no add-to-cart.
- Kill it if its click rate is under 0.8% after 2,000 views.
- Keep an ad if cost per sale is ≤ $20. Scale it (+20% every 3 days) if ≤ $14.
- Never raise the total ad budget while the reserve is under $100.

**Organic**
- A video that keeps viewers 40%+ of the way through or gets 2%+ shares is a winner: make 3 versions of it and run it as an ad.

**Product**
- Week 3 review: if 3 rounds of new videos and one page rewrite still give cost per sale over $30, switch hero to alternate #1. The brand and site stay the same; only `lib/product.js` changes.

**Supplier**
- More than 3% of orders late (over 7 business days) or more than 2% defective → open a backup supplier the same week.

**Cash**
- CJ wallet below $40 → top it up from Stripe payouts before anything else.

---

## 5. Content engine (the real sales driver)

**Volume:** 2–3 TikToks + 1 Reel per day in weeks 1–4. Faceless and AI clips build reach. Real footage (CJ media + your test unit) is the only footage that shows the product working. No fake "customer" videos, no fake reviews, no fake scarcity.

**Hooks to rotate:**
1. "POV: your indoor cat finally gets to hunt" (slow reel-in, pounce)
2. "My cat ignored every toy until this" (honest only if true for the test unit's cat; otherwise phrase it as a question)
3. "10 minutes a night = calm cat" → show the routine (no health claims)
4. "Why a reel? Prey that escapes is what cats chase", a 3-second explainer
5. "Couch-potato owner, athlete cat": the telescopic rod lets you play sitting down
6. Before/after energy: chaos at 9 pm vs. a snoozing cat after a 10-minute hunt
7. Duet/stitch trending cat videos with "they need a hunt, not a laser"

**Every video ends with:** "Comment LINK and I'll send it" (comment-to-DM).

**Weekly:**
- Claude reads the numbers.
- Keep the top 20% of hooks, drop the bottom 50%.
- Make new versions of the winners.

---

## 6. Who does what, every week after launch

| | Claude | You |
|---|---|---|
| Daily | Content batch, comment-reply drafts, ad checks against §4 rules, order/fulfilment check (failed CJ orders alert you) | Post the day's videos (~15 min), approve anything that spends money |
| Weekly | Report: revenue, profit, cost per sale, best/worst content, next experiment. Restock CJ wallet reminder | 30-min review, approve next week's experiment |
| Monthly | Unit-economics update, product-line decision, supplier check | Bookkeeping, taxes set-aside (≈25% of profit), payouts |

Claude can't create accounts, pass ID checks, pay, or press "spend" without you. Those stay yours.

---

## 7. Your repo list: what gets used, and when

Only ★ (verified) entries are used. ◐ and SaaS-only entries are skipped, as you asked.

| When | Repo (list #) | Used for |
|---|---|---|
| Now | #17 OpenSIN-Code/cj-dropshipping-skill (installed) | CJ product search, freight, order checks |
| Now | #19 dcam9586/scout-source2 | CJ API reference; used to harden `lib/cj.js` (pay-step check, cheapest ≤5-day US shipping) |
| Now | #161 AgriciDaniel/claude-ads, #170 coreyhaines31/marketingskills (installed) | Ad audits, hooks, landing-page CRO, email copy |
| Now | #172 nexscope-ai/eCommerce-Skills (installed earlier) | Pricing, email flows, TikTok Shop playbooks |
| Stage 1–2 | #144 resend/resend-node, #145 react-email | Nicer transactional and flow emails |
| Stage 2 | #140 ecomm-ai-skills-hub (shipment-tracking) | Better tracking pages / delay alerts |
| Stage 3 | #52 Medusa dtc-starter (installed), #1 Sparx adapter pattern (installed) | Multi-product store, one adapter per supplier |
| Stage 3 | #119 TikTok-Shop-Api-SDKs, #97/#120 tiktok-shop-mcp | TikTok Shop listing + affiliates |
| Stage 3 | #2 MarketOS (installed) | Product discovery and margin model for products 2–3 |
| Stage 4 | #99 Hyperswitch (installed) | Second processor / payment routing at volume |
| Stage 4–5 | #10 3dsellers/ebay-mcp-server | One catalogue → Amazon / Walmart / eBay / Etsy |
| Any time | #5 LaimaWu/anythingmcp | Turn any supplier API into tools Claude can use |
| Any time | #90 changedetection.io | Watch competitor prices and stock |

Setup for the installed stack: `store-stack/setup.sh` (re-creates it on any machine).

---

## 8. Risks and what we do about them

| Risk | Prevention / response |
|---|---|
| No sales in week 1 | Expected for many new stores. Read the funnel; fix the single weakest step; product switch at week 3 if rules say so |
| Poor product quality | Test unit; 30-day guarantee; backup supplier lined up in week 2 |
| Stripe account hold | US warehouse, clear policies, tracking emails, fast refunds, honest copy |
| Ad account rejection | No health/"calming" claims, no fake urgency; run `dropship-ad-compliance` before each launch |
| IP / patent complaint | Reel rod skipped unless cleared (US 10,271,519). Never use "Caster" names (KITTY CASTER is a registered mark). Own name and images only; check every listing for patent marks |
| Cash crunch | Reserve ≥ $100 rule; ads scale only from profit |
| Burnout / time | Owner tasks capped at ~10 h/week; everything else Claude |
