import Stripe from 'stripe';
import { CURRENCY, OFFERS, UPSELL, PRODUCT } from './product';

let client;
export function stripe() {
  if (!process.env.STRIPE_SECRET_KEY) throw new Error('STRIPE_SECRET_KEY is not set');
  client ||= new Stripe(process.env.STRIPE_SECRET_KEY);
  return client;
}

// Find-or-create Stripe prices by lookup_key, so nothing has to be set up
// by hand in the Stripe dashboard. Changing a price in product.js creates a
// new lookup key (the amount is part of it).
const lookupKey = (id, amount) => `${PRODUCT.slug}-${id}-${amount}`;

export async function ensurePrices() {
  const items = [
    ...OFFERS.map((o) => ({ id: o.id, amount: o.price, name: `${PRODUCT.name} — ${o.label}`, units: o.units })),
    { id: UPSELL.id, amount: UPSELL.price, name: UPSELL.name, units: 0 },
  ];
  const keys = items.map((i) => lookupKey(i.id, i.amount));
  const existing = await stripe().prices.list({ lookup_keys: keys, active: true, limit: 100 });
  const byKey = Object.fromEntries(existing.data.map((p) => [p.lookup_key, p.id]));

  const result = {};
  for (const item of items) {
    const key = lookupKey(item.id, item.amount);
    if (!byKey[key]) {
      const price = await stripe().prices.create({
        currency: CURRENCY,
        unit_amount: item.amount,
        lookup_key: key,
        product_data: {
          name: item.name,
          metadata: { offer_id: item.id, units: String(item.units) },
        },
        metadata: { offer_id: item.id, units: String(item.units) },
      });
      byKey[key] = price.id;
    }
    result[item.id] = byKey[key];
  }
  return result;
}
