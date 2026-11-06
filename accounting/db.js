// Database: Postgres everywhere.
//  - Online (Vercel): DATABASE_URL / POSTGRES_URL from a free Neon database.
//  - On your own computer: an embedded Postgres (PGlite) stored in ./data/pg – nothing to install.
// All money is stored as integer cents to avoid floating-point errors.
const path = require('path');
const fs = require('fs');
const { AsyncLocalStorage } = require('async_hooks');

const DATA_DIR = process.env.DATA_DIR || path.join(__dirname, 'data');
const DB_URL = process.env.DATABASE_URL || process.env.POSTGRES_URL || '';
const ON_VERCEL = !!process.env.VERCEL;
const als = new AsyncLocalStorage();

class NotConfigured extends Error {}

const NOW = `(to_char(now() AT TIME ZONE 'UTC', 'YYYY-MM-DD HH24:MI:SS'))`;
const SCHEMA = `
CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT);

CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  pass_hash TEXT NOT NULL,
  role TEXT NOT NULL CHECK (role IN ('owner','staff','accountant')),
  active INTEGER NOT NULL DEFAULT 1,
  created_at TEXT NOT NULL DEFAULT ${NOW}
);

CREATE TABLE IF NOT EXISTS sessions (
  token TEXT PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id),
  created_at TEXT NOT NULL DEFAULT ${NOW}
);

CREATE TABLE IF NOT EXISTS contacts (
  id SERIAL PRIMARY KEY,
  type TEXT NOT NULL CHECK (type IN ('client','vendor','employee','owner')),
  name TEXT NOT NULL,
  email TEXT, phone TEXT, address TEXT,
  tax_id TEXT,
  is_1099 INTEGER NOT NULL DEFAULT 0,
  profit_share DOUBLE PRECISION,
  notes TEXT,
  active INTEGER NOT NULL DEFAULT 1,
  created_at TEXT NOT NULL DEFAULT ${NOW}
);

CREATE TABLE IF NOT EXISTS accounts (
  id SERIAL PRIMARY KEY,
  code TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  type TEXT NOT NULL CHECK (type IN ('asset','liability','equity','income','expense')),
  subtype TEXT,
  tax_category TEXT,
  is_payment INTEGER NOT NULL DEFAULT 0,
  owner_contact_id INTEGER REFERENCES contacts(id),
  system INTEGER NOT NULL DEFAULT 0,
  active INTEGER NOT NULL DEFAULT 1,
  description TEXT
);

CREATE TABLE IF NOT EXISTS entries (
  id SERIAL PRIMARY KEY,
  date TEXT NOT NULL,
  kind TEXT NOT NULL,
  memo TEXT,
  reference TEXT,
  contact_id INTEGER REFERENCES contacts(id),
  voided INTEGER NOT NULL DEFAULT 0,
  void_of INTEGER REFERENCES entries(id),
  import_hash TEXT,
  created_by INTEGER REFERENCES users(id),
  created_at TEXT NOT NULL DEFAULT ${NOW}
);
CREATE INDEX IF NOT EXISTS idx_entries_date ON entries(date);
CREATE UNIQUE INDEX IF NOT EXISTS idx_entries_import ON entries(import_hash) WHERE import_hash IS NOT NULL;

CREATE TABLE IF NOT EXISTS lines (
  id SERIAL PRIMARY KEY,
  entry_id INTEGER NOT NULL REFERENCES entries(id),
  account_id INTEGER NOT NULL REFERENCES accounts(id),
  debit BIGINT NOT NULL DEFAULT 0,
  credit BIGINT NOT NULL DEFAULT 0,
  memo TEXT,
  cleared INTEGER NOT NULL DEFAULT 0,
  CHECK (debit >= 0 AND credit >= 0 AND NOT (debit > 0 AND credit > 0))
);
CREATE INDEX IF NOT EXISTS idx_lines_entry ON lines(entry_id);
CREATE INDEX IF NOT EXISTS idx_lines_account ON lines(account_id);

CREATE TABLE IF NOT EXISTS attachments (
  id SERIAL PRIMARY KEY,
  entry_id INTEGER NOT NULL REFERENCES entries(id),
  filename TEXT NOT NULL,
  stored TEXT NOT NULL,
  storage TEXT NOT NULL DEFAULT 'disk',
  mime TEXT, size INTEGER,
  uploaded_by INTEGER REFERENCES users(id),
  uploaded_at TEXT NOT NULL DEFAULT ${NOW}
);

CREATE TABLE IF NOT EXISTS invoices (
  id SERIAL PRIMARY KEY,
  number TEXT NOT NULL UNIQUE,
  client_id INTEGER NOT NULL REFERENCES contacts(id),
  date TEXT NOT NULL,
  due_date TEXT NOT NULL,
  memo TEXT,
  subtotal BIGINT NOT NULL,
  tax_rate DOUBLE PRECISION NOT NULL DEFAULT 0,
  tax BIGINT NOT NULL DEFAULT 0,
  total BIGINT NOT NULL,
  income_account_id INTEGER NOT NULL REFERENCES accounts(id),
  entry_id INTEGER REFERENCES entries(id),
  voided INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL DEFAULT ${NOW}
);

CREATE TABLE IF NOT EXISTS invoice_items (
  id SERIAL PRIMARY KEY,
  invoice_id INTEGER NOT NULL REFERENCES invoices(id),
  description TEXT NOT NULL,
  qty DOUBLE PRECISION NOT NULL,
  unit_price BIGINT NOT NULL,
  amount BIGINT NOT NULL
);

CREATE TABLE IF NOT EXISTS invoice_payments (
  id SERIAL PRIMARY KEY,
  invoice_id INTEGER NOT NULL REFERENCES invoices(id),
  entry_id INTEGER NOT NULL REFERENCES entries(id),
  amount BIGINT NOT NULL
);

CREATE TABLE IF NOT EXISTS payroll_items (
  id SERIAL PRIMARY KEY,
  entry_id INTEGER NOT NULL REFERENCES entries(id),
  employee_id INTEGER NOT NULL REFERENCES contacts(id),
  pay_date TEXT NOT NULL,
  period_start TEXT, period_end TEXT,
  gross BIGINT NOT NULL,
  fed_wh BIGINT NOT NULL DEFAULT 0,
  ss_ee BIGINT NOT NULL DEFAULT 0,
  med_ee BIGINT NOT NULL DEFAULT 0,
  state_wh BIGINT NOT NULL DEFAULT 0,
  city_wh BIGINT NOT NULL DEFAULT 0,
  sdi_pfl BIGINT NOT NULL DEFAULT 0,
  other_ded BIGINT NOT NULL DEFAULT 0,
  net BIGINT NOT NULL,
  ss_er BIGINT NOT NULL DEFAULT 0,
  med_er BIGINT NOT NULL DEFAULT 0,
  futa BIGINT NOT NULL DEFAULT 0,
  suta BIGINT NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS reconciliations (
  id SERIAL PRIMARY KEY,
  account_id INTEGER NOT NULL REFERENCES accounts(id),
  statement_date TEXT NOT NULL,
  statement_balance BIGINT NOT NULL,
  cleared_balance BIGINT NOT NULL,
  user_id INTEGER REFERENCES users(id),
  created_at TEXT NOT NULL DEFAULT ${NOW}
);

CREATE TABLE IF NOT EXISTS login_attempts (key TEXT NOT NULL, at TEXT NOT NULL DEFAULT ${NOW});
CREATE INDEX IF NOT EXISTS idx_login_attempts ON login_attempts(key, at);

CREATE TABLE IF NOT EXISTS audit (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  action TEXT NOT NULL,
  detail TEXT,
  at TEXT NOT NULL DEFAULT ${NOW}
);
`;

