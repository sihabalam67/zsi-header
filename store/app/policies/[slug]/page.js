import { notFound } from 'next/navigation';
import { BRAND } from '@/lib/product';

// Starter policies. Not legal advice: review before launch.
const POLICIES = {
  shipping: {
    title: 'Shipping Policy',
    body: [
      'We ship to addresses in the United States only.',
      'Orders are processed within 1–3 business days and ship from a US warehouse. Delivery usually takes 5–7 business days in total.',
      'Shipping is free on orders over $29; otherwise a flat $4.99 applies at checkout.',
      'You will receive a tracking number by email once your order ships. If it has not arrived within 10 business days, contact us and we will make it right.',
    ],
  },
  returns: {
    title: 'Returns & Refunds',
    body: [
      'If you are not happy with your order, contact us within 30 days of delivery.',
      'Damaged or defective items: send a photo and we will send a replacement or a full refund. No need to return the item.',
      'Other returns: unused items in original packaging can be returned for a refund of the item price. We will send the return address.',
      'Refunds go back to the original payment method within 5–10 business days of approval.',
    ],
  },
  privacy: {
    title: 'Privacy Policy',
    body: [
      'We collect the information needed to fulfil your order: name, email, phone, shipping address and order details.',
      'Payments are processed by Stripe; we never see or store your full card number.',
      'Your shipping details are shared with our fulfilment partner only to deliver your order.',
      'We send order and shipping emails. We only send marketing emails if you opt in, and you can unsubscribe at any time.',
      `To access or delete your data, email ${BRAND.supportEmail}.`,
    ],
  },
  terms: {
    title: 'Terms of Service',
    body: [
      `These terms apply to purchases from ${BRAND.name}.`,
      'Prices are in US dollars and may change without notice. Orders are confirmed once payment is received.',
      'Our toys are for supervised play with pets. Store string toys out of reach when not in use.',
      'To the extent permitted by law, our liability is limited to the amount you paid for the order.',
    ],
  },
  contact: {
    title: 'Contact Us',
    body: [`Email: ${BRAND.supportEmail}`, `Mail: ${BRAND.address}`, 'We reply within 1 business day.'],
  },
};

export function generateStaticParams() {
  return Object.keys(POLICIES).map((slug) => ({ slug }));
}

export default async function Policy({ params }) {
  const { slug } = await params;
  const p = POLICIES[slug];
  if (!p) notFound();
  return (
    <section className="policy">
      <h1>{p.title}</h1>
      {p.body.map((t) => (
        <p key={t}>{t}</p>
      ))}
    </section>
  );
}
