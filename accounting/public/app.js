/* Zsi Books – single-page frontend (no build step). */
'use strict';

const S = { user: null, settings: {}, accounts: [], contacts: [] };
const root = document.getElementById('root');

// ---------- utilities ----------
const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const money = (c, blankZero) => {
  if (c == null || c === '') return '';
  if (blankZero && !c) return '';
  const s = '$' + (Math.abs(c) / 100).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  return c < 0 ? `<span class="neg">(${s})</span>` : s;
};
const plain = c => (c / 100).toFixed(2);
const today = () => new Date().toISOString().slice(0, 10);
const addDays = (d, n) => { const x = new Date(d + 'T00:00:00Z'); x.setUTCDate(x.getUTCDate() + n); return x.toISOString().slice(0, 10); };
const canWrite = () => S.user && ['owner', 'staff'].includes(S.user.role);
const isOwner = () => S.user && S.user.role === 'owner';
const KIND = { expense: 'Expense', income: 'Income', owner_contribution: 'Owner deposit', owner_draw: 'Owner withdrawal', transfer: 'Transfer', payroll: 'Payroll', journal: 'Journal', invoice: 'Invoice', invoice_payment: 'Invoice payment', import: 'Bank import', void: 'Reversal' };

async function api(method, url, body) {
  const opt = { method, headers: {} };
  if (body instanceof FormData) opt.body = body;
  else if (body !== undefined) { opt.headers['Content-Type'] = 'application/json'; opt.body = JSON.stringify(body); }
  const r = await fetch(url, opt);
  if (r.status === 401 && !url.includes('/api/login')) { S.user = null; boot(); throw new Error('Please sign in'); }
  const data = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(data.error || `Request failed (${r.status})`);
  return data;
}
function toast(msg, err) {
  document.querySelectorAll('.toast').forEach(x => x.remove());
  const t = document.createElement('div');
  t.className = 'toast' + (err ? ' err' : '');
  t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(() => t.remove(), err ? 6000 : 3000);
}
const formObj = form => {
  const o = {};
  new FormData(form).forEach((v, k) => { if (!(v instanceof File)) o[k] = v; });
  form.querySelectorAll('input[type=checkbox][name]').forEach(c => { o[c.name] = c.checked; });
  return o;
};
async function guard(fn, btn) {
  if (btn) btn.disabled = true;
  try { return await fn(); } catch (e) { toast(e.message, true); } finally { if (btn) btn.disabled = false; }
}
async function loadRefs() {
  [S.accounts, S.contacts] = await Promise.all([api('GET', '/api/accounts'), api('GET', '/api/contacts')]);
}
const acct = id => S.accounts.find(a => a.id === Number(id));

// <option> builders
function acctOptions(groups, selected, placeholder = 'Choose…') {
  let h = `<option value="">${esc(placeholder)}</option>`;
  for (const [label, filter] of groups) {
    const list = S.accounts.filter(a => a.active && filter(a));
    if (!list.length) continue;
    h += `<optgroup label="${esc(label)}">` + list.map(a => `<option value="${a.id}" ${Number(selected) === a.id ? 'selected' : ''}>${esc(a.code)} · ${esc(a.name)}</option>`).join('') + '</optgroup>';
  }
  return h;
}
const G = {
  payment: [['Bank & cash', a => a.is_payment && a.type === 'asset'], ['Credit cards', a => a.is_payment && a.type !== 'asset']],
  expense: [['Expenses', a => a.type === 'expense'], ['Buy an asset / prepay', a => a.type === 'asset' && !a.is_payment && a.subtype !== 'receivable'],
    ['Pay down a liability (payroll taxes, sales tax, loans, bills)', a => a.type === 'liability' && !a.is_payment]],
  income: [['Income', a => a.type === 'income'], ['Loan received / other liability', a => a.type === 'liability' && !a.is_payment], ['Refund of an expense', a => a.type === 'expense']],
  all: [['Assets', a => a.type === 'asset'], ['Liabilities', a => a.type === 'liability'], ['Equity', a => a.type === 'equity'], ['Income', a => a.type === 'income'], ['Expenses', a => a.type === 'expense']],
  category: [['Income', a => a.type === 'income'], ['Expenses', a => a.type === 'expense'], ['Owner capital / draws', a => a.type === 'equity' && a.owner_contact_id],
    ['Liabilities (taxes, loans, bills)', a => a.type === 'liability' && !a.is_payment], ['Other assets', a => a.type === 'asset' && !a.is_payment], ['Other equity', a => a.type === 'equity' && !a.owner_contact_id]],
};
function contactOptions(type, selected, { allowNew = true, blank = 'None' } = {}) {
  const list = S.contacts.filter(c => (!type || c.type === type) && c.active);
  let h = blank !== false ? `<option value="">${esc(blank)}</option>` : '';
  h += list.map(c => `<option value="${c.id}" ${Number(selected) === c.id ? 'selected' : ''}>${esc(c.name)}${type ? '' : ` (${c.type})`}</option>`).join('');
  if (allowNew && canWrite()) h += `<option value="__new">+ Add new ${type || 'contact'}…</option>`;
  return h;
}
// "+ Add new" handling for any contact <select data-ctype>
document.addEventListener('change', async e => {
  const sel = e.target;
  if (sel.tagName !== 'SELECT' || sel.value !== '__new') return;
  const type = sel.dataset.ctype || 'vendor';
  const name = prompt(`New ${type} name:`);
  if (!name) { sel.value = ''; return; }
  await guard(async () => {
    const r = await api('POST', '/api/contacts', { type, name });
    await loadRefs();
    document.querySelectorAll(`select[data-ctype="${type}"]`).forEach(s => {
      const keep = s === sel ? r.id : s.value;
      s.innerHTML = contactOptions(type, keep, { blank: s.dataset.blank || 'None' });
    });
    toast(`${name} added`);
  });
});

// ---------- routing ----------
function parseHash() {
  const h = location.hash.slice(1) || '/';
  const [p, qs] = h.split('?');
  return { parts: p.split('/').filter(Boolean), q: Object.fromEntries(new URLSearchParams(qs || '')) };
}
window.addEventListener('hashchange', () => render());

async function boot() {
  const st = await api('GET', '/api/state');
  S.user = st.user; S.settings = st.settings || {};
  if (!st.setup) return setupPage();
  if (!S.user) return loginPage();
  await loadRefs();
  render();
}

const NAV = [
  ['', 'Dashboard'], ['new/expense', '＋ Record money'], ['transactions', 'Transactions'], ['invoices', 'Invoices'],
  ['contacts', 'Clients, vendors & people'], ['accounts', 'Chart of accounts'], ['sep'], ['reconcile', 'Reconcile bank'], ['import', 'Import bank CSV'],
  ['sep'], ['reports', 'Reports & tax package'], ['settings', 'Settings'],
];

function shell(active) {
  const nav = NAV.filter(([p]) => canWrite() || !['new/expense', 'import'].includes(p)).map(([p, l]) => p === 'sep' ? '<div class="sep"></div>' :
    `<a href="#/${p}" class="${active === p.split('/')[0] ? 'on' : ''}">${esc(l)}</a>`).join('');
  root.innerHTML = `
  <div class="mobilebar"><b>Zsi Books</b><button id="menuBtn">Menu</button></div>
  <div class="app">
    <nav class="side" id="side">
      <div class="logo">Zsi Books</div>
      <div class="co">${esc(S.settings.company || '')}</div>
      ${nav}
      <div class="sep"></div>
      <div class="who">${esc(S.user.name)} · ${esc(S.user.role)}<br><a href="#" id="logout" style="padding:4px 0;display:inline">Sign out</a></div>
    </nav>
    <main class="main" id="main"><p class="muted">Loading…</p></main>
  </div>`;
  document.getElementById('menuBtn').onclick = () => document.getElementById('side').classList.toggle('open');
  document.getElementById('side').addEventListener('click', e => { if (e.target.tagName === 'A') document.getElementById('side').classList.remove('open'); });
  document.getElementById('logout').onclick = async e => { e.preventDefault(); await api('POST', '/api/logout'); S.user = null; boot(); };
  return document.getElementById('main');
}

async function render() {
  if (!S.user) return;
  const { parts, q } = parseHash();
  const page = parts[0] || '';
  const main = shell(page);
  window.scrollTo(0, 0);
  try {
    const fn = {
      '': dashboard, new: newTx, transactions, entry: entryPage, invoices, invoice: invoicePage, contacts, accounts,
      reconcile, import: importPage, reports: reportsPage, report: reportView, settings,
    }[page];
    if (!fn) main.innerHTML = '<p>Page not found.</p>';
    else await fn(main, parts, q);
  } catch (e) {
    main.innerHTML = `<div class="note">${esc(e.message)}</div>`;
  }
}

