# Skipped Automation Tests

This file tracks test cases in the test suite that have been skipped due to application-side issues or missing functionality.

---

| #   | Test File                                      | Test Case                            | Skip Reason                                                                  |
| --- | ---------------------------------------------- | ------------------------------------ | ---------------------------------------------------------------------------- |
| 1   | `tests/master_menu/test_attribute_values.py`   | `test_view_attribute_value`          | View dialog is not opening in the UI                                         |
| 2   | `tests/master_menu/test_account_groups.py`     | `test_retrieve_account_group`        | Restore functionality is not working in the app                              |
| 3   | `tests/master_menu/test_expense_categories.py` | `test_view_expense_category`         | View option is not available for expense categories                          |
| 4   | `tests/master_menu/test_racks.py`              | `test_delete_branch_containing_rack` | System currently allows deleting a branch that contains an active rack (bug) |
| 5   | `tests/master_menu/test_users.py`              | `test_reject_user_email_without_valid_domain_suffix` | User email without a valid domain suffix is accepted (bug)       |
| 6   | `tests/master_menu/test_branches.py`           | `test_reject_branch_phone_with_invalid_start_digit` | Phone numbers starting outside 6-9 are accepted (bug)            |
| 7   | `tests/master_menu/test_bank_accounts.py`      | `test_reject_alphanumeric_bank_account_number` | Alphanumeric bank account numbers are accepted (bug)             |
| 8   | `tests/master_menu/test_cities.py`             | `test_reject_city_name_containing_numbers` | City names containing numbers are accepted (bug)                 |
| 9   | `tests/main_menu/test_products.py`             | `test_delete_category_assigned_to_product_is_blocked` | Category assigned to an active product can be deleted (bug)      |
| 10  | `tests/main_menu/test_products.py`             | `test_delete_unit_type_assigned_to_product_is_blocked` | Unit type assigned to an active product can be deleted (bug)     |
| 11  | `tests/main_menu/test_products.py`             | `test_delete_hsn_sac_assigned_to_product_is_blocked` | HSN/SAC code assigned to an active product can be deleted (bug)  |
| 12  | `tests/main_menu/test_suppliers.py`            | `test_validate_supplier_field_formats[email-without-domain-suffix]` | Supplier email `test@gmail` is accepted without a valid suffix (bug) |
| 13  | `tests/main_menu/test_products.py`             | `test_delete_brand_after_assigned_product_is_deleted` | Brand remains undeletable after its assigned product is deleted (bug) |
| 14  | `tests/main_menu/test_suppliers.py`            | `test_validate_supplier_field_formats[phone-invalid-start-digit]` | Supplier phone `1223456789` is accepted although it does not start with 6-9 (bug) |
| 15  | `tests/master_menu/test_branches.py`           | `test_branch_actions_column_sorting_is_available` | Branch Actions column has no sorting option (UI gap)              |
| 16  | `tests/master_menu/test_product_attributes.py` | `test_product_attribute_row_actions_are_available` | Product Attribute rows have no view, edit, or delete actions (UI gap) |
| 17  | `tests/main_menu/test_purchase_request.py`     | `test_delete_supplier_assigned_to_purchase_request_is_blocked` | Supplier assigned to an active purchase request can be deleted (bug) |
| 18  | `tests/main_menu/test_expenses.py`             | All test cases                                                 | Expenses module throws 403 Forbidden error (App-side permission bug, fix pending) |

---

**Total Skipped:** 18

### Removed (no longer skipped in code)
- `tests/main_menu/test_products.py` → `test_import_products`
- `tests/main_menu/test_products.py` → `test_add_product`
- `tests/main_menu/test_suppliers.py` → `test_import_supplier`
- `tests/master_menu/test_users.py` → `test_delete_role_assigned_to_user`
