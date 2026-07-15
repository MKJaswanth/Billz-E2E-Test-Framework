# Crystal Billz — Complete User Flow & Module Continuity Map

> This document traces the **end-to-end user journey** through Crystal Billz, showing how data flows between modules and where each test/page object fits. It is designed so that automation tests can be executed in this exact order with full data continuity (each step feeds the next).

---

## How to Read This Document

- **Bold items** = modules with existing test/page coverage
- Each step shows what data it **requires** (input from prior steps) and what it **produces** (output for later steps)
- The `→` arrow shows data flow between modules
- `[page: xxx_page.py]` and `[test: test_xxx.py]` reference the automation files

---

## Flow Overview (Dependency Graph)

```
LOGIN
  │
  ▼
DASHBOARD
  │
  ▼
┌─────────────────────── MASTER MENU (Setup - do first) ───────────────────────┐
│                                                                               │
│  Cities ──→ Branches ──→ Racks                                                │
│               │                                                               │
│               ▼                                                               │
│  Roles ───→ Users                                                             │
│                                                                               │
│  Categories ─┐                                                                │
│  Brands ─────┤                                                                │
│  Unit Types ─┼──→ Products                                                    │
│  SAC/HSN ────┘      │                                                         │
│                     │                                                         │
│  Attribute Keys ──→ Attribute Values ──→ Product Attributes                   │
│                                                                               │
│  Bank Accounts ──→ Vouchers / Payments                                        │
│  Account Groups ──→ Ledgers / Financial Reports                               │
│  Voucher Types ──→ Voucher Creation                                           │
│  Expense Categories ──→ Expenses                                              │
│  Enquiry Types ──→ Enquiry Stage Workflows ──→ Enquiries                      │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────── MAIN MENU (Daily Operations) ─────────────────────────┐
│                                                                               │
│  Products + Suppliers + Branches ──→ Purchase Requests ──→ Purchases          │
│                                                              │                │
│                                                              ├──→ Batches     │
│                                                              ├──→ Inventories │
│                                                              └──→ Purchase Returns │
│                                                                               │
│  Products + Customers + Branches ──→ Sales Quotes ──→ Sales/Orders            │
│                                                          │                    │
│                                                          ├──→ Sale Returns    │
│                                                          └──→ Payments        │
│                                                                               │
│  Expense Categories + Branches ──→ Expenses                                   │
│  Account Groups + Customers/Suppliers ──→ Ledgers                             │
│  Enquiry Workflows + Customers ──→ Enquiries                                  │
│  Customers + Bank Accounts ──→ Chits                                          │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────── ACCOUNTING ───────────────────────────────────────────┐
│                                                                               │
│  Bank Accounts + Customers/Suppliers ──→ Receipt Voucher                      │
│  Bank Accounts + Customers/Suppliers ──→ Payment Voucher                      │
│  Bank Accounts ──→ Contra Voucher                                             │
│  Account Groups ──→ Journal Voucher                                           │
│  Chits + Bank Accounts ──→ Chit Entry Voucher                                 │
│  Bank Accounts ──→ MDR Settlement Voucher                                     │
│                                                                               │
│  Branch Fund Transfers (between branch bank accounts)                         │
│  Day Book (aggregates all vouchers for a date)                                │
│  P&L, Trial Balance, Balance Sheet, Cash Flow, Ledger Statement               │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────── REPORTS ──────────────────────────────────────────────┐
│                                                                               │
│  Outstanding Bills (unpaid sale/purchase invoices)                             │
│  Customer Outstanding / Supplier Outstanding                                  │
│  MDR Report (merchant discount rate tracking)                                 │
│  Stock Summary (current inventory levels across branches)                     │
│  GSTR-1 B2B / GSTR-1 B2C (GST tax filing reports)                            │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘
```

---


## Phase 1 — Authentication & Dashboard

### Step 1.1: Login

| | |
|---|---|
| **Route** | `/login` |
| **Page Object** | `pages/auth/login_page.py` → `LoginPage` |
| **Test File** | `tests/test_auth.py` |
| **Requires** | Valid admin email + password (from `.env`) |
| **Produces** | Authenticated session (`auth_state.json`) used by ALL subsequent tests |

**User Action:** Admin opens the app URL → sees login form → enters email + password → clicks "Login" → redirected to Dashboard.

**Continuity:** The `auth_state` fixture in `conftest.py` runs this flow ONCE per test session. All other test fixtures (`logged_in_page`, `module_page`) inherit the session cookie from this step.

---

### Step 1.2: Dashboard

| | |
|---|---|
| **Route** | `/dashboard` |
| **Page Object** | `pages/dashboard_page.py` → `DashboardPage` |
| **Test File** | `tests/test_dashboard.py` |
| **Requires** | Authenticated session from Step 1.1 |
| **Produces** | Confirmation that the app is operational (heading visible, widgets loaded) |

**User Action:** After login, user lands on the Dashboard showing summary widgets (total sales, purchases, top products, monthly revenue, pending payments).

**Continuity:** Dashboard is the home base. All sidebar navigation departs from here.

---


## Phase 2 — Master Menu: Foundation Setup

> These are the first modules a business admin configures. They provide the building blocks for everything else.

### Step 2.1: Cities

| | |
|---|---|
| **Route** | `/cities` |
| **Page Object** | `pages/master_menu/cities_page.py` → `CitiesPage` |
| **Test File** | `tests/master_menu/test_cities.py` |
| **Requires** | Nothing (standalone master) |
| **Produces** | City records used by **Branches**, **Suppliers**, **Customers** |

**User Action:** Admin navigates to Master Menu → Cities → clicks "Add City" → enters city name (e.g., "Chennai") → saves. Can also search, edit, delete, and restore cities.

**Data Produced:** `city_id` + `city_name` — referenced as a dropdown option when creating Branches, Supplier addresses, and Customer addresses.

---

### Step 2.2: Branches

| | |
|---|---|
| **Route** | `/branches` |
| **Page Object** | `pages/master_menu/branches_page.py` → `BranchesPage` |
| **Test File** | `tests/master_menu/test_branches.py` |
| **Requires** | At least 1 City from Step 2.1 |
| **Produces** | Branch records used by **Products (stock)**, **Purchases**, **Sales**, **Racks**, **Users**, **Expenses**, **Stock Transfers** |

**User Action:** Admin navigates to Master Menu → Branches → clicks "Add Branch" → fills name, code, address, selects State ("Tamil Nadu"), selects City (from Step 2.1), enters postal code, phone, email, and invoice copies → saves.

**Data Produced:** `branch_id` + `branch_name` — appears as dropdown in Purchase forms, Sale forms, Product opening stock, Expense forms, and Stock Transfer forms.

**Why Cities First:** The Branch form's City dropdown is populated from the Cities master. Without a city, the branch form cannot be completed.

---

### Step 2.3: Roles

