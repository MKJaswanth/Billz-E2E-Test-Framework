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

@pytest.fixture(scope="module")
def module_city(module_page):
    """Create a single city once per module, reused by every customer test,
    and delete it after the whole module has finished."""
    cities_page = CitiesPage(module_page)
    cities_page.navigate()
    city_name = generate_random_name("auto_city_cust")
    cities_page.add_city(city_name)
    yield city_name
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
def make_customer(customers_page, module_city, customer_cleanup):
    """Factory that creates a customer against the shared module city and
    registers it for cleanup. Returns the customer name."""
    def _make(prefix="auto_cust", **kwargs):
        customers_page.navigate()
        customers_page.page.wait_for_load_state("networkidle")
        name = kwargs.pop("name", generate_random_name(prefix))
        kwargs.setdefault("city_name", module_city)
        customers_page.add_customer(name=name, **kwargs)
        customer_cleanup.append(name)
        return name
    return _make



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


def test_delete_customer(customers_page, make_customer, customer_cleanup):
    name = make_customer()
    assert customers_page.delete_customer(name)
    customer_cleanup.remove(name)


def test_retrieve_customer(customers_page, make_customer):
    name = make_customer()
    assert customers_page.delete_customer(name)
    assert customers_page.retrieve_customer(name)
    assert customers_page.search_customer(name)



def test_validate_customer_required_fields(customers_page):
    assert customers_page.validate_required_fields()

@pytest.mark.parametrize(
    ("field", "value"),
    [
        pytest.param("email", "invalid-email", id="invalid-email"),
        pytest.param("email", "test@gmail", id="email-without-domain-suffix"),
        pytest.param("phone", "123", id="short-phone"),
        pytest.param("phone", "1223456789", id="phone-invalid-start-digit"),
        pytest.param("postal_code", "12345", id="short-postal-code"),
        pytest.param("postal_code", "62AB12", id="alphanumeric-postal-code"),
    ],
)
def test_validate_customer_invalid_fields(customers_page, module_city, field, value):
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
        city_name=module_city,
        postal_code=generate_random_postal_code(),
        field=field,
        value=value,
    ), f"Expected validation feedback for invalid {field}"


@pytest.mark.parametrize("duplicate_field", ["email", "phone"])
def test_reject_duplicate_customer_identifier(
    customers_page, module_city, customer_cleanup, duplicate_field
):
    duplicate_email = generate_random_email("duplicate")
    duplicate_phone = generate_random_phone()
    postal_code = generate_random_postal_code()

    first_name = generate_random_name("dup_cust")
    customers_page.add_customer(
        name=first_name,
        customer_type="Person",
        email=duplicate_email,
        phone=duplicate_phone,
        city_name=module_city,
        postal_code=postal_code,
    )
    customer_cleanup.append(first_name)

    second_email = generate_random_email("second_duplicate")
    second_phone = generate_random_phone()
    if duplicate_field == "email":
        second_email = duplicate_email
    else:
        second_phone = duplicate_phone

    assert customers_page.validate_duplicate_customer(
        name=generate_random_name("second_dup_cust"),
        customer_type="Person",
        email=second_email,
        phone=second_phone,
        notes="note",
        contact_person="contact",
        address_line1="line 1",
        address_line2="line 2",
        state_name="Tamil Nadu",
        city_name=module_city,
        postal_code=postal_code,
    ), f"Expected validation feedback for duplicate customer {duplicate_field}"

def test_delete_customer_with_sale_is_allowed(
    customers_page, make_customer, logged_in_page, module_branch, module_product
):
    from pages.main_menu.sales_page import SalesPage
    from pages.main_menu.products_page import ProductsPage
    import re
    
    # 1. Create a customer
    customer_name = make_customer("allow_del_cust")
    
    # 2. Add opening stock to product in the branch
    products_page = ProductsPage(logged_in_page)
    products_page.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    products_page.update_opening_stock(
        name=module_product,
        branch_name=module_branch,
        quantity="10",
        cost_price="200"
    )
    
    # 3. Create a Sale for this customer
    sales_page = SalesPage(logged_in_page)
    sales_page.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    sales_page.add_sale(
        customer_name=customer_name,
        branch_name=module_branch,
        paid_amount="0",
        price="300",
        product_name=module_product,
        quantity=1,
        salesperson_name="Super Admin"
    )
    
    # 4. Verify Customer deletion is allowed (soft-deleted)
    customers_page.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    assert customers_page.delete_customer(customer_name)
    
    # 5. Verify we can retrieve them back (confirming they were indeed in the soft-deleted state)
    assert customers_page.retrieve_customer(customer_name)



