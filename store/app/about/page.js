import Link from 'next/link';
import { BRAND } from '@/lib/product';
import { JsonLd, breadcrumbLd } from '@/lib/seo';

export const metadata = {
  title: 'About Us',
  description: `${BRAND.name} makes simple, interactive play easy for indoor cats and the people who live with them.`,
  alternates: { canonical: '/about' },
};

export default function About() {
  return (
    <section className="article">
      <nav className="crumbs" aria-label="Breadcrumb"><Link href="/">Home</Link> › About</nav>
      <h1 data-split>About {BRAND.name}</h1>
      <p className="lede">{BRAND.tagline}</p>
      <p>
        Indoor cats are safer, but many of them are bored. Cats are built to stalk, chase and catch, and a few
        minutes of real “hunting” a day makes a big difference for a lot of them. We focus on one thing: making
        that daily play simple for busy owners.
      </p>
      <h2>What we promise</h2>
      <ul>
        <li>Orders ship from a US warehouse and usually arrive in 5–7 business days, with tracking.</li>
        <li>30-day returns. Damaged or defective items are replaced or refunded with just a photo.</li>
        <li>Honest product pages: no fake reviews, no fake countdown timers, no health claims.</li>
        <li>Free play guides for everyone, whether or not you buy from us.</li>
      </ul>
      <h2>Contact</h2>
      <p>Email <a href={`mailto:${BRAND.supportEmail}`}>{BRAND.supportEmail}</a>. We reply within one business day.</p>
      <JsonLd data={breadcrumbLd([['Home', '/'], ['About', '/about']])} />
    </section>
  );
}
