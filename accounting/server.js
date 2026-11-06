// Zsi Books – HTTP server and JSON API. Runs locally (`npm start`) or on Vercel (api/index.js).
const express = require('express');
const crypto = require('crypto');
const path = require('path');
const fs = require('fs');
const multer = require('multer');
const yazl = require('yazl');
const { db, DATA_DIR, ON_VERCEL, NotConfigured, getSetting, setSetting, createOwnerAccounts, audit } = require('./db');
const L = require('./ledger');
const reports = require('./reports');

const app = express();
app.disable('x-powered-by');
if (ON_VERCEL) app.set('trust proxy', true);
app.use(express.json({ limit: '4mb' }));
app.use((req, res, next) => {
  res.set('X-Content-Type-Options', 'nosniff');
  res.set('X-Frame-Options', 'DENY');
  res.set('Referrer-Policy', 'same-origin');
  next();
});
app.use(express.static(path.join(__dirname, 'public')));

// ---------- receipt storage: Vercel Blob (private) online, ./data/uploads locally ----------
const USE_BLOB = !!process.env.BLOB_READ_WRITE_TOKEN;
const UPLOADS = path.join(DATA_DIR, 'uploads');
const upload = multer({ storage: multer.memoryStorage(), limits: { fileSize: ON_VERCEL ? 4 * 1024 * 1024 : 20 * 1024 * 1024, files: 10 } });

async function saveFile(f) {
  const name = crypto.randomBytes(16).toString('hex') + path.extname(f.originalname).toLowerCase().replace(/[^.a-z0-9]/g, '');
  if (USE_BLOB) {
    const { put } = require('@vercel/blob');
    const r = await put(`receipts/${name}`, f.buffer, { access: 'private', contentType: f.mimetype, addRandomSuffix: false });
    return { stored: r.pathname, storage: 'blob' };
  }
  if (ON_VERCEL) throw new L.UserError('Receipt storage is not connected. In Vercel: Storage → Create → Blob (private) → connect to this project.');
  fs.mkdirSync(UPLOADS, { recursive: true });
  fs.writeFileSync(path.join(UPLOADS, name), f.buffer);
  return { stored: name, storage: 'disk' };
}
async function readFile(a) {
  if (a.storage === 'blob') {
    const { get } = require('@vercel/blob');
    const r = await get(a.stored, { access: 'private' });
    if (!r || !r.stream) return null;
    return Buffer.from(await new Response(r.stream).arrayBuffer());
  }
  const p = path.join(UPLOADS, path.basename(a.stored));
  return fs.existsSync(p) ? fs.readFileSync(p) : null;
}

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
const SECURE = ON_VERCEL || process.env.COOKIE_SECURE === '1';
const setSession = (res, token) => res.set('Set-Cookie', `sid=${token}; HttpOnly; Path=/; SameSite=Lax; Max-Age=${60 * 60 * 24 * 30}${SECURE ? '; Secure' : ''}`);
const lower = s => String(s || '').trim().toLowerCase();

async function currentUser(req) {
  const t = cookie(req).sid;
  if (!t) return null;
  return (await db.get(`SELECT u.id,u.name,u.email,u.role FROM sessions s JOIN users u ON u.id=s.user_id
    WHERE s.token=? AND u.active=1 AND s.created_at > to_char(now() AT TIME ZONE 'UTC' - interval '30 days', 'YYYY-MM-DD HH24:MI:SS')`, t)) || null;
}
const auth = (...roles) => async (req, res, next) => {
  try {
    const u = await currentUser(req);
    if (!u) return res.status(401).json({ error: 'Please sign in' });
    if (roles.length && !roles.includes(u.role)) return res.status(403).json({ error: 'Your role does not allow this action' });
    req.user = u;
    next();
  } catch (e) { fail(res, e); }
};
const WRITE = ['owner', 'staff'];

// Login throttling, kept in the database so it works across serverless instances.
async function tooManyAttempts(key) {
  const ago = m => `to_char(now() AT TIME ZONE 'UTC' - interval '${m}', 'YYYY-MM-DD HH24:MI:SS')`;
  await db.run(`DELETE FROM login_attempts WHERE at < ${ago('1 day')}`);
  await db.run('INSERT INTO login_attempts(key) VALUES(?)', key);
  const r = await db.get(`SELECT COUNT(*) c FROM login_attempts WHERE key=? AND at > ${ago('15 minutes')}`, key);
  return r.c > 10;
}

function fail(res, e) {
  if (res.headersSent) return;
  if (e instanceof NotConfigured) return res.status(503).json({ error: e.message, not_configured: true });
  if (e instanceof L.UserError || /unique|duplicate key|violates check/i.test(e.message)) return res.status(400).json({ error: e.message });
  if (e && e.code === 'LIMIT_FILE_SIZE') return res.status(400).json({ error: 'File too large (max 4 MB online). Take a smaller photo or compress the PDF.' });
  console.error(e);
  res.status(500).json({ error: 'Something went wrong: ' + e.message });
}
const h = fn => async (req, res) => {
  try {
    const out = await fn(req, res);
    if (out !== undefined && !res.headersSent) res.json(out);
  } catch (e) { fail(res, e); }
};

