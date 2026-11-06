// Reports. Each returns { title, subtitle, columns, rows, notes } so the UI, CSV export
// and the accountant package all render from the same data.
const { db, getSetting } = require('./db');

const T = 'text', M = 'money', D = 'date';
const col = (label, type = T) => ({ label, type });
const row = (cells, style, link) => ({ cells, style: style || null, link: link || null });
const credNormal = t => t === 'liability' || t === 'equity' || t === 'income';
const today = () => new Date().toISOString().slice(0, 10);

async function fiscalYearStart(dateStr) {
  const m = Number(await getSetting('fiscal_start_month', '1'));
  const d = new Date(dateStr + 'T00:00:00Z');
  let y = d.getUTCFullYear();
  if (d.getUTCMonth() + 1 < m) y--;
  return `${y}-${String(m).padStart(2, '0')}-01`;
}
function dayBefore(s) {
  const d = new Date(s + 'T00:00:00Z'); d.setUTCDate(d.getUTCDate() - 1);
  return d.toISOString().slice(0, 10);
}
async function range(q) {
  const to = q.to || today();
  const from = q.from || await fiscalYearStart(to);
  return { from, to };
}

// Sum of (debit - credit) per account between dates (inclusive). from=null → from the beginning.
async function sums(from, to) {
  const rows = await db.all(`SELECT l.account_id id, SUM(l.debit) dr, SUM(l.credit) cr FROM lines l JOIN entries e ON e.id=l.entry_id
     WHERE e.date <= ? ${from ? 'AND e.date >= ?' : ''} GROUP BY l.account_id`, ...[to, ...(from ? [from] : [])]);
  const m = new Map();
  rows.forEach(r => m.set(r.id, { dr: r.dr, cr: r.cr, net: r.dr - r.cr }));
  return m;
}
const accounts = () => db.all('SELECT * FROM accounts ORDER BY code');
const natural = (a, s) => s ? (credNormal(a.type) ? -s.net : s.net) : 0;

async function netIncome(from, to) {
  const s = await sums(from, to);
  let ni = 0;
  for (const a of await accounts()) {
    const v = s.get(a.id);
    if (!v) continue;
    if (a.type === 'income') ni += -v.net;
    if (a.type === 'expense') ni -= v.net;
  }
  return ni;
}

const R = {};

R.pnl = async q => {
  const { from, to } = await range(q);
  const s = await sums(from, to);
  const accs = await accounts();
  const rows = [];
  const section = (type, label) => {
    rows.push(row([label, null], 'header'));
    let t = 0;
    for (const a of accs.filter(a => a.type === type)) {
      const v = natural(a, s.get(a.id));
      if (!v) continue;
      t += v;
      rows.push(row([`${a.code} · ${a.name}`, v], null, `#/report/general_ledger?account_id=${a.id}&from=${from}&to=${to}`));
    }
    rows.push(row([`Total ${label}`, t], 'total'));
    return t;
  };
  const inc = section('income', 'Income');
  const exp = section('expense', 'Expenses');
  rows.push(row(['NET INCOME (PROFIT / LOSS)', inc - exp], 'grand'));
  return { title: 'Profit & Loss', subtitle: `${from} to ${to}`, columns: [col('Account'), col('Amount', M)], rows };
};

