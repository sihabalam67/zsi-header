import { NextResponse } from 'next/server';
import { stripe } from '@/lib/stripe';
import { createOrder } from '@/lib/cj';
import { sendEmail } from '@/lib/email';
import { CJ_VARIANTS, UPSELL, PRODUCT, BRAND } from '@/lib/product';

// Stripe → CJ: when a checkout is paid, place the order at the supplier.
// The PaymentIntent's metadata is the order record (no database needed):
//   fulfillment: pending | placed | shipped | error
//   cj_order_id, tracking
export async function POST(req) {
  const sig = req.headers.get('stripe-signature');
  const raw = await req.text();
  let event;
  try {
    event = stripe().webhooks.constructEvent(raw, sig, process.env.STRIPE_WEBHOOK_SECRET);
  } catch (err) {
    return NextResponse.json({ error: `Bad signature: ${err.message}` }, { status: 400 });
  }

  if (event.type !== 'checkout.session.completed') return NextResponse.json({ ok: true });

  const session = await stripe().checkout.sessions.retrieve(event.data.object.id, {
    expand: ['line_items.data.price', 'payment_intent'],
  });
  const pi = session.payment_intent;
  if (session.payment_status !== 'paid' || !pi) return NextResponse.json({ ok: true });
  if (pi.metadata?.cj_order_id) return NextResponse.json({ ok: true, duplicate: true });

  // Translate what was bought into supplier units.
  let wands = 0;
  let refills = 0;
  for (const li of session.line_items.data) {
    const offerId = li.price.metadata?.offer_id;
    if (offerId === UPSELL.id) refills += li.quantity;
    else wands += Number(li.price.metadata?.units || 0) * li.quantity;
  }
  const items = [];
  if (wands) items.push({ vid: CJ_VARIANTS.wand, quantity: wands });
  if (refills) items.push({ vid: CJ_VARIANTS.refill, quantity: refills });

  const ship = session.collected_information?.shipping_details || session.shipping_details;
  const email = session.customer_details?.email;

  try {
    const cjOrderId = await createOrder({
      orderNumber: session.id,
      address: ship.address,
      name: ship.name,
      phone: session.customer_details?.phone,
      email,
      items,
    });
    await stripe().paymentIntents.update(pi.id, {
      metadata: { fulfillment: 'placed', cj_order_id: String(cjOrderId) },
    });
    await sendEmail({
      to: email,
      subject: `Your ${PRODUCT.name} order is confirmed`,
      text: `Thanks for your order from ${BRAND.name}!\n\nIt ships from our US warehouse and usually arrives in 5–7 business days. We'll email your tracking number as soon as it ships.`,
    });
  } catch (err) {
    console.error('CJ order failed', err);
    await stripe().paymentIntents.update(pi.id, {
      metadata: { fulfillment: 'error', fulfillment_error: String(err.message).slice(0, 450) },
    });
    // Alert the owner so a human can place it by hand.
    if (process.env.OWNER_EMAIL) {
      await sendEmail({
        to: process.env.OWNER_EMAIL,
        subject: `ACTION NEEDED: supplier order failed for ${session.id}`,
        text: `Automatic CJ order failed: ${err.message}\nStripe payment: ${pi.id}\nShip to: ${ship?.name}, ${JSON.stringify(ship?.address)}\nItems: ${JSON.stringify(items)}`,
      });
    }
  }
  return NextResponse.json({ ok: true });
}
