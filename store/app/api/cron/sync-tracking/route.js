import { NextResponse } from 'next/server';
import { stripe } from '@/lib/stripe';
import { retryPayment, syncTracking } from '@/lib/fulfill';

// Runs on a Vercel cron schedule (see vercel.json).
// 1. Retries paying CJ for orders that waited on wallet balance.
// 2. Emails tracking numbers for orders that have shipped.
export async function GET(req) {
  if (req.headers.get('authorization') !== `Bearer ${process.env.CRON_SECRET}`) {
    return NextResponse.json({ error: 'unauthorized' }, { status: 401 });
  }
  const results = [];

  const unpaid = await stripe().paymentIntents.search({ query: "metadata['fulfillment']:'unpaid'", limit: 100 });
  for (const pi of unpaid.data) {
    try {
      results.push({ pi: pi.id, paidNow: await retryPayment(pi) });
    } catch (err) {
      results.push({ pi: pi.id, error: err.message });
    }
  }

  const placed = await stripe().paymentIntents.search({ query: "metadata['fulfillment']:'placed'", limit: 100 });
  for (const pi of placed.data) {
    try {
      results.push({ pi: pi.id, ...(await syncTracking(pi)) });
    } catch (err) {
      results.push({ pi: pi.id, error: err.message });
    }
  }
  return NextResponse.json({ checked: results.length, results });
}