R.balance_sheet = async q => {
  const to = q.to || today();
  const fy = await fiscalYearStart(to);
  const s = await sums(null, to);
  const accs = await accounts();
  const rows = [];
  const sec = (type, label) => {
    rows.push(row([label, null], 'header'));
    let t = 0;
    for (const a of accs.filter(a => a.type === type)) {
      const v = natural(a, s.get(a.id));
      if (!v) continue;
      t += v;
      rows.push(row([`${a.code} · ${a.name}`, v], null, `#/report/general_ledger?account_id=${a.id}&to=${to}`));
    }
    return t;
  };
  const assets = sec('asset', 'Assets');
  rows.push(row(['Total Assets', assets], 'grand'));
  const liab = sec('liability', 'Liabilities');
  rows.push(row(['Total Liabilities', liab], 'total'));
  let eq = sec('equity', 'Equity');
  const prior = await netIncome(null, dayBefore(fy));
  const cur = await netIncome(fy, to);
  if (prior) rows.push(row(['Retained Earnings (prior years’ net income)', prior]));
  rows.push(row([`Net Income – current fiscal year (since ${fy})`, cur]));
  eq += prior + cur;
  rows.push(row(['Total Equity', eq], 'total'));
  rows.push(row(['Total Liabilities & Equity', liab + eq], 'grand'));
  const notes = assets === liab + eq ? ['✔ Balanced: Assets = Liabilities + Equity'] : [`⚠ Out of balance by ${(assets - liab - eq) / 100}`];
  return { title: 'Balance Sheet', subtitle: `As of ${to}`, columns: [col('Account'), col('Amount', M)], rows, notes };
};

R.trial_balance = async q => {
  const to = q.to || today();
  const s = await sums(null, to);
  const rows = [];
  let dr = 0, cr = 0;
  for (const a of await accounts()) {
    const v = s.get(a.id);
    if (!v || !v.net) continue;
    const d = v.net > 0 ? v.net : null, c = v.net < 0 ? -v.net : null;
    dr += d || 0; cr += c || 0;
    rows.push(row([a.code, a.name, a.type, d, c], null, `#/report/general_ledger?account_id=${a.id}&to=${to}`));
  }
  rows.push(row(['', 'TOTAL', '', dr, cr], 'grand'));
  return {
    title: 'Trial Balance', subtitle: `As of ${to}`,
    columns: [col('Code'), col('Account'), col('Type'), col('Debit', M), col('Credit', M)], rows,
    notes: [dr === cr ? '✔ Debits equal credits' : '⚠ Debits do not equal credits'],
  };
};

R.general_ledger = async q => {
  const { from, to } = await range(q);
  const all = await accounts();
  const accs = q.account_id ? all.filter(a => a.id === Number(q.account_id)) : all;
  const before = await sums(null, dayBefore(from));
  const lines = await db.all(`SELECT l.*, e.date, e.kind, e.memo emo, e.reference, e.voided, c.name cname,
      (SELECT COUNT(*) FROM attachments x WHERE x.entry_id=e.id) att
    FROM lines l JOIN entries e ON e.id=l.entry_id LEFT JOIN contacts c ON c.id=e.contact_id
    WHERE e.date BETWEEN ? AND ? ${q.account_id ? 'AND l.account_id=?' : ''} ORDER BY e.date, e.id, l.id`, from, to, ...(q.account_id ? [Number(q.account_id)] : []));
  const byAcc = new Map();
  lines.forEach(l => { if (!byAcc.has(l.account_id)) byAcc.set(l.account_id, []); byAcc.get(l.account_id).push(l); });
  const rows = [];
  for (const a of accs) {
    const ls = byAcc.get(a.id) || [];
    const open = natural(a, before.get(a.id));
    if (!ls.length && !open && !q.account_id) continue;
    rows.push(row([`${a.code} · ${a.name}`, '', '', '', '', null, null, null, ''], 'header'));
    rows.push(row([from, '', '', 'Opening balance', '', null, null, open, '']));
    let bal = open;
    for (const l of ls) {
      bal += credNormal(a.type) ? l.credit - l.debit : l.debit - l.credit;
      rows.push(row([l.date, `#${l.entry_id}`, l.kind + (l.voided ? ' (voided)' : ''), l.cname || '', [l.emo, l.memo].filter(Boolean).join(' — '),
        l.debit || null, l.credit || null, bal, l.att ? '📎' : ''], null, `#/entry/${l.entry_id}`));
    }
    rows.push(row([to, '', '', 'Closing balance', '', null, null, bal, ''], 'total'));
  }
  return {
    title: 'General Ledger', subtitle: `${from} to ${to}`,
    columns: [col('Date', D), col('Entry'), col('Type'), col('Name'), col('Memo'), col('Debit', M), col('Credit', M), col('Balance', M), col('Receipt')], rows,
  };
};