// ---------- setup & login ----------
function setupPage() {
  root.innerHTML = `<div class="center"><div class="card">
    <h1>Set up your books</h1><p class="muted">One-time setup. You can change everything later in Settings.</p>
    <form id="f">
      <div class="field"><label>Company legal name</label><input name="company" required placeholder="Zsi.AI LLC"></div>
      <div class="grid g2">
        <div class="field"><label>Entity / tax type</label><select name="entity_type">
          <option>Multi-member LLC (taxed as partnership – Form 1065)</option><option>S Corporation (Form 1120-S)</option>
          <option>C Corporation (Form 1120)</option><option>Single-member LLC (Schedule C)</option><option>Not sure – ask accountant</option></select></div>
        <div class="field"><label>EIN (optional)</label><input name="ein" placeholder="12-3456789"></div>
      </div>
      <div class="field"><label>Business address</label><textarea name="address" placeholder="Street&#10;New York, NY 100xx"></textarea></div>
      <div class="grid g2">
        <div class="field"><label>Main bank account name</label><input name="bank_name" value="Business Checking"></div>
        <div class="field"><label>Fiscal year starts</label><select name="fiscal_start_month">${[...Array(12)].map((_, i) => `<option value="${i + 1}">${new Date(2000, i, 1).toLocaleString('en-US', { month: 'long' })}</option>`).join('')}</select></div>
      </div>
      <h3>Owners</h3>
      <div class="grid g2"><div class="field"><label>Owner 1 name</label><input name="o1" required></div><div class="field"><label>Owner 1 profit share %</label><input name="s1" type="number" step="0.01" value="50"></div></div>
      <div class="grid g2"><div class="field"><label>Owner 2 name</label><input name="o2"></div><div class="field"><label>Owner 2 profit share %</label><input name="s2" type="number" step="0.01" value="50"></div></div>
      <h3>Your login</h3>
      <div class="field"><label>Your name</label><input name="name" required></div>
      <div class="grid g2"><div class="field"><label>Email</label><input name="email" type="email" required></div>
      <div class="field"><label>Password (8+ characters)</label><input name="password" type="password" minlength="8" required></div></div>
      <button class="primary" style="width:100%;justify-content:center">Create my books</button>
    </form></div></div>`;
  document.getElementById('f').onsubmit = e => {
    e.preventDefault();
    const b = formObj(e.target);
    b.owners = [{ name: b.o1, share: b.s1 }, { name: b.o2, share: b.s2 }];
    guard(async () => {
      await api('POST', '/api/setup', b);
      await api('POST', '/api/login', { email: b.email, password: b.password });
      location.hash = '#/';
      boot();
    }, e.submitter);
  };
}
function loginPage() {
  root.innerHTML = `<div class="center"><div class="card"><h1>Zsi Books</h1><p class="muted">${esc(S.settings.company || 'Sign in')}</p>
    <form id="f"><div class="field"><label>Email</label><input name="email" type="email" required autofocus></div>
    <div class="field"><label>Password</label><input name="password" type="password" required></div>
    <button class="primary" style="width:100%;justify-content:center">Sign in</button></form></div></div>`;
  document.getElementById('f').onsubmit = e => {
    e.preventDefault();
    guard(async () => { await api('POST', '/api/login', formObj(e.target)); boot(); }, e.submitter);
  };
}

// ---------- dashboard ----------
async function dashboard(main) {
  const d = await api('GET', '/api/dashboard');
  const cash = d.accounts.filter(a => a.type === 'asset').reduce((t, a) => t + a.balance, 0);
  const max = Math.max(1, ...d.months.map(m => Math.max(m.income, m.expenses)));
  main.innerHTML = `
  <div class="top"><div><h1>Dashboard</h1><div class="muted">Fiscal year from ${d.fy} · today ${d.today}</div></div>
    ${canWrite() ? '<div class="row"><a class="btn primary" href="#/new/expense">＋ Record money</a><a class="btn" href="#/invoices/new">New invoice</a></div>' : ''}</div>
  <div class="grid g4">
    <div class="kpi"><div class="l">Cash in bank</div><div class="v">${money(cash)}</div><div class="s">${d.accounts.filter(a => a.type === 'asset').length} accounts</div></div>
    <div class="kpi"><div class="l">Profit this year</div><div class="v">${money(d.ytd.net)}</div><div class="s">${money(d.ytd.income)} in · ${money(d.ytd.expenses)} out</div></div>
    <div class="kpi"><div class="l">Clients owe you</div><div class="v">${money(d.ar)}</div><div class="s ${d.overdue ? 'bad' : ''}">${d.overdue ? money(d.overdue) + ' overdue' : 'nothing overdue'}</div></div>
    <div class="kpi"><div class="l">Taxes held / owed</div><div class="v">${money(d.taxes_owed)}</div><div class="s">payroll & sales tax liabilities</div></div>
  </div>
  ${d.missing_receipts ? `<div class="note" style="margin-top:14px">${d.missing_receipts} expense(s) this year have no receipt attached. <a href="#/report/missing_receipts">Fix them</a> so your accountant has proof.</div>` : ''}
  ${canWrite() ? `<div class="card" style="margin-top:14px"><h2>What happened?</h2><div class="actions">
    <a href="#/new/expense">Paid a bill / expense<span>rent, hosting, software…</span></a>
    <a href="#/new/payroll">Paid salary<span>payroll with withholdings</span></a>
    <a href="#/invoices/new">Billed a client<span>create invoice</span></a>
    <a href="#/new/income">Client paid / money in<span>without an invoice</span></a>
    <a href="#/new/owner_contribution">Owner put money in<span>capital deposit</span></a>
    <a href="#/new/owner_draw">Owner took money out<span>draw / distribution</span></a>
    <a href="#/new/transfer">Moved money<span>between accounts / pay card</span></a>
    <a href="#/import">Import bank statement<span>CSV from your bank</span></a>
  </div></div>` : ''}
  <div class="grid g2">
    <div class="card"><h2>Income vs expenses – last 12 months</h2>
      <div class="legend"><span><i style="background:#3b5bfd"></i>Income</span><span><i style="background:#f79009"></i>Expenses</span></div>
      <div class="bars">${d.months.map(m => `<div class="m" title="${m.month}: in ${plain(m.income)}, out ${plain(m.expenses)}">
        <div class="pair"><div class="b inc" style="height:${Math.max(0, m.income) / max * 100}%"></div><div class="b exp" style="height:${Math.max(0, m.expenses) / max * 100}%"></div></div>
        <div class="lab">${m.month.slice(5)}</div></div>`).join('')}</div>
    </div>
    <div class="card"><h2>Accounts</h2><table class="t">${d.accounts.map(a => `<tr class="click" data-href="#/report/general_ledger?account_id=${a.id}"><td>${esc(a.name)}</td><td class="num">${money(a.balance)}</td></tr>`).join('')}</table>
      <h3>Owners – net money put in</h3><table class="t">${d.owners.map(o => `<tr><td>${esc(o.name)} <span class="muted small">${esc(o.share)}</span></td><td class="num">${money(o.net)}</td></tr>`).join('') || '<tr><td class="muted">No owners yet</td></tr>'}</table>
      <div class="small" style="margin-top:6px"><a href="#/report/owner_equity">Owner capital statement →</a></div>
    </div>
  </div>
  <div class="card"><div class="row"><h2>Recent activity</h2><a class="right" href="#/transactions">All transactions →</a></div>${entryTable(d.recent)}</div>`;
  bindRowLinks(main);
}

function entryTable(list) {
  if (!list.length) return '<p class="muted">Nothing recorded yet.</p>';
  return `<div class="tablewrap"><table class="t"><tr><th>Date</th><th>#</th><th>Type</th><th>Name</th><th>Memo</th>${list[0].accounts !== undefined ? '<th>Accounts</th>' : ''}<th class="num">Amount</th><th></th></tr>
  ${list.map(e => `<tr class="click ${e.voided ? 'voided' : ''}" data-href="#/entry/${e.id}"><td>${e.date}</td><td>${e.id}</td><td>${esc(KIND[e.kind] || e.kind)}</td>
    <td>${esc(e.contact_name || '')}</td><td>${esc(e.memo || '')}${e.reference ? ` <span class="muted small">Ref ${esc(e.reference)}</span>` : ''}</td>
    ${e.accounts !== undefined ? `<td class="small muted">${esc(e.accounts || '')}</td>` : ''}<td class="num">${money(e.amount)}</td>
    <td>${e.attachments ? '📎' : ''}${e.voided ? ' <span class="badge bad">void</span>' : ''}</td></tr>`).join('')}</table></div>`;
}
function bindRowLinks(el) {
  el.querySelectorAll('tr[data-href]').forEach(tr => tr.addEventListener('click', e => { if (e.target.closest('a,button,input,select')) return; location.hash = tr.dataset.href; }));
}

// ---------- record money ----------
const TX_TABS = [['expense', 'Expense / bill'], ['income', 'Money in'], ['owner_contribution', 'Owner deposit'], ['owner_draw', 'Owner withdrawal'], ['payroll', 'Payroll'], ['transfer', 'Transfer'], ['journal', 'Journal entry']];

