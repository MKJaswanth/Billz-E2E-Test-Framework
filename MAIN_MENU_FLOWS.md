# Crystal Billz — Main Menu Modules User Flows & Interconnections

This document details the user flows, data dependencies, and module interconnections across the **Main Menu** section of Crystal Billz. Use this as a reference when writing tests to understand which modules must be set up first and how data flows between them.

---

## 🔗 Module Dependency Map (Read This First)

The Main Menu modules are heavily interconnected. The diagram below shows the data flow — an arrow means "depends on" or "feeds into".

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        MASTER MENU (Setup Layer)                        │
│                                                                         │
│  Cities ──► Branches ──► Users                                          │
│  Categories, Brands, Unit Types, SAC/HSN Codes ──► Products             │
│  Expense Categories ──► Expenses                                        │
│  Enquiry Types ──► Enquiry Stage Workflows ──► Enquiries                │
│  Account Groups ──► Ledgers                                             │
│  Bank Accounts ──► Payments / Accounting Vouchers                       │
│  Racks ──► Inventory Storage                                            │
└──────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                        MAIN MENU (Transaction Layer)                    │
│                                                                         │
│  Products ◄── (Brand, Category, Unit Type, HSN)                         │
│      │                                                                  │
│      ├──► Opening Stock ──► Inventories                                 │
│      │                                                                  │
│      ├──► Purchase Request ──► Purchase Order ──► Inventories (IN)      │
│      │         │                     │                                  │
│      │         │              Purchase Returns ──► Inventories (OUT)    │
│      │         │                                                        │
│      ├──► Sales Quote ──► Sale/Invoice ──► Inventories (OUT)            │
│      │                        │                                         │
│      │                 Sale Returns ──► Inventories (IN)                │
│      │                                                                  │
│      ├──► Batches (tracks batch numbers, expiry per product)            │
│      │                                                                  │
│  Customers ──► Sales, Sales Quotes, Enquiries, Payments (Receivable)   │
│  Suppliers ──► Purchases, Purchase Requests, Payments (Payable)        │
│  Expenses ──► Expense Category + Amount + Branch                        │
│  Payments ──► Settles outstanding invoices (Sales/Purchases)            │
│  Ledgers ──► Automatically created for Customers, Suppliers, Banks     │
│  Enquiries ──► Customer + Enquiry Type + Workflow Stage tracking        │
│                                                                         │
└──────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                      ACCOUNTING (Reporting Layer)                        │
│                                                                         │
│  All transactions auto-generate vouchers ──► Day Book ──► Ledger Stmt   │
│  ──► Trial Balance ──► P&L ──► Balance Sheet ──► Cash Flow              │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 📋 Test Setup Order (Prerequisites)

When running tests, modules must be set up in this order due to cascading dependencies:

| Order | Module              | Depends On                                                    |
|-------|---------------------|---------------------------------------------------------------|
| 1     | Cities              | —                                                             |
| 2     | Branches            | Cities                                                        |
| 3     | Roles               | —                                                             |
| 4     | Users               | Branches, Roles                                               |
| 5     | Categories          | —                                                             |
| 6     | Brands              | —                                                             |
| 7     | Unit Types          | —                                                             |
| 8     | SAC/HSN Codes       | —                                                             |
| 9     | Expense Categories  | —                                                             |
| 10    | Enquiry Types       | —                                                             |
| 11    | **Products**        | Brands, Categories, Unit Types, SAC/HSN Codes                 |
| 12    | **Customers**       | —                                                             |
| 13    | **Suppliers**       | —                                                             |
| 14    | Enquiry Workflows   | Enquiry Types                                                 |
| 15    | **Enquiries**       | Customers, Enquiry Types, Enquiry Stage Workflows             |
| 16    | **Purchase Requests**| Products, Suppliers                                          |
| 17    | **Purchases**       | Products, Suppliers, (optionally Purchase Requests)           |
| 18    | **Purchase Returns** | Purchases (requires an existing purchase to return against)  |
| 19    | **Sales Quotes**    | Products, Customers                                           |
| 20    | **Sales / Invoices**| Products, Customers, (optionally Sales Quotes)                |
| 21    | **Sale Returns**    | Sales (requires an existing sale to return against)           |
| 22    | **Expenses**        | Expense Categories, Branches                                  |
| 23    | **Payments**        | Customers or Suppliers (to settle outstanding invoices)       |
| 24    | **Inventories**     | Products, Branches (read-only view, auto-updated by transactions) |
| 25    | **Batches**         | Products (tracks batch-level details per product)             |

