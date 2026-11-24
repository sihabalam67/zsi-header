# Indoor Hunt Co.: automated dropshipping store

A one-product store with no Shopify. A paid order flows through it like this:

```
Customer pays (Stripe Checkout)
   → Stripe webhook  /api/stripe-webhook
   → order placed at CJ Dropshipping (US warehouse), paid from CJ wallet
   → confirmation email (Resend)
Once a day: Vercel cron  /api/cron/sync-tracking (Hobby plan allows daily; Pro allows hourly)
   → retries paying CJ for orders that waited on wallet balance
   → reads CJ order status → emails tracking number to the customer
If a supplier order fails → OWNER_EMAIL gets an "ACTION NEEDED" alert
```

There's no database. Each order's state lives in the Stripe PaymentIntent's metadata
(`fulfillment: pending | placed | shipped | error`, `cj_order_id`, `tracking`).

## Change the product or offer
Everything lives in `lib/product.js`: brand, product copy, bundle prices, free-shipping threshold and the upsell.
Stripe prices are created automatically from these values on the first checkout.

## Accounts the owner must create (need real identity)
1. **Stripe** (stripe.com): account verification, bank payouts. Copy the secret key.
   Add a webhook to `https://YOUR-DOMAIN/api/stripe-webhook` for `checkout.session.completed`
   and copy its signing secret.
2. **CJ Dropshipping** (cjdropshipping.com): free. Fund the wallet (start with about $60). Generate an API key.
   Find the fishing-rod toy **in the US warehouse** and copy its variant ID (`vid`) into `CJ_VID_WAND`.
3. **Resend** (resend.com): free tier. Verify the domain and copy the API key.
4. **Domain**: about $15/yr. Point it at Vercel.

Then set every variable from `.env.example` in Vercel. Deploy with root directory = `store`.

## Before going live: test one order end to end
Use Stripe test mode with card `4242 4242 4242 4242`. Check that an order appears in CJ.
Use `CJ_PAY_TYPE` that does not auto-pay while testing, then cancel the test order in CJ.
The CJ API field names in `lib/cj.js` follow CJ's v2 docs. Re-check them against the live docs when you connect the account.

## Local development
```
npm install
cp .env.example .env.local   # fill in test keys
npm run dev
```
