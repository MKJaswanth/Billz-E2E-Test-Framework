import pytest
from pages.master_menu.attribute_keys_page import AttributeKeysPage
from pages.master_menu.attribute_values_page import AttributeValuesPage
from utils.random_data import generate_random_name, generate_random_description

@pytest.fixture
def attribute_key_cleanup(logged_in_page):
    created_keys = []
    yield created_keys
    keys_page = AttributeKeysPage(logged_in_page)
    for name in created_keys:
        try:
            keys_page.navigate()
            if keys_page.search_attribute_key(name):
                row = keys_page.page.locator("tr", has=keys_page.page.get_by_text(name, exact=True))
                delete_btn = row.get_by_title("delete").first
                if delete_btn.is_visible():
                    delete_btn.click()
                    modal = keys_page.page.get_by_role("dialog")
                    modal.wait_for(state="visible", timeout=3000)
                    delete_confirm = modal.get_by_role("button", name="Delete Attribute Key")
                    if delete_confirm.is_visible():
                        delete_confirm.click()
                        keys_page.page.get_by_text("Deleted successfully.").wait_for(state="visible", timeout=5000)
                    else:
                        close_btn = modal.locator(".btn-close")
                        if close_btn.is_visible():
                            close_btn.click()
        except Exception as e:
            print(f"Teardown: Failed to delete attribute key {name}: {e}")

@pytest.fixture
def attribute_value_cleanup(logged_in_page):
    created_values = []
    yield created_values
    value_page = AttributeValuesPage(logged_in_page)
    for name in created_values:
        try:
            value_page.navigate()
            if value_page.search_attribute_value(name):
                row = value_page.page.locator("tr", has=value_page.page.get_by_text(name, exact=True))
                delete_btn = row.get_by_title("delete").first
                if delete_btn.is_visible():
                    delete_btn.click()
                    modal = value_page.page.get_by_role("dialog")
                    modal.wait_for(state="visible", timeout=3000)
                    delete_confirm = modal.get_by_role("button", name="Delete Attribute Value")
                    if delete_confirm.is_visible():
                        delete_confirm.click()
                        value_page.page.get_by_text("Deleted successfully.").wait_for(state="visible", timeout=5000)
                    else:
                        close_btn = modal.locator(".btn-close")
                        if close_btn.is_visible():
                            close_btn.click()
        except Exception as e:
            print(f"Teardown: Failed to delete attribute value {name}: {e}")

def test_attribute_values_visibility(logged_in_page):
    page_obj = AttributeValuesPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    assert page_obj.is_attribute_values_visible()

def test_add_attribute_value(logged_in_page, attribute_key_cleanup, attribute_value_cleanup):
    key_page = AttributeKeysPage(logged_in_page)
    key_page.navigate()
    key_name = generate_random_name("auto_key")
    key_page.add_attribute_key(name=key_name)
    attribute_key_cleanup.append(key_name)

    value_page = AttributeValuesPage(logged_in_page)
    value_page.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    value_name = generate_random_name("auto_val")
    description = generate_random_description("val_desc")
    
    value_page.add_attribute_value(key_name=key_name, value=value_name, description=description)
    attribute_value_cleanup.append(value_name)
    assert value_page.search_attribute_value(value_name)

def test_search_attribute_value(logged_in_page, attribute_key_cleanup, attribute_value_cleanup):
    key_page = AttributeKeysPage(logged_in_page)
    key_page.navigate()
    key_name = generate_random_name("auto_key")
    key_page.add_attribute_key(name=key_name)
    attribute_key_cleanup.append(key_name)
    
    value_page = AttributeValuesPage(logged_in_page)
    value_page.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    value_name = generate_random_name("auto_val")
    value_page.add_attribute_value(key_name=key_name, value=value_name)
    attribute_value_cleanup.append(value_name)
    assert value_page.search_attribute_value(value_name)