---

## 1. 📦 Products

* **Path**: `/products`
* **Purpose**: The central catalogue. Every purchase, sale, and inventory record references a product.

### Dependencies (Master Menu)
A product cannot be created without these existing first:
* **Brand** (dropdown) — from Master ➔ Brands
* **Category** (dropdown) — from Master ➔ Categories
* **Unit Type** (dropdown) — from Master ➔ Unit Types
* **SAC/HSN Code** (dropdown) — from Master ➔ GST Codes
* **GST Percentage** (dropdown) — system values (0%, 5%, 12%, 18%, 28%)

### Form Fields
| Field            | Type          | Required |
|------------------|---------------|----------|
| Product Name     | Text input    | ✅       |
| Brand            | React-Select  | ✅       |
| Category         | React-Select  | ✅       |
| Cost Price       | Number input  | ✅       |
| Selling Price    | Number input  | ✅       |
| GST Percentage   | React-Select  | ✅       |
| HSN/SAC Code     | React-Select  | ✅       |
| Unit Type        | React-Select  | ✅       |
| Low Stock Alert  | Number input  | Optional |

### Special Actions
* **Opening Stock Update**: Set initial stock quantity per branch (requires a Branch). This updates the Inventory.
* **View / Edit / Delete / Restore**: Standard CRUD lifecycle.

### Downstream Impact
* Adding products populates dropdown options in: Purchases, Sales, Sales Quotes, Purchase Requests, Batches.
* Opening Stock feeds directly into the Inventories module.

---

## 2. 👥 Customers

* **Path**: `/customers`
* **Purpose**: Parties who buy from the business. Required for Sales, Sales Quotes, Enquiries, and Payments.

### Form Fields
| Field             | Type         | Required |
|-------------------|--------------|----------|
| Customer Name     | Text input   | ✅       |
| Contact Person    | Text input   | Optional |
| Email             | Text input   | Optional |
| Phone             | Text input   | ✅       |
| Address           | Text area    | Optional |
| City              | React-Select | Optional |
| GST Number        | Text input   | Optional |
| Opening Balance   | Number input | Optional |

### Downstream Impact
* Creates a **Customer Ledger** automatically in the Accounting system.
* Available as a party selection in: **Sales**, **Sales Quotes**, **Enquiries**, **Receipt Vouchers**.

---

## 3. 🏭 Suppliers

* **Path**: `/suppliers`
* **Purpose**: Parties from whom the business buys. Required for Purchases and Purchase Requests.

### Form Fields
| Field             | Type         | Required |
|-------------------|--------------|----------|
| Supplier Name     | Text input   | ✅       |
| Contact Person    | Text input   | Optional |
| Email             | Text input   | Optional |
| Phone             | Text input   | ✅       |
| GST Number        | Text input   | Optional |
| Address           | Text area    | Optional |
| City              | React-Select | Optional |

### Downstream Impact
* Creates a **Supplier Ledger** automatically in the Accounting system.
* Available as a party selection in: **Purchases**, **Purchase Requests**, **Payment Vouchers**.

---

## 4. 📋 Enquiries

* **Path**: `/enquiries`
* **Purpose**: Track pre-sale customer interest. Follows a stage-based workflow.

### Dependencies
* **Customer** — who is enquiring
* **Enquiry Type** — from Master ➔ Enquiry Types
* **Enquiry Stage Workflow** — from Master ➔ Enquiry Stage Workflows (defines the stage progression)

