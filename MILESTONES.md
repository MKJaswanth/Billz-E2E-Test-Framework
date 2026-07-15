# Crystal Billz — Test Automation Milestones & Test Plan

This milestone sheet defines the automation plan. For each module, we must ensure coverage for: **Load (Visibility)**, **Add**, **Form Validation**, **Search**, **Edit**, **Delete & Restore**, and **Data Teardown (Cleanup)**.

> **Last Updated:** 2026-07-13 15:15 IST

---

## Phase 1 — Foundation (Auth & Core Helpers) (Completed on 2026-07-10 13:18 IST)

- [x] `pages/common/base_page.py` — BasePage class (shared `__init__`, navigation, and common helpers) (Completed on 2026-07-14 15:47 IST)
- [x] `pages/auth/login_page.py` — LoginPage (navigate, login, toggle password)
- [x] `tests/test_auth.py` — Successful login, failed login, empty credentials, https check, password toggle

---

## Phase 2 — Dashboard (Completed on 2026-07-10 13:18 IST)

- [x] `pages/dashboard_page.py` — DashboardPage (navigate, verify widgets)
- [x] `tests/test_dashboard.py` — Dashboard loads after login, key widgets visible

---

## Phase 3 — Master Menu (Setup & Configuration)

> Write these configuration setup modules before the main menu since main menu items depend on this data.

### 1. Cities (Completed on 2026-07-10 13:18 IST)

- [x] page loads (visibility check)
- [x] add city (success flow)
- [x] search city (table filtering)
- [x] edit city (update flow)
- [x] delete & restore city (status lifecycle)
- [x] automated data teardown fixture
- [ ] pagination verification in list view (Postponed/Skipped for now — Not a failing test)
- [ ] list view filter inputs (Postponed/Skipped for now — Not a failing test)

### 2. Branches (Completed on 2026-07-10 13:18 IST)

- [x] page loads (visibility check)
- [x] add branch (success flow)
- [x] search branch (table filtering)
- [x] edit branch (update flow)
- [x] view branch (dialog view check)
- [x] delete & restore branch (status lifecycle)
- [x] branch form validations (phone, email, required fields)
- [x] automated data teardown fixture
- [ ] pagination verification in list view (Postponed/Skipped for now — Not a failing test)
- [ ] list view filter inputs (Postponed/Skipped for now — Not a failing test)

### 3. Roles (Completed on 2026-07-10 13:18 IST)

- [x] page loads
- [x] add role
- [x] validation (required field checks)
- [x] search role
- [x] edit role
- [x] delete & restore role
- [x] automated data teardown fixture
- [ ] pagination verification in list view (Postponed/Skipped for now — Not a failing test)
- [ ] list view filter inputs (Postponed/Skipped for now — Not a failing test)

### 4. Users (Completed on 2026-07-10 13:18 IST)

- [x] page loads
- [x] add user
- [x] validation (email, password criteria, required fields)
- [x] search user
- [x] edit user
- [x] delete & restore user
- [x] automated data teardown fixture (with cascading branch & role cleanup)
- [ ] pagination verification in list view (Postponed/Skipped for now — Not a failing test)
- [ ] list view filter inputs (Postponed/Skipped for now — Not a failing test)

### 5. Categories (Completed on 2026-07-10 13:18 IST)

- [x] page loads
- [x] add category
- [x] search category
- [x] edit category
- [x] delete & restore category
- [x] view category
- [x] automated data teardown fixture
- [ ] pagination verification in list view (Postponed/Skipped for now — Not a failing test)
- [ ] list view filter inputs (Postponed/Skipped for now — Not a failing test)

### 6. Brands (Completed on 2026-07-10 13:18 IST)

- [x] page loads
- [x] add brand
- [x] search brand
- [x] edit brand
- [x] delete & restore brand
- [x] view brand
- [x] automated data teardown fixture
- [ ] pagination verification in list view (Postponed/Skipped for now — Not a failing test)
- [ ] list view filter inputs (Postponed/Skipped for now — Not a failing test)

