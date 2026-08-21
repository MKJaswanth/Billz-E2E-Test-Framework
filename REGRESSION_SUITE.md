# Cross-Module CI Regression Suite & E2E Flow Guide

This document outlines the architecture, data isolation strategy, and core End-to-End (E2E) flows for the **Crystal Billz CI Regression Suite** (`tests/regression/`).

---

## 🏗️ Architecture & Hardened Isolation Design

The CI Regression Suite is designed for deterministic, flake-free, and high-speed PR verification in both sequential and parallel (`-n 4 --dist loadfile`) CI environments.

### Key Principles:
1. **Safety Lockout Guard**: Mutation tests require `ALLOW_MUTATING_TESTS=1` and `TEST_ENV=dev|staging|local|test` in `.env`. Production/UAT hostnames are blocked automatically.
2. **Session-Scoped Immutable Master Data**: Truly static supporting entities (`City`, `Category`, `Brand`, `Unit Type`, `HSN/SAC Code`) are created once per session by `tests/regression/conftest.py`.
3. **Function-Scoped Dynamic Isolation**: Dynamic entities (`Branches`, `Suppliers`, `Customers`, `Products`) are created freshly per test flow with `worker_id` and unique run UUIDs (`regr_{worker}_{uuid}_...`). No test shares stock, financial debt, or voucher balances.
4. **Structured Results & Fail-Fast POMs**: Page Object methods return typed models (`PurchaseResult`, `SaleResult`, `VoucherResult`, `StockTransferResult`) with exact references. Swallowed errors and `.first` queries are eliminated.
5. **Exact `Decimal` Invariants**: Financial balances and stock counts are checked using exact `Decimal` equality (`==`) rather than loose substring or `>=` checks.

---

## 🎯 The Core E2E CI Regression Suites

| # | Regression Suite / Flow Title | Test File | Key Coverage & Verifications | Status |
|---|---|---|---|:---:|
| **1** | **Master Commerce & Returns Lifecycle** | [`tests/regression/test_master_commerce_lifecycle_flow.py`](file:///c:/Users/ccl15/Documents/billz/playwright-python-tests/tests/regression/test_master_commerce_lifecycle_flow.py) | Full P2P + O2C + Debt Settlement + Returns + Enterprise Stock Invariants | ✅ **Completed & Hardened** |
| **2** | **EMI Financing & Auto-Reconciliation** | [`tests/regression/test_emi_sale_and_reconciliation.py`](file:///c:/Users/ccl15/Documents/billz/playwright-python-tests/tests/regression/test_emi_sale_and_reconciliation.py) | Financed Sales, Auto 3-Way Voucher, Macro/Micro Reconciliation Report | ✅ **Completed & Hardened** |
| **3** | **Inter-Branch Stock Transfer Flow** | [`tests/regression/test_stock_transfer_between_branches.py`](file:///c:/Users/ccl15/Documents/billz/playwright-python-tests/tests/regression/test_stock_transfer_between_branches.py) | Multi-Branch Transfers, Negative Validation, In-Transit Isolation, Stock Conservation | ✅ **Completed & Hardened** |
| **4** | **Day Book, Ledgers & Accounting Impact** | [`tests/regression/test_daybook_and_ledger_impact.py`](file:///c:/Users/ccl15/Documents/billz/playwright-python-tests/tests/regression/test_daybook_and_ledger_impact.py) | Day Book DR=CR balance, Running Ledgers, Cash Account Reconciliation, Trial Balance | ✅ **Completed & Hardened** |
| **5** | **Financial Statements, Reports & GSTR-1 Tax Audit Flow** | [`tests/regression/test_financial_reports_and_gstr_flow.py`](file:///c:/Users/ccl15/Documents/billz/playwright-python-tests/tests/regression/test_financial_reports_and_gstr_flow.py) | B2B/B2C Tax Compliance, GSTR-1 Return Isolation, Stock Summary Valuation, Financial Statement Invariants, XLSX/PDF Exports | ✅ **Completed & Hardened** |

---

## ⚡ Execution Commands

### Run Full Regression Suite (Sequential)
```bash
python -m pytest tests/regression/ -v
```

### Run Parallel Execution (CI Mode — Isolated Workers)
```bash
python -m pytest tests/regression/ -n 4 --dist loadfile -v
```

### Run Specific Accounting Suite
```bash
python -m pytest tests/regression/test_daybook_and_ledger_impact.py -v
```

### Run by Markers
```bash
python -m pytest -m "regression and accounting" -v
```