### User Flow
1. User creates an enquiry, selecting a Customer, Enquiry Type, and entering details.
2. The enquiry starts at the first stage of the assigned workflow.
3. User progresses the enquiry through stages (e.g., New ➔ Follow-up ➔ Negotiation ➔ Closed Won/Lost).
4. A "Closed Won" enquiry can be converted into a **Sales Quote** or **Sale**.

### Downstream Impact
* Enquiries can be converted to Sales Quotes or Sales, linking pre-sale tracking to actual revenue.

---

## 5. 📝 Purchase Requests

* **Path**: `/purchase-requests`
* **Purpose**: Internal request to procure goods. Acts as an approval step before placing a purchase order.

### Dependencies
* **Supplier** — from whom to purchase
* **Products** — line items with quantities

### Form Fields
| Field           | Type            | Required |
|-----------------|-----------------|----------|
| Supplier        | React-Select    | ✅       |
| Branch          | React-Select    | ✅       |
| Date            | Datepicker      | ✅       |
| Product Lines   | Multi-row table | ✅       |
| ├─ Product      | React-Select    | ✅       |
| ├─ Quantity     | Number input    | ✅       |
| └─ Rate         | Number input    | ✅       |
| Notes           | Text area       | Optional |

### User Flow
1. User creates a Purchase Request with product line items.
2. Manager reviews and **Approves** or **Rejects** the request.
3. An approved request can be **Converted to a Purchase Order**.

### Downstream Impact
* Approved Purchase Requests feed into the **Purchases** module.

---

## 6. 🛒 Purchases (Purchase Orders / Bills)

* **Path**: `/purchases`
* **Purpose**: Record goods bought from suppliers. Increases inventory and creates payable obligations.

### Dependencies
* **Supplier** — party from whom goods are bought
* **Products** — line items with quantities and rates
* **Branch** — destination branch for the stock

### Form Fields
| Field           | Type            | Required |
|-----------------|-----------------|----------|
| Supplier        | React-Select    | ✅       |
| Branch          | React-Select    | ✅       |
| Invoice Number  | Text input      | Optional |
| Date            | Datepicker      | ✅       |
| Product Lines   | Multi-row table | ✅       |
| ├─ Product      | React-Select    | ✅       |
| ├─ Quantity     | Number input    | ✅       |
| ├─ Rate         | Number input    | ✅       |
| ├─ Discount     | Number input    | Optional |
| └─ GST          | Auto-calculated | —        |
| Total Amount    | Auto-calculated | —        |

### Downstream Impact
* **Inventory** increases for the purchased products at the specified branch.
* **Supplier Ledger** is credited (payable obligation created).
* A **Payment Voucher** can later be created to settle this purchase.
* Purchase can be partially or fully returned via **Purchase Returns**.

---

## 7. ↩️ Purchase Returns

* **Path**: `/purchase-returns`
* **Purpose**: Return purchased goods back to the supplier.

### Dependencies
* **Existing Purchase** — must reference an original purchase invoice

### User Flow
1. User selects an existing Purchase to return against.
2. Selects specific products and quantities to return (partial or full).
3. System calculates the refund/credit amount.
4. On submission:
   - **Inventory decreases** for returned items.
   - **Supplier Ledger** is debited (reduces payable).

---

## 8. 📄 Sales Quotes (Quotations / Proforma)

* **Path**: `/sales-quotes`
* **Purpose**: Provide a price estimate to a customer before confirming a sale.

### Dependencies
* **Customer** — who receives the quote
* **Products** — line items with quantities and prices

### User Flow
1. User creates a quote with customer details and product line items.
2. Quote is shared with the customer (print / PDF).
3. If the customer accepts, the quote can be **Converted to a Sale/Invoice**.

### Downstream Impact
* Approved quotes feed directly into the **Sales** module, pre-filling all line items.

---

## 9. 💰 Sales (Invoices)

* **Path**: `/sales`
* **Purpose**: Record goods sold to customers. Decreases inventory and creates receivable obligations.

### Dependencies
* **Customer** — party to whom goods are sold
* **Products** — line items with quantities and rates
* **Branch** — source branch from which stock is dispatched

