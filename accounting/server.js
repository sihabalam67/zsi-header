// Zsi Books – HTTP server and JSON API.
const express = require('express');
const crypto = require('crypto');
const path = require('path');
const fs = require('fs');
const multer = require('multer');
const yazl = require('yazl');
const { db, DATA_DIR, getSetting, setSetting, createOwnerAccounts, audit } = require('./db');
const L = require('./ledger');
const reports = require('./reports');

const app = express();
app.disable('x-powered-by');
app.use(express.json({ limit: '5mb' }));
app.use((req, res, next) => {
  res.set('X-Content-Type-Options', 'nosniff');
  res.set('X-Frame-Options', 'DENY');
  res.set('Referrer-Policy', 'same-origin');
  next();
});
app.use(express.static(path.join(__dirname, 'public')));

const UPLOADS = path.join(DATA_DIR, 'uploads');
const upload = multer({
  storage: multer.diskStorage({
    destination: UPLOADS,
    filename: (req, f, cb) => cb(null, crypto.randomBytes(16).toString('hex') + path.extname(f.originalname).toLowerCase().replace(/[^.a-z0-9]/g, '')),
  }),
  limits: { fileSize: 20 * 1024 * 1024, files: 10 },
});

// ---------- auth ----------
const hash = pw => {
  const salt = crypto.randomBytes(16).toString('hex');
  return `${salt}:${crypto.scryptSync(pw, salt, 64).toString('hex')}`;
};
const verify = (pw, stored) => {
  const [salt, h] = stored.split(':');
  const a = Buffer.from(h, 'hex'), b = crypto.scryptSync(pw, salt, 64);
  return a.length === b.length && crypto.timingSafeEqual(a, b);
};
const cookie = req => Object.fromEntries((req.headers.cookie || '').split(';').map(c => c.trim().split('=')).filter(p => p[0]));
const SECURE = process.env.COOKIE_SECURE === '1';
const setSession = (res, token) => res.set('Set-Cookie', `sid=${token}; HttpOnly; Path=/; SameSite=Lax; Max-Age=${60 * 60 * 24 * 30}${SECURE ? '; Secure' : ''}`);

function currentUser(req) {
  const t = cookie(req).sid;
  if (!t) return null;
  return db.prepare(`SELECT u.id,u.name,u.email,u.role FROM sessions s JOIN users u ON u.id=s.user_id
    WHERE s.token=? AND u.active=1 AND s.created_at > datetime('now','-30 days')`).get(t) || null;
}
const auth = (...roles) => (req, res, next) => {
  const u = currentUser(req);
  if (!u) return res.status(401).json({ error: 'Please sign in' });
  if (roles.length && !roles.includes(u.role)) return res.status(403).json({ error: 'Your role does not allow this action' });
  req.user = u;
  next();
};
const WRITE = ['owner', 'staff'];
const ANY = [];

const attempts = new Map();
function rateLimit(key) {
  const now = Date.now();
  const a = (attempts.get(key) || []).filter(t => now - t < 15 * 60e3);
  a.push(now);
  attempts.set(key, a);
  return a.length > 10;
}

const h = fn => (req, res) => {
  try {
    const out = fn(req, res);
    if (out !== undefined && !res.headersSent) res.json(out);
  } catch (e) {
    if (e instanceof L.UserError || /UNIQUE|CHECK/.test(e.message)) return res.status(400).json({ error: e.message });
    console.error(e);
    res.status(500).json({ error: 'Something went wrong: ' + e.message });
  }
};

const isSetup = () => !!db.prepare('SELECT 1 FROM users LIMIT 1').get();
const allSettings = () => Object.fromEntries(db.prepare('SELECT key,value FROM settings').all().map(r => [r.key, r.value]));

app.get('/api/state', h(req => ({ setup: isSetup(), user: currentUser(req), settings: isSetup() ? allSettings() : {} })));

