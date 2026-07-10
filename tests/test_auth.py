from playwright.sync_api import Page
from utils.constants import  ADMIN_EMAIL, ADMIN_PASSWORD , DASHBOARD_URL
from pages.auth.login_page import LoginPage

def test_successful_login(page):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
    page.wait_for_url(lambda url: "/login" not in url , timeout=5000)
    
    assert page.url == DASHBOARD_URL
    
def test_failed_login(page):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("invalid@example.com", "invalidpassword")
    login_page.verify_invalid_credentials_message()

def test_empty_credentials(page):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("", "")
    assert login_page.page.get_by_text("Email is required").is_visible()
    assert login_page.page.get_by_text("Password is required").is_visible()

def test_url_has_https(page: Page):
    login_page = LoginPage(page)
    login_page.navigate()
    assert page.url.startswith("https://")
    
def test_toggle_password_visibility(page: Page):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.password_input.fill("testpassword")
    login_page.toggle_password_visibility()
    assert login_page.password_input.get_attribute("type") == "text"
    
    

    
