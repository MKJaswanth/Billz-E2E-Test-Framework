# Crystal Billz — Test Automation Milestones & Test Plan

This milestone sheet defines the automation plan. For each module, we must ensure coverage for: **Load (Visibility)**, **Add**, **Form Validation**, **Search**, **Edit**, **Delete & Restore**, and **Data Teardown (Cleanup)**.

---

## Phase 1 — Foundation (Auth & Core Helpers)

- [ ] `pages/common/base_page.py` — BasePage class (shared `__init__`, navigation, and common helpers)
- [x] `pages/auth/login_page.py` — LoginPage (navigate, login, toggle password)
- [x] `tests/test_auth.py` — Successful login, failed login, empty credentials, https check, password toggle

---

## Phase 2 — Dashboard

- [x] `pages/dashboard_page.py` — DashboardPage (navigate, verify widgets)
- [x] `tests/test_dashboard.py` — Dashboard loads after login, key widgets visible

---

## Phase 3 — Master Menu (Setup & Configuration)

> Write these configuration setup modules before the main menu since main menu items depend on this data.

### 1. Cities
- [x] page loads (visibility check)
- [x] add city (success flow)
- [x] search city (table filtering)
- [x] edit city (update flow)
- [x] delete & restore city (status lifecycle)
- [x] automated data teardown fixture

### 2. Branches
- [x] page loads (visibility check)
- [x] add branch (success flow)
- [x] search branch (table filtering)
- [x] edit branch (update flow)
- [x] view branch (dialog view check)
- [x] delete & restore branch (status lifecycle)
- [x] branch form validations (phone, email, required fields)
- [x] automated data teardown fixture

### 3. Roles
- [x] page loads
- [x] add role
- [x] validation (required field checks)
- [x] search role
- [x] edit role
- [x] delete & restore role
- [x] automated data teardown fixture

### 4. Users
- [x] page loads
- [x] add user
- [x] validation (email, password criteria, required fields)
- [x] search user
- [x] edit user
- [x] delete & restore user
- [x] automated data teardown fixture (with cascading branch & role cleanup)

### 5. Categories
- [x] page loads
- [x] add category
- [x] search category
- [x] edit category
- [x] delete & restore category
- [x] view category
- [x] automated data teardown fixture

### 6. Brands
- [x] page loads
- [x] add brand
- [x] search brand
- [x] edit brand
- [x] delete & restore brand
- [x] view brand
- [x] automated data teardown fixture

### 7. Unit Types
- [x] page loads
- [x] add unit type
- [x] search unit type
- [x] edit unit type
- [x] delete & restore unit type
- [x] view unit type
- [x] automated data teardown fixture

### 8. Attribute Keys, Values, & Product Attributes
- [x] page loads
- [x] add / edit / delete attribute keys
- [x] add / edit / delete attribute values
- [x] product attributes assignment & validations
- [x] automated data teardown fixtures (with cascading key cleanup)

### 9. Finance & Accounts Setup
- [x] bank accounts (add / edit / delete)
- [x] automated bank accounts data teardown fixture
- [x] account groups (add / edit / delete)
- [x] automated account groups data teardown fixture
- [x] voucher types (add / edit / delete)
- [x] automated voucher types data rollback fixture

### 10. Miscellaneous Setup
- [ ] expense categories (add / edit / delete)
- [ ] enquiry types (add / edit / delete)
- [ ] SAC / HSN codes (add / edit / delete)
- [ ] racks setup (add / edit / delete)

### 11. Enquiry Stage Workflows
- [ ] enquiry stage workflows (add / edit / delete)

---

## Phase 4 — Main Menu (Core Business Flows)

> Products must be automated before Sales & Purchases.

### 1. Products
- [ ] page loads
- [ ] add product (valid inputs, file/image upload)
- [ ] validation (name duplicate, invalid price)
- [ ] search product
- [ ] edit product
- [ ] delete & restore product

### 2. Customers & Suppliers
- [ ] add / edit / delete customer
- [ ] customer validation (phone, email)
- [ ] add / edit / delete supplier
- [ ] supplier validation (GST number, phone)

### 3. Purchases & Orders
- [ ] create purchase request
- [ ] create purchase order
- [ ] receive purchase (updates inventory)
- [ ] purchase returns

### 4. Sales & Invoicing
- [ ] create sales quote
- [ ] create sale / invoice (updates inventory)
- [ ] sale returns

### 5. Inventory & Stocks
- [ ] stock level verification after sales / purchases
- [ ] batch management (adding batch numbers, expiry dates)

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
| Phase 3 — Master Menu | 97               | 91        | 5         |
| Phase 4 — Main Menu   | 35               | 0         | 35        |
| Phase 5 — Accounting  | 15               | 0         | 15        |
| Phase 6 — Reports     | 6                | 0         | 6         |
| **Total**             | **158**          | **96**    | **62**    |