app.post('/api/setup', h(req => {
  if (isSetup()) throw new L.UserError('Already set up');
  const b = req.body;
  if (!b.company || !b.name || !b.email || !b.password) throw new L.UserError('Fill in company, your name, email and password');
  if (String(b.password).length < 8) throw new L.UserError('Password must be at least 8 characters');
  const owners = (b.owners || []).map(o => ({ name: String(o.name || '').trim(), share: Number(o.share || 0) })).filter(o => o.name);
  if (!owners.length) throw new L.UserError('Add at least one owner');
  db.transaction(() => {
    setSetting('company', b.company);
    setSetting('ein', b.ein || '');
    setSetting('address', b.address || '');
    setSetting('entity_type', b.entity_type || 'Multi-member LLC (taxed as partnership)');
    setSetting('fiscal_start_month', b.fiscal_start_month || '1');
    setSetting('invoice_prefix', 'INV-');
    setSetting('invoice_next', '1001');
    setSetting('threshold_1099', '2000');
    setSetting('sales_tax_rate', '0');
    setSetting('lock_date', '');
    const u = db.prepare('INSERT INTO users(name,email,pass_hash,role) VALUES(?,?,?,?)').run(b.name, b.email, hash(b.password), 'owner');
    for (const o of owners) {
      const r = db.prepare(`INSERT INTO contacts(type,name,profit_share) VALUES('owner',?,?)`).run(o.name, o.share);
      createOwnerAccounts({ id: r.lastInsertRowid, name: o.name });
    }
    if (b.bank_name) db.prepare(`UPDATE accounts SET name=? WHERE code='1000'`).run(b.bank_name);
    audit(u.lastInsertRowid, 'setup', { company: b.company });
  })();
  return { ok: true };
}));

app.post('/api/login', h((req, res) => {
  if (rateLimit(req.ip)) return res.status(429).json({ error: 'Too many attempts. Try again in 15 minutes.' });
  const u = db.prepare('SELECT * FROM users WHERE email=? AND active=1').get(String(req.body.email || ''));
  if (!u || !verify(String(req.body.password || ''), u.pass_hash)) throw new L.UserError('Wrong email or password');
  const token = crypto.randomBytes(32).toString('hex');
  db.prepare('INSERT INTO sessions(token,user_id) VALUES(?,?)').run(token, u.id);
  setSession(res, token);
  audit(u.id, 'login');
  return { ok: true };
}));
app.post('/api/logout', h((req, res) => {
  db.prepare('DELETE FROM sessions WHERE token=?').run(cookie(req).sid || '');
  res.set('Set-Cookie', 'sid=; Path=/; Max-Age=0');
  return { ok: true };
}));

// ---------- settings & users ----------
const SETTING_KEYS = ['company', 'ein', 'address', 'entity_type', 'fiscal_start_month', 'invoice_prefix', 'invoice_next', 'threshold_1099', 'sales_tax_rate', 'lock_date', 'nys_sales_tax_id', 'phone', 'email'];
app.put('/api/settings', auth('owner'), h(req => {
  for (const k of SETTING_KEYS) if (k in req.body) {
    if (k === 'lock_date' && req.body[k] && !L.isDate(req.body[k])) throw new L.UserError('Lock date must be a date');
    setSetting(k, req.body[k]);
  }
  audit(req.user.id, 'settings.update', req.body);
  return allSettings();
}));

app.get('/api/users', auth('owner'), h(() => db.prepare('SELECT id,name,email,role,active,created_at FROM users').all()));
app.post('/api/users', auth('owner'), h(req => {
  const { name, email, password, role } = req.body;
  if (!name || !email || !password || password.length < 8) throw new L.UserError('Name, email and an 8+ character password are required');
  const r = db.prepare('INSERT INTO users(name,email,pass_hash,role) VALUES(?,?,?,?)').run(name, email, hash(password), role || 'staff');
  audit(req.user.id, 'user.create', { email, role });
  return { id: r.lastInsertRowid };
}));
app.patch('/api/users/:id', auth('owner'), h(req => {
  const id = Number(req.params.id);
  const b = req.body;
  if (b.password) { if (b.password.length < 8) throw new L.UserError('Password must be 8+ characters'); db.prepare('UPDATE users SET pass_hash=? WHERE id=?').run(hash(b.password), id); db.prepare('DELETE FROM sessions WHERE user_id=?').run(id); }
  if (b.role) db.prepare('UPDATE users SET role=? WHERE id=?').run(b.role, id);
  if ('active' in b) {
    if (id === req.user.id && !b.active) throw new L.UserError('You cannot deactivate yourself');
    db.prepare('UPDATE users SET active=? WHERE id=?').run(b.active ? 1 : 0, id);
    if (!b.active) db.prepare('DELETE FROM sessions WHERE user_id=?').run(id);
  }
  audit(req.user.id, 'user.update', { id, role: b.role, active: b.active, password: b.password ? 'changed' : undefined });
  return { ok: true };
}));
app.post('/api/me/password', auth(), h(req => {
  const u = db.prepare('SELECT * FROM users WHERE id=?').get(req.user.id);
  if (!verify(String(req.body.current || ''), u.pass_hash)) throw new L.UserError('Current password is wrong');
  if (String(req.body.password || '').length < 8) throw new L.UserError('New password must be 8+ characters');
  db.prepare('UPDATE users SET pass_hash=? WHERE id=?').run(hash(req.body.password), u.id);
  audit(u.id, 'password.change');
  return { ok: true };
}));