async function newTx(main, parts) {
  if (!canWrite()) { main.innerHTML = '<div class="note">Your role is read-only.</div>'; return; }
  const type = parts[1] || 'expense';
  const tabs = `<div class="tabs">${TX_TABS.map(([t, l]) => `<a href="#/new/${t}" class="${t === type ? 'on' : ''}">${l}</a>`).join('')}</div>`;
  const common = `<div class="grid g2"><div class="field"><label>Memo / description</label><input name="memo"></div>
    <div class="field"><label>Reference (check #, bill #, transaction ID)</label><input name="reference"></div></div>
    <div class="field"><label>Receipt / bill / proof (photo or PDF)</label><input type="file" name="files" multiple accept="image/*,application/pdf,.doc,.docx,.xls,.xlsx,.csv,.txt"><div class="hint">Attach it now – the accountant will need it.</div></div>`;
  const payFrom = (name, label) => `<div class="field"><label>${label}</label><select name="${name}" required>${acctOptions(G.payment, S.accounts.find(a => a.code === '1000')?.id)}</select></div>`;
  const dateF = `<div class="field"><label>Date</label><input type="date" name="date" value="${today()}" required></div>`;
  const amt = (name = 'amount', label = 'Amount ($)') => `<div class="field"><label>${label}</label><input name="${name}" type="number" step="0.01" min="0" inputmode="decimal" required></div>`;
  let body = '';
  const owners = S.contacts.filter(c => c.type === 'owner' && c.active);
  if (type === 'expense') {
    body = `<div class="info">Use this for rent, hosting, software, AI/API bills, contractors, fees – and for paying payroll taxes or sales tax you owe (choose it under “Pay down a liability”). To pay off the credit card from the bank, use <a href="#/new/transfer">Transfer</a>.</div>
    <div class="grid g3">${dateF}<div class="field"><label>Paid to (vendor)</label><select name="contact_id" data-ctype="vendor">${contactOptions('vendor')}</select></div>${payFrom('paid_from', 'Paid from')}</div>
    <div id="items"></div><button type="button" id="split">＋ Split across another category</button>
    <div class="right" style="font-weight:700;margin:8px 0" id="tot"></div>`;
  } else if (type === 'income') {
    body = `<div class="info">For money received <b>without an invoice</b>. If you sent an invoice, open the invoice and click “Record payment” instead. Owner deposits go under <a href="#/new/owner_contribution">Owner deposit</a> – never as income.</div>
    <div class="grid g2">${dateF}<div class="field"><label>Received from</label><select name="contact_id" data-ctype="client">${contactOptions('client')}</select></div></div>
    <div class="grid g3"><div class="field"><label>Category</label><select name="account_id" required>${acctOptions(G.income, S.accounts.find(a => a.code === '4000')?.id)}</select></div>${amt()}${payFrom('deposit_to', 'Deposited to')}</div>`;
  } else if (type === 'owner_contribution' || type === 'owner_draw') {
    const inn = type === 'owner_contribution';
    body = `<div class="info">${inn ? 'Money an owner puts into the company is <b>owner capital</b> (equity). It is not income and not taxed as revenue. Each owner’s total is tracked separately.' : 'Money an owner takes out for personal use is an <b>owner draw</b>. It is not a business expense and not salary.'}</div>
    <div class="grid g2">${dateF}<div class="field"><label>Owner</label><select name="contact_id" required data-ctype="owner" data-blank="Choose owner…">${contactOptions('owner', owners.length === 1 ? owners[0].id : null, { blank: 'Choose owner…' })}</select></div></div>
    <div class="grid g2">${amt()}${payFrom(inn ? 'deposit_to' : 'paid_from', inn ? 'Deposited into' : 'Paid from')}</div>`;
  } else if (type === 'transfer') {
    body = `<div class="info">Moving money between your own accounts (checking → savings), or paying the credit card bill from the bank. Not income, not expense.</div>
    <div class="grid g2">${dateF}${amt()}</div><div class="grid g2">${payFrom('from_account', 'From')}<div class="field"><label>To</label><select name="to_account" required>${acctOptions(G.payment)}</select></div></div>`;
  } else if (type === 'payroll') {
    const f = (n, l, hint) => `<div class="field"><label>${l}</label><input name="${n}" type="number" step="0.01" min="0" inputmode="decimal" value="">${hint ? `<div class="hint">${hint}</div>` : ''}</div>`;
    body = `<div class="info">Record one pay run per employee. Copy the numbers from your payroll provider’s pay stub (Gusto, ADP, etc.). This records wages, every tax withheld (owed to IRS / NY), and employer taxes – exactly what the accountant needs for W-2, 941, 940 and NYS-45.</div>
    <div class="grid g3">${dateF}<div class="field"><label>Employee</label><select name="contact_id" required data-ctype="employee" data-blank="Choose employee…">${contactOptions('employee', null, { blank: 'Choose employee…' })}</select></div>${payFrom('paid_from', 'Net pay paid from')}</div>
    <div class="grid g3"><div class="field"><label>Pay period start</label><input type="date" name="period_start"></div><div class="field"><label>Pay period end</label><input type="date" name="period_end"></div>${f('gross', 'Gross pay ($)')}</div>
    <h3>Withheld from employee</h3>
    <div class="grid g4">${f('fed_wh', 'Federal income tax')}${f('ss_ee', 'Social Security (6.2%)')}${f('med_ee', 'Medicare (1.45%)')}${f('state_wh', 'NY State income tax')}</div>
    <div class="grid g4">${f('city_wh', 'NYC income tax')}${f('sdi_pfl', 'NY SDI / Paid Family Leave')}${f('other_ded', 'Other deductions', 'e.g. health premium, 401k')}<div class="field"><label>Net pay (calculated)</label><input id="net" disabled></div></div>
    <h3>Paid by the company (employer taxes)</h3>
    <div class="grid g4">${f('ss_er', 'Social Security (6.2%)')}${f('med_er', 'Medicare (1.45%)')}${f('futa', 'FUTA')}${f('suta', 'NY Unemployment (SUI)')}</div>
    <button type="button" id="fica" style="margin-bottom:16px">Auto-fill Social Security & Medicare from gross</button>`;
  } else if (type === 'journal') {
    body = `<div class="info">Advanced: free-form double-entry. Total debits must equal total credits. Mostly for the accountant’s adjustments (depreciation, accruals, opening balances).</div>
    <div class="grid g2">${dateF}<div class="field"><label>Contact (optional)</label><select name="contact_id" data-ctype="vendor">${contactOptions(null, null, { allowNew: false })}</select></div></div>
    <div class="tablewrap"><table class="t" id="jl"><tr><th>Account</th><th>Debit</th><th>Credit</th><th>Line memo</th></tr></table></div>
    <div class="row" style="margin:8px 0"><button type="button" id="addl">＋ Line</button><span class="right" id="jt"></span></div>`;
  }
  main.innerHTML = `<div class="top"><h1>Record money</h1></div>${tabs}<div class="card"><form id="f">${body}${common}
    <div class="row"><button class="primary" name="go" value="view">Save</button><button name="go" value="new">Save & add another</button></div></form></div>`;
  const form = document.getElementById('f');

  if (type === 'expense') {
    const box = document.getElementById('items');
    const addItem = () => {
      const d = document.createElement('div');
      d.className = 'grid g3 item';
      d.innerHTML = `<div class="field"><label>Category</label><select class="ia" required>${acctOptions(G.expense)}</select></div>
        <div class="field"><label>Amount ($)</label><input class="iv" type="number" step="0.01" inputmode="decimal" required></div>
        <div class="field"><label>Line note (optional)</label><input class="im"></div>`;
      box.appendChild(d);
    };
    addItem();
    document.getElementById('split').onclick = addItem;
    form.addEventListener('input', () => {
      const t = [...form.querySelectorAll('.iv')].reduce((s, i) => s + Math.round(Number(i.value || 0) * 100), 0);
      document.getElementById('tot').innerHTML = form.querySelectorAll('.item').length > 1 ? 'Total: ' + money(t) : '';
    });
  }
  if (type === 'payroll') {
    const n = k => Math.round(Number(form.elements[k].value || 0) * 100);
    const calc = () => { document.getElementById('net').value = plain(n('gross') - ['fed_wh', 'ss_ee', 'med_ee', 'state_wh', 'city_wh', 'sdi_pfl', 'other_ded'].reduce((s, k) => s + n(k), 0)); };
    form.addEventListener('input', calc);
    document.getElementById('fica').onclick = () => {
      const g = n('gross');
      form.elements.ss_ee.value = form.elements.ss_er.value = plain(Math.round(g * 0.062));
      form.elements.med_ee.value = form.elements.med_er.value = plain(Math.round(g * 0.0145));
      calc();
    };
  }
  if (type === 'journal') {
    const tbl = document.getElementById('jl');
    const add = () => {
      const tr = tbl.insertRow();
      tr.className = 'jline';
      tr.innerHTML = `<td><select class="ja">${acctOptions(G.all)}</select></td><td><input class="jd" type="number" step="0.01" min="0"></td><td><input class="jc" type="number" step="0.01" min="0"></td><td><input class="jm"></td>`;
    };
    add(); add();
    document.getElementById('addl').onclick = add;
    form.addEventListener('input', () => {
      const s = c => [...form.querySelectorAll(c)].reduce((t, i) => t + Math.round(Number(i.value || 0) * 100), 0);
      const d = s('.jd'), c = s('.jc');
      document.getElementById('jt').innerHTML = `Debits ${money(d)} · Credits ${money(c)} ${d === c ? '<span class="badge good">balanced</span>' : '<span class="badge bad">off by ' + money(d - c) + '</span>'}`;
    });
  }

  form.onsubmit = e => {
    e.preventDefault();
    const b = formObj(form);
    if (type === 'expense') b.items = [...form.querySelectorAll('.item')].map(d => ({ account_id: d.querySelector('.ia').value, amount: d.querySelector('.iv').value, memo: d.querySelector('.im').value }));
    if (type === 'journal') b.lines = [...form.querySelectorAll('.jline')].map(r => ({ account_id: r.querySelector('.ja').value, debit: r.querySelector('.jd').value, credit: r.querySelector('.jc').value, memo: r.querySelector('.jm').value })).filter(l => l.account_id);
    if (b.contact_id === '__new') b.contact_id = '';
    const go = e.submitter && e.submitter.value;
    guard(async () => {
      const r = await api('POST', `/api/tx/${type}`, b);
      await uploadFiles(r.id, form.querySelector('input[type=file]'));
      toast(`Saved as entry #${r.id}`);
      if (go === 'new') render(); else location.hash = `#/entry/${r.id}`;
    }, e.submitter);
  };
}
async function uploadFiles(entryId, input) {
  if (!input || !input.files.length) return;
  const fd = new FormData();
  [...input.files].forEach(f => fd.append('files', f));
  await api('POST', `/api/entries/${entryId}/attachments`, fd);
}

