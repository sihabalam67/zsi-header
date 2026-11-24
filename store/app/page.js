import Link from 'next/link';
import BuyBox from './components/BuyBox';
import { BRAND, PRODUCT } from '@/lib/product';
import { FAQ } from '@/lib/faq';
import { GUIDES } from '@/lib/guides';
import { JsonLd, productLd, faqLd } from '@/lib/seo';

export const metadata = {
  title: { absolute: `${PRODUCT.name}: Interactive Cat Toy for Indoor Cats | ${BRAND.name}` },
  description: `${PRODUCT.short}. Built for the 10-minute nightly hunt. Ships from a US warehouse in 5–7 business days, free US shipping over $29, 30-day returns.`,
  alternates: { canonical: '/' },
};

export default function Home() {
  return (
    <>
      <section className="hero">
        <div className="hero-media">
          <img src={PRODUCT.images[0]} alt={PRODUCT.short} width="600" height="600" />
        </div>
        <div className="hero-copy">
          <p className="eyebrow">For indoor cats with too much energy</p>
          <h1>{PRODUCT.name}</h1>
          <p className="lede">{PRODUCT.short}. Cast it, reel it in, and watch your cat stalk, pounce and finally settle down.</p>
          <ul className="bullets">
            {PRODUCT.bullets.map((b) => (
              <li key={b}>{b}</li>
            ))}
          </ul>
          <BuyBox />
        </div>
      </section>

      <section className="band">
        <h2>The 10-minute nightly hunt</h2>
        <div className="steps">
          <div><b>1. Cast</b><p>Extend the rod and flick the lure across the floor, away from your cat.</p></div>
          <div><b>2. Reel</b><p>Wind it back in short darts with pauses. Prey that “escapes” is what triggers the stalk.</p></div>
          <div><b>3. Let them win</b><p>End with a catch, then feed. A finished hunt is the satisfying part for your cat.</p></div>
        </div>
        <p className="more"><Link href="/guides/how-to-play-with-an-indoor-cat">Read the full play guide →</Link></p>
      </section>

      <section className="faq">
        <h2>Questions</h2>
        {FAQ.slice(0, 6).map(({ q, a }) => (
          <details key={q}>
            <summary>{q}</summary>
            <p>{a}</p>
          </details>
        ))}
        <p className="fine">{PRODUCT.safety} <Link href="/faq">All questions →</Link></p>
      </section>

      <section className="guides-teaser">
        <h2>Indoor cat play guides</h2>
        <ul className="cards">
          {GUIDES.slice(0, 3).map((g) => (
            <li key={g.slug}>
              <Link href={`/guides/${g.slug}`}><b>{g.title}</b><span>{g.description}</span></Link>
            </li>
          ))}
        </ul>
      </section>

      <p className="tagline">{BRAND.tagline}</p>
      <JsonLd data={productLd()} />
      <JsonLd data={faqLd(FAQ)} />
    </>
  );
}