// ---------- accounts ----------
app.get('/api/accounts', auth(), h(() => {
  const s = reports.sums(null, '9999-12-31');
  return db.prepare('SELECT * FROM accounts ORDER BY code').all().map(a => {
    const v = s.get(a.id);
    const bal = v ? (['liability', 'equity', 'income'].includes(a.type) ? -v.net : v.net) : 0;
    return { ...a, balance: bal };
  });
}));
app.post('/api/accounts', auth('owner'), h(req => {
  const { code, name, type, subtype, tax_category, is_payment, description } = req.body;
  if (!code || !name || !type) throw new L.UserError('Code, name and type are required');
  const r = db.prepare('INSERT INTO accounts(code,name,type,subtype,tax_category,is_payment,description) VALUES(?,?,?,?,?,?,?)')
    .run(code, name, type, subtype || (is_payment ? (type === 'asset' ? 'bank' : 'card') : null), tax_category || null, is_payment ? 1 : 0, description || null);
  audit(req.user.id, 'account.create', req.body);
  return { id: r.lastInsertRowid };
}));
app.patch('/api/accounts/:id', auth('owner'), h(req => {
  const a = db.prepare('SELECT * FROM accounts WHERE id=?').get(Number(req.params.id));
  if (!a) throw new L.UserError('Not found');
  const b = { ...a, ...req.body };
  db.prepare('UPDATE accounts SET name=?, tax_category=?, active=?, description=? WHERE id=?')
    .run(b.name, b.tax_category || null, b.active ? 1 : 0, b.description || null, a.id);
  audit(req.user.id, 'account.update', { id: a.id, ...req.body });
  return { ok: true };
}));

// ---------- contacts ----------
app.get('/api/contacts', auth(), h(req => {
  const t = req.query.type;
  return db.prepare(`SELECT * FROM contacts ${t ? 'WHERE type=?' : ''} ORDER BY type, name`).all(...(t ? [t] : []));
}));
app.post('/api/contacts', auth(...WRITE), h(req => {
  const b = req.body;
  if (!b.name || !b.type) throw new L.UserError('Name and type are required');
  return db.transaction(() => {
    const r = db.prepare('INSERT INTO contacts(type,name,email,phone,address,tax_id,is_1099,profit_share,notes) VALUES(?,?,?,?,?,?,?,?,?)')
      .run(b.type, b.name.trim(), b.email || null, b.phone || null, b.address || null, b.tax_id || null, b.is_1099 ? 1 : 0, b.type === 'owner' ? Number(b.profit_share || 0) : null, b.notes || null);
    if (b.type === 'owner') createOwnerAccounts({ id: r.lastInsertRowid, name: b.name.trim() });
    audit(req.user.id, 'contact.create', { id: r.lastInsertRowid, type: b.type, name: b.name });
    return { id: r.lastInsertRowid };
  })();
}));
app.patch('/api/contacts/:id', auth(...WRITE), h(req => {
  const c = db.prepare('SELECT * FROM contacts WHERE id=?').get(Number(req.params.id));
  if (!c) throw new L.UserError('Not found');
  const b = { ...c, ...req.body };
  db.prepare('UPDATE contacts SET name=?,email=?,phone=?,address=?,tax_id=?,is_1099=?,profit_share=?,notes=?,active=? WHERE id=?')
    .run(b.name, b.email, b.phone, b.address, b.tax_id, b.is_1099 ? 1 : 0, c.type === 'owner' ? Number(b.profit_share || 0) : null, b.notes, b.active ? 1 : 0, c.id);
  if (c.type === 'owner' && b.name !== c.name) {
    db.prepare(`UPDATE accounts SET name=? WHERE owner_contact_id=? AND subtype='capital'`).run(`Owner Capital – ${b.name}`, c.id);
    db.prepare(`UPDATE accounts SET name=? WHERE owner_contact_id=? AND subtype='draws'`).run(`Owner Draws – ${b.name}`, c.id);
  }
  audit(req.user.id, 'contact.update', { id: c.id, ...req.body });
  return { ok: true };
}));

// ---------- transactions ----------
app.post('/api/tx/:type', auth(...WRITE), h(req => ({ id: L.record(req.params.type, req.body, req.user.id) })));