// ---------- transactions ----------
async function transactions(main, parts, q) {
  const qs = new URLSearchParams(Object.entries(q).filter(([, v]) => v)).toString();
  const list = await api('GET', '/api/entries?' + qs);
  main.innerHTML = `<div class="top"><h1>Transactions</h1>${canWrite() ? '<a class="btn primary" href="#/new/expense">＋ Record money</a>' : ''}</div>
  <div class="card"><form id="flt" class="grid g4" style="align-items:end">
    <div class="field"><label>From</label><input type="date" name="from" value="${esc(q.from || '')}"></div>
    <div class="field"><label>To</label><input type="date" name="to" value="${esc(q.to || '')}"></div>
    <div class="field"><label>Type</label><select name="kind"><option value="">All</option>${Object.entries(KIND).map(([k, v]) => `<option value="${k}" ${q.kind === k ? 'selected' : ''}>${v}</option>`).join('')}</select></div>
    <div class="field"><label>Account</label><select name="account_id">${acctOptions(G.all, q.account_id, 'All')}</select></div>
    <div class="field"><label>Contact</label><select name="contact_id">${contactOptions(null, q.contact_id, { allowNew: false, blank: 'All' })}</select></div>
    <div class="field"><label>Search</label><input name="q" value="${esc(q.q || '')}" placeholder="memo, ref, name, #"></div>
    <div class="field"><button class="primary">Filter</button> <a class="btn" href="#/transactions">Clear</a></div>
  </form></div>
  <div class="card">${entryTable(list)}<div class="muted small" style="margin-top:8px">${list.length} shown</div></div>`;
  document.getElementById('flt').onsubmit = e => { e.preventDefault(); location.hash = '#/transactions?' + new URLSearchParams(Object.entries(formObj(e.target)).filter(([, v]) => v)).toString(); };
  bindRowLinks(main);
}

async function entryPage(main, parts) {
  const e = await api('GET', `/api/entries/${parts[1]}`);
  const dr = e.lines.reduce((s, l) => s + l.debit, 0);
  const p = e.payroll;
  main.innerHTML = `<div class="top"><div><h1>${esc(KIND[e.kind] || e.kind)} #${e.id} ${e.voided ? '<span class="badge bad">VOIDED</span>' : ''}</h1>
    <div class="muted">${e.date} · ${money(dr)} · entered by ${esc(e.created_by_name || '—')} on ${esc(e.created_at)} UTC</div></div>
    <div class="row">${isOwner() && !e.voided && e.kind !== 'void' ? '<button class="danger" id="void">Void…</button>' : ''}</div></div>
  ${e.reversal ? `<div class="note">This entry was voided. Reversal: <a href="#/entry/${e.reversal.id}">#${e.reversal.id}</a></div>` : ''}
  ${e.void_of ? `<div class="note">This is the reversal of <a href="#/entry/${e.void_of}">#${e.void_of}</a>.</div>` : ''}
  ${e.invoice ? `<div class="info">Linked to invoice <a href="#/invoice/${e.invoice.id}">${esc(e.invoice.number)}</a></div>` : ''}
  <div class="grid g2">
    <div class="card"><h2>Details</h2>
      <form id="mf"><div class="field"><label>Name</label><div>${esc(e.contact_name || '—')}</div></div>
      <div class="field"><label>Memo</label><input name="memo" value="${esc(e.memo || '')}" ${canWrite() ? '' : 'disabled'}></div>
      <div class="field"><label>Reference</label><input name="reference" value="${esc(e.reference || '')}" ${canWrite() ? '' : 'disabled'}></div>
      ${canWrite() ? '<button>Save memo</button>' : ''}</form>
      <div class="hint">Amounts and accounts can’t be edited – void the entry and record it again. That keeps a clean audit trail.</div>
    </div>
    <div class="card"><h2>Receipts & documents</h2>
      ${e.attachments.map(a => `<div><a href="/api/attachments/${a.id}" target="_blank">📎 ${esc(a.filename)}</a> <span class="muted small">${Math.round(a.size / 1024)} KB</span></div>`).join('') || '<p class="muted">None attached.</p>'}
      ${canWrite() ? `<form id="af" style="margin-top:12px"><input type="file" name="files" multiple required><button style="margin-top:8px">Upload</button></form>` : ''}
    </div>
  </div>
  <div class="card"><h2>Journal lines</h2><div class="tablewrap"><table class="t"><tr><th>Account</th><th>Memo</th><th class="num">Debit</th><th class="num">Credit</th></tr>
    ${e.lines.map(l => `<tr class="click" data-href="#/report/general_ledger?account_id=${l.account_id}"><td>${esc(l.code)} · ${esc(l.account_name)}</td><td>${esc(l.memo || '')}</td><td class="num">${money(l.debit, 1)}</td><td class="num">${money(l.credit, 1)}</td></tr>`).join('')}
    <tr class="total"><td>Total</td><td></td><td class="num">${money(dr)}</td><td class="num">${money(e.lines.reduce((s, l) => s + l.credit, 0))}</td></tr></table></div></div>
  ${p ? `<div class="card"><h2>Pay stub</h2><table class="t">${[['Gross', p.gross], ['Federal WH', p.fed_wh], ['Soc. Sec. (EE)', p.ss_ee], ['Medicare (EE)', p.med_ee], ['NY State WH', p.state_wh], ['NYC WH', p.city_wh], ['NY SDI/PFL', p.sdi_pfl], ['Other', p.other_ded], ['Net pay', p.net], ['Soc. Sec. (ER)', p.ss_er], ['Medicare (ER)', p.med_er], ['FUTA', p.futa], ['NY SUI', p.suta]]
    .map(([l, v]) => `<tr><td>${l}</td><td class="num">${money(v)}</td></tr>`).join('')}</table><div class="muted small">Period ${esc(p.period_start || '?')} – ${esc(p.period_end || '?')}</div></div>` : ''}`;
  bindRowLinks(main);
  const mf = document.getElementById('mf');
  mf.onsubmit = ev => { ev.preventDefault(); guard(async () => { await api('PATCH', `/api/entries/${e.id}`, formObj(mf)); toast('Saved'); }, ev.submitter); };
  const af = document.getElementById('af');
  if (af) af.onsubmit = ev => { ev.preventDefault(); guard(async () => { await uploadFiles(e.id, af.querySelector('input')); toast('Uploaded'); render(); }, ev.submitter); };
  const v = document.getElementById('void');
  if (v) v.onclick = () => {
    const reason = prompt('Reason for voiding (kept in the audit log):');
    if (reason === null) return;
    guard(async () => { const r = await api('POST', `/api/entries/${e.id}/void`, { reason }); toast(`Voided. Reversal #${r.reversal}`); render(); }, v);
  };
}

