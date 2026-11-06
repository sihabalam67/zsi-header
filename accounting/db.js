// Database: schema, seed chart of accounts, and low-level helpers.
// All money is stored as integer cents to avoid floating-point errors.
const Database = require('better-sqlite3');
const path = require('path');
const fs = require('fs');

const DATA_DIR = process.env.DATA_DIR || path.join(__dirname, 'data');
fs.mkdirSync(path.join(DATA_DIR, 'uploads'), { recursive: true });

const db = new Database(path.join(DATA_DIR, 'books.db'));
db.pragma('journal_mode = WAL');
db.pragma('foreign_keys = ON');

db.exec(`
CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT);

CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE COLLATE NOCASE,
  pass_hash TEXT NOT NULL,
  role TEXT NOT NULL CHECK (role IN ('owner','staff','accountant')),
  active INTEGER NOT NULL DEFAULT 1,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS sessions (
  token TEXT PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id),
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS contacts (
  id INTEGER PRIMARY KEY,
  type TEXT NOT NULL CHECK (type IN ('client','vendor','employee','owner')),
  name TEXT NOT NULL,
  email TEXT, phone TEXT, address TEXT,
  tax_id TEXT,                 -- EIN / SSN last 4 / W-9 info
  is_1099 INTEGER NOT NULL DEFAULT 0,
  profit_share REAL,           -- owners only, percent
  notes TEXT,
  active INTEGER NOT NULL DEFAULT 1,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS accounts (
  id INTEGER PRIMARY KEY,
  code TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  type TEXT NOT NULL CHECK (type IN ('asset','liability','equity','income','expense')),
  subtype TEXT,                -- bank, card, receivable, fixed_asset, payroll_liability, sales_tax, loan, capital, draws, retained ...
  tax_category TEXT,           -- label for the tax preparer
  is_payment INTEGER NOT NULL DEFAULT 0, -- money moves in/out of it (bank, cash, credit card)
  owner_contact_id INTEGER REFERENCES contacts(id),
  system INTEGER NOT NULL DEFAULT 0,
  active INTEGER NOT NULL DEFAULT 1,
  description TEXT
);

CREATE TABLE IF NOT EXISTS entries (
  id INTEGER PRIMARY KEY,
  date TEXT NOT NULL,          -- YYYY-MM-DD
  kind TEXT NOT NULL,          -- expense, income, owner_contribution, owner_draw, transfer, payroll, journal, invoice, invoice_payment, import, void
  memo TEXT,
  reference TEXT,              -- check #, bill #, invoice #
  contact_id INTEGER REFERENCES contacts(id),
  voided INTEGER NOT NULL DEFAULT 0,
  void_of INTEGER REFERENCES entries(id),
  import_hash TEXT,
  created_by INTEGER REFERENCES users(id),
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_entries_date ON entries(date);
CREATE UNIQUE INDEX IF NOT EXISTS idx_entries_import ON entries(import_hash) WHERE import_hash IS NOT NULL;

CREATE TABLE IF NOT EXISTS lines (
  id INTEGER PRIMARY KEY,
  entry_id INTEGER NOT NULL REFERENCES entries(id),
  account_id INTEGER NOT NULL REFERENCES accounts(id),
  debit INTEGER NOT NULL DEFAULT 0,
  credit INTEGER NOT NULL DEFAULT 0,
  memo TEXT,
  cleared INTEGER NOT NULL DEFAULT 0,
  CHECK (debit >= 0 AND credit >= 0 AND NOT (debit > 0 AND credit > 0))
);
CREATE INDEX IF NOT EXISTS idx_lines_entry ON lines(entry_id);
CREATE INDEX IF NOT EXISTS idx_lines_account ON lines(account_id);

CREATE TABLE IF NOT EXISTS attachments (
  id INTEGER PRIMARY KEY,
  entry_id INTEGER NOT NULL REFERENCES entries(id),
  filename TEXT NOT NULL,
  stored TEXT NOT NULL,
  mime TEXT, size INTEGER,
  uploaded_by INTEGER REFERENCES users(id),
  uploaded_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS invoices (
  id INTEGER PRIMARY KEY,
  number TEXT NOT NULL UNIQUE,
  client_id INTEGER NOT NULL REFERENCES contacts(id),
  date TEXT NOT NULL,
  due_date TEXT NOT NULL,
  memo TEXT,
  subtotal INTEGER NOT NULL,
  tax_rate REAL NOT NULL DEFAULT 0,
  tax INTEGER NOT NULL DEFAULT 0,
  total INTEGER NOT NULL,
  income_account_id INTEGER NOT NULL REFERENCES accounts(id),
  entry_id INTEGER REFERENCES entries(id),
  voided INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS invoice_items (
  id INTEGER PRIMARY KEY,
  invoice_id INTEGER NOT NULL REFERENCES invoices(id),
  description TEXT NOT NULL,
  qty REAL NOT NULL,
  unit_price INTEGER NOT NULL,
  amount INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS invoice_payments (
  id INTEGER PRIMARY KEY,
  invoice_id INTEGER NOT NULL REFERENCES invoices(id),
  entry_id INTEGER NOT NULL REFERENCES entries(id),
  amount INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS payroll_items (
  id INTEGER PRIMARY KEY,
  entry_id INTEGER NOT NULL REFERENCES entries(id),
  employee_id INTEGER NOT NULL REFERENCES contacts(id),
  pay_date TEXT NOT NULL,
  period_start TEXT, period_end TEXT,
  gross INTEGER NOT NULL,
  fed_wh INTEGER NOT NULL DEFAULT 0,
  ss_ee INTEGER NOT NULL DEFAULT 0,
  med_ee INTEGER NOT NULL DEFAULT 0,
  state_wh INTEGER NOT NULL DEFAULT 0,
  city_wh INTEGER NOT NULL DEFAULT 0,
  sdi_pfl INTEGER NOT NULL DEFAULT 0,
  other_ded INTEGER NOT NULL DEFAULT 0,
  net INTEGER NOT NULL,
  ss_er INTEGER NOT NULL DEFAULT 0,
  med_er INTEGER NOT NULL DEFAULT 0,
  futa INTEGER NOT NULL DEFAULT 0,
  suta INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS reconciliations (
  id INTEGER PRIMARY KEY,
  account_id INTEGER NOT NULL REFERENCES accounts(id),
  statement_date TEXT NOT NULL,
  statement_balance INTEGER NOT NULL,
  cleared_balance INTEGER NOT NULL,
  user_id INTEGER REFERENCES users(id),
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS audit (
  id INTEGER PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  action TEXT NOT NULL,
  detail TEXT,
  at TEXT NOT NULL DEFAULT (datetime('now'))
);
`);

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