const isSetup = async () => !!(await db.get('SELECT 1 x FROM users LIMIT 1'));
const allSettings = async () => Object.fromEntries((await db.all('SELECT key,value FROM settings')).map(r => [r.key, r.value]));

app.get('/api/state', h(async req => {
  const setup = await isSetup();
  return { setup, user: await currentUser(req), settings: setup ? await allSettings() : {}, storage: USE_BLOB ? 'blob' : (ON_VERCEL ? 'missing' : 'disk') };
}));

app.post('/api/setup', h(async req => {
  const b = req.body;
  if (!b.company || !b.name || !b.email || !b.password) throw new L.UserError('Fill in company, your name, email and password');
  if (String(b.password).length < 8) throw new L.UserError('Password must be at least 8 characters');
  const owners = (b.owners || []).map(o => ({ name: String(o.name || '').trim(), share: Number(o.share || 0) })).filter(o => o.name);
  if (!owners.length) throw new L.UserError('Add at least one owner');
  await db.tx(async () => {
    await db.run('LOCK TABLE users IN EXCLUSIVE MODE');
    if (await isSetup()) throw new L.UserError('Already set up');
    const defaults = { company: b.company, ein: b.ein || '', address: b.address || '', entity_type: b.entity_type || 'Multi-member LLC (taxed as partnership)',
      fiscal_start_month: b.fiscal_start_month || '1', invoice_prefix: 'INV-', invoice_next: '1001', threshold_1099: '2000', sales_tax_rate: '0', lock_date: '' };
    for (const [k, v] of Object.entries(defaults)) await setSetting(k, v);
    const uid = await db.insert('INSERT INTO users(name,email,pass_hash,role) VALUES(?,?,?,?)', b.name, lower(b.email), hash(b.password), 'owner');
    for (const o of owners) {
      const id = await db.insert(`INSERT INTO contacts(type,name,profit_share) VALUES('owner',?,?)`, o.name, o.share);
      await createOwnerAccounts({ id, name: o.name });
    }
    if (b.bank_name) await db.run(`UPDATE accounts SET name=? WHERE code='1000'`, b.bank_name);
    await audit(uid, 'setup', { company: b.company });
  });
  return { ok: true };
}));

app.post('/api/login', h(async (req, res) => {
  if (await tooManyAttempts(`ip:${req.ip}`)) return res.status(429).json({ error: 'Too many attempts. Try again in 15 minutes.' });
  const u = await db.get('SELECT * FROM users WHERE email=? AND active=1', lower(req.body.email));
  if (!u || !verify(String(req.body.password || ''), u.pass_hash)) throw new L.UserError('Wrong email or password');
  const token = crypto.randomBytes(32).toString('hex');
  await db.run('INSERT INTO sessions(token,user_id) VALUES(?,?)', token, u.id);
  setSession(res, token);
  await audit(u.id, 'login');
  return { ok: true };
}));
app.post('/api/logout', h(async (req, res) => {
  await db.run('DELETE FROM sessions WHERE token=?', cookie(req).sid || '');
  res.set('Set-Cookie', `sid=; Path=/; Max-Age=0${SECURE ? '; Secure' : ''}`);
  return { ok: true };
}));

// ---------- settings & users ----------
const SETTING_KEYS = ['company', 'ein', 'address', 'entity_type', 'fiscal_start_month', 'invoice_prefix', 'invoice_next', 'threshold_1099', 'sales_tax_rate', 'lock_date', 'nys_sales_tax_id', 'phone', 'email'];
app.put('/api/settings', auth('owner'), h(async req => {
  for (const k of SETTING_KEYS) if (k in req.body) {
    if (k === 'lock_date' && req.body[k] && !L.isDate(req.body[k])) throw new L.UserError('Lock date must be a date');
    await setSetting(k, req.body[k]);
  }
  await audit(req.user.id, 'settings.update', req.body);
  return allSettings();
}));

