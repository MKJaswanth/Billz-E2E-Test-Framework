import time
from playwright.sync_api import sync_playwright
from pages.auth.login_page import LoginPage
from pages.master_menu.brands_page import BrandPage
from utils.constants import ADMIN_EMAIL, ADMIN_PASSWORD
from utils.random_data import generate_random_name, generate_random_description

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
        
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.wait_for_url(lambda url: "/login" not in url, timeout=10000)
        page.wait_for_load_state("networkidle")
        
        brand_page = BrandPage(page)
        brand_page.navigate()
        page.wait_for_load_state("networkidle")
        
        brand_name = generate_random_name("cle")
        description = generate_random_description("cle")
        
        print(f"Creating brand. Name: '{brand_name}', Description: '{description}'")
        brand_page.add_brand(brand_name, description)
        
        print("Calling search_brand...")
        res = brand_page.search_brand(brand_name)
        print(f"search_brand returned: {res}")
        
        # Let's inspect the count and elements matched by get_by_text
        locator = page.get_by_text(brand_name, exact=True)
        print(f"get_by_text match count: {locator.count()}")
        for i in range(locator.count()):
            try:
                print(f"Match {i}: tag={locator.nth(i).evaluate('el => el.tagName')}, visible={locator.nth(i).is_visible()}")
            except Exception as e:
                print(f"Match {i} info failed: {e}")
                
        # Clean up
        brand_page.delete_brand(brand_name)
        browser.close()

if __name__ == "__main__":
    run()
