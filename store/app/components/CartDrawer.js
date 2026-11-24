'use client';
import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useCart, startCheckout } from './cart';
import { money, FREE_SHIPPING_THRESHOLD, UPSELL } from '@/lib/product';

export function CartButton() {
  const { count, setOpen } = useCart();
  return (
    <button className="cart-btn" onClick={() => setOpen(true)} aria-label={`Open cart, ${count} items`}>
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden="true"><path d="M6 7h12l-1 13H7L6 7z" /><path d="M9 7a3 3 0 0 1 6 0" /></svg>
      {count > 0 && <span className="cart-count">{count}</span>}
    </button>
  );
}

export function CartDrawer() {
  const { lines, subtotal, toFreeShipping, setQty, open, setOpen, add, items } = useCart();
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const onKey = (e) => e.key === 'Escape' && setOpen(false);
    document.addEventListener('keydown', onKey);
    document.body.style.overflow = open ? 'hidden' : '';
    return () => document.removeEventListener('keydown', onKey);
  }, [open, setOpen]);

  async function checkout() {
    setBusy(true);
    setError('');
    try {
      await startCheckout(items);
    } catch (e) {
      setError(e.message);
      setBusy(false);
    }
  }

  const pct = Math.min(100, Math.round((subtotal / FREE_SHIPPING_THRESHOLD) * 100));
  const hasUpsell = UPSELL && lines.some((l) => l.product.slug === UPSELL.slug);

  return (
    <div className={`drawer-wrap ${open ? 'open' : ''}`} aria-hidden={!open}>
      <div className="drawer-scrim" onClick={() => setOpen(false)} />
      <aside className="drawer" role="dialog" aria-label="Shopping cart" aria-modal="true">
        <div className="drawer-head">
          <h2>Your cart</h2>
          <button className="icon-btn" onClick={() => setOpen(false)} aria-label="Close cart">✕</button>
        </div>

        {lines.length > 0 && (
          <div className="ship-meter">
            <p>{toFreeShipping > 0 ? <>You’re <b>{money(toFreeShipping)}</b> away from free shipping</> : <>You’ve unlocked <b>free US shipping</b></>}</p>
            <div className="meter"><span style={{ width: `${pct}%` }} /></div>
          </div>
        )}

        <div className="drawer-body">
          {lines.length === 0 && (
            <div className="empty">
              <p>Your cart is empty.</p>
              <Link href="/shop" className="btn" onClick={() => setOpen(false)}>Shop all</Link>
            </div>
          )}
          {lines.map((l) => (
            <div className="line" key={`${l.slug}-${l.bundle}`}>
              <img src={l.product.images[0]} alt="" width="72" height="72" />
              <div className="line-info">
                <Link href={`/products/${l.slug}`} onClick={() => setOpen(false)}><b>{l.product.name}</b></Link>
                <small>{l.bundle.label}</small>
                <div className="qty">
                  <button onClick={() => setQty(l.slug, l.bundle.id, l.qty - 1)} aria-label="Decrease quantity">−</button>
                  <span>{l.qty}</span>
                  <button onClick={() => setQty(l.slug, l.bundle.id, l.qty + 1)} aria-label="Increase quantity">+</button>
                </div>
              </div>
              <b>{money(l.total)}</b>
            </div>
          ))}
          {lines.length > 0 && UPSELL && !hasUpsell && (
            <div className="upsell">
              <img src={UPSELL.images[0]} alt="" width="56" height="56" />
              <div><b>Add a {UPSELL.name}</b><small>{UPSELL.tagline}</small></div>
              <button className="btn small" onClick={() => add(UPSELL.slug, UPSELL.bundles[0].id)}>+ {money(UPSELL.bundles[0].price)}</button>
            </div>
          )}
        </div>

        {lines.length > 0 && (
          <div className="drawer-foot">
            <div className="row"><span>Subtotal</span><b>{money(subtotal)}</b></div>
            <button className="btn primary block" onClick={checkout} disabled={busy}>{busy ? 'Opening secure checkout…' : 'Checkout securely'}</button>
            {error && <p className="error">{error}</p>}
            <p className="fine center">Secure payment by Stripe · Ships from a US warehouse · 30-day returns</p>
          </div>
        )}
      </aside>
    </div>
  );
}
