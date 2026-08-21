# 🎯 Playwright Automation Milestones V2 (Daily Execution Roadmap)

This document defines the **Milestone V2 Roadmap** for bringing the entire `billz` Playwright Python test suite to 100% production-ready status.

All modules must be automated and verified according to the 15 mandatory standards in **[RULEBOOK.md](file:///c:/Users/ccl15/Documents/billz/playwright-python-tests/RULEBOOK.md)**:
1. **Single E2E CRUD Lifecycle Pattern** (`test_<entity>_crud_lifecycle`)
2. **Deterministic `xfail` Bug Tagging** (Zero skipped tests for active application defects)
3. **Teardown Cleanup Optimization** (`cleanup.remove(item_name)`)
4. **Soft Delete & Restore Locators** (`i.bi-trash` vs `i.bi-arrow-clockwise` with explicit wait)
5. **Two-Level Validation Assertions** (UI feedback + HTTP API `422` / `403` status)
6. **Page Object `@property` Locators**
7. **Parallel Worker Execution** (`python -m pytest ... -n 4 --dist loadfile`)
8. **Financial & Mathematical Invariants** (`Decimal`-based reconciliation)
9. **Test Data Safety & Cleanup Ownership**
10. **Deterministic Waiting & API Synchronization**
11. **Parallel-Test Data Isolation**
12. **Semantic, Scoped Locator Priority**
13. **UI, API & Persistence Verification After Edit**
14. **Failure, Retry & Diagnostic Artifact Policy**
15. **Module Completion & Tracker Synchronization**

---

## 📊 Overall Completion Tracker

```
Day 1: Master Setup Quad & RBAC       [████████████████████] 100% COMPLETED (verified 3 August 2026)
Day 2: Master Inventory & Attributes  [████████████████████] 100% COMPLETED (verified 3 August 2026)
Day 3: Financial Setup & Workflows    [████████████████████] 100% COMPLETED (verified 3 August 2026)
Day 4: Core Entity Management         [░░░░░░░░░░░░░░░░░░░░]   0% Pending
Day 5: Transactions & Stock Flow      [░░░░░░░░░░░░░░░░░░░░]   0% Pending
Day 6: Accounting Vouchers & Ledgers  [░░░░░░░░░░░░░░░░░░░░]   0% Pending
Day 7: Reports & Tax Compliance       [░░░░░░░░░░░░░░░░░░░░]   0% Pending
```

### Master Menu Regression Baseline — 3 August 2026

- **Scope:** 18 functional Master Menu modules plus RBAC (19 automation areas)
- **Execution:** 121 tests using four parallel workers with `--dist loadfile`
- **Result:** **103 passed, 18 xfailed, 0 unexpected failures**
- **Runtime:** **4 minutes 36 seconds**
- **Status:** Master Menu automation is CI-ready. The 18 deterministic `xfail` cases remain active as documented application defects and are not automation failures.

---

## 🗓️ Daily Execution Roadmap

### 🟢 DAY 1 — Master Setup Quad & RBAC Security (COMPLETED - verified 28 July 2026)
> **Goal**: Establish core foundation entities, user management, and 3-layer RBAC security verification.
> **Status**: Cities, Branches, Roles, Users, and RBAC were stabilized and verified in the current regression cycle. See the latest generated test report for execution totals.

- [x] **Cities Module** (`pages/master_menu/cities_page.py`, `tests/master_menu/test_cities.py`)
  - [x] CRUD Lifecycle (Create &rarr; Search &rarr; Edit &rarr; Delete &rarr; Restore)
  - [x] Post-edit name persistence verified by reopening Edit (View action unavailable)
  - [x] Required name & 100-char max length validation
  - [x] Duplicate city in state check (422)
  - [x] Default city selection persistence
  - [x] Numeric city name bug (`xfail`)
  - [x] Branch assignment dependency deletion bug (`xfail`)
- [x] **Branches Module** (`pages/master_menu/branches_page.py`, `tests/master_menu/test_branches.py`)
  - [x] CRUD Lifecycle (Create &rarr; Search &rarr; View &rarr; Edit &rarr; Delete &rarr; Restore)
  - [x] Required name/code/address validation
  - [x] Duplicate branch name & code checks (422)
  - [x] Format checks (postal code, phone, email)
  - [x] Post-edit persistence for name, code, address, postal code, phone, email, sort order, and retained City
  - [x] Invalid phone start digit bug (`xfail`)
- [x] **Roles Module** (`pages/master_menu/roles_page.py`, `tests/master_menu/test_roles.py`)
  - [x] CRUD Lifecycle (Create &rarr; Search &rarr; View &rarr; Edit &rarr; Delete &rarr; Restore)
  - [x] Required & duplicate role name checks (422)
  - [x] Permission toggles (Suppliers, Products)
  - [x] Post-edit name and description persistence verified in View
  - [x] Role assigned to user dependency bug (`xfail`)
- [x] **Users Module** (`pages/master_menu/users_page.py`, `tests/master_menu/test_users.py`)
  - [x] CRUD Lifecycle (Create &rarr; Search &rarr; View &rarr; Edit &rarr; Delete &rarr; Restore)
  - [x] Required fields, email format, weak password validation
  - [x] Duplicate email check (422)
  - [x] Fast React-select search typing
  - [x] Post-edit name and email persistence plus retained Branch verification
  - [x] Email without domain suffix bug (`xfail`)
- [x] **RBAC Security Module** (`tests/master_menu/test_rbac_permissions.py`)
  - [x] Layer 1: Route & Menu Authorization (Hidden links, 403 / redirect on direct URL)
  - [x] Layer 2: UI Action Button Restrictions (Add/Edit/Delete hidden/disabled)
  - [x] Layer 3: Direct API Protection (HTTP 403 Forbidden on unauthorized POST/PUT/DELETE)

---

### 🔵 DAY 2 — Master Inventory & Attributes (COMPLETED - verified 3 August 2026)
> **Goal**: Automate master inventory entities, product attributes, and tax codes.
> **Verified four-module regression (28 July 2026)**: **15 passed, 1 xfailed, 0 failed**. Parallel run with `-n 4 --dist loadfile` completed in approximately 1 minute.

- [x] **Racks Module** (`pages/master_menu/racks_page.py`, `tests/master_menu/test_racks.py`) — verified 28 July 2026
  - [x] Single `test_racks_crud_lifecycle` (Create &rarr; Search &rarr; View &rarr; Edit &rarr; Delete &rarr; Restore)
  - [x] Required Rack Name, Rack Code, and Branch validation with no invalid API submission
  - [x] Duplicate Rack UI validation and API `422` rejection
  - [x] Post-edit persistence for name, code, description, sort order, and retained Branch
  - [x] API-response synchronization and active/deleted cleanup handling
  - [x] Branch assignment dependency check
  - [x] Active Rack Branch deletion defect (`xfail`)
  - [x] Standalone and parallel verification: **3 passed, 1 xfailed, 0 failed**
- [x] **Categories Module** (`pages/master_menu/categories_page.py`, `tests/master_menu/test_categories.py`) — verified 28 July 2026
  - [x] Single `test_category_crud_lifecycle` (Create &rarr; Search &rarr; View &rarr; Edit &rarr; Delete &rarr; Restore)
  - [x] Required field validation check
  - [x] Duplicate category name validation (422)
  - [x] Post-edit name, description, and sort-order persistence
  - [x] API-response synchronization and deterministic cleanup
  - [x] Standalone verification: **3 passed, 0 failed**
- [x] **Brands Module** (`pages/master_menu/brands_page.py`, `tests/master_menu/test_brands.py`) — verified 28 July 2026
  - [x] Single `test_brand_crud_lifecycle` (Create &rarr; Search &rarr; View &rarr; Edit &rarr; Delete &rarr; Restore)
  - [x] Required field validation check
  - [x] Blank-only brand name rejection check
  - [x] Duplicate brand name validation (422)
  - [x] Post-edit name and description persistence
  - [x] API-response synchronization and deterministic cleanup
  - [x] Standalone verification: **4 passed, 0 failed**
- [x] **Unit Types Module** (`pages/master_menu/unit_types_page.py`, `tests/master_menu/test_unit_types.py`) — verified 28 July 2026
  - [x] Single `test_unit_type_crud_lifecycle` (Create &rarr; Search &rarr; View &rarr; Edit &rarr; Delete &rarr; Restore)
  - [x] Required Name, Symbol, and Description validation with no invalid API submission
  - [x] Duplicate Unit Type name UI validation and API `422` rejection
  - [x] Sort-order minimum and integer validation
  - [x] Post-edit persistence for name, symbol, description, and sort order
  - [x] API-response synchronization and active/deleted cleanup handling
  - [x] Standalone verification: **5 passed, 0 failed**
- [x] **Attribute Keys & Values Modules** (`pages/master_menu/attribute_keys_page.py`, `attribute_values_page.py`) — verified 28 July 2026
  - [x] Attribute Key single CRUD lifecycle (Create &rarr; Search &rarr; View &rarr; Edit &rarr; Delete &rarr; Restore)
  - [x] Attribute Value single CRUD lifecycle with active View dialog assertions
  - [x] React-Select dynamic key option lookup and selection
  - [x] Required-field validation without invalid network submission
  - [x] Duplicate Attribute Value UI validation and API `422` rejection
  - [x] Standalone verification: **5 passed, 0 failed**
- [x] **Product Attributes Module** (`pages/master_menu/product_attributes_page.py`, `tests/master_menu/test_product_attributes.py`) — verified 3 August 2026
  - [x] Create, search, required-name, maximum-length, and duplicate validation coverage
  - [x] Duplicate validation requires both HTTP rejection and visible UI feedback
  - [x] Action buttons availability defect (`xfail`)
- [x] **SAC / HSN Codes Module** (`pages/master_menu/sac_hsn_code_page.py`, `tests/master_menu/test_sac_hsn.py`) — verified 3 August 2026
  - [x] Single CRUD lifecycle with View, edit persistence, delete, and restore
  - [x] Required code, maximum length, sort-order minimum, and duplicate validation
  - [x] Alphabetic and too-short code defects (`xfail`)

---

### 🔵 DAY 3 — Financial Setup & Workflow Configuration (COMPLETED - verified 3 August 2026)
> **Goal**: Cover financial setup masters, expense categories, and workflow stage rules.

- [x] **Bank Accounts Module** (`pages/master_menu/bank_accounts_page.py`, `tests/master_menu/test_bank_accounts.py`) — verified 28 July 2026
  - [x] Single Bank Account CRUD lifecycle
  - [x] Post-edit persistence for name, bank branch, account number, and IFSC
  - [x] Required-field validation
  - [x] Invalid IFSC and numeric-only account-number validation
  - [x] Soft delete, restore, and owned-record cleanup
- [x] **Account Groups Module** (`pages/master_menu/account_groups_page.py`, `tests/master_menu/test_account_groups.py`) — verified 28 July 2026
  - [x] Parent and child Account Group lifecycle
  - [x] Parent relationship selection and persistence
  - [x] Post-edit name and retained-parent verification
  - [x] Required-field validation
  - [x] Owned-record cleanup in child-before-parent order
  - [x] Account Group restore defect remains active (`xfail`)
- [x] **Expense Categories** (`pages/master_menu/expense_categories_page.py`, `tests/master_menu/test_expense_categories.py`) — verified 3 August 2026
  - [x] Single CRUD lifecycle with edit persistence, delete, and restore
  - [x] Required name and duplicate rejection validation
  - [x] Unavailable View action defect (`xfail`)
- [x] **Voucher Types** (`pages/master_menu/voucher_types_page.py`, `tests/master_menu/test_voucher_types.py`) — verified 3 August 2026
  - [x] Complete editable configuration persistence with automatic rollback
  - [x] Manual numbering sets and disables reset frequency as Never
  - [x] Prefix maximum-length validation without an invalid API request
  - [x] System-owned name, slug, sort order, and last number remain read-only
- [x] **Enquiry Types & Stage Workflows** (`pages/master_menu/enquiry_types_page.py`, `enquiry_stage_workflows_page.py`) — verified 3 August 2026
  - [x] Enquiry Type CRUD lifecycle, full edit persistence, and validation
  - [x] Workflow scope visibility, uniqueness, resolution priority, and restore
  - [x] Workflow edit persistence with retained enquiry type and branch
  - [x] Stage ordering, completeness, default replacement, edit persistence, delete, and restore
  - [x] Parallel batch verification: **23 passed, 0 failed**

---

### 🔵 DAY 4 — Main Menu Core Entities (Target: Day 4)
> **Goal**: Automate primary master entities used in transactions (Products, Customers, Suppliers, Ledgers).

- [ ] **Products Module** (`pages/main_menu/products_page.py`, `tests/main_menu/test_products.py`)
  - [ ] Single `test_product_crud_lifecycle` (Category, Brand, Unit Type, SAC/HSN, Tax, Price)
  - [ ] Negative opening stock validation (MM-ADD-092)
  - [ ] Category / Unit Type / HSN assigned product deletion block (MM-ADD-091)
- [ ] **Customers Module** (`pages/main_menu/customers_page.py`, `tests/main_menu/test_customers.py`)
  - [ ] Customer CRUD lifecycle (Person vs Company types)
  - [ ] Multi-address management (Billing, Shipping, Billing with Delivery)
  - [ ] Company GST 15-char uppercase validation
  - [ ] Phone start digit (6-9), postal code, and email domain suffix validation
  - [ ] Active sale customer deletion block (MM-ADD-089)
- [ ] **Suppliers Module** (`pages/main_menu/suppliers_page.py`)
  - [ ] Supplier CRUD lifecycle
  - [ ] Phone / Email domain validation (`xfail`)
  - [ ] Active purchase supplier deletion block (MM-ADD-090)
- [ ] **Ledgers Module** (`pages/main_menu/ledgers_page.py`, `tests/main_menu/test_ledgers.py`)
  - [ ] Ledger creation & group assignment
  - [ ] Opening balance credit/debit validation

---

### 🔵 DAY 5 — Transactions & Stock Flow (Target: Day 5)
> **Goal**: Automate order processing, sales, purchases, stock adjustments, and inventory tracking.

- [ ] **Purchase Requests Module** (`pages/main_menu/purchase_request_page.py`, `tests/main_menu/test_purchase_request.py`)
  - [ ] Purchase Request CRUD lifecycle
  - [ ] Required date logic (Delivery date after request date)
  - [ ] Product & Branch deletion blocks on active PR (MM-ADD-105 / MM-ADD-106)
  - [ ] Post-GRN deletion lock
- [ ] **Purchases & Purchase Returns** (`pages/main_menu/purchases_page.py`, `test_purchases.py`, `test_purchase_returns.py`)
  - [ ] Purchase invoice creation & item line calculations
  - [ ] Purchase return processing & stock reduction
- [ ] **Sales Quotes, Sales & Sale Returns** (`pages/main_menu/sales_page.py`, `test_sales.py`, `test_sales_quotes.py`)
  - [ ] Sales Quote creation & conversion to Sale
  - [ ] Sale invoice creation & instant stock deduction
  - [ ] Sale return processing & stock restoration
- [ ] **Stock Transfers & Inventories** (`pages/main_menu/stock_transfers_page.py`, `test_inventories.py`)
  - [ ] Inter-branch stock transfer dispatch & receipt
  - [ ] Stock level reconciliation across transactions

---

### 🔵 DAY 6 — Accounting Vouchers & Statements (Target: Day 6)
> **Goal**: Validate financial vouchers, approval workflows, and accounting identities using `Decimal` math.

- [ ] **Create Voucher & Voucher History** (`pages/accounting/create_voucher_page.py`, `voucher_history_page.py`, `test_create_voucher.py`)
  - [ ] Payment, Receipt, Journal, Contra voucher creation
  - [ ] Manual Entry Payment Voucher defect automation
  - [ ] Voucher approval pipeline
- [ ] **Branch Fund Transfers** (`pages/accounting/branch_fund_transfers_page.py`, `test_branch_fund_transfers.py`)
  - [ ] Branch to Branch cash/bank fund transfer lifecycle
- [ ] **Day Book & Ledger Statements** (`pages/accounting/day_book_page.py`, `ledger_statement_page.py`, `test_day_book.py`)
  - [ ] Day Book daily transaction reconciliation
  - [ ] Ledger running balance calculations
- [ ] **Financial Statements (Decimal Mathematical Invariants)**
  - [ ] Trial Balance debit = credit identity
  - [ ] Profit & Loss statement (`Net Profit = Income - Expense`)
  - [ ] Balance Sheet identity (`Assets = Liabilities + Equity`)
  - [ ] Cash Flow statement (`Closing Cash = Opening Cash + Net Flow`)

---

### 🔵 DAY 7 — Reports, Tax & Final Suite Optimization (Target: Day 7)
> **Goal**: Verify reports, tax compliance, list filters/pagination across 18 modules, and final parallel tuning.

- [ ] **Stock Summary Report** (`pages/report/stock_summary_page.py`, `test_stock_summary.py`)
  - [ ] Quantity & valuation filter verification
- [ ] **Outstanding Reports** (`customer_outstanding_page.py`, `supplier_outstanding_page.py`, `outstanding_bills_page.py`)
  - [ ] Aging bucket calculations & bill settlement tracking
- [ ] **GSTR-1 Tax Reports (B2B & B2C)** (`gstr_1_b2b_page.py`, `gstr_1_b2c_page.py`)
  - [ ] Tax rate group aggregation & HSN summary math
- [ ] **List Filters & Pagination Engine** (18 Modules)
  - [ ] Reusable filter/pagination helpers applied across all list views
- [ ] **Final Performance & CI Pipeline Optimization**
  - [ ] Verify clean, failure-free run under `python -m pytest tests/ -n 4 --dist loadfile` under 5 minutes.

---

## 🛠️ Module Verification Checklist (Rulebook 15 Standards)

Before marking any module **[x] COMPLETED** in this milestone sheet, verify:
- [ ] Happy-path flow uses single `test_<entity>_crud_lifecycle` where applicable.
- [ ] Known app bugs are tagged `@pytest.mark.xfail(reason="Bug #...: ...")`.
- [ ] Deleted records execute `cleanup.remove(item_name)`.
- [ ] Delete and restore actions use distinct scoped icon locators.
- [ ] Page Objects use `@property` locators.
- [ ] Form validation asserts both UI message and network 422/403 status.
- [ ] Test-owned records are used for destructive operations and cleaned up.
- [ ] Fixed sleeps are absent; observable UI/API events provide synchronization.
- [ ] Test data is unique and isolated across workers.
- [ ] Locators are semantic and scoped to the correct row, modal, or form.
- [ ] Every edit is reopened and all changed fields are verified for persistence.
- [ ] Applicable accounting/report calculations use exact `Decimal` invariants.
- [ ] RBAC modules verify route/menu, UI action, and direct API security.
- [ ] Retries do not hide flaky tests and failure diagnostics remain available.
- [ ] Tracker Pass/Fail/Not Executed status matches the latest verified run.
- [ ] Tests run deterministically in parallel (`-n 4 --dist loadfile`).
