import Link from 'next/link';
import { notFound } from 'next/navigation';
import { loadSession, shippingOf, supplierItems, trackingLink } from '@/lib/fulfill';
import { money } from '@/lib/product';
import { retryFulfillment, retryCjPayment, checkTracking } from '../../actions';

export default async function Order({ params, searchParams }) {
  const { id } = await params;
  const { msg } = await searchParams;
  let session;
  try {
    session = await loadSession(id);
  } catch {
    notFound();
  }
  const pi = session.payment_intent;
  const m = pi?.metadata || {};
  const ship = shippingOf(session);
  const status = m.fulfillment || 'pending';

  return (
    <>
      <p><Link href="/admin">← All orders</Link></p>
      <h1>Order {new Date(session.created * 1000).toLocaleString('en-US')}</h1>
      {msg && <p className="notice">{msg}</p>}

      <div className="tiles">
        <div className="tile"><small>Total</small><strong>{money(session.amount_total)}</strong><span>{session.payment_status}</span></div>
        <div className="tile"><small>Fulfilment</small><strong className={`pill ${status}`}>{status}</strong><span>{m.cj_order_id ? `CJ ${m.cj_order_id}` : 'No CJ order yet'}</span></div>
        <div className="tile"><small>Tracking</small><strong>{m.tracking || '—'}</strong><span>{m.tracking ? <a href={trackingLink(m.tracking)} target="_blank">Track</a> : 'Not shipped yet'}</span></div>
      </div>

      {m.fulfillment_error && <p className="error">Last error: {m.fulfillment_error}</p>}

      <section className="panel">
        <h2>Actions</h2>
        <div className="actions">
          {(status === 'error' || status === 'pending') && (
            <form action={retryFulfillment}><input type="hidden" name="id" value={id} /><button className="cta inline">Retry supplier order</button></form>
          )}
          {status === 'unpaid' && (
            <form action={retryCjPayment}><input type="hidden" name="id" value={id} /><button className="cta inline">Retry CJ payment</button></form>
          )}
          {m.cj_order_id && (
            <form action={checkTracking}><input type="hidden" name="id" value={id} /><button className="cta inline">Check tracking now</button></form>
          )}
          {m.tracking && (
            <form action={checkTracking}><input type="hidden" name="id" value={id} /><input type="hidden" name="force" value="1" /><button className="cta inline secondary">Resend tracking email</button></form>
          )}
          {pi && <a className="cta inline secondary" href={`https://dashboard.stripe.com/payments/${pi.id}`} target="_blank">Refund in Stripe</a>}
        </div>
      </section>

      <section className="panel">
        <h2>Customer</h2>
        <p>{session.customer_details?.name}<br />{session.customer_details?.email}<br />{session.customer_details?.phone}</p>
        <h3>Ship to</h3>
        {ship ? (
          <p>{ship.name}<br />{ship.address?.line1}{ship.address?.line2 ? `, ${ship.address.line2}` : ''}<br />{ship.address?.city}, {ship.address?.state} {ship.address?.postal_code}</p>
        ) : <p>—</p>}
      </section>

      <section className="panel">
        <h2>Items</h2>
        <ul>
          {session.line_items.data.map((li) => (
            <li key={li.id}>{li.quantity} × {li.description} · {money(li.amount_total)}</li>
          ))}
        </ul>
        <p className="fine">Sent to supplier as: {JSON.stringify(supplierItems(session))}</p>
      </section>
    </>
  );
}
