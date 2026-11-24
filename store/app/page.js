import Link from 'next/link';
import BuyBox from './components/BuyBox';
import Gallery from './components/Gallery';
import ProductCard from './components/ProductCard';
import { BRAND, FEATURED, PRODUCTS, RETURN_DAYS, money, FREE_SHIPPING_THRESHOLD } from '@/lib/product';
import { FAQ } from '@/lib/faq';
import { GUIDES } from '@/lib/guides';
import { JsonLd, productLd, faqLd, itemListLd } from '@/lib/seo';

export const metadata = {
  title: { absolute: `${BRAND.name} | Interactive Cat Toys for Indoor Cats` },
  description: `Wand toys, window bird feeders and play guides that give indoor cats a real hunt. Ships from a US warehouse in 5–7 business days, free US shipping over ${money(FREE_SHIPPING_THRESHOLD)}, ${RETURN_DAYS}-day returns.`,
  alternates: { canonical: '/' },
};

export default function Home() {
  return (
    <>
      <section className="hero-split">
        <div className="wrap hero-grid">
          <div className="hero-text">
            <p className="eyebrow">For indoor cats with energy to burn</p>
            <h1>Give your indoor cat a <em>real</em> hunt.</h1>
            <p className="lede">Cats are built to stalk, pounce and catch. Ten minutes of the right kind of play a day makes a big difference for a lot of indoor cats, and we make it easy.</p>
            <div className="hero-ctas">
              <Link href={`/products/${FEATURED.slug}`} className="btn primary lg">Shop the {FEATURED.name}</Link>
              <Link href="/guides/how-to-play-with-an-indoor-cat" className="btn ghost lg">How the hunt works</Link>
            </div>
            <ul className="trust-inline">
              <li>Ships from the US</li><li>{RETURN_DAYS}-day returns</li><li>Secure checkout</li>
            </ul>
          </div>
          <div className="hero-art"><img src="/products/indoor-hunt-wand.svg" alt={`${FEATURED.name}: ${FEATURED.tagline}`} width="800" height="800" fetchPriority="high" /></div>
        </div>
      </section>

      <section className="trust-bar">
        <div className="wrap trust-grid">
          <div><b>Fast US shipping</b><span>5–7 business days, tracking by email</span></div>
          <div><b>Free over {money(FREE_SHIPPING_THRESHOLD)}</b><span>Flat $4.99 below that</span></div>
          <div><b>{RETURN_DAYS}-day returns</b><span>Damaged? Just send a photo</span></div>
          <div><b>Secure checkout</b><span>Payments handled by Stripe</span></div>
        </div>
      </section>

      <section className="section">
        <div className="wrap">
          <div className="section-head">
            <h2>Shop indoor cat play</h2>
            <Link href="/shop" className="link-arrow">View all →</Link>
          </div>
          <div className="pgrid">{PRODUCTS.map((p) => <ProductCard key={p.slug} product={p} />)}</div>
        </div>
      </section>

      <section className="section feature">
        <div className="wrap feature-grid">
          <Gallery images={FEATURED.images} alt={`${FEATURED.name}: ${FEATURED.tagline}`} />
          <div>
            <p className="eyebrow">Our signature toy</p>
            <h2 className="h1">{FEATURED.name}</h2>
            <p className="lede">{FEATURED.tagline}.</p>
            <ul className="ticks">{FEATURED.bullets.map((b) => <li key={b}>{b}</li>)}</ul>
            <BuyBox slug={FEATURED.slug} />
          </div>
        </div>
      </section>

      <section className="section band-dark">
        <div className="wrap">
          <h2 className="center">The 10-minute nightly hunt</h2>
          <p className="center lede light">A simple routine built on how cats hunt: stalk, pounce, catch, eat.</p>
          <div className="steps3">
            <div><span className="step-n">1</span><h3>Stalk</h3><p>Move the lure away from your cat in short darts. Prey runs; it never charges.</p></div>
            <div><span className="step-n">2</span><h3>Pounce</h3><p>Pause and let it peek out from behind the couch. The pause is when the wiggle starts.</p></div>
            <div><span className="step-n">3</span><h3>Catch &amp; eat</h3><p>Let your cat win, then offer a meal or treat. Hunt, catch, eat, rest.</p></div>
          </div>
          <p className="center"><Link href="/guides/how-to-play-with-an-indoor-cat" className="btn light">Read the full guide</Link></p>
        </div>
      </section>

      <section className="section">
        <div className="wrap compare-wrap">
          <div>
            <p className="eyebrow">Why ours</p>
            <h2>Built for the way cats actually hunt</h2>
            <p className="lede">Most wand toys are a stick and a single feather. Here’s what we changed.</p>
          </div>
          <table className="compare">
            <thead><tr><th></th><th>{BRAND.name}</th><th>Typical cheap wand</th></tr></thead>
            <tbody>
              <tr><td>Reach</td><td>Telescopic, about 3 ft</td><td>Short fixed stick</td></tr>
              <tr><td>Lures</td><td>6 interchangeable</td><td>1, glued on</td></tr>
              <tr><td>Refills</td><td>Clip-on refill packs</td><td>Buy a new wand</td></tr>
              <tr><td>Shipping</td><td>US warehouse, 5–7 days</td><td>Often 2–4 weeks from overseas</td></tr>
              <tr><td>Returns</td><td>{RETURN_DAYS} days</td><td>Varies</td></tr>
            </tbody>
          </table>
        </div>
      </section>

      <section className="section promise">
        <div className="wrap promise-grid">
          <div className="seal" aria-hidden="true"><span>{RETURN_DAYS}</span><small>DAY</small></div>
          <div>
            <h2>The play-or-return promise</h2>
            <p>If your cat isn’t into it, return it within {RETURN_DAYS} days of delivery. If anything arrives damaged, send us a photo and we’ll replace it or refund you. No forms, no fuss.</p>
            <Link href="/policies/returns" className="link-arrow">Read the returns policy →</Link>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="wrap">
          <div className="section-head">
            <h2>Indoor cat play guides</h2>
            <Link href="/guides" className="link-arrow">All guides →</Link>
          </div>
          <ul className="cards">
            {GUIDES.slice(0, 3).map((g) => (
              <li key={g.slug}><Link href={`/guides/${g.slug}`}><b>{g.title}</b><span>{g.description}</span></Link></li>
            ))}
          </ul>
        </div>
      </section>

      <section className="section faq-sec">
        <div className="wrap narrow">
          <h2 className="center">Questions, answered</h2>
          {FAQ.slice(0, 6).map(({ q, a }) => (
            <details key={q}><summary>{q}</summary><p>{a}</p></details>
          ))}
          <p className="center"><Link href="/faq" className="link-arrow">More questions →</Link></p>
        </div>
      </section>

      <JsonLd data={productLd(FEATURED)} />
      <JsonLd data={itemListLd(PRODUCTS)} />
      <JsonLd data={faqLd(FAQ)} />
    </>
  );
}
