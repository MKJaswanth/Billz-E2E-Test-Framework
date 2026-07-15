import os
import pytest
from pages.auth.login_page import LoginPage
from utils.constants import ADMIN_EMAIL, ADMIN_PASSWORD

STORAGE_STATE_PATH = os.path.join(os.path.dirname(__file__), "auth_state.json")

def pytest_addoption(parser):
    parser.addoption(
        "--playback",
        action="store_true",
        default=False,
        help="Enable the interactive draggable playback control panel"
    )


@pytest.fixture(autouse=True, scope="session")
def _playback_control(request):
    ui_enabled = request.config.getoption("--playback", default=False)
    request.config._playback_enabled = ui_enabled
    if ui_enabled:
        from utils.playback import playback
        playback.start()
        yield
        playback.stop()
    else:
        yield

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
    """A bank account funded with ₹500 via a small Sale.

    Creates minimal dependencies: 1 product (using existing deps), 1 bank
    account, 1 sale. Uses ₹500 (not ₹100k) to minimise report noise.
    """
    from pages.master_menu.bank_accounts_page import BankAccountPage
    from pages.master_menu.categories_page import CategoriesPage
    from pages.master_menu.brands_page import BrandPage
    from pages.master_menu.unit_types_page import UnitTypesPage
    from pages.master_menu.sac_hsn_page import SacHsnPage
    from pages.main_menu.products_page import ProductsPage
    from pages.main_menu.customers_page import CustomersPage
    from pages.main_menu.sales_page import SalesPage
    from utils.random_data import generate_random_name
    import random

    context = browser.new_context(storage_state=auth_state, ignore_https_errors=True)
    page = context.new_page()

    # 1. Product dependencies
    categories_page = CategoriesPage(page)
    categories_page.navigate()
    cat_name = generate_random_name("fund_cat")
    categories_page.add_category(name=cat_name, description="bank funding")
    categories_page.page.get_by_text("Category created successfully").wait_for(state="visible", timeout=5000)

    brand_page = BrandPage(page)
    brand_page.navigate()
    brand_name = generate_random_name("fund_brand")
    brand_page.add_brand(brand_name, "bank funding")

    unit_page = UnitTypesPage(page)
    unit_page.navigate()
    unit_name = generate_random_name("fund_unit")
    unit_page.add_unit_type(name=unit_name, unit="pcs", description="bank funding")

    sac_page = SacHsnPage(page)
    sac_page.navigate()
    sac_code = str(random.randint(100000, 999999))
    sac_page.add_sac_hsn_code("SAC", sac_code, description="bank funding")

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
        selling_price="500",
        gst_percentage="18%",
    )

    # 2. Customer
    customers_page = CustomersPage(page)
    customer_name = generate_random_name("fund_cust")
    customers_page.add_customer(name=customer_name)

    # 3. Bank account
    bank_page = BankAccountPage(page)
    bank_page.navigate()
    bank_name = generate_random_name("fund_bank")
    bank_page.add_bank_account(
        bank_name=bank_name,
        branch="Main Branch",
        account_number=str(random.randint(100000000000, 999999999999)),
        ifsc_code="IDFC0000899",
    )

    # 4. Add opening stock
    products_page.navigate()
    products_page.update_opening_stock(
        name=product_name,
        branch_name="Main Branch",
        quantity="1",
        cost_price="1",
    )

    # 5. Sell the product — payment goes into our bank account
    sales_page = SalesPage(page)
    sales_page.add_sale(
        customer_name=customer_name,
        branch_name="Main Branch",
        product_name=product_name,
        price="500",
        paid_amount="500",
        payment_method=bank_name,
    )

    yield bank_name

    # Sale references keep these undeletable — just close context
    context.close()


