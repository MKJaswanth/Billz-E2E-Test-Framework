import pytest
from pages.master_menu.unit_types_page import UnitTypesPage
from utils.random_data import generate_random_name, generate_random_unit, generate_random_description

@pytest.fixture
def unit_type_cleanup(logged_in_page):
    created_units = []
    yield created_units
    unit_page = UnitTypesPage(logged_in_page)
    for name in created_units:
        try:
            unit_page.navigate()
            if unit_page.search_unit_type(name):
                row = unit_page.page.locator("tr", has=unit_page.page.get_by_text(name, exact=True))
                if row.get_by_title("delete").first.is_visible():
                    unit_page.delete_unit_type(name)
        except Exception as e:
            print(f"Teardown: Failed to delete unit type {name}: {e}")

def test_unit_types_visibility(logged_in_page):
    unit_types_page = UnitTypesPage(logged_in_page)
    unit_types_page.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    assert unit_types_page.is_unit_types_visible()

def test_add_unit_type(logged_in_page, unit_type_cleanup):
    unit_types_page = UnitTypesPage(logged_in_page)
    unit_types_page.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    unit_name = generate_random_name("auto_unit")
    unit = generate_random_unit()
    description = generate_random_description("unit_description")
    
    assert unit_types_page.add_unit_type(name=unit_name, unit=unit, description=description)
    unit_type_cleanup.append(unit_name)

def test_search_unit_type(logged_in_page, unit_type_cleanup):
    unit_types_page = UnitTypesPage(logged_in_page)
    unit_types_page.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    unit_name = generate_random_name("auto_unit")
    unit = generate_random_unit()
    description = generate_random_description("unit_description")
    
    unit_types_page.add_unit_type(name=unit_name, unit=unit, description=description)
    unit_type_cleanup.append(unit_name)
    assert unit_types_page.search_unit_type(unit_name)

def test_view_unit_type(logged_in_page, unit_type_cleanup):
    unit_types_page = UnitTypesPage(logged_in_page)
    unit_types_page.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    unit_name = generate_random_name("auto_unit")
    unit = generate_random_unit()
    description = generate_random_description("unit_description")
    
    unit_types_page.add_unit_type(name=unit_name, unit=unit, description=description)
    unit_type_cleanup.append(unit_name)
    unit_types_page.search_unit_type(unit_name)
    assert unit_types_page.view_unit_type(unit_name)

def test_edit_unit_type(logged_in_page, unit_type_cleanup):
    unit_types_page = UnitTypesPage(logged_in_page)
    unit_types_page.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    unit_name = generate_random_name("auto_unit")
    new_name = generate_random_name("new_unit")
    unit = generate_random_unit()
    new_unit = generate_random_unit()
    description = generate_random_description("unit_description")
    new_description = generate_random_description("new_unit_description")
    
    unit_types_page.add_unit_type(name=unit_name, unit=unit, description=description)
    unit_type_cleanup.append(unit_name)
    unit_type_cleanup.append(new_name)
    unit_types_page.search_unit_type(unit_name)
    
    assert unit_types_page.edit_unit_type(unit_name, new_name, new_unit, new_description)
    assert unit_types_page.search_unit_type(new_name)
    assert not unit_types_page.search_unit_type(unit_name)

def test_delete_unit_type(logged_in_page, unit_type_cleanup):
    unit_types_page = UnitTypesPage(logged_in_page)
    unit_types_page.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    unit_name = generate_random_name("auto_unit")
    unit = generate_random_unit()
    description = generate_random_description("unit_description")
    
    unit_types_page.add_unit_type(name=unit_name, unit=unit, description=description)
    unit_type_cleanup.append(unit_name)
    unit_types_page.search_unit_type(unit_name)
    assert unit_types_page.delete_unit_type(unit_name)

def test_retrieve_unit_type(logged_in_page, unit_type_cleanup):
    unit_types_page = UnitTypesPage(logged_in_page)
    unit_types_page.navigate()
    logged_in_page.wait_for_load_state("networkidle")   
    unit_name = generate_random_name("auto_unit")
    unit = generate_random_unit()
    description = generate_random_description("unit_description")
    
    unit_types_page.add_unit_type(name=unit_name, unit=unit, description=description)
    unit_type_cleanup.append(unit_name)
    unit_types_page.search_unit_type(unit_name)
    assert unit_types_page.delete_unit_type(unit_name)
    assert unit_types_page.retrieve_unit_type(unit_name)
    assert unit_types_page.search_unit_type(unit_name)

def test_validate_unit_type(logged_in_page):
    unit_types_page = UnitTypesPage(logged_in_page)
    unit_types_page.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    assert unit_types_page.validate_required_fields()


def test_reject_duplicate_unit_type(logged_in_page, unit_type_cleanup):
    unit_types_page = UnitTypesPage(logged_in_page)
    unit_types_page.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    name = generate_random_name("duplicate_unit")
    unit = generate_random_unit()
    description = generate_random_description("duplicate_unit_description")
    assert unit_types_page.add_unit_type(name, unit, description)
    unit_type_cleanup.append(name)
    assert unit_types_page.validate_duplicate_unit(name, unit, description), (
        "Expected visible validation feedback for a duplicate unit name or symbol"
    )
