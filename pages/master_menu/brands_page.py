from __future__ import annotations

from playwright.sync_api import Page

from utils.constants import BRANDS_URL
from pages.common.form_page import has_validation_feedback

class BrandPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.url = BRANDS_URL

    def navigate(self) -> None:
        self.page.goto(self.url)

    def is_brands_visible(self) -> bool:
        return self.page.get_by_role("button", name="Add Brand").is_visible()

    def search_brand(self, brand_name: str) -> bool:
        search_box = self.page.get_by_role("textbox", name="Search...")
        search_box.fill(brand_name)
        search_box.press("Enter")
        self.page.wait_for_load_state("networkidle", timeout=5000)
        locator = self.page.get_by_text(brand_name, exact=True).first
        try:
            locator.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False
        

    def add_brand(self, name: str, description: str) -> str:
        self.page.get_by_role("button", name="Add Brand").click()
        self.page.locator("input[name='name']").fill(name)
        self.page.locator("textarea[name=\"description\"]").fill(description)
        self.page.locator("button[type='submit']").click()
        self.page.get_by_text("Brand created successfully").wait_for(state="visible" , timeout=3000)

        return name

    def edit_brand(self, old_name: str, new_name: str) -> bool:
        self.search_brand(old_name)
        category_row = self.page.locator("tr", has=self.page.get_by_text(old_name, exact=True))
        category_row.wait_for(state="visible", timeout=15000)
        
        category_row.get_by_title("edit").click()
        self.page.locator("input[name=\"name\"]").fill(new_name)
        self.page.get_by_role("button", name="Update").click()
        
        toast = self.page.get_by_text("Brand updated successfully")
        try:
            toast.wait_for(state="visible", timeout=15000)
            return True
        except Exception:
            return False  

    def view_brand(self, name: str) -> bool:
        self.search_brand(name)
        category_row = self.page.locator("tr", has=self.page.get_by_text(name, exact=True))
        category_row.wait_for(state="visible", timeout=15000)
        
        category_row.get_by_title("view").click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=15000)
        name_locator = modal.get_by_text(name, exact=True).first
        try:
            name_locator.wait_for(state="visible", timeout=13000)
            is_name_visible = True
        except Exception:
            is_name_visible = False
            
    
        self.page.get_by_role("button", name="Back to List").click()
        return is_name_visible


    def delete_brand(self, brand_name: str) -> bool:
        self.search_brand(brand_name)
        category_row = self.page.locator("tr", has=self.page.get_by_text(brand_name, exact=True))
        category_row.wait_for(state="visible", timeout=15000)
        
        category_row.get_by_title("delete").click()
        self.page.get_by_role("button", name="Delete Brand").click()
        toast = self.page.get_by_text("Deleted successfully.")
        try:
            toast.wait_for(state="visible", timeout=15000)
            return True
        except Exception:
            return False  

    def retrieve_brand(self, brand_name: str) -> bool:
        self.search_brand(brand_name)
        brand_row = self.page.locator("tr", has=self.page.get_by_text(brand_name, exact=True))
        brand_row.wait_for(state="visible", timeout=15000)
        
        brand_row.get_by_title("delete").click()
        self.page.get_by_role("button", name="Delete Brand").click()
        brand_row.get_by_title("delete").click()
        self.page.get_by_role("button", name="Retrieve Brand").click()
        toast = self.page.get_by_text("Retrieved successfully.")
        try:
            toast.wait_for(state="visible", timeout=15000)
            return True
        except Exception:
            return False  

    def validate_required_fields(self) -> bool:
        self.page.get_by_role("button", name="Add Brand").click()
        self.page.get_by_role("button", name="Create").click()
        
        error_locator = self.page.get_by_text("Brand Name is required")
        try:
            error_locator.wait_for(state="visible", timeout=15000)
            is_valid = True
        except Exception:
            is_valid = False
            
        self.navigate()
        return is_valid

    def validate_blank_only_name(self) -> bool:
        self.page.get_by_role("button", name="Add Brand").click()
        self.page.locator("input[name='name']").fill("   ")
        self.page.locator('textarea[name="description"]').fill("validation test")
        self.page.locator("button[type='submit']").click()
        return has_validation_feedback(
            self.page,
            r"brand name.*required",
            r"name.*blank",
            r"name.*empty",
        )

    def validate_name_is_trimmed(self, name: str, description: str) -> bool:
        self.add_brand(f"  {name}  ", description)
        return self.search_brand(name)

    def validate_duplicate_brand(self, name: str, description: str) -> bool:
        self.page.get_by_role("button", name="Add Brand").click()
        self.page.locator("input[name='name']").fill(name)
        self.page.locator("textarea[name=\"description\"]").fill(description)
        self.page.locator("button[type='submit']").click()
        
        return has_validation_feedback(
            self.page,
            r"brand.*name.*already.*taken",
            r"name.*already.*taken",
            r"already been taken",
            r"duplicate",
        )

