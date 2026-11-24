import Link from 'next/link';
import { GUIDES } from '@/lib/guides';
import { JsonLd, breadcrumbLd } from '@/lib/seo';

export const metadata = {
  title: 'Indoor Cat Play Guides',
  description: 'Short, practical guides on playing with indoor cats: how to play, how much playtime they need, night-time zoomies, toy safety and choosing toys.',
  alternates: { canonical: '/guides' },
};

export default function Guides() {
  return (
    <section className="article">
      <nav className="crumbs" aria-label="Breadcrumb"><Link href="/">Home</Link> › Guides</nav>
      <h1>Indoor cat play guides</h1>
      <p className="lede">Practical answers for keeping an indoor cat active and happy, starting with the direct answer.</p>
      <ul className="cards">
        {GUIDES.map((g) => (
          <li key={g.slug}>
            <Link href={`/guides/${g.slug}`}><b>{g.title}</b><span>{g.description}</span></Link>
          </li>
        ))}
      </ul>
      <JsonLd data={breadcrumbLd([['Home', '/'], ['Guides', '/guides']])} />
    </section>
  );
}