// ---------- invoices ----------
function invStatus(i) {
  if (i.voided) return '<span class="badge">void</span>';
  if (i.paid >= i.total) return '<span class="badge good">paid</span>';
  if (i.due_date < today()) return '<span class="badge bad">overdue</span>';
  if (i.paid > 0) return '<span class="badge warn">partial</span>';
  return '<span class="badge blue">open</span>';
}
async function invoices(main, parts) {
  if (parts[1] === 'new') return invoiceForm(main);
  const list = await api('GET', '/api/invoices');
  main.innerHTML = `<div class="top"><h1>Invoices</h1>${canWrite() ? '<a class="btn primary" href="#/invoices/new">＋ New invoice</a>' : ''}</div>
  <div class="card">${list.length ? `<div class="tablewrap"><table class="t"><tr><th>Number</th><th>Client</th><th>Date</th><th>Due</th><th class="num">Total</th><th class="num">Balance</th><th>Status</th></tr>
  ${list.map(i => `<tr class="click" data-href="#/invoice/${i.id}"><td>${esc(i.number)}</td><td>${esc(i.client_name)}</td><td>${i.date}</td><td>${i.due_date}</td><td class="num">${money(i.total)}</td><td class="num">${i.voided ? '' : money(i.total - i.paid)}</td><td>${invStatus(i)}</td></tr>`).join('')}
  </table></div>` : '<p class="muted">No invoices yet.</p>'}</div>`;
  bindRowLinks(main);
}
async function invoiceForm(main) {
  const { number } = await api('GET', '/api/invoices/next-number');
  main.innerHTML = `<div class="top"><h1>New invoice</h1></div><div class="card"><form id="f">
    <div class="grid g4"><div class="field"><label>Client</label><select name="client_id" required data-ctype="client" data-blank="Choose client…">${contactOptions('client', null, { blank: 'Choose client…' })}</select></div>
    <div class="field"><label>Invoice #</label><input name="number" value="${esc(number)}"></div>
    <div class="field"><label>Date</label><input type="date" name="date" value="${today()}" required></div>
    <div class="field"><label>Due date</label><input type="date" name="due_date" value="${addDays(today(), 30)}" required></div></div>
    <div class="grid g2"><div class="field"><label>Income category</label><select name="income_account_id">${acctOptions([['Income', a => a.type === 'income']], S.accounts.find(a => a.code === '4000')?.id)}</select></div>
    <div class="field"><label>NY sales tax rate %</label><input name="tax_rate" type="number" step="0.001" min="0" value="${esc(S.settings.sales_tax_rate || 0)}"><div class="hint">Leave 0 for non-taxable services. NYC combined rate is 8.875% – confirm taxability with your accountant.</div></div></div>
    <div class="tablewrap"><table class="t" id="items"><tr><th style="width:55%">Description</th><th>Qty / hours</th><th>Rate ($)</th><th class="num">Amount</th></tr></table></div>
    <div class="row" style="margin:8px 0"><button type="button" id="add">＋ Line</button><b class="right" id="tot"></b></div>
    <div class="field"><label>Notes on invoice (payment instructions etc.)</label><textarea name="memo"></textarea></div>
    <button class="primary">Create invoice</button></form></div>`;
  const tbl = document.getElementById('items');
  const add = () => { const r = tbl.insertRow(); r.className = 'li'; r.innerHTML = `<td><input class="d" placeholder="AI development – October"></td><td><input class="q" type="number" step="0.01" value="1"></td><td><input class="p" type="number" step="0.01"></td><td class="num a"></td>`; };
  add();
  document.getElementById('add').onclick = add;
  const form = document.getElementById('f');
  form.addEventListener('input', () => {
    let sub = 0;
    form.querySelectorAll('.li').forEach(r => { const a = Math.round(Number(r.querySelector('.q').value || 0) * Number(r.querySelector('.p').value || 0) * 100); r.querySelector('.a').innerHTML = money(a); sub += a; });
    const tax = Math.round(sub * Number(form.elements.tax_rate.value || 0) / 100);
    document.getElementById('tot').innerHTML = `Subtotal ${money(sub)}${tax ? ` + tax ${money(tax)}` : ''} = ${money(sub + tax)}`;
  });
  form.onsubmit = e => {
    e.preventDefault();
    const b = formObj(form);
    b.items = [...form.querySelectorAll('.li')].map(r => ({ description: r.querySelector('.d').value, qty: r.querySelector('.q').value, unit_price: r.querySelector('.p').value }));
    guard(async () => { const r = await api('POST', '/api/invoices', b); toast('Invoice created'); location.hash = `#/invoice/${r.id}`; }, e.submitter);
  };
}
async function invoicePage(main, parts) {
  const i = await api('GET', `/api/invoices/${parts[1]}`);
  const due = i.total - i.paid;
  main.innerHTML = `<div class="top"><div><h1>Invoice ${esc(i.number)} ${invStatus(i)}</h1><div class="muted">${esc(i.client_name)} · issued ${i.date} · due ${i.due_date}</div></div>
    <div class="row"><a class="btn" href="/invoice/${i.id}/print" target="_blank">Print / PDF</a><a class="btn" href="#/entry/${i.entry_id}">Journal entry</a>
    ${isOwner() && !i.voided ? '<button class="danger" id="void">Void</button>' : ''}</div></div>
  <div class="grid g2"><div class="card"><h2>Items</h2><table class="t"><tr><th>Description</th><th class="num">Qty</th><th class="num">Rate</th><th class="num">Amount</th></tr>
    ${i.items.map(t => `<tr><td>${esc(t.description)}</td><td class="num">${t.qty}</td><td class="num">${money(t.unit_price)}</td><td class="num">${money(t.amount)}</td></tr>`).join('')}
    <tr class="total"><td colspan="3">Subtotal</td><td class="num">${money(i.subtotal)}</td></tr>
    ${i.tax ? `<tr><td colspan="3">Sales tax ${i.tax_rate}%</td><td class="num">${money(i.tax)}</td></tr>` : ''}
    <tr class="grand"><td colspan="3">Total</td><td class="num">${money(i.total)}</td></tr>
    <tr><td colspan="3">Paid</td><td class="num">${money(i.paid)}</td></tr><tr class="total"><td colspan="3">Balance due</td><td class="num">${money(due)}</td></tr></table></div>
  <div class="card"><h2>Payments</h2>
    ${i.payments.map(p => `<div class="${p.voided ? 'muted' : ''}"><a href="#/entry/${p.entry_id}">${p.date} – ${money(p.amount)}</a> ${p.voided ? '(voided)' : ''}</div>`).join('') || '<p class="muted">No payments yet.</p>'}
    ${canWrite() && !i.voided && due > 0 ? `<form id="pf" style="margin-top:14px"><h3>Record payment</h3>
      <div class="grid g2"><div class="field"><label>Date received</label><input type="date" name="date" value="${today()}"></div>
      <div class="field"><label>Amount ($)</label><input name="amount" type="number" step="0.01" value="${plain(due)}"></div></div>
      <div class="grid g2"><div class="field"><label>Deposited to</label><select name="deposit_to" required>${acctOptions(G.payment, S.accounts.find(a => a.code === '1000')?.id)}</select></div>
      <div class="field"><label>Processing fee deducted ($)</label><input name="fee" type="number" step="0.01" min="0" placeholder="Stripe / PayPal / wire fee"></div></div>
      <div class="field"><label>Reference / proof</label><input type="file" name="files" multiple></div>
      <button class="primary">Record payment</button></form>` : ''}
  </div></div>
  ${i.memo ? `<div class="card"><h2>Notes</h2><div style="white-space:pre-line">${esc(i.memo)}</div></div>` : ''}`;
  const pf = document.getElementById('pf');
  if (pf) pf.onsubmit = e => { e.preventDefault(); guard(async () => { const r = await api('POST', `/api/invoices/${i.id}/payments`, formObj(pf)); await uploadFiles(r.entry_id, pf.querySelector('input[type=file]')); toast('Payment recorded'); render(); }, e.submitter); };
  const v = document.getElementById('void');
  if (v) v.onclick = () => { const reason = prompt('Reason for voiding this invoice:'); if (reason === null) return; guard(async () => { await api('POST', `/api/invoices/${i.id}/void`, { reason }); toast('Invoice voided'); render(); }, v); };
}

// ---------- contacts ----------
const CTYPES = [['client', 'Clients'], ['vendor', 'Vendors'], ['employee', 'Employees'], ['owner', 'Owners']];
async function contacts(main, parts, q) {
  const type = q.type || 'client';
  const editing = q.edit ? S.contacts.find(c => c.id === Number(q.edit)) : null;
  const list = S.contacts.filter(c => c.type === type);
  const c = editing || { type };
  main.innerHTML = `<div class="top"><h1>Clients, vendors & people</h1></div>
  <div class="tabs">${CTYPES.map(([t, l]) => `<a href="#/contacts?type=${t}" class="${t === type ? 'on' : ''}">${l}</a>`).join('')}</div>
  <div class="grid g2" style="grid-template-columns: minmax(0,3fr) minmax(0,2fr)">
  <div class="card"><div class="tablewrap"><table class="t"><tr><th>Name</th><th>Email</th><th>${type === 'owner' ? 'Profit share' : 'Tax ID'}</th>${type === 'vendor' ? '<th>1099</th>' : ''}<th></th></tr>
    ${list.map(x => `<tr class="${x.active ? '' : 'voided'}"><td><a href="#/transactions?contact_id=${x.id}">${esc(x.name)}</a></td><td>${esc(x.email || '')}</td><td>${type === 'owner' ? esc(x.profit_share) + '%' : esc(x.tax_id || '')}</td>
    ${type === 'vendor' ? `<td>${x.is_1099 ? '<span class="badge warn">1099</span>' : ''}</td>` : ''}<td>${canWrite() ? `<a href="#/contacts?type=${type}&edit=${x.id}">Edit</a>` : ''}</td></tr>`).join('') || '<tr><td class="muted">None yet</td></tr>'}
  </table></div></div>
  ${canWrite() ? `<div class="card"><h2>${editing ? 'Edit ' + esc(editing.name) : 'Add ' + type}</h2><form id="f">
    <div class="field"><label>Name</label><input name="name" required value="${esc(c.name || '')}"></div>
    <div class="grid g2"><div class="field"><label>Email</label><input name="email" type="email" value="${esc(c.email || '')}"></div><div class="field"><label>Phone</label><input name="phone" value="${esc(c.phone || '')}"></div></div>
    <div class="field"><label>Address</label><textarea name="address">${esc(c.address || '')}</textarea></div>
    ${type !== 'owner' ? `<div class="field"><label>${type === 'employee' ? 'SSN (last 4) / employee ID' : 'EIN / Tax ID (from W-9)'}</label><input name="tax_id" value="${esc(c.tax_id || '')}"></div>` : ''}
    ${type === 'vendor' ? `<div class="field"><label class="check"><input type="checkbox" name="is_1099" ${c.is_1099 ? 'checked' : ''}> Contractor / freelancer – needs a 1099-NEC</label><div class="hint">Tick for individuals and LLCs you pay for services (not corporations, not card payments). Get a W-9 from them.</div></div>` : ''}
    ${type === 'owner' ? `<div class="field"><label>Profit share %</label><input name="profit_share" type="number" step="0.01" value="${esc(c.profit_share ?? 50)}"><div class="hint">As in your operating agreement. Adding an owner creates their own Capital and Draws accounts.</div></div>` : ''}
    <div class="field"><label>Notes</label><textarea name="notes">${esc(c.notes || '')}</textarea></div>
    ${editing ? `<div class="field"><label class="check"><input type="checkbox" name="active" ${c.active ? 'checked' : ''}> Active</label></div>` : ''}
    <div class="row"><button class="primary">${editing ? 'Save' : 'Add'}</button>${editing ? `<a class="btn" href="#/contacts?type=${type}">Cancel</a>` : ''}</div></form></div>` : ''}
  </div>`;
  const f = document.getElementById('f');
  if (f) f.onsubmit = e => {
    e.preventDefault();
    const b = formObj(f);
    guard(async () => {
      if (editing) await api('PATCH', `/api/contacts/${editing.id}`, b); else await api('POST', '/api/contacts', { ...b, type });
      await loadRefs(); toast('Saved'); location.hash = `#/contacts?type=${type}`; if (!editing) render();
    }, e.submitter);
  };
}

