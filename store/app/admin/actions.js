'use server';

import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';
import { revalidatePath } from 'next/cache';
import { COOKIE, checkPassword, createSessionToken, verifySessionToken } from '@/lib/auth';
import { stripe } from '@/lib/stripe';
import { loadSession, fulfillSession, retryPayment, syncTracking } from '@/lib/fulfill';
import { abs, SITE_URL } from '@/lib/site';
import { GUIDES } from '@/lib/guides';

async function requireAdmin() {
  const jar = await cookies();
  if (!(await verifySessionToken(jar.get(COOKIE)?.value))) redirect('/admin/login');
}

export async function login(_prev, formData) {
  if (!process.env.ADMIN_PASSWORD) return { error: 'Set ADMIN_PASSWORD in Vercel first.' };
  if (!(await checkPassword(String(formData.get('password') || '')))) {
    await new Promise((r) => setTimeout(r, 800)); // slow down guessing
    return { error: 'Wrong password.' };
  }
  const { token, maxAge } = await createSessionToken();
  (await cookies()).set(COOKIE, token, { httpOnly: true, secure: true, sameSite: 'lax', path: '/', maxAge });
  redirect('/admin');
}

export async function logout() {
  (await cookies()).delete(COOKIE);
  redirect('/admin/login');
}

async function orderAction(sessionId, fn) {
  await requireAdmin();
  let message;
  try {
    message = await fn(await loadSession(sessionId));
  } catch (err) {
    message = `Failed: ${err.message}`;
  }
  revalidatePath(`/admin/orders/${sessionId}`);
  redirect(`/admin/orders/${sessionId}?msg=${encodeURIComponent(message)}`);
}

export async function retryFulfillment(formData) {
  const id = String(formData.get('id'));
  await orderAction(id, async (session) => {
    const pi = session.payment_intent;
    if (pi.metadata?.fulfillment === 'error') {
      // Clear the failed attempt so fulfillSession runs again.
      await stripe().paymentIntents.update(pi.id, { metadata: { cj_order_id: '' } });
      session.payment_intent.metadata.cj_order_id = '';
    }
    const r = await fulfillSession(session, { notifyCustomer: false });
    if (r.error) return `Supplier order failed again: ${r.error}`;
    if (r.skipped) return `Nothing to do (${r.skipped}).`;
    return r.paid ? `Supplier order placed and paid (CJ ${r.cjOrderId}).` : `Supplier order placed (CJ ${r.cjOrderId}) but not paid: top up the CJ wallet.`;
  });
}

export async function retryCjPayment(formData) {
  const id = String(formData.get('id'));
  await orderAction(id, async (session) =>
    (await retryPayment(session.payment_intent)) ? 'CJ order paid.' : 'Still unpaid: CJ wallet balance is too low.'
  );
}

export async function checkTracking(formData) {
  const id = String(formData.get('id'));
  const force = formData.get('force') === '1';
  await orderAction(id, async (session) => {
    const r = await syncTracking(session.payment_intent, { force });
    if (!r.tracking) return `No tracking yet (CJ status: ${r.status}).`;
    return r.emailed === false ? `Tracking ${r.tracking} saved (no customer email found).` : `Tracking ${r.tracking} emailed to the customer.`;
  });
}

// Tells Bing (and other IndexNow engines) that pages changed. Bing's index
// also powers ChatGPT search and Copilot.
export async function notifySearchEngines() {
  await requireAdmin();
  const key = process.env.INDEXNOW_KEY;
  let msg;
  if (!key) {
    msg = 'Set INDEXNOW_KEY in Vercel first.';
  } else {
    const urlList = ['/', '/guides', '/faq', '/about', ...GUIDES.map((g) => `/guides/${g.slug}`)].map(abs);
    const res = await fetch('https://api.indexnow.org/indexnow', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json; charset=utf-8' },
      body: JSON.stringify({ host: new URL(SITE_URL).host, key, keyLocation: abs('/indexnow.txt'), urlList }),
    });
    msg = res.ok ? `Sent ${urlList.length} pages to IndexNow (status ${res.status}).` : `IndexNow returned ${res.status}.`;
  }
  redirect(`/admin?msg=${encodeURIComponent(msg)}`);
}
