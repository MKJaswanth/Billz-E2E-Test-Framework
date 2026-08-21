# 🚀 Crystal Billz — CI Regression Suite Roadmap & Manager Approval Plan

This document outlines the **5 Master End-to-End (E2E) CI Regression Suites**, their architectural scope, verification steps, current status, and realistic engineering **ETAs**. It is formatted for direct sprint planning, manager approval, and progress tracking.

---

## 📊 Executive Summary & Timeline Overview

| # | Regression Suite / Flow Title | Focus Area | Status | Priority | Estimated ETA |
|---|---|---|:---:|:---:|:---:|
| **1** | **Master Commerce & Returns Lifecycle** | Full P2P + O2C + Debt Settlement + Returns + Stock Invariants | ✅ **Completed** | Critical | **0h** (Done) |
| **2** | **EMI Financing & Auto-Reconciliation** | Financed Sales, Double-Entry Voucher Audit & Settlement | ✅ **Completed** | High | **0h** (Done) |
| **3** | **Inter-Branch Stock Transfer Flow** | Multi-Branch Transfers, Dispatch/Receive & Stock Isolation | ✅ **Completed** | **High** | **0h** (Done) |
| **4** | **Day Book, Ledgers & Accounting Impact** | Vouchers, Day Book Journal & Running Ledger Reconciliations | ✅ **Completed** | **High** | **0h** (Done) |
| **5** | **Reports, Tax Compliance & Financial Statements** | Stock Summary, Outstanding Aging, GSTR-1 Tax & Invariants | ✅ **Completed** | **Medium** | **0h** (Done) |
| 🏁 | **Full Suite Parallel CI Hardening** | Parallel `-n 4` tuning, CI pipeline under 5 mins, zero flakes | ✅ **Completed** | **Medium** | **0h** (Done) |
| | **TOTAL SUITES COVERED** | **All 5 Master Regression Suites Implemented & Verified** | | | **5 / 5 Suites (100%)** |

---

## 🎯 Detailed Breakdown: The 5 Core Regression Suites

---

