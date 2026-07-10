import pytest
from pages.master_menu.voucher_types_page import VoucherTypesPage
from utils.random_data import generate_random_name

@pytest.fixture
def voucher_type_rollback(logged_in_page):
    edited_voucher_types = []
    yield edited_voucher_types
    page_obj = VoucherTypesPage(logged_in_page)
    for name, orig_prefix in edited_voucher_types:
        try:
            page_obj.navigate()
            page_obj.edit_voucher_type(name, orig_prefix)
        except Exception as e:
            print(f"Teardown: Failed to rollback voucher type {name}: {e}")

def test_voucher_types_visibility(logged_in_page):
    page_obj = VoucherTypesPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    assert page_obj.is_voucher_types_visible()

def test_edit_voucher_type(logged_in_page, voucher_type_rollback):
    page_obj = VoucherTypesPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    
    name = "Payment Voucher"
    original_prefix = "PAY"
    new_prefix = "PYM"
    
    # Register for rollback
    voucher_type_rollback.append((name, original_prefix))
    
    assert page_obj.edit_voucher_type(name, new_prefix)
    
    # Verify prefix is updated in the table
    row = page_obj.page.locator("tr", has=page_obj.page.get_by_text(name, exact=True))
    assert page_obj.page.get_by_text(new_prefix, exact=True).is_visible()