R.journal = async q => {
  const { from, to } = await range(q);
  const entries = await db.all(`SELECT e.*, c.name cname, (SELECT COUNT(*) FROM attachments x WHERE x.entry_id=e.id) att
    FROM entries e LEFT JOIN contacts c ON c.id=e.contact_id WHERE e.date BETWEEN ? AND ? ORDER BY e.date, e.id`, from, to);
  const lines = await db.all(`SELECT l.*, a.code, a.name FROM lines l JOIN accounts a ON a.id=l.account_id JOIN entries e ON e.id=l.entry_id
    WHERE e.date BETWEEN ? AND ? ORDER BY l.id`, from, to);
  const byE = new Map();
  lines.forEach(l => { if (!byE.has(l.entry_id)) byE.set(l.entry_id, []); byE.get(l.entry_id).push(l); });
  const rows = [];
  for (const e of entries) {
    rows.push(row([e.date, `#${e.id}`, e.kind + (e.voided ? ' (voided)' : ''), e.cname || '', [e.memo, e.reference && `Ref ${e.reference}`].filter(Boolean).join(' · '), null, null, e.att ? `📎 ${e.att}` : ''], 'header', `#/entry/${e.id}`));
    for (const l of byE.get(e.id) || []) rows.push(row(['', '', '', `${l.code} · ${l.name}`, l.memo || '', l.debit || null, l.credit || null, '']));
  }
  return { title: 'Journal (all transactions)', subtitle: `${from} to ${to}`, columns: [col('Date', D), col('Entry'), col('Type'), col('Name / Account'), col('Memo'), col('Debit', M), col('Credit', M), col('Receipts')], rows };
};

R.cash_flow = async q => {
  const { from, to } = await range(q);
  const accs = new Map((await accounts()).map(a => [a.id, a]));
  const pay = [...accs.values()].filter(a => a.is_payment);
  const paySet = new Set(pay.map(a => a.id));
  const lines = await db.all(`SELECT l.* FROM lines l JOIN entries e ON e.id=l.entry_id WHERE e.date BETWEEN ? AND ?`, from, to);
  const by = new Map();
  for (const l of lines) {
    if (paySet.has(l.account_id)) continue;
    by.set(l.account_id, (by.get(l.account_id) || 0) + l.credit - l.debit); // cash effect of the counterpart
  }
  const groups = { Operating: [], Investing: [], Financing: [] };
  for (const [id, v] of by) {
    if (!v) continue;
    const a = accs.get(id);
    const g = a.subtype === 'fixed_asset' ? 'Investing' : (a.type === 'equity' || a.subtype === 'loan') ? 'Financing' : 'Operating';
    groups[g].push([a, v]);
  }
  const before = await sums(null, dayBefore(from));
  // bank & cash minus credit-card debt
  const open = pay.reduce((t, a) => t + (before.get(a.id) || { net: 0 }).net, 0);
  const rows = [];
  let total = 0;
  for (const [g, items] of Object.entries(groups)) {
    rows.push(row([`${g} activities`, null], 'header'));
    let t = 0;
    items.sort((x, y) => x[0].code.localeCompare(y[0].code)).forEach(([a, v]) => { t += v; rows.push(row([`${a.code} · ${a.name}`, v])); });
    rows.push(row([`Net cash from ${g.toLowerCase()} activities`, t], 'total'));
    total += t;
  }
  rows.push(row(['Net change in cash (bank & cash, net of credit cards)', total], 'grand'));
  rows.push(row(['Opening cash, net of card balances', open]));
  rows.push(row(['Closing cash, net of card balances', open + total], 'total'));
  return { title: 'Cash Flow Statement', subtitle: `${from} to ${to}`, columns: [col('Item'), col('Amount', M)], rows };
};

