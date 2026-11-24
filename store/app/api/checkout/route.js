import { NextResponse } from 'next/server';
import { stripe, ensurePrices, priceKey } from '@/lib/stripe';
import { getProduct, getBundle, cjVid, UPSELL, FREE_SHIPPING_THRESHOLD, STANDARD_SHIPPING, CURRENCY } from '@/lib/product';

// Body: { items: [{ slug, bundle, qty }] }. Prices always come from the server
// catalog, never from the browser.
export async function POST(req) {
  let body;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: 'Bad request' }, { status: 400 });
  }

  const lines = [];
  for (const it of Array.isArray(body?.items) ? body.items.slice(0, 20) : []) {
    const product = getProduct(it.slug);
    const bundle = getBundle(product, it.bundle);
    const qty = Math.min(Math.max(parseInt(it.qty, 10) || 1, 1), 10);
    if (!product || !bundle) return NextResponse.json({ error: 'Unknown item in cart' }, { status: 400 });
    if (!cjVid(product)) {
      return NextResponse.json({ error: `${product.name} isn’t available yet. Please remove it and try again.` }, { status: 409 });
    }
    lines.push({ product, bundle, qty });
  }
  if (!lines.length) return NextResponse.json({ error: 'Your cart is empty' }, { status: 400 });

  try {
    const prices = await ensurePrices();
    const origin = process.env.SITE_URL || req.nextUrl.origin;
    const subtotal = lines.reduce((s, l) => s + l.bundle.price * l.qty, 0);
    const freeShipping = subtotal >= FREE_SHIPPING_THRESHOLD;
    const offerUpsell = UPSELL && cjVid(UPSELL) && !lines.some((l) => l.product.slug === UPSELL.slug);

    const session = await stripe().checkout.sessions.create({
      mode: 'payment',
      line_items: lines.map((l) => ({ price: prices[priceKey(l.product.slug, l.bundle.id)], quantity: l.qty })),
      ...(offerUpsell && {
        optional_items: [{ price: prices[priceKey(UPSELL.slug, UPSELL.bundles[0].id)], quantity: 1, adjustable_quantity: { enabled: true, maximum: 3 } }],
      }),
      shipping_address_collection: { allowed_countries: ['US'] },
      phone_number_collection: { enabled: true },
      shipping_options: [
        {
          shipping_rate_data: {
            type: 'fixed_amount',
            display_name: freeShipping ? 'Free US shipping' : 'Standard US shipping',
            fixed_amount: { amount: freeShipping ? 0 : STANDARD_SHIPPING, currency: CURRENCY },
            delivery_estimate: { minimum: { unit: 'business_day', value: 5 }, maximum: { unit: 'business_day', value: 7 } },
          },
        },
      ],
      payment_intent_data: { metadata: { fulfillment: 'pending' } },
      success_url: `${origin}/success?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${origin}/cart`,
    });
    return NextResponse.json({ url: session.url });
  } catch (err) {
    console.error('Checkout failed', err);
    return NextResponse.json({ error: 'Checkout is temporarily unavailable. Please try again shortly.' }, { status: 503 });
  }
}
