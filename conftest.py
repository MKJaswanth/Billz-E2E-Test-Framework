import os
import pytest
from pages.auth.login_page import LoginPage
from utils.constants import ADMIN_EMAIL, ADMIN_PASSWORD

STORAGE_STATE_PATH = "auth_state.json"

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "ignore_https_errors": True,
        "viewport": {"width": 1280, "height": 720}
    }

@pytest.fixture(scope="session")
def auth_state(browser):
    # Log in once per test session and save storage state
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
    page.wait_for_url(lambda url: "/login" not in url, timeout=10000)
    page.wait_for_load_state("networkidle")
    
    # Save the session state (cookies, local storage, etc.)
    context.storage_state(path=STORAGE_STATE_PATH)
    context.close()
    
    yield STORAGE_STATE_PATH
    
    # Clean up file after session completes
    if os.path.exists(STORAGE_STATE_PATH):
        try:
            os.remove(STORAGE_STATE_PATH)
        except Exception:
            pass

@pytest.fixture
def logged_in_page(browser, auth_state):
    # Create a new context using the pre-authenticated state
    context = browser.new_context(storage_state=auth_state, ignore_https_errors=True)
    page = context.new_page()
    yield page
    context.close()
