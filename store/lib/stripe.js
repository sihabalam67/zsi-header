import Stripe from 'stripe';
import { CURRENCY, PRODUCTS } from './product';

let client;
export function stripe() {
  if (!process.env.STRIPE_SECRET_KEY) throw new Error('STRIPE_SECRET_KEY is not set');
  client ||= new Stripe(process.env.STRIPE_SECRET_KEY);
  return client;
}

// Find-or-create a Stripe price for every product bundle, keyed by lookup_key,
// so nothing has to be set up by hand in Stripe. The amount is part of the key,
// so changing a price in lib/product.js creates a new Stripe price.
export const priceKey = (slug, bundleId) => `${slug}:${bundleId}`;
const lookupKey = (slug, b) => `${slug}-${b.id}-${b.price}`;

export async function ensurePrices() {
  const items = PRODUCTS.flatMap((p) => p.bundles.map((b) => ({ p, b, key: lookupKey(p.slug, b) })));
  const byKey = {};
  for (let i = 0; i < items.length; i += 10) {
    const keys = items.slice(i, i + 10).map((x) => x.key);
    const existing = await stripe().prices.list({ lookup_keys: keys, active: true, limit: 10 });
    for (const pr of existing.data) byKey[pr.lookup_key] = pr.id;
  }
  const result = {};
  for (const { p, b, key } of items) {
    if (!byKey[key]) {
      const meta = { product: p.slug, bundle: b.id, units: String(b.units) };
      const price = await stripe().prices.create({
        currency: CURRENCY,
        unit_amount: b.price,
        lookup_key: key,
        product_data: { name: `${p.name}: ${b.label}`, metadata: meta },
        metadata: meta,
      });
      byKey[key] = price.id;
    }
    result[priceKey(p.slug, b.id)] = byKey[key];
  }
  return result;
}
