# Tests Need To Do

This document tracks automation that is still pending. It combines the test cases currently marked **Not Executed** in the **Automated Test Cases Main Menu** tracker with additional coverage identified by reviewing the frontend and backend source code.

The source code describes the intended implementation, but the final result must always be confirmed against the deployed application. A test should be marked **Pass** or **Fail** only after it has been executed against the target environment.

## Not Executed in Tracker

### 1. MM-ADD-089 - Prevent deleting a customer referenced by a sale

- **Modules:** Customers / Sales
- **Purpose:** Confirm that transaction history cannot be damaged by deleting a customer used in an active or completed sale.
- **Preconditions:** A customer and a completed or active sale linked to that customer exist.
- **Automation:** Create a customer, complete a sale for that customer, attempt to delete the customer, and verify both the dependency message and that the customer and sale still exist.
- **Expected:** Customer deletion is blocked with a clear message.
- **Current status:** Not Executed. The Sales dependency setup is not implemented in the current automation suite.
- **Source observation:** The database relationship may cascade when a customer is deleted. This makes the test high priority because the current implementation may remove related data instead of blocking deletion.

### 2. MM-ADD-090 - Prevent deleting a supplier referenced by a purchase

- **Modules:** Suppliers / Purchases
- **Purpose:** Verify that a supplier used in a purchase cannot be deleted and leave invalid purchase history.
- **Preconditions:** A supplier and a purchase linked to that supplier exist.
- **Automation:** Create a supplier, create a purchase for it, attempt supplier deletion, and confirm the supplier and purchase remain available.
- **Expected:** Supplier deletion is blocked with a clear dependency message.
- **Current status:** Not Executed. The required Purchase workflow and fixture are not implemented.

### 3. MM-ADD-091 - Prevent deleting a product referenced by a transaction

- **Modules:** Products / Sales / Purchases
- **Purpose:** Verify dependency handling when a product is already used in a sale or purchase line.
- **Preconditions:** A product is referenced by at least one completed or active transaction.
- **Automation:** Create a product, use it in a sale and a purchase as separate cases, attempt deletion, and verify transaction data is preserved.
- **Expected:** Deletion is blocked or handled according to the confirmed business requirement without damaging transaction history.
- **Current status:** Not Executed. Cross-module transaction fixtures are not implemented.

### 4. MM-ADD-092 - Reject negative opening-stock values

- **Module:** Products
- **Purpose:** Ensure stock quantity and cost cannot be saved as negative values.
- **Preconditions:** A product and branch exist and the Opening Stock Update form is available.
- **Automation:** Test `quantity=-1` and `cost_price=-1` independently. Scope the assertion to the relevant field error and verify that no stock update request succeeds.
- **Expected:** Each invalid value is rejected and opening stock remains unchanged.
- **Current status:** Not Executed. Current automation covers only a valid opening-stock update.

### 5. MM-ADD-105 - Prevent deleting a product assigned to an active Purchase Request

- **Modules:** Purchase Requests / Products
- **Purpose:** Verify that deleting a product does not silently remove or corrupt an active Purchase Request item.
- **Preconditions:** An active Purchase Request contains the product.
- **Automation:** Create isolated product and Purchase Request fixtures, attempt product deletion, then reopen the Purchase Request and verify its item remains intact.
- **Expected:** Product deletion is blocked with a clear dependency message.
- **Current status:** Not Executed. An isolated product dependency fixture and cleanup are pending.
- **Source observation:** The Purchase Request item foreign key appears to use cascade deletion. The live test may expose destructive behavior.

### 6. MM-ADD-106 - Prevent deleting a branch assigned to an active Purchase Request

- **Modules:** Purchase Requests / Branches
- **Purpose:** Verify that an active Purchase Request is not removed or damaged when its branch is deleted.
- **Preconditions:** An active Purchase Request is assigned to the branch.
- **Automation:** Create isolated branch and Purchase Request fixtures, attempt branch deletion, and verify the Purchase Request still exists with its original branch association.
- **Expected:** Branch deletion is blocked with a clear dependency message.
- **Current status:** Not Executed. An isolated branch dependency fixture and cleanup are pending.
- **Source observation:** The Purchase Request branch foreign key appears to use cascade deletion. This test should be treated as high priority.

## Additional Tests Identified from Source Code

### Customer validation and behavior

1. **Verify Customer phone start-digit validation**
   Test a 10-digit phone such as `1223456789`. The current source validation checks length/digits but does not clearly enforce an Indian mobile start digit of 6, 7, 8, or 9. The existing Playwright assertion may be matching placeholder text instead of an error, so it must assert the exact field error and confirm the customer was not created.

