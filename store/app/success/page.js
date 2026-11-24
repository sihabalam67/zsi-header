import Link from 'next/link';

export const metadata = { title: 'Order confirmed' };

export default function Success() {
  return (
    <section className="center">
      <h1>Order confirmed 🎣</h1>
      <p>Thanks! A confirmation email is on its way. Your order ships from our US warehouse and usually arrives in 5–7 business days. We’ll email tracking as soon as it ships.</p>
      <Link href="/" className="cta inline">Back to the store</Link>
    </section>
  );
}