app.get('/api/users', auth('owner'), h(() => db.all('SELECT id,name,email,role,active,created_at FROM users ORDER BY id')));
app.post('/api/users', auth('owner'), h(async req => {
  const { name, email, password, role } = req.body;
  if (!name || !email || !password || password.length < 8) throw new L.UserError('Name, email and an 8+ character password are required');
  const id = await db.insert('INSERT INTO users(name,email,pass_hash,role) VALUES(?,?,?,?)', name, lower(email), hash(password), role || 'staff');
  await audit(req.user.id, 'user.create', { email, role });
  return { id };
}));
app.patch('/api/users/:id', auth('owner'), h(async req => {
  const id = Number(req.params.id);
  const b = req.body;
  if (b.password) {
    if (b.password.length < 8) throw new L.UserError('Password must be 8+ characters');
    await db.run('UPDATE users SET pass_hash=? WHERE id=?', hash(b.password), id);
    await db.run('DELETE FROM sessions WHERE user_id=?', id);
  }
  if (b.role) await db.run('UPDATE users SET role=? WHERE id=?', b.role, id);
  if ('active' in b) {
    if (id === req.user.id && !b.active) throw new L.UserError('You cannot deactivate yourself');
    await db.run('UPDATE users SET active=? WHERE id=?', b.active ? 1 : 0, id);
    if (!b.active) await db.run('DELETE FROM sessions WHERE user_id=?', id);
  }
  await audit(req.user.id, 'user.update', { id, role: b.role, active: b.active, password: b.password ? 'changed' : undefined });
  return { ok: true };
}));
app.post('/api/me/password', auth(), h(async req => {
  const u = await db.get('SELECT * FROM users WHERE id=?', req.user.id);
  if (!verify(String(req.body.current || ''), u.pass_hash)) throw new L.UserError('Current password is wrong');
  if (String(req.body.password || '').length < 8) throw new L.UserError('New password must be 8+ characters');
  await db.run('UPDATE users SET pass_hash=? WHERE id=?', hash(req.body.password), u.id);
  await audit(u.id, 'password.change');
  return { ok: true };
}));

// ---------- accounts ----------
app.get('/api/accounts', auth(), h(async () => {
  const s = await reports.sums(null, '9999-12-31');
  return (await db.all('SELECT * FROM accounts ORDER BY code')).map(a => {
    const v = s.get(a.id);
    const bal = v ? (['liability', 'equity', 'income'].includes(a.type) ? -v.net : v.net) : 0;
    return { ...a, balance: bal };
  });
}));
app.post('/api/accounts', auth('owner'), h(async req => {
  const { code, name, type, subtype, tax_category, is_payment, description } = req.body;
  if (!code || !name || !type) throw new L.UserError('Code, name and type are required');
  const id = await db.insert('INSERT INTO accounts(code,name,type,subtype,tax_category,is_payment,description) VALUES(?,?,?,?,?,?,?)',
    code, name, type, subtype || (is_payment ? (type === 'asset' ? 'bank' : 'card') : null), tax_category || null, is_payment ? 1 : 0, description || null);
  await audit(req.user.id, 'account.create', req.body);
  return { id };
}));
app.patch('/api/accounts/:id', auth('owner'), h(async req => {
  const a = await db.get('SELECT * FROM accounts WHERE id=?', Number(req.params.id));
  if (!a) throw new L.UserError('Not found');
  const b = { ...a, ...req.body };
  await db.run('UPDATE accounts SET name=?, tax_category=?, active=?, description=? WHERE id=?', b.name, b.tax_category || null, b.active ? 1 : 0, b.description || null, a.id);
  await audit(req.user.id, 'account.update', { id: a.id, ...req.body });
  return { ok: true };
}));

// ---------- contacts ----------
app.get('/api/contacts', auth(), h(req => {
  const t = req.query.type;
  return t ? db.all('SELECT * FROM contacts WHERE type=? ORDER BY type, name', t) : db.all('SELECT * FROM contacts ORDER BY type, name');
}));
app.post('/api/contacts', auth(...WRITE), h(async req => {
  const b = req.body;
  if (!b.name || !b.type) throw new L.UserError('Name and type are required');
  return db.tx(async () => {
    const id = await db.insert('INSERT INTO contacts(type,name,email,phone,address,tax_id,is_1099,profit_share,notes) VALUES(?,?,?,?,?,?,?,?,?)',
      b.type, b.name.trim(), b.email || null, b.phone || null, b.address || null, b.tax_id || null, b.is_1099 ? 1 : 0, b.type === 'owner' ? Number(b.profit_share || 0) : null, b.notes || null);
    if (b.type === 'owner') await createOwnerAccounts({ id, name: b.name.trim() });
    await audit(req.user.id, 'contact.create', { id, type: b.type, name: b.name });
    return { id };
  });
}));
app.patch('/api/contacts/:id', auth(...WRITE), h(async req => {
  const c = await db.get('SELECT * FROM contacts WHERE id=?', Number(req.params.id));
  if (!c) throw new L.UserError('Not found');
  const b = { ...c, ...req.body };
  await db.run('UPDATE contacts SET name=?,email=?,phone=?,address=?,tax_id=?,is_1099=?,profit_share=?,notes=?,active=? WHERE id=?',
    b.name, b.email, b.phone, b.address, b.tax_id, b.is_1099 ? 1 : 0, c.type === 'owner' ? Number(b.profit_share || 0) : null, b.notes, b.active ? 1 : 0, c.id);
  if (c.type === 'owner' && b.name !== c.name) {
    await db.run(`UPDATE accounts SET name=? WHERE owner_contact_id=? AND subtype='capital'`, `Owner Capital – ${b.name}`, c.id);
    await db.run(`UPDATE accounts SET name=? WHERE owner_contact_id=? AND subtype='draws'`, `Owner Draws – ${b.name}`, c.id);
  }
  await audit(req.user.id, 'contact.update', { id: c.id, ...req.body });
  return { ok: true };
}));

