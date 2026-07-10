import os
import time
from playwright.sync_api import sync_playwright
from pages.auth.login_page import LoginPage
from pages.master_menu.brands_page import BrandPage
from utils.constants import ADMIN_EMAIL, ADMIN_PASSWORD

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
        
        # Login
        print("Logging in...")
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.wait_for_url(lambda url: "/login" not in url, timeout=10000)
        page.wait_for_load_state("networkidle")
        
        # Navigate to Brands
        print("Navigating to Brands page...")
        brand_page = BrandPage(page)
        brand_page.navigate()
        page.wait_for_load_state("networkidle")
        
        # Add a brand
        brand_name = "cle_debug_123"
        print(f"Adding brand: {brand_name}")
        brand_page.add_brand(brand_name, "Debugging description")
        
        # Search the brand
        print(f"Searching for brand: {brand_name}")
        search_input = page.get_by_role("textbox", name="Search...")
        search_input.fill(brand_name)
        search_input.press("Enter")
        
        # Wait a few seconds for any updates
        time.sleep(5)
        
        # Capture screenshot
        screenshot_path = "brands_search_debug.png"
        page.screenshot(path=screenshot_path)
        print(f"Saved screenshot to {screenshot_path}")
        
        # Print table text content
        table = page.locator("table")
        if table.count() > 0:
            print("Table content:")
            print(table.first.inner_text())
        else:
            print("No table found on page!")
            
        browser.close()

if __name__ == "__main__":
    run()
