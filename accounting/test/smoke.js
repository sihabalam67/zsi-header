// End-to-end test: runs the server against a temp database and checks the books balance.
const os = require('os');
const fs = require('fs');
const path = require('path');
const assert = require('assert');

process.env.DATA_DIR = fs.mkdtempSync(path.join(os.tmpdir(), 'zsibooks-'));
const app = require('../server');

(async () => {
  const srv = app.listen(0);
  const base = `http://127.0.0.1:${srv.address().port}`;
  let cookie = '';
  const call = async (method, url, body) => {
    const r = await fetch(base + url, { method, headers: { 'Content-Type': 'application/json', cookie }, body: body ? JSON.stringify(body) : undefined });
    const sc = r.headers.get('set-cookie');
    if (sc) cookie = sc.split(';')[0];
    const ct = r.headers.get('content-type') || '';
    const data = ct.includes('json') ? await r.json() : await r.text();
    if (!r.ok) throw new Error(`${method} ${url} → ${r.status} ${JSON.stringify(data)}`);
    return data;
  };
  const expectFail = async (p, re) => { try { await p; } catch (e) { assert.match(e.message, re); return; } throw new Error('expected failure'); };

  try {
    await call('POST', '/api/setup', { company: 'Zsi.AI LLC', name: 'Owner A', email: 'a@zsi.ai', password: 'password123', owners: [{ name: 'Alpha', share: 50 }, { name: 'Beta', share: 50 }] });
    await call('POST', '/api/login', { email: 'a@zsi.ai', password: 'password123' });
    const accts = await call('GET', '/api/accounts');
    const A = code => accts.find(a => a.code === code).id;
    const contacts = await call('GET', '/api/contacts');
    const [alpha, beta] = contacts.filter(c => c.type === 'owner');
    const bank = A('1000');

    // Owners deposit unequal amounts
    await call('POST', '/api/tx/owner_contribution', { date: '2026-01-05', contact_id: alpha.id, amount: '20000', deposit_to: bank });
    await call('POST', '/api/tx/owner_contribution', { date: '2026-01-06', contact_id: beta.id, amount: '5,000.00', deposit_to: bank });

    // Vendors, client, employee
    const landlord = (await call('POST', '/api/contacts', { type: 'vendor', name: 'NYC Office LLC' })).id;
    const aws = (await call('POST', '/api/contacts', { type: 'vendor', name: 'AWS' })).id;
    const dev = (await call('POST', '/api/contacts', { type: 'vendor', name: 'Freelance Dev', is_1099: true, tax_id: '12-0000000' })).id;
    const client = (await call('POST', '/api/contacts', { type: 'client', name: 'Acme Corp' })).id;
    const emp = (await call('POST', '/api/contacts', { type: 'employee', name: 'Jane Employee' })).id;

    await call('POST', '/api/tx/expense', { date: '2026-02-01', contact_id: landlord, paid_from: bank, items: [{ account_id: A('5300'), amount: 3000 }] });
    await call('POST', '/api/tx/expense', { date: '2026-02-03', contact_id: aws, paid_from: A('2100'), items: [{ account_id: A('5400'), amount: 450.5 }, { account_id: A('5420'), amount: 49.5 }] });
    await call('POST', '/api/tx/expense', { date: '2026-03-01', contact_id: dev, paid_from: bank, items: [{ account_id: A('5200'), amount: 2500 }] });

    // Payroll
    const pr = await call('POST', '/api/tx/payroll', { date: '2026-02-15', contact_id: emp, paid_from: bank, gross: 5000, fed_wh: 600, ss_ee: 310, med_ee: 72.5, state_wh: 250, city_wh: 150, sdi_pfl: 20, ss_er: 310, med_er: 72.5, futa: 30, suta: 200 });

    // Invoice with NYC sales tax, partial payment with Stripe fee
    const inv = await call('POST', '/api/invoices', { client_id: client, date: '2026-02-10', due_date: '2026-03-10', tax_rate: 8.875, items: [{ description: 'AI build', qty: 10, unit_price: 150 }] });
    const invd = await call('GET', `/api/invoices/${inv.id}`);
    assert.strictEqual(invd.total, 150000 + 13313);
    await call('POST', `/api/invoices/${inv.id}/payments`, { date: '2026-03-01', amount: 1000, deposit_to: bank, fee: 29.3 });
    await expectFail(call('POST', `/api/invoices/${inv.id}/payments`, { date: '2026-03-02', amount: 99999, deposit_to: bank }), /more than/);

    // Transfer to pay the card, owner draw
    await call('POST', '/api/tx/transfer', { date: '2026-03-05', from_account: bank, to_account: A('2100'), amount: 500 });
    await call('POST', '/api/tx/owner_draw', { date: '2026-03-10', contact_id: alpha.id, amount: 1000, paid_from: bank });

    // Unbalanced journal must fail
    await expectFail(call('POST', '/api/tx/journal', { date: '2026-03-11', lines: [{ account_id: A('5990'), debit: 10 }, { account_id: bank, credit: 9 }] }), /out of balance/);

    // Void the rent and check it nets out
    const ents = await call('GET', '/api/entries?kind=expense');
    const rent = ents.find(e => e.contact_id === landlord);
    await call('POST', `/api/entries/${rent.id}/void`, { reason: 'test' });

    // Bank import with duplicate detection
    const rows = [{ date: '2026-03-20', description: 'GITHUB INC', amount: -21, account_id: A('5410') }, { date: '2026-03-21', description: 'Interest', amount: 1.23, account_id: A('4900') }];
    let r = await call('POST', '/api/import', { account_id: bank, rows });
    assert.strictEqual(r.created, 2);
    r = await call('POST', '/api/import', { account_id: bank, rows });
    assert.strictEqual(r.skipped, 2);

    // Lock date
    await call('PUT', '/api/settings', { lock_date: '2026-01-31' });
    await expectFail(call('POST', '/api/tx/expense', { date: '2026-01-15', paid_from: bank, items: [{ account_id: A('5990'), amount: 5 }] }), /closed/);

    // ---- Reports ----
    const q = '?from=2026-01-01&to=2026-12-31';
    const tb = await call('GET', '/api/reports/trial_balance' + q);
    const g = tb.rows.find(x => x.style === 'grand').cells;
    assert.strictEqual(g[3], g[4], 'trial balance must balance');
    const bs = await call('GET', '/api/reports/balance_sheet' + q);
    assert.match(bs.notes[0], /Balanced/);
    const pnl = await call('GET', '/api/reports/pnl' + q);
    const net = pnl.rows.find(x => x.style === 'grand').cells[1];
    // Income 1500 + 1.23 ; expenses: aws 500 + dev 2500 + payroll 5000 + er 612.5 + fee 29.3 + github 21 (rent voided)
    assert.strictEqual(net, 150000 + 123 - (50000 + 250000 + 500000 + 61250 + 2930 + 2100));
    const oe = await call('GET', '/api/reports/owner_equity' + q);
    const alphaRow = oe.rows.find(x => x.cells[0] === 'Alpha').cells;
    assert.strictEqual(alphaRow[3], 2000000); assert.strictEqual(alphaRow[4], 100000);
    const nec = await call('GET', '/api/reports/contractors_1099' + q);
    assert.ok(nec.rows.find(x => x.cells[0] === 'Freelance Dev').cells[7].startsWith('YES'));
    const ps = await call('GET', '/api/reports/payroll_summary' + q);
    assert.strictEqual(ps.rows.find(x => x.style === 'grand').cells[1], 500000);
    const cf = await call('GET', '/api/reports/cash_flow' + q);
    const dash = await call('GET', '/api/dashboard');
    const cash = dash.accounts.filter(a => a.type === 'asset').reduce((t, a) => t + a.balance, 0);
    const card = -dash.accounts.filter(a => a.type !== 'asset').reduce((t, a) => t + a.balance, 0);
    assert.strictEqual(cf.rows[cf.rows.length - 1].cells[1], cash + card, 'cash flow closing = bank - card debt');
    for (const name of (await call('GET', '/api/reports')).map(x => x.id)) {
      await call('GET', `/api/reports/${name}${q}`);
      const csv = await call('GET', `/api/reports/${name}${q}&format=csv`);
      assert.ok(csv.length > 10);
    }
    const pk = await fetch(`${base}/api/export/package${q}`, { headers: { cookie } });
    assert.strictEqual(pk.status, 200);
    assert.ok((await pk.arrayBuffer()).byteLength > 1000);

    // Roles: accountant is read-only
    await call('POST', '/api/users', { name: 'CPA', email: 'cpa@x.com', password: 'password123', role: 'accountant' });
    await call('POST', '/api/login', { email: 'cpa@x.com', password: 'password123' });
    await expectFail(call('POST', '/api/tx/expense', { date: '2026-04-01', paid_from: bank, items: [{ account_id: A('5990'), amount: 5 }] }), /403/);
    await call('GET', '/api/reports/pnl' + q);

    console.log('✔ All smoke tests passed. Net income:', net / 100, '| cash:', cash / 100);
  } catch (e) {
    console.error('✘', e);
    process.exitCode = 1;
  } finally {
    srv.close();
  }
})();
