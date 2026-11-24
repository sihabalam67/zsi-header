import BuyBox from './components/BuyBox';
import { BRAND, PRODUCT } from '@/lib/product';

const FAQ = [
  ['How long does shipping take?', 'Orders ship from a US warehouse and usually arrive in 5–7 business days. You get a tracking number by email as soon as it ships.'],
  ['Will my cat actually play with it?', 'Most cats chase moving prey-like lures, but every cat is different. If yours isn’t interested, see our 30-day return policy.'],
  ['Is it safe?', 'It’s a string toy, so play together and store it out of reach afterwards. Replace a lure when it gets worn.'],
  ['Can I get extra lures?', 'Yes. You can add a 3-lure refill pack at checkout.'],
  ['What if it arrives damaged?', 'Email us a photo within 30 days and we’ll send a replacement or a refund.'],
];

export default function Home() {
  return (
    <>
      <section className="hero">
        <div className="hero-media">
          <img src={PRODUCT.images[0]} alt={PRODUCT.short} />
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
          <div><b>1. Cast</b><p>Extend the rod and flick the lure across the floor.</p></div>
          <div><b>2. Reel</b><p>Wind it back slowly. Prey that “escapes” is what triggers the stalk.</p></div>
          <div><b>3. Let them win</b><p>End with a catch. A finished hunt is the satisfying part for your cat.</p></div>
        </div>
      </section>

      <section className="faq">
        <h2>Questions</h2>
        {FAQ.map(([q, a]) => (
          <details key={q}>
            <summary>{q}</summary>
            <p>{a}</p>
          </details>
        ))}
        <p className="fine">{PRODUCT.safety}</p>
      </section>
      <p className="tagline">{BRAND.tagline}</p>
    </>
  );
}
