from __future__ import annotations

from playwright.sync_api import Page

from utils.constants import CITY_URL
from pages.common.form_page import has_validation_feedback


class CitiesPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.citypage_url = CITY_URL

    def navigate(self) -> None:
        self.page.goto(self.citypage_url)

    def is_cities_visible(self) -> bool:
        return self.page.get_by_role("button", name="Add City").is_visible()

    def add_city(self, city_name: str) -> bool:
        self.page.get_by_role("button", name="Add City").click()
        self.page.locator(".react-select__input-container").nth(1).click()
        self.page.get_by_role("option", name="Tamil Nadu").click()
        self.page.locator("input[name=\"name\"]").fill(city_name)
        self.page.get_by_role("button", name="Create").click()
        self.page.get_by_text("City created successfully").wait_for()
        self.page.wait_for_load_state("networkidle")
        return self.page.get_by_text("City created successfully").is_visible()

    def validate_duplicate_city(self, city_name: str) -> bool:
        self.page.get_by_role("button", name="Add City").click()
        self.page.locator(".react-select__input-container").nth(1).click()
        self.page.get_by_role("option", name="Tamil Nadu").click()
        self.page.locator('input[name="name"]').fill(city_name)
        self.page.get_by_role("button", name="Create").click()
        return has_validation_feedback(
            self.page,
            r"already been taken",
            r"already exists",
            r"duplicate",
        )

    def validate_invalid_city_name(self, city_name: str) -> bool:
        self.page.get_by_role("button", name="Add City").click()
        self.page.locator(".react-select__input-container").nth(1).click()
        self.page.get_by_role("option", name="Tamil Nadu").click()
        self.page.locator('input[name="name"]').fill(city_name)
        self.page.get_by_role("button", name="Create").click()

        return has_validation_feedback(
            self.page,
            r"city.*(?:letters|alphabet|invalid|numbers)",
            r"name.*(?:letters|alphabet|invalid|numbers)",
        )

    def is_city_added(self, city_name: str) -> bool:
        self.page.get_by_role("textbox", name="Search...").fill(city_name)
        city_locator = self.page.get_by_text(city_name, exact=True).first
        try:
            city_locator.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False
    
    def search_city(self, city_name: str) -> bool:
        search_box = self.page.get_by_role("textbox", name="Search...")
        search_box.fill(city_name)
        search_box.press("Enter")
        self.page.wait_for_load_state("networkidle", timeout=5000)
        locator = self.page.get_by_text(city_name, exact=True).first
        try:
            locator.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False
        
    
    def delete_city(self, city_name: str) -> bool:
        self.page.get_by_role("textbox", name="Search...").fill(city_name)
        city_row = self.page.locator("tr", has=self.page.get_by_text(city_name, exact=True))
        city_row.wait_for(state="visible", timeout=5000) 
        city_row.get_by_title("delete").click()
        #self.page.get_by_title("delete").nth(0).click()
        self.page.get_by_role("button", name="Delete City").click()
        self.page.get_by_text("Deleted successfully.").wait_for()
        return self.page.get_by_text("Deleted successfully.").is_visible()
    
    def retrieve_city(self, city_name: str) -> bool:
        self.page.get_by_role("textbox", name="Search...").fill(city_name)
        city_row = self.page.locator("tr", has=self.page.get_by_text(city_name, exact=True))
        city_row.wait_for(state="visible", timeout=5000) 
        self.page.get_by_title("delete").first.click()
        self.page.get_by_role("button", name="Retrieve City").click()
        self.page.get_by_text("Retrieved successfully.").wait_for()
        return self.page.get_by_text("Retrieved successfully.").is_visible()
    
    def edit_city(self, old_city_name: str, new_city_name: str) -> bool:
        self.page.get_by_role("textbox", name="Search...").fill(old_city_name)
        city_row = self.page.locator("tr", has=self.page.get_by_text(old_city_name, exact=True))
        city_row.wait_for(state="visible", timeout=5000) 
        self.page.get_by_title("edit").click()
        self.page.locator("input[name=\"name\"]").fill(new_city_name)
        self.page.get_by_role("button", name="Update").click()
        self.page.get_by_text("City updated successfully").wait_for()
        return self.page.get_by_text("City updated successfully").is_visible()

    def delete_city_expect_fail(self, city_name: str) -> bool:
        self.page.get_by_role("textbox", name="Search...").fill(city_name)
        city_row = self.page.locator("tr", has=self.page.get_by_text(city_name, exact=True))
        city_row.wait_for(state="visible", timeout=5000) 
        city_row.get_by_title("delete").click()
        self.page.get_by_role("button", name="Delete City").click()
        
        # We expect a failure/error toast or the modal remaining open with an error
        # In either case, the city row should still exist in the table listing after a reload
        self.page.wait_for_timeout(2000)
        self.navigate()
        return self.search_city(city_name)