| | |
|---|---|
| **Route** | `/roles` |
| **Page Object** | `pages/master_menu/roles_page.py` → `RolesPage` |
| **Test File** | `tests/master_menu/test_roles.py` |
| **Requires** | Nothing (standalone master) |
| **Produces** | Role records used by **Users** |

**User Action:** Admin navigates to Master Menu → Roles → clicks "Add Role" → enters role name (e.g., "Store Manager") → optionally assigns permissions → saves.

**Data Produced:** `role_id` + `role_name` — required dropdown when creating Users.

---

### Step 2.4: Users

| | |
|---|---|
| **Route** | `/users` |
| **Page Object** | `pages/master_menu/users_page.py` → `UsersPage` |
| **Test File** | `tests/master_menu/test_users.py` |
| **Requires** | At least 1 Role (Step 2.3) + at least 1 Branch (Step 2.2) |
| **Produces** | User accounts (can later appear as "Salesperson" in Sales forms) |

**User Action:** Admin navigates to Master Menu → Users → clicks "Add User" → enters name, email, password → selects Branch(es) from multi-select (from Step 2.2) → selects Role (from Step 2.3) → saves.

**Data Produced:** `user_id` + `user_name` — appears as "Salesperson" dropdown in Sales and Enquiry forms.

**Why Roles + Branches First:** The User form requires picking both a role and branch assignments. Without them, the react-select dropdowns are empty.

---


## Phase 3 — Master Menu: Product Foundation

> These modules define the product catalog structure. All must exist before creating a Product.

### Step 3.1: Categories

| | |
|---|---|
| **Route** | `/categories` |
| **Page Object** | `pages/master_menu/categories_page.py` → `CategoriesPage` |
| **Test File** | `tests/master_menu/test_categories.py` |
| **Requires** | Nothing |
| **Produces** | Category records for **Products** |

**User Action:** Admin → Master Menu → Categories → "Add Category" → enters name + description → saves.

**Data Produced:** `category_id` + `category_name` — required dropdown in the Product creation form.

---

### Step 3.2: Brands

| | |
|---|---|
| **Route** | `/brands` |
| **Page Object** | `pages/master_menu/brands_page.py` → `BrandPage` |
| **Test File** | `tests/master_menu/test_brands.py` |
| **Requires** | Nothing |
| **Produces** | Brand records for **Products** |

**User Action:** Admin → Master Menu → Brands → "Add Brand" → enters name + description → saves.

**Data Produced:** `brand_id` + `brand_name` — required dropdown in the Product creation form.

---

### Step 3.3: Unit Types

| | |
|---|---|
| **Route** | `/unit-types` |
| **Page Object** | `pages/master_menu/unit_types_page.py` → `UnitTypesPage` |
| **Test File** | `tests/master_menu/test_unit_types.py` |
| **Requires** | Nothing |
| **Produces** | Unit type records for **Products** (e.g., "pcs", "kg", "box") |

**User Action:** Admin → Master Menu → Unit Types → "Add Unit Type" → enters name + unit abbreviation + description → saves.

**Data Produced:** `unit_type_id` + `unit_name` — required dropdown in the Product creation form.

---

### Step 3.4: SAC/HSN Codes

| | |
|---|---|
| **Route** | `/gst-codes` |
| **Page Object** | `pages/master_menu/sac_hsn_page.py` → `SacHsnPage` |
| **Test File** | `tests/master_menu/test_sac_hsn.py` |
| **Requires** | Nothing |
| **Produces** | GST tax codes for **Products** (determines tax rate on invoices) |

**User Action:** Admin → Master Menu → SAC/HSN → "Add Code" → selects type (SAC or HSN) → enters numeric code + description → saves.

**Data Produced:** `gst_code_id` + `code` — required dropdown in the Product form. The HSN/SAC code determines what GST percentage applies to the product.

---

### Step 3.5: Attribute Keys

| | |
|---|---|
| **Route** | `/attribute-keys` |
| **Page Object** | `pages/master_menu/attribute_keys_page.py` → `AttributeKeysPage` |
| **Test File** | `tests/master_menu/test_attribute_keys.py` |
| **Requires** | Nothing |
| **Produces** | Attribute key definitions for **Attribute Values** (e.g., "Color", "Size") |

**User Action:** Admin → Master Menu → Attribute Keys → "Add Attribute Key" → enters key name → saves.

**Data Produced:** `attribute_key_id` + `key_name` — referenced when creating Attribute Values.

---

### Step 3.6: Attribute Values

| | |
|---|---|
| **Route** | `/attribute-values` |
| **Page Object** | `pages/master_menu/attribute_values_page.py` → `AttributeValuesPage` |
| **Test File** | `tests/master_menu/test_attribute_values.py` |
| **Requires** | At least 1 Attribute Key (Step 3.5) |
| **Produces** | Concrete values for keys (e.g., Key="Color" → Values="Red","Blue","Green") |

**User Action:** Admin → Master Menu → Attribute Values → "Add Attribute Value" → selects Attribute Key (from Step 3.5) → enters value name → saves.

**Data Produced:** `attribute_value_id` + `value_name` — used in Product Attributes assignments.

---

### Step 3.7: Product Attributes

