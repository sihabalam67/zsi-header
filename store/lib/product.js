// The catalog: single source of truth for brand, products, bundles and prices.
// The brand is the sub-niche ("indoor cat play"), so products can be added or
// swapped here without touching the rest of the site.
//
// A product can only be bought once its CJ variant ID env var is set
// (checkout refuses anything not connected to the supplier).

export const BRAND = {
  name: 'Indoor Hunt Co.',
  tagline: 'Ten minutes of real hunting for indoor cats.',
  promise: 'Play that feels like the wild, for cats who live indoors.',
  supportEmail: process.env.SUPPORT_EMAIL || 'support@example.com',
  address: process.env.BUSINESS_ADDRESS || 'Business address to be added',
};

export const CURRENCY = 'usd';
export const FREE_SHIPPING_THRESHOLD = 2900; // cents
export const STANDARD_SHIPPING = 499;
export const RETURN_DAYS = 30;

export const PRODUCTS = [
  {
    slug: 'indoor-hunt-wand',
    name: 'Indoor Hunt Wand',
    tagline: 'Telescopic cat wand with 6 interchangeable lures',
    category: 'Wand toys',
    featured: true,
    images: ['/products/indoor-hunt-wand.svg', '/products/indoor-hunt-wand-lures.svg', '/products/how-to-hunt.svg'],
    bullets: [
      'Extends from 14 in to about 3 ft, so the lure moves like real prey, away from your hand',
      '6 clip-on lures: feathers, fuzzy mice and crinkle fish to match how your cat likes to hunt',
      'Play from the couch: the long reach does the running for you',
      'Folds down small and stores in a drawer',
    ],
    details: [
      ['What’s in the box', 'One telescopic wand and 6 interchangeable lures.'],
      ['How to use it', 'Move the lure away from your cat in short darts with pauses, let your cat catch it often, and end each session with a final catch and a meal or treat.'],
      ['Safety', 'String toy: play together, then store it out of reach. Replace lures when they start to fray.'],
    ],
    bundles: [
      { id: 'single', label: '1 wand', sub: 'For one cat', units: 1, price: 1999 },
      { id: 'duo', label: '2 wands', sub: 'Multi-cat home · free shipping', units: 2, price: 3499, badge: 'Best value' },
      { id: 'trio', label: '3 wands', sub: 'One for every room · free shipping', units: 3, price: 4799 },
    ],
    cjVidEnv: 'CJ_VID_HUNT_WAND',
  },
  {
    slug: 'cat-tv-window-bird-feeder',
    name: 'Cat TV Window Bird Feeder',
    tagline: 'Clear window feeder that brings birds to your cat’s eye level',
    category: 'Window watching',
    images: ['/products/cat-tv-window-bird-feeder.svg'],
    bullets: [
      'Clear acrylic: your cat watches birds up close through the glass',
      'Strong suction cups mount it on most windows in a minute',
      'Removable seed tray for easy refills and cleaning',
      'Hours of “cat TV” while you’re at work',
    ],
    details: [
      ['What’s in the box', 'One clear window feeder with suction cups. Bird seed not included.'],
      ['Tip', 'Mount it on a window your cat already sits by. Birds can take a few days to find a new feeder.'],
      ['Care', 'Clean the window and cups before mounting; wipe the tray every week or two.'],
    ],
    bundles: [
      { id: 'single', label: '1 feeder', sub: 'One window', units: 1, price: 3299 },
      { id: 'duo', label: '2 feeders', sub: 'Two windows · free shipping', units: 2, price: 5999, badge: 'Best value' },
    ],
    cjVidEnv: 'CJ_VID_WINDOW_FEEDER',
  },
  {
    slug: 'lure-refill-pack',
    name: 'Lure Refill Pack',
    tagline: '6 replacement lures for the Indoor Hunt Wand',
    category: 'Refills',
    upsell: true,
    images: ['/products/lure-refill-pack.svg'],
    bullets: [
      'Mixed set of feathers, fuzzy mice and crinkle fish',
      'Clips straight onto the Indoor Hunt Wand',
      'Swap lures to keep play new: cats lose interest in the same “prey”',
    ],
    details: [
      ['What’s in the box', '6 assorted lures.'],
      ['When to replace', 'Whenever a lure looks worn or frayed. Active cats go through lures in a few weeks.'],
    ],
    bundles: [
      { id: 'single', label: '1 pack', sub: '6 lures', units: 1, price: 999 },
      { id: 'duo', label: '2 packs', sub: '12 lures', units: 2, price: 1799 },
    ],
    cjVidEnv: 'CJ_VID_LURE_REFILL',
  },
  {
    slug: 'silvervine-chew-sticks',
    name: 'Silvervine Chew Sticks',
    tagline: 'Natural silvervine sticks for chewing and play',
    category: 'Treats & play',
    images: ['/products/silvervine-chew-sticks.svg'],
    bullets: [
      'Natural silvervine (matatabi) wood sticks',
      'Many cats who ignore catnip respond to silvervine',
      'Rub on a lure to make a “boring” toy interesting again',
    ],
    details: [
      ['What’s in the box', 'A pack of silvervine sticks.'],
      ['Good to know', 'Not every cat responds to silvervine. Supervise chewing and replace sticks once they splinter.'],
    ],
    bundles: [
      { id: 'single', label: '1 pack', sub: 'Try it', units: 1, price: 999 },
      { id: 'duo', label: '2 packs', sub: 'Stock up', units: 2, price: 1799 },
    ],
    cjVidEnv: 'CJ_VID_SILVERVINE',
  },
];

export const FEATURED = PRODUCTS.find((p) => p.featured) || PRODUCTS[0];
export const UPSELL = PRODUCTS.find((p) => p.upsell);

export const getProduct = (slug) => PRODUCTS.find((p) => p.slug === slug);
export const getBundle = (product, id) => product?.bundles.find((b) => b.id === id);
export const fromPrice = (p) => Math.min(...p.bundles.map((b) => b.price));
export const cjVid = (p) => process.env[p.cjVidEnv];

export const money = (cents) => `$${(cents / 100).toFixed(2)}`;
