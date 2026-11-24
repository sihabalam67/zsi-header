import { NextResponse } from 'next/server';
import { stripe } from '@/lib/stripe';
import { loadSession, fulfillSession } from '@/lib/fulfill';

// Stripe → CJ: when a checkout is paid, place the order at the supplier.
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

  const session = await loadSession(event.data.object.id);
  const result = await fulfillSession(session);
  return NextResponse.json({ ok: true, ...result });
}