// ---------- Chart of accounts (New York / US small business) ----------
// [code, name, type, subtype, tax_category, is_payment]
const SEED_ACCOUNTS = [
  ['1000', 'Business Checking', 'asset', 'bank', null, 1],
  ['1010', 'Business Savings', 'asset', 'bank', null, 1],
  ['1050', 'Petty Cash', 'asset', 'bank', null, 1],
  ['1100', 'Accounts Receivable', 'asset', 'receivable', null, 0],
  ['1200', 'Prepaid Expenses', 'asset', 'prepaid', null, 0],
  ['1500', 'Computer & Office Equipment', 'asset', 'fixed_asset', 'Depreciable assets (Form 4562)', 0],
  ['1590', 'Accumulated Depreciation', 'asset', 'fixed_asset', 'Depreciable assets (Form 4562)', 0],
  ['2000', 'Accounts Payable', 'liability', 'payable', null, 0],
  ['2100', 'Business Credit Card', 'liability', 'card', null, 1],
  ['2200', 'Federal Income Tax Withheld', 'liability', 'payroll_liability', 'Payroll: Form 941', 0],
  ['2210', 'FICA Payable (Social Security & Medicare)', 'liability', 'payroll_liability', 'Payroll: Form 941', 0],
  ['2220', 'NY State Income Tax Withheld', 'liability', 'payroll_liability', 'Payroll: NYS-45', 0],
  ['2230', 'NYC Income Tax Withheld', 'liability', 'payroll_liability', 'Payroll: NYS-45', 0],
  ['2240', 'NY SDI / Paid Family Leave Withheld', 'liability', 'payroll_liability', 'Payroll: NY DBL/PFL', 0],
  ['2250', 'FUTA Payable', 'liability', 'payroll_liability', 'Payroll: Form 940', 0],
  ['2260', 'NY Unemployment (SUI) Payable', 'liability', 'payroll_liability', 'Payroll: NYS-45', 0],
  ['2270', 'Other Payroll Deductions Payable', 'liability', 'payroll_liability', null, 0],
  ['2300', 'NY Sales Tax Payable', 'liability', 'sales_tax', 'NY Sales Tax (ST-100/ST-101)', 0],
  ['2400', 'Accrued Expenses', 'liability', 'accrued', null, 0],
  ['2500', 'Loans Payable', 'liability', 'loan', null, 0],
  ['3900', 'Retained Earnings', 'equity', 'retained', null, 0],
  ['4000', 'Service / Project Revenue', 'income', null, 'Gross receipts or sales', 0],
  ['4100', 'Subscription / SaaS Revenue', 'income', null, 'Gross receipts or sales', 0],
  ['4900', 'Other Income (Interest etc.)', 'income', null, 'Other income', 0],
  ['5000', 'Salaries & Wages', 'expense', 'payroll', 'Salaries and wages', 0],
  ['5100', 'Payroll Taxes (Employer)', 'expense', 'payroll', 'Taxes and licenses', 0],
  ['5150', 'Employee Benefits', 'expense', null, 'Employee benefit programs', 0],
  ['5200', 'Contractors (1099)', 'expense', null, 'Contract labor', 0],
  ['5300', 'Rent', 'expense', null, 'Rent', 0],
  ['5400', 'Hosting & Cloud', 'expense', null, 'Other deductions: Hosting & cloud', 0],
  ['5410', 'Software & SaaS Subscriptions', 'expense', null, 'Other deductions: Software', 0],
  ['5420', 'AI / API Usage', 'expense', null, 'Other deductions: Software', 0],
  ['5500', 'Internet & Phone', 'expense', null, 'Utilities', 0],
  ['5600', 'Legal & Accounting Fees', 'expense', null, 'Legal and professional services', 0],
  ['5700', 'Advertising & Marketing', 'expense', null, 'Advertising', 0],
  ['5800', 'Travel', 'expense', null, 'Travel', 0],
  ['5810', 'Business Meals', 'expense', null, 'Meals (generally 50% deductible)', 0],
  ['5900', 'Office Supplies', 'expense', null, 'Office expense', 0],
  ['5910', 'Bank & Payment Processing Fees', 'expense', null, 'Other deductions: Bank fees', 0],
  ['5920', 'Insurance', 'expense', null, 'Insurance', 0],
  ['5930', 'Taxes, Licenses & Filing Fees', 'expense', null, 'Taxes and licenses', 0],
  ['5940', 'Depreciation', 'expense', null, 'Depreciation', 0],
  ['5950', 'Interest Expense', 'expense', null, 'Interest', 0],
  ['5990', 'Other Expenses', 'expense', null, 'Other deductions', 0],
];

