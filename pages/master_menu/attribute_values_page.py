from __future__ import annotations

from playwright.sync_api import Page

from utils.constants import ATTRIBUTE_VALUES_URL
from pages.common.form_page import has_validation_feedback

class AttributeValuesPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.attribute_values_url = ATTRIBUTE_VALUES_URL
        
    def navigate(self) -> None:
        self.page.goto(self.attribute_values_url)
        
    def is_attribute_values_visible(self) -> bool:
        return self.page.get_by_role("button", name="Add Attribute Values").is_visible()
        
    def add_attribute_value(self, key_name: str, value: str, description: str | None = None) -> None:
        self.page.get_by_role("button", name="Add Attribute Values").click()
        
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)
        
        modal.locator(".react-select__control").first.click()
        self.page.get_by_role("option", name=key_name).click()
        

        modal.locator("input[name=\"items.0.value\"]").fill(value)
        
        if description:
            modal.get_by_role("button", name="Add Notes").click()
            modal.locator("textarea[name=\"items.0.description\"]").fill(description)
            
        modal.get_by_role("button", name="Create").click()
        
    def search_attribute_value(self, value: str) -> bool:
        search_box = self.page.get_by_role("textbox", name="Search...")
        search_box.fill(value)
        search_box.press("Enter")
        self.page.wait_for_load_state("networkidle", timeout=5000)
        locator = self.page.get_by_text(value, exact=True).first
        try:
            locator.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False

    def view_attribute_value(self, value: str) -> bool:
        self.search_attribute_value(value)
        row = self.page.locator("tr", has=self.page.get_by_text(value, exact=True))
        row.wait_for(state="visible", timeout=5000)
        
        row.get_by_title("view").click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)
        
        try:
            modal.get_by_text(value, exact=True).first.wait_for(state="visible", timeout=5000)
            is_visible = True
        except Exception:
            is_visible = False
            
        modal.locator(".btn-close").click()
        return is_visible

    def edit_attribute_value(self, old_value: str, new_value: str) -> bool:
        self.search_attribute_value(old_value)
        row = self.page.locator("tr", has=self.page.get_by_text(old_value, exact=True))
        row.wait_for(state="visible", timeout=5000)
        
        row.get_by_title("edit").click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)
        
        try:
            modal.locator(".spinner-border").wait_for(state="hidden", timeout=10000)
        except Exception:
            pass
            
        modal.locator("input[name=\"items.0.value\"]").fill(new_value)
        modal.get_by_role("button", name="Update").click()
        
        toast = self.page.get_by_text("Attribute values updated").first
        try:
            toast.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False

    def delete_attribute_value(self, value: str) -> bool:
        self.search_attribute_value(value)
        row = self.page.locator("tr", has=self.page.get_by_text(value, exact=True))
        row.wait_for(state="visible", timeout=5000)
        
        row.get_by_title("delete").first.click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)
        
        modal.get_by_role("button", name="Delete Attribute Value").click()
        
        toast = self.page.get_by_text("Deleted successfully.")
        try:
            toast.wait_for(state="visible", timeout=10000)
            return True
        except Exception:
            return False

    def retrieve_attribute_value(self, value: str) -> bool:
        self.search_attribute_value(value)
        row = self.page.locator("tr", has=self.page.get_by_text(value, exact=True))
        row.wait_for(state="visible", timeout=5000)
        
        row.get_by_title("delete").first.click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)
        
        modal.get_by_role("button", name="Retrieve Attribute Value").click()
        
        toast = self.page.get_by_text("Retrieved successfully.")
        try:
            toast.wait_for(state="visible", timeout=10000)
            return True
        except Exception:
            return False

    def validate_required_fields(self) -> bool:
        self.page.get_by_role("button", name="Add Attribute Values").click()
        self.page.get_by_role("button", name="Create").click()
        
        error_locator = self.page.get_by_text("Value is required")
        try:
            error_locator.wait_for(state="visible", timeout=5000)
            is_valid = True
        except Exception:
            is_valid = False
            
        self.navigate()
        return is_valid

    def validate_duplicate_value(self, key_name: str, value: str) -> bool:
        self.page.get_by_role("button", name="Add Attribute Values").click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)
        modal.locator(".react-select__control").first.click()
        self.page.get_by_role("option", name=key_name).click()
        modal.locator('input[name="items.0.value"]').fill(value)
        modal.get_by_role("button", name="Create").click()
        return has_validation_feedback(
            self.page,
            r"already been taken",
            r"already exists",
            r"duplicate",
        )