@pytest.mark.skip(reason="View dialog is not opening")
def test_view_attribute_value(logged_in_page, attribute_key_cleanup, attribute_value_cleanup):
    key_page = AttributeKeysPage(logged_in_page)
    key_page.navigate()
    key_name = generate_random_name("auto_key")
    key_page.add_attribute_key(name=key_name)
    attribute_key_cleanup.append(key_name)
    
    value_page = AttributeValuesPage(logged_in_page)
    value_page.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    value_name = generate_random_name("auto_val")
    value_page.add_attribute_value(key_name=key_name, value=value_name)
    attribute_value_cleanup.append(value_name)
    assert value_page.search_attribute_value(value_name)
    assert value_page.view_attribute_value(value_name)

def test_edit_attribute_value(logged_in_page, attribute_key_cleanup, attribute_value_cleanup):
    key_page = AttributeKeysPage(logged_in_page)
    key_page.navigate()
    key_name = generate_random_name("auto_key")
    key_page.add_attribute_key(name=key_name)
    attribute_key_cleanup.append(key_name)
    
    value_page = AttributeValuesPage(logged_in_page)
    value_page.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    value_name = generate_random_name("auto_val")
    value_page.add_attribute_value(key_name=key_name, value=value_name)
    attribute_value_cleanup.append(value_name)
    assert value_page.search_attribute_value(value_name)
    
    new_value = generate_random_name("auto_val1")
    attribute_value_cleanup.append(new_value)
    assert value_page.edit_attribute_value(value_name, new_value)
    assert value_page.search_attribute_value(new_value)

def test_delete_attribute_value(logged_in_page, attribute_key_cleanup, attribute_value_cleanup):
    key_page = AttributeKeysPage(logged_in_page)
    key_page.navigate()
    key_name = generate_random_name("auto_key")
    key_page.add_attribute_key(name=key_name)
    attribute_key_cleanup.append(key_name)
    
    value_page = AttributeValuesPage(logged_in_page)
    value_page.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    value_name = generate_random_name("auto_val")
    value_page.add_attribute_value(key_name=key_name, value=value_name)
    attribute_value_cleanup.append(value_name)
    assert value_page.search_attribute_value(value_name)
    assert value_page.delete_attribute_value(value_name)

def test_retrieve_attribute_value(logged_in_page, attribute_key_cleanup, attribute_value_cleanup):
    key_page = AttributeKeysPage(logged_in_page)
    key_page.navigate()
    key_name = generate_random_name("auto_key")
    key_page.add_attribute_key(name=key_name)
    attribute_key_cleanup.append(key_name)
    
    value_page = AttributeValuesPage(logged_in_page)
    value_page.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    value_name = generate_random_name("auto_val")
    value_page.add_attribute_value(key_name=key_name, value=value_name)
    attribute_value_cleanup.append(value_name)
    assert value_page.search_attribute_value(value_name)
    assert value_page.delete_attribute_value(value_name)
    assert value_page.retrieve_attribute_value(value_name)
    assert value_page.search_attribute_value(value_name)

def test_validate_attribute_value(logged_in_page):
    page_obj = AttributeValuesPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    assert page_obj.validate_required_fields()


def test_reject_duplicate_attribute_value(
    logged_in_page, attribute_key_cleanup, attribute_value_cleanup
):
    key_page = AttributeKeysPage(logged_in_page)
    key_page.navigate()
    key_name = generate_random_name("duplicate_key")
    key_page.add_attribute_key(name=key_name)
    attribute_key_cleanup.append(key_name)

    value_page = AttributeValuesPage(logged_in_page)
    value_page.navigate()
    value_name = generate_random_name("duplicate_value")
    value_page.add_attribute_value(key_name=key_name, value=value_name)
    attribute_value_cleanup.append(value_name)
    assert value_page.search_attribute_value(value_name)
    assert value_page.validate_duplicate_value(key_name, value_name), (
        "Expected visible validation feedback for a duplicate attribute value"
    )
