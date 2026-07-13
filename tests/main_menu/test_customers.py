import pytest
from pages.main_menu.customers_page import CustomersPage
from pages.master_menu.cities_page import CitiesPage
from utils.random_data import (
    generate_random_name,
    generate_random_email,
    generate_random_phone,
    generate_random_postal_code,
    generate_random_address,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def city_cleanup(logged_in_page):
    created_cities = []
    yield created_cities
    cities_page = CitiesPage(logged_in_page)
    for city_name in created_cities:
        try:
            cities_page.navigate()
            if cities_page.search_city(city_name):
                cities_page.delete_city(city_name)
        except Exception as e:
            print(f"Teardown: Failed to delete city {city_name}: {e}")


@pytest.fixture
def customer_cleanup(logged_in_page):
    created_customers = []
    yield created_customers
    customers_page = CustomersPage(logged_in_page)
    for name in created_customers:
        try:
            customers_page.navigate()
            if customers_page.search_customer(name):
                customers_page.delete_customer(name)
        except Exception as e:
            print(f"Teardown: Failed to delete customer {name}: {e}")


@pytest.fixture
def customers_page(logged_in_page):
    """A CustomersPage already navigated to the customers list."""
    page = CustomersPage(logged_in_page)
    page.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    return page


@pytest.fixture
def make_city(logged_in_page, city_cleanup):
    """Factory that creates a city and registers it for cleanup.
    Returns the generated city name. Leaves the browser on the cities page."""
    def _make(prefix="AutoCity"):
        cities_page = CitiesPage(logged_in_page)
        cities_page.navigate()
        city_name = generate_random_name(prefix)
        cities_page.add_city(city_name)
        city_cleanup.append(city_name)
        return city_name
    return _make


@pytest.fixture
def make_customer(customers_page, customer_cleanup, city_cleanup):
    """Factory that creates a customer (auto-creating a city unless one is
    passed) and registers both for cleanup. Returns the customer name."""
    def _make(prefix="auto_cust", **kwargs):
        name = kwargs.pop("name", generate_random_name(prefix))
        city_name = customers_page.add_customer(name=name, **kwargs)
        city_cleanup.append(city_name)
        customer_cleanup.append(name)
        return name
    return _make


# ---------------------------------------------------------------------------
# CRUD tests
# ---------------------------------------------------------------------------

def test_customers_visibility(customers_page):
    assert customers_page.is_customers_visible()


def test_add_customer(customers_page, make_customer):
    name = make_customer()
    assert customers_page.search_customer(name)


def test_search_customer(customers_page, make_customer):
    name = make_customer()
    assert customers_page.search_customer(name)


def test_view_customer(customers_page, make_customer):
    name = make_customer()
    assert customers_page.view_customer(name)


def test_edit_customer(customers_page, make_customer, customer_cleanup):
    old_name = make_customer("auto_cust_old")
    new_name = generate_random_name("auto_cust_new")
    customer_cleanup.append(new_name)

    assert customers_page.edit_customer(old_name, new_name)
    assert customers_page.search_customer(new_name)
    assert not customers_page.search_customer(old_name)


def test_delete_customer(customers_page, make_customer):
    name = make_customer()
    assert customers_page.delete_customer(name)


def test_retrieve_customer(customers_page, make_customer):
    name = make_customer()
    assert customers_page.delete_customer(name)
    assert customers_page.retrieve_customer(name)
    assert customers_page.search_customer(name)


# ---------------------------------------------------------------------------
# Validation tests
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    ("field", "value"),
    [
        pytest.param("email", "invalid-email", id="invalid-email"),
        pytest.param("phone", "123", id="short-phone"),
        pytest.param("postal_code", "12345", id="short-postal-code"),
    ],
)
def test_validate_customer_invalid_fields(logged_in_page, make_city, field, value):
    city_name = make_city("AutoCity_val")

    customers_page = CustomersPage(logged_in_page)
    customers_page.navigate()
    logged_in_page.wait_for_load_state("networkidle")

    assert customers_page.validate_invalid_field(
        name=generate_random_name("invalid_cust"),
        customer_type="Person",
        email=generate_random_email("valid"),
        phone=generate_random_phone(),
        notes="val note",
        contact_person="Contact Val",
        address_line1="Line 1",
        address_line2="Line 2",
        state_name="Tamil Nadu",
        city_name=city_name,
        postal_code=generate_random_postal_code(),
        field=field,
        value=value,
    ), f"Expected validation feedback for invalid {field}"


def test_reject_duplicate_customer_email(logged_in_page, make_city, customer_cleanup):
    city_name = make_city("AutoCity_dup")
    duplicate_email = generate_random_email("duplicate")
    postal_code = generate_random_postal_code()

    customers_page = CustomersPage(logged_in_page)
    customers_page.navigate()
    logged_in_page.wait_for_load_state("networkidle")

    first_name = generate_random_name("dup_cust")
    customers_page.add_customer(
        name=first_name,
        customer_type="Person",
        email=duplicate_email,
        phone=generate_random_phone(),
        city_name=city_name,
        postal_code=postal_code,
    )
    customer_cleanup.append(first_name)

    # Attempt to create a second customer reusing the same email.
    assert customers_page.validate_duplicate_customer(
        name=generate_random_name("second_dup_cust"),
        customer_type="Person",
        email=duplicate_email,
        phone=generate_random_phone(),  # unique phone
        notes="note",
        contact_person="contact",
        address_line1="line 1",
        address_line2="line 2",
        state_name="Tamil Nadu",
        city_name=city_name,
        postal_code=postal_code,
    ), "Expected validation feedback for duplicate customer email"