### Form Fields
| Field           | Type            | Required |
|-----------------|-----------------|----------|
| Customer        | React-Select    | ✅       |
| Branch          | React-Select    | ✅       |
| Invoice Number  | Auto-generated  | —        |
| Date            | Datepicker      | ✅       |
| Product Lines   | Multi-row table | ✅       |
| ├─ Product      | React-Select    | ✅       |
| ├─ Quantity     | Number input    | ✅       |
| ├─ Rate         | Number input    | ✅       |
| ├─ Discount     | Number input    | Optional |
| └─ GST          | Auto-calculated | —        |
| Payment Method  | React-Select    | ✅       |
| Total Amount    | Auto-calculated | —        |

### Downstream Impact
* **Inventory decreases** for sold products at the specified branch.
* **Customer Ledger** is debited (receivable obligation created).
* A **Receipt Voucher** can later be created to record payment collection.
* Sale can be partially or fully returned via **Sale Returns**.
* Accounting voucher is auto-generated and appears in **Day Book**.

---

## 10. ↩️ Sale Returns (Credit Notes)

* **Path**: `/sale-returns`
* **Purpose**: Accept returned goods from a customer.

### Dependencies
* **Existing Sale** — must reference an original sale invoice

### User Flow
1. User selects an existing Sale to return against.
2. Selects specific products and quantities being returned (partial or full).
3. System calculates the credit note amount.
4. On submission:
   - **Inventory increases** for returned items.
   - **Customer Ledger** is credited (reduces receivable).

---

## 11. 📊 Inventories (Stock View)

* **Path**: `/inventories`
* **Purpose**: Read-only consolidated view of stock levels across all branches.

### Data Sources (Auto-Updated By)
| Action                | Effect on Stock |
|-----------------------|-----------------|
| Opening Stock Update  | ⬆️ Increases    |
| Purchase Received     | ⬆️ Increases    |
| Purchase Return       | ⬇️ Decreases    |
| Sale / Invoice        | ⬇️ Decreases    |
| Sale Return           | ⬆️ Increases    |

### Key Columns
* Product Name, Branch, Available Quantity, Reserved Quantity, Cost Price, Selling Price.

### User Actions
* Filter by Branch, Category, or Product Name.
* View low-stock alerts (products below their Low Stock threshold).

---

## 12. 🏷️ Batches

* **Path**: `/batches`
* **Purpose**: Track batch-level information per product (batch number, manufacturing date, expiry date).

### Dependencies
* **Products** — each batch is linked to a specific product

### User Flow
1. When adding stock (via Purchase or Opening Stock), the user can optionally assign a Batch Number and Expiry Date.
2. The Batches page lists all batch records with their associated product, quantity, and dates.
3. Useful for industries requiring lot tracking (pharma, food, cosmetics).

---

## 13. 💸 Expenses

* **Path**: `/expenses`
* **Purpose**: Record business operating expenses (rent, utilities, travel, etc.).

### Dependencies
* **Expense Category** — from Master ➔ Expense Categories
* **Branch** — which branch incurred the expense

### Form Fields
| Field              | Type         | Required |
|--------------------|--------------|----------|
| Expense Category   | React-Select | ✅       |
| Branch             | React-Select | ✅       |
| Amount             | Number input | ✅       |
| Date               | Datepicker   | ✅       |
| Description/Notes  | Text area    | Optional |
| Payment Method     | React-Select | Optional |

### Downstream Impact
* Expense entries create accounting voucher entries that appear in the **Day Book** and **P&L Statement**.

---

## 14. 💳 Payments

* **Path**: `/payments`
* **Purpose**: Record and settle outstanding invoices from Sales (receivables) and Purchases (payables).

### Dependencies
* **Customer** or **Supplier** — party whose balance is being settled
* **Bank Account** — from Master ➔ Bank Accounts (for non-cash payments)

