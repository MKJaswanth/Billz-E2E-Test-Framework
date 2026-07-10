import sys
import os
import time
from playwright.sync_api import sync_playwright

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pages.auth.login_page import LoginPage
from pages.master_menu.roles_page import RolesPage
from utils.constants import ADMIN_EMAIL, ADMIN_PASSWORD

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
        
        roles_page = RolesPage(page)
        roles_page.navigate()
        page.wait_for_load_state("networkidle")
        
        print("Adding role...")
        role_name = roles_page.add_roles()
        page.wait_for_load_state("networkidle")
        
        print(f"Viewing role: {role_name}")
        page.get_by_role("textbox", name="Search roles...").fill(role_name)
        
        role_row = page.locator("tr", has=page.get_by_text(role_name, exact=True))
        role_row.wait_for(state="visible", timeout=5000)
        role_row.get_by_title("view").click()
        
        time.sleep(1)
        dialogs = page.locator("[role='dialog'], .modal, .modal-content, form")
        print(f"Found {dialogs.count()} dialogs/modals")
        if dialogs.count() > 0:
            print("Modal Inner HTML:")
            print(dialogs.first.inner_html()[:2000])
            print("Modal Inner Text:")
            print(dialogs.first.inner_text())
        else:
            print("No modal dialog visible!")
            
        browser.close()

if __name__ == "__main__":
    run()
