import pytest
from pages.master_menu.enquiry_types_page import EnquiryTypesPage
from utils.random_data import generate_random_name

@pytest.fixture
def enquiry_type_cleanup(logged_in_page):
    created_types = []
    yield created_types
    page_obj = EnquiryTypesPage(logged_in_page)
    for name in created_types:
        try:
            page_obj.navigate()
            if page_obj.search_enquiry_type(name):
                row = page_obj.page.locator("tr", has=page_obj.page.get_by_text(name, exact=True))
                delete_btn = row.get_by_title("delete").first
                if delete_btn.is_visible() and delete_btn.is_enabled():
                    delete_btn.click()
                    modal = page_obj.page.get_by_role("dialog")
                    modal.wait_for(state="visible", timeout=3000)
                    delete_confirm = modal.get_by_role("button", name="Delete Enquiry")
                    if delete_confirm.is_visible():
                        delete_confirm.click()
                        page_obj.page.get_by_text("Deleted successfully.").first.wait_for(state="visible", timeout=5000)
                    else:
                        close_btn = modal.locator(".btn-close")
                        if close_btn.is_visible():
                            close_btn.click()
        except Exception as e:
            print(f"Teardown: Failed to delete enquiry type {name}: {e}")

def test_enquiry_types_visibility(logged_in_page):
    page_obj = EnquiryTypesPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    assert page_obj.is_enquiry_types_visible()

def test_add_enquiry_type(logged_in_page, enquiry_type_cleanup):
    page_obj = EnquiryTypesPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")

    name = generate_random_name("auto_enq")
    page_obj.add_enquiry_type(name, notes="test notes")
    enquiry_type_cleanup.append(name)
    assert page_obj.search_enquiry_type(name)

def test_search_enquiry_type(logged_in_page, enquiry_type_cleanup):
    page_obj = EnquiryTypesPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")

    name = generate_random_name("auto_enq")
    page_obj.add_enquiry_type(name)
    enquiry_type_cleanup.append(name)
    assert page_obj.search_enquiry_type(name)

def test_view_enquiry_type(logged_in_page, enquiry_type_cleanup):
    page_obj = EnquiryTypesPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")

    name = generate_random_name("auto_enq")
    page_obj.add_enquiry_type(name)
    enquiry_type_cleanup.append(name)
    assert page_obj.view_enquiry_type(name)

def test_edit_enquiry_type(logged_in_page, enquiry_type_cleanup):
    page_obj = EnquiryTypesPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")

    name = generate_random_name("auto_enq")
    page_obj.add_enquiry_type(name)
    enquiry_type_cleanup.append(name)
    assert page_obj.search_enquiry_type(name)

    new_name = generate_random_name("auto_enq_new")
    enquiry_type_cleanup.append(new_name)
    assert page_obj.edit_enquiry_type(name, new_name)
    assert page_obj.search_enquiry_type(new_name)

def test_delete_enquiry_type(logged_in_page, enquiry_type_cleanup):
    page_obj = EnquiryTypesPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")

    name = generate_random_name("auto_enq")
    page_obj.add_enquiry_type(name)
    enquiry_type_cleanup.append(name)
    assert page_obj.search_enquiry_type(name)
    assert page_obj.delete_enquiry_type(name)

def test_retrieve_enquiry_type(logged_in_page, enquiry_type_cleanup):
    page_obj = EnquiryTypesPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")

    name = generate_random_name("auto_enq")
    page_obj.add_enquiry_type(name)
    enquiry_type_cleanup.append(name)
    assert page_obj.search_enquiry_type(name)
    assert page_obj.delete_enquiry_type(name)
    assert page_obj.retrieve_enquiry_type(name)
    assert page_obj.search_enquiry_type(name)
