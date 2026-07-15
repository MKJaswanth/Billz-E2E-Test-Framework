# Crystal Billz — Accounting Modules User Flows

This document details the user flows, expected inputs, and core business rules of the **Accounting** section in Crystal Billz. This serves as a functional guide for QA and developer teams when implementing and verifying automated tests.

---

## 📂 Accounting Submenus Overview
The Accounting module is divided into three main operational groups:
1. **Voucher Management**: Handled via **Voucher History** and **Create Voucher** tools.
2. **Ledgers & Accounts**: Handled via the **Ledger List** and specific transaction category pages.
3. **Reports & Financial Statements**: Output screens (Day Book, Ledger Statement, Trial Balance, Profit & Loss, Balance Sheet, Cash Flow).

---

## 1. 📝 Voucher Creation Flow
* **Path**: `Accounting` ➔ `Vouchers` ➔ `Create`
* **Purpose**: Records financial transactions (debits and credits) between ledgers.

### A. Supported Voucher Types
* **Payment Voucher**: Used for outflows. Cash/Bank is credited; an expense/supplier ledger is debited.
* **Receipt Voucher**: Used for inflows. Cash/Bank is debited; income/customer ledger is credited.
* **Contra Voucher**: Used for internal cash/bank transactions (e.g., depositing cash into a bank).
* **Journal Voucher**: Multi-line adjustment entry. Total debits must equal total credits before saving.
* **Chit Entry**: Manages specialized chit fund accounts and transactions.
* **MDR Settlement**: Reconciles POS card payments against bank charges.

### B. Standard Form Fields
* **Voucher Type**: Dropdown (Selects the category above).
* **Date**: Datepicker.
* **Reference No**: Text input (Invoice / Bill reference).
* **Debit Ledger**: React-Select dropdown.
* **Credit Ledger**: React-Select dropdown.
* **Amount**: Numeric input.
* **Narration**: Text area (Reason or detail for the transaction).

### C. Allocation Feature (Invoice Matching)
* When a user creates a **Receipt Voucher** (selecting a customer ledger) or a **Payment Voucher** (selecting a supplier ledger), the form dynamically fetches outstanding invoices.
* The user can allocate the voucher amount against one or more of these invoices to reduce their outstanding balances.

---

## 2. 🔍 Audit & Verification Flows

### A. Voucher History
* **Path**: `Accounting` ➔ `Vouchers` ➔ `History`
* **User Actions**:
  - **Search**: Filter list by voucher number or reference.
  - **View Details**: Click "View" to open a modal displaying full debit/credit details.
  - **Print**: Generate a print-friendly view or PDF download.
  - **Cancel**: Void an incorrect or duplicate transaction.

### B. Day Book
* **Path**: `Accounting` ➔ `Day Book`
* **User Actions**:
  - Filter transactions by **Date Range**, **Voucher Type**, and **Branch**.
  - Review chronological balance logs to check daily entry totals.

### C. Ledger Statement
* **Path**: `Accounting` ➔ `Reports` ➔ `Ledger Statement`
* **User Actions**:
  - Select a target ledger account (e.g., Bank Account, Expense Ledger).
  - Select the **Branch** and **Date Range**.
  - **Metrics Displayed**: Opening Balance, Total Debits, Total Credits, and Closing Balance.
  - **Table Content**: Details each transaction (Date, Voucher ID, Narration, Debit, Credit) and features a running balance column.

---

## 3. 📈 Financial Statements & Closing Flows

### A. Trial Balance
* **Path**: `Accounting` ➔ `Reports` ➔ `Trial Balance`
* **User Actions**:
  - View list of all active ledger accounts categorized by Asset, Liability, Equity, Income, or Expense.
  - Drill down to expand/collapse subgroups.
  - Click on individual accounts to navigate directly to their detailed Ledger Statements.

### B. Profit & Loss (P&L) Statement
* **Path**: `Accounting` ➔ `Reports` ➔ `Profit & Loss`
* **User Actions**:
  - View summarized operating revenue, cost of sales, gross profit, overhead expenses, and net profit.

### C. Balance Sheet
* **Path**: `Accounting` ➔ `Reports` ➔ `Balance Sheet`
* **User Actions**:
  - View the overall financial position of the company. Shows the formula: `Assets = Liabilities + Owner's Equity`.

### D. Cash Flow Statement
* **Path**: `Accounting` ➔ `Reports` ➔ `Cash Flow`
* **User Actions**:
  - Check cash movements classified into Operating, Investing, and Financing activities.
