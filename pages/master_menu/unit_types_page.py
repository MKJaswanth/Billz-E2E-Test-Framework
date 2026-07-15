from __future__ import annotations

from playwright.sync_api import Page

from utils.constants import UNIT_TYPES_URL
from pages.common.form_page import has_validation_feedback


class UnitTypesPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.unit_types_url = UNIT_TYPES_URL
        
    def navigate(self) -> None:
        self.page.goto(self.unit_types_url)
    
    def is_unit_types_visible(self) -> bool:
        return self.page.get_by_role("button", name="Add Unit Type").is_visible()

    def add_unit_type(self, name: str, unit: str, description: str) -> bool:
        self.page.get_by_role("button", name="Add Unit Type").click()
        self.page.get_by_role("textbox", name="Enter unit type name").fill(name)
        self.page.get_by_role("textbox", name="Enter unit symbol (e.g., kg,").fill(unit)
        self.page.get_by_role("textbox", name="Enter unit type description").fill(description)
        self.page.get_by_role("button", name="Create Unit Type").click()

        toast = self.page.get_by_text("Unit type created successfully")
        try:
            toast.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False

    def search_unit_type(self, name: str) -> bool:
        search_box = self.page.get_by_role("textbox", name="Search...")
        search_box.fill(name)
        search_box.press("Enter")
        self.page.wait_for_load_state("networkidle", timeout=5000)
        locator = self.page.get_by_text(name, exact=True).first
        try:
            locator.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False

    def view_unit_type(self, name: str) -> bool:
        self.page.get_by_title("view").click()
        
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)
        
        unit_locator = modal.get_by_text(name, exact=True).first
        try:
            unit_locator.wait_for(state="visible", timeout=3000)
            is_visible = True
        except Exception: 
            is_visible = False
        
        modal.get_by_role("button", name="Close").click()
        return is_visible

    def edit_unit_type(self, old_name: str, new_name: str, new_unit: str, new_description: str) -> bool:
        self.search_unit_type(old_name)
        unit_row = self.page.locator("tr", has=self.page.get_by_text(old_name, exact=True))
        unit_row.wait_for(state="visible", timeout=5000)
        
        unit_row.get_by_title("edit").click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)
        
        self.page.get_by_role("textbox", name="Enter unit type name").fill(new_name)
        self.page.get_by_role("textbox", name="Enter unit symbol (e.g., kg,").fill(new_unit)
        self.page.get_by_role("textbox", name="Enter unit type description").fill(new_description)
        
        self.page.get_by_role("button", name="Update Unit Type").click()
        
        toast = self.page.get_by_text("Unit type updated successfully")
        try:
            toast.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False

    def delete_unit_type(self, name: str) -> bool:
        self.search_unit_type(name)
        unit_row = self.page.locator("tr", has=self.page.get_by_text(name, exact=True))
        unit_row.wait_for(state="visible", timeout=5000)
        
        unit_row.get_by_title("delete").click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)
        
        modal.get_by_role("button", name="Delete Unit Type").click()
        
        toast = self.page.get_by_text("Deleted successfully.")
        try:
            toast.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False

    def retrieve_unit_type(self, name: str) -> bool:
        self.search_unit_type(name)
        unit_row = self.page.locator("tr", has=self.page.get_by_text(name, exact=True))
        unit_row.wait_for(state="visible", timeout=5000)
        
        unit_row.get_by_title("delete").first.click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)
        
        modal.get_by_role("button", name="Retrieve Unit Type").click()
        
        toast = self.page.get_by_text("Retrieved successfully.")
        try:
            toast.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False

    def validate_required_fields(self) -> bool:
        self.page.get_by_role("button", name="Add Unit Type").click()
        self.page.get_by_role("button", name="Create Unit Type").click()
        
        name_err = self.page.get_by_text("Name is required")
        symbol_err = self.page.get_by_text("Symbol is required")
        desc_err = self.page.get_by_text("Description is required")
        
        try:
            name_err.wait_for(state="visible", timeout=5000)
            symbol_err.wait_for(state="visible", timeout=5000)
            desc_err.wait_for(state="visible", timeout=5000)
            is_valid = True
        except Exception:
            is_valid = False
            
        self.navigate()
        return is_valid

    def validate_duplicate_unit(self, name: str, unit: str, description: str) -> bool:
        self.page.get_by_role("button", name="Add Unit Type").click()
        self.page.get_by_role("textbox", name="Enter unit type name").fill(name)
        self.page.get_by_role("textbox", name="Enter unit symbol (e.g., kg,").fill(unit)
        self.page.get_by_role("textbox", name="Enter unit type description").fill(description)
        self.page.get_by_role("button", name="Create Unit Type").click()
        return has_validation_feedback(
            self.page,
            r"already been taken",
            r"already exists",
            r"duplicate",
        )
