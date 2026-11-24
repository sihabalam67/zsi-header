import Link from 'next/link';
import { notFound } from 'next/navigation';
import BuyBox from '../../components/BuyBox';
import Gallery from '../../components/Gallery';
import ProductCard from '../../components/ProductCard';
import { PRODUCTS, getProduct, money, fromPrice, RETURN_DAYS } from '@/lib/product';
import { JsonLd, productLd, breadcrumbLd } from '@/lib/seo';

export function generateStaticParams() {
  return PRODUCTS.map((p) => ({ slug: p.slug }));
}

export async function generateMetadata({ params }) {
  const { slug } = await params;
  const p = getProduct(slug);
  if (!p) return {};
  const description = `${p.tagline}. From ${money(fromPrice(p))}. Ships from a US warehouse in 5–7 business days, ${RETURN_DAYS}-day returns.`;
  return {
    title: `${p.name}: ${p.tagline}`,
    description,
    alternates: { canonical: `/products/${p.slug}` },
    openGraph: { title: p.name, description, url: `/products/${p.slug}` },
  };
}

export default async function ProductPage({ params }) {
  const { slug } = await params;
  const p = getProduct(slug);
  if (!p) notFound();
  const related = PRODUCTS.filter((x) => x.slug !== p.slug).slice(0, 3);

  return (
    <>
      <section className="section pdp">
        <div className="wrap">
          <nav className="crumbs" aria-label="Breadcrumb"><Link href="/">Home</Link> › <Link href="/shop">Shop</Link> › {p.name}</nav>
          <div className="pdp-grid">
            <Gallery images={p.images} alt={`${p.name}: ${p.tagline}`} />
            <div className="pdp-info">
              <small className="eyebrow">{p.category}</small>
              <h1>{p.name}</h1>
              <p className="lede">{p.tagline}.</p>
              <ul className="ticks">{p.bullets.map((b) => <li key={b}>{b}</li>)}</ul>
              <BuyBox slug={p.slug} />
              <div className="accordions">
                {p.details.map(([h, t]) => (
                  <details key={h}><summary>{h}</summary><p>{t}</p></details>
                ))}
                <details><summary>Shipping</summary><p>Ships from a US warehouse within 1–3 business days and usually arrives in 5–7 business days. Tracking is emailed when it ships. <Link href="/policies/shipping">Shipping policy</Link></p></details>
                <details><summary>Returns</summary><p>{RETURN_DAYS} days from delivery. Damaged or defective items are replaced or refunded with just a photo. <Link href="/policies/returns">Returns policy</Link></p></details>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="wrap">
          <h2 data-split>You might also like</h2>
          <div className="pgrid three" data-stagger>{related.map((r) => <ProductCard key={r.slug} product={r} />)}</div>
        </div>
      </section>

      <JsonLd data={productLd(p)} />
      <JsonLd data={breadcrumbLd([['Home', '/'], ['Shop', '/shop'], [p.name, `/products/${p.slug}`]])} />
    </>
  );
}
