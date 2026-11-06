// Posting engine: turns simple business actions into balanced double-entry journal entries.
const { db, getSetting, accountByCode, audit } = require('./db');

class UserError extends Error {}

const cents = v => {
  if (v === '' || v == null) return 0;
  const n = Number(String(v).replace(/[$,\s]/g, ''));
  if (!Number.isFinite(n)) throw new UserError(`"${v}" is not a valid amount`);
  return Math.round(n * 100);
};
const isDate = d => /^\d{4}-\d{2}-\d{2}$/.test(d || '') && !isNaN(Date.parse(d));

function account(id) {
  const a = db.prepare('SELECT * FROM accounts WHERE id=?').get(Number(id));
  if (!a) throw new UserError('Please choose an account / category');
  if (!a.active) throw new UserError(`Account "${a.name}" is inactive`);
  return a;
}
function contact(id, type) {
  if (!id) return null;
  const c = db.prepare('SELECT * FROM contacts WHERE id=?').get(Number(id));
  if (!c) throw new UserError('Contact not found');
  if (type && c.type !== type) throw new UserError(`${c.name} is not a ${type}`);
  return c;
}
function paymentAccount(id) {
  const a = account(id);
  if (!a.is_payment) throw new UserError(`"${a.name}" is not a bank / cash / card account`);
  return a;
}

function checkLock(date) {
  if (!isDate(date)) throw new UserError('Please enter a valid date');
  const lock = getSetting('lock_date');
  if (lock && date <= lock)
    throw new UserError(`The books are closed through ${lock}. Ask an owner to change the lock date, or post a correction in an open period.`);
}

// Core: write an entry with lines. lines: [{account_id, debit, credit, memo}] in cents.
function post({ date, kind, memo, reference, contact_id, lines, userId, import_hash }) {
  checkLock(date);
  lines = lines.filter(l => (l.debit || 0) > 0 || (l.credit || 0) > 0);
  if (lines.length < 2) throw new UserError('An entry needs at least two non-zero lines');
  let dr = 0, cr = 0;
  for (const l of lines) {
    if ((l.debit || 0) < 0 || (l.credit || 0) < 0) throw new UserError('Amounts must be positive');
    if (l.debit > 0 && l.credit > 0) throw new UserError('A line cannot have both a debit and a credit');
    account(l.account_id);
    dr += l.debit || 0; cr += l.credit || 0;
  }
  if (dr !== cr) throw new UserError(`Entry is out of balance: debits $${(dr / 100).toFixed(2)} vs credits $${(cr / 100).toFixed(2)}`);
  const r = db.prepare(`INSERT INTO entries(date,kind,memo,reference,contact_id,created_by,import_hash)
    VALUES(?,?,?,?,?,?,?)`).run(date, kind, memo || null, reference || null, contact_id || null, userId || null, import_hash || null);
  const id = r.lastInsertRowid;
  const ins = db.prepare('INSERT INTO lines(entry_id,account_id,debit,credit,memo) VALUES(?,?,?,?,?)');
  for (const l of lines) ins.run(id, Number(l.account_id), l.debit || 0, l.credit || 0, l.memo || null);
  audit(userId, 'entry.create', { id, kind, date, amount: dr });
  return Number(id);
}