R.owner_equity = async q => {
  const { from, to } = await range(q);
  const owners = await db.all(`SELECT * FROM contacts WHERE type='owner' ORDER BY id`);
  const ownerAccts = await db.all(`SELECT id, owner_contact_id, subtype FROM accounts WHERE subtype IN ('capital','draws')`);
  const before = await sums(null, dayBefore(from));
  const during = await sums(from, to);
  const ni = await netIncome(from, to);
  const rows = [];
  const tot = [0, 0, 0, 0, 0];
  for (const o of owners) {
    const cap = ownerAccts.find(a => a.owner_contact_id === o.id && a.subtype === 'capital');
    const drw = ownerAccts.find(a => a.owner_contact_id === o.id && a.subtype === 'draws');
    const g = (m, a) => a && m.get(a.id) ? -m.get(a.id).net : 0;
    const open = g(before, cap) + g(before, drw);
    const contrib = g(during, cap);
    const draws = -g(during, drw);
    const share = Math.round(ni * (o.profit_share || 0) / 100);
    const vals = [open, contrib, draws, open + contrib - draws, share];
    vals.forEach((v, i) => tot[i] += v);
    rows.push(row([o.name, `${o.profit_share || 0}%`, ...vals]));
  }
  rows.push(row(['TOTAL', '', ...tot], 'grand'));
  return {
    title: 'Owners’ Capital Statement', subtitle: `${from} to ${to}  ·  Company net income for period: $${(ni / 100).toLocaleString('en-US', { minimumFractionDigits: 2 })}`,
    columns: [col('Owner'), col('Profit share'), col('Net contributed – opening', M), col('Contributed in period', M), col('Draws in period', M), col('Net contributed – closing', M), col('Share of net income (by %)', M)],
    rows,
    notes: ['Contributions are owner capital (equity), not income and not loans.', 'Profit share is the percentage set on each owner’s contact. The accountant allocates income per the operating agreement (e.g. on Schedule K-1).'],
  };
};

R.owner_activity = async q => {
  const { from, to } = await range(q);
  const rows = (await db.all(`SELECT e.id, e.date, e.kind, e.memo, e.voided, c.name, SUM(l.credit - l.debit) amt
    FROM entries e JOIN lines l ON l.entry_id=e.id JOIN accounts a ON a.id=l.account_id LEFT JOIN contacts c ON c.id=a.owner_contact_id
    WHERE a.subtype IN ('capital','draws') AND e.date BETWEEN ? AND ? GROUP BY e.id, c.name ORDER BY e.date, e.id`, from, to))
    .map(r => row([r.date, `#${r.id}`, r.name, r.kind + (r.voided ? ' (voided)' : ''), r.memo || '', r.amt > 0 ? r.amt : null, r.amt < 0 ? -r.amt : null], null, `#/entry/${r.id}`));
  return { title: 'Owner Contributions & Draws (detail)', subtitle: `${from} to ${to}`, columns: [col('Date', D), col('Entry'), col('Owner'), col('Type'), col('Memo'), col('Money in', M), col('Money out', M)], rows };
};

