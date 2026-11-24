import { stripe } from './stripe';
import { getBalance } from './cj';
import { PRODUCT } from './product';

// Everything the admin dashboard shows, read live from Stripe and CJ.

export async function recentOrders(days = 30) {
  const since = Math.floor(Date.now() / 1000) - days * 86400;
  const orders = [];
  let starting_after;
  for (let page = 0; page < 5; page++) {
    const res = await stripe().checkout.sessions.list({
      created: { gte: since },
      limit: 100,
      expand: ['data.payment_intent'],
      ...(starting_after && { starting_after }),
    });
    for (const s of res.data) {
      if (s.payment_status !== 'paid') continue;
      const pi = s.payment_intent;
      orders.push({
        id: s.id,
        created: s.created * 1000,
        email: s.customer_details?.email || '',
        name: s.customer_details?.name || '',
        amount: s.amount_total,
        piId: pi?.id,
        fulfillment: pi?.metadata?.fulfillment || 'pending',
        cjOrderId: pi?.metadata?.cj_order_id || '',
        tracking: pi?.metadata?.tracking || '',
        error: pi?.metadata?.fulfillment_error || '',
      });
    }
    if (!res.has_more) break;
    starting_after = res.data[res.data.length - 1].id;
  }
  return orders;
}

export function summarize(orders) {
  const now = Date.now();
  const window = (days) => {
    const list = orders.filter((o) => o.created >= now - days * 86400000);
    const revenue = list.reduce((s, o) => s + (o.amount || 0), 0);
    return { count: list.length, revenue, aov: list.length ? Math.round(revenue / list.length) : 0 };
  };
  const needsAction = orders.filter((o) => ['error', 'unpaid', 'pending'].includes(o.fulfillment));
  return { today: window(1), week: window(7), month: window(30), needsAction };
}

export async function cjBalance() {
  if (!process.env.CJ_API_KEY) return { configured: false };
  try {
    const b = await getBalance();
    return { configured: true, amount: Number(b?.amount ?? 0), frozen: Number(b?.frozenAmount ?? 0) };
  } catch (err) {
    return { configured: true, error: err.message };
  }
}

// Launch-readiness checklist: what's configured and what's still missing.
export function readiness() {
  const env = (k) => Boolean(process.env[k]);
  const live = (process.env.STRIPE_SECRET_KEY || '').startsWith('sk_live_');
  return [
    { group: 'Payments', label: 'Stripe secret key', ok: env('STRIPE_SECRET_KEY'), note: env('STRIPE_SECRET_KEY') ? (live ? 'Live mode' : 'Test mode') : 'STRIPE_SECRET_KEY' },
    { group: 'Payments', label: 'Stripe webhook signing secret', ok: env('STRIPE_WEBHOOK_SECRET'), note: 'STRIPE_WEBHOOK_SECRET' },
    { group: 'Supplier', label: 'CJ API key', ok: env('CJ_API_KEY'), note: 'CJ_API_KEY' },
    { group: 'Supplier', label: 'CJ product variant ID', ok: env('CJ_VID_WAND'), note: 'CJ_VID_WAND' },
    { group: 'Supplier', label: 'CJ add-on variant ID', ok: env('CJ_VID_REFILL'), note: 'CJ_VID_REFILL' },
    { group: 'Supplier', label: 'Real product photos', ok: !PRODUCT.images.some((i) => i.includes('placeholder')), note: 'lib/product.js images' },
    { group: 'Email', label: 'Resend API key', ok: env('RESEND_API_KEY'), note: 'RESEND_API_KEY' },
    { group: 'Email', label: 'Your alert email', ok: env('OWNER_EMAIL'), note: 'OWNER_EMAIL' },
    { group: 'Email', label: 'Support email', ok: env('SUPPORT_EMAIL'), note: 'SUPPORT_EMAIL' },
    { group: 'Legal', label: 'Business mailing address', ok: env('BUSINESS_ADDRESS'), note: 'BUSINESS_ADDRESS' },
    { group: 'Site', label: 'Domain set as site URL', ok: env('SITE_URL'), note: 'SITE_URL' },
    { group: 'Site', label: 'Daily job secret', ok: env('CRON_SECRET'), note: 'CRON_SECRET' },
    { group: 'Search', label: 'Google Search Console verified', ok: env('GOOGLE_SITE_VERIFICATION'), note: 'GOOGLE_SITE_VERIFICATION' },
    { group: 'Search', label: 'Bing Webmaster verified', ok: env('BING_SITE_VERIFICATION'), note: 'BING_SITE_VERIFICATION' },
    { group: 'Search', label: 'IndexNow key', ok: env('INDEXNOW_KEY'), note: 'INDEXNOW_KEY' },
    { group: 'Social', label: 'Instagram profile URL', ok: env('SOCIAL_INSTAGRAM'), note: 'SOCIAL_INSTAGRAM' },
    { group: 'Social', label: 'TikTok profile URL', ok: env('SOCIAL_TIKTOK'), note: 'SOCIAL_TIKTOK' },
  ];
}
