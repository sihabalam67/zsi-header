import { stripe } from './stripe';
import { createOrder, ensurePaid, getOrder } from './cj';
import { sendEmail } from './email';
import { CJ_VARIANTS, UPSELL, PRODUCT, BRAND } from './product';

// Order state lives in the Stripe PaymentIntent's metadata (no database):
//   fulfillment: pending | placed | unpaid | shipped | error
//   cj_order_id, tracking, fulfillment_error

export async function loadSession(sessionId) {
  return stripe().checkout.sessions.retrieve(sessionId, {
    expand: ['line_items.data.price', 'payment_intent'],
  });
}

export async function sessionForPaymentIntent(piId) {
  const list = await stripe().checkout.sessions.list({ payment_intent: piId, limit: 1 });
  return list.data[0] ? loadSession(list.data[0].id) : null;
}

// What the customer bought, translated into supplier units.
export function supplierItems(session) {
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
  return items;
}

export function shippingOf(session) {
  return session.collected_information?.shipping_details || session.shipping_details;
}

// Places the supplier order for a paid Checkout Session. Safe to call twice:
// it does nothing if a CJ order already exists for this payment.
export async function fulfillSession(session, { notifyCustomer = true } = {}) {
  const pi = session.payment_intent;
  if (session.payment_status !== 'paid' || !pi) return { skipped: 'not paid' };
  if (pi.metadata?.cj_order_id) return { skipped: 'already placed', cjOrderId: pi.metadata.cj_order_id };

  const items = supplierItems(session);
  const ship = shippingOf(session);
  const email = session.customer_details?.email;

  try {
    const { orderId, paid } = await createOrder({
      orderNumber: session.id,
      address: ship.address,
      name: ship.name,
      phone: session.customer_details?.phone,
      email,
      items,
    });
    await stripe().paymentIntents.update(pi.id, {
      metadata: { fulfillment: paid ? 'placed' : 'unpaid', cj_order_id: String(orderId), fulfillment_error: '' },
    });
    if (notifyCustomer) {
      await sendEmail({
        to: email,
        subject: `Your ${PRODUCT.name} order is confirmed`,
        text: `Thanks for your order from ${BRAND.name}!\n\nIt ships from our US warehouse and usually arrives in 5–7 business days. We'll email your tracking number as soon as it ships.`,
      });
    }
    if (!paid) {
      await alertOwner(
        `New order: top up your CJ wallet to ship it`,
        `A customer paid and the order is waiting at CJ (order ${orderId}), but the CJ wallet balance is too low to pay for it.\n\nAdd funds at https://cjdropshipping.com (My CJ → Wallet). The store retries the payment automatically on its next daily check, or press "Retry CJ payment" in your admin dashboard.`
      );
    }
    return { cjOrderId: orderId, paid };
  } catch (err) {
    console.error('CJ order failed', err);
    await stripe().paymentIntents.update(pi.id, {
      metadata: { fulfillment: 'error', fulfillment_error: String(err.message).slice(0, 450) },
    });
    await alertOwner(
      `ACTION NEEDED: supplier order failed for ${session.id}`,
      `Automatic CJ order failed: ${err.message}\nStripe payment: ${pi.id}\nShip to: ${ship?.name}, ${JSON.stringify(ship?.address)}\nItems: ${JSON.stringify(items)}\n\nOpen your admin dashboard and press "Retry supplier order", or place it by hand in CJ.`
    );
    return { error: err.message };
  }
}

export async function retryPayment(pi) {
  if (!pi.metadata?.cj_order_id) throw new Error('No CJ order on this payment yet');
  const paid = await ensurePaid(pi.metadata.cj_order_id);
  if (paid) await stripe().paymentIntents.update(pi.id, { metadata: { fulfillment: 'placed' } });
  return paid;
}

// Checks CJ for a tracking number; emails the customer once when it appears.
export async function syncTracking(pi, { force = false } = {}) {
  const order = await getOrder(pi.metadata.cj_order_id);
  const tracking = order.trackNumber;
  if (!tracking) return { status: order.orderStatus };
  if (pi.metadata.fulfillment === 'shipped' && !force) return { tracking };
  const link = trackingLink(tracking);
  const email = pi.receipt_email || (await sessionForPaymentIntent(pi.id))?.customer_details?.email;
  if (email) {
    await sendEmail({
      to: email,
      subject: `Your ${PRODUCT.name} has shipped`,
      text: `Good news: your order is on its way.\n\nTracking number: ${tracking}\nTrack it here: ${link}`,
    });
  }
  await stripe().paymentIntents.update(pi.id, { metadata: { fulfillment: 'shipped', tracking } });
  return { tracking, emailed: Boolean(email) };
}

export const trackingLink = (t) => `https://parcelsapp.com/en/tracking/${encodeURIComponent(t)}`;

async function alertOwner(subject, text) {
  if (process.env.OWNER_EMAIL) await sendEmail({ to: process.env.OWNER_EMAIL, subject, text });
}