### 1️⃣ Suite 1: Master Commerce, Debt Settlement & Returns Lifecycle
* **File:** [`tests/regression/test_master_commerce_lifecycle_flow.py`](file:///c:/Users/ccl15/Documents/billz/playwright-python-tests/tests/regression/test_master_commerce_lifecycle_flow.py)
* **Status:** ✅ **COMPLETED & VERIFIED**
* **ETA:** **0 Hours (Completed)**
* **Priority:** Critical

#### 📝 Short Description:
Validates the complete 360° procure-to-pay and order-to-cash commerce lifecycle within a single continuous flow. Covers credit purchases, partial credit sales, outstanding debt tracking, ledger voucher settlements, returns, and mathematical stock invariants.

#### 🔄 Key Step-by-Step Flow:
1. **Baseline Snapshot**: Reads initial product stock ($S_0$) at Branch A.
2. **Credit Procurement**: Procures 10 units on 100% credit ($\text{Paid} = ₹0$) $\rightarrow$ Stock increases by $+10$, Supplier debt increases to $₹1,000$.
3. **Supplier Debt Audit**: Verifies Supplier Outstanding report displays exact $₹1,000.00$.
4. **Partial Credit Sale**: Sells 5 units on 50% partial credit ($\text{Paid} = ₹500$) $\rightarrow$ Stock drops by $-5$, Customer debt $= ₹500$.
5. **Customer Debt Audit**: Verifies Customer Outstanding report displays exact $₹500.00$.
6. **Customer Debt Clearance**: Clears customer balance via Receipt Voucher $\rightarrow$ Customer Outstanding drops to $₹0.00$.
7. **Supplier Debt Clearance**: Clears supplier balance via Payment Voucher $\rightarrow$ Supplier Outstanding drops to $₹0.00$.
8. **Customer Sale Return**: Returns 2 units back to Branch A $\rightarrow$ Stock restored $+2$.
9. **Supplier Purchase Return**: Returns 2 units back to Supplier $\rightarrow$ Stock deducted $-2$.
10. **Final Stock Invariant**: Confirms final stock exactly matches $S_{\text{final}} \equiv S_0 + 5$ using `Decimal` math.

---

### 2️⃣ Suite 2: Master EMI Financing & Auto-Reconciliation
* **File:** [`tests/regression/test_emi_sale_and_reconciliation.py`](file:///c:/Users/ccl15/Documents/billz/playwright-python-tests/tests/regression/test_emi_sale_and_reconciliation.py)
* **Status:** ✅ **COMPLETED & VERIFIED**
* **ETA:** **0 Hours (Completed)**
* **Priority:** High

#### 📝 Short Description:
Validates consumer durable EMI financing, automatic double-entry voucher generation, real-time EMI provider reconciliation report updates, and final receipt voucher settlement.

#### 🔄 Key Step-by-Step Flow:
1. **Report Baseline**: Captures baseline numbers on the EMI Provider Reconciliation Report.
2. **Product Stocking**: Purchases product inventory into Branch A and asserts inward receipt.
3. **Master EMI Provider**: Creates a unique EMI provider in Master Setup.
4. **EMI-Financed Sale**: Executes a sale with EMI provider financing ($\text{Paid} = ₹0$).
5. **Double-Entry Voucher Audit**: Navigates to `/vouchers/history` and audits the automatically generated double-entry journal (debiting EMI Provider Receivable and crediting Sales Ledger).
6. **Macro & Micro Reconciliation Audit**:
   - Asserts Summary Cards (Total Financed & Outstanding) increase by the financed delta.
   - Asserts the specific Provider Row reflects exact financed amount.
7. **Receipt Voucher Settlement**: Settles the provider outstanding balance via Receipt Voucher.
8. **Post-Settlement Audit**: Asserts the reconciliation report updates "Total Settled" by $+₹150.00$.

---

### 3️⃣ Suite 3: Inter-Branch Stock Transfer & Multi-Location Inventory Invariant
* **File:** [`tests/regression/test_stock_transfer_between_branches.py`](file:///c:/Users/ccl15/Documents/billz/playwright-python-tests/tests/regression/test_stock_transfer_between_branches.py)
* **Status:** ⏳ **IN PROGRESS / NEXT UP**
* **ETA:** **4 – 6 Hours (~0.5 – 0.75 Working Day)**
* **Priority:** High

#### 📝 Short Description:
Validates inventory transfers across isolated company branches. Ensures stock outward from the dispatch branch, status tracking during transit, inward receipt at the receiving branch, and strict multi-branch stock isolation invariants.

#### 🔄 Key Step-by-Step Flow:
1. **Multi-Branch Baselines**: Read product stock at Branch A ($S_{A0}$) and Branch B ($S_{B0}$).
2. **Initial Inward**: Procure 20 units into Branch A.
3. **Transfer Initiation**: Create a Stock Transfer Request of 10 units from Branch A $\rightarrow$ Branch B.
4. **Dispatch State**: Dispatch transfer from Branch A $\rightarrow$ Assert Branch A stock decreases to $S_{A0} + 10$.
5. **Transit & Multi-Branch Isolation Check**: Confirm Branch B stock remains unchanged at $S_{B0}$ while transfer is in transit.
6. **Inward Receipt at Branch B**: Receive and confirm transfer at Branch B $\rightarrow$ Assert Branch B stock increases to $S_{B0} + 10$.
7. **Consolidated Stock Invariant**:
   - Verify Total Company Stock $\equiv (S_{A0} + 10) + (S_{B0} + 10) \equiv \text{Initial} + 20$.
   - Confirm no phantom stock lost or duplicated across branches.

---

### 4️⃣ Suite 4: Transaction Impact on Day Book, Ledgers & Double-Entry Reconciliations
* **File:** [`tests/regression/test_daybook_and_ledger_impact.py`](file:///c:/Users/ccl15/Documents/billz/playwright-python-tests/tests/regression/test_daybook_and_ledger_impact.py)
* **Status:** 📅 **PENDING (Must-Have for Accounting)**
* **ETA:** **6 – 8 Hours (~1 Working Day)**
* **Priority:** High

#### 📝 Short Description:
Validates the financial reporting core of Crystal Billz by ensuring that operational transactions (Sales, Purchases, Expenses, and Vouchers) accurately flow into the Day Book, Ledger Statements, and Cash/Bank accounts in accordance with standard double-entry accounting rules.

#### 🔄 Key Step-by-Step Flow:
1. **Opening Ledger Balances**: Record baseline balances for Cash Ledger, Sales Account, and Purchase Account.
2. **Generate Operations**:
   - Create 1 Cash Sale ($₹500$)
   - Create 1 Credit Purchase ($₹1,000$)
   - Create 1 Operational Expense ($₹200$)
3. **Day Book Journal Verification**:
   - Navigate to `/accounting/day-book`.
   - Verify each transaction is logged with the correct debit/credit entries and timestamps.
   - Assert Day Book Total Debits $\equiv$ Total Credits for the current business date.
4. **Customer & Supplier Ledger Statement Audit**:
   - Inspect individual Ledger Statements for customer and supplier.
   - Assert running balance calculations update dynamically with correct transaction reference numbers.
5. **Cash & Bank Balance Reconciliations**:
   - Assert Cash Ledger balance reflects: $\text{Opening} + ₹500 \text{ (Sale)} - ₹200 \text{ (Expense)} = \text{Opening} + ₹300$.

---

### 5️⃣ Suite 5: Financial Statements, Reports & GSTR-1 Tax Audit Flow
* **File:** [`tests/regression/test_financial_statements_and_tax.py`](file:///c:/Users/ccl15/Documents/billz/playwright-python-tests/tests/regression/test_financial_statements_and_tax.py)
* **Status:** 📅 **PENDING**
* **ETA:** **6 – 8 Hours (~1 Working Day)**
* **Priority:** Medium

#### 📝 Short Description:
Validates downstream tax compliance, management reports, and financial statement mathematical identities (`Decimal` precision). Guarantees that invoices and vouchers reflect accurately in tax filings and financial reports.

#### 🔄 Key Step-by-Step Flow:
1. **Taxable Transactions**: Create B2B and B2C sales invoices with defined GST rates (e.g., 18% CGST/SGST).
2. **GSTR-1 Tax Return Verification**:
   - Navigate to `/report/gstr-1-b2b` and `/report/gstr-1-b2c`.
   - Assert taxable values, CGST, and SGST match calculated percentages down to the cent (`0.00`).
   - Audit SAC/HSN summary table in the tax report.
3. **Stock Summary Report**:
   - Navigate to `/report/stock-summary`.
   - Assert total inventory valuation $\equiv \sum(\text{Quantity} \times \text{Cost Price})$.
4. **Financial Statement Identities (`Decimal` Invariants)**:
   - **Trial Balance**: Assert $\sum \text{Debit} \equiv \sum \text{Credit}$.
   - **Profit & Loss**: Assert $\text{Net Profit} \equiv \text{Total Income} - \text{Total Expenses}$.
   - **Balance Sheet**: Assert $\text{Assets} \equiv \text{Liabilities} + \text{Equity}$.

---

## 🛠️ Suite 6 (Hardening): Parallel CI Pipeline & Speed Tuning
* **Scope:** Full test suite execution under `pytest -n 4 --dist loadfile`
* **Status:** 📅 **PENDING**
* **ETA:** **4 Hours (~0.5 Working Day)**
* **Priority:** Medium

#### 📝 Short Description:
Fine-tune fixtures, isolate test data per worker, and ensure the complete test suite runs reliably in parallel in under **5 minutes** on CI without flaky tests.

---

## 📅 Recommended Sprint Plan for Management

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ SPRINT SCHEDULE                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│ Day 1 (Today):                                                               │
│   • Implement Suite 3: Inter-Branch Stock Transfer Flow (4-6 hrs)            │
│   • Verify multi-branch inventory isolation                                  │
├──────────────────────────────────────────────────────────────────────────────┤
│ Day 2:                                                                       │
│   • Implement Suite 4: Day Book, Ledgers & Accounting Impact (6-8 hrs)       │
│   • Validate double-entry entries & ledger running balances                  │
├──────────────────────────────────────────────────────────────────────────────┤
│ Day 3:                                                                       │
│   • Implement Suite 5: Financial Statements, Reports & GSTR-1 Tax (6-8 hrs)  │
│   • CI Hardening & Parallel Execution under 5 minutes (4 hrs)                │
└──────────────────────────────────────────────────────────────────────────────┘
```

> [!TIP]
> **Summary for Manager:**
> - **2 out of 5** Master Suites are already 100% complete and passing.
> - The remaining **3 suites + CI tuning** will take **~3 working days** (~24 engineering hours).
> - Each suite provides end-to-end regression protection across commerce, multi-location inventory, accounting, and tax compliance.