// ---------- Business actions ----------
const builders = {
  // Paying a bill / expense. items allow splitting one payment across categories.
  expense(b) {
    const from = paymentAccount(b.paid_from);
    const c = contact(b.contact_id);
    const items = (b.items && b.items.length ? b.items : [{ account_id: b.account_id, amount: b.amount, memo: b.memo }])
      .map(i => ({ account_id: account(i.account_id).id, amt: cents(i.amount), memo: i.memo }))
      .filter(i => i.amt !== 0);
    const total = items.reduce((s, i) => s + i.amt, 0);
    if (total <= 0) throw new UserError('Enter an amount greater than zero');
    return {
      kind: 'expense', contact_id: c && c.id,
      lines: [
        ...items.map(i => i.amt > 0 ? { account_id: i.account_id, debit: i.amt, memo: i.memo } : { account_id: i.account_id, credit: -i.amt, memo: i.memo }),
        { account_id: from.id, credit: total },
      ],
    };
  },

  // Money received that is not tied to an invoice.
  income(b) {
    const to = paymentAccount(b.deposit_to);
    const cat = account(b.account_id);
    const amt = cents(b.amount);
    if (amt <= 0) throw new UserError('Enter an amount greater than zero');
    const c = contact(b.contact_id);
    return { kind: 'income', contact_id: c && c.id, lines: [{ account_id: to.id, debit: amt }, { account_id: cat.id, credit: amt }] };
  },

  owner_contribution(b) {
    const owner = contact(b.contact_id, 'owner');
    if (!owner) throw new UserError('Choose which owner put the money in');
    const to = paymentAccount(b.deposit_to);
    const cap = db.prepare(`SELECT * FROM accounts WHERE owner_contact_id=? AND subtype='capital'`).get(owner.id);
    const amt = cents(b.amount);
    if (amt <= 0) throw new UserError('Enter an amount greater than zero');
    return { kind: 'owner_contribution', contact_id: owner.id, lines: [{ account_id: to.id, debit: amt }, { account_id: cap.id, credit: amt }] };
  },

  owner_draw(b) {
    const owner = contact(b.contact_id, 'owner');
    if (!owner) throw new UserError('Choose which owner took the money');
    const from = paymentAccount(b.paid_from);
    const dr = db.prepare(`SELECT * FROM accounts WHERE owner_contact_id=? AND subtype='draws'`).get(owner.id);
    const amt = cents(b.amount);
    if (amt <= 0) throw new UserError('Enter an amount greater than zero');
    return { kind: 'owner_draw', contact_id: owner.id, lines: [{ account_id: dr.id, debit: amt }, { account_id: from.id, credit: amt }] };
  },

  transfer(b) {
    const from = paymentAccount(b.from_account);
    const to = paymentAccount(b.to_account);
    if (from.id === to.id) throw new UserError('From and To must be different accounts');
    const amt = cents(b.amount);
    if (amt <= 0) throw new UserError('Enter an amount greater than zero');
    return { kind: 'transfer', lines: [{ account_id: to.id, debit: amt }, { account_id: from.id, credit: amt }] };
  },

  // Payroll: records gross wages, every withholding as a liability, employer taxes, and net pay.
  payroll(b) {
    const emp = contact(b.contact_id, 'employee');
    if (!emp) throw new UserError('Choose the employee');
    const from = paymentAccount(b.paid_from);
    const p = {};
    for (const k of ['gross', 'fed_wh', 'ss_ee', 'med_ee', 'state_wh', 'city_wh', 'sdi_pfl', 'other_ded', 'ss_er', 'med_er', 'futa', 'suta'])
      p[k] = cents(b[k]);
    if (p.gross <= 0) throw new UserError('Enter the gross pay');
    p.net = p.gross - p.fed_wh - p.ss_ee - p.med_ee - p.state_wh - p.city_wh - p.sdi_pfl - p.other_ded;
    if (p.net <= 0) throw new UserError('Deductions are larger than gross pay');
    const er = p.ss_er + p.med_er + p.futa + p.suta;
    const A = code => accountByCode(code).id;
    return {
      kind: 'payroll', contact_id: emp.id,
      lines: [
        { account_id: A('5000'), debit: p.gross, memo: 'Gross wages' },
        { account_id: A('5100'), debit: er, memo: 'Employer payroll taxes' },
        { account_id: from.id, credit: p.net, memo: 'Net pay' },
        { account_id: A('2200'), credit: p.fed_wh, memo: 'Federal income tax withheld' },
        { account_id: A('2210'), credit: p.ss_ee + p.med_ee + p.ss_er + p.med_er, memo: 'Social Security & Medicare (employee + employer)' },
        { account_id: A('2220'), credit: p.state_wh, memo: 'NY State withholding' },
        { account_id: A('2230'), credit: p.city_wh, memo: 'NYC withholding' },
        { account_id: A('2240'), credit: p.sdi_pfl, memo: 'NY SDI / PFL' },
        { account_id: A('2250'), credit: p.futa, memo: 'FUTA' },
        { account_id: A('2260'), credit: p.suta, memo: 'NY SUI' },
        { account_id: A('2270'), credit: p.other_ded, memo: 'Other deductions' },
      ],
      after(entryId, date) {
        db.prepare(`INSERT INTO payroll_items(entry_id,employee_id,pay_date,period_start,period_end,gross,fed_wh,ss_ee,med_ee,state_wh,city_wh,sdi_pfl,other_ded,net,ss_er,med_er,futa,suta)
          VALUES(@entry_id,@employee_id,@pay_date,@period_start,@period_end,@gross,@fed_wh,@ss_ee,@med_ee,@state_wh,@city_wh,@sdi_pfl,@other_ded,@net,@ss_er,@med_er,@futa,@suta)`)
          .run({ ...p, entry_id: entryId, employee_id: emp.id, pay_date: date, period_start: b.period_start || null, period_end: b.period_end || null });
      },
    };
  },

  // Free-form journal entry for the accountant / adjustments.
  journal(b) {
    const lines = (b.lines || []).map(l => ({ account_id: l.account_id, debit: cents(l.debit), credit: cents(l.credit), memo: l.memo }));
    return { kind: 'journal', contact_id: b.contact_id || null, lines };
  },
};

