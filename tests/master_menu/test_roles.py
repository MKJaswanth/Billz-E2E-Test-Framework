import pytest
from pages.master_menu.roles_page import RolesPage
from utils.random_data import generate_random_name

@pytest.fixture
def role_cleanup(logged_in_page):
    created_roles = []
    yield created_roles
    roles_page = RolesPage(logged_in_page)
    for name in created_roles:
        try:
            roles_page.navigate()
            if roles_page.search_roles(name):
                row = roles_page.page.locator("tr", has=roles_page.page.get_by_text(name, exact=True))
                if row.get_by_title("delete").first.is_visible():
                    roles_page.delete_role(name)
        except Exception as e:
            print(f"Teardown: Failed to delete role {name}: {e}")

def test_roles_visible(logged_in_page):
    roles_page = RolesPage(logged_in_page)
    roles_page.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    assert roles_page.is_roles_visible()

def test_add_roles(logged_in_page, role_cleanup):
    roles_page = RolesPage(logged_in_page)
    roles_page.navigate()
    
    role_name = roles_page.add_roles()
    role_cleanup.append(role_name)
    assert logged_in_page.get_by_text(role_name, exact=True).is_visible()
    assert logged_in_page.get_by_text("Role created successfully").is_visible()
    
def test_search_roles(logged_in_page, role_cleanup):
    roles_page = RolesPage(logged_in_page)
    roles_page.navigate()
    
    role_name = roles_page.add_roles()
    role_cleanup.append(role_name)
    assert roles_page.search_roles(role_name)
    
def test_view_roles(logged_in_page, role_cleanup):
    roles_page = RolesPage(logged_in_page)
    roles_page.navigate()
    
    role_name = roles_page.add_roles()
    role_cleanup.append(role_name)
    assert roles_page.search_roles(role_name)
    assert roles_page.view_roles(role_name)
    
def test_edit_roles(logged_in_page, role_cleanup):
    roles_page = RolesPage(logged_in_page)
    roles_page.navigate()
    
    role_name = roles_page.add_roles()
    role_cleanup.append(role_name)
    new_role_name = generate_random_name("editiedrole")
    role_cleanup.append(new_role_name)
    assert roles_page.edit_role(role_name, new_role_name)
    
def test_delete_roles(logged_in_page, role_cleanup):
    roles_page = RolesPage(logged_in_page)
    roles_page.navigate()
    
    role_name = roles_page.add_roles()
    role_cleanup.append(role_name)
    assert roles_page.delete_role(role_name)
    
def test_retrieve_roles(logged_in_page, role_cleanup):
    roles_page = RolesPage(logged_in_page)
    roles_page.navigate()
    
    role_name = roles_page.add_roles()
    role_cleanup.append(role_name)
    assert roles_page.retrieve_role(role_name)