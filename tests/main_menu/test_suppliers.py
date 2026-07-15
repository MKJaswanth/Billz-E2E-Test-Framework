import pytest
import random
import string
from pages.main_menu.suppliers_page import SuppliersPage
from pages.master_menu.cities_page import CitiesPage
from utils.random_data import (
    generate_random_name,
    generate_random_email,
    generate_random_phone,
    generate_random_address,
    generate_random_postal_code,
)


def _random_gst():
    pan = (
        "".join(random.choices(string.ascii_uppercase, k=5))
        + "".join(random.choices(string.digits, k=4))
        + random.choice(string.ascii_uppercase)
    )
    return f"33{pan}1Z{random.choice(string.ascii_uppercase + string.digits)}"


def _supplier_data(prefix="auto_sup", city_name="Udumalpet_edit"):
    return {
        "name": generate_random_name(prefix),
        "contact_person": generate_random_name("contact"),
        "email": generate_random_email("supplier"),
        "phone": generate_random_phone(),
        "gst_number": _random_gst(),
        "state_name": "Tamil Nadu",
        "city_name": city_name,
        "postal_code": generate_random_postal_code(),
        "address": generate_random_address(),
        "notes": "automation test notes",
    }


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def module_city(module_page):
    """Create a single city once per module, reused by every supplier test,
    and delete it after the whole module has finished."""
    cities_page = CitiesPage(module_page)
    cities_page.navigate()
    city_name = generate_random_name("auto_city_sup")
    cities_page.add_city(city_name)
    yield city_name
    try:
        cities_page.navigate()
        if cities_page.search_city(city_name):
            cities_page.delete_city(city_name)
    except Exception as e:
        print(f"Teardown: Failed to delete city {city_name}: {e}")


@pytest.fixture
def supplier_cleanup(logged_in_page):
    created_suppliers = []
    yield created_suppliers
    supplier_page = SuppliersPage(logged_in_page)
    for name in created_suppliers:
        try:
            supplier_page.navigate()
            if supplier_page.search_supplier(name):
                supplier_page.delete_supplier(name)
        except Exception as e:
            print(f"Teardown: Failed to delete supplier {name}: {e}")


@pytest.fixture
def suppliers_page(logged_in_page):
    """A SuppliersPage already navigated to the suppliers list."""
    page = SuppliersPage(logged_in_page)
    page.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    return page


@pytest.fixture
def make_supplier(suppliers_page, module_city, supplier_cleanup):
    """Factory that creates a supplier using the shared module city and
    registers it for cleanup. Returns the supplier data dict."""
    def _make(prefix="auto_sup"):
        suppliers_page.navigate()
        suppliers_page.page.wait_for_load_state("networkidle")
        data = _supplier_data(prefix, city_name=module_city)
        suppliers_page.add_supplier(**data)
        supplier_cleanup.append(data["name"])
        return data
    return _make


# ---------------------------------------------------------------------------
# CRUD tests
# ---------------------------------------------------------------------------

def test_suppliers_visibility(suppliers_page):
    assert suppliers_page.is_suppliers_visible()


def test_add_supplier(suppliers_page, make_supplier):
    data = make_supplier()
    assert suppliers_page.search_supplier(data["name"])


def test_search_supplier(suppliers_page, make_supplier):
    data = make_supplier()
    assert suppliers_page.search_supplier(data["name"])


def test_view_supplier(suppliers_page, make_supplier):
    data = make_supplier()
    assert suppliers_page.search_supplier(data["name"])
    assert suppliers_page.view_supplier(data["name"])


def test_edit_supplier(suppliers_page, make_supplier, supplier_cleanup):
    data = make_supplier()
    assert suppliers_page.search_supplier(data["name"])

    new_name = generate_random_name("auto_sup_edit")
    supplier_cleanup.append(new_name)
    assert suppliers_page.edit_supplier(data["name"], new_name)
    assert suppliers_page.search_supplier(new_name)


def test_delete_supplier(suppliers_page, make_supplier, supplier_cleanup):
    data = make_supplier("auto_sup_del")
    assert suppliers_page.search_supplier(data["name"])
    assert suppliers_page.delete_supplier(data["name"])
    supplier_cleanup.remove(data["name"])


def test_retrieve_supplier(suppliers_page, make_supplier):
    data = make_supplier("auto_sup_ret")
    assert suppliers_page.search_supplier(data["name"])
    assert suppliers_page.delete_supplier(data["name"])
    assert suppliers_page.retrieve_supplier(data["name"])


# ---------------------------------------------------------------------------
# Validation tests
# ---------------------------------------------------------------------------

def test_validate_supplier(suppliers_page):
    assert suppliers_page.validate_required_fields()


@pytest.mark.parametrize(
    ("field", "value"),
    [
        pytest.param("email", "invalid-email", id="invalid-email"),
        pytest.param(
            "email",
            "test@gmail",
            id="email-without-domain-suffix",
            marks=pytest.mark.skip(
                reason="Known bug: supplier email without a valid domain suffix is accepted"
            ),
        ),
        pytest.param(
            "phone",
            "1223456789",
            id="phone-invalid-start-digit",
            marks=pytest.mark.skip(
                reason="Known bug: supplier phone numbers starting outside 6-9 are accepted"
            ),
        ),
        pytest.param("phone", "123", id="short-phone"),
        pytest.param("gst_number", "123456789012345", id="invalid-gstin-format"),
        pytest.param("postal_code", "62AB12", id="alphanumeric-postal-code"),
    ],
)
def test_validate_supplier_field_formats(
    suppliers_page, module_city, supplier_cleanup, field, value
):
    data = _supplier_data(f"invalid_{field}", city_name=module_city)
    supplier_cleanup.append(data["name"])
    assert suppliers_page.validate_invalid_field(data, field, value), (
        f"Expected validation feedback for invalid supplier {field}"
    )


@pytest.mark.parametrize("duplicate_field", ["email", "gst_number"])
def test_reject_duplicate_supplier_identifier(
    suppliers_page, make_supplier, module_city, supplier_cleanup, duplicate_field
):
    data = make_supplier("duplicate_supplier")
    duplicate_data = _supplier_data(
        "second_duplicate_supplier", city_name=module_city
    )
    duplicate_data[duplicate_field] = data[duplicate_field]
    supplier_cleanup.append(duplicate_data["name"])
    assert suppliers_page.validate_duplicate_supplier(duplicate_data), (
        f"Expected duplicate validation for an existing supplier {duplicate_field}"
    )