2. **Verify Customer postal-code rules**
   Test short and alphanumeric values such as `12345` and `62AB12`. Frontend validation appears to enforce only a maximum length, while backend validation permits a longer string. Confirm the actual requirement, then test the exact field error and failed API submission.

3. **Verify Customer email domain-suffix validation**
   Test `test@gmail` and other malformed addresses. Assert the email field's validation message and verify no customer is created. Do not use page-wide text matching.

4. **Test Person and Company customer types**
   Confirm that switching customer type displays the correct fields, preserves valid data, removes irrelevant requirements, and submits the correct payload.

5. **Validate Company GST number**
   Confirm GST is required for a Company and accepts only the required 15-character uppercase alphanumeric structure. Cover blank, short, lowercase, special-character, and valid values.

6. **Validate Customer sort order**
   Test blank, negative, zero, decimal, and valid positive values. Frontend and backend minimum values appear inconsistent, so record the live behavior and raise a defect if the contracts differ.

7. **Test multiple Customer addresses**
   Add, edit, and remove multiple addresses. Verify all addresses are saved and displayed correctly after reopening the customer.

8. **Enforce one default Customer address**
   Mark different addresses as default and verify only one address remains the default after saving.

9. **Test Customer search and filtering**
   Search independently by exact name, email, and phone, and test the Customer Type filter. Verify the matching value in the returned row rather than checking only that a row exists.

10. **Test Customer permissions**
    Use roles with view, create, update, and delete permissions removed independently. Verify both UI controls and direct API access are blocked as expected.

### Purchase Request validation and behavior

1. **Reject expected delivery date before request date**
   Set the expected delivery date earlier than the request date and confirm submission is blocked with a field-level message.

2. **Reject decimal quantity for the General business type**
   Test a value such as `1.5`. Source rules indicate General Purchase Requests require an integer quantity, while another business type may allow decimals.

3. **Validate Purchase Request notes length**
   Test notes at the boundary and above the maximum length. Source validation indicates a 1000-character limit.

4. **Validate Purchase Request item-notes length**
   Test item notes at the boundary and above the maximum length. Source validation indicates a 500-character limit.

5. **Validate all required Purchase Request fields independently**
   Cover branch, supplier, request date, status, priority, product, and quantity separately. Verify the relevant field error and that no create request succeeds.

6. **Prevent deletion after a GRN is created**
   Create a Purchase Request, create its GRN, attempt deletion, and verify the request remains available with the locked/dependency message.

7. **Strengthen Purchase Request search verification**
   Search by a unique supplier or Purchase Request identifier and assert that exact value in every returned row. The current test only verifies that some row is visible, while the backend source does not appear to process the frontend search parameter.

8. **Target the correct row for Purchase Request actions**
   For View, Edit, Download, Delete, and Retrieve, locate the row containing the exact supplier or request identifier before clicking the action. Avoid `.first` because it can operate on an unrelated record.

9. **Verify Purchase Request workflow API routes**
   Add integration checks for submit, approve, reject, cancel, convert-to-draft, statistics, branch/user filtering, and item updates. The frontend exposes these operations, but matching backend routes were not found during the source review. Confirm which operations are supported before adding UI tests.

10. **Verify Purchase Request status handling**
    Compare the status selected in the form with the create/update request payload and the status saved by the backend. Source files contain inconsistent defaults and accepted fields.

### Voucher Type and Voucher defects

1. **Create a Payment Voucher when numbering method is Manual**
   Set **Payment Voucher** numbering method to **Manual Entry**, save the Voucher Type, and create a Payment Voucher using valid supplier, ledger, outstanding bill, amount, allocation, and date data. The application currently returns an SQL error. It should display a required manual Voucher Number field, validate that it is not blank or duplicated for the same Voucher Type, and create the voucher without exposing a database error.

   **Source finding:** The Payment Voucher form and its API payload do not contain `voucher_no`. The settlement service then calls `Voucher::create()` without `voucher_no`. Automatic numbering fills this value in the Voucher model, but Manual numbering does not, while the database requires a non-null Voucher Number. This is the direct failure path seen in the source.

   **Automation requirements:**
   - Verify Manual Entry displays an editable Voucher Number field.
   - Verify a unique manual Voucher Number creates the Payment Voucher.
   - Verify blank manual Voucher Number is rejected before submission.
   - Verify duplicate manual Voucher Number is rejected with a controlled validation message.
   - Verify automatic numbering still generates a number without manual input.
   - Verify no SQL statement or internal database error is exposed in the UI or API response.

   **Current result:** Fail, manually observed. Automation is pending.

