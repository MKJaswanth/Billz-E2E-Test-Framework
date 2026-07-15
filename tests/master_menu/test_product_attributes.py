import pytest
from pages.master_menu.product_attributes_page import ProductAttributesPage
from utils.random_data import generate_random_name, generate_random_description

@pytest.fixture
def product_attr_cleanup(logged_in_page):
    created_attrs = []
    yield created_attrs
    attr_page = ProductAttributesPage(logged_in_page)
    for name in created_attrs:
        try:
            attr_page.navigate()
            if attr_page.search_product_attribute(name):
                row = attr_page.page.locator("tr", has=attr_page.page.get_by_text(name, exact=True))
                if row.get_by_title("delete").first.is_visible():
                    attr_page.delete_product_attribute(name)
        except Exception as e:
            print(f"Teardown: Failed to delete product attribute {name}: {e}")

def test_product_attributes_visibility(logged_in_page):
    page_obj = ProductAttributesPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    assert page_obj.is_product_attributes_visible()

def test_add_product_attribute(logged_in_page, product_attr_cleanup):
    page_obj = ProductAttributesPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    
    attr_name = generate_random_name("auto_attr")
    description = generate_random_description("attr_desc")
    
    page_obj.add_product_attribute(name=attr_name, unique=True, description=description)
    product_attr_cleanup.append(attr_name)
    assert page_obj.search_product_attribute(attr_name)

def test_search_product_attribute(logged_in_page, product_attr_cleanup):
    page_obj = ProductAttributesPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    
    attr_name = generate_random_name("auto_attr")
    page_obj.add_product_attribute(name=attr_name)
    product_attr_cleanup.append(attr_name)
    assert page_obj.search_product_attribute(attr_name)

def test_validate_product_attribute(logged_in_page):
    page_obj = ProductAttributesPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    assert page_obj.validate_required_fields()


def test_reject_overlength_product_attribute_name(logged_in_page):
    page_obj = ProductAttributesPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    assert page_obj.validate_name_too_long("A" * 256), (
        "Expected visible validation feedback for an overlength attribute name"
    )


@pytest.mark.skip(
    reason="Known UI gap: Product Attribute rows have no view, edit, or delete actions"
)
def test_product_attribute_row_actions_are_available(
    logged_in_page, product_attr_cleanup
):
    page_obj = ProductAttributesPage(logged_in_page)
    page_obj.navigate()
    attribute_name = generate_random_name("attribute_actions")
    page_obj.add_product_attribute(name=attribute_name)
    product_attr_cleanup.append(attribute_name)
    assert page_obj.has_row_actions(attribute_name), (
        "Expected view, edit, and delete actions for the Product Attribute row"
    )
