'use client';
import { useEffect } from 'react';
import Link from 'next/link';
import { useCart } from '../components/cart';

export default function Success() {
  const { clear } = useCart();
  useEffect(() => clear(), []); // eslint-disable-line react-hooks/exhaustive-deps
  return (
    <section className="section">
      <div className="wrap narrow center">
        <h1>Thank you. Your order is confirmed.</h1>
        <p className="lede">A confirmation email is on its way. Your order ships from our US warehouse and usually arrives in 5–7 business days. We’ll email your tracking number as soon as it ships.</p>
        <p><Link href="/guides/how-to-play-with-an-indoor-cat" className="btn primary">While you wait: the play guide</Link></p>
      </div>
    </section>
  );
}