app.get('/api/entries', auth(), h(req => {
  const q = req.query;
  const where = ['1=1'], p = [];
  if (q.from) { where.push('e.date >= ?'); p.push(q.from); }
  if (q.to) { where.push('e.date <= ?'); p.push(q.to); }
  if (q.kind) { where.push('e.kind = ?'); p.push(q.kind); }
  if (q.contact_id) { where.push('e.contact_id = ?'); p.push(Number(q.contact_id)); }
  if (q.account_id) { where.push('EXISTS (SELECT 1 FROM lines x WHERE x.entry_id=e.id AND x.account_id=?)'); p.push(Number(q.account_id)); }
  if (q.q) { where.push(`(e.memo LIKE ? OR e.reference LIKE ? OR c.name LIKE ? OR CAST(e.id AS TEXT)=?)`); p.push(`%${q.q}%`, `%${q.q}%`, `%${q.q}%`, q.q); }
  const limit = Math.min(Number(q.limit) || 500, 5000);
  return db.prepare(`SELECT e.*, c.name contact_name,
      (SELECT SUM(debit) FROM lines WHERE entry_id=e.id) amount,
      (SELECT COUNT(*) FROM attachments WHERE entry_id=e.id) attachments,
      (SELECT group_concat(a.name, ' / ') FROM lines l JOIN accounts a ON a.id=l.account_id WHERE l.entry_id=e.id) accounts
    FROM entries e LEFT JOIN contacts c ON c.id=e.contact_id WHERE ${where.join(' AND ')} ORDER BY e.date DESC, e.id DESC LIMIT ${limit}`).all(...p);
}));

app.get('/api/entries/:id', auth(), h(req => {
  const id = Number(req.params.id);
  const e = db.prepare(`SELECT e.*, c.name contact_name, u.name created_by_name FROM entries e LEFT JOIN contacts c ON c.id=e.contact_id
    LEFT JOIN users u ON u.id=e.created_by WHERE e.id=?`).get(id);
  if (!e) throw new L.UserError('Entry not found');
  e.lines = db.prepare('SELECT l.*, a.code, a.name account_name, a.type account_type FROM lines l JOIN accounts a ON a.id=l.account_id WHERE entry_id=? ORDER BY l.id').all(id);
  e.attachments = db.prepare('SELECT id, filename, mime, size, uploaded_at FROM attachments WHERE entry_id=?').all(id);
  e.payroll = db.prepare('SELECT * FROM payroll_items WHERE entry_id=?').get(id) || null;
  e.reversal = db.prepare('SELECT id FROM entries WHERE void_of=?').get(id) || null;
  const inv = db.prepare('SELECT id, number FROM invoices WHERE entry_id=?').get(id)
    || db.prepare('SELECT i.id, i.number FROM invoice_payments p JOIN invoices i ON i.id=p.invoice_id WHERE p.entry_id=?').get(id);
  e.invoice = inv || null;
  return e;
}));
app.post('/api/entries/:id/void', auth('owner'), h(req => ({ reversal: L.voidEntry(Number(req.params.id), req.user.id, req.body.reason) })));
app.patch('/api/entries/:id', auth(...WRITE), h(req => {
  // Only descriptive fields are editable; amounts/accounts require a void + re-entry.
  const e = db.prepare('SELECT * FROM entries WHERE id=?').get(Number(req.params.id));
  if (!e) throw new L.UserError('Not found');
  db.prepare('UPDATE entries SET memo=?, reference=? WHERE id=?').run(req.body.memo ?? e.memo, req.body.reference ?? e.reference, e.id);
  audit(req.user.id, 'entry.edit_memo', { id: e.id, before: { memo: e.memo, reference: e.reference }, after: req.body });
  return { ok: true };
}));

app.post('/api/entries/:id/attachments', auth(...WRITE), upload.array('files', 10), h(req => {
  const id = Number(req.params.id);
  if (!db.prepare('SELECT 1 FROM entries WHERE id=?').get(id)) throw new L.UserError('Entry not found');
  const ins = db.prepare('INSERT INTO attachments(entry_id,filename,stored,mime,size,uploaded_by) VALUES(?,?,?,?,?,?)');
  for (const f of req.files || []) ins.run(id, f.originalname, f.filename, f.mimetype, f.size, req.user.id);
  audit(req.user.id, 'attachment.add', { entry: id, files: (req.files || []).map(f => f.originalname) });
  return { ok: true, count: (req.files || []).length };
}));
app.get('/api/attachments/:id', auth(), (req, res) => {
  const a = db.prepare('SELECT * FROM attachments WHERE id=?').get(Number(req.params.id));
  if (!a) return res.status(404).end();
  const inline = /^(image\/|application\/pdf)/.test(a.mime || '');
  res.set('Content-Type', inline ? a.mime : 'application/octet-stream');
  res.set('Content-Disposition', `${inline ? 'inline' : 'attachment'}; filename="${a.filename.replace(/[^\w.\- ]/g, '_')}"`);
  res.sendFile(path.join(UPLOADS, path.basename(a.stored)));
});