### User Flow — Receiving Payment (from Customer)
1. Select Customer.
2. System shows all outstanding Sale invoices for that customer.
3. Enter the payment amount and allocate it against one or more invoices.
4. Creates a **Receipt Voucher** in Accounting.

### User Flow — Making Payment (to Supplier)
1. Select Supplier.
2. System shows all outstanding Purchase invoices for that supplier.
3. Enter the payment amount and allocate it against one or more invoices.
4. Creates a **Payment Voucher** in Accounting.

---

## 15. 📒 Ledgers

* **Path**: `/ledgers`
* **Purpose**: View and manage all financial ledger accounts.

### Auto-Created Ledgers
The system automatically creates ledger accounts when:
* A **Customer** is added ➔ Customer Ledger (under Sundry Debtors group)
* A **Supplier** is added ➔ Supplier Ledger (under Sundry Creditors group)
* A **Bank Account** is added ➔ Bank Ledger (under Bank Accounts group)

### User Actions
* View list of all ledgers.
* Click a ledger to view its detailed **Ledger Statement** (transactions, running balance).

---

## 🔄 End-to-End Business Cycle Summary

A typical complete business cycle through these modules flows like this:

```
1. Setup Products (with Brand, Category, Unit Type, HSN)
        │
2. Add Customers & Suppliers
        │
3. ┌─── BUYING CYCLE ────────────────────────────────────────┐
   │  Purchase Request ➔ Approve ➔ Convert to Purchase       │
   │  Purchase ➔ Stock IN ➔ Supplier Ledger Credited          │
   │  (Optional) Purchase Return ➔ Stock OUT ➔ Ledger Debited │
   └──────────────────────────────────────────────────────────┘
        │
4. ┌─── SELLING CYCLE ───────────────────────────────────────┐
   │  Enquiry ➔ Follow-up ➔ Sales Quote ➔ Convert to Sale    │
   │  Sale/Invoice ➔ Stock OUT ➔ Customer Ledger Debited      │
   │  (Optional) Sale Return ➔ Stock IN ➔ Ledger Credited     │
   └──────────────────────────────────────────────────────────┘
        │
5. ┌─── PAYMENT CYCLE ──────────────────────────────────────┐
   │  Receive Payment from Customer ➔ Receipt Voucher         │
   │  Make Payment to Supplier ➔ Payment Voucher              │
   └──────────────────────────────────────────────────────────┘
        │
6. ┌─── EXPENSE TRACKING ──────────────────────────────────┐
   │  Record Expenses ➔ Expense Voucher ➔ P&L Impact          │
   └──────────────────────────────────────────────────────────┘
        │
7. ┌─── VERIFICATION (Accounting Layer) ─────────────────────┐
   │  Day Book ➔ Ledger Statements ➔ Trial Balance             │
   │  ➔ Profit & Loss ➔ Balance Sheet ➔ Cash Flow              │
   └──────────────────────────────────────────────────────────┘
```

---

## ✅ Where to Check After Each Action

Use this quick-reference table when testing to know which downstream modules to verify:

| After This Action...         | Verify These Modules...                                     |
|------------------------------|-------------------------------------------------------------|
| Add Product                  | Product appears in Products list; available in Sales/Purchase dropdowns |
| Set Opening Stock            | Inventories shows updated quantity for that branch          |
| Create Purchase              | Inventories ⬆️, Supplier Ledger credited, Day Book entry   |
| Create Purchase Return       | Inventories ⬇️, Supplier Ledger debited, Day Book entry    |
| Create Sale                  | Inventories ⬇️, Customer Ledger debited, Day Book entry    |
| Create Sale Return           | Inventories ⬆️, Customer Ledger credited, Day Book entry   |
| Receive Payment (Customer)   | Customer Ledger balance reduced, Receipt Voucher in history |
| Make Payment (Supplier)      | Supplier Ledger balance reduced, Payment Voucher in history |
| Record Expense               | Expense Ledger debited, appears in P&L under expenses      |
| Add Customer                 | Customer Ledger auto-created in Ledgers list                |
| Add Supplier                 | Supplier Ledger auto-created in Ledgers list                |
