import pytest
from pages.master_menu.categories_page import CategoriesPage
from utils.random_data import generate_random_name, generate_random_description

@pytest.fixture
def category_cleanup(logged_in_page):
    created_categories = []
    yield created_categories
    categories_page = CategoriesPage(logged_in_page)
    for name in created_categories:
        try:
            categories_page.navigate()
            if categories_page.search_category(name):
                row = categories_page.page.locator("tr", has=categories_page.page.get_by_text(name, exact=True))
                if row.get_by_title("delete").first.is_visible():
                    categories_page.delete_category(name)
        except Exception as e:
            print(f"Teardown: Failed to delete category {name}: {e}")

def test_categories_visibility(logged_in_page):
    categories_page = CategoriesPage(logged_in_page)
    categories_page.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    assert categories_page.is_categories_visible()

def test_add_category(logged_in_page, category_cleanup):
    categories_page = CategoriesPage(logged_in_page)
    categories_page.navigate()
    
    category_name = generate_random_name("auto_cat")
    description = generate_random_description("description")
    
    categories_page.add_category(name=category_name, description=description)
    category_cleanup.append(category_name)
    assert categories_page.search_category(category_name)

def test_edit_category(logged_in_page, category_cleanup):
    categories_page = CategoriesPage(logged_in_page)
    categories_page.navigate()
    
    category_name = generate_random_name("auto_edit_cat")
    description = generate_random_description("edit_description")
    
    categories_page.add_category(name=category_name, description=description)
    category_cleanup.append(category_name)
    assert categories_page.search_category(category_name)
    
    new_name = generate_random_name("updated_cat")
    category_cleanup.append(new_name)
    assert categories_page.edit_category(category_name, new_name)
    assert categories_page.search_category(new_name)
    assert not categories_page.search_category(category_name)

def test_delete_category(logged_in_page, category_cleanup):
    categories_page = CategoriesPage(logged_in_page)
    categories_page.navigate()
    
    category_name = generate_random_name("auto_delete_cat")
    description = generate_random_description("delete_description")
    
    categories_page.add_category(name=category_name, description=description)
    category_cleanup.append(category_name)
    assert categories_page.search_category(category_name)
    assert categories_page.delete_category(category_name)   

def test_retrieve_category(logged_in_page, category_cleanup):
    categories_page = CategoriesPage(logged_in_page)
    categories_page.navigate()
    
    category_name = generate_random_name("auto_retrieve_cat")
    description = generate_random_description("retrieve_description")
    
    categories_page.add_category(name=category_name, description=description)
    category_cleanup.append(category_name)
    assert categories_page.search_category(category_name)
    assert categories_page.delete_category(category_name)
    assert categories_page.retrieve_category(category_name)
    assert categories_page.search_category(category_name)   

def test_view_category(logged_in_page, category_cleanup):
    categories_page = CategoriesPage(logged_in_page)
    categories_page.navigate()
    
    category_name = generate_random_name("auto_view_cat")
    description = generate_random_description("view_description")
    
    categories_page.add_category(name=category_name, description=description)
    category_cleanup.append(category_name)
    assert categories_page.search_category(category_name)
    assert categories_page.view_category(category_name)

def test_validate_required_fields(logged_in_page):
    categories_page = CategoriesPage(logged_in_page)
    categories_page.navigate()
    assert categories_page.validate_required_fields()   