function record(type, body, userId) {
  const fn = builders[type];
  if (!fn) throw new UserError('Unknown transaction type');
  return db.transaction(() => {
    const built = fn(body);
    const id = post({ date: body.date, memo: body.memo, reference: body.reference, ...built, userId });
    if (built.after) built.after(id, body.date);
    return id;
  })();
}

// Never delete: a void posts an exact reversing entry and flags the original.
function voidEntry(id, userId, reason) {
  return db.transaction(() => {
    const e = db.prepare('SELECT * FROM entries WHERE id=?').get(id);
    if (!e) throw new UserError('Entry not found');
    if (e.voided) throw new UserError('Already voided');
    if (e.kind === 'void') throw new UserError('A reversal cannot itself be voided');
    const inv = db.prepare('SELECT id FROM invoices WHERE entry_id=? AND voided=0').get(id);
    if (inv && db.prepare('SELECT COUNT(*) c FROM invoice_payments p JOIN entries e ON e.id=p.entry_id WHERE p.invoice_id=? AND e.voided=0').get(inv.id).c)
      throw new UserError('This invoice has payments. Void the payments first.');
    const lock = getSetting('lock_date');
    const today = new Date().toISOString().slice(0, 10);
    const date = lock && e.date <= lock ? today : e.date; // reverse in the same period unless that period is closed
    const lines = db.prepare('SELECT * FROM lines WHERE entry_id=?').all(id)
      .map(l => ({ account_id: l.account_id, debit: l.credit, credit: l.debit, memo: l.memo }));
    const rid = post({ date, kind: 'void', memo: `VOID of #${id}${reason ? ': ' + reason : ''}`, reference: e.reference, contact_id: e.contact_id, lines, userId });
    db.prepare('UPDATE entries SET voided=1 WHERE id=?').run(id);
    db.prepare('UPDATE entries SET void_of=? WHERE id=?').run(id, rid);
    if (inv) db.prepare('UPDATE invoices SET voided=1 WHERE id=?').run(inv.id);
    audit(userId, 'entry.void', { id, reversal: rid, reason });
    return rid;
  })();
}

// ---------- Invoices ----------
function nextInvoiceNumber() {
  const prefix = getSetting('invoice_prefix', 'INV-');
  let n = Number(getSetting('invoice_next', '1001'));
  while (db.prepare('SELECT 1 FROM invoices WHERE number=?').get(prefix + n)) n++;
  return prefix + n;
}