// ---------- invoices ----------
app.get('/api/invoices', auth(), h(() => db.prepare(`SELECT i.*, c.name client_name FROM invoices i JOIN contacts c ON c.id=i.client_id ORDER BY i.date DESC, i.id DESC`).all()
  .map(i => ({ ...i, paid: L.invoicePaid(i.id) }))));
app.get('/api/invoices/next-number', auth(), h(() => ({ number: L.nextInvoiceNumber() })));
app.get('/api/invoices/:id', auth(), h(req => {
  const i = db.prepare(`SELECT i.*, c.name client_name, c.email client_email, c.address client_address FROM invoices i JOIN contacts c ON c.id=i.client_id WHERE i.id=?`).get(Number(req.params.id));
  if (!i) throw new L.UserError('Invoice not found');
  i.items = db.prepare('SELECT * FROM invoice_items WHERE invoice_id=?').all(i.id);
  i.payments = db.prepare('SELECT p.*, e.date, e.voided FROM invoice_payments p JOIN entries e ON e.id=p.entry_id WHERE p.invoice_id=? ORDER BY e.date').all(i.id);
  i.paid = L.invoicePaid(i.id);
  return i;
}));
app.post('/api/invoices', auth(...WRITE), h(req => ({ id: L.createInvoice(req.body, req.user.id) })));
app.post('/api/invoices/:id/payments', auth(...WRITE), h(req => ({ entry_id: L.payInvoice(Number(req.params.id), req.body, req.user.id) })));
app.post('/api/invoices/:id/void', auth('owner'), h(req => {
  const i = db.prepare('SELECT * FROM invoices WHERE id=?').get(Number(req.params.id));
  if (!i) throw new L.UserError('Invoice not found');
  return { reversal: L.voidEntry(i.entry_id, req.user.id, req.body.reason) };
}));

app.get('/invoice/:id/print', (req, res) => {
  if (!currentUser(req)) return res.redirect('/');
  const i = db.prepare(`SELECT i.*, c.name cname, c.email cemail, c.address caddr FROM invoices i JOIN contacts c ON c.id=i.client_id WHERE i.id=?`).get(Number(req.params.id));
  if (!i) return res.status(404).send('Not found');
  const items = db.prepare('SELECT * FROM invoice_items WHERE invoice_id=?').all(i.id);
  const paid = L.invoicePaid(i.id);
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const $ = c => '$' + (c / 100).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  const s = allSettings();
  res.send(`<!doctype html><html><head><meta charset="utf-8"><title>Invoice ${esc(i.number)}</title>
<style>body{font:14px/1.5 system-ui,sans-serif;max-width:780px;margin:40px auto;color:#111;padding:0 20px}h1{margin:0;font-size:28px}
table{width:100%;border-collapse:collapse;margin-top:24px}th,td{padding:8px;border-bottom:1px solid #ddd;text-align:left}td.r,th.r{text-align:right}
.top{display:flex;justify-content:space-between;gap:20px}.muted{color:#666}.tot td{border:none}.big{font-size:18px;font-weight:700}
${i.voided ? '.void{color:#b00;font-size:40px;font-weight:800}' : ''}@media print{.noprint{display:none}}</style></head><body>
<button class="noprint" onclick="print()">Print / Save as PDF</button>
<div class="top"><div><h1>${esc(s.company)}</h1><div class="muted" style="white-space:pre-line">${esc(s.address)}${s.ein ? '\nEIN ' + esc(s.ein) : ''}${s.email ? '\n' + esc(s.email) : ''}</div></div>
<div style="text-align:right"><h1>INVOICE</h1><div>${esc(i.number)}</div><div class="muted">Date: ${i.date}<br>Due: ${i.due_date}</div>${i.voided ? '<div class="void">VOID</div>' : ''}</div></div>
<p style="margin-top:28px"><b>Bill to</b><br>${esc(i.cname)}<br><span class="muted" style="white-space:pre-line">${esc(i.caddr)}${i.cemail ? '\n' + esc(i.cemail) : ''}</span></p>
<table><tr><th>Description</th><th class="r">Qty</th><th class="r">Rate</th><th class="r">Amount</th></tr>
${items.map(t => `<tr><td>${esc(t.description)}</td><td class="r">${t.qty}</td><td class="r">${$(t.unit_price)}</td><td class="r">${$(t.amount)}</td></tr>`).join('')}
<tr class="tot"><td></td><td></td><td class="r">Subtotal</td><td class="r">${$(i.subtotal)}</td></tr>
${i.tax ? `<tr class="tot"><td></td><td></td><td class="r">Sales tax (${i.tax_rate}%)</td><td class="r">${$(i.tax)}</td></tr>` : ''}
<tr class="tot"><td></td><td></td><td class="r big">Total</td><td class="r big">${$(i.total)}</td></tr>
${paid ? `<tr class="tot"><td></td><td></td><td class="r">Paid</td><td class="r">-${$(paid)}</td></tr><tr class="tot"><td></td><td></td><td class="r big">Balance due</td><td class="r big">${$(i.total - paid)}</td></tr>` : ''}
</table>${i.memo ? `<p class="muted" style="margin-top:24px;white-space:pre-line">${esc(i.memo)}</p>` : ''}</body></html>`);
});