// ---------- transactions ----------
app.post('/api/tx/:type', auth(...WRITE), h(async req => ({ id: await L.record(req.params.type, req.body, req.user.id) })));

app.get('/api/entries', auth(), h(req => {
  const q = req.query;
  const where = ['1=1'], p = [];
  if (q.from) { where.push('e.date >= ?'); p.push(q.from); }
  if (q.to) { where.push('e.date <= ?'); p.push(q.to); }
  if (q.kind) { where.push('e.kind = ?'); p.push(q.kind); }
  if (q.contact_id) { where.push('e.contact_id = ?'); p.push(Number(q.contact_id)); }
  if (q.account_id) { where.push('EXISTS (SELECT 1 FROM lines x WHERE x.entry_id=e.id AND x.account_id=?)'); p.push(Number(q.account_id)); }
  if (q.q) { where.push(`(e.memo ILIKE ? OR e.reference ILIKE ? OR c.name ILIKE ? OR CAST(e.id AS TEXT)=?)`); p.push(`%${q.q}%`, `%${q.q}%`, `%${q.q}%`, q.q); }
  const limit = Math.min(Number(q.limit) || 500, 5000);
  return db.all(`SELECT e.*, c.name contact_name,
      (SELECT SUM(debit) FROM lines WHERE entry_id=e.id) amount,
      (SELECT COUNT(*) FROM attachments WHERE entry_id=e.id) attachments,
      (SELECT string_agg(a.name, ' / ') FROM lines l JOIN accounts a ON a.id=l.account_id WHERE l.entry_id=e.id) accounts
    FROM entries e LEFT JOIN contacts c ON c.id=e.contact_id WHERE ${where.join(' AND ')} ORDER BY e.date DESC, e.id DESC LIMIT ${limit}`, ...p);
}));

app.get('/api/entries/:id', auth(), h(async req => {
  const id = Number(req.params.id);
  const e = await db.get(`SELECT e.*, c.name contact_name, u.name created_by_name FROM entries e LEFT JOIN contacts c ON c.id=e.contact_id
    LEFT JOIN users u ON u.id=e.created_by WHERE e.id=?`, id);
  if (!e) throw new L.UserError('Entry not found');
  e.lines = await db.all('SELECT l.*, a.code, a.name account_name, a.type account_type FROM lines l JOIN accounts a ON a.id=l.account_id WHERE entry_id=? ORDER BY l.id', id);
  e.attachments = await db.all('SELECT id, filename, mime, size, uploaded_at FROM attachments WHERE entry_id=? ORDER BY id', id);
  e.payroll = (await db.get('SELECT * FROM payroll_items WHERE entry_id=?', id)) || null;
  e.reversal = (await db.get('SELECT id FROM entries WHERE void_of=?', id)) || null;
  e.invoice = (await db.get('SELECT id, number FROM invoices WHERE entry_id=?', id))
    || (await db.get('SELECT i.id, i.number FROM invoice_payments p JOIN invoices i ON i.id=p.invoice_id WHERE p.entry_id=?', id)) || null;
  return e;
}));
app.post('/api/entries/:id/void', auth('owner'), h(async req => ({ reversal: await L.voidEntry(Number(req.params.id), req.user.id, req.body.reason) })));
app.patch('/api/entries/:id', auth(...WRITE), h(async req => {
  // Only descriptive fields are editable; amounts/accounts require a void + re-entry.
  const e = await db.get('SELECT * FROM entries WHERE id=?', Number(req.params.id));
  if (!e) throw new L.UserError('Not found');
  await db.run('UPDATE entries SET memo=?, reference=? WHERE id=?', req.body.memo ?? e.memo, req.body.reference ?? e.reference, e.id);
  await audit(req.user.id, 'entry.edit_memo', { id: e.id, before: { memo: e.memo, reference: e.reference }, after: req.body });
  return { ok: true };
}));

app.post('/api/entries/:id/attachments', auth(...WRITE), (req, res, next) => upload.array('files', 10)(req, res, err => err ? fail(res, err) : next()), h(async req => {
  const id = Number(req.params.id);
  if (!(await db.get('SELECT 1 x FROM entries WHERE id=?', id))) throw new L.UserError('Entry not found');
  for (const f of req.files || []) {
    const s = await saveFile(f);
    await db.run('INSERT INTO attachments(entry_id,filename,stored,storage,mime,size,uploaded_by) VALUES(?,?,?,?,?,?,?)', id, f.originalname, s.stored, s.storage, f.mimetype, f.size, req.user.id);
  }
  await audit(req.user.id, 'attachment.add', { entry: id, files: (req.files || []).map(f => f.originalname) });
  return { ok: true, count: (req.files || []).length };
}));
app.get('/api/attachments/:id', auth(), h(async (req, res) => {
  const a = await db.get('SELECT * FROM attachments WHERE id=?', Number(req.params.id));
  const buf = a && await readFile(a);
  if (!buf) return res.status(404).json({ error: 'File not found' });
  const inline = /^(image\/(png|jpeg|gif|webp)|application\/pdf)$/.test(a.mime || '');
  res.set('Content-Type', inline ? a.mime : 'application/octet-stream');
  res.set('Content-Disposition', `${inline ? 'inline' : 'attachment'}; filename="${a.filename.replace(/[^\w.\- ]/g, '_')}"`);
  res.set('Cache-Control', 'private, max-age=3600');
  res.send(buf);
}));

