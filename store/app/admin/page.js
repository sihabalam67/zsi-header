import Link from 'next/link';
import { recentOrders, summarize, cjBalance, readiness } from '@/lib/admin-data';
import { money } from '@/lib/product';
import { SITE_URL } from '@/lib/site';
import { logout, notifySearchEngines } from './actions';

const STATUS = {
  pending: 'Waiting for supplier order',
  placed: 'Ordered at CJ',
  unpaid: 'Needs CJ payment',
  shipped: 'Shipped',
  error: 'Supplier order failed',
};

export default async function Admin({ searchParams }) {
  const { msg } = await searchParams;
  const checks = readiness();
  const stripeReady = checks[0].ok;
  let orders = [];
  let loadError = '';
  if (stripeReady) {
    try {
      orders = await recentOrders(30);
    } catch (err) {
      loadError = err.message;
    }
  }
  const stats = summarize(orders);
  const balance = await cjBalance();
  const done = checks.filter((c) => c.ok).length;

  return (
    <>
      <div className="admin-head">
        <h1>Store admin</h1>
        <form action={logout}><button className="link">Log out</button></form>
      </div>
      {msg && <p className="notice">{msg}</p>}

      <div className="tiles">
        <Tile label="Today" value={money(stats.today.revenue)} sub={`${stats.today.count} orders`} />
        <Tile label="Last 7 days" value={money(stats.week.revenue)} sub={`${stats.week.count} orders`} />
        <Tile label="Last 30 days" value={money(stats.month.revenue)} sub={`${stats.month.count} orders · avg ${money(stats.month.aov)}`} />
        <Tile
          label="CJ wallet"
          value={balance.configured ? (balance.error ? 'Error' : money(Math.round((balance.amount || 0) * 100))) : '—'}
          sub={balance.configured ? (balance.error ? balance.error.slice(0, 60) : 'Balance for supplier orders') : 'Add CJ_API_KEY'}
        />
      </div>

      {stats.needsAction.length > 0 && (
        <section className="panel warn">
          <h2>Needs your attention ({stats.needsAction.length})</h2>
          <ul>
            {stats.needsAction.map((o) => (
              <li key={o.id}>
                <Link href={`/admin/orders/${o.id}`}>{new Date(o.created).toLocaleString('en-US')} · {o.email} · {money(o.amount)}</Link> · {STATUS[o.fulfillment] || o.fulfillment}
              </li>
            ))}
          </ul>
        </section>
      )}

      <section className="panel">
        <h2>Orders (last 30 days)</h2>
        {!stripeReady && <p>Add your Stripe key to see orders.</p>}
        {loadError && <p className="error">Couldn’t load orders: {loadError}</p>}
        {stripeReady && !loadError && orders.length === 0 && <p>No orders yet.</p>}
        {orders.length > 0 && (
          <div className="table-wrap">
            <table>
              <thead><tr><th>Date</th><th>Customer</th><th>Total</th><th>Status</th><th>Tracking</th></tr></thead>
              <tbody>
                {orders.map((o) => (
                  <tr key={o.id}>
                    <td><Link href={`/admin/orders/${o.id}`}>{new Date(o.created).toLocaleDateString('en-US')}</Link></td>
                    <td>{o.name || o.email}</td>
                    <td>{money(o.amount)}</td>
                    <td><span className={`pill ${o.fulfillment}`}>{STATUS[o.fulfillment] || o.fulfillment}</span></td>
                    <td>{o.tracking || '—'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      <section className="panel">
        <h2>Search engines &amp; AI visibility</h2>
        <ul className="links">
          <li><a href={`${SITE_URL}/sitemap.xml`} target="_blank">Sitemap</a> · <a href={`${SITE_URL}/robots.txt`} target="_blank">robots.txt</a> · <a href={`${SITE_URL}/llms.txt`} target="_blank">llms.txt</a> · <a href={`${SITE_URL}/products.xml`} target="_blank">Shopping feed</a></li>
          <li><a href="https://search.google.com/search-console" target="_blank">Google Search Console</a> · <a href="https://www.bing.com/webmasters" target="_blank">Bing Webmaster Tools</a> · <a href="https://merchants.google.com" target="_blank">Google Merchant Center</a></li>
          <li><a href={`https://search.google.com/test/rich-results?url=${encodeURIComponent(SITE_URL)}`} target="_blank">Test rich results</a> · <a href={`https://pagespeed.web.dev/analysis?url=${encodeURIComponent(SITE_URL)}`} target="_blank">PageSpeed</a></li>
        </ul>
        <form action={notifySearchEngines}><button className="cta inline">Notify search engines (IndexNow)</button></form>
      </section>

      <section className="panel">
        <h2>Launch checklist ({done}/{checks.length})</h2>
        <ul className="checks">
          {checks.map((c) => (
            <li key={c.label} className={c.ok ? 'ok' : 'todo'}>
              <span aria-hidden>{c.ok ? '✓' : '○'}</span> <b>{c.group}:</b> {c.label} <small>{c.ok ? c.note === 'Test mode' || c.note === 'Live mode' ? c.note : '' : `set ${c.note}`}</small>
            </li>
          ))}
        </ul>
      </section>

      <section className="panel">
        <h2>Quick links</h2>
        <ul className="links">
          <li><a href="https://dashboard.stripe.com/payments" target="_blank">Stripe payments &amp; refunds</a></li>
          <li><a href="https://cjdropshipping.com" target="_blank">CJ Dropshipping (orders, wallet)</a></li>
          <li><a href="https://resend.com/emails" target="_blank">Sent emails (Resend)</a></li>
          <li><a href="https://vercel.com/dashboard" target="_blank">Vercel (hosting, settings, logs)</a></li>
        </ul>
      </section>
    </>
  );
}

function Tile({ label, value, sub }) {
  return (
    <div className="tile">
      <small>{label}</small>
      <strong>{value}</strong>
      <span>{sub}</span>
    </div>
  );
}
