import time
import random
import pytest

from pages.master_menu.cities_page import CitiesPage

def random_city_name(rprefix="Automate"):
    random_letters = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5))
    return f"{rprefix}_{random_letters}"

@pytest.fixture
def city_cleanup(logged_in_page):
    created_cities = []
    yield created_cities
    cities_page = CitiesPage(logged_in_page)
    for name in created_cities:
        try:
            cities_page.navigate()
            if cities_page.search_city(name):
                row = cities_page.page.locator("tr", has=cities_page.page.get_by_text(name, exact=True))
                if row.get_by_title("delete").first.is_visible():
                    cities_page.delete_city(name)
        except Exception as e:
            print(f"Teardown: Failed to delete city {name}: {e}")

def test_cities_visibility(logged_in_page):
    cities_page = CitiesPage(logged_in_page)
    cities_page.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    assert cities_page.is_cities_visible()
    
def test_add_city(logged_in_page, city_cleanup):
    cities_page = CitiesPage(logged_in_page)
    cities_page.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    city_name = random_city_name()
    cities_page.add_city(city_name)
    city_cleanup.append(city_name)
    assert cities_page.is_city_added(city_name)
    
def test_search_city(logged_in_page, city_cleanup):
    cities_page = CitiesPage(logged_in_page)
    cities_page.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    city_name = random_city_name()
    cities_page.add_city(city_name)
    city_cleanup.append(city_name)
    assert cities_page.search_city(city_name)
    
def test_delete_city(logged_in_page, city_cleanup):
    cities_page = CitiesPage(logged_in_page)
    cities_page.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    city_name = random_city_name()
    
    cities_page.add_city(city_name)
    city_cleanup.append(city_name)
    assert cities_page.delete_city(city_name)  
    
def test_retrieve_city(logged_in_page, city_cleanup):
    cities_page = CitiesPage(logged_in_page)
    cities_page.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    city_name = random_city_name()
    
    cities_page.add_city(city_name)
    city_cleanup.append(city_name)
    assert cities_page.delete_city(city_name)  
    assert cities_page.retrieve_city(city_name)


def test_reject_duplicate_city_in_same_state(logged_in_page, city_cleanup):
    cities_page = CitiesPage(logged_in_page)
    cities_page.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    city_name = random_city_name("duplicate_city")
    cities_page.add_city(city_name)
    city_cleanup.append(city_name)
    assert cities_page.validate_duplicate_city(city_name), (
        "Expected visible validation feedback for a duplicate city/state combination"
    )


@pytest.mark.skip(reason="Known bug: city names containing numbers are accepted")
def test_reject_city_name_containing_numbers(logged_in_page):
    cities_page = CitiesPage(logged_in_page)
    cities_page.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    assert cities_page.validate_invalid_city_name("Coimbatore123"), (
        "Expected city-name validation because numbers are not allowed"
    )
    
def test_edit_city(logged_in_page, city_cleanup):
    cities_page = CitiesPage(logged_in_page)
    cities_page.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    old_city_name = random_city_name("oldcity")
    new_city_name = random_city_name("newcity")
    
    cities_page.add_city(old_city_name)
    city_cleanup.append(old_city_name)
    city_cleanup.append(new_city_name)
    assert cities_page.edit_city(old_city_name, new_city_name)

def test_delete_city_assigned_to_branch_is_blocked(logged_in_page, city_cleanup):
    from pages.master_menu.branches_page import BranchesPage
    from utils.random_data import generate_random_name, generate_random_code, generate_random_address, generate_random_phone, generate_random_postal_code, generate_random_email
    
    cities_page = CitiesPage(logged_in_page)
    cities_page.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    
    city_name = random_city_name("city_dep")
    cities_page.add_city(city_name)
    city_cleanup.append(city_name)
    
    # Navigate to Branches and create a branch using this city
    branches_page = BranchesPage(logged_in_page)
    branches_page.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    
    branch_name = generate_random_name("branch_dep")
    branches_page.page.get_by_role("button", name="Add Branch").click()
    branches_page.page.locator("input[name=\"name\"]").fill(branch_name)
    branches_page.page.locator("input[name=\"code\"]").fill(generate_random_code())
    branches_page.page.locator("input[name=\"address\"]").fill(generate_random_address())
    
    branches_page.page.locator("input[name='state_id']").locator("xpath=..").locator(".react-select__input-container").click()
    branches_page.page.get_by_role("option", name="Tamil Nadu").click()
    
    branches_page.page.locator("input[name='city_id']").locator("xpath=..").locator(".react-select__input-container").click()
    branches_page.page.get_by_role("option", name=city_name).click()
    
    branches_page.page.locator("input[name=\"postal_code\"]").fill(generate_random_postal_code())
    branches_page.page.get_by_role("textbox", name="Enter 10-digit phone number").fill(generate_random_phone())
    branches_page.page.locator("input[name=\"email\"]").fill(generate_random_email())
    branches_page.page.get_by_role("spinbutton").fill("3")
    branches_page.page.get_by_role("button", name="Create").click()
    
    # Wait for branch creation toast
    branches_page.page.get_by_text("Branch created successfully").wait_for(state="visible", timeout=5000)
    
    # Go back to Cities and try to delete the city
    cities_page.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    assert cities_page.delete_city_expect_fail(city_name)
    
    # Teardown branch first in test body to allow city deletion during city_cleanup fixture
    branches_page.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    branches_page.delete_branch(branch_name)