// ---------- chart of accounts ----------
async function accounts(main, parts, q) {
  await loadRefs();
  const editing = q.edit ? acct(q.edit) : null;
  const types = ['asset', 'liability', 'equity', 'income', 'expense'];
  main.innerHTML = `<div class="top"><div><h1>Chart of accounts</h1><div class="muted">The “buckets” every dollar goes into. Tax category tells the accountant where it lands on the return.</div></div></div>
  <div class="grid" style="grid-template-columns:minmax(0,3fr) minmax(0,1.3fr)">
  <div class="card"><div class="tablewrap"><table class="t"><tr><th>Code</th><th>Name</th><th>Tax category</th><th class="num">Balance</th><th></th></tr>
  ${types.map(t => `<tr class="header"><td colspan="5">${t[0].toUpperCase() + t.slice(1)}${t === 'liability' ? ' (what you owe)' : t === 'equity' ? ' (owners)' : ''}</td></tr>` +
    S.accounts.filter(a => a.type === t).map(a => `<tr class="${a.active ? '' : 'voided'}"><td>${esc(a.code)}</td><td><a href="#/report/general_ledger?account_id=${a.id}">${esc(a.name)}</a> ${a.is_payment ? '<span class="badge blue">bank/card</span>' : ''}</td>
      <td class="small muted">${esc(a.tax_category || '')}</td><td class="num">${money(a.balance)}</td><td>${isOwner() ? `<a href="#/accounts?edit=${a.id}">Edit</a>` : ''}</td></tr>`).join('')).join('')}
  </table></div></div>
  ${isOwner() ? `<div class="card"><h2>${editing ? 'Edit ' + esc(editing.code) : 'Add account'}</h2><form id="f">
    ${editing ? '' : `<div class="grid g2"><div class="field"><label>Code</label><input name="code" required placeholder="5430"></div>
      <div class="field"><label>Type</label><select name="type">${types.map(t => `<option>${t}</option>`).join('')}</select></div></div>`}
    <div class="field"><label>Name</label><input name="name" required value="${esc(editing?.name || '')}"></div>
    <div class="field"><label>Tax category</label><input name="tax_category" value="${esc(editing?.tax_category || '')}" placeholder="e.g. Other deductions: Hosting"></div>
    ${editing ? `<div class="field"><label class="check"><input type="checkbox" name="active" ${editing.active ? 'checked' : ''}> Active</label></div>` :
      `<div class="field"><label class="check"><input type="checkbox" name="is_payment"> This is a bank, cash or credit-card account</label></div>`}
    <div class="row"><button class="primary">Save</button>${editing ? '<a class="btn" href="#/accounts">Cancel</a>' : ''}</div>
    <p class="hint">Accounts are never deleted (history must stay). Deactivate instead.</p></form></div>` : ''}</div>`;
  const f = document.getElementById('f');
  if (f) f.onsubmit = e => {
    e.preventDefault();
    guard(async () => {
      if (editing) await api('PATCH', `/api/accounts/${editing.id}`, formObj(f)); else await api('POST', '/api/accounts', formObj(f));
      toast('Saved'); location.hash = '#/accounts'; if (!editing) render();
    }, e.submitter);
  };
}

// ---------- reconcile ----------
async function reconcile(main, parts, q) {
  const pays = S.accounts.filter(a => a.is_payment && a.active);
  const accId = q.account_id || pays[0]?.id;
  const to = q.to || today();
  const d = await api('GET', `/api/reconcile?account_id=${accId}&to=${to}`);
  main.innerHTML = `<div class="top"><div><h1>Reconcile</h1><div class="muted">Tick every item that appears on your bank / card statement. When the cleared balance equals the statement balance, your books are proven correct.</div></div></div>
  <div class="card"><form id="sel" class="grid g4" style="align-items:end">
    <div class="field"><label>Account</label><select name="account_id">${pays.map(a => `<option value="${a.id}" ${a.id === Number(accId) ? 'selected' : ''}>${esc(a.name)}</option>`).join('')}</select></div>
    <div class="field"><label>Statement end date</label><input type="date" name="to" value="${to}"></div>
    <div class="field"><label>Statement ending balance ($)</label><input id="sb" type="number" step="0.01" value="${esc(q.bal || '')}"></div>
    <div class="field"><button>Load</button></div></form>
    ${d.last ? `<div class="muted small">Last reconciled through ${d.last.statement_date} at ${money(d.last.statement_balance)}.</div>` : ''}</div>
  <div class="grid g3"><div class="kpi"><div class="l">Cleared balance</div><div class="v" id="cb">${money(d.cleared)}</div></div>
    <div class="kpi"><div class="l">Statement balance</div><div class="v" id="sv">—</div></div>
    <div class="kpi"><div class="l">Difference</div><div class="v" id="df">—</div><div class="s">Books balance (all items): ${money(d.book)}</div></div></div>
  <div class="card" style="margin-top:14px"><div class="tablewrap"><table class="t"><tr><th>✓</th><th>Date</th><th>#</th><th>Name / memo</th><th class="num">${d.sign > 0 ? 'Deposit' : 'Payment / credit'}</th><th class="num">${d.sign > 0 ? 'Withdrawal' : 'Charge'}</th></tr>
  ${d.lines.map(l => `<tr><td><input type="checkbox" class="cl" data-id="${l.id}" data-amt="${(l.debit - l.credit) * d.sign}" ${l.cleared ? 'checked' : ''} ${canWrite() ? '' : 'disabled'}></td>
    <td>${l.date}</td><td><a href="#/entry/${l.entry_id}">${l.entry_id}</a></td><td>${esc(l.contact_name || '')} <span class="muted">${esc(l.memo || '')}</span></td>
    <td class="num">${money(d.sign > 0 ? l.debit : l.debit, 1)}</td><td class="num">${money(l.credit, 1)}</td></tr>`).join('') || '<tr><td colspan="6" class="muted">No transactions</td></tr>'}</table></div>
  ${canWrite() ? '<div class="row" style="margin-top:12px"><button class="primary" id="fin" disabled>Finish reconciliation</button><span class="muted small">Enabled when the difference is $0.00</span></div>' : ''}</div>`;
  let cleared = d.cleared;
  const upd = () => {
    const sb = Math.round(Number(document.getElementById('sb').value || 0) * 100);
    const has = document.getElementById('sb').value !== '';
    document.getElementById('cb').innerHTML = money(cleared);
    document.getElementById('sv').innerHTML = has ? money(sb) : '—';
    document.getElementById('df').innerHTML = has ? (sb === cleared ? '<span class="good">$0.00 ✓</span>' : money(sb - cleared)) : '—';
    const fin = document.getElementById('fin');
    if (fin) fin.disabled = !has || sb !== cleared;
  };
  upd();
  document.getElementById('sb').oninput = upd;
  document.getElementById('sel').onsubmit = e => { e.preventDefault(); const b = formObj(e.target); location.hash = `#/reconcile?account_id=${b.account_id}&to=${b.to}&bal=${document.getElementById('sb').value}`; };
  main.querySelectorAll('.cl').forEach(c => c.onchange = () => guard(async () => {
    await api('PATCH', `/api/lines/${c.dataset.id}/cleared`, { cleared: c.checked });
    cleared += (c.checked ? 1 : -1) * Number(c.dataset.amt); upd();
  }));
  const fin = document.getElementById('fin');
  if (fin) fin.onclick = () => guard(async () => {
    await api('POST', '/api/reconciliations', { account_id: accId, statement_date: document.querySelector('[name=to]').value, statement_balance: document.getElementById('sb').value });
    toast('Reconciliation saved'); location.hash = '#/report/reconciliations';
  }, fin);
}

