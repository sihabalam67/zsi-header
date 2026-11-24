import { FREE_SHIPPING_THRESHOLD, UPSELL, money } from './product';

// Shared by the home page, /faq, FAQPage structured data and llms.txt.
// Answers lead with the direct answer (best for search snippets and AI answers).
export const FAQ = [
  {
    q: 'How long does shipping take?',
    a: 'Orders ship from a US warehouse and usually arrive in 5–7 business days. You get a tracking number by email as soon as your order ships.',
  },
  {
    q: 'How much is shipping?',
    a: `Shipping is free on US orders over ${money(FREE_SHIPPING_THRESHOLD)}. Smaller orders pay a flat $4.99.`,
  },
  {
    q: 'Do you ship outside the United States?',
    a: 'Not yet. We currently ship to US addresses only.',
  },
  {
    q: 'Will my cat actually play with it?',
    a: 'Most cats chase toys that move like prey (darting away, hiding, then stopping), but every cat is different. If yours isn’t interested, our 30-day return policy covers you.',
  },
  {
    q: 'Is a wand toy safe for cats?',
    a: 'Yes, when used together. It’s a string toy, so play with your cat, then store it out of reach so it can’t be chewed or swallowed. Replace a lure when it gets worn.',
  },
  {
    q: 'Can I buy extra lures?',
    a: `Yes. The ${UPSELL.name} has 6 replacement lures for ${money(UPSELL.bundles[0].price)}, and you can add it from the cart or at checkout.`,
  },
  {
    q: 'What is your return policy?',
    a: 'You have 30 days from delivery. Damaged or defective items are replaced or refunded with just a photo. Unused items can be returned for a refund of the item price.',
  },
  {
    q: 'How do I contact you?',
    a: 'Email us any time. We reply within one business day. The address is on our Contact page.',
  },
];
