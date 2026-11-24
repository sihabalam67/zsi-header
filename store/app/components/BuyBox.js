'use client';
import { useEffect, useState } from 'react';
import { OFFERS, UPSELL, FREE_SHIPPING_THRESHOLD, money } from '@/lib/product';

export default function BuyBox() {
  const [selected, setSelected] = useState('duo');

  // Links from Google Shopping / structured data use ?offer=<id>.
  useEffect(() => {
    const offer = new URLSearchParams(window.location.search).get('offer');
    if (OFFERS.some((o) => o.id === offer)) setSelected(offer);
  }, []);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  async function checkout() {
    setLoading(true);
    setError('');
    try {
      const res = await fetch('/api/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ offerId: selected }),
      });
      const data = await res.json();
      if (!data.url) throw new Error(data.error || 'Checkout unavailable');
      window.location.href = data.url;
    } catch (e) {
      setError(e.message);
      setLoading(false);
    }
  }

  return (
    <div className="buybox">
      {OFFERS.map((o) => {
        const perUnit = o.price / o.units;
        return (
          <label key={o.id} className={`offer ${selected === o.id ? 'on' : ''}`}>
            <input
              type="radio"
              name="offer"
              checked={selected === o.id}
              onChange={() => setSelected(o.id)}
            />
            <span className="offer-main">
              <strong>{o.label}</strong>
              {o.badge && <em className="badge">{o.badge}</em>}
              <small>{o.sub}</small>
            </span>
            <span className="offer-price">
              <strong>{money(o.price)}</strong>
              {o.units > 1 && <small>{money(perUnit)} each</small>}
            </span>
          </label>
        );
      })}
      <button className="cta" onClick={checkout} disabled={loading}>
        {loading ? 'Opening secure checkout…' : 'Get my cat hunting'}
      </button>
      {error && <p className="error">{error}</p>}
      <p className="fine">
        Free US shipping on orders over {money(FREE_SHIPPING_THRESHOLD)} · Ships from a US warehouse in 5–7
        business days · Add a {UPSELL.name.toLowerCase()} at checkout
      </p>
    </div>
  );
}