@pytest.fixture(autouse=True)
def auto_test_banner(request):
    """Automatically adds a test name banner to the browser in headed mode,
    or integrates with the playback overlay if active.
    Only runs when --headed or --playback is set.
    """
    is_headed = False
    try:
        is_headed = request.config.getoption("--headed")
    except Exception:
        pass
    
    playback_enabled = getattr(request.config, "_playback_enabled", False)
    if not is_headed and not playback_enabled:
        return

    # Only run for tests that request a page fixture
    page_fixtures = ["page", "logged_in_page", "module_page"]
    page = None
    for name in page_fixtures:
        if name in request.fixturenames:
            try:
                page = request.getfixturevalue(name)
                break
            except Exception:
                pass

    if not page:
        return

    # Get test name and format it nicely
    test_name = request.node.name
    display_name = test_name.replace("test_", "").replace("_", " ").title()

    # If playback is enabled, update playback and trigger an update immediately
    if playback_enabled:
        try:
            from utils.playback import playback
            playback.test_name = f"Running: {display_name}"
            playback._update(page)
        except Exception:
            pass
        return

    # Headed mode: inject the yellow banner
    script = f"""
    (() => {{
        const showBanner = () => {{
            if (document.getElementById('playwright-test-banner')) return;
            const banner = document.createElement('div');
            banner.id = 'playwright-test-banner';
            banner.innerText = 'Running: {display_name}';
            banner.style.position = 'fixed';
            banner.style.top = '0';
            banner.style.left = '0';
            banner.style.width = '100%';
            banner.style.backgroundColor = '#ffeb3b';
            banner.style.color = '#000000';
            banner.style.zIndex = '999999';
            banner.style.fontSize = '14px';
            banner.style.fontFamily = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif';
            banner.style.fontWeight = 'bold';
            banner.style.padding = '8px';
            banner.style.textAlign = 'center';
            banner.style.borderBottom = '2px solid #fbc02d';
            banner.style.boxShadow = '0 2px 8px rgba(0,0,0,0.15)';
            banner.style.pointerEvents = 'none';
            document.body.appendChild(banner);
        }};
        if (document.body) {{
            showBanner();
        }} else {{
            document.addEventListener('DOMContentLoaded', showBanner);
        }}
    }})();
    """
    try:
        page.context.add_init_script(script)
        if page.url != "about:blank":
            page.evaluate(script)
    except Exception:
        pass


@pytest.fixture
def debug_pause(request):
    """A fixture that returns a helper function to pause execution for debugging.
    If running in headed mode, it prompts the user in the terminal to press Enter.
    If a page is passed, it visually highlights the pause on the test name banner.
    """
    def _pause(page=None, duration=None, message="Paused for debugging"):
        import time

        is_headed = False
        try:
            is_headed = request.config.getoption("--headed")
        except Exception:
            pass

        # Update the banner/playback visually to indicate a pause
        if page:
            try:
                page.evaluate(f"""
                    (() => {{
                        const banner = document.getElementById('playwright-test-banner');
                        if (banner) {{
                            banner.innerText = '⏸️ {message}';
                            banner.style.backgroundColor = '#ff9800'; // Orange
                            banner.style.borderBottom = '2px solid #f57c00';
                        }}
                        const pbTitle = document.getElementById('pb-title');
                        if (pbTitle) {{
                            pbTitle.textContent = ' - ⏸️ {message}';
                            pbTitle.style.color = '#ff9800';
                        }}
                    }})()
                """)
            except Exception:
                pass

        print(f"\n[DEBUG PAUSE] {message}")
        if duration is not None:
            print(f"Sleeping for {duration} seconds...")
            time.sleep(duration)
        else:
            if is_headed:
                input(f"Paused: {message}. Press Enter in terminal to continue...")
            else:
                print("Running in headless mode, sleeping for 2 seconds instead of waiting for input...")
                time.sleep(2)

        # Restore original banner/playback status
        if page:
            try:
                test_name = request.node.name
                display_name = test_name.replace("test_", "").replace("_", " ").title()
                page.evaluate(f"""
                    (() => {{
                        const banner = document.getElementById('playwright-test-banner');
                        if (banner) {{
                            banner.innerText = 'Running: {display_name}';
                            banner.style.backgroundColor = '#ffeb3b';
                            banner.style.borderBottom = '2px solid #fbc02d';
                        }}
                        const pbTitle = document.getElementById('pb-title');
                        if (pbTitle) {{
                            pbTitle.textContent = ' - {display_name}';
                            pbTitle.style.color = '#ffeb3b';
                        }}
                    }})()
                """)
            except Exception:
                pass

    return _pause


# Pytest hooks for tracking fixture setup/teardown phases
def pytest_fixture_setup(fixturedef, request):
    """Called before a fixture's setup starts."""
    if getattr(request.config, "_playback_enabled", False):
        try:
            from utils.playback import playback
            playback.test_name = f"Fixture Setup: {fixturedef.argname}"
        except Exception:
            pass


def pytest_runtest_setup(item):
    """Called before a test's setup starts (before running fixtures)."""
    if getattr(item.config, "_playback_enabled", False):
        try:
            from utils.playback import playback
            display_name = item.name.replace("test_", "").replace("_", " ").title()
            playback.test_name = f"Preparing: {display_name}"
        except Exception:
            pass


def pytest_runtest_call(item):
    """Called to run the test case itself."""
    if getattr(item.config, "_playback_enabled", False):
        try:
            from utils.playback import playback
            display_name = item.name.replace("test_", "").replace("_", " ").title()
            playback.test_name = f"Running: {display_name}"
        except Exception:
            pass


def pytest_runtest_teardown(item, nextitem):
    """Called before a test's teardown starts."""
    if getattr(item.config, "_playback_enabled", False):
        try:
            from utils.playback import playback
            display_name = item.name.replace("test_", "").replace("_", " ").title()
            playback.test_name = f"Teardown: {display_name}"
        except Exception:
            pass



