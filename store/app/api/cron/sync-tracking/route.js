import { NextResponse } from 'next/server';
import { stripe } from '@/lib/stripe';
import { getOrder } from '@/lib/cj';
import { sendEmail } from '@/lib/email';
import { PRODUCT } from '@/lib/product';

// Runs on a Vercel cron schedule (see vercel.json). For every order placed at
// CJ that hasn't shipped yet, check for a tracking number and email it.
export async function GET(req) {
  if (req.headers.get('authorization') !== `Bearer ${process.env.CRON_SECRET}`) {
    return NextResponse.json({ error: 'unauthorized' }, { status: 401 });
  }

  const pending = await stripe().paymentIntents.search({
    query: "metadata['fulfillment']:'placed'",
    limit: 100,
  });

  const results = [];
  for (const pi of pending.data) {
    try {
      const order = await getOrder(pi.metadata.cj_order_id);
      const tracking = order.trackNumber;
      if (!tracking) {
        results.push({ pi: pi.id, status: order.orderStatus });
        continue;
      }
      const link = `https://parcelsapp.com/en/tracking/${encodeURIComponent(tracking)}`;
      const email = pi.receipt_email || (await customerEmail(pi));
      if (email) {
        await sendEmail({
          to: email,
          subject: `Your ${PRODUCT.name} has shipped`,
          text: `Good news: your order is on its way.\n\nTracking number: ${tracking}\nTrack it here: ${link}`,
        });
      }
      await stripe().paymentIntents.update(pi.id, {
        metadata: { fulfillment: 'shipped', tracking },
      });
      results.push({ pi: pi.id, shipped: tracking });
    } catch (err) {
      results.push({ pi: pi.id, error: err.message });
    }
  }
  return NextResponse.json({ checked: results.length, results });
}

async function customerEmail(pi) {
  const sessions = await stripe().checkout.sessions.list({ payment_intent: pi.id, limit: 1 });
  return sessions.data[0]?.customer_details?.email;
}
