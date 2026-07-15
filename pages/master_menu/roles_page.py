from __future__ import annotations

from playwright.sync_api import Page

from utils.constants import ROLES_URL
from utils.random_data import generate_random_name , generate_random_description

class RolesPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.roles_url = ROLES_URL
        
    def navigate(self) -> None:
        self.page.goto(self.roles_url)
    
    def is_roles_visible(self) -> bool:
        return self.page.get_by_role("button", name="Add Role").is_visible()
    
    def add_roles(self) -> str:
        role_name =  generate_random_name("Role")
        role_description = generate_random_description("description")
        self.page.get_by_role("button", name="Add Role").click()
        self.page.get_by_role("textbox", name="Enter role name").fill(role_name)
        self.page.get_by_role("textbox", name="Enter role description").fill(role_description)
        self.page.locator("#group-products").check()
        self.page.get_by_role("checkbox", name="Create Suppliers").check()
        self.page.get_by_role("button", name="Create Role").click()
        self.page.get_by_text("Role created successfully").wait_for()
        return role_name
    
    def search_roles(self, role_name: str) -> bool:
        search_box = self.page.get_by_role("textbox", name="Search roles...")
        search_box.fill(role_name)
        search_box.press("Enter")
        self.page.wait_for_load_state("networkidle", timeout=5000)
        locator = self.page.get_by_text(role_name, exact=True).first
        try:
            locator.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False   
        
    def view_roles(self, role_name: str) -> bool:
        self.page.get_by_role("textbox", name="Search roles...").fill(role_name)
        role_row = self.page.locator("tr", has=self.page.get_by_text(role_name, exact=True))
        role_row.wait_for(state="visible", timeout=5000)
        
        role_row.get_by_title("view").click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)
        print(modal.inner_text())

        try:
            modal.get_by_text(role_name, exact=True).wait_for(state="visible", timeout=10000)
            return True
        except Exception:
            return False
        
    def edit_role(self, role_name: str, new_role_name: str) -> bool:
        
        self.page.get_by_role("textbox", name="Search roles...").fill(role_name)
        role_row = self.page.locator("tr", has=self.page.get_by_text(role_name, exact=True))
        role_row.wait_for(state="visible", timeout=5000)
        
        role_row.get_by_title("edit").click()
        self.page.locator("input[name=\"name\"]").fill(new_role_name)
        self.page.get_by_role("button", name="Update").click()
        
        toast = self.page.get_by_text("updated successfully")
        
        try:
            toast.wait_for(state="visible" , timeout=5000)
            return True
        except Exception:
            return False
        
    def delete_role(self, role_name: str) -> bool:
        self.page.get_by_role("textbox", name="Search roles...").fill(role_name)
        role_row = self.page.locator("tr", has=self.page.get_by_text(role_name, exact=True))
        role_row.wait_for(state="visible", timeout=5000)
        
        self.page.get_by_title("delete").first.click()
        self.page.get_by_role("button", name="Delete Role").click()
        
        toast = self.page.get_by_text("Deleted successfully.").first
        
        try:
            toast.wait_for(state = "visible" , timeout=1000)
            return True 
        except Exception:
            return False
        
    def retrieve_role(self, role_name: str) -> bool:
        
        self.page.get_by_role("textbox", name="Search roles...").fill(role_name)
        role_row = self.page.locator("tr", has=self.page.get_by_text(role_name, exact=True))
        role_row.wait_for(state="visible", timeout=5000) 
        role_row.get_by_title("delete").first.click()
        
        self.page.get_by_role("button", name="Delete Role").click()
        self.page.get_by_text("Deleted successfully.").wait_for(state="visible", timeout=5000)
        
        role_row.get_by_title("delete").click()
        self.page.get_by_role("button", name="Retrieve Role").click()
        toast = self.page.get_by_text("Retrieved successfully.")
        
        try:
            toast.wait_for(state = "visible" , timeout=1000)
            return True 
        except Exception:
            return False
