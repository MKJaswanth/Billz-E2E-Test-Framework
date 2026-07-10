import pytest
from pages.master_menu.attribute_keys_page import AttributeKeysPage
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
                if row.get_by_title("delete").first.is_visible():
                    keys_page.delete_attribute_key(name)
        except Exception as e:
            print(f"Teardown: Failed to delete attribute key {name}: {e}")

def test_attribute_keys_visibility(logged_in_page):
    page_obj = AttributeKeysPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    assert page_obj.is_attribute_keys_visible()

def test_add_attribute_key(logged_in_page, attribute_key_cleanup):
    page_obj = AttributeKeysPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    
    name = generate_random_name("auto_key")
    description = generate_random_description("key_desc")
    page_obj.add_attribute_key(name=name, description=description)
    attribute_key_cleanup.append(name)
    assert page_obj.search_attribute_key(name)

def test_search_attribute_key(logged_in_page, attribute_key_cleanup):
    page_obj = AttributeKeysPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    
    name = generate_random_name("auto_key")
    description = generate_random_description("key_desc")
    page_obj.add_attribute_key(name=name, description=description)
    attribute_key_cleanup.append(name)
    assert page_obj.search_attribute_key(name)

def test_view_attribute_key(logged_in_page, attribute_key_cleanup):
    page_obj = AttributeKeysPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    
    name = generate_random_name("auto_key")
    description = generate_random_description("key_desc")
    page_obj.add_attribute_key(name=name, description=description)
    attribute_key_cleanup.append(name)
    assert page_obj.search_attribute_key(name)
    assert page_obj.view_attribute_key(name)

def test_edit_attribute_key(logged_in_page, attribute_key_cleanup):
    page_obj = AttributeKeysPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    
    name = generate_random_name("auto_key")
    description = generate_random_description("key_desc")
    page_obj.add_attribute_key(name=name, description=description)
    attribute_key_cleanup.append(name)
    assert page_obj.search_attribute_key(name)
    
    new_name = generate_random_name("auto_key1")
    attribute_key_cleanup.append(new_name)
    assert page_obj.edit_attribute_key(name, new_name)
    assert page_obj.search_attribute_key(new_name)

def test_delete_attribute_key(logged_in_page, attribute_key_cleanup):
    page_obj = AttributeKeysPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    
    name = generate_random_name("auto_key")
    description = generate_random_description("key_desc")
    page_obj.add_attribute_key(name=name, description=description)
    attribute_key_cleanup.append(name)
    assert page_obj.search_attribute_key(name)
    assert page_obj.delete_attribute_key(name)

def test_retrieve_attribute_key(logged_in_page, attribute_key_cleanup):
    page_obj = AttributeKeysPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    
    name = generate_random_name("auto_key")
    description = generate_random_description("key_desc")
    page_obj.add_attribute_key(name=name, description=description)
    attribute_key_cleanup.append(name)
    assert page_obj.search_attribute_key(name)
    assert page_obj.delete_attribute_key(name)
    assert page_obj.retrieve_attribute_key(name)
    assert page_obj.search_attribute_key(name)

def test_validate_attribute_key(logged_in_page):
    page_obj = AttributeKeysPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    assert page_obj.validate_required_fields()
