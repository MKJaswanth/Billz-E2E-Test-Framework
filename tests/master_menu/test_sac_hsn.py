import random
import pytest
from pages.master_menu.sac_hsn_page import SacHsnPage
from utils.random_data import generate_random_description

def generate_random_numeric_code():
    return str(random.randint(100000, 999999))

@pytest.fixture
def sac_hsn_cleanup(logged_in_page):
    created_codes = []
    yield created_codes
    page_obj = SacHsnPage(logged_in_page)
    for code in created_codes:
        try:
            page_obj.navigate()
            if page_obj.search_sac_hsn_code(code):
                row = page_obj.page.locator("tr", has=page_obj.page.get_by_text(code, exact=True))
                delete_btn = row.get_by_title("delete").first
                if delete_btn.is_visible() and delete_btn.is_enabled():
                    delete_btn.click()
                    modal = page_obj.page.get_by_role("dialog")
                    modal.wait_for(state="visible", timeout=3000)
                    delete_confirm = modal.get_by_role("button", name="Delete Code")
                    if delete_confirm.is_visible():
                        delete_confirm.click()
                        page_obj.page.get_by_text("Deleted successfully.").first.wait_for(state="visible", timeout=5000)
                    else:
                        close_btn = modal.locator(".btn-close")
                        if close_btn.is_visible():
                            close_btn.click()
        except Exception as e:
            print(f"Teardown: Failed to delete SAC/HSN code {code}: {e}")

def test_sac_hsn_visibility(logged_in_page):
    page_obj = SacHsnPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    assert page_obj.is_sac_hsn_visible()

def test_add_sac_hsn_code(logged_in_page, sac_hsn_cleanup):
    page_obj = SacHsnPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")

    code = generate_random_numeric_code()
    page_obj.add_sac_hsn_code("SAC", code, description="test description")
    sac_hsn_cleanup.append(code)
    assert page_obj.search_sac_hsn_code(code)

def test_search_sac_hsn_code(logged_in_page, sac_hsn_cleanup):
    page_obj = SacHsnPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")

    code = generate_random_numeric_code()
    page_obj.add_sac_hsn_code("SAC", code)
    sac_hsn_cleanup.append(code)
    assert page_obj.search_sac_hsn_code(code)

def test_view_sac_hsn_code(logged_in_page, sac_hsn_cleanup):
    page_obj = SacHsnPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")

    code = generate_random_numeric_code()
    page_obj.add_sac_hsn_code("SAC", code)
    sac_hsn_cleanup.append(code)
    assert page_obj.view_sac_hsn_code(code)

def test_edit_sac_hsn_code(logged_in_page, sac_hsn_cleanup):
    page_obj = SacHsnPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")

    code = generate_random_numeric_code()
    page_obj.add_sac_hsn_code("SAC", code)
    sac_hsn_cleanup.append(code)
    assert page_obj.search_sac_hsn_code(code)

    new_code = generate_random_numeric_code()
    sac_hsn_cleanup.append(new_code)
    assert page_obj.edit_sac_hsn_code(code, new_code)
    assert page_obj.search_sac_hsn_code(new_code)

def test_delete_sac_hsn_code(logged_in_page, sac_hsn_cleanup):
    page_obj = SacHsnPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")

    code = generate_random_numeric_code()
    page_obj.add_sac_hsn_code("SAC", code)
    sac_hsn_cleanup.append(code)
    assert page_obj.search_sac_hsn_code(code)
    assert page_obj.delete_sac_hsn_code(code)

def test_retrieve_sac_hsn_code(logged_in_page, sac_hsn_cleanup):
    page_obj = SacHsnPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")

    code = generate_random_numeric_code()
    page_obj.add_sac_hsn_code("SAC", code)
    sac_hsn_cleanup.append(code)
    assert page_obj.search_sac_hsn_code(code)
    assert page_obj.delete_sac_hsn_code(code)
    assert page_obj.retrieve_sac_hsn_code(code)
    assert page_obj.search_sac_hsn_code(code)


@pytest.mark.parametrize(
    "invalid_code",
    [
        pytest.param("ABCDEF", id="alphabetic"),
        pytest.param("12", id="too-short"),
        pytest.param("123456789012345", id="too-long"),
    ],
)
def test_validate_sac_hsn_code_format(logged_in_page, invalid_code):
    page_obj = SacHsnPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    assert page_obj.validate_invalid_code(invalid_code), (
        f"Expected visible code validation feedback for {invalid_code!r}"
    )

def test_duplicate_sac_hsn_code(logged_in_page, sac_hsn_cleanup):
    page_obj = SacHsnPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    
    code = generate_random_numeric_code()
    page_obj.add_sac_hsn_code("SAC", code)
    sac_hsn_cleanup.append(code)
    
    assert page_obj.validate_duplicate_sac_hsn_code(code)

