import os
import pytest
from pages.auth.login_page import LoginPage
from utils.constants import ADMIN_EMAIL, ADMIN_PASSWORD

STORAGE_STATE_PATH = os.path.join(os.path.dirname(__file__), "auth_state.json")

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "ignore_https_errors": True,
        "viewport": {"width": 1280, "height": 720}
    }

@pytest.fixture(scope="session")
def auth_state(browser):

    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
    page.wait_for_url(lambda url: "/login" not in url, timeout=10000)
    page.wait_for_load_state("networkidle")


    context.storage_state(path=STORAGE_STATE_PATH)
    context.close()

    yield STORAGE_STATE_PATH

@pytest.fixture
def logged_in_page(browser, auth_state):
    context = browser.new_context(storage_state=auth_state, ignore_https_errors=True)
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture(scope="module")
def module_page(browser, auth_state):
    context = browser.new_context(storage_state=auth_state, ignore_https_errors=True)
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture(scope="session")
def funded_bank_account(browser, auth_state):
    """A bank account pre-loaded with a large balance, so Purchases/Vouchers
    tests that pay out of it don't hit "insufficient amount". Funding works
    by collecting a large Sale's payment directly into the bank account
    (Sale type -> pick the bank account by name -> paid_amount is credited
    to it), since that's the only funding path the app exposes.

    Session-scoped (not module-scoped) on purpose: Sales has no delete/void
    flow yet, and real accounting systems generally don't allow deleting a
    financial transaction outright (only reversing it, e.g. Sale Return,
    which doesn't undo the bank credit). So the customer/branch/product/
    bank account this creates will likely become permanently undeletable
    once the funding Sale references them - creating this once per test run
    instead of once per module keeps that leftover data to a minimum.
    """
    from pages.master_menu.bank_accounts_page import BankAccountPage
    from pages.master_menu.categories_page import CategoriesPage
    from pages.master_menu.brands_page import BrandPage
    from pages.master_menu.unit_types_page import UnitTypesPage
    from pages.master_menu.sac_hsn_page import SacHsnPage
    from pages.master_menu.branches_page import BranchesPage
    from pages.main_menu.products_page import ProductsPage
    from pages.main_menu.customers_page import CustomersPage
    from pages.main_menu.sales_page import SalesPage
    from utils.random_data import generate_random_name, generate_random_code
    import random

    context = browser.new_context(storage_state=auth_state, ignore_https_errors=True)
    page = context.new_page()

    # 1. Minimal product dependencies (throwaway, just enough for one line item)
    categories_page = CategoriesPage(page)
    categories_page.navigate()
    cat_name = generate_random_name("fund_cat")
    categories_page.add_category(name=cat_name, description="bank funding setup")
    categories_page.page.get_by_text("Category created successfully").wait_for(state="visible", timeout=5000)

    brand_page = BrandPage(page)
    brand_page.navigate()
    brand_name = generate_random_name("fund_brand")
    brand_page.add_brand(brand_name, "bank funding setup")

    unit_page = UnitTypesPage(page)
    unit_page.navigate()
    unit_name = generate_random_name("fund_unit")
    unit_page.add_unit_type(name=unit_name, unit="pcs", description="bank funding setup")

    sac_page = SacHsnPage(page)
    sac_page.navigate()
    sac_code = str(random.randint(100000, 999999))
    sac_page.add_sac_hsn_code("SAC", sac_code, description="bank funding setup")

    products_page = ProductsPage(page)
    products_page.navigate()
    product_name = generate_random_name("fund_prod")
    products_page.add_product(
        name=product_name,
        brand_name=brand_name,
        category_name=cat_name,
        hsn_code=sac_code,
        unit_type=unit_name,
        cost_price="1",
        selling_price="100000",
        gst_percentage="18%",
    )

    # 2. Branch + customer to sell against
    branches_page = BranchesPage(page)
    branches_page.navigate()
    branch_name = branches_page.add_branch()
    branches_page.page.get_by_text("Branch created successfully.").wait_for(state="visible", timeout=5000)

    customers_page = CustomersPage(page)
    customer_name = generate_random_name("fund_cust")
    customers_page.add_customer(name=customer_name)

    # 3. Bank account to fund
    bank_page = BankAccountPage(page)
    bank_page.navigate()
    bank_name = generate_random_name("fund_bank")
    bank_page.add_bank_account(
        bank_name=bank_name,
        branch="Main Branch",
        account_number=str(random.randint(100000000000, 999999999999)),
        ifsc_code="IDFC0000899",
    )

    # 4. Fund it: a large cash sale, collected directly into this bank account
    sales_page = SalesPage(page)
    sales_page.add_sale(
        customer_name=customer_name,
        branch_name=branch_name,
        product_name=product_name,
        price="100000",
        paid_amount="100000",
        payment_method=bank_name,
    )

    yield bank_name

    # No cleanup attempted here on purpose - see docstring. The funding Sale
    # almost certainly keeps these records referenced/undeletable, so a
    # teardown block would just fail silently every run without benefit.
    print(
        f"funded_bank_account: leaving {bank_name} (and its supporting "
        f"customer/branch/product) in place - a Sale references them and "
        f"there is no delete/void flow to reverse that yet."
    )
    context.close()