// Postgres returns BIGINT / NUMERIC (e.g. SUM of cents) as strings. Money here is always whole cents,
// so convert those columns to plain numbers for every query, whichever driver is used.
function numify(r) {
  const num = (r.fields || []).filter(f => f.dataTypeID === 20 || f.dataTypeID === 1700).map(f => f.name);
  if (num.length) for (const row of r.rows) for (const k of num) if (row[k] != null) row[k] = Number(row[k]);
  return { rows: r.rows, rowCount: r.rowCount ?? r.affectedRows };
}

// ---------- driver ----------
// Both drivers expose: exec(sql, params) -> { rows, rowCount }, and transaction(fn(execFn)).
let ready = null;
function connect() {
  if (ready) return ready;
  ready = (async () => {
    let drv;
    if (DB_URL) {
      const pg = require('pg');
      const pool = new pg.Pool({ connectionString: DB_URL, max: 3, idleTimeoutMillis: 10000 });
      drv = {
        exec: (sql, p) => pool.query(sql, p).then(numify),
        async transaction(fn) {
          const c = await pool.connect();
          try {
            await c.query('BEGIN');
            const out = await fn((sql, p) => c.query(sql, p).then(numify));
            await c.query('COMMIT');
            return out;
          } catch (e) {
            await c.query('ROLLBACK').catch(() => {});
            throw e;
          } finally { c.release(); }
        },
      };
      await drv.transaction(async x => {
        await x('SELECT pg_advisory_xact_lock(4242001)'); // avoid concurrent schema creation on cold starts
        await x(SCHEMA);
      });
    } else {
      if (ON_VERCEL) throw new NotConfigured('Database not connected. In Vercel: Storage → Create Database → Neon (free) → connect it to this project, then redeploy.');
      const { PGlite } = require('@electric-sql/pglite');
      const dir = process.env.PGLITE_MEMORY ? undefined : path.join(DATA_DIR, 'pg');
      if (dir) fs.mkdirSync(dir, { recursive: true });
      const pgl = new PGlite(dir);
      let chain = Promise.resolve();
      // PGlite is single-connection: serialize transactions so they can't interleave.
      const serial = fn => { const p = chain.then(fn, fn); chain = p.catch(() => {}); return p; };
      drv = {
        exec: (sql, p) => pgl.query(sql, p).then(numify),
        transaction: fn => serial(() => pgl.transaction(tx => fn((sql, p) => tx.query(sql, p).then(numify)))),
      };
      await pgl.exec(SCHEMA);
      drv.serial = serial;
    }
    const n = (await drv.exec('SELECT COUNT(*) c FROM accounts')).rows[0].c;
    if (!n) {
      await drv.transaction(async x => {
        for (const a of SEED_ACCOUNTS)
          await x(`INSERT INTO accounts (code,name,type,subtype,tax_category,is_payment,system) VALUES ($1,$2,$3,$4,$5,$6,1) ON CONFLICT (code) DO NOTHING`, a);
      });
    }
    return drv;
  })();
  ready.catch(() => { ready = null; });
  return ready;
}