// ---------- invoices ----------
app.get('/api/invoices', auth(), h(() => db.all(`SELECT i.*, c.name client_name,
    (SELECT COALESCE(SUM(p.amount),0) FROM invoice_payments p JOIN entries e ON e.id=p.entry_id WHERE p.invoice_id=i.id AND e.voided=0) paid
  FROM invoices i JOIN contacts c ON c.id=i.client_id ORDER BY i.date DESC, i.id DESC`)));
app.get('/api/invoices/next-number', auth(), h(async () => ({ number: await L.nextInvoiceNumber() })));
app.get('/api/invoices/:id', auth(), h(async req => {
  const i = await db.get(`SELECT i.*, c.name client_name, c.email client_email, c.address client_address FROM invoices i JOIN contacts c ON c.id=i.client_id WHERE i.id=?`, Number(req.params.id));
  if (!i) throw new L.UserError('Invoice not found');
  i.items = await db.all('SELECT * FROM invoice_items WHERE invoice_id=? ORDER BY id', i.id);
  i.payments = await db.all('SELECT p.*, e.date, e.voided FROM invoice_payments p JOIN entries e ON e.id=p.entry_id WHERE p.invoice_id=? ORDER BY e.date', i.id);
  i.paid = await L.invoicePaid(i.id);
  return i;
}));
app.post('/api/invoices', auth(...WRITE), h(async req => ({ id: await L.createInvoice(req.body, req.user.id) })));
app.post('/api/invoices/:id/payments', auth(...WRITE), h(async req => ({ entry_id: await L.payInvoice(Number(req.params.id), req.body, req.user.id) })));
app.post('/api/invoices/:id/void', auth('owner'), h(async req => {
  const i = await db.get('SELECT * FROM invoices WHERE id=?', Number(req.params.id));
  if (!i) throw new L.UserError('Invoice not found');
  return { reversal: await L.voidEntry(i.entry_id, req.user.id, req.body.reason) };
}));

app.get('/invoice/:id/print', h(async (req, res) => {
  if (!(await currentUser(req))) return res.redirect('/');
  const i = await db.get(`SELECT i.*, c.name cname, c.email cemail, c.address caddr FROM invoices i JOIN contacts c ON c.id=i.client_id WHERE i.id=?`, Number(req.params.id));
  if (!i) return res.status(404).send('Not found');
  const items = await db.all('SELECT * FROM invoice_items WHERE invoice_id=? ORDER BY id', i.id);
  const paid = await L.invoicePaid(i.id);
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const $ = c => '$' + (c / 100).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  const s = await allSettings();
  res.send(`<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Invoice ${esc(i.number)}</title>
<style>body{font:14px/1.5 system-ui,sans-serif;max-width:780px;margin:40px auto;color:#111;padding:0 20px}h1{margin:0;font-size:28px}
table{width:100%;border-collapse:collapse;margin-top:24px}th,td{padding:8px;border-bottom:1px solid #ddd;text-align:left}td.r,th.r{text-align:right}
.top{display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap}.muted{color:#666}.tot td{border:none}.big{font-size:18px;font-weight:700}
.void{color:#b00;font-size:40px;font-weight:800}@media print{.noprint{display:none}}</style></head><body>
<button class="noprint" onclick="print()">Print / Save as PDF</button>
<div class="top"><div><h1>${esc(s.company)}</h1><div class="muted" style="white-space:pre-line">${esc(s.address)}${s.ein ? '\nEIN ' + esc(s.ein) : ''}${s.email ? '\n' + esc(s.email) : ''}</div></div>
<div style="text-align:right"><h1>INVOICE</h1><div>${esc(i.number)}</div><div class="muted">Date: ${esc(i.date)}<br>Due: ${esc(i.due_date)}</div>${i.voided ? '<div class="void">VOID</div>' : ''}</div></div>
<p style="margin-top:28px"><b>Bill to</b><br>${esc(i.cname)}<br><span class="muted" style="white-space:pre-line">${esc(i.caddr)}${i.cemail ? '\n' + esc(i.cemail) : ''}</span></p>
<table><tr><th>Description</th><th class="r">Qty</th><th class="r">Rate</th><th class="r">Amount</th></tr>
${items.map(t => `<tr><td>${esc(t.description)}</td><td class="r">${t.qty}</td><td class="r">${$(t.unit_price)}</td><td class="r">${$(t.amount)}</td></tr>`).join('')}
<tr class="tot"><td></td><td></td><td class="r">Subtotal</td><td class="r">${$(i.subtotal)}</td></tr>
${i.tax ? `<tr class="tot"><td></td><td></td><td class="r">Sales tax (${i.tax_rate}%)</td><td class="r">${$(i.tax)}</td></tr>` : ''}
<tr class="tot"><td></td><td></td><td class="r big">Total</td><td class="r big">${$(i.total)}</td></tr>
${paid ? `<tr class="tot"><td></td><td></td><td class="r">Paid</td><td class="r">-${$(paid)}</td></tr><tr class="tot"><td></td><td></td><td class="r big">Balance due</td><td class="r big">${$(i.total - paid)}</td></tr>` : ''}
</table>${i.memo ? `<p class="muted" style="margin-top:24px;white-space:pre-line">${esc(i.memo)}</p>` : ''}</body></html>`);
}));