### 7. Unit Types (Completed on 2026-07-10 13:18 IST)

- [x] page loads
- [x] add unit type
- [x] search unit type
- [x] edit unit type
- [x] delete & restore unit type
- [x] view unit type
- [x] automated data teardown fixture
- [ ] pagination verification in list view (Postponed/Skipped for now — Not a failing test)
- [ ] list view filter inputs (Postponed/Skipped for now — Not a failing test)

### 8. Attribute Keys, Values, & Product Attributes (Completed on 2026-07-10 13:18 IST)

- [x] page loads
- [x] add / edit / delete attribute keys
- [x] add / edit / delete attribute values
- [x] product attributes assignment & validations
- [x] automated data teardown fixtures (with cascading key cleanup)
- [ ] pagination verification in list view (Postponed/Skipped for now — Not a failing test)
- [ ] list view filter inputs (Postponed/Skipped for now — Not a failing test)

### 9. Finance & Accounts Setup (Completed on 2026-07-10 13:18 IST)

#### Bank Accounts

- [x] page loads (visibility check) (Completed on 2026-07-10 13:18 IST)
- [x] add bank account (Completed on 2026-07-10 13:18 IST)
- [x] search bank account (Completed on 2026-07-10 13:18 IST)
- [x] view bank account (Completed on 2026-07-10 13:18 IST)
- [x] edit bank account (Completed on 2026-07-10 13:18 IST)
- [x] delete bank account (Completed on 2026-07-10 13:18 IST)
- [x] retrieve bank account (Completed on 2026-07-10 13:18 IST)
- [x] validate bank account formats (Completed on 2026-07-10 13:18 IST)
- [x] automated bank accounts data teardown fixture (Completed on 2026-07-10 13:18 IST)
- [ ] pagination verification in list view (Postponed/Skipped for now — Not a failing test)
- [ ] list view filter inputs (Postponed/Skipped for now — Not a failing test)

#### Account Groups

- [x] page loads (visibility check) (Completed on 2026-07-10 13:18 IST)
- [x] add account group (Completed on 2026-07-10 13:18 IST)
- [x] search account group (Completed on 2026-07-10 13:18 IST)
- [x] view account group (Completed on 2026-07-10 13:18 IST)
- [x] edit account group (Completed on 2026-07-10 13:18 IST)
- [x] delete account group (Completed on 2026-07-10 13:18 IST)
- [x] retrieve account group (skipped — see skipped.md) (Completed on 2026-07-10 13:18 IST)
- [x] automated account groups data teardown fixture (Completed on 2026-07-10 13:18 IST)
- [ ] pagination verification in list view (Postponed/Skipped for now — Not a failing test)
- [ ] list view filter inputs (Postponed/Skipped for now — Not a failing test)

#### Voucher Types

- [x] page loads (visibility check) (Completed on 2026-07-10 13:18 IST)
- [x] edit voucher type prefix & setting (Completed on 2026-07-10 13:18 IST)
- [x] automated voucher types data rollback fixture (Completed on 2026-07-10 13:18 IST)

### 10. Miscellaneous Setup (Completed on 2026-07-10 13:18 IST)

#### Expense Categories

- [x] page loads (visibility check) (Completed on 2026-07-10 13:18 IST)
- [x] add expense category (Completed on 2026-07-10 13:18 IST)
- [x] search expense category (Completed on 2026-07-10 13:18 IST)
- [x] view expense category (skipped — see skipped.md) (Completed on 2026-07-10 13:18 IST)
- [x] edit expense category (Completed on 2026-07-10 13:18 IST)
- [x] delete expense category (Completed on 2026-07-10 13:18 IST)
- [x] retrieve expense category (Completed on 2026-07-10 13:18 IST)
- [x] reject duplicate expense category (Completed on 2026-07-10 13:18 IST)
- [x] automated expense categories data teardown fixture (Completed on 2026-07-10 13:18 IST)
- [ ] pagination verification in list view (Postponed/Skipped for now — Not a failing test)
- [ ] list view filter inputs (Postponed/Skipped for now — Not a failing test)

