import pytest
import random
from pages.main_menu.products_page import ProductsPage
from pages.master_menu.categories_page import CategoriesPage
from pages.master_menu.brands_page import BrandPage
from pages.master_menu.unit_types_page import UnitTypesPage
from pages.master_menu.sac_hsn_page import SacHsnPage
from pages.master_menu.branches_page import BranchesPage
from utils.random_data import generate_random_name


# ---------------------------------------------------------------------------
# Dependency fixtures (categories, brands, unit types, HSN codes, branches)
# ---------------------------------------------------------------------------

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
            branches_page.delete_branch(branch_name)
    except Exception as e:
        print(f"Teardown: Failed to delete branch {branch_name}: {e}")
    branches_page.cleanup_auto_city(branch_name)


@pytest.fixture(scope="module")
def module_category(module_page):
    categories_page = CategoriesPage(module_page)
    categories_page.navigate()
    cat_name = generate_random_name("auto_cat")
    categories_page.add_category(name=cat_name, description="cat desc")
    yield cat_name
    try:
        categories_page.navigate()
        if categories_page.search_category(cat_name):
            categories_page.delete_category(cat_name)
    except Exception as e:
        print(f"Teardown: Failed to delete category {cat_name}: {e}")


@pytest.fixture(scope="module")
def module_brand(module_page):
    brand_page = BrandPage(module_page)
    brand_page.navigate()
    brand_name = generate_random_name("auto_brand")
    brand_page.add_brand(brand_name, "brand desc")
    yield brand_name
    try:
        brand_page.navigate()
        if brand_page.search_brand(brand_name):
            brand_page.delete_brand(brand_name)
    except Exception as e:
        print(f"Teardown: Failed to delete brand {brand_name}: {e}")


@pytest.fixture(scope="module")
def module_unit_type(module_page):
    unit_page = UnitTypesPage(module_page)
    unit_page.navigate()
    unit_name = generate_random_name("auto_unit")
    unit_page.add_unit_type(name=unit_name, unit="pcs", description="unit desc")
    yield unit_name
    try:
        unit_page.navigate()
        if unit_page.search_unit_type(unit_name):
            unit_page.delete_unit_type(unit_name)
    except Exception as e:
        print(f"Teardown: Failed to delete unit type {unit_name}: {e}")


@pytest.fixture(scope="module")
def module_hsn_code(module_page):
    sac_page = SacHsnPage(module_page)
    sac_page.navigate()
    sac_code = str(random.randint(100000, 999999))
    sac_page.add_sac_hsn_code("SAC", sac_code, description="sac desc")
    yield sac_code
    try:
        sac_page.navigate()
        if sac_page.search_sac_hsn_code(sac_code):
            sac_page.delete_sac_hsn_code(sac_code)
    except Exception as e:
        print(f"Teardown: Failed to delete SAC/HSN code {sac_code}: {e}")


@pytest.fixture(scope="module")
def product_dependencies(module_category, module_brand, module_unit_type, module_hsn_code):
    """Bundle the master-data a product needs into a single dict."""
    return {
        "category": module_category,
        "brand": module_brand,
        "unit_type": module_unit_type,
        "hsn_code": module_hsn_code,
    }


# ---------------------------------------------------------------------------
# Page & factory fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def products_page(logged_in_page):
    """A ProductsPage already navigated to the products list."""
    page = ProductsPage(logged_in_page)
    page.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    return page


@pytest.fixture
def product_cleanup(logged_in_page):
    created_products = []
    yield created_products
    page_obj = ProductsPage(logged_in_page)
    for name in created_products:
        try:
            page_obj.navigate()
            if page_obj.search_product(name):
                page_obj.delete_product(name)
        except Exception as e:
            print(f"Teardown: Failed to delete product {name}: {e}")


@pytest.fixture
def make_product(products_page, product_dependencies, product_cleanup):
    """Factory that creates a product with the shared dependencies and
    registers it for cleanup. Returns the generated product name."""
    def _make(prefix="auto_prod"):
        products_page.navigate()
        products_page.page.wait_for_load_state("networkidle")
        name = generate_random_name(prefix)
        products_page.add_product(
            name=name,
            brand_name=product_dependencies["brand"],
            category_name=product_dependencies["category"],
            hsn_code=product_dependencies["hsn_code"],
            unit_type=product_dependencies["unit_type"],
        )
        product_cleanup.append(name)
        return name
    return _make


# ---------------------------------------------------------------------------
# CRUD tests
# ---------------------------------------------------------------------------

def test_products_visibility(products_page):
    assert products_page.is_products_visible()


def test_add_product(products_page, make_product):
    name = make_product()
    assert products_page.search_product(name)


def test_search_product(products_page, make_product):
    name = make_product()
    assert products_page.search_product(name)


def test_view_product(products_page, make_product):
    name = make_product()
    assert products_page.view_product(name)


def test_edit_product(products_page, make_product, product_cleanup):
    name = make_product()
    new_name = generate_random_name("auto_prod_new")
    product_cleanup.append(new_name)

    assert products_page.edit_product(name, new_name)
    assert products_page.search_product(new_name)