2. **Reject an oversized Sort Order before it reaches the database**
   Enter a Sort Order longer than six digits, such as `1234567`, in a screen where Sort Order is editable and submit it. The application currently returns an SQL error. It should enforce the agreed maximum length/range in both frontend and backend validation and show a field-level message without attempting an invalid database write.

   **Source finding:** Sort Order is stored as an integer in many tables, but several frontend and backend forms do not define a consistent maximum value. In the reviewed Voucher Type source, Sort Order is display-only and excluded from updates, which indicates that the deployed Voucher Type screen may differ from this source version. Reproduce and record the exact module, request URL, payload, response status, and SQL message before implementing the automated case.

   **Automation requirements:**
   - Test the maximum accepted six-digit value and the first rejected seven-digit value.
   - Test negative, decimal, alphabetic, blank, and database integer-boundary values where applicable.
   - Assert the exact Sort Order field error.
   - Verify the record remains unchanged after rejection.
   - Verify the API returns a controlled `422` validation response rather than an SQL or `500` response.

   **Current result:** Fail, manually observed. Exact affected form must be confirmed before automation.

### Shared automation reliability

1. **Use field-scoped validation assertions**
   Validation helpers must locate the error associated with the exact input. Page-wide regular-expression matching can incorrectly pass by finding labels, placeholders, or unrelated messages.

2. **Verify rejected submissions at two levels**
   For each invalid form case, assert both visible field feedback and that the create/update API did not succeed or the invalid record does not appear in the list.

3. **Use exact record targeting**
   Search results and action tests must identify records using a unique generated name, email, supplier, or request number before interacting with the row.

4. **Add API-level validation and dependency tests**
   Use API tests for boundary validation, permissions, foreign-key behavior, and dependency rules. Retain Playwright tests for complete user workflows and visible UI behavior.

## List Filters and Pagination

`MILESTONES.md` postpones list-filter and pagination verification across most modules. Search tests alone do not cover this behavior because filters can use different API parameters, dropdown values, date ranges, status values, and reset rules.

### Modules requiring list-filter coverage

- Cities
- Branches
- Roles
- Users
- Categories
- Brands
- Unit Types
- Attribute Keys, Attribute Values, and Product Attributes
- Bank Accounts and Account Groups
- Expense Categories and Enquiry Types
- SAC / HSN Codes
- Racks
- Enquiry Stage Workflows
- Products
- Customers and Suppliers
- Purchase Requests, Purchases, and Purchase Returns
- Sales Quotes, Sales, and Sale Returns
- Inventory and Stock lists

For each list, automate only the filters that are actually available in that module. The minimum checks are:

1. Verify that the filter controls are visible and contain the expected options.
2. Apply every filter independently and verify the matching field in every displayed row.
3. Apply supported filter combinations and verify that all selected conditions are respected.
4. Verify the empty-result state when no record matches.
5. Clear or reset filters and confirm the unfiltered list returns.
6. Verify filters remain correctly applied when moving between result pages.
7. Verify the frontend sends the expected filter parameters and the backend applies them.
8. Use unique fixture data so an unrelated existing row cannot make the test pass.

### Modules requiring pagination coverage

The same list modules above require pagination tests wherever pagination controls are available. Each test needs enough isolated records to exceed one page.

1. Verify the default page number and default page size.
2. Verify Next, Previous, First, and Last controls where available.
3. Verify boundary controls are disabled on the first and last pages.
4. Verify page-size selection changes the number of displayed records.
5. Verify records are not duplicated or omitted while moving through pages.
6. Verify search, filters, and sorting remain applied after changing pages.
7. Verify changing a filter resets to the first valid page.
8. Verify pagination after creating, deleting, or restoring a record at a page boundary.
9. Verify the displayed total count and page count match the API response.
10. Verify direct or invalid page parameters are handled safely.

## Other Unfinished Milestone Work

The following unchecked work is listed in `MILESTONES.md` in addition to list filters and pagination:

### Main Menu workflows

- Add the third Customer address/delivery type: **Billing with Delivery**.
- Verify Supplier Import status. The milestone still lists it as skipped, but `skipped.md` says the skip was removed from code.
- Create a product inline from the Purchase Request form.
- Create and verify the complete Purchase Order workflow.
- Test purchase adjustments in the Purchase form.
- Create a customer and product inline from the Sales Quote form.
- Verify stock levels after purchases, sales, purchase returns, and sale returns.