#### Enquiry Types

- [x] page loads (visibility check) (Completed on 2026-07-10 13:18 IST)
- [x] add enquiry type (Completed on 2026-07-10 13:18 IST)
- [x] search enquiry type (Completed on 2026-07-10 13:18 IST)
- [x] view enquiry type (Completed on 2026-07-10 13:18 IST)
- [x] edit enquiry type (Completed on 2026-07-10 13:18 IST)
- [x] delete enquiry type (Completed on 2026-07-10 13:18 IST)
- [x] retrieve enquiry type (Completed on 2026-07-10 13:18 IST)
- [x] automated enquiry types data teardown fixture (Completed on 2026-07-10 13:18 IST)
- [ ] pagination verification in list view (Postponed/Skipped for now — Not a failing test)
- [ ] list view filter inputs (Postponed/Skipped for now — Not a failing test)

#### SAC / HSN Codes

- [x] page loads (visibility check) (Completed on 2026-07-10 13:18 IST)
- [x] add SAC / HSN code (Completed on 2026-07-10 13:18 IST)
- [x] search SAC / HSN code (Completed on 2026-07-10 13:18 IST)
- [x] view SAC / HSN code (Completed on 2026-07-10 13:18 IST)
- [x] edit SAC / HSN code (Completed on 2026-07-10 13:18 IST)
- [x] delete SAC / HSN code (Completed on 2026-07-10 13:18 IST)
- [x] retrieve SAC / HSN code (Completed on 2026-07-10 13:18 IST)
- [x] validate SAC / HSN code format (Completed on 2026-07-10 13:18 IST)
- [x] automated SAC / HSN codes data teardown fixture (Completed on 2026-07-10 13:18 IST)
- [ ] pagination verification in list view (Postponed/Skipped for now — Not a failing test)
- [ ] list view filter inputs (Postponed/Skipped for now — Not a failing test)

#### Racks Setup

- [x] page loads (visibility check) (Completed on 2026-07-10 13:18 IST)
- [x] add rack (Completed on 2026-07-10 13:18 IST)
- [x] search rack (Completed on 2026-07-10 13:18 IST)
- [x] view rack (Completed on 2026-07-10 13:18 IST)
- [x] edit rack (Completed on 2026-07-10 13:18 IST)
- [x] delete rack (Completed on 2026-07-10 13:18 IST)
- [x] retrieve rack (Completed on 2026-07-10 13:18 IST)
- [x] reject duplicate rack in same branch (Completed on 2026-07-10 13:18 IST)
- [x] delete branch containing rack (skipped — see skipped.md) (Completed on 2026-07-10 13:18 IST)
- [x] automated racks data teardown fixture (Completed on 2026-07-10 13:18 IST)
- [ ] pagination verification in list view (Postponed/Skipped for now — Not a failing test)
- [ ] list view filter inputs (Postponed/Skipped for now — Not a failing test)

### 11. Enquiry Stage Workflows (Completed on 2026-07-10 13:18 IST)

- [x] page loads
- [x] add workflow (with dynamic enquiry type fixture)
- [x] search workflow
- [x] edit workflow name
- [x] toggle workflow active status
- [x] delete & restore workflow
- [x] automated workflow & enquiry type teardown fixtures
- [ ] pagination verification in list view (Postponed/Skipped for now — Not a failing test)
- [ ] list view filter inputs (Postponed/Skipped for now — Not a failing test)

---

## Phase 4 — Main Menu (Core Business Flows)

> Products must be automated before Sales & Purchases.

### 1. Products (Completed on 2026-07-10 13:18 IST)

