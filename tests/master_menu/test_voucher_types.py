import pytest
from pages.master_menu.voucher_types_page import VoucherTypesPage

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
    # Read the real current prefix instead of assuming it — a crashed earlier
    # run may have left a different value, and rollback must restore truth.
    original_prefix = page_obj.get_current_prefix(name)
    new_prefix = "PYM" if original_prefix != "PYM" else "PAY"

    # Register for rollback
    voucher_type_rollback.append((name, original_prefix))
    
    assert page_obj.edit_voucher_type(name, new_prefix)
    
    # Verify prefix is updated in this voucher's own row
    row = page_obj.page.locator("tr", has=page_obj.page.get_by_text(name, exact=True))
    assert row.get_by_text(new_prefix, exact=True).is_visible()