### Accounting

- Create accounting vouchers.
- Automate voucher approval.
- Verify Day Book entries.
- Verify Ledger statements.
- Verify Trial Balance, Profit and Loss, Balance Sheet, and Cash Flow statements.

### Reports

- Verify Stock Summary report filters.
- Verify Outstanding Payments reports.
- Verify MDR reports.

### Milestone tracking corrections

- Phase 3 is reported as fully complete even though list filters and pagination remain unchecked across its modules.
- Tests marked skipped for known defects are shown as completed in some module checklists. Under the current project rule, skipped defect tests must be reported as failures, not completed passes.
- Supplier Import is still shown as skipped in the milestone although it appears under **Removed (no longer skipped in code)** in `skipped.md`.
- The progress totals should be recalculated after the postponed and skipped items are classified consistently.

## Active Skipped Defects to Re-test

The following 17 tests are currently active in `skipped.md`. They remain known failures until the application behavior is fixed and each test passes without a skip marker.

| # | Module | Pending verification | Current issue |
| --- | --- | --- | --- |
| 1 | Attribute Values | View an Attribute Value | View dialog does not open. |
| 2 | Account Groups | Restore a deleted Account Group | Restore functionality does not work. |
| 3 | Expense Categories | View an Expense Category | View action is unavailable. |
| 4 | Racks / Branches | Prevent deleting a Branch containing an active Rack | Application permits the dependency deletion. |
| 5 | Users | Reject email without a valid domain suffix | Invalid email is accepted. |
| 6 | Branches | Reject phone starting outside 6-9 | Invalid Indian mobile number is accepted. |
| 7 | Bank Accounts | Reject alphanumeric account number | Invalid account number is accepted. |
| 8 | Cities | Reject a City name containing numbers | Invalid City name is accepted. |
| 9 | Products / Categories | Prevent deleting an assigned Category | Assigned Category can be deleted. |
| 10 | Products / Unit Types | Prevent deleting an assigned Unit Type | Assigned Unit Type can be deleted. |
| 11 | Products / HSN-SAC | Prevent deleting an assigned HSN/SAC code | Assigned code can be deleted. |
| 12 | Suppliers | Reject email without a domain suffix | `test@gmail` is accepted. |
| 13 | Products / Brands | Delete Brand after its Product is deleted | Stale dependency continues to block Brand deletion. |
| 14 | Suppliers | Reject phone starting outside 6-9 | `1223456789` is accepted. |
| 15 | Branches | Verify Actions-column sorting | Actions sorting control is unavailable. |
| 16 | Product Attributes | Verify row actions | View, Edit, and Delete actions are unavailable. |
| 17 | Purchase Requests / Suppliers | Prevent deleting an assigned Supplier | Supplier assigned to an active Purchase Request can be deleted. |

For every skipped test, remove the skip only after the defect is fixed, execute it against the deployed environment, and update both `skipped.md` and the tracker with the observed result.

## Recommended Implementation Order

1. Repair field-scoped validation and exact-row helper methods so new tests cannot create false passes.
2. Re-run Customer phone, postal-code, and email validation and correct their tracker statuses if required.
3. Strengthen Purchase Request search and row-action tests and re-run the existing cases.
4. Add reusable list-filter and pagination helpers, then cover the highest-use Customer, Supplier, Product, Purchase Request, Purchase, and Sales lists first.
5. Automate negative opening-stock validation.
6. Automate Purchase Request product and branch dependency cases using isolated fixtures.
7. Add Customer type, GST, address, filter, and permission coverage.
8. Add Purchase Request date, quantity, notes, status, GRN lock, and workflow-route coverage.
9. Implement the Sales and Purchases transaction fixtures, then automate the remaining Customer, Supplier, and Product dependency cases.
10. Automate the Manual Payment Voucher numbering defect and Sort Order boundary validation after capturing their exact API responses.
11. Re-test all 17 skipped defects after development fixes and remove resolved skips.
12. Complete the remaining Accounting and Reports milestones.

## Status Summary

- **Not Executed cases copied from tracker:** 6
- **Additional source-review test areas:** 24
- **List modules/groups needing filter and pagination coverage:** 18
- **Active skipped application defects reviewed:** 17
- **New manually observed Voucher/Sort Order defects:** 2
- **Other unfinished milestone areas:** Main Menu workflows, Accounting, and Reports