// ---------- bank CSV import ----------
function parseCSV(text) {
  const rows = []; let row = [], f = '', q = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (q) { if (c === '"') { if (text[i + 1] === '"') { f += '"'; i++; } else q = false; } else f += c; }
    else if (c === '"') q = true;
    else if (c === ',') { row.push(f); f = ''; }
    else if (c === '\n' || c === '\r') { if (c === '\r' && text[i + 1] === '\n') i++; row.push(f); rows.push(row); row = []; f = ''; }
    else f += c;
  }
  if (f || row.length) { row.push(f); rows.push(row); }
  return rows.filter(r => r.some(x => x.trim()));
}
function normDate(s) {
  s = (s || '').trim();
  let m = s.match(/^(\d{4})-(\d{1,2})-(\d{1,2})/);
  if (m) return `${m[1]}-${m[2].padStart(2, '0')}-${m[3].padStart(2, '0')}`;
  m = s.match(/^(\d{1,2})\/(\d{1,2})\/(\d{2,4})/);
  if (m) return `${m[3].length === 2 ? '20' + m[3] : m[3]}-${m[1].padStart(2, '0')}-${m[2].padStart(2, '0')}`;
  return '';
}
const num = s => { s = String(s || '').replace(/[$,\s]/g, ''); if (/^\(.*\)$/.test(s)) s = '-' + s.slice(1, -1); return Number(s) || 0; };

async function importPage(main) {
  if (!canWrite()) { main.innerHTML = '<div class="note">Read-only role.</div>'; return; }
  main.innerHTML = `<div class="top"><div><h1>Import bank / card statement</h1><div class="muted">Download a CSV from your bank (Chase, Bank of America, Mercury, etc.), then categorize each line. Duplicates are skipped automatically.</div></div></div>
  <div class="card"><div class="grid g3" style="align-items:end"><div class="field"><label>Into account</label><select id="acc">${acctOptions(G.payment, S.accounts.find(a => a.code === '1000')?.id)}</select></div>
  <div class="field"><label>CSV file</label><input type="file" id="file" accept=".csv,text/csv"></div></div>
  <div class="info">Tip: picking a category for one row fills the same category on other rows with a similar description. Owner deposits → choose “Owner Capital – name”. Owner withdrawals → “Owner Draws – name”. Paying the card from the bank → choose the card account under Liabilities.</div>
  <div id="map"></div></div><div id="rows"></div>`;
  let header = [], data = [];
  document.getElementById('file').onchange = async e => {
    const file = e.target.files[0];
    if (!file) return;
    const rows = parseCSV(await file.text());
    const hi = rows.findIndex(r => r.some(c => /date/i.test(c)));
    header = rows[Math.max(0, hi)]; data = rows.slice(Math.max(0, hi) + 1);
    const find = re => header.findIndex(h => re.test(h));
    const opts = sel => `<option value="-1">—</option>` + header.map((h, i) => `<option value="${i}" ${i === sel ? 'selected' : ''}>${esc(h)}</option>`).join('');
    const dI = find(/date/i), desc = find(/desc|memo|payee|name|details/i), amtI = find(/^amount$|amount/i), dbI = find(/debit|withdraw/i), crI = find(/credit|deposit/i);
    document.getElementById('map').innerHTML = `<h3>Columns</h3><div class="grid g4">
      <div class="field"><label>Date</label><select id="cD">${opts(dI)}</select></div><div class="field"><label>Description</label><select id="cS">${opts(desc)}</select></div>
      <div class="field"><label>Amount (+in / −out)</label><select id="cA">${opts(amtI >= 0 && amtI !== dbI && amtI !== crI ? amtI : -1)}</select></div>
      <div class="field"><label>…or Money out / Money in columns</label><div class="row"><select id="cO" style="width:48%">${opts(dbI)}</select><select id="cI" style="width:48%">${opts(crI)}</select></div></div></div>
      <label class="check"><input type="checkbox" id="flip"> Flip sign (for card statements where charges are positive)</label>
      <button class="primary" id="prev" style="margin-top:10px">Preview</button>`;
    document.getElementById('prev').onclick = preview;
  };
  function preview() {
    const g = id => Number(document.getElementById(id).value);
    const [cD, cS, cA, cO, cI] = ['cD', 'cS', 'cA', 'cO', 'cI'].map(g);
    const flip = document.getElementById('flip').checked ? -1 : 1;
    const seen = {};
    const items = data.map(r => {
      let amt = cA >= 0 ? num(r[cA]) : (cI >= 0 ? Math.abs(num(r[cI])) : 0) - (cO >= 0 ? Math.abs(num(r[cO])) : 0);
      amt *= flip;
      const date = normDate(r[cD]), description = (r[cS] || '').trim();
      const key = `${date}|${amt}|${description}`;
      seen[key] = (seen[key] || 0) + 1;
      return { date, description, amount: amt, dup: seen[key] - 1 };
    }).filter(x => x.date && x.amount);
    const box = document.getElementById('rows');
    box.innerHTML = `<div class="card"><div class="tablewrap"><table class="t"><tr><th><input type="checkbox" id="all" checked></th><th>Date</th><th>Description</th><th class="num">Amount</th><th>Category</th><th>Name</th></tr>
      ${items.map((x, i) => `<tr data-i="${i}"><td><input type="checkbox" class="inc" checked></td><td>${x.date}</td><td class="desc">${esc(x.description)}</td><td class="num">${money(Math.round(x.amount * 100))}</td>
      <td><select class="cat">${acctOptions(G.category)}</select></td><td><select class="who">${contactOptions(null, null, { allowNew: false })}</select></td></tr>`).join('')}
    </table></div><div class="row" style="margin-top:12px"><button class="primary" id="post">Post selected</button><span id="cnt" class="muted"></span></div></div>`;
    const key = s => s.toLowerCase().replace(/[^a-z ]/g, ' ').split(/\s+/).filter(Boolean).slice(0, 2).join(' ');
    box.querySelectorAll('.cat').forEach(sel => sel.onchange = () => {
      const k = key(sel.closest('tr').querySelector('.desc').textContent);
      if (!k) return;
      box.querySelectorAll('tr[data-i]').forEach(tr => { const s = tr.querySelector('.cat'); if (!s.value && key(tr.querySelector('.desc').textContent) === k) s.value = sel.value; });
    });
    document.getElementById('all').onchange = e => box.querySelectorAll('.inc').forEach(c => c.checked = e.target.checked);
    document.getElementById('post').onclick = e => {
      const rows = [];
      let missing = 0;
      box.querySelectorAll('tr[data-i]').forEach(tr => {
        if (!tr.querySelector('.inc').checked) return;
        const x = items[tr.dataset.i];
        const cat = tr.querySelector('.cat').value;
        if (!cat) { missing++; return; }
        rows.push({ ...x, account_id: cat, contact_id: tr.querySelector('.who').value || null });
      });
      if (missing && !confirm(`${missing} selected row(s) have no category and will be skipped. Continue?`)) return;
      guard(async () => {
        const r = await api('POST', '/api/import', { account_id: document.getElementById('acc').value, rows });
        toast(`Imported ${r.created}, skipped ${r.skipped} duplicates${r.errors.length ? ', ' + r.errors.length + ' errors' : ''}`, r.errors.length > 0);
        if (r.errors.length) document.getElementById('cnt').textContent = r.errors.join(' · ');
        else location.hash = '#/transactions?kind=import';
      }, e.target);
    };
  }
}