function createInvoice(b, userId) {
  return db.transaction(() => {
    const client = contact(b.client_id, 'client');
    if (!client) throw new UserError('Choose a client');
    if (!isDate(b.due_date)) throw new UserError('Enter a due date');
    const income = account(b.income_account_id || accountByCode('4000').id);
    if (income.type !== 'income') throw new UserError('Invoice category must be an income account');
    const items = (b.items || []).filter(i => i.description || i.unit_price)
      .map(i => {
        const qty = Number(i.qty || 1);
        const unit = cents(i.unit_price);
        return { description: i.description || 'Services', qty, unit_price: unit, amount: Math.round(qty * unit) };
      });
    if (!items.length) throw new UserError('Add at least one line item');
    const subtotal = items.reduce((s, i) => s + i.amount, 0);
    if (subtotal <= 0) throw new UserError('Invoice total must be greater than zero');
    const tax_rate = Number(b.tax_rate || 0);
    const tax = Math.round(subtotal * tax_rate / 100);
    const total = subtotal + tax;
    const number = (b.number || '').trim() || nextInvoiceNumber();
    if (db.prepare('SELECT 1 FROM invoices WHERE number=?').get(number)) throw new UserError(`Invoice number ${number} already exists`);
    const entryId = post({
      date: b.date, kind: 'invoice', memo: `Invoice ${number} – ${client.name}`, reference: number, contact_id: client.id, userId,
      lines: [
        { account_id: accountByCode('1100').id, debit: total },
        { account_id: income.id, credit: subtotal },
        { account_id: accountByCode('2300').id, credit: tax, memo: `Sales tax ${tax_rate}%` },
      ],
    });
    const r = db.prepare(`INSERT INTO invoices(number,client_id,date,due_date,memo,subtotal,tax_rate,tax,total,income_account_id,entry_id)
      VALUES(?,?,?,?,?,?,?,?,?,?,?)`).run(number, client.id, b.date, b.due_date, b.memo || null, subtotal, tax_rate, tax, total, income.id, entryId);
    const ins = db.prepare('INSERT INTO invoice_items(invoice_id,description,qty,unit_price,amount) VALUES(?,?,?,?,?)');
    items.forEach(i => ins.run(r.lastInsertRowid, i.description, i.qty, i.unit_price, i.amount));
    const m = number.match(/(\d+)$/);
    if (m && Number(m[1]) >= Number(getSetting('invoice_next', '1001'))) require('./db').setSetting('invoice_next', Number(m[1]) + 1);
    return Number(r.lastInsertRowid);
  })();
}

function invoicePaid(invoiceId) {
  return db.prepare(`SELECT COALESCE(SUM(p.amount),0) s FROM invoice_payments p JOIN entries e ON e.id=p.entry_id
    WHERE p.invoice_id=? AND e.voided=0`).get(invoiceId).s;
}

function payInvoice(invoiceId, b, userId) {
  return db.transaction(() => {
    const inv = db.prepare('SELECT * FROM invoices WHERE id=?').get(invoiceId);
    if (!inv || inv.voided) throw new UserError('Invoice not found or voided');
    const due = inv.total - invoicePaid(inv.id);
    const amt = b.amount ? cents(b.amount) : due;
    if (amt <= 0) throw new UserError('Enter an amount greater than zero');
    if (amt > due) throw new UserError(`Payment is more than the $${(due / 100).toFixed(2)} still due`);
    const to = paymentAccount(b.deposit_to);
    const fee = cents(b.fee); // e.g. Stripe / PayPal fee taken out before deposit
    const lines = [
      { account_id: to.id, debit: amt - fee },
      { account_id: accountByCode('5910').id, debit: fee, memo: 'Payment processing fee' },
      { account_id: accountByCode('1100').id, credit: amt },
    ];
    const entryId = post({ date: b.date, kind: 'invoice_payment', memo: `Payment for ${inv.number}`, reference: inv.number, contact_id: inv.client_id, lines, userId });
    db.prepare('INSERT INTO invoice_payments(invoice_id,entry_id,amount) VALUES(?,?,?)').run(inv.id, entryId, amt);
    return entryId;
  })();
}

// ---------- Bank CSV import ----------
function importRows(accountId, rows, userId) {
  const bank = paymentAccount(accountId);
  let created = 0, skipped = 0;
  const errors = [];
  for (const [i, r] of rows.entries()) {
    try {
      const amt = cents(r.amount);
      if (!amt) { skipped++; continue; }
      const cat = account(r.account_id);
      const hash = `${bank.id}|${r.date}|${amt}|${(r.description || '').trim().toLowerCase()}|${r.dup || 0}`;
      if (db.prepare('SELECT 1 FROM entries WHERE import_hash=?').get(hash)) { skipped++; continue; }
      const lines = amt > 0
        ? [{ account_id: bank.id, debit: amt }, { account_id: cat.id, credit: amt }]
        : [{ account_id: cat.id, debit: -amt }, { account_id: bank.id, credit: -amt }];
      db.transaction(() => post({ date: r.date, kind: 'import', memo: r.description, contact_id: r.contact_id || null, lines, userId, import_hash: hash }))();
      created++;
    } catch (e) {
      errors.push(`Row ${i + 1}: ${e.message}`);
    }
  }
  return { created, skipped, errors };
}

module.exports = { UserError, cents, isDate, record, voidEntry, createInvoice, payInvoice, invoicePaid, importRows, nextInvoiceNumber, post };
