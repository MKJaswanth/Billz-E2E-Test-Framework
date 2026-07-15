import pytest
from pages.master_menu.branches_page import BranchesPage

@pytest.fixture
def branch_cleanup(logged_in_page):
    created_branches = []
    yield created_branches
    branches_page = BranchesPage(logged_in_page)
    for name in created_branches:
        try:
            branches_page.navigate()
            if branches_page.search_branch(name):
                row = branches_page.page.locator("tr", has=branches_page.page.get_by_text(name, exact=True))
                if row.get_by_title("delete").first.is_visible():
                    branches_page.delete_branch(name)
        except Exception as e:
            print(f"Teardown: Failed to delete branch {name}: {e}")
        branches_page.cleanup_auto_city(name)

def test_branches_visibility(logged_in_page):
    branches_page = BranchesPage(logged_in_page)
    branches_page.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    assert branches_page.is_branches_visible()
    
def test_add_branch(logged_in_page, branch_cleanup):
    branches_page = BranchesPage(logged_in_page)
    branches_page.navigate()
    logged_in_page.wait_for_load_state("networkidle")

    branch_name = branches_page.add_branch()
    branch_cleanup.append(branch_name)
    branches_page.page.get_by_text("Branch created successfully.").wait_for()
    
    assert branches_page.page.get_by_text("Branch created successfully.").is_visible()
    
def test_search_branch(logged_in_page, branch_cleanup):
    branches_page = BranchesPage(logged_in_page)
    branches_page.navigate()
    logged_in_page.wait_for_load_state("networkidle", timeout=10000)

    branch_name = branches_page.add_branch()
    branch_cleanup.append(branch_name)
    
    branch_name2 = branches_page.add_branch()
    branch_cleanup.append(branch_name2)
    
    assert branches_page.search_branch(branch_name)
    
def test_view_branch(logged_in_page, branch_cleanup):
    branches_page = BranchesPage(logged_in_page)
    branches_page.navigate()
    logged_in_page.wait_for_load_state("networkidle", timeout=10000)

    branch_name = branches_page.add_branch()
    branch_cleanup.append(branch_name)
    
    assert branches_page.view_branch(branch_name)
    
def test_edit_branch(logged_in_page, branch_cleanup):
    branches_page = BranchesPage(logged_in_page)
    branches_page.navigate()
    logged_in_page.wait_for_load_state("networkidle", timeout=10000)

    branch_name = branches_page.add_branch()
    branch_cleanup.append(branch_name)
    branch_cleanup.append(branch_name + "_edited")
    
    assert branches_page.edit_branch(branch_name)
    
def test_delete_branch(logged_in_page, branch_cleanup):
    branches_page = BranchesPage(logged_in_page)
    branches_page.navigate()
    logged_in_page.wait_for_load_state("networkidle", timeout=10000)

    branch_name = branches_page.add_branch()
    branch_cleanup.append(branch_name)
    
    assert branches_page.delete_branch(branch_name)
    
def test_retrieve_branch(logged_in_page, branch_cleanup):
    branches_page = BranchesPage(logged_in_page)
    branches_page.navigate()
    logged_in_page.wait_for_load_state("networkidle", timeout=10000)

    branch_name = branches_page.add_branch()
    branch_cleanup.append(branch_name)
    
    assert branches_page.delete_branch(branch_name)
    assert branches_page.retrieve_branch(branch_name)
    
def test_validate_branch(logged_in_page):
    branches_page = BranchesPage(logged_in_page)
    branches_page.navigate()
    logged_in_page.wait_for_load_state("networkidle", timeout=10000)
    
    assert branches_page.validate_branch_name()

def test_duplicate_branch(logged_in_page, branch_cleanup):
    branches_page = BranchesPage(logged_in_page)
    branches_page.navigate()
    logged_in_page.wait_for_load_state("networkidle", timeout=10000)

    branch_name = branches_page.add_branch()
    branch_cleanup.append(branch_name)

    assert branches_page.duplicate_branch_name(branch_name)


@pytest.mark.parametrize("phone", ["123", "abcdefghij"])
def test_validate_branch_phone(logged_in_page, phone):
    branches_page = BranchesPage(logged_in_page)
    branches_page.navigate()
    logged_in_page.wait_for_load_state("networkidle", timeout=10000)
    assert branches_page.validate_invalid_phone(phone), (
        f"Expected visible phone validation feedback for {phone!r}"
    )


@pytest.mark.skip(reason="Known bug: phone numbers starting outside 6-9 are accepted")
def test_reject_branch_phone_with_invalid_start_digit(logged_in_page):
    branches_page = BranchesPage(logged_in_page)
    branches_page.navigate()
    logged_in_page.wait_for_load_state("networkidle", timeout=10000)
    assert branches_page.validate_invalid_phone("1234567890"), (
        "Expected phone validation when the first digit is not 6, 7, 8, or 9"
    )


@pytest.mark.skip(reason="Known UI gap: Branch Actions column has no sorting option")
def test_branch_actions_column_sorting_is_available(logged_in_page):
    branches_page = BranchesPage(logged_in_page)
    branches_page.navigate()
    logged_in_page.wait_for_load_state("networkidle", timeout=10000)
    assert branches_page.has_actions_sorting_control(), (
        "Expected a sorting control in the Branch Actions column"
    )