def test_opening_stock_update(products_page, make_product, temp_branch):
    name = make_product()
    assert products_page.update_opening_stock(name, temp_branch, "10", "2500")


def test_delete_product(products_page, make_product, product_cleanup):
    name = make_product()
    assert products_page.search_product(name)
    assert products_page.delete_product(name)
    product_cleanup.remove(name)


def test_retrieve_product(products_page, make_product):
    name = make_product()
    assert products_page.search_product(name)
    assert products_page.delete_product(name)
    assert products_page.retrieve_product(name)
    assert products_page.search_product(name)


# ---------------------------------------------------------------------------
# Validation tests
# ---------------------------------------------------------------------------

def test_validate_product_required_fields(products_page):
    assert products_page.validate_required_fields()


@pytest.mark.parametrize(
    ("field", "value"),
    [
        pytest.param("cost_price", "-1", id="negative-cost-price"),
        pytest.param("selling_price", "-1", id="negative-selling-price"),
        pytest.param("low_stock", "-1", id="negative-low-stock"),
    ],
)
def test_reject_negative_product_values(
    products_page, product_dependencies, product_cleanup, field, value
):
    product_name = generate_random_name(f"invalid_{field}")
    product_cleanup.append(product_name)
    assert products_page.validate_invalid_numeric_field(
        name=product_name,
        brand_name=product_dependencies["brand"],
        category_name=product_dependencies["category"],
        hsn_code=product_dependencies["hsn_code"],
        unit_type=product_dependencies["unit_type"],
        field=field,
        value=value,
    ), f"Expected validation feedback for negative {field}"


def test_reject_duplicate_product_name(products_page, make_product, product_dependencies):
    product_name = make_product("duplicate_product")
    assert products_page.validate_duplicate_product(
        name=product_name,
        brand_name=product_dependencies["brand"],
        category_name=product_dependencies["category"],
        hsn_code=product_dependencies["hsn_code"],
        unit_type=product_dependencies["unit_type"],
    ), "Expected validation feedback for a duplicate product name"


# ---------------------------------------------------------------------------
# Dependency-deletion protection tests
# ---------------------------------------------------------------------------

def test_delete_brand_assigned_to_product_is_blocked(
    logged_in_page, product_dependencies, make_product
):
    make_product("brand_dependency")
    brand_page = BrandPage(logged_in_page)
    brand_page.navigate()
    assert not brand_page.delete_brand(product_dependencies["brand"]), (
        "An assigned brand must not be deleted"
    )


@pytest.mark.skip(
    reason="Known bug: brand remains undeletable after its assigned product is deleted"
)
def test_delete_brand_after_assigned_product_is_deleted(
    logged_in_page, product_dependencies, product_cleanup
):
    brand_page = BrandPage(logged_in_page)
    brand_page.navigate()
    brand_name = generate_random_name("deleted_product_brand")
    brand_page.add_brand(brand_name, "brand dependency validation")

    product_page = ProductsPage(logged_in_page)
    product_page.navigate()
    product_name = generate_random_name("deleted_brand_dependency_product")
    product_page.add_product(
        name=product_name,
        brand_name=brand_name,
        category_name=product_dependencies["category"],
        hsn_code=product_dependencies["hsn_code"],
        unit_type=product_dependencies["unit_type"],
    )
    product_cleanup.append(product_name)
    assert product_page.delete_product(product_name)

    brand_page.navigate()
    assert brand_page.delete_brand(brand_name), (
        "A brand should be deletable after its assigned product is deleted"
    )


@pytest.mark.skip(reason="Known bug: category assigned to an active product can be deleted")
def test_delete_category_assigned_to_product_is_blocked(
    logged_in_page, product_dependencies, make_product
):
    make_product("category_dependency")
    category_page = CategoriesPage(logged_in_page)
    category_page.navigate()
    assert not category_page.delete_category(product_dependencies["category"]), (
        "An assigned category must not be deleted"
    )


@pytest.mark.skip(reason="Known bug: unit type assigned to an active product can be deleted")
def test_delete_unit_type_assigned_to_product_is_blocked(
    logged_in_page, product_dependencies, make_product
):
    make_product("unit_dependency")
    unit_page = UnitTypesPage(logged_in_page)
    unit_page.navigate()
    assert not unit_page.delete_unit_type(product_dependencies["unit_type"]), (
        "An assigned unit type must not be deleted"
    )


@pytest.mark.skip(reason="Known bug: HSN/SAC code assigned to an active product can be deleted")
def test_delete_hsn_sac_assigned_to_product_is_blocked(
    logged_in_page, product_dependencies, make_product
):
    make_product("hsn_dependency")
    hsn_page = SacHsnPage(logged_in_page)
    hsn_page.navigate()
    assert not hsn_page.delete_sac_hsn_code(product_dependencies["hsn_code"]), (
        "An assigned HSN/SAC code must not be deleted"
    )
