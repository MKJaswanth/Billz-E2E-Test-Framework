from __future__ import annotations

import re

from playwright.sync_api import Page

from utils.constants import BRANCHES_URL
from utils.random_data import generate_random_address, generate_random_name, generate_random_code, generate_random_phone, generate_random_postal_code, generate_random_email
from pages.common.form_page import has_validation_feedback

class BranchesPage:
    # Cities auto-created by add_branch/duplicate_branch_name, keyed by branch
    # name. Class-level so teardown fixtures that build a fresh BranchesPage
    # can still find and delete the cities that belong to a branch.
    _auto_cities: dict[str, list[str]] = {}

    def __init__(self, page: Page) -> None:
        self.page = page
        self.branches_url = BRANCHES_URL

    def cleanup_auto_city(self, branch_name: str) -> None:
        """Best-effort delete of the auto-created cities for a branch. Must
        run after the branch is deleted; the backend refuses to delete a city
        still assigned to a branch (including soft-deleted ones), so a
        failure here is logged, not raised."""
        from pages.master_menu.cities_page import CitiesPage

        city_names = self._auto_cities.pop(branch_name, [])
        if not city_names:
            return
        cities_page = CitiesPage(self.page)
        for city_name in city_names:
            try:
                cities_page.navigate()
                if cities_page.search_city(city_name):
                    cities_page.delete_city(city_name)
            except Exception as e:
                print(f"Teardown: could not delete auto city {city_name} for branch {branch_name}: {e}")
        
    def navigate(self) -> None:
        self.page.goto(self.branches_url)
    
    def is_branches_visible(self) -> bool:
        return self.page.get_by_role("button", name="Add Branch").is_visible()

    def has_actions_sorting_control(self) -> bool:
        header = self.page.get_by_role(
            "columnheader", name=re.compile(r"^actions?$", re.IGNORECASE)
        ).first
        if header.count() == 0:
            return False
        return (
            header.get_attribute("aria-sort") is not None
            or header.locator("button, [role='button'], [data-sort], .sort-icon").count() > 0
        )
    
    def add_branch(self) -> str:
        from pages.master_menu.cities_page import CitiesPage
        from utils.random_data import generate_random_code
        
        # 1. Create a dynamic city
        cities_page = CitiesPage(self.page)
        cities_page.navigate()
        city_name = f"AutoCity_{generate_random_code('C')}"
        cities_page.add_city(city_name)
        
        # 2. Go back to branches page and add branch
        self.navigate()
        
        branch_name = generate_random_name()
        self.page.get_by_role("button", name="Add Branch").click()
        self.page.locator("input[name=\"name\"]").fill(branch_name)
        self.page.locator("input[name=\"code\"]").fill(generate_random_code())
        self.page.locator("input[name=\"address\"]").fill(generate_random_address())
        
        self.page.locator("input[name='state_id']").locator("xpath=..").locator(".react-select__input-container").click()
        self.page.get_by_role("option", name="Tamil Nadu").click()
        
        self.page.locator("input[name='city_id']").locator("xpath=..").locator(".react-select__input-container").click()
        self.page.get_by_role("option", name=city_name).click()
        
        self.page.locator("input[name=\"postal_code\"]").fill(generate_random_postal_code())
        self.page.get_by_role("textbox", name="Enter 10-digit phone number").fill(generate_random_phone())
        self.page.locator("input[name=\"email\"]").fill(generate_random_email())
        self.page.get_by_role("spinbutton").fill("3")
        self.page.get_by_role("button", name="Create").click()
        self._auto_cities.setdefault(branch_name, []).append(city_name)
        return branch_name
    
    
    def search_branch(self, branch_name: str) -> bool:
        search_box = self.page.get_by_role("textbox", name="Search branches...")
        search_box.fill(branch_name)
        search_box.press("Enter")
        self.page.wait_for_load_state("networkidle", timeout=5000)
        locator = self.page.get_by_text(branch_name, exact=True).first
        try:
            locator.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False
        
    def view_branch(self, branch_name: str) -> bool:
        self.page.get_by_role("textbox", name="Search branches...").fill(branch_name)
        branch_row = self.page.locator("tr", has=self.page.get_by_text(branch_name, exact=True))
        branch_row.wait_for(state="visible", timeout=5000)
        branch_row.get_by_title("view").click()
        
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)
        name_locator = modal.get_by_text(branch_name, exact=True)
        try:
            name_locator.wait_for(state="visible", timeout=3000)
            is_name_visible = True
        except Exception:
            is_name_visible = False
            
    
        self.page.get_by_role("button", name="Back to List").click()
        return is_name_visible
        
    def edit_branch(self, branch_name: str) -> bool:
        self.page.get_by_role("textbox", name="Search branches...").fill(branch_name)
        branch_row = self.page.locator("tr", has=self.page.get_by_text(branch_name, exact=True))
        branch_row.wait_for(state="visible", timeout=5000) 
        self.page.get_by_title("edit").first.click()
        self.page.locator("input[name=\"name\"]").click()
        self.page.locator("input[name=\"name\"]").fill(branch_name + "_edited")
        self.page.locator("input[name=\"code\"]").click()
        self.page.get_by_role("button", name="Update").click()
        toast_locator = self.page.get_by_text("Branch updated successfully")
        try:
            toast_locator.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False
        
    def delete_branch(self, branch_name: str) -> bool:
        self.page.get_by_role("textbox", name="Search branches...").fill(branch_name)
        branch_row = self.page.locator("tr", has=self.page.get_by_text(branch_name, exact=True))
        branch_row.wait_for(state="visible", timeout=5000) 
        self.page.get_by_title("delete").first.click()
        self.page.get_by_role("button", name="Delete Branch").click()
        toast_locator = self.page.get_by_text("Deleted successfully.")
        try:
            toast_locator.wait_for(state="visible", timeout=1000)
            return True
        except Exception:
            return False    
        
    def retrieve_branch(self, branch_name: str) -> bool:
        self.page.get_by_role("textbox", name="Search branches...").fill(branch_name)
        branch_row = self.page.locator("tr", has=self.page.get_by_text(branch_name, exact=True))
        branch_row.wait_for(state="visible", timeout=5000) 
        self.page.get_by_title("delete").first.click()
        self.page.get_by_role("button", name="Retrieve Branch").click()
        toast_locator = self.page.get_by_text("Retrieved successfully.")
        try:
            toast_locator.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False
        
    def validate_branch_name(self) -> bool:
        self.page.get_by_role("button", name="Add Branch").click()
        self.page.locator("input[name=\"name\"]").fill("")
        self.page.get_by_role("button", name="Create").click()
        error_locator = self.page.get_by_text("Branch name is required")
        try:
            error_locator.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False
        
    def duplicate_branch_name(self, branch_name: str) -> bool:
        from pages.master_menu.cities_page import CitiesPage
        from utils.random_data import generate_random_code
        
        # Create a dynamic city
        cities_page = CitiesPage(self.page)
        cities_page.navigate()
        city_name = f"AutoCity_{generate_random_code('C')}"
        cities_page.add_city(city_name)
        self._auto_cities.setdefault(branch_name, []).append(city_name)

        self.navigate()

        self.page.get_by_role("button", name="Add Branch").click()
        self.page.locator("input[name=\"name\"]").fill(branch_name)
        self.page.locator("input[name=\"code\"]").fill(generate_random_code())
        self.page.locator("input[name=\"address\"]").fill(generate_random_address())
        
        self.page.locator("input[name='state_id']").locator("xpath=..").locator(".react-select__input-container").click()
        self.page.get_by_role("option", name="Tamil Nadu").click()
        
        self.page.locator("input[name='city_id']").locator("xpath=..").locator(".react-select__input-container").click()
        self.page.get_by_role("option", name=city_name).click()
        
        self.page.locator("input[name=\"postal_code\"]").fill(generate_random_postal_code())
        self.page.get_by_role("spinbutton").fill("3")
        self.page.get_by_role("button", name="Create").click()
        
        error_locator = self.page.get_by_text("The name has already been taken.")
        try:
            error_locator.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False

    def validate_invalid_phone(self, phone: str) -> bool:
        self.page.get_by_role("button", name="Add Branch").click()
        self.page.locator('input[name="name"]').fill(generate_random_name("invalid_phone"))
        self.page.locator('input[name="code"]').fill(generate_random_code())
        self.page.locator('input[name="address"]').fill(generate_random_address())

        self.page.locator("input[name='state_id']").locator("xpath=..").locator(".react-select__input-container").click()
        self.page.get_by_role("option", name="Tamil Nadu").click()

        self.page.locator('input[name="postal_code"]').fill(generate_random_postal_code())
        self.page.get_by_role("textbox", name="Enter 10-digit phone number").fill(phone)
        self.page.locator('input[name="email"]').fill(generate_random_email())
        self.page.get_by_role("spinbutton").fill("3")
        self.page.get_by_role("button", name="Create").click()

        return has_validation_feedback(
            self.page,
            r"phone.*(?:10|invalid|valid|digits)",
            r"10[- ]digit.*phone",
        )