// Convert "?" placeholders to $1, $2 ...
const toPg = sql => { let i = 0; return sql.replace(/\?/g, () => `$${++i}`); };

async function exec(sql, params = []) {
  const inTx = als.getStore();
  if (inTx) return inTx(toPg(sql), params);
  const drv = await connect();
  if (drv.serial) return drv.serial(() => drv.exec(toPg(sql), params));
  return drv.exec(toPg(sql), params);
}

const db = {
  all: async (sql, ...p) => (await exec(sql, p)).rows,
  get: async (sql, ...p) => (await exec(sql, p)).rows[0],
  run: async (sql, ...p) => exec(sql, p),
  // INSERT ... returns the new id
  insert: async (sql, ...p) => (await exec(sql + ' RETURNING id', p)).rows[0].id,
  // Everything awaited inside fn runs in one database transaction.
  async tx(fn) {
    if (als.getStore()) return fn();
    const drv = await connect();
    return drv.transaction(x => als.run(x, fn));
  },
  ready: connect,
};

// ---------- helpers ----------
const getSetting = async (k, def = null) => {
  const r = await db.get('SELECT value FROM settings WHERE key=?', k);
  return r ? r.value : def;
};
const setSetting = (k, v) =>
  db.run('INSERT INTO settings(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value', k, v == null ? null : String(v));

const accountByCode = async code => {
  const a = await db.get('SELECT * FROM accounts WHERE code=?', code);
  if (!a) throw new Error(`Account ${code} is missing from the chart of accounts`);
  return a;
};

// Owners get their own Capital and Draws equity accounts so each owner's
// money in / money out is tracked separately (needed for K-1 capital accounts).
async function createOwnerAccounts(contact) {
  const next = async base => {
    const r = await db.get(`SELECT MAX(CAST(code AS INTEGER)) m FROM accounts WHERE code ~ '^[0-9]+$' AND CAST(code AS INTEGER) BETWEEN ? AND ?`, base, base + 389);
    return String((r.m || base) + 10);
  };
  const sql = `INSERT INTO accounts (code,name,type,subtype,owner_contact_id,system,tax_category) VALUES (?,?,'equity',?,?,1,?)`;
  await db.run(sql, await next(3000), `Owner Capital – ${contact.name}`, 'capital', contact.id, 'Owner capital contributions');
  await db.run(sql, await next(3500), `Owner Draws – ${contact.name}`, 'draws', contact.id, 'Owner distributions / draws');
}

function audit(userId, action, detail) {
  return db.run('INSERT INTO audit(user_id,action,detail) VALUES(?,?,?)', userId || null, action, detail ? JSON.stringify(detail) : null);
}

module.exports = { db, DATA_DIR, ON_VERCEL, NotConfigured, getSetting, setSetting, accountByCode, createOwnerAccounts, audit };