R.tax_categories = async q => {
  const { from, to } = await range(q);
  const s = await sums(from, to);
  const groups = new Map();
  for (const a of (await accounts()).filter(a => a.type === 'income' || a.type === 'expense')) {
    const v = natural(a, s.get(a.id));
    if (!v) continue;
    const k = `${a.type === 'income' ? '1' : '2'}|${a.tax_category || 'Uncategorized'}`;
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push([a, v]);
  }
  const rows = [];
  for (const k of [...groups.keys()].sort()) {
    const [t, cat] = k.split('|');
    const items = groups.get(k);
    const total = items.reduce((s, x) => s + x[1], 0);
    rows.push(row([`${t === '1' ? 'INCOME' : 'EXPENSE'} · ${cat}`, '', total], 'header'));
    items.forEach(([a, v]) => rows.push(row(['', `${a.code} · ${a.name}`, v])));
  }
  return { title: 'Income & Expenses by Tax Category', subtitle: `${from} to ${to}`, columns: [col('Tax category'), col('Account'), col('Amount', M)], rows,
    notes: ['Categories are labels to speed up tax preparation; the accountant decides final form lines (e.g. Form 1065, 1120-S, Schedule C).', 'Business meals are shown at 100%; the deductible portion is usually 50%.'] };
};

const PAYCOLS = ['gross', 'fed_wh', 'ss_ee', 'med_ee', 'state_wh', 'city_wh', 'sdi_pfl', 'other_ded', 'net', 'ss_er', 'med_er', 'futa', 'suta'];
const PAYLABELS = ['Gross wages', 'Federal WH', 'Soc. Sec. (EE)', 'Medicare (EE)', 'NY State WH', 'NYC WH', 'NY SDI/PFL', 'Other ded.', 'Net pay', 'Soc. Sec. (ER)', 'Medicare (ER)', 'FUTA', 'NY SUI'];
R.payroll_summary = async q => {
  const { from, to } = await range(q);
  const sumsql = PAYCOLS.map(c => `SUM(p.${c}) ${c}`).join(',');
  const rows = [];
  rows.push(row(['By employee', ...PAYCOLS.map(() => null)], 'header'));
  const emp = await db.all(`SELECT c.name, COUNT(*) n, ${sumsql} FROM payroll_items p JOIN entries e ON e.id=p.entry_id JOIN contacts c ON c.id=p.employee_id
    WHERE e.voided=0 AND p.pay_date BETWEEN ? AND ? GROUP BY c.id ORDER BY c.name`, from, to);
  emp.forEach(r => rows.push(row([`${r.name} (${r.n} pay runs)`, ...PAYCOLS.map(c => r[c])])));
  rows.push(row(['By calendar quarter (for Form 941 / NYS-45)', ...PAYCOLS.map(() => null)], 'header'));
  const qs = await db.all(`SELECT substr(p.pay_date,1,4) || '-Q' || ((CAST(substr(p.pay_date,6,2) AS INTEGER)+2)/3) qtr, ${sumsql}
    FROM payroll_items p JOIN entries e ON e.id=p.entry_id WHERE e.voided=0 AND p.pay_date BETWEEN ? AND ? GROUP BY qtr ORDER BY qtr`, from, to);
  qs.forEach(r => rows.push(row([r.qtr, ...PAYCOLS.map(c => r[c])])));
  const t = await db.get(`SELECT ${sumsql} FROM payroll_items p JOIN entries e ON e.id=p.entry_id WHERE e.voided=0 AND p.pay_date BETWEEN ? AND ?`, from, to);
  rows.push(row(['TOTAL', ...PAYCOLS.map(c => t[c] || 0)], 'grand'));
  return { title: 'Payroll Summary', subtitle: `${from} to ${to}`, columns: [col('Employee / Period'), ...PAYLABELS.map(l => col(l, M))], rows,
    notes: ['EE = withheld from employee; ER = paid by the company. Use with your payroll provider’s W-2 / 941 / 940 / NYS-45 filings.'] };
};

