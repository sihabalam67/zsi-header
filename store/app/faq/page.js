import Link from 'next/link';
import { FAQ } from '@/lib/faq';
import { JsonLd, faqLd, breadcrumbLd } from '@/lib/seo';

export const metadata = {
  title: 'FAQ: Shipping, Returns and Cat Toy Safety',
  description: 'Answers about shipping times, free shipping, returns, wand toy safety and extra lures.',
  alternates: { canonical: '/faq' },
};

export default function FaqPage() {
  return (
    <section className="article">
      <nav className="crumbs" aria-label="Breadcrumb"><Link href="/">Home</Link> › FAQ</nav>
      <h1>Frequently asked questions</h1>
      {FAQ.map(({ q, a }) => (
        <div key={q} className="qa">
          <h2>{q}</h2>
          <p>{a}</p>
        </div>
      ))}
      <p>Still have a question? <Link href="/policies/contact">Contact us</Link>.</p>
      <JsonLd data={faqLd(FAQ)} />
      <JsonLd data={breadcrumbLd([['Home', '/'], ['FAQ', '/faq']])} />
    </section>
  );
}