// ---------- reconciliation ----------
app.get('/api/reconcile', auth(), h(async req => {
  const acc = await db.get('SELECT * FROM accounts WHERE id=? AND is_payment=1', Number(req.query.account_id) || 0);
  if (!acc) throw new L.UserError('Choose a bank, cash or card account');
  const to = L.isDate(req.query.to) ? req.query.to : new Date().toISOString().slice(0, 10);
  const lines = await db.all(`SELECT l.id, l.debit, l.credit, l.cleared, e.id entry_id, e.date, e.kind, e.memo, c.name contact_name
    FROM lines l JOIN entries e ON e.id=l.entry_id LEFT JOIN contacts c ON c.id=e.contact_id
    WHERE l.account_id=? AND e.date<=? AND (l.cleared=0 OR e.date >= to_char(CAST(? AS date) - 45, 'YYYY-MM-DD')) ORDER BY e.date, e.id`, acc.id, to, to);
  const cleared = (await db.get(`SELECT COALESCE(SUM(l.debit-l.credit),0) s FROM lines l JOIN entries e ON e.id=l.entry_id WHERE l.account_id=? AND l.cleared=1 AND e.date<=?`, acc.id, to)).s;
  const book = (await db.get(`SELECT COALESCE(SUM(l.debit-l.credit),0) s FROM lines l JOIN entries e ON e.id=l.entry_id WHERE l.account_id=? AND e.date<=?`, acc.id, to)).s;
  const sign = acc.type === 'asset' ? 1 : -1;
  const last = await db.get('SELECT * FROM reconciliations WHERE account_id=? ORDER BY statement_date DESC LIMIT 1', acc.id);
  return { account: acc, lines, cleared: cleared * sign, book: book * sign, sign, last };
}));
app.patch('/api/lines/:id/cleared', auth(...WRITE), h(async req => {
  await db.run('UPDATE lines SET cleared=? WHERE id=?', req.body.cleared ? 1 : 0, Number(req.params.id));
  return { ok: true };
}));
app.post('/api/reconciliations', auth(...WRITE), h(async req => {
  const b = req.body;
  const acc = await db.get('SELECT * FROM accounts WHERE id=? AND is_payment=1', Number(b.account_id) || 0);
  if (!acc || !L.isDate(b.statement_date)) throw new L.UserError('Account and statement date are required');
  const sign = acc.type === 'asset' ? 1 : -1;
  const cleared = sign * (await db.get(`SELECT COALESCE(SUM(l.debit-l.credit),0) s FROM lines l JOIN entries e ON e.id=l.entry_id WHERE l.account_id=? AND l.cleared=1 AND e.date<=?`, acc.id, b.statement_date)).s;
  const stmt = L.cents(b.statement_balance);
  if (cleared !== stmt && !b.force) throw new L.UserError(`Cleared balance ($${(cleared / 100).toFixed(2)}) does not match the statement ($${(stmt / 100).toFixed(2)}). Find the difference first.`);
  await db.run('INSERT INTO reconciliations(account_id,statement_date,statement_balance,cleared_balance,user_id) VALUES(?,?,?,?,?)', acc.id, b.statement_date, stmt, cleared, req.user.id);
  await audit(req.user.id, 'reconcile', { account: acc.name, date: b.statement_date, statement: stmt, cleared });
  return { ok: true };
}));

// ---------- bank import ----------
app.post('/api/import', auth(...WRITE), h(req => L.importRows(Number(req.body.account_id), req.body.rows || [], req.user.id)));