R.contractors_1099 = async q => {
  const { from, to } = await range(q);
  const threshold = Math.round(Number(await getSetting('threshold_1099', '2000')) * 100);
  const vs = await db.all(`SELECT c.*,
      SUM(CASE WHEN a.subtype='card' THEN l.credit - l.debit ELSE 0 END) card,
      SUM(CASE WHEN a.subtype IS NULL OR a.subtype<>'card' THEN l.credit - l.debit ELSE 0 END) bank
    FROM contacts c JOIN entries e ON e.contact_id=c.id JOIN lines l ON l.entry_id=e.id JOIN accounts a ON a.id=l.account_id
    WHERE c.type='vendor' AND a.is_payment=1 AND e.date BETWEEN ? AND ? GROUP BY c.id ORDER BY c.is_1099 DESC, c.name`, from, to);
  const rows = vs.filter(v => v.card || v.bank).map(v => row([v.name, v.tax_id || (v.is_1099 ? '⚠ missing W-9' : ''), v.address || '', v.is_1099 ? 'Yes' : 'No', v.bank, v.card, v.bank + v.card,
    v.is_1099 && v.bank >= threshold ? 'YES – file 1099-NEC' : '']));
  return { title: 'Vendor Payments & 1099 Report', subtitle: `${from} to ${to}`,
    columns: [col('Vendor'), col('Tax ID (W-9)'), col('Address'), col('1099 vendor?'), col('Paid by bank/cash', M), col('Paid by card', M), col('Total paid', M), col('1099-NEC needed?')], rows,
    notes: [`Threshold set in Settings: $${threshold / 100}. Card payments are excluded (reported on 1099-K by the card processor). Confirm the threshold for the tax year with your accountant.`] };
};

R.ar_aging = async q => {
  const to = q.to || today();
  const invs = await db.all(`SELECT i.*, c.name,
      (SELECT COALESCE(SUM(p.amount),0) FROM invoice_payments p JOIN entries e ON e.id=p.entry_id WHERE p.invoice_id=i.id AND e.voided=0 AND e.date<=?) paid
    FROM invoices i JOIN contacts c ON c.id=i.client_id WHERE i.voided=0 AND i.date<=? ORDER BY i.due_date`, to, to);
  const rows = [];
  const tot = [0, 0, 0, 0, 0, 0];
  for (const i of invs) {
    const bal = i.total - i.paid;
    if (bal <= 0) continue;
    const days = Math.floor((Date.parse(to) - Date.parse(i.due_date)) / 864e5);
    const b = days <= 0 ? 0 : days <= 30 ? 1 : days <= 60 ? 2 : days <= 90 ? 3 : 4;
    const cells = [null, null, null, null, null];
    cells[b] = bal;
    tot[b] += bal; tot[5] += bal;
    rows.push(row([i.name, i.number, i.date, i.due_date, ...cells, bal], null, `#/invoice/${i.id}`));
  }
  rows.push(row(['TOTAL', '', '', '', ...tot], 'grand'));
  return { title: 'Accounts Receivable Aging', subtitle: `As of ${to}`,
    columns: [col('Client'), col('Invoice'), col('Date', D), col('Due', D), col('Current', M), col('1–30 days', M), col('31–60', M), col('61–90', M), col('90+', M), col('Balance', M)], rows };
};

async function byContact(q, type, title) {
  const { from, to } = await range(q);
  const sign = type === 'income' ? '(l.credit - l.debit)' : '(l.debit - l.credit)';
  const rs = await db.all(`SELECT COALESCE(c.name,'(no name)') cname, a.code, a.name aname, SUM(${sign}) amt
    FROM lines l JOIN entries e ON e.id=l.entry_id JOIN accounts a ON a.id=l.account_id LEFT JOIN contacts c ON c.id=e.contact_id
    WHERE a.type=? AND e.date BETWEEN ? AND ? GROUP BY c.id, c.name, a.id, a.code, a.name HAVING SUM(${sign})<>0 ORDER BY cname, a.code`, type, from, to);
  const rows = [];
  let cur = null, sub = 0, grand = 0;
  const flush = () => { if (cur !== null) rows.push(row([`Total ${cur}`, '', sub], 'total')); };
  for (const r of rs) {
    if (r.cname !== cur) { flush(); cur = r.cname; sub = 0; rows.push(row([r.cname, '', null], 'header')); }
    sub += r.amt; grand += r.amt;
    rows.push(row(['', `${r.code} · ${r.aname}`, r.amt]));
  }
  flush();
  rows.push(row(['TOTAL', '', grand], 'grand'));
  return { title, subtitle: `${from} to ${to}`, columns: [col(type === 'income' ? 'Client' : 'Vendor / Payee'), col('Account'), col('Amount', M)], rows };
}
R.income_by_client = q => byContact(q, 'income', 'Income by Client');
R.expenses_by_vendor = q => byContact(q, 'expense', 'Expenses by Vendor');

