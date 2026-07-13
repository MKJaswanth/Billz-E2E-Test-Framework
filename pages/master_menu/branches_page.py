import re

from utils.constants import BRANCHES_URL
from utils.random_data import generate_random_address, generate_random_name, generate_random_code, generate_random_phone, generate_random_postal_code, generate_random_email
from pages.common.form_page import has_validation_feedback

class BranchesPage:
    def __init__(self, page):
        self.page = page
        self.branches_url = BRANCHES_URL
        
    def navigate(self):
        return self.page.goto(self.branches_url)
    
    def is_branches_visible(self):
        return self.page.get_by_role("button", name="Add Branch").is_visible()

    def has_actions_sorting_control(self):
        header = self.page.get_by_role(
            "columnheader", name=re.compile(r"^actions?$", re.IGNORECASE)
        ).first
        if header.count() == 0:
            return False
        return (
            header.get_attribute("aria-sort") is not None
            or header.locator("button, [role='button'], [data-sort], .sort-icon").count() > 0
        )
    
    def add_branch(self):
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
        
        self.page.locator(".react-select__input-container.css-19bb58m").first.click()
        self.page.get_by_role("option", name="Tamil Nadu").click()
        
        self.page.locator(".react-select__control.css-my3gbk-control > .react-select__value-container > .react-select__input-container").click()
        self.page.get_by_role("option", name=city_name).click()
        
        self.page.locator("input[name=\"postal_code\"]").fill(generate_random_postal_code())
        self.page.get_by_role("textbox", name="Enter 10-digit phone number").fill(generate_random_phone())
        self.page.locator("input[name=\"email\"]").fill(generate_random_email())
        self.page.get_by_role("spinbutton").fill("3")
        self.page.get_by_role("button", name="Create").click()
        return branch_name
    
    
    def search_branch(self, branch_name):
        self.page.get_by_role("textbox", name="Search branches...").fill(branch_name)
        branch_locator = self.page.get_by_text(branch_name, exact=True)
        try:
            branch_locator.wait_for(state="visible", timeout=10000)
            return True
        except Exception:
            return False
        
    def view_branch(self, branch_name):
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
        
    def edit_branch(self, branch_name):
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
        
    def delete_branch(self, branch_name):
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
        
    def retrieve_branch(self, branch_name):
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
        
    def validate_branch_name(self):
        self.page.get_by_role("button", name="Add Branch").click()
        self.page.locator("input[name=\"name\"]").fill("")
        self.page.get_by_role("button", name="Create").click()
        error_locator = self.page.get_by_text("Branch name is required")
        try:
            error_locator.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False
        
    def duplicate_branch_name(self, branch_name):
        from pages.master_menu.cities_page import CitiesPage
        from utils.random_data import generate_random_code
        
        # Create a dynamic city
        cities_page = CitiesPage(self.page)
        cities_page.navigate()
        city_name = f"AutoCity_{generate_random_code('C')}"
        cities_page.add_city(city_name)
        
        self.navigate()
        
        self.page.get_by_role("button", name="Add Branch").click()
        self.page.locator("input[name=\"name\"]").fill(branch_name)
        self.page.locator("input[name=\"code\"]").fill(generate_random_code())
        self.page.locator("input[name=\"address\"]").fill(generate_random_address())
        
        self.page.locator(".react-select__input-container.css-19bb58m").first.click()
        self.page.get_by_role("option", name="Tamil Nadu").click()
        
        self.page.locator(".react-select__control.css-my3gbk-control > .react-select__value-container > .react-select__input-container").click()
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

    def validate_invalid_phone(self, phone):
        self.page.get_by_role("button", name="Add Branch").click()
        self.page.locator('input[name="name"]').fill(generate_random_name("invalid_phone"))
        self.page.locator('input[name="code"]').fill(generate_random_code())
        self.page.locator('input[name="address"]').fill(generate_random_address())

        self.page.locator(".react-select__input-container.css-19bb58m").first.click()
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
   