// ---------- reconciliation ----------
app.get('/api/reconcile', auth(), h(req => {
  const acc = db.prepare('SELECT * FROM accounts WHERE id=? AND is_payment=1').get(Number(req.query.account_id));
  if (!acc) throw new L.UserError('Choose a bank, cash or card account');
  const to = req.query.to || new Date().toISOString().slice(0, 10);
  const lines = db.prepare(`SELECT l.id, l.debit, l.credit, l.cleared, e.id entry_id, e.date, e.kind, e.memo, c.name contact_name
    FROM lines l JOIN entries e ON e.id=l.entry_id LEFT JOIN contacts c ON c.id=e.contact_id
    WHERE l.account_id=? AND e.date<=? AND (l.cleared=0 OR e.date >= date(?, '-45 days')) ORDER BY e.date, e.id`).all(acc.id, to, to);
  const cleared = db.prepare(`SELECT COALESCE(SUM(l.debit-l.credit),0) s FROM lines l JOIN entries e ON e.id=l.entry_id WHERE l.account_id=? AND l.cleared=1 AND e.date<=?`).get(acc.id, to).s;
  const book = db.prepare(`SELECT COALESCE(SUM(l.debit-l.credit),0) s FROM lines l JOIN entries e ON e.id=l.entry_id WHERE l.account_id=? AND e.date<=?`).get(acc.id, to).s;
  const sign = acc.type === 'asset' ? 1 : -1;
  const last = db.prepare('SELECT * FROM reconciliations WHERE account_id=? ORDER BY statement_date DESC LIMIT 1').get(acc.id);
  return { account: acc, lines, cleared: cleared * sign, book: book * sign, sign, last };
}));
app.patch('/api/lines/:id/cleared', auth(...WRITE), h(req => {
  db.prepare('UPDATE lines SET cleared=? WHERE id=?').run(req.body.cleared ? 1 : 0, Number(req.params.id));
  return { ok: true };
}));
app.post('/api/reconciliations', auth(...WRITE), h(req => {
  const b = req.body;
  const acc = db.prepare('SELECT * FROM accounts WHERE id=? AND is_payment=1').get(Number(b.account_id));
  if (!acc || !L.isDate(b.statement_date)) throw new L.UserError('Account and statement date are required');
  const sign = acc.type === 'asset' ? 1 : -1;
  const cleared = sign * db.prepare(`SELECT COALESCE(SUM(l.debit-l.credit),0) s FROM lines l JOIN entries e ON e.id=l.entry_id WHERE l.account_id=? AND l.cleared=1 AND e.date<=?`).get(acc.id, b.statement_date).s;
  const stmt = L.cents(b.statement_balance);
  if (cleared !== stmt && !b.force) throw new L.UserError(`Cleared balance ($${(cleared / 100).toFixed(2)}) does not match the statement ($${(stmt / 100).toFixed(2)}). Find the difference first.`);
  db.prepare('INSERT INTO reconciliations(account_id,statement_date,statement_balance,cleared_balance,user_id) VALUES(?,?,?,?,?)').run(acc.id, b.statement_date, stmt, cleared, req.user.id);
  audit(req.user.id, 'reconcile', { account: acc.name, date: b.statement_date, statement: stmt, cleared });
  return { ok: true };
}));

