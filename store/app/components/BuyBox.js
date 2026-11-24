'use client';
import { useEffect, useRef, useState } from 'react';
import { useCart } from './cart';
import { getProduct, money, FREE_SHIPPING_THRESHOLD } from '@/lib/product';

// Bundle picker + add to cart, with a sticky bar on mobile once the main button scrolls away.
export default function BuyBox({ slug }) {
  const product = getProduct(slug);
  const { add } = useCart();
  const defaultBundle = product.bundles.find((b) => b.badge)?.id || product.bundles[0].id;
  const [selected, setSelected] = useState(defaultBundle);
  const [showSticky, setShowSticky] = useState(false);
  const btnRef = useRef(null);

  // Links from Google Shopping / structured data use ?offer=<bundle id>.
  useEffect(() => {
    const offer = new URLSearchParams(window.location.search).get('offer');
    if (product.bundles.some((b) => b.id === offer)) setSelected(offer);
  }, [product]);

  useEffect(() => {
    const el = btnRef.current;
    if (!el || !('IntersectionObserver' in window)) return;
    const io = new IntersectionObserver(([e]) => setShowSticky(!e.isIntersecting && e.boundingClientRect.top < 0));
    io.observe(el);
    return () => io.disconnect();
  }, []);

  const bundle = product.bundles.find((b) => b.id === selected);
  const single = product.bundles[0];

  return (
    <div className="buybox">
      <fieldset className="bundles">
        <legend className="sr-only">Choose a bundle</legend>
        {product.bundles.map((b) => {
          const save = single.price * b.units - b.price;
          return (
            <label key={b.id} className={`bundle ${selected === b.id ? 'on' : ''}`}>
              <input type="radio" name={`bundle-${slug}`} checked={selected === b.id} onChange={() => setSelected(b.id)} />
              <span className="b-main">
                <span className="b-label">{b.label}{b.badge && <em className="badge">{b.badge}</em>}</span>
                <small>{b.sub}</small>
              </span>
              <span className="b-price">
                <b>{money(b.price)}</b>
                {save > 0 && <small className="save">Save {money(save)}</small>}
              </span>
            </label>
          );
        })}
      </fieldset>
      <button ref={btnRef} className="btn primary block lg" onClick={() => add(product.slug, selected)}>
        Add to cart · {money(bundle.price)}
      </button>
      <ul className="assurances">
        <li><Icon d="M3 7h11v9H3zM14 10h4l3 3v3h-7z" /><span>Free US shipping over {money(FREE_SHIPPING_THRESHOLD)}</span></li>
        <li><Icon d="M12 3l8 4v5c0 5-3.5 8-8 9-4.5-1-8-4-8-9V7z" /><span>Secure checkout by Stripe</span></li>
        <li><Icon d="M4 12a8 8 0 1 0 3-6.2M4 4v4h4" /><span>30-day returns</span></li>
      </ul>
      <div className={`sticky-buy ${showSticky ? 'show' : ''}`}>
        <div><b>{product.name}</b><small>{bundle.label} · {money(bundle.price)}</small></div>
        <button className="btn primary" onClick={() => add(product.slug, selected)}>Add to cart</button>
      </div>
    </div>
  );
}

function Icon({ d }) {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinejoin="round" aria-hidden="true"><path d={d} /></svg>
  );
}