R.sales_tax = async q => {
  const { from, to } = await range(q);
  const rs = await db.all(`SELECT substr(e.date,1,7) m, SUM(l.credit) collected, SUM(l.debit) paid
    FROM lines l JOIN entries e ON e.id=l.entry_id JOIN accounts a ON a.id=l.account_id WHERE a.subtype='sales_tax' AND e.date BETWEEN ? AND ? GROUP BY m ORDER BY m`, from, to);
  const taxable = await db.all(`SELECT substr(date,1,7) m, SUM(subtotal) s FROM invoices WHERE voided=0 AND tax>0 AND date BETWEEN ? AND ? GROUP BY m`, from, to);
  const tm = new Map(taxable.map(t => [t.m, t.s]));
  const rows = rs.map(r => row([r.m, tm.get(r.m) || 0, r.collected, r.paid]));
  const t = rs.reduce((a, r) => [a[0] + (tm.get(r.m) || 0), a[1] + r.collected, a[2] + r.paid], [0, 0, 0]);
  rows.push(row(['TOTAL', ...t], 'grand'));
  return { title: 'NY Sales Tax', subtitle: `${from} to ${to}`, columns: [col('Month'), col('Taxable sales', M), col('Tax charged / adjusted', M), col('Tax paid to NYS / reversed', M)], rows,
    notes: ['NY quarterly sales tax periods run Mar–May, Jun–Aug, Sep–Nov, Dec–Feb. Whether your services are taxable in NY (e.g. software vs. consulting) is for your accountant to confirm.'] };
};

R.missing_receipts = async q => {
  const { from, to } = await range(q);
  const rs = await db.all(`SELECT e.id, e.date, e.kind, e.memo, c.name, (SELECT SUM(debit) FROM lines WHERE entry_id=e.id) amt FROM entries e LEFT JOIN contacts c ON c.id=e.contact_id
    WHERE e.kind IN ('expense','import','payroll') AND e.voided=0 AND e.date BETWEEN ? AND ?
    AND NOT EXISTS (SELECT 1 FROM attachments a WHERE a.entry_id=e.id)
    AND (e.kind<>'import' OR EXISTS (SELECT 1 FROM lines l JOIN accounts a ON a.id=l.account_id WHERE l.entry_id=e.id AND a.type='expense'))
    ORDER BY e.date`, from, to);
  return { title: 'Transactions Missing a Receipt', subtitle: `${from} to ${to}`, columns: [col('Date', D), col('Entry'), col('Type'), col('Payee'), col('Memo'), col('Amount', M)],
    rows: rs.map(r => row([r.date, `#${r.id}`, r.kind, r.name || '', r.memo || '', r.amt], null, `#/entry/${r.id}`)),
    notes: ['Attach a receipt or bill to each of these so the accountant has proof of every expense.'] };
};

R.reconciliations = async () => {
  const rs = await db.all(`SELECT r.*, a.name aname, u.name uname FROM reconciliations r JOIN accounts a ON a.id=r.account_id LEFT JOIN users u ON u.id=r.user_id ORDER BY r.statement_date DESC`);
  return { title: 'Bank Reconciliations', subtitle: 'History', columns: [col('Account'), col('Statement date', D), col('Statement balance', M), col('Cleared in books', M), col('Difference', M), col('By'), col('Done at (UTC)')],
    rows: rs.map(r => row([r.aname, r.statement_date, r.statement_balance, r.cleared_balance, r.statement_balance - r.cleared_balance, r.uname || '', r.created_at])) };
};