// ---------- bank import ----------
app.post('/api/import', auth(...WRITE), h(req => L.importRows(Number(req.body.account_id), req.body.rows || [], req.user.id)));

// ---------- dashboard ----------
app.get('/api/dashboard', auth(), h(() => {
  const today = new Date().toISOString().slice(0, 10);
  const fy = reports.fiscalYearStart(today);
  const month = today.slice(0, 8) + '01';
  const s = reports.sums(null, today);
  const accs = db.prepare('SELECT * FROM accounts WHERE is_payment=1 AND active=1 ORDER BY code').all()
    .map(a => ({ id: a.id, name: a.name, type: a.type, balance: a.type === 'asset' ? (s.get(a.id) || { net: 0 }).net : -(s.get(a.id) || { net: 0 }).net }));
  const pl = (f, t) => {
    const x = reports.sums(f, t);
    let inc = 0, exp = 0;
    for (const a of db.prepare(`SELECT id,type FROM accounts WHERE type IN ('income','expense')`).all()) {
      const v = x.get(a.id); if (!v) continue;
      if (a.type === 'income') inc -= v.net; else exp += v.net;
    }
    return { income: inc, expenses: exp, net: inc - exp };
  };
  const months = [];
  const d = new Date(today.slice(0, 7) + '-01T00:00:00Z');
  for (let i = 11; i >= 0; i--) {
    const a = new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth() - i, 1));
    const b = new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth() - i + 1, 0));
    months.push({ month: a.toISOString().slice(0, 7), ...pl(a.toISOString().slice(0, 10), b.toISOString().slice(0, 10)) });
  }
  const ar = db.prepare('SELECT * FROM invoices WHERE voided=0').all().reduce((t, i) => t + (i.total - L.invoicePaid(i.id)), 0);
  const overdue = db.prepare('SELECT * FROM invoices WHERE voided=0 AND due_date < ?').all(today).reduce((t, i) => t + (i.total - L.invoicePaid(i.id)), 0);
  const owners = reports.run('owner_equity', { from: '1900-01-01', to: today }).rows.filter(r => !r.style).map(r => ({ name: r.cells[0], share: r.cells[1], net: r.cells[5] }));
  const payrollLiab = db.prepare(`SELECT id FROM accounts WHERE subtype IN ('payroll_liability','sales_tax')`).all().reduce((t, a) => t - ((s.get(a.id) || { net: 0 }).net), 0);
  const missing = reports.run('missing_receipts', { from: fy, to: today }).rows.length;
  const recent = db.prepare(`SELECT e.id,e.date,e.kind,e.memo,e.voided,c.name contact_name,(SELECT SUM(debit) FROM lines WHERE entry_id=e.id) amount FROM entries e LEFT JOIN contacts c ON c.id=e.contact_id ORDER BY e.id DESC LIMIT 10`).all();
  return { today, fy, accounts: accs, ytd: pl(fy, today), mtd: pl(month, today), months, ar, overdue, owners, taxes_owed: payrollLiab, missing_receipts: missing, recent };
}));

// ---------- reports & exports ----------
app.get('/api/reports', auth(), h(() => reports.CATALOG.map(([id, title, desc]) => ({ id, title, desc }))));
app.get('/api/reports/:name', auth(), h((req, res) => {
  const rep = reports.run(req.params.name, req.query);
  if (!rep) throw new L.UserError('Unknown report');
  if (req.query.format === 'csv') {
    res.set('Content-Type', 'text/csv; charset=utf-8');
    res.set('Content-Disposition', `attachment; filename="${req.params.name}_${req.query.to || 'latest'}.csv"`);
    res.send('﻿' + reports.toCSV(rep));
    return;
  }
  return rep;
}));

