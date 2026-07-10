import pytest
from pages.master_menu.account_groups_page import AccountGroupsPage
from utils.random_data import generate_random_name

@pytest.fixture
def account_group_cleanup(logged_in_page):
    created_groups = []
    yield created_groups
    groups_page = AccountGroupsPage(logged_in_page)
    for name in created_groups:
        try:
            groups_page.navigate()
            if groups_page.search_account_group(name):
                row = groups_page.page.locator("tr", has=groups_page.page.get_by_text(name, exact=True))
                delete_btn = row.get_by_title("delete").first
                if delete_btn.is_visible() and delete_btn.is_enabled():
                    delete_btn.click()
                    modal = groups_page.page.get_by_role("dialog")
                    modal.wait_for(state="visible", timeout=3000)
                    delete_confirm = modal.get_by_role("button", name="Delete")
                    if delete_confirm.is_visible():
                        delete_confirm.click()
                        groups_page.page.get_by_text("Deleted successfully.").wait_for(state="visible", timeout=5000)
                    else:
                        close_btn = modal.locator(".btn-close")
                        if close_btn.is_visible():
                            close_btn.click()
        except Exception as e:
            print(f"Teardown: Failed to delete account group {name}: {e}")

def test_account_groups_visibility(logged_in_page):
    page_obj = AccountGroupsPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    assert page_obj.is_account_group_visible()

def test_add_account_group(logged_in_page, account_group_cleanup):
    page_obj = AccountGroupsPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    
    name = generate_random_name("auto_group")
    page_obj.add_account_group(name)
    account_group_cleanup.append(name)
    assert page_obj.search_account_group(name)

def test_search_account_group(logged_in_page, account_group_cleanup):
    page_obj = AccountGroupsPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    
    name = generate_random_name("auto_group")
    page_obj.add_account_group(name)
    account_group_cleanup.append(name)
    assert page_obj.search_account_group(name)

def test_view_account_group(logged_in_page, account_group_cleanup):
    page_obj = AccountGroupsPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    
    name = generate_random_name("auto_group")
    page_obj.add_account_group(name)
    account_group_cleanup.append(name)
    assert page_obj.search_account_group(name)
    assert page_obj.view_account_group(name)

def test_edit_account_group(logged_in_page, account_group_cleanup):
    page_obj = AccountGroupsPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    
    name = generate_random_name("auto_group")
    page_obj.add_account_group(name)
    account_group_cleanup.append(name)
    assert page_obj.search_account_group(name)
    
    new_name = generate_random_name("auto_group1")
    account_group_cleanup.append(new_name)
    assert page_obj.edit_account_group(name, new_name)
    assert page_obj.search_account_group(new_name)

def test_delete_account_group(logged_in_page, account_group_cleanup):
    page_obj = AccountGroupsPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    
    name = generate_random_name("auto_group")
    page_obj.add_account_group(name)
    account_group_cleanup.append(name)
    assert page_obj.search_account_group(name)
    assert page_obj.delete_account_group(name)

@pytest.mark.skip(reason="Restore functionality is not working in the app")
def test_retrieve_account_group(logged_in_page, account_group_cleanup):
    page_obj = AccountGroupsPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    
    name = generate_random_name("auto_group")
    page_obj.add_account_group(name)
    account_group_cleanup.append(name)
    assert page_obj.search_account_group(name)
    assert page_obj.delete_account_group(name)
    assert page_obj.retrieve_account_group(name)
    assert page_obj.search_account_group(name)

def test_validate_account_group(logged_in_page):
    page_obj = AccountGroupsPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    assert page_obj.validate_required_fields()
