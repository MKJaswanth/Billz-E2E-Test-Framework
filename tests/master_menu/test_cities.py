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
    
def test_edit_city(logged_in_page, city_cleanup):
    cities_page = CitiesPage(logged_in_page)
    cities_page.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    old_city_name = f"Automate_city{int(time.time())}"
    new_city_name = f"Edited_Automate_city{int(time.time())}"
    
    cities_page.add_city(old_city_name)
    city_cleanup.append(old_city_name)
    city_cleanup.append(new_city_name)
    assert cities_page.edit_city(old_city_name, new_city_name)