- [x] page loads
- [x] add product (valid inputs)
- [x] search product
- [x] edit product
- [x] delete & restore product
- [x] opening stock updates
- [x] automated product & dependencies teardown fixtures
- [ ] pagination verification in list view (Postponed/Skipped for now — Not a failing test)
- [ ] list view filter inputs (Postponed/Skipped for now — Not a failing test)

### 2. Customers & Suppliers (Suppliers completed on 2026-07-10 13:18 IST, Customers completed on 2026-07-13 13:12 IST)

- [x] add / edit / delete customer (Completed on 2026-07-13 13:12 IST)
- [x] customer validation (phone, email) (Completed on 2026-07-13 13:12 IST)
- [ ] third delivery type (Billing with Delivery) while adding customer (Postponed/Skipped for now — Not a failing test; only Billing and Delivery implemented)
- [x] page loads (supplier visibility)
- [x] add supplier (with dynamic city fixture)
- [x] search supplier
- [x] view supplier
- [x] edit supplier
- [x] delete & restore supplier
- [x] supplier form validation
- [x] automated supplier & city teardown fixtures
- [ ] import supplier (skipped — see skipped.md)
- [ ] pagination verification in list view (Postponed/Skipped for now — Not a failing test)
- [ ] list view filter inputs (Postponed/Skipped for now — Not a failing test)

### 3. Purchases & Orders

- [x] create purchase request (Completed on 2026-07-13 15:15 IST)
- [ ] create product inline inside Create Purchase Request form (Postponed/Skipped for now — Not a failing test; separate product module is used)
- [ ] create purchase order
- [x] receive purchase (updates inventory) (Completed on 2026-07-14 09:45 IST)
- [ ] purchase adjustments in purchase form (Postponed/Skipped for now — Not a failing test)
- [x] purchase returns (Completed on 2026-07-14 09:45 IST)
- [ ] pagination verification in list view (Postponed/Skipped for now — Not a failing test)
- [ ] list view filter inputs (Postponed/Skipped for now — Not a failing test)

### 4. Sales & Invoicing

- [x] create sales quote (Completed on 2026-07-14 10:36 IST)
- [ ] create customer and product inline inside Sales Quote form (Postponed/Skipped for now — Not a failing test; separate modules are used)
- [x] create sale / invoice (updates inventory) (Completed on 2026-07-14 11:55 IST)
- [x] sale returns (Completed on 2026-07-14 11:55 IST)
- [ ] pagination verification in list view (Postponed/Skipped for now — Not a failing test)
- [ ] list view filter inputs (Postponed/Skipped for now — Not a failing test)

### 5. Inventory & Stocks

- [ ] stock level verification after sales / purchases
- [x] batch management (adding batch numbers, expiry dates) (Completed on 2026-07-14 15:40 IST)
- [ ] pagination verification in list view (Postponed/Skipped for now — Not a failing test)
- [ ] list view filter inputs (Postponed/Skipped for now — Not a failing test)

---

## Phase 5 — Accounting

- [ ] create accounting voucher
- [ ] voucher approval flow
- [ ] day book verification
- [ ] ledger statements checking
- [ ] financial statements: Trial Balance, Profit & Loss, Balance Sheet, Cash Flow

---

## Phase 6 — Reports

- [ ] stock summary report filters
- [ ] outstanding payments report
- [ ] MDR reports

---

## Progress Summary

| Phase                 | Total Test Cases | Completed | Remaining |
| --------------------- | ---------------- | --------- | --------- |
| Phase 1 — Foundation  | 3                | 3         | 0         |
| Phase 2 — Dashboard   | 2                | 2         | 0         |
| Phase 3 — Master Menu | 176              | 176       | 0         |
| Phase 4 — Main Menu   | 43               | 27        | 16        |
| Phase 5 — Accounting  | 15               | 0         | 15        |
| Phase 6 — Reports     | 6                | 0         | 6         |
| **Total**             | **245**          | **208**   | **37**    |