function seedAccounts() {
  const n = db.prepare('SELECT COUNT(*) c FROM accounts').get().c;
  if (n) return;
  const ins = db.prepare(`INSERT INTO accounts (code,name,type,subtype,tax_category,is_payment,system)
    VALUES (?,?,?,?,?,?,1)`);
  db.transaction(() => SEED_ACCOUNTS.forEach(a => ins.run(...a)))();
}
seedAccounts();

// ---------- helpers ----------
const getSetting = (k, def = null) => {
  const r = db.prepare('SELECT value FROM settings WHERE key=?').get(k);
  return r ? r.value : def;
};
const setSetting = (k, v) =>
  db.prepare('INSERT INTO settings(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value').run(k, v == null ? null : String(v));

const accountByCode = code => {
  const a = db.prepare('SELECT * FROM accounts WHERE code=?').get(code);
  if (!a) throw new Error(`Account ${code} is missing from the chart of accounts`);
  return a;
};

// Owners get their own Capital and Draws equity accounts so each owner's
// money in / money out is tracked separately (needed for K-1 capital accounts).
function createOwnerAccounts(contact) {
  const next = base => {
    const r = db.prepare(`SELECT MAX(CAST(code AS INTEGER)) m FROM accounts WHERE CAST(code AS INTEGER) BETWEEN ? AND ?`).get(base, base + 389);
    return String((r.m || base) + 10);
  };
  const ins = db.prepare(`INSERT INTO accounts (code,name,type,subtype,owner_contact_id,system,tax_category)
    VALUES (?,?,'equity',?,?,1,?)`);
  ins.run(next(3000), `Owner Capital – ${contact.name}`, 'capital', contact.id, 'Owner capital contributions');
  ins.run(next(3500), `Owner Draws – ${contact.name}`, 'draws', contact.id, 'Owner distributions / draws');
}

function audit(userId, action, detail) {
  db.prepare('INSERT INTO audit(user_id,action,detail) VALUES(?,?,?)')
    .run(userId || null, action, detail ? JSON.stringify(detail) : null);
}

module.exports = { db, DATA_DIR, getSetting, setSetting, accountByCode, createOwnerAccounts, audit };
