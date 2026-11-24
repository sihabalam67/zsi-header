'use client';
import { useEffect } from 'react';
import Link from 'next/link';
import { useCart } from '../components/cart';

// Stripe's "back" link lands here; open the cart drawer over the shop.
export default function CartPage() {
  const { setOpen, count } = useCart();
  useEffect(() => setOpen(true), [setOpen]);
  return (
    <section className="section">
      <div className="wrap narrow center">
        <h1>Your cart</h1>
        <p className="lede">{count ? 'Your items are still in your cart.' : 'Your cart is empty.'}</p>
        <p><button className="btn primary" onClick={() => setOpen(true)}>Open cart</button> <Link href="/shop" className="btn ghost">Keep shopping</Link></p>
      </div>
    </section>
  );
}
