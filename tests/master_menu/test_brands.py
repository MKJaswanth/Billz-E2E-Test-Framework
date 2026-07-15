import pytest
from pages.master_menu.brands_page import BrandPage
from utils.random_data import generate_random_description, generate_random_name 

@pytest.fixture
def brand_cleanup(logged_in_page):
    created_brands = []
    yield created_brands
    brand_page = BrandPage(logged_in_page)
    for name in created_brands:
        try:
            brand_page.navigate()
            if brand_page.search_brand(name):
                row = brand_page.page.locator("tr", has=brand_page.page.get_by_text(name, exact=True))
                if row.get_by_title("delete").first.is_visible():
                    brand_page.delete_brand(name)
        except Exception as e:
            print(f"Teardown: Failed to delete brand {name}: {e}")

def test_brands_visibility(logged_in_page):
    brand_page = BrandPage(logged_in_page)
    brand_page.navigate()
    logged_in_page.wait_for_load_state("networkidle", timeout=10000)
    assert brand_page.is_brands_visible()

def test_search_brand(logged_in_page, brand_cleanup):
    name = generate_random_name("auto")
    description = generate_random_description("description")
    brand_page = BrandPage(logged_in_page)
    brand_page.navigate()

    brand_name = brand_page.add_brand(name, description)
    brand_cleanup.append(brand_name)
    assert brand_page.search_brand(brand_name)

def test_add_brand(logged_in_page, brand_cleanup):
    brand_page = BrandPage(logged_in_page)
    brand_page.navigate()
    
    brand_name = generate_random_name("auto_brand")
    description = generate_random_description("description")
    
    brand_page.add_brand(brand_name, description)
    brand_cleanup.append(brand_name)
    assert brand_page.search_brand(brand_name)

def test_edit_brand(logged_in_page, brand_cleanup):
    brand_page = BrandPage(logged_in_page)
    brand_page.navigate()
    
    brand_name = generate_random_name("auto_brand")
    description = generate_random_description("description")
    
    brand_page.add_brand(brand_name, description)
    brand_cleanup.append(brand_name)
    assert brand_page.search_brand(brand_name)
    
    new_name = generate_random_name("updated_brand")
    brand_cleanup.append(new_name)  
    assert brand_page.edit_brand(brand_name, new_name)
    assert brand_page.search_brand(new_name) 

def test_view_brand(logged_in_page, brand_cleanup):
    brand_page = BrandPage(logged_in_page)
    brand_page.navigate()
    brand_name = generate_random_name("auto_brand")
    description = generate_random_description("description")    

    brand_page.add_brand(brand_name, description)
    brand_cleanup.append(brand_name)
    assert brand_page.search_brand(brand_name)
    assert brand_page.view_brand(brand_name)

def test_delete_brand(logged_in_page, brand_cleanup):
    brand_page = BrandPage(logged_in_page)
    brand_page.navigate()

    brand_name = generate_random_name("delete")
    description = generate_random_description("delete des")

    brand_page.add_brand(brand_name, description)
    brand_cleanup.append(brand_name)  
    assert brand_page.delete_brand(brand_name)

def test_retrieve_brand(logged_in_page, brand_cleanup):
    brand_page = BrandPage(logged_in_page)
    brand_page.navigate()

    brand_name = generate_random_name("retrieve")
    description = generate_random_description("retrieve des")

    brand_page.add_brand(brand_name, description)
    brand_cleanup.append(brand_name)
    assert brand_page.retrieve_brand(brand_name)

def test_validate_brand(logged_in_page):
    brand_page = BrandPage(logged_in_page)
    brand_page.navigate()
    assert brand_page.validate_required_fields()


def test_reject_blank_only_brand_name(logged_in_page):
    brand_page = BrandPage(logged_in_page)
    brand_page.navigate()
    assert brand_page.validate_blank_only_name(), (
        "Expected visible validation feedback for a blank-only brand name"
    )


def test_trim_brand_name_whitespace(logged_in_page, brand_cleanup):
    brand_page = BrandPage(logged_in_page)
    brand_page.navigate()
    name = generate_random_name("trimmed_brand")
    description = generate_random_description("trim_validation")
    assert brand_page.validate_name_is_trimmed(name, description)
    brand_cleanup.append(name)

def test_duplicate_brand_name(logged_in_page, brand_cleanup):
    brand_page = BrandPage(logged_in_page)
    brand_page.navigate()
    
    brand_name = generate_random_name("dup_brand")
    description = generate_random_description("description")
    brand_page.add_brand(brand_name, description)
    brand_cleanup.append(brand_name)
    
    assert brand_page.validate_duplicate_brand(brand_name, description)