| | |
|---|---|
| **Route** | `/product-unit-attributes` |
| **Page Object** | `pages/master_menu/product_attributes_page.py` → `ProductAttributesPage` |
| **Test File** | `tests/master_menu/test_product_attributes.py` |
| **Requires** | Attribute Keys (3.5) + Attribute Values (3.6) + Unit Types (3.3) |
| **Produces** | Product variant definitions (links a product's unit type to specific attribute combinations) |

**User Action:** Admin → Master Menu → Product Attributes → "Add Product Attribute" → selects Unit Type → selects Attribute Key → selects applicable Values → saves.

**Data Produced:** Variant matrix that enables SKU-level inventory tracking (e.g., "T-Shirt / pcs → Color: Red, Size: M").

---


## Phase 4 — Master Menu: Finance & Miscellaneous Setup

### Step 4.1: Bank Accounts

| | |
|---|---|
| **Route** | `/bank-accounts` |
| **Page Object** | `pages/master_menu/bank_accounts_page.py` → `BankAccountPage` |
| **Test File** | `tests/master_menu/test_bank_accounts.py` |
| **Requires** | At least 1 Branch (Step 2.2) |
| **Produces** | Bank account records for **Sales (payment method)**, **Purchases (payment)**, **Vouchers**, **Branch Fund Transfers** |

**User Action:** Admin → Master Menu → Bank Accounts → "Add Bank Account" → enters bank name, selects branch, enters account number + IFSC code → saves.

**Data Produced:** `bank_account_id` + `bank_name` — appears as payment method in Sale/Purchase forms ("Bank Account" type) and as debit/credit account in Voucher forms.

**Why This Matters:** When a Sale or Purchase is marked as "paid via bank", the amount is credited/debited to this bank account's balance. Voucher forms (Receipt, Payment, Contra) also reference these accounts.

---

### Step 4.2: Account Groups

| | |
|---|---|
| **Route** | `/account-groups` |
| **Page Object** | `pages/master_menu/account_groups_page.py` → `AccountGroupsPage` |
| **Test File** | `tests/master_menu/test_account_groups.py` |
| **Requires** | Nothing (has built-in parent groups) |
| **Produces** | Accounting hierarchy for **Ledgers**, **Trial Balance**, **Balance Sheet**, **P&L** |

**User Action:** Admin → Master Menu → Account Groups → "Add Account Group" → enters name, selects parent group (e.g., "Current Assets" under "Assets") → saves.

**Data Produced:** `account_group_id` + tree structure — defines the chart of accounts hierarchy used in all financial reports.

---

### Step 4.3: Voucher Types

| | |
|---|---|
| **Route** | `/voucher-types` |
| **Page Object** | `pages/master_menu/voucher_types_page.py` → `VoucherTypesPage` |
| **Test File** | `tests/master_menu/test_voucher_types.py` |
| **Requires** | Nothing (seeded by the system) |
| **Produces** | Voucher type configuration (prefix, numbering mode) for **Accounting Vouchers** |

**User Action:** Admin → Master Menu → Voucher Types → clicks "Edit" on a seeded type (Receipt, Payment, Contra, Journal) → updates prefix or auto/manual numbering → saves.

**Note:** Voucher types are pre-seeded. Tests only edit existing records, not create new ones. The prefix setting determines invoice number format (e.g., "RCV-001").

---

### Step 4.4: Expense Categories

| | |
|---|---|
| **Route** | `/expense-categories` |
| **Page Object** | `pages/master_menu/expense_categories_page.py` → `ExpenseCategoriesPage` |
| **Test File** | `tests/master_menu/test_expense_categories.py` |
| **Requires** | Nothing |
| **Produces** | Expense category records for **Expenses** module |

**User Action:** Admin → Master Menu → Expense Categories → "Add Expense Category" → enters name + description → saves.

**Data Produced:** `expense_category_id` + `name` — required dropdown when recording an Expense.

---

### Step 4.5: Racks

| | |
|---|---|
| **Route** | `/racks` |
| **Page Object** | `pages/master_menu/racks_page.py` → `RacksPage` |
| **Test File** | `tests/master_menu/test_racks.py` |
| **Requires** | At least 1 Branch (Step 2.2) |
| **Produces** | Storage location records for product organization |

**User Action:** Admin → Master Menu → Racks → "Add Rack" → enters rack name + selects Branch → saves.

**Data Produced:** `rack_id` + `rack_name` — optional field in product/inventory management for physical location tracking.

---

### Step 4.6: Enquiry Types

| | |
|---|---|
| **Route** | `/enquiry-types` |
| **Page Object** | `pages/master_menu/enquiry_types_page.py` → `EnquiryTypesPage` |
| **Test File** | `tests/master_menu/test_enquiry_types.py` |
| **Requires** | Nothing |
| **Produces** | Enquiry type records for **Enquiry Stage Workflows** |

**User Action:** Admin → Master Menu → Enquiry Types → "Add Enquiry Type" → enters name → saves.

**Data Produced:** `enquiry_type_id` + `name` — required when creating Enquiry Stage Workflows.

---

### Step 4.7: Enquiry Stage Workflows

| | |
|---|---|
| **Route** | `/enquiry-stage-workflows` |
| **Page Object** | `pages/master_menu/enquiry_stage_workflows_page.py` → `EnquiryStageWorkflowsPage` |
| **Test File** | `tests/master_menu/test_enquiry_stage_workflows.py` |
| **Requires** | At least 1 Enquiry Type (Step 4.6) |
| **Produces** | Workflow pipelines for **Enquiries** (defines stages like "New → Contacted → Qualified → Won/Lost") |

**User Action:** Admin → Master Menu → Enquiry Stage Workflows → "Add Workflow" → enters name, selects Enquiry Type, marks active → saves. Then adds Stages within the workflow.

**Data Produced:** `workflow_id` + stages — determines the pipeline view and stage transitions available in the Enquiry module.

---


## Phase 5 — Main Menu: Core Business Entities

> Now that all masters are configured, the business creates the core data it operates on daily.

### Step 5.1: Products

| | |
|---|---|
| **Route** | `/products` |
| **Page Object** | `pages/main_menu/products_page.py` → `ProductsPage` |
| **Test File** | `tests/main_menu/test_products.py` |
| **Requires** | Category (3.1) + Brand (3.2) + Unit Type (3.3) + SAC/HSN Code (3.4) |
| **Produces** | Product records for **Purchases**, **Sales**, **Sales Quotes**, **Purchase Requests**, **Inventories**, **Batches** |

**User Action:** User → Main Menu → Products → "Add Product" → enters product name → selects Brand, Category, HSN Code, Unit Type → enters cost price, selling price, GST% → saves.

**After creation — Opening Stock:** User navigates back to the product → clicks "Opening Stock" → selects Branch (Step 2.2) → enters quantity + cost price → saves. This is REQUIRED before the product can be sold (stock must exist).

**Data Produced:** `product_id` + `product_name` + pricing + stock levels per branch. Referenced in every transactional form.

**Why All Masters First:** The product form has 4 mandatory react-select dropdowns (Brand, Category, HSN, Unit Type). If any master is missing, the form cannot be submitted.

---

### Step 5.2: Suppliers

| | |
|---|---|
| **Route** | `/suppliers` |
| **Page Object** | `pages/main_menu/suppliers_page.py` → `SuppliersPage` |
| **Test File** | `tests/main_menu/test_suppliers.py` |
| **Requires** | At least 1 City (Step 2.1) |
| **Produces** | Supplier records for **Purchases**, **Purchase Requests**, **Purchase Returns**, **Supplier Outstanding Report** |

**User Action:** User → Main Menu → Suppliers → "Add Supplier" → enters name, contact person, email, phone, GST number → selects State + City (from Step 2.1) → enters postal code + address → saves.

**Data Produced:** `supplier_id` + `supplier_name` — required dropdown in Purchase and Purchase Request forms.

---

### Step 5.3: Customers

| | |
|---|---|
| **Route** | `/customers` |
| **Page Object** | `pages/main_menu/customers_page.py` → `CustomersPage` |
| **Test File** | `tests/main_menu/test_customers.py` |
| **Requires** | At least 1 City (Step 2.1) |
| **Produces** | Customer records for **Sales**, **Sales Quotes**, **Sale Returns**, **Enquiries**, **Chits**, **Customer Outstanding Report**, **Receipt Vouchers** |

**User Action:** User → Main Menu → Customers → "Add Customer" → selects type (Person/Company) → enters name, email, phone → adds address (contact person, address lines, State, City from Step 2.1, postal code) → marks as default → saves.

**Data Produced:** `customer_id` + `customer_name` + addresses — required in Sales forms. The address appears as "Billing Address" dropdown in the Sale form.

**Why City First:** Customer address requires State → City dropdown cascade. The City list is populated from the Cities master.

---


## Phase 6 — Main Menu: Purchase Flow (Procurement Cycle)

> This is the buy-side of the business. Products flow IN through this cycle.

### Step 6.1: Purchase Requests

| | |
|---|---|
| **Route** | `/purchase-requests` (list) / `/purchase-requests/add` (form) |
| **Page Object** | `pages/main_menu/purchase_request_page.py` → `PurchaseRequestPage` |
| **Test File** | `tests/main_menu/test_purchase_request.py` |
| **Requires** | Product (5.1) + Supplier (5.2) + Branch (2.2) |
| **Produces** | Purchase request document (can be converted to a Purchase later) |

**User Action:** User → Main Menu → Purchase Request → enters request details → selects Supplier, Branch → adds product line items (product name, quantity, price) → saves.

**Data Produced:** Purchase Request with status "Pending" → can be approved and converted into an actual Purchase. Also supports PDF download for sending to supplier.

**Continuity from prior steps:**
- Supplier dropdown ← Step 5.2
- Branch dropdown ← Step 2.2
- Product dropdown in line items ← Step 5.1

---

### Step 6.2: Purchases (Receive Goods)

| | |
|---|---|
| **Route** | `/purchases/add` (form) / `/purchases` (list) |
| **Page Object** | `pages/main_menu/purchases_page.py` → `PurchasesPage` |
| **Test File** | `tests/main_menu/test_purchases.py` |
| **Requires** | Product (5.1) + Supplier (5.2) + Branch (2.2) + optionally Bank Account (4.1) |
| **Produces** | Purchase records → **automatically increases product stock** → creates **Batches** → feeds **Purchase Returns**, **Inventories**, **Day Book**, **Supplier Outstanding** |

**User Action:** User → Main Menu → Purchases → "Add Purchase" → selects Supplier → selects Branch → enters reference number → adds product line items (product, quantity, price) → enters paid amount → if paying, selects payment type (Cash / Bank Account from Step 4.1) → clicks "Create".

**What happens on save:**
1. Product stock in the selected Branch **increases** by the purchased quantity
2. A **Batch** record is automatically created (linking the products to this purchase for traceability)
3. If `paid_amount < total`, the difference becomes **Supplier Outstanding** (an unpaid liability)
4. The purchase appears in the **Day Book** and affects **P&L** as cost of goods

**Continuity:**
- Supplier dropdown ← Step 5.2
- Branch dropdown ← Step 2.2
- Product line items ← Step 5.1
- Bank Account (if paid) ← Step 4.1 (credits from the bank balance)
- Stock increase → visible in Inventories (Step 7.2) and Batches (Step 6.4)

---

### Step 6.3: Purchase Returns

| | |
|---|---|
| **Route** | `/purchases/return/:id` (form) / `/purchase-returns` (list) |
| **Page Object** | `pages/main_menu/purchase_returns_page.py` → `PurchaseReturnsPage` |
| **Test File** | `tests/main_menu/test_purchase_returns.py` |
| **Requires** | An existing Purchase (Step 6.2) with returnable items |
| **Produces** | Return record → **decreases product stock** → adjusts Supplier Outstanding |

**User Action:** User navigates to the Purchases list → finds the purchase → clicks "Purchase Return" action → enters return quantity → clicks "Return".

**What happens on save:**
1. Product stock **decreases** by the returned quantity
2. Supplier Outstanding is adjusted (reduces liability if the purchase was on credit)
3. The return appears in the Purchase Returns list with full traceability

**Continuity:** This step is ONLY possible after a Purchase exists. The return form pre-fills supplier, branch, and product details from the original purchase.

---

### Step 6.4: Batches

| | |
|---|---|
| **Route** | `/batches` |
| **Page Object** | `pages/main_menu/batches_page.py` → `BatchesPage` |
| **Test File** | `tests/main_menu/test_batches.py` |
| **Requires** | At least 1 completed Purchase (Step 6.2) |
| **Produces** | Batch traceability records (which purchase brought which products, with remaining/sold quantities) |

**User Action:** User → Main Menu → Batches → searches for a product → sees batch rows showing "Available / Total" quantities → clicks to open traceability drawer showing the full history.

**What happens automatically:** Every Purchase creates a batch entry. As Sales consume stock, the batch's "available" quantity decreases. This provides full FIFO traceability.

**Continuity:**
- Batches are READ-ONLY from user perspective — they're auto-created by Purchases
- Each batch row links back to its source Purchase
- The "10 / 10" display means 10 available out of 10 purchased (none sold yet)

---


## Phase 7 — Main Menu: Sales Flow (Revenue Cycle)

> This is the sell-side. Products flow OUT through this cycle. Stock must exist (from Purchases) before selling.

### Step 7.1: Sales Quotes

| | |
|---|---|
| **Route** | `/sales-quotes/add` (form) / `/sales-quotes` (list) |
| **Page Object** | `pages/main_menu/sales_quotes_page.py` → `SalesQuotesPage` |
| **Test File** | `tests/main_menu/test_sales_quotes.py` |
| **Requires** | Product (5.1) + Customer (5.3) + Branch (2.2) |
| **Produces** | Quotation document (can be converted to a Sale later) |

**User Action:** User → Main Menu → Sales Quotes → "Add Sales Quote" → selects Customer → selects Branch → adds product line items (product, quantity, price) → saves.

**Data Produced:** Quote with status "Open" → can be sent to customer as PDF. Can later be converted to a confirmed Sale/Order.

**Continuity:**
- Customer dropdown ← Step 5.3
- Branch dropdown ← Step 2.2
- Product line items ← Step 5.1 (must have stock via Purchase in Step 6.2)

---

### Step 7.2: Sales / Orders (Create Invoice)

| | |
|---|---|
| **Route** | `/sales/add` (form) / `/sales` (list) |
| **Page Object** | `pages/main_menu/sales_page.py` → `SalesPage` |
| **Test File** | `tests/main_menu/test_sales.py` |
| **Requires** | Product with stock (5.1 + 6.2) + Customer (5.3) + Branch (2.2) + optionally Bank Account (4.1) |
| **Produces** | Sale invoice → **decreases product stock** → creates **Customer Outstanding** → generates downloadable invoice PDF → feeds **Sale Returns**, **Day Book**, **P&L**, **GSTR-1** |

**User Action:** User → Main Menu → Orders → "Add Sale" → selects Customer → selects Branch → optionally selects Salesperson (User from Step 2.4) → selects Billing Address (from customer's saved addresses) → adds product line items → enters price → enters paid amount → selects Sale Type (Cash / Bank Account) → if bank, selects specific bank account (Step 4.1) → clicks "Create".

**What happens on save:**
1. Product stock in the selected Branch **decreases** by sold quantity
2. If `paid_amount < total`, difference becomes **Customer Outstanding** (receivable)
3. If paid via bank, the bank account balance **increases** by paid_amount
4. The sale appears in **Day Book**, contributes to **P&L** revenue, and is included in **GSTR-1** reports
5. Invoice PDF becomes downloadable from the sales list

**Continuity:**
- Customer dropdown ← Step 5.3 (customer's address becomes billing address)
- Branch dropdown ← Step 2.2
- Product line items ← Step 5.1 (must have opening stock or purchased stock)
- Salesperson dropdown ← Step 2.4 (Users)
- Bank Account ← Step 4.1 (for bank payments)
- Stock deduction → reflected in Inventories and Batches

---

### Step 7.3: Sale Returns

| | |
|---|---|
| **Route** | `/sales/return/:id` (form) / `/sale-returns` (list) |
| **Page Object** | `pages/main_menu/sale_returns_page.py` → `SaleReturnsPage` |
| **Test File** | `tests/main_menu/test_sale_returns.py` |
| **Requires** | An existing Sale (Step 7.2) with returnable items |
| **Produces** | Return record → **increases product stock** → adjusts Customer Outstanding |

**User Action:** User navigates to Sales list → finds the sale → clicks "Sale Return" action → enters return quantity → clicks "Return".

**What happens on save:**
1. Product stock **increases** by returned quantity (goods come back)
2. Customer Outstanding is reduced (refund or credit note)
3. The return appears in the Sale Returns list with PDF download

**Continuity:** Only possible after a Sale. The form pre-fills customer, branch, product details from the original sale.

---

### Step 7.4: Inventories

| | |
|---|---|
| **Route** | `/inventories` |
| **Page Object** | `pages/main_menu/inventories_page.py` (stub) |
| **Test File** | `tests/main_menu/test_inventories.py` (empty) |
| **Requires** | Products with stock movements (Purchases increase, Sales decrease) |
| **Produces** | Real-time stock levels per product per branch |

**User Action:** User → Main Menu → Inventories → sees a card/list view of all products with current stock quantities, filterable by branch and category.

**What it shows:**
- Current available quantity per product per branch
- Cost value and selling value of stock
- Unit attribute breakdowns (if product has variants like Color/Size)

**Continuity:** This is a READ view — stock levels are the NET result of:
- Opening Stock (Step 5.1) + Purchases (Step 6.2) − Sales (Step 7.2) − Purchase Returns (Step 6.3) + Sale Returns (Step 7.3)

---


## Phase 8 — Main Menu: Supporting Modules

### Step 8.1: Expenses

| | |
|---|---|
| **Route** | `/expenses` |
| **Page Object** | `pages/main_menu/expenses_page.py` (stub) |
| **Test File** | `tests/main_menu/test_expenses.py` (empty) |
| **Requires** | Expense Category (Step 4.4) + Branch (Step 2.2) + optionally Bank Account (4.1) |
| **Produces** | Expense records → feeds **Day Book**, **P&L** (reduces profit) |

**User Action:** User → Main Menu → Expenses → "Add Expense" → selects Expense Category (from Step 4.4) → selects Branch → enters amount, date, description → selects payment method (Cash/Bank) → saves.

**Continuity:**
- Expense Category dropdown ← Step 4.4
- Branch dropdown ← Step 2.2
- Bank Account (if paid by bank) ← Step 4.1
- Expense totals reduce profit in P&L report

---

### Step 8.2: Payments

| | |
|---|---|
| **Route** | `/payments` |
| **Page Object** | `pages/main_menu/payments_page.py` (stub) |
| **Test File** | `tests/main_menu/test_payments.py` (empty) |
| **Requires** | Sales with outstanding amounts (Step 7.2) or Purchases with outstanding amounts (Step 6.2) |
| **Produces** | Payment records → reduces Outstanding balances |

**User Action:** User → Main Menu → Payments → sees list of all payment transactions (both incoming from customers and outgoing to suppliers).

**Continuity:** Payments are primarily created through:
- Sale forms (paid_amount at time of sale)
- Receipt Vouchers (collecting payment for outstanding invoices later)
- Purchase forms (paying suppliers)
- Payment Vouchers (paying supplier outstanding later)

---

### Step 8.3: Ledgers

| | |
|---|---|
| **Route** | `/ledgers` |
| **Page Object** | `pages/main_menu/ledgers_page.py` (stub) |
| **Test File** | `tests/main_menu/test_ledgers.py` (empty) |
| **Requires** | Account Groups (Step 4.2) + optionally Customers (5.3) / Suppliers (5.2) |
| **Produces** | Ledger accounts for **Voucher creation**, **Ledger Statement report**, **Trial Balance** |

**User Action:** User → Main Menu → Ledgers → "Add Ledger" → enters ledger name → selects Account Group (from Step 4.2) → optionally links to a Customer or Supplier → saves.

**Continuity:**
- Account Group dropdown ← Step 4.2 (determines where this ledger sits in the chart of accounts)
- Linked Customer/Supplier ← Steps 5.3/5.2
- Ledger entries feed Trial Balance, Balance Sheet, P&L

---

### Step 8.4: Enquiries

| | |
|---|---|
| **Route** | `/enquiries` (list) / `/enquiries/pipeline` (Kanban) |
| **Page Object** | `pages/main_menu/enquiry_page.py` (stub) |
| **Test File** | `tests/main_menu/test_enquiry.py` (empty) |
| **Requires** | Enquiry Stage Workflow (Step 4.7) + Customer (5.3) + optionally User/Salesperson (2.4) |
| **Produces** | Enquiry pipeline records (CRM-like lead tracking) |

**User Action:** User → Main Menu → Enquiry → "Add Enquiry" → selects Enquiry Type → selects Customer → enters description, expected value → assigns to salesperson → saves. The enquiry appears on the Pipeline (Kanban board) and can be moved between stages.

**Continuity:**
- Enquiry Type ← Step 4.6 (determines which workflow/pipeline applies)
- Workflow Stages ← Step 4.7 (defines the columns on the Kanban board)
- Customer ← Step 5.3
- Salesperson ← Step 2.4 (Users)

---

### Step 8.5: Chits

| | |
|---|---|
| **Route** | `/chits` |
| **Page Object** | `pages/main_menu/chits_page.py` (stub) |
| **Test File** | `tests/main_menu/test_chits.py` (empty) |
| **Requires** | Customer (5.3) + Bank Account (4.1) |
| **Produces** | Chit fund records → feeds **Chit Entry Vouchers**, **Chit payments** |

**User Action:** User → Main Menu → Chits → "Add Chit" → enters chit details (name, total value, number of months, installment amount) → links to customer → saves. Then records monthly payments against the chit.

**Continuity:**
- Customer ← Step 5.3 (chit holder)
- Bank Account ← Step 4.1 (for payment recording)
- Chit Entry Voucher (Accounting module) references this chit

---


## Phase 9 — Accounting: Vouchers & Financial Records

> Vouchers are the double-entry accounting transactions. They settle outstanding balances and move money between accounts.

### Step 9.1: Create Voucher (Type Selection)

| | |
|---|---|
| **Route** | `/vouchers/create` |
| **Page Object** | `pages/accounting/create_voucher_page.py` |
| **Test File** | `tests/accounting/test_create_voucher.py` (empty) |
| **Requires** | Voucher Types configured (Step 4.3) |
| **Produces** | Redirects to specific voucher form based on selection |

**User Action:** User → Accounting → Vouchers → Create Voucher → sees buttons for each type (Receipt, Payment, Contra, Journal, Chit Entry, MDR Settlement) → clicks one.

---

### Step 9.2: Receipt Voucher (Collect money FROM customer)

| | |
|---|---|
| **Route** | `/vouchers/receipt/create` |
| **Requires** | Bank Account (4.1) + Customer with outstanding balance (from credit Sales in Step 7.2) |
| **Produces** | Receipt record → **reduces Customer Outstanding** → **increases Bank balance** |

**User Action:** User selects "Receipt Voucher" → selects Customer → sees their outstanding invoices → selects which invoices to settle → enters amount received → selects receiving bank account → saves.

**Continuity:** This is how credit sales get paid later. The outstanding amount from Step 7.2 decreases.

---

### Step 9.3: Payment Voucher (Pay money TO supplier)

| | |
|---|---|
| **Route** | `/vouchers/payment/create` |
| **Requires** | Bank Account (4.1) + Supplier with outstanding balance (from credit Purchases in Step 6.2) |
| **Produces** | Payment record → **reduces Supplier Outstanding** → **decreases Bank balance** |

**User Action:** User selects "Payment Voucher" → selects Supplier → sees their outstanding invoices → selects which to pay → enters amount → selects paying bank account → saves.

**Continuity:** This is how credit purchases get settled later. The outstanding from Step 6.2 decreases.

---

### Step 9.4: Contra Voucher (Transfer between own accounts)

| | |
|---|---|
| **Route** | `/vouchers/contra/create` |
| **Requires** | 2+ Bank Accounts (Step 4.1) |
| **Produces** | Inter-account transfer record (e.g., move cash from savings to current account) |

**User Action:** User selects "Contra Voucher" → selects source bank account → selects destination bank account → enters transfer amount → saves.

---

### Step 9.5: Journal Voucher (Non-cash accounting adjustments)

| | |
|---|---|
| **Route** | `/vouchers/journal/create` |
| **Requires** | Account Groups/Ledgers (Steps 4.2, 8.3) |
| **Produces** | Journal entry (debit one account, credit another — for adjustments, depreciation, etc.) |

---

### Step 9.6: Chit Entry Voucher

| | |
|---|---|
| **Route** | `/vouchers/chit/create` |
| **Requires** | Chits (Step 8.5) + Bank Account (4.1) |
| **Produces** | Records a chit installment payment from a customer |

---

### Step 9.7: MDR Settlement Voucher

| | |
|---|---|
| **Route** | `/vouchers/mdr/create` |
| **Requires** | Bank Accounts (4.1) with card/UPI transaction history |
| **Produces** | Records merchant discount rate deductions by payment processors |

---

### Step 9.8: Voucher History

| | |
|---|---|
| **Route** | `/vouchers/history` |
| **Page Object** | `pages/accounting/voucher_history_page.py` |
| **Test File** | `tests/accounting/test_voucher_history.py` (empty) |
| **Requires** | At least 1 voucher created (Steps 9.2–9.7) |
| **Produces** | Chronological list of all vouchers with filters |

---

### Step 9.9: Branch Fund Transfers

| | |
|---|---|
| **Route** | `/branch-fund-transfers` |
| **Requires** | 2+ Branches (Step 2.2) each with Bank Accounts (Step 4.1) |
| **Produces** | Records fund movement between branches |

**User Action:** User → Accounting → Branch Fund Transfers → "Create" → selects source branch + bank → selects destination branch + bank → enters amount → saves.

---

### Step 9.10: Day Book

| | |
|---|---|
| **Route** | `/accounting/day-book` |
| **Page Object** | `pages/accounting/day_book_page.py` |
| **Test File** | `tests/accounting/test_day_book.py` (empty) |
| **Requires** | Any financial transactions (Sales, Purchases, Vouchers, Expenses) |
| **Produces** | Daily transaction summary (all debits and credits for a date range) |

**User Action:** User → Accounting → Day Book → selects date range → sees all transactions for that period with running totals.

**Continuity:** Aggregates data from: Sales (7.2), Purchases (6.2), Expenses (8.1), all Vouchers (9.2–9.7).

---


## Phase 10 — Accounting: Financial Statements

> These are read-only reports generated from accumulated transaction data.

### Step 10.1: Profit & Loss

| | |
|---|---|
| **Route** | `/reports/profit-loss` |
| **Page Object** | `pages/accounting/profit_loss_page.py` |
| **Test File** | `tests/accounting/test_profit_loss.py` (empty) |
| **Requires** | Sales revenue (Step 7.2) + Purchase costs (Step 6.2) + Expenses (Step 8.1) |
| **Produces** | Profit/Loss statement for a financial year |

**What it shows:** Revenue (from Sales) minus Cost of Goods (from Purchases) minus Operating Expenses = Net Profit/Loss.

---

### Step 10.2: Trial Balance

| | |
|---|---|
| **Route** | `/reports/trial-balance` |
| **Page Object** | `pages/accounting/trial_balance_page.py` |
| **Test File** | `tests/accounting/test_trial_balance.py` (empty) |
| **Requires** | Account Groups (4.2) + any transactions creating ledger entries |
| **Produces** | Debit/Credit balance of all ledger accounts |

---

### Step 10.3: Balance Sheet

| | |
|---|---|
| **Route** | `/reports/balance-sheet` |
| **Page Object** | `pages/accounting/balance_sheet_page.py` |
| **Test File** | `tests/accounting/test_balance_sheet.py` (empty) |
| **Requires** | Account Groups (4.2) + accumulated assets, liabilities, equity |
| **Produces** | Assets = Liabilities + Equity snapshot |

---

### Step 10.4: Cash Flow

| | |
|---|---|
| **Route** | `/reports/cash-flow` |
| **Page Object** | `pages/accounting/cash_flow_page.py` |
| **Test File** | `tests/accounting/test_cash_flow.py` (empty) |
| **Requires** | Bank transactions + Cash transactions from all modules |
| **Produces** | Cash inflow/outflow statement |

---

### Step 10.5: Ledger Statement

| | |
|---|---|
| **Route** | `/reports/ledger-statement` |
| **Page Object** | `pages/accounting/ledger_statement_page.py` |
| **Test File** | `tests/accounting/test_ledger_statement.py` (empty) |
| **Requires** | Ledgers (8.3) with transactions |
| **Produces** | Transaction history for a specific ledger account |

---

## Phase 11 — Reports Module

> Business intelligence reports that aggregate data across modules.

### Step 11.1: Outstanding Bills

| | |
|---|---|
| **Route** | `/vouchers/outstanding` |
| **Page Object** | `pages/reports/outstanding_page.py` |
| **Test File** | `tests/reports/test_outstanding.py` (empty) |
| **Requires** | Credit Sales (Step 7.2 with paid_amount < total) or Credit Purchases (Step 6.2 with paid_amount < total) |
| **Produces** | List of all unpaid invoices with aging |

**What it shows:** All invoices where `paid_amount < invoice_total`, grouped by customer/supplier, with days outstanding.

---

### Step 11.2: Customer Outstanding

| | |
|---|---|
| **Route** | `/reports/customer-outstanding` |
| **Requires** | Credit Sales (Step 7.2) |
| **Produces** | Per-customer breakdown of receivables |

---

### Step 11.3: Supplier Outstanding

| | |
|---|---|
| **Route** | `/reports/supplier-outstanding` |
| **Requires** | Credit Purchases (Step 6.2) |
| **Produces** | Per-supplier breakdown of payables |

---

### Step 11.4: Stock Summary

| | |
|---|---|
| **Route** | `/reports/stock-summary` |
| **Page Object** | `pages/reports/stock_summary_page.py` |
| **Test File** | `tests/reports/test_stock_summary.py` (empty) |
| **Requires** | Products with stock (Steps 5.1, 6.2, 7.2) |
| **Produces** | Current stock levels, value, and movement summary per product per branch |

---

### Step 11.5: MDR Report

| | |
|---|---|
| **Route** | `/reports/mdr-report` |
| **Page Object** | `pages/reports/mdr_report_page.py` |
| **Test File** | `tests/reports/test_mdr_report.py` (empty) |
| **Requires** | Sales paid via bank (card/UPI transactions from Step 7.2) |
| **Produces** | Merchant discount rate tracking (how much payment processors deducted) |

---

### Step 11.6: GSTR-1 B2B

| | |
|---|---|
| **Route** | `/reports/gstr1-b2b` |
| **Requires** | Sales to registered businesses (GST-registered customers from Step 7.2) |
| **Produces** | GST filing data for Business-to-Business transactions |

---

### Step 11.7: GSTR-1 B2C

| | |
|---|---|
| **Route** | `/reports/gstr1-b2c` |
| **Requires** | Sales to unregistered consumers (from Step 7.2) |
| **Produces** | GST filing data for Business-to-Consumer transactions |

---


## Recommended Test Execution Order

Run tests in this exact order to maintain data continuity:

```bash
# Phase 1 — Auth & Dashboard
python -m pytest tests/test_auth.py
python -m pytest tests/test_dashboard.py

# Phase 2 — Foundation Masters
python -m pytest tests/master_menu/test_cities.py
python -m pytest tests/master_menu/test_branches.py
python -m pytest tests/master_menu/test_roles.py
python -m pytest tests/master_menu/test_users.py

# Phase 3 — Product Masters
python -m pytest tests/master_menu/test_categories.py
python -m pytest tests/master_menu/test_brands.py
python -m pytest tests/master_menu/test_unit_types.py
python -m pytest tests/master_menu/test_sac_hsn.py
python -m pytest tests/master_menu/test_attribute_keys.py
python -m pytest tests/master_menu/test_attribute_values.py
python -m pytest tests/master_menu/test_product_attributes.py

# Phase 4 — Finance & Misc Masters
python -m pytest tests/master_menu/test_bank_accounts.py
python -m pytest tests/master_menu/test_account_groups.py
python -m pytest tests/master_menu/test_voucher_types.py
python -m pytest tests/master_menu/test_expense_categories.py
python -m pytest tests/master_menu/test_racks.py
python -m pytest tests/master_menu/test_enquiry_types.py
python -m pytest tests/master_menu/test_enquiry_stage_workflows.py

# Phase 5 — Core Entities
python -m pytest tests/main_menu/test_products.py
python -m pytest tests/main_menu/test_suppliers.py
python -m pytest tests/main_menu/test_customers.py

# Phase 6 — Purchase Flow
python -m pytest tests/main_menu/test_purchase_request.py
python -m pytest tests/main_menu/test_purchases.py
python -m pytest tests/main_menu/test_purchase_returns.py
python -m pytest tests/main_menu/test_batches.py

# Phase 7 — Sales Flow
python -m pytest tests/main_menu/test_sales_quotes.py
python -m pytest tests/main_menu/test_sales.py
python -m pytest tests/main_menu/test_sale_returns.py
python -m pytest tests/main_menu/test_inventories.py

# Phase 8 — Supporting Modules
python -m pytest tests/main_menu/test_expenses.py
python -m pytest tests/main_menu/test_payments.py
python -m pytest tests/main_menu/test_ledgers.py
python -m pytest tests/main_menu/test_enquiry.py
python -m pytest tests/main_menu/test_chits.py

# Phase 9-10 — Accounting
python -m pytest tests/accounting/

# Phase 11 — Reports
python -m pytest tests/reports/
```

---

## Module Coverage Matrix

| Module | Page Object | Test File | Status |
|--------|------------|-----------|--------|
| **Auth / Login** | `pages/auth/login_page.py` | `tests/test_auth.py` | ✅ Complete |
| **Dashboard** | `pages/dashboard_page.py` | `tests/test_dashboard.py` | ✅ Complete |
| **Cities** | `pages/master_menu/cities_page.py` | `tests/master_menu/test_cities.py` | ✅ Complete |
| **Branches** | `pages/master_menu/branches_page.py` | `tests/master_menu/test_branches.py` | ✅ Complete |
| **Roles** | `pages/master_menu/roles_page.py` | `tests/master_menu/test_roles.py` | ✅ Complete |
| **Users** | `pages/master_menu/users_page.py` | `tests/master_menu/test_users.py` | ✅ Complete |
| **Categories** | `pages/master_menu/categories_page.py` | `tests/master_menu/test_categories.py` | ✅ Complete |
| **Brands** | `pages/master_menu/brands_page.py` | `tests/master_menu/test_brands.py` | ✅ Complete |
| **Unit Types** | `pages/master_menu/unit_types_page.py` | `tests/master_menu/test_unit_types.py` | ✅ Complete |
| **SAC/HSN** | `pages/master_menu/sac_hsn_page.py` | `tests/master_menu/test_sac_hsn.py` | ✅ Complete |
| **Attribute Keys** | `pages/master_menu/attribute_keys_page.py` | `tests/master_menu/test_attribute_keys.py` | ✅ Complete |
| **Attribute Values** | `pages/master_menu/attribute_values_page.py` | `tests/master_menu/test_attribute_values.py` | ✅ Complete |
| **Product Attributes** | `pages/master_menu/product_attributes_page.py` | `tests/master_menu/test_product_attributes.py` | ✅ Complete |
| **Bank Accounts** | `pages/master_menu/bank_accounts_page.py` | `tests/master_menu/test_bank_accounts.py` | ✅ Complete |
| **Account Groups** | `pages/master_menu/account_groups_page.py` | `tests/master_menu/test_account_groups.py` | ✅ Complete |
| **Voucher Types** | `pages/master_menu/voucher_types_page.py` | `tests/master_menu/test_voucher_types.py` | ✅ Complete |
| **Expense Categories** | `pages/master_menu/expense_categories_page.py` | `tests/master_menu/test_expense_categories.py` | ✅ Complete |
| **Racks** | `pages/master_menu/racks_page.py` | `tests/master_menu/test_racks.py` | ✅ Complete |
| **Enquiry Types** | `pages/master_menu/enquiry_types_page.py` | `tests/master_menu/test_enquiry_types.py` | ✅ Complete |
| **Enquiry Workflows** | `pages/master_menu/enquiry_stage_workflows_page.py` | `tests/master_menu/test_enquiry_stage_workflows.py` | ✅ Complete |
| **Products** | `pages/main_menu/products_page.py` | `tests/main_menu/test_products.py` | ✅ Complete |
| **Suppliers** | `pages/main_menu/suppliers_page.py` | `tests/main_menu/test_suppliers.py` | ✅ Complete |
| **Customers** | `pages/main_menu/customers_page.py` | `tests/main_menu/test_customers.py` | ✅ Complete |
| **Purchase Requests** | `pages/main_menu/purchase_request_page.py` | `tests/main_menu/test_purchase_request.py` | ✅ Complete |
| **Purchases** | `pages/main_menu/purchases_page.py` | `tests/main_menu/test_purchases.py` | ✅ Complete |
| **Purchase Returns** | `pages/main_menu/purchase_returns_page.py` | `tests/main_menu/test_purchase_returns.py` | ✅ Complete |
| **Batches** | `pages/main_menu/batches_page.py` | `tests/main_menu/test_batches.py` | ✅ Complete |
| **Sales Quotes** | `pages/main_menu/sales_quotes_page.py` | `tests/main_menu/test_sales_quotes.py` | ✅ Complete |
| **Sales** | `pages/main_menu/sales_page.py` | `tests/main_menu/test_sales.py` | ✅ Complete |
| **Sale Returns** | `pages/main_menu/sale_returns_page.py` | `tests/main_menu/test_sale_returns.py` | ✅ Complete |
| **Inventories** | `pages/main_menu/inventories_page.py` (stub) | `tests/main_menu/test_inventories.py` (empty) | ❌ Not started |
| **Expenses** | `pages/main_menu/expenses_page.py` (stub) | `tests/main_menu/test_expenses.py` (empty) | ❌ Not started |
| **Payments** | `pages/main_menu/payments_page.py` (stub) | `tests/main_menu/test_payments.py` (empty) | ❌ Not started |
| **Ledgers** | `pages/main_menu/ledgers_page.py` (stub) | `tests/main_menu/test_ledgers.py` (empty) | ❌ Not started |
| **Enquiries** | `pages/main_menu/enquiry_page.py` (stub) | `tests/main_menu/test_enquiry.py` (empty) | ❌ Not started |
| **Chits** | `pages/main_menu/chits_page.py` (stub) | `tests/main_menu/test_chits.py` (empty) | ❌ Not started |
| **Create Voucher** | `pages/accounting/create_voucher_page.py` | `tests/accounting/test_create_voucher.py` (empty) | ❌ Not started |
| **Day Book** | `pages/accounting/day_book_page.py` | `tests/accounting/test_day_book.py` (empty) | ❌ Not started |
| **Voucher History** | `pages/accounting/voucher_history_page.py` | `tests/accounting/test_voucher_history.py` (empty) | ❌ Not started |
| **Ledger Statement** | `pages/accounting/ledger_statement_page.py` | `tests/accounting/test_ledger_statement.py` (empty) | ❌ Not started |
| **Trial Balance** | `pages/accounting/trial_balance_page.py` | `tests/accounting/test_trial_balance.py` (empty) | ❌ Not started |
| **Profit & Loss** | `pages/accounting/profit_loss_page.py` | `tests/accounting/test_profit_loss.py` (empty) | ❌ Not started |
| **Balance Sheet** | `pages/accounting/balance_sheet_page.py` | `tests/accounting/test_balance_sheet.py` (empty) | ❌ Not started |
| **Cash Flow** | `pages/accounting/cash_flow_page.py` | `tests/accounting/test_cash_flow.py` (empty) | ❌ Not started |
| **Stock Summary** | `pages/reports/stock_summary_page.py` | `tests/reports/test_stock_summary.py` (empty) | ❌ Not started |
| **Outstanding** | `pages/reports/outstanding_page.py` | `tests/reports/test_outstanding.py` (empty) | ❌ Not started |
| **MDR Report** | `pages/reports/mdr_report_page.py` | `tests/reports/test_mdr_report.py` (empty) | ❌ Not started |

---

## Key Data Continuity Rules

1. **A Product CANNOT be sold until it has stock** — stock comes from Opening Stock (manual) or Purchases (automatic)
2. **A Sale/Purchase Return is ONLY possible against an existing Sale/Purchase** — the return form is accessed from the original transaction's action button
3. **Batches are auto-created** — they cannot be manually created; they appear after a Purchase is saved
4. **Outstanding amounts are the DIFFERENCE** between invoice total and paid amount — they decrease when Receipt/Payment Vouchers are created
5. **Bank Account balance changes ONLY through transactions** — Sales payments, Purchase payments, Vouchers, and Branch Fund Transfers. There's no "add balance" button.
6. **Financial reports are aggregations** — they don't have their own data; they READ from all other modules

---

## End-to-End Scenario Example

> "A shop buys 50 T-Shirts from Supplier A, sells 30 to Customer B, processes a return of 5, and generates a profit report"

| Step | Module | Action | Stock Effect |
|------|--------|--------|-------------|
| 1 | Master Setup | Create City, Branch, Category, Brand, Unit, HSN, Bank Account | — |
| 2 | Products | Create "T-Shirt" (cost ₹200, sell ₹499, 18% GST) | 0 |
| 3 | Suppliers | Create "Supplier A" | — |
| 4 | Customers | Create "Customer B" | — |
| 5 | Purchases | Buy 50 T-Shirts from Supplier A at ₹200 each (₹10,000 total), pay ₹5,000 via bank | +50 |
| 6 | Batches | Auto-created: Batch shows "50/50" | — |
| 7 | Sales | Sell 30 T-Shirts to Customer B at ₹499 (₹14,970 total), collect ₹10,000 via bank | -30 → 20 left |
| 8 | Sale Returns | Customer returns 5 T-Shirts | +5 → 25 left |
| 9 | Inventories | Shows 25 T-Shirts available | — |
| 10 | Receipt Voucher | Collect remaining ₹4,970 from Customer B | Customer Outstanding → ₹0 |
| 11 | Payment Voucher | Pay remaining ₹5,000 to Supplier A | Supplier Outstanding → ₹0 |
| 12 | Day Book | Shows all 5 transactions for today | — |
| 13 | P&L Report | Revenue ₹12,475 (30−5=25 shirts × ₹499) − COGS ₹5,000 (25 × ₹200) = Gross Profit ₹7,475 | — |
| 14 | Stock Summary | T-Shirt: 25 units, value ₹5,000 (at cost) | — |
| 15 | Outstanding | Both Customer and Supplier show ₹0 outstanding | — |
