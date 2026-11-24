import Link from 'next/link';
import ProductCard from '../components/ProductCard';
import { PRODUCTS } from '@/lib/product';
import { JsonLd, itemListLd, breadcrumbLd } from '@/lib/seo';

export const metadata = {
  title: 'Shop Indoor Cat Toys',
  description: 'Interactive wand toys, window bird feeders, lure refills and silvervine for indoor cats. Ships from a US warehouse.',
  alternates: { canonical: '/shop' },
};

export default function Shop() {
  return (
    <section className="section">
      <div className="wrap">
        <nav className="crumbs" aria-label="Breadcrumb"><Link href="/">Home</Link> › Shop</nav>
        <h1>Shop indoor cat play</h1>
        <p className="lede">Everything you need for the 10-minute nightly hunt, plus things to keep your cat busy while you’re out.</p>
        <div className="pgrid">{PRODUCTS.map((p) => <ProductCard key={p.slug} product={p} />)}</div>
      </div>
      <JsonLd data={itemListLd(PRODUCTS)} />
      <JsonLd data={breadcrumbLd([['Home', '/'], ['Shop', '/shop']])} />
    </section>
  );
}