app.get('/api/export/package', auth('owner', 'accountant'), (req, res) => {
  try {
    const { from, to } = reports.range(req.query);
    const s = allSettings();
    const zip = new yazl.ZipFile();
    const name = `${(s.company || 'books').replace(/[^\w]+/g, '_')}_accountant_package_${from}_to_${to}`;
    const order = ['pnl', 'balance_sheet', 'cash_flow', 'trial_balance', 'tax_categories', 'owner_equity', 'owner_activity', 'payroll_summary', 'contractors_1099',
      'income_by_client', 'expenses_by_vendor', 'ar_aging', 'sales_tax', 'general_ledger', 'journal', 'missing_receipts', 'reconciliations', 'chart_of_accounts', 'audit_log'];
    order.forEach((r, i) => zip.addBuffer(Buffer.from('﻿' + reports.toCSV(reports.run(r, { from, to }))), `${name}/${String(i + 1).padStart(2, '0')}_${r}.csv`));
    // raw data tables
    const csv = rows => {
      if (!rows.length) return '';
      const keys = Object.keys(rows[0]);
      const esc = v => v == null ? '' : /[",\n]/.test(String(v)) ? `"${String(v).replace(/"/g, '""')}"` : String(v);
      return '﻿' + [keys.join(','), ...rows.map(r => keys.map(k => esc(r[k])).join(','))].join('\r\n');
    };
    zip.addBuffer(Buffer.from(csv(db.prepare(`SELECT id,type,name,email,phone,address,tax_id,is_1099,profit_share FROM contacts ORDER BY type,name`).all())), `${name}/data_contacts.csv`);
    zip.addBuffer(Buffer.from(csv(db.prepare(`SELECT i.number,i.date,i.due_date,c.name client,i.subtotal/100.0 subtotal,i.tax_rate,i.tax/100.0 tax,i.total/100.0 total,i.voided FROM invoices i JOIN contacts c ON c.id=i.client_id WHERE i.date BETWEEN ? AND ? ORDER BY i.date`).all(from, to))), `${name}/data_invoices.csv`);
    const atts = db.prepare(`SELECT a.*, e.date, e.memo, e.kind FROM attachments a JOIN entries e ON e.id=a.entry_id WHERE e.date BETWEEN ? AND ? ORDER BY e.date, e.id`).all(from, to);
    const idx = [];
    for (const a of atts) {
      const fn = `receipts/${a.date}_entry${a.entry_id}_${a.id}_${a.filename.replace(/[^\w.\-]+/g, '_')}`;
      const p = path.join(UPLOADS, path.basename(a.stored));
      if (fs.existsSync(p)) zip.addFile(p, `${name}/${fn}`);
      idx.push({ entry: a.entry_id, date: a.date, type: a.kind, memo: a.memo, file: fn });
    }
    zip.addBuffer(Buffer.from(csv(idx)), `${name}/receipts_index.csv`);
    const readme = `${s.company} — Accountant package
Period: ${from} to ${to}
Entity: ${s.entity_type || ''}   EIN: ${s.ein || ''}
Address: ${(s.address || '').replace(/\n/g, ', ')}
Fiscal year starts in month: ${s.fiscal_start_month}   Books locked through: ${s.lock_date || '(not locked)'}
Generated: ${new Date().toISOString()} by ${currentUser(req).name}

Basis: accrual (invoices are income when issued; payments clear Accounts Receivable).
All amounts in USD. Double-entry; the trial balance must show debits = credits.
Owner deposits are recorded as OWNER CAPITAL (equity), per owner — not income, not loans.
Owner withdrawals are recorded as OWNER DRAWS, per owner.
Voided transactions are kept and reversed with an offsetting entry (see journal / audit log).
Every receipt/bill attached in the app is in /receipts and listed in receipts_index.csv by entry number.

Files:
${order.map((r, i) => `  ${String(i + 1).padStart(2, '0')}_${r}.csv`).join('\n')}
  data_contacts.csv, data_invoices.csv, receipts_index.csv, receipts/
`;
    zip.addBuffer(Buffer.from(readme), `${name}/README.txt`);
    zip.end();
    audit(currentUser(req).id, 'export.package', { from, to });
    res.set('Content-Type', 'application/zip');
    res.set('Content-Disposition', `attachment; filename="${name}.zip"`);
    zip.outputStream.pipe(res);
  } catch (e) {
    console.error(e);
    res.status(500).json({ error: e.message });
  }
});

app.get('/api/export/backup', auth('owner'), async (req, res) => {
  const f = path.join(DATA_DIR, `backup-${Date.now()}.db`);
  await db.backup(f);
  audit(req.user.id, 'export.backup');
  res.download(f, `books-backup-${new Date().toISOString().slice(0, 10)}.db`, () => fs.unlink(f, () => {}));
});

app.use('/api', (req, res) => res.status(404).json({ error: 'Not found' }));
app.get('*', (req, res) => res.sendFile(path.join(__dirname, 'public', 'index.html')));

const PORT = Number(process.env.PORT) || 3000;
if (require.main === module) app.listen(PORT, () => console.log(`Zsi Books running at http://localhost:${PORT}`));
module.exports = app;
