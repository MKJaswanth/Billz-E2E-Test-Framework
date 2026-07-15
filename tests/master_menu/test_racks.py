import pytest
from pages.master_menu.racks_page import RacksPage
from pages.master_menu.branches_page import BranchesPage
from utils.random_data import generate_random_name, generate_random_code


@pytest.fixture
def temp_branch(logged_in_page):
    branches_page = BranchesPage(logged_in_page)
    branches_page.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    branch_name = branches_page.add_branch()

    yield branch_name

    try:
        branches_page.navigate()
        if branches_page.search_branch(branch_name):
            row = branches_page.page.locator(
                "tr", has=branches_page.page.get_by_text(branch_name, exact=True)
            )
            if row.get_by_title("delete").first.is_visible():
                branches_page.delete_branch(branch_name)
    except Exception as e:
        print(f"Teardown: Failed to delete branch {branch_name}: {e}")
    branches_page.cleanup_auto_city(branch_name)


@pytest.fixture
def rack_cleanup(logged_in_page):
    created_racks = []
    yield created_racks
    page_obj = RacksPage(logged_in_page)
    for name in created_racks:
        try:
            page_obj.navigate()
            if page_obj.search_rack(name):
                row = page_obj.page.locator(
                    "tr", has=page_obj.page.get_by_text(name, exact=True)
                )
                delete_btn = row.get_by_title("delete").first
                if delete_btn.is_visible() and delete_btn.is_enabled():
                    delete_btn.click()
                    modal = page_obj.page.get_by_role("dialog")
                    modal.wait_for(state="visible", timeout=3000)
                    delete_confirm = modal.get_by_role("button", name="Delete Rack")
                    if delete_confirm.is_visible():
                        delete_confirm.click()
                        page_obj.page.get_by_text("Deleted successfully.").first.wait_for(
                            state="visible", timeout=5000
                        )
                    else:
                        close_btn = modal.locator(".btn-close")
                        if close_btn.is_visible():
                            close_btn.click()
        except Exception as e:
            print(f"Teardown: Failed to delete rack {name}: {e}")


def test_racks_visibility(logged_in_page):
    page_obj = RacksPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    assert page_obj.is_racks_visible()


def test_add_rack(logged_in_page, temp_branch, rack_cleanup):
    page_obj = RacksPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    name = generate_random_name("auto_rack")
    code = generate_random_code("RK")
    page_obj.add_rack(name, code, branch_name=temp_branch, description="test description")
    rack_cleanup.append(name)
    assert page_obj.search_rack(name)


def test_search_rack(logged_in_page, temp_branch, rack_cleanup):
    page_obj = RacksPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    name = generate_random_name("auto_rack")
    code = generate_random_code("RK")
    page_obj.add_rack(name, code, branch_name=temp_branch)
    rack_cleanup.append(name)
    assert page_obj.search_rack(name)


def test_view_rack(logged_in_page, temp_branch, rack_cleanup):
    page_obj = RacksPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    name = generate_random_name("auto_rack")
    code = generate_random_code("RK")
    page_obj.add_rack(name, code, branch_name=temp_branch)
    rack_cleanup.append(name)
    assert page_obj.view_rack(name)


def test_edit_rack(logged_in_page, temp_branch, rack_cleanup):
    page_obj = RacksPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    name = generate_random_name("auto_rack")
    code = generate_random_code("RK")
    page_obj.add_rack(name, code, branch_name=temp_branch)
    rack_cleanup.append(name)
    assert page_obj.search_rack(name)
    new_name = generate_random_name("auto_rack_new")
    rack_cleanup.append(new_name)
    assert page_obj.edit_rack(name, new_name)
    assert page_obj.search_rack(new_name)


def test_delete_rack(logged_in_page, temp_branch, rack_cleanup):
    page_obj = RacksPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    name = generate_random_name("auto_rack")
    code = generate_random_code("RK")
    page_obj.add_rack(name, code, branch_name=temp_branch)
    rack_cleanup.append(name)
    assert page_obj.search_rack(name)
    assert page_obj.delete_rack(name)


def test_retrieve_rack(logged_in_page, temp_branch, rack_cleanup):
    page_obj = RacksPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    name = generate_random_name("auto_rack")
    code = generate_random_code("RK")
    page_obj.add_rack(name, code, branch_name=temp_branch)
    rack_cleanup.append(name)
    assert page_obj.search_rack(name)
    assert page_obj.delete_rack(name)
    assert page_obj.retrieve_rack(name)
    assert page_obj.search_rack(name)


def test_reject_duplicate_rack_in_branch(logged_in_page, temp_branch, rack_cleanup):
    page_obj = RacksPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    name = generate_random_name("duplicate_rack")
    code = generate_random_code("DUP")
    page_obj.add_rack(name, code, branch_name=temp_branch)
    rack_cleanup.append(name)
    assert page_obj.search_rack(name)
    assert page_obj.validate_duplicate_rack(name, code, temp_branch), (
        "Expected visible validation feedback for a duplicate rack"
    )


@pytest.mark.skip(
    reason="System currently allows deleting a branch that contains an active rack (missing restriction/bug)"
)
def test_delete_branch_containing_rack(logged_in_page, temp_branch, rack_cleanup):
    racks_page = RacksPage(logged_in_page)
    racks_page.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    rack_name = generate_random_name("auto_dependency_rack")
    rack_code = generate_random_code("DRK")
    racks_page.add_rack(rack_name, rack_code, branch_name=temp_branch)
    rack_cleanup.append(rack_name)
    assert racks_page.search_rack(rack_name)
    branches_page = BranchesPage(logged_in_page)
    branches_page.navigate()
    assert not branches_page.delete_branch(temp_branch)