// ---------- dashboard ----------
app.get('/api/dashboard', auth(), h(async () => {
  const today = new Date().toISOString().slice(0, 10);
  const fy = await reports.fiscalYearStart(today);
  const month = today.slice(0, 8) + '01';
  const s = await reports.sums(null, today);
  const accs = (await db.all('SELECT * FROM accounts WHERE is_payment=1 AND active=1 ORDER BY code'))
    .map(a => ({ id: a.id, name: a.name, type: a.type, balance: (a.type === 'asset' ? 1 : -1) * (s.get(a.id) || { net: 0 }).net }));
  // Income & expenses per month for the last 12 months, in one query
  const start = new Date(Date.UTC(Number(today.slice(0, 4)), Number(today.slice(5, 7)) - 12, 1)).toISOString().slice(0, 10);
  const pm = await db.all(`SELECT substr(e.date,1,7) m, a.type, SUM(l.debit - l.credit) net FROM lines l JOIN entries e ON e.id=l.entry_id JOIN accounts a ON a.id=l.account_id
    WHERE a.type IN ('income','expense') AND e.date >= ? AND e.date <= ? GROUP BY m, a.type`, start, today);
  const months = [];
  for (let i = 11; i >= 0; i--) {
    const m = new Date(Date.UTC(Number(today.slice(0, 4)), Number(today.slice(5, 7)) - 1 - i, 1)).toISOString().slice(0, 7);
    const inc = -(pm.find(r => r.m === m && r.type === 'income') || { net: 0 }).net;
    const exp = (pm.find(r => r.m === m && r.type === 'expense') || { net: 0 }).net;
    months.push({ month: m, income: inc, expenses: exp, net: inc - exp });
  }
  const pl = async (f, t) => {
    const r = await db.all(`SELECT a.type, SUM(l.debit - l.credit) net FROM lines l JOIN entries e ON e.id=l.entry_id JOIN accounts a ON a.id=l.account_id
      WHERE a.type IN ('income','expense') AND e.date BETWEEN ? AND ? GROUP BY a.type`, f, t);
    const inc = -(r.find(x => x.type === 'income') || { net: 0 }).net, exp = (r.find(x => x.type === 'expense') || { net: 0 }).net;
    return { income: inc, expenses: exp, net: inc - exp };
  };
  const inv = await db.all(`SELECT i.total, i.due_date, (SELECT COALESCE(SUM(p.amount),0) FROM invoice_payments p JOIN entries e ON e.id=p.entry_id WHERE p.invoice_id=i.id AND e.voided=0) paid
    FROM invoices i WHERE i.voided=0`);
  const ar = inv.reduce((t, i) => t + i.total - i.paid, 0);
  const overdue = inv.filter(i => i.due_date < today).reduce((t, i) => t + i.total - i.paid, 0);
  const owners = (await reports.run('owner_equity', { from: '1900-01-01', to: today })).rows.filter(r => !r.style).map(r => ({ name: r.cells[0], share: r.cells[1], net: r.cells[5] }));
  const taxAccts = await db.all(`SELECT id FROM accounts WHERE subtype IN ('payroll_liability','sales_tax')`);
  const taxes_owed = taxAccts.reduce((t, a) => t - ((s.get(a.id) || { net: 0 }).net), 0);
  const missing = (await reports.run('missing_receipts', { from: fy, to: today })).rows.length;
  const recent = await db.all(`SELECT e.id,e.date,e.kind,e.memo,e.voided,c.name contact_name,(SELECT SUM(debit) FROM lines WHERE entry_id=e.id) amount FROM entries e LEFT JOIN contacts c ON c.id=e.contact_id ORDER BY e.id DESC LIMIT 10`);
  return { today, fy, accounts: accs, ytd: await pl(fy, today), mtd: await pl(month, today), months, ar, overdue, owners, taxes_owed, missing_receipts: missing, recent };
}));

// ---------- reports & exports ----------
app.get('/api/reports', auth(), h(() => reports.CATALOG.map(([id, title, desc]) => ({ id, title, desc }))));
app.get('/api/reports/:name', auth(), h(async (req, res) => {
  const rep = await reports.run(req.params.name, req.query);
  if (!rep) throw new L.UserError('Unknown report');
  if (req.query.format === 'csv') {
    res.set('Content-Type', 'text/csv; charset=utf-8');
    res.set('Content-Disposition', `attachment; filename="${req.params.name.replace(/\W/g, '')}_${String(req.query.to || 'latest').replace(/[^\d-]/g, '')}.csv"`);
    res.send('﻿' + reports.toCSV(rep));
    return;
  }
  return rep;
}));

