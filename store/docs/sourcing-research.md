# Sourcing research: telescopic fishing-rod cat toy with working reel + interchangeable lures

Date: 2026-11-24. Research only: no accounts, purchases or emails. Method: web search, plus page fetches where sites allowed them.
Legend: **[V]** = verified on the page or in a search snippet · **[U]** = unverified, inferred or stale

---

## 1. CJ Dropshipping: NOT VERIFIED (blocked)

- Every request to `cjdropshipping.com/search/...` redirects to `frontend.cjdropshipping.com/egg/cj/validation.html`, a "Human verification" captcha page **[V]**. No product content can be read without a browser session.
- Search engines do not index CJ product pages for this item. Queries for "cat fishing rod toy reel", "telescopic cat teaser wand reel" and "retractable cat fishing pole" (with and without site:cjdropshipping.com) returned **zero** CJ URLs **[V]**.
- A `cj-dropshipping` skill is installed in this environment. It uses a cached API token that belongs to a different account ("OpenSIN"/ShopSIN, EU-focused), and its notes say the token expires 2026-11-24, which is today. **I did not use it**, because the brief says no accounts and the credentials are not this store's.
- **Result:** I have no CJ URL, SKU/PID, price, US-warehouse flag, processing time, weight, variant or refill-pack data. All of it is **[U]**.
- **How to finish this step (needs a human or the store's own CJ account):** log in to CJ, search the three terms, and filter Warehouse = US. Or call the CJ API with the store's own token: `GET /api2.0/v1/product/list?productNameEn=cat fishing rod&countryCode=US`, then `product/query?pid=` for weight and variants, then `product/stock/queryByVid` to check US stock. Record processing time plus US-domestic shipping (CJ advertises roughly 2–5 day US-warehouse delivery **[U, from general knowledge, not checked today]**). Many China-origin versions exist (eBay listing 236740021530 says "3 Replacement Lures", origin China **[V]**), so a CN-only CJ listing is likely. A US-stock listing is **not confirmed**.

## 2. Backup sources (US warehouse, no MOQ, API/CSV)

None of these is confirmed to carry a **reel** version that **ships from the US** with **no MOQ**. The best leads:

| Option | What was found | Gaps / caveats |
|---|---|---|
| **Syncee** (supplier "Dog Hugs Cat") | Telescopic cat-toy sets incl. "telescopic rod*1, fishing line*1, replacement head*6" e.g. https://syncee.com/product/394443_77761_6925843923027/feather-frenzy-telescopic-cat-toy-set **[V snippet]** | Product page fetch returned the homepage. The ship-from country is **not shown** **[U]**, and the listing likely has **no reel**. Syncee has a US-supplier filter plus Shopify app/CSV. |
| **Faire**: Whiskers 'n Paws | Telescopic pole 70"→21", pole + line + 1 lure, MSRP $20: https://www.faire.com/product/p_qgu6ycxb45. Separate lure refills (Max Lure, MSRP $5.50): https://www.faire.com/product/p_wng3var3te **[V snippet]** | **No reel.** Faire is wholesale with brand minimums (about $100–250 seen on comparable listings **[V]**), so it is **not no-MOQ and not a dropship model**. It could still be a refill-lure source. |
| **Branded US distributors (SPOT / Ethical Pet "Fishing Rod 'N Reel Kitty Teaser")** | The closest real "rod + reel + replaceable lure" product, sold widely at US retail. Chewy: https://www.chewy.com/ethical-pet-fishing-rod-reel-kitty/dp/215873 (snippet: 3.8★, 224 ratings, ~$12.66) **[V snippet; page 429 on fetch]** | Need a dropship distributor (Doba/Wholesale2B-type) that lists it. **Not found** on Doba or Wholesale2B via web search **[U]**, so check inside the catalogs. Branded resale may come with MAP pricing. |
| **Doba / Wholesale2B** | Only general mentions that they carry pet/fishing categories (EPROLO blog: https://eprolo.com/uk/dropship-fishing-gear) **[V]** | No matching SKU found. The catalogs are behind login **[U]**. |

## 3. Patent / trademark facts (no legal conclusions)

- **"Cat Caster"** is sold under the **Kid Casters** brand (photo credit in https://www.wideopencountry.com/cat-caster/). Specs: rod 29" extended / 17" retracted, 80 ft line, 2 teaser toys **[V]**. Retailer page: https://profishiency.com/products/kid-casters-cat-caster-fishing-pole ($13.50 sale / $16.87 regular, out of stock, 1 soft teaser + 2 plastic fish, copy says **"patented TANGLE FREE design"** with **no patent number**) **[V]**. The tangle-free feature is described as line fed through the center of the shaft (Ace/Canadian Tire copy) **[V]**.
- Trademarks found: **KID CASTERS** registrations, e.g. Reg. 4939450 / SN 86684970 (Class 28) https://trademark.justia.com/866/84/kid-86684970.html, and SN 86903747 https://trademarkdir.com/trademark/kid-casters-86903747 **[V snippet]**. **No "CAT CASTER" exact-mark record** came up on Justia search **[V for search, not exhaustive]**. **"KITTY CASTER"** is registered and renewed, SN 77494540: https://trademark.justia.com/774/94/kitty-77494540.html. Hartz sells a "Just Cats Kitty Caster" toy: https://hartz.com/product/hartz-just-cats-kitty-caster-cat-toy **[V]**. Avoid "Caster"-based names in product titles.
- Related patents seen:
  - **US 10,271,519 "Pet toy caster"** (issued 2019-04-30): claims a reel mounted on a rod for casting/reeling a line with a pet toy. https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10271519 **[V snippet]**. I did not check whether it is still in force (maintenance fees) **[U]**.
  - **US 6,314,913 "Reelable cat toy"** (2001): https://patents.google.com/patent/US6314913. Its 20-year term would normally have ended around 2019–2020 **[U, computed]**.
  - US 8,997,695 (casting pet toy, stretchable cord), cited as prior art **[V snippet]**.
- **Market saturation:** many unrelated sellers sell reel-style cat rods at US retail: SPOT/Ethical Pet (Chewy, PetSupermarket, Jeffers, Ace, Farm & Fleet), Mad Cat (PetSmart), Hartz, BESTSKY/Yirtree/Rechale (Walmart), plus many eBay CN listings **[V]**. This is a fact pattern only, not a freedom-to-operate opinion. US 10,271,519 is the one to have reviewed.

## 4. Competitor price check (target retail $24.99)

| Listing | Price | Reviews | Reel? | Source |
|---|---|---|---|---|
| Ethical Pet/SPOT Fishing Rod & Reel (Chewy) | ~$12.66 | 224 ratings, 3.8★ | Yes | https://www.chewy.com/ethical-pet-fishing-rod-reel-kitty/dp/215873 **[V snippet]** |
| Yirtree cat fishing pole (Walmart) | ~$10.49 | 112 reviews (another Yirtree listing: 9 ratings, 4.0★) | Yes (per listing title) | https://www.walmart.com/ip/2412575255 **[V snippet; exact listing↔count mapping U]** |
| ZEZE telescopic rod + 3 minnows (Target, 3P seller Safety Pet Supplies) | $19.99 (reg. $28.56) | 2 reviews, 5★ | No reel mentioned | https://www.target.com/p/zeze-telescopic-fishing-rod-fishing-cat-toy-blue/-/A-1006120639 **[V fetched]** |
| Kid Casters Cat Caster (Amazon/retail) | $16.87 regular; $34.99 (was $41.99) in a SheKnows article | Amazon count not found; ~4/5 per article | Yes, 80 ft line | https://profishiency.com/products/kid-casters-cat-caster-fishing-pole, https://www.sheknows.com/living/articles/2788604/fishing-pole-cat-toy/ **[V, prices dated]** |

**Read:** reel cat rods mostly sell for **$10–$20**. Only the viral Cat Caster has been seen at $35. At **$24.99**, a generic version sits above most mass listings and needs a bundle (extra lures or a refill pack) or brand positioning to justify the price. No Amazon review counts were captured (Amazon wasn't reached) **[U]**. No TikTok Shop data was captured.

## Open items
1. CJ US-warehouse listing: needs a logged-in CJ search or the store's own API token.
2. Whether US 10,271,519 is in force, and whether its claims cover the chosen SKU (counsel).
3. A dropship (not wholesale) source for SPOT/Ethical Pet reel teaser inside Doba/Wholesale2B catalogs.
