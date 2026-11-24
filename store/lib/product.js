// Single source of truth for the store's brand, product and offer.
// Swap the product here later without touching the rest of the site
// (the brand is the sub-niche "indoor cat play", not the product).

export const BRAND = {
  name: 'Indoor Hunt Co.',
  tagline: 'Ten minutes of real hunting for indoor cats.',
  supportEmail: process.env.SUPPORT_EMAIL || 'support@example.com',
  // Physical mailing address is legally required in commercial emails (CAN-SPAM)
  // and expected on policy pages. Fill in before launch.
  address: process.env.BUSINESS_ADDRESS || 'Business address to be added',
};

export const CURRENCY = 'usd';

// Free shipping once the cart's main items reach this amount (cents).
// Set just above the single-unit price so the 2-pack unlocks it.
export const FREE_SHIPPING_THRESHOLD = 2900;
export const STANDARD_SHIPPING = 499;

export const PRODUCT = {
  slug: 'reel-hunter-wand',
  name: 'Reel Hunter Wand',
  short: 'Telescopic fishing-rod cat toy with a working reel + 3 lures',
  // Supplier media goes in /public/product/. Placeholder until real photos arrive.
  images: ['/product-placeholder.svg'],
  bullets: [
    'Telescopic rod extends so you can play from the couch',
    'Working reel lets you "cast" and reel the lure in, so your cat stalks it like prey',
    '3 interchangeable lures (feather, fuzzy mouse, crinkle fish)',
    'Lightweight, folds down for storage',
  ],
  safety:
    'String toy: play together, then store it out of reach. Replace lures when worn.',
};

// Bundles = the AOV engine. `cjVid` is the CJ Dropshipping variant ID for one unit.
export const OFFERS = [
  {
    id: 'single',
    label: '1 Wand',
    sub: 'For one cat',
    price: 2499,
    units: 1,
  },
  {
    id: 'duo',
    label: '2 Wands',
    sub: 'Multi-cat home · free shipping',
    price: 3999,
    units: 2,
    badge: 'Best value',
  },
  {
    id: 'trio',
    label: '3 Wands',
    sub: 'Never run out · free shipping',
    price: 5499,
    units: 3,
  },
];

// Upsell shown as an optional add-on inside Stripe Checkout.
export const UPSELL = {
  id: 'lure-refill',
  name: 'Lure Refill Pack (3 lures)',
  price: 999,
};

export const CJ_VARIANTS = {
  wand: process.env.CJ_VID_WAND, // variant ID of the wand
  refill: process.env.CJ_VID_REFILL, // variant ID of the lure refill
};

export function getOffer(id) {
  return OFFERS.find((o) => o.id === id);
}

export const money = (cents) => `$${(cents / 100).toFixed(2)}`;
