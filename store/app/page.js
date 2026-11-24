import Link from 'next/link';
import Image from 'next/image';
import BuyBox from './components/BuyBox';
import Gallery from './components/Gallery';
import ProductCard from './components/ProductCard';
import { BRAND, FEATURED, PRODUCTS, RETURN_DAYS, money, FREE_SHIPPING_THRESHOLD, getProduct } from '@/lib/product';
import { FAQ } from '@/lib/faq';
import { GUIDES } from '@/lib/guides';
import { PHOTOS } from '@/lib/photos';
import { JsonLd, productLd, faqLd, itemListLd } from '@/lib/seo';

export const metadata = {
  title: { absolute: `${BRAND.name} | Interactive Cat Toys for Indoor Cats` },
  description: `Wand toys, window bird feeders and play guides that give indoor cats a real hunt. Ships from a US warehouse in 5–7 business days, free US shipping over ${money(FREE_SHIPPING_THRESHOLD)}, ${RETURN_DAYS}-day returns.`,
  alternates: { canonical: '/' },
};

const HUNT = [
  { n: '01', title: 'Stalk', text: 'Move the lure away from your cat in short darts. Prey runs; it never charges.', photo: PHOTOS.stalk },
  { n: '02', title: 'Pounce', text: 'Pause. Let it peek out from behind the couch. The pause is when the wiggle starts.', photo: PHOTOS.pounce },
  { n: '03', title: 'Catch', text: 'Let your cat win often. A hunt with no catch is just frustration.', photo: PHOTOS.feather },
  { n: '04', title: 'Eat & rest', text: 'Finish with a meal or a treat. Hunt, catch, eat, sleep: the natural order.', photo: PHOTOS.rest },
];

export default function Home() {
  const feeder = getProduct('cat-tv-window-bird-feeder');
  return (
    <>
      <section className="hero-photo-sec">
        <div className="hero-photo">
          <Image src={PHOTOS.hero.src} alt={PHOTOS.hero.alt} fill priority sizes="100vw" />
        </div>
        <div className="hero-scrim" />
        <div className="wrap hero-content">
          <p className="eyebrow light"><span>For indoor cats with energy to burn</span></p>
          <h1 data-split>Give your indoor cat a <em>real</em> hunt.</h1>
          <div>
            <p className="lede light">Ten minutes of the right kind of play a day. Built on how cats actually hunt, made easy for busy people.</p>
            <div className="hero-ctas">
              <Link href={`/products/${FEATURED.slug}`} className="btn primary lg on-dark" data-magnetic>Shop the {FEATURED.name}</Link>
              <Link href="/shop" className="btn light lg">Shop all</Link>
            </div>
            <ul className="trust-inline light"><li>Ships from the US</li><li>{RETURN_DAYS}-day returns</li><li>Secure checkout</li></ul>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="wrap">
          <div className="section-head">
            <h2 data-split>Shop indoor cat play</h2>
            <Link href="/shop" className="link-arrow">View all →</Link>
          </div>
          <div className="pgrid" data-stagger>{PRODUCTS.map((p) => <ProductCard key={p.slug} product={p} />)}</div>
        </div>
      </section>

      <section className="hunt" aria-labelledby="hunt-title">
        <div className="hunt-track">
          <div className="hunt-intro">
            <p className="eyebrow">The 10-minute nightly hunt</p>
            <h2 id="hunt-title" data-split>Four steps your cat already knows.</h2>
            <p className="lede">Cats are built for short bursts: stalk, pounce, catch, then rest. Play that follows that order is the play they come back for.</p>
            <Link href="/guides/how-to-play-with-an-indoor-cat" className="link-arrow">Read the full guide →</Link>
          </div>
          {HUNT.map((h) => (
            <article className="hunt-panel" key={h.n}>
              <figure className="hunt-photo"><Image src={h.photo.src} alt={h.photo.alt} fill sizes="(min-width: 821px) 34vw, 100vw" /></figure>
              <div className="hunt-text"><span className="hunt-n">{h.n}</span><h3>{h.title}</h3><p>{h.text}</p></div>
            </article>
          ))}
        </div>
      </section>

      <section className="section feature">
        <div className="wrap feature-grid">
          <Gallery images={FEATURED.images} alt={`${FEATURED.name}: ${FEATURED.tagline}`} />
          <div>
            <p className="eyebrow">Our signature toy</p>
            <h2 className="h1" data-split>{FEATURED.name}</h2>
            <p className="lede">{FEATURED.tagline}.</p>
            <ul className="ticks">{FEATURED.bullets.map((b) => <li key={b}>{b}</li>)}</ul>
            <BuyBox slug={FEATURED.slug} />
          </div>
        </div>
      </section>

      {feeder && (
        <section className="section editorial">
          <div className="wrap editorial-grid">
            <figure className="editorial-photo" data-reveal><Image src={PHOTOS.window.src} alt={PHOTOS.window.alt} fill sizes="(min-width: 821px) 45vw, 100vw" /></figure>
            <div>
              <p className="eyebrow">While you’re at work</p>
              <h2 data-split>Cat TV, starring the birds outside.</h2>
              <p className="lede">A clear window feeder brings birds to your cat’s eye level. It’s hours of watching for the times you can’t play.</p>
              <ul className="ticks">{feeder.bullets.slice(0, 3).map((b) => <li key={b}>{b}</li>)}</ul>
              <Link href={`/products/${feeder.slug}`} className="btn primary lg" data-magnetic>Shop the {feeder.name}</Link>
            </div>
          </div>
        </section>
      )}

      <section className="section">
        <div className="wrap compare-wrap">
          <div>
            <p className="eyebrow">Why ours</p>
            <h2 data-split>Built for the way cats actually hunt</h2>
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

      <section className="promise-photo">
        <div className="promise-bg"><Image src={PHOTOS.couch.src} alt={PHOTOS.couch.alt} fill sizes="100vw" /></div>
        <div className="promise-scrim" />
        <div className="wrap promise-inner">
          <div className="seal" aria-hidden="true"><span>{RETURN_DAYS}</span><small>DAY</small></div>
          <h2 data-split>The play-or-return promise</h2>
          <p className="lede light">If your cat isn’t into it, return it within {RETURN_DAYS} days of delivery. Arrived damaged? Send a photo and we’ll replace it or refund you.</p>
          <Link href="/policies/returns" className="btn light">Read the returns policy</Link>
        </div>
      </section>

      <section className="section">
        <div className="wrap">
          <div className="section-head">
            <h2 data-split>Indoor cat play guides</h2>
            <Link href="/guides" className="link-arrow">All guides →</Link>
          </div>
          <ul className="gcards" data-stagger>
            {GUIDES.slice(0, 3).map((g, i) => {
              const photo = [PHOTOS.eyes, PHOTOS.pounce, PHOTOS.rest][i];
              return (
                <li key={g.slug}>
                  <Link href={`/guides/${g.slug}`}>
                    <span className="gcard-img"><Image src={photo.src} alt="" fill sizes="(min-width: 821px) 33vw, 100vw" /></span>
                    <b>{g.title}</b><span className="muted">{g.description}</span>
                  </Link>
                </li>
              );
            })}
          </ul>
        </div>
      </section>

      <section className="section faq-sec">
        <div className="wrap narrow">
          <h2 className="center" data-split>Questions, answered</h2>
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