R.audit_log = async q => {
  const { from, to } = await range(q);
  const rs = await db.all(`SELECT a.*, u.name FROM audit a LEFT JOIN users u ON u.id=a.user_id WHERE substr(a.at,1,10) BETWEEN ? AND ? ORDER BY a.id DESC LIMIT 5000`, from, to);
  return { title: 'Audit Log', subtitle: `${from} to ${to}`, columns: [col('When (UTC)'), col('User'), col('Action'), col('Detail')],
    rows: rs.map(r => row([r.at, r.name || '', r.action, r.detail || ''])) };
};

R.chart_of_accounts = async () => {
  const s = await sums(null, today());
  return { title: 'Chart of Accounts', subtitle: `Balances as of ${today()}`, columns: [col('Code'), col('Name'), col('Type'), col('Subtype'), col('Tax category'), col('Active'), col('Balance', M)],
    rows: (await accounts()).map(a => row([a.code, a.name, a.type, a.subtype || '', a.tax_category || '', a.active ? 'Yes' : 'No', natural(a, s.get(a.id))])) };
};

const CATALOG = [
  ['pnl', 'Profit & Loss', 'Income minus expenses = profit. The basis for income tax.'],
  ['balance_sheet', 'Balance Sheet', 'What the company owns, owes, and the owners’ equity.'],
  ['cash_flow', 'Cash Flow Statement', 'Where cash came from and where it went.'],
  ['trial_balance', 'Trial Balance', 'Every account balance; debits must equal credits.'],
  ['general_ledger', 'General Ledger', 'Every transaction, account by account, with running balances.'],
  ['journal', 'Journal', 'Every entry with its debit / credit lines.'],
  ['tax_categories', 'Income & Expenses by Tax Category', 'Totals grouped the way the tax return needs them.'],
  ['owner_equity', 'Owners’ Capital Statement', 'Each owner’s contributions, draws and profit share.'],
  ['owner_activity', 'Owner Contributions & Draws', 'Every owner deposit and withdrawal, listed.'],
  ['payroll_summary', 'Payroll Summary', 'Wages and withholdings by employee and by quarter.'],
  ['contractors_1099', 'Vendor Payments & 1099', 'Who needs a 1099-NEC.'],
  ['income_by_client', 'Income by Client', 'Revenue per client.'],
  ['expenses_by_vendor', 'Expenses by Vendor', 'Spending per vendor / payee.'],
  ['ar_aging', 'A/R Aging', 'Unpaid invoices and how overdue they are.'],
  ['sales_tax', 'NY Sales Tax', 'Sales tax charged and paid.'],
  ['missing_receipts', 'Missing Receipts', 'Expenses with no receipt attached.'],
  ['reconciliations', 'Bank Reconciliations', 'Proof the books match the bank statements.'],
  ['chart_of_accounts', 'Chart of Accounts', 'All accounts with tax categories and balances.'],
  ['audit_log', 'Audit Log', 'Who did what, and when.'],
];

async function run(name, q) {
  if (!Object.prototype.hasOwnProperty.call(R, name)) return null;
  return R[name](q || {});
}

function toCSV(rep) {
  const esc = v => {
    if (v == null) return '';
    const s = String(v);
    return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
  };
  const out = [[rep.title], [rep.subtitle || ''], [], rep.columns.map(c => c.label)];
  for (const r of rep.rows) out.push(r.cells.map((v, i) => rep.columns[i] && rep.columns[i].type === M && typeof v === 'number' ? (v / 100).toFixed(2) : v));
  (rep.notes || []).forEach(n => out.push([], [n]));
  return out.map(r => r.map(esc).join(',')).join('\r\n') + '\r\n';
}

module.exports = { run, toCSV, CATALOG, range, fiscalYearStart, netIncome, sums };
