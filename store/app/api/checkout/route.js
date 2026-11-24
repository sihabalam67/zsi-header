import { NextResponse } from 'next/server';
import { stripe, ensurePrices } from '@/lib/stripe';
import { getOffer, FREE_SHIPPING_THRESHOLD, STANDARD_SHIPPING, CURRENCY, UPSELL } from '@/lib/product';

export async function POST(req) {
  try {
    return await createSession(req);
  } catch (err) {
    console.error('Checkout failed', err);
    return NextResponse.json({ error: 'Checkout is temporarily unavailable. Please try again shortly.' }, { status: 503 });
  }
}

async function createSession(req) {
  const { offerId } = await req.json();
  const offer = getOffer(offerId);
  if (!offer) return NextResponse.json({ error: 'Unknown offer' }, { status: 400 });

  const prices = await ensurePrices();
  const origin = process.env.SITE_URL || req.nextUrl.origin;
  const freeShipping = offer.price >= FREE_SHIPPING_THRESHOLD;

  const session = await stripe().checkout.sessions.create({
    mode: 'payment',
    line_items: [{ price: prices[offer.id], quantity: 1 }],
    optional_items: [
      { price: prices[UPSELL.id], quantity: 1, adjustable_quantity: { enabled: true, maximum: 3 } },
    ],
    shipping_address_collection: { allowed_countries: ['US'] },
    phone_number_collection: { enabled: true },
    shipping_options: [
      {
        shipping_rate_data: {
          type: 'fixed_amount',
          display_name: freeShipping ? 'Free US shipping' : 'Standard US shipping',
          fixed_amount: { amount: freeShipping ? 0 : STANDARD_SHIPPING, currency: CURRENCY },
          delivery_estimate: {
            minimum: { unit: 'business_day', value: 5 },
            maximum: { unit: 'business_day', value: 7 },
          },
        },
      },
    ],
    payment_intent_data: { metadata: { offer_id: offer.id, fulfillment: 'pending' } },
    metadata: { offer_id: offer.id },
    success_url: `${origin}/success?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${origin}/`,
  });

  return NextResponse.json({ url: session.url });
}