// ---------- reports ----------
function presets() {
  const t = new Date(), y = t.getFullYear(), m = t.getMonth();
  const iso = d => d.toISOString().slice(0, 10);
  const D = (yy, mm, dd) => new Date(Date.UTC(yy, mm, dd));
  const q = Math.floor(m / 3);
  return [
    ['This year', iso(D(y, 0, 1)), iso(D(y, 11, 31))], ['Last year', iso(D(y - 1, 0, 1)), iso(D(y - 1, 11, 31))],
    ['This quarter', iso(D(y, q * 3, 1)), iso(D(y, q * 3 + 3, 0))], ['Last quarter', iso(D(y, q * 3 - 3, 1)), iso(D(y, q * 3, 0))],
    ['This month', iso(D(y, m, 1)), iso(D(y, m + 1, 0))], ['Last month', iso(D(y, m - 1, 1)), iso(D(y, m, 0))],
  ];
}
function rangeForm(q, id) {
  return `<form id="${id}" class="row noprint" style="align-items:end">
    <div><label>From</label><input type="date" name="from" value="${esc(q.from || '')}"></div>
    <div><label>To</label><input type="date" name="to" value="${esc(q.to || '')}"></div>
    <select name="preset" style="width:auto"><option value="">Quick range…</option>${presets().map(([l, f, t]) => `<option value="${f}|${t}">${l}</option>`).join('')}</select>
    <button class="primary">Apply</button></form>`;
}
function bindRange(id, cb) {
  const f = document.getElementById(id);
  f.elements.preset.onchange = () => { const [a, b] = f.elements.preset.value.split('|'); if (a) { f.elements.from.value = a; f.elements.to.value = b; } };
  f.onsubmit = e => { e.preventDefault(); const b = formObj(f); delete b.preset; cb(b); };
}
async function reportsPage(main) {
  const list = await api('GET', '/api/reports');
  const y = new Date().getFullYear();
  const canPkg = ['owner', 'accountant'].includes(S.user.role);
  main.innerHTML = `<div class="top"><h1>Reports & tax package</h1></div>
  ${canPkg ? `<div class="card" style="border-color:#c7d2fe;background:#f8f9ff"><h2>📦 Accountant / tax package</h2>
    <p>One ZIP with every report (CSV, opens in Excel), the full general ledger and journal, owner capital, payroll, 1099s, sales tax, all receipts, and a README explaining how the books are kept. Give this to your tax preparer – they shouldn’t need to ask anything.</p>
    <div class="row" style="align-items:end"><div><label>From</label><input type="date" id="pf" value="${y - 1}-01-01"></div><div><label>To</label><input type="date" id="pt" value="${y - 1}-12-31"></div>
    <button class="primary" id="pkg">Download package</button></div>
    <div class="hint">Before sending: reconcile every bank & card account through year-end, clear “Missing receipts”, then lock the year in Settings.</div></div>` : ''}
  <div class="grid g3">${list.map(r => `<a class="card" href="#/report/${r.id}" style="color:inherit;text-decoration:none;margin:0"><b>${esc(r.title)}</b><div class="muted small">${esc(r.desc)}</div></a>`).join('')}</div>`;
  const p = document.getElementById('pkg');
  if (p) p.onclick = () => { location.href = `/api/export/package?from=${document.getElementById('pf').value}&to=${document.getElementById('pt').value}`; };
}
async function reportView(main, parts, q) {
  const name = parts[1];
  const qs = new URLSearchParams(q).toString();
  const rep = await api('GET', `/api/reports/${name}?${qs}`);
  const pointInTime = ['balance_sheet', 'trial_balance', 'ar_aging'].includes(name);
  main.innerHTML = `<div class="top"><div><a href="#/reports" class="noprint small">← Reports</a><h1>${esc(rep.title)}</h1><div class="muted">${esc(S.settings.company || '')} · ${esc(rep.subtitle || '')}</div></div>
    <div class="row noprint"><a class="btn" href="/api/reports/${name}?${qs}&format=csv">Export CSV</a><button onclick="print()">Print / PDF</button></div></div>
  <div class="card noprint">${name === 'general_ledger' ? `<div class="field" style="max-width:420px"><label>Account</label><select id="gla">${acctOptions(G.all, q.account_id, 'All accounts')}</select></div>` : ''}
    ${rangeForm(q, 'rf')}${pointInTime ? '<div class="hint">This report is “as of” the To date.</div>' : ''}</div>
  <div class="card"><div class="tablewrap"><table class="t"><tr>${rep.columns.map(c => `<th class="${c.type === 'money' ? 'num' : ''}">${esc(c.label)}</th>`).join('')}</tr>
  ${rep.rows.map(r => `<tr class="${r.style || ''} ${r.link ? 'click' : ''}" ${r.link ? `data-href="${esc(r.link)}"` : ''}>${r.cells.map((v, i) => {
    const t = rep.columns[i]?.type;
    return `<td class="${t === 'money' ? 'num' : ''}">${t === 'money' && typeof v === 'number' ? money(v) : esc(v ?? '')}</td>`;
  }).join('')}</tr>`).join('') || `<tr><td colspan="${rep.columns.length}" class="muted">No data for this period.</td></tr>`}
  </table></div>${(rep.notes || []).map(n => `<p class="small muted">${esc(n)}</p>`).join('')}</div>`;
  bindRowLinks(main);
  bindRange('rf', b => {
    const gla = document.getElementById('gla');
    if (gla && gla.value) b.account_id = gla.value;
    location.hash = `#/report/${name}?` + new URLSearchParams(Object.entries(b).filter(([, v]) => v)).toString();
  });
  const gla = document.getElementById('gla');
  if (gla) gla.onchange = () => document.getElementById('rf').requestSubmit();
}

// ---------- settings ----------
async function settings(main) {
  const s = S.settings;
  const owner = isOwner();
  const users = owner ? await api('GET', '/api/users') : [];
  const dis = owner ? '' : 'disabled';
  main.innerHTML = `<div class="top"><h1>Settings</h1></div>
  <div class="grid g2"><div class="card"><h2>Company</h2><form id="sf">
    <div class="field"><label>Legal name</label><input name="company" value="${esc(s.company || '')}" ${dis}></div>
    <div class="grid g2"><div class="field"><label>EIN</label><input name="ein" value="${esc(s.ein || '')}" ${dis}></div><div class="field"><label>NYS sales tax ID</label><input name="nys_sales_tax_id" value="${esc(s.nys_sales_tax_id || '')}" ${dis}></div></div>
    <div class="field"><label>Entity / tax type</label><input name="entity_type" value="${esc(s.entity_type || '')}" ${dis}></div>
    <div class="field"><label>Address</label><textarea name="address" ${dis}>${esc(s.address || '')}</textarea></div>
    <div class="grid g2"><div class="field"><label>Email (shown on invoices)</label><input name="email" value="${esc(s.email || '')}" ${dis}></div><div class="field"><label>Phone</label><input name="phone" value="${esc(s.phone || '')}" ${dis}></div></div>
    <div class="grid g2"><div class="field"><label>Fiscal year start month (1–12)</label><input name="fiscal_start_month" type="number" min="1" max="12" value="${esc(s.fiscal_start_month || 1)}" ${dis}></div>
    <div class="field"><label>1099-NEC threshold ($)</label><input name="threshold_1099" type="number" value="${esc(s.threshold_1099 || 2000)}" ${dis}><div class="hint">$2,000 for payments from 2026 on ($600 before). Confirm with your accountant.</div></div></div>
    <div class="grid g3"><div class="field"><label>Invoice prefix</label><input name="invoice_prefix" value="${esc(s.invoice_prefix || 'INV-')}" ${dis}></div>
    <div class="field"><label>Next invoice #</label><input name="invoice_next" value="${esc(s.invoice_next || '1001')}" ${dis}></div>
    <div class="field"><label>Default sales tax %</label><input name="sales_tax_rate" type="number" step="0.001" value="${esc(s.sales_tax_rate || 0)}" ${dis}></div></div>
    ${owner ? '<button class="primary">Save</button>' : ''}</form></div>
  <div>
    <div class="card"><h2>Close the books</h2><p class="muted">After the accountant files, lock the period. Nobody can add, change or void anything dated on or before this date.</p>
      <form id="lf" class="row"><input type="date" name="lock_date" value="${esc(s.lock_date || '')}" style="width:auto" ${dis}>${owner ? '<button>Set lock date</button>' : ''}</form></div>
    ${owner ? `<div class="card"><h2>Backup</h2><p class="muted">Download the complete database (one file). Keep a copy somewhere safe every month.</p><a class="btn" href="/api/export/backup">Download backup</a></div>` : ''}
    <div class="card"><h2>My password</h2><form id="pw"><div class="grid g2"><div class="field"><label>Current</label><input type="password" name="current" required></div>
      <div class="field"><label>New (8+)</label><input type="password" name="password" minlength="8" required></div></div><button>Change password</button></form></div>
  </div></div>
  ${owner ? `<div class="card"><h2>Users</h2><p class="muted">Owner = everything. Staff = record transactions, no voids/settings. Accountant = read-only + reports & tax package.</p>
    <div class="tablewrap"><table class="t"><tr><th>Name</th><th>Email</th><th>Role</th><th>Status</th><th></th></tr>
    ${users.map(u => `<tr><td>${esc(u.name)}</td><td>${esc(u.email)}</td><td>${esc(u.role)}</td><td>${u.active ? 'active' : '<span class="badge">disabled</span>'}</td>
      <td class="row"><button data-u="${u.id}" data-act="pw">Reset password</button>${u.id !== S.user.id ? `<button data-u="${u.id}" data-act="toggle" data-active="${u.active}">${u.active ? 'Disable' : 'Enable'}</button>` : ''}</td></tr>`).join('')}</table></div>
    <h3>Add user</h3><form id="uf" class="grid g4" style="align-items:end"><div class="field"><label>Name</label><input name="name" required></div><div class="field"><label>Email</label><input name="email" type="email" required></div>
      <div class="field"><label>Role</label><select name="role"><option value="accountant">accountant</option><option value="staff">staff</option><option value="owner">owner</option></select></div>
      <div class="field"><label>Temporary password</label><input name="password" minlength="8" required></div><div><button class="primary">Add user</button></div></form></div>` : ''}`;
  const save = async (b, btn) => guard(async () => { S.settings = await api('PUT', '/api/settings', b); toast('Saved'); }, btn);
  const sf = document.getElementById('sf');
  sf.onsubmit = e => { e.preventDefault(); save(formObj(sf), e.submitter); };
  const lf = document.getElementById('lf');
  lf.onsubmit = e => { e.preventDefault(); const b = formObj(lf); if (confirm(b.lock_date ? `Lock all transactions on or before ${b.lock_date}?` : 'Remove the lock?')) save(b, e.submitter); };
  const pw = document.getElementById('pw');
  pw.onsubmit = e => { e.preventDefault(); guard(async () => { await api('POST', '/api/me/password', formObj(pw)); toast('Password changed'); pw.reset(); }, e.submitter); };
  const uf = document.getElementById('uf');
  if (uf) uf.onsubmit = e => { e.preventDefault(); guard(async () => { await api('POST', '/api/users', formObj(uf)); toast('User added'); render(); }, e.submitter); };
  main.querySelectorAll('button[data-u]').forEach(b => b.onclick = () => guard(async () => {
    if (b.dataset.act === 'pw') { const p = prompt('New password (8+ characters):'); if (!p) return; await api('PATCH', `/api/users/${b.dataset.u}`, { password: p }); toast('Password reset'); }
    else { await api('PATCH', `/api/users/${b.dataset.u}`, { active: b.dataset.active !== '1' }); render(); }
  }, b));
}

boot().catch(e => { root.innerHTML = `<div class="center"><div class="note">${esc(e.message)}</div></div>`; });
