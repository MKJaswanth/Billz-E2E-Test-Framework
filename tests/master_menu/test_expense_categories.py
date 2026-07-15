import pytest
from pages.master_menu.expense_categories_page import ExpenseCategoriesPage
from utils.random_data import generate_random_name

@pytest.fixture
def expense_category_cleanup(logged_in_page):
    created_categories = []
    yield created_categories
    cat_page = ExpenseCategoriesPage(logged_in_page)
    for name in created_categories:
        try:
            cat_page.navigate()
            if cat_page.search_expense_category(name):
                row = cat_page.page.locator("tr", has=cat_page.page.get_by_text(name, exact=True))
                delete_btn = row.get_by_title("delete").first
                if delete_btn.is_visible() and delete_btn.is_enabled():
                    delete_btn.click()
                    modal = cat_page.page.get_by_role("dialog")
                    modal.wait_for(state="visible", timeout=3000)
                    delete_confirm = modal.get_by_role("button", name="Delete Category")
                    if delete_confirm.is_visible():
                        delete_confirm.click()
                        cat_page.page.get_by_text("Deleted successfully.").first.wait_for(state="visible", timeout=5000)
                    else:
                        close_btn = modal.locator(".btn-close")
                        if close_btn.is_visible():
                            close_btn.click()
        except Exception as e:
            print(f"Teardown: Failed to delete expense category {name}: {e}")

def test_expense_categories_visibility(logged_in_page):
    page_obj = ExpenseCategoriesPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    assert page_obj.is_expense_categories_visible()

def test_add_expense_category(logged_in_page, expense_category_cleanup):
    page_obj = ExpenseCategoriesPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")

    name = generate_random_name("auto_expense")
    page_obj.add_expense_category(name, description="test description")
    expense_category_cleanup.append(name)
    assert page_obj.search_expense_category(name)

def test_search_expense_category(logged_in_page, expense_category_cleanup):
    page_obj = ExpenseCategoriesPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")

    name = generate_random_name("auto_expense")
    page_obj.add_expense_category(name)
    expense_category_cleanup.append(name)
    assert page_obj.search_expense_category(name)

@pytest.mark.skip(reason="View option is not available for expense categories")
def test_view_expense_category(logged_in_page, expense_category_cleanup):
    page_obj = ExpenseCategoriesPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")

    name = generate_random_name("auto_expense")
    page_obj.add_expense_category(name)
    expense_category_cleanup.append(name)
    assert page_obj.search_expense_category(name)

def test_edit_expense_category(logged_in_page, expense_category_cleanup):
    page_obj = ExpenseCategoriesPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")

    name = generate_random_name("auto_expense")
    page_obj.add_expense_category(name)
    expense_category_cleanup.append(name)
    assert page_obj.search_expense_category(name)

    new_name = generate_random_name("auto_expense1")
    expense_category_cleanup.append(new_name)
    assert page_obj.edit_expense_category(name, new_name)
    assert page_obj.search_expense_category(new_name)

def test_delete_expense_category(logged_in_page, expense_category_cleanup):
    page_obj = ExpenseCategoriesPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")

    name = generate_random_name("auto_expense")
    page_obj.add_expense_category(name)
    expense_category_cleanup.append(name)
    assert page_obj.search_expense_category(name)
    assert page_obj.delete_expense_category(name)

def test_retrieve_expense_category(logged_in_page, expense_category_cleanup):
    page_obj = ExpenseCategoriesPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")

    name = generate_random_name("auto_expense")
    page_obj.add_expense_category(name)
    expense_category_cleanup.append(name)
    assert page_obj.search_expense_category(name)
    assert page_obj.delete_expense_category(name)
    assert page_obj.retrieve_expense_category(name)
    assert page_obj.search_expense_category(name)


def test_reject_duplicate_expense_category(logged_in_page, expense_category_cleanup):
    page_obj = ExpenseCategoriesPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    name = generate_random_name("duplicate_expense")
    page_obj.add_expense_category(name)
    expense_category_cleanup.append(name)
    assert page_obj.validate_duplicate_category(name), (
        "Expected visible validation feedback for a duplicate expense category"
    )
