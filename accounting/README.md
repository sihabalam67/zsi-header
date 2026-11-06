# Zsi Books: accounting for Zsi.AI

Double-entry bookkeeping for a two-owner New York company, in USD. It's built so your tax preparer gets everything from one download and doesn't have to ask you questions.

## Run it

```bash
cd accounting
npm install
npm start            # http://localhost:3000
npm test             # end-to-end accounting checks
```

The first time you open it, a setup screen asks for the company name, both owners, profit shares and your login.

Everything is stored in `accounting/data/`:

- `books.db` is the whole ledger in one SQLite file.
- `uploads/` holds the receipts you attach.

Back up that folder. You can also go to Settings → Download backup.

### Put it online for both owners

Use any host that gives you a **persistent disk**. Render, Railway and Fly.io work, and so does a $5 VPS. Vercel and Netlify serverless don't keep files, so they won't work.

1. Set the start command to `npm start` and the root folder to `accounting/`.
2. Set `DATA_DIR` to the mounted disk path, for example `/data`.
3. Serve it over HTTPS and set `COOKIE_SECURE=1`.

## How each situation is recorded

| What happened | Where | What the books do |
|---|---|---|
| An owner puts money in, in any amount or none | Record money → **Owner deposit** | Bank ↑, *Owner Capital – that owner* ↑. This is equity, not income and not a loan. Each owner is tracked separately, so unequal deposits are fine. |
| An owner takes money out | Record money → **Owner withdrawal** | *Owner Draws – that owner* ↑, Bank ↓. This is not an expense. |
| Rent, hosting, AWS, OpenAI, software, contractors | Record money → **Expense** | Expense ↑, Bank or card ↓. You can split one payment across several categories and attach the receipt. |
| Salary | Record money → **Payroll** | Gross wages and employer taxes are expenses. Every withholding (Federal, FICA, NY State, NYC, SDI/PFL, FUTA, SUI) becomes a liability. Net pay comes out of the bank. |
| Paying the IRS or NY the withheld taxes | Expense → category under "Pay down a liability" | Clears the liability. |
| Billing a client | **Invoices → New** | Accounts Receivable ↑, Revenue ↑, plus NY sales tax if you set a rate. You can print it to PDF. |
| A client pays | Open the invoice → **Record payment** | Bank ↑, Receivable ↓. Partial payments work, and Stripe/PayPal fees can be recorded on the payment. |
| Money in without an invoice | Record money → **Money in** | Bank ↑, Income ↑. |
| Paying the credit card, or moving money to savings | Record money → **Transfer** | Neither income nor expense. |
| A bank statement | **Import bank CSV** | Categorize each row. Duplicates are skipped. |
| A mistake | Open the entry → **Void** | An exact reversing entry is posted. Nothing is ever deleted. |

## What the accountant gets

Go to **Reports → Accountant / tax package** and choose the year. You get one ZIP containing:

- Profit & Loss, Balance Sheet, Cash Flow, Trial Balance
- General Ledger and full Journal
- Income and expenses grouped by tax category
- Owners' capital statement and every owner deposit and draw (for K-1 capital accounts)
- Payroll summary by employee and by quarter (for W-2, 941, 940 and NYS-45)
- Vendor payments and 1099-NEC list
- Income by client, expenses by vendor
- A/R aging and NY sales tax
- Bank reconciliations
- Chart of accounts and the audit log
- Every receipt, named by entry number
- A README explaining how the books are kept

You can also give the accountant their own **read-only login**: Settings → Users → role "accountant".

## Year-end checklist

1. Reconcile every bank and card account through Dec 31. Use **Reconcile bank**.
2. Clear the **Missing receipts** report.
3. Download the accountant package and send it.
4. After the return is filed, lock the year: **Settings → Close the books**.

## Rules the software enforces

- Every entry must balance: debits = credits. Money is stored as integer cents.
- Amounts can't be edited. You void and re-enter, which keeps a clean audit trail.
- Closed periods are locked.
- Roles:
  - **owner** can do everything.
  - **staff** can record transactions but can't void or change settings.
  - **accountant** has read-only access plus exports.
- Every change is written to the audit log.

> The tax categories, 1099 threshold and sales-tax handling are there to speed things up for your CPA. They don't replace your CPA's judgment. Confirm your entity type (partnership, S-corp, …) and whether NY sales tax applies to your services.