const toCsvRows = rows => {
  if (!rows.length) return '';
  const keys = Object.keys(rows[0]);
  const esc = v => v == null ? '' : /[",\n]/.test(String(v)) ? `"${String(v).replace(/"/g, '""')}"` : String(v);
  return '﻿' + [keys.join(','), ...rows.map(r => keys.map(k => esc(r[k])).join(','))].join('\r\n');
};

app.get('/api/export/package', auth('owner', 'accountant'), h(async (req, res) => {
  const { from, to } = await reports.range(req.query);
  const s = await allSettings();
  const zip = new yazl.ZipFile();
  const name = `${(s.company || 'books').replace(/[^\w]+/g, '_')}_accountant_package_${from}_to_${to}`;
  const order = ['pnl', 'balance_sheet', 'cash_flow', 'trial_balance', 'tax_categories', 'owner_equity', 'owner_activity', 'payroll_summary', 'contractors_1099',
    'income_by_client', 'expenses_by_vendor', 'ar_aging', 'sales_tax', 'general_ledger', 'journal', 'missing_receipts', 'reconciliations', 'chart_of_accounts', 'audit_log'];
  for (const [i, r] of order.entries())
    zip.addBuffer(Buffer.from('﻿' + reports.toCSV(await reports.run(r, { from, to }))), `${name}/${String(i + 1).padStart(2, '0')}_${r}.csv`);
  zip.addBuffer(Buffer.from(toCsvRows(await db.all(`SELECT id,type,name,email,phone,address,tax_id,is_1099,profit_share FROM contacts ORDER BY type,name`))), `${name}/data_contacts.csv`);
  zip.addBuffer(Buffer.from(toCsvRows(await db.all(`SELECT i.number,i.date,i.due_date,c.name client,i.subtotal/100.0 subtotal,i.tax_rate,i.tax/100.0 tax,i.total/100.0 total,i.voided FROM invoices i JOIN contacts c ON c.id=i.client_id WHERE i.date BETWEEN ? AND ? ORDER BY i.date`, from, to))), `${name}/data_invoices.csv`);
  const atts = await db.all(`SELECT a.*, e.date, e.memo, e.kind FROM attachments a JOIN entries e ON e.id=a.entry_id WHERE e.date BETWEEN ? AND ? ORDER BY e.date, e.id`, from, to);
  const idx = [];
  for (const a of atts) {
    const fn = `receipts/${a.date}_entry${a.entry_id}_${a.id}_${a.filename.replace(/[^\w.\-]+/g, '_')}`;
    const buf = await readFile(a).catch(() => null);
    if (buf) zip.addBuffer(buf, `${name}/${fn}`);
    idx.push({ entry: a.entry_id, date: a.date, type: a.kind, memo: a.memo, file: buf ? fn : '(missing)' });
  }
  zip.addBuffer(Buffer.from(toCsvRows(idx)), `${name}/receipts_index.csv`);
  zip.addBuffer(Buffer.from(`${s.company} — Accountant package
Period: ${from} to ${to}
Entity: ${s.entity_type || ''}   EIN: ${s.ein || ''}
Address: ${(s.address || '').replace(/\n/g, ', ')}
Fiscal year starts in month: ${s.fiscal_start_month}   Books locked through: ${s.lock_date || '(not locked)'}
Generated: ${new Date().toISOString()} by ${req.user.name}

Basis: accrual (invoices are income when issued; payments clear Accounts Receivable).
All amounts in USD. Double-entry; the trial balance must show debits = credits.
Owner deposits are recorded as OWNER CAPITAL (equity), per owner — not income, not loans.
Owner withdrawals are recorded as OWNER DRAWS, per owner.
Voided transactions are kept and reversed with an offsetting entry (see journal / audit log).
Every receipt/bill attached in the app is in /receipts and listed in receipts_index.csv by entry number.

Files:
${order.map((r, i) => `  ${String(i + 1).padStart(2, '0')}_${r}.csv`).join('\n')}
  data_contacts.csv, data_invoices.csv, receipts_index.csv, receipts/
`), `${name}/README.txt`);
  zip.end();
  await audit(req.user.id, 'export.package', { from, to });
  res.set('Content-Type', 'application/zip');
  res.set('Content-Disposition', `attachment; filename="${name}.zip"`);
  await new Promise((resolve, reject) => zip.outputStream.pipe(res).on('finish', resolve).on('error', reject));
}));

// Full backup: every table as CSV in one ZIP (receipts are in the accountant package / blob store).
app.get('/api/export/backup', auth('owner'), h(async (req, res) => {
  const zip = new yazl.ZipFile();
  for (const t of ['settings', 'users', 'contacts', 'accounts', 'entries', 'lines', 'attachments', 'invoices', 'invoice_items', 'invoice_payments', 'payroll_items', 'reconciliations', 'audit']) {
    const rows = await db.all(t === 'users' ? 'SELECT id,name,email,role,active,created_at FROM users ORDER BY id' : `SELECT * FROM ${t}${t === 'settings' ? '' : ' ORDER BY id'}`);
    zip.addBuffer(Buffer.from(toCsvRows(rows)), `backup/${t}.csv`);
  }
  zip.end();
  await audit(req.user.id, 'export.backup');
  res.set('Content-Type', 'application/zip');
  res.set('Content-Disposition', `attachment; filename="books-backup-${new Date().toISOString().slice(0, 10)}.zip"`);
  await new Promise((resolve, reject) => zip.outputStream.pipe(res).on('finish', resolve).on('error', reject));
}));

app.use('/api', (req, res) => res.status(404).json({ error: 'Not found' }));
app.get('*', (req, res) => res.sendFile(path.join(__dirname, 'public', 'index.html')));

const PORT = Number(process.env.PORT) || 3000;
if (require.main === module) db.ready().then(() => app.listen(PORT, () => console.log(`Zsi Books running at http://localhost:${PORT}`)));
module.exports = app;
