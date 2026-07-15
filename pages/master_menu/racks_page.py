from __future__ import annotations

from playwright.sync_api import Page

from utils.constants import RACKS_URL
from pages.common.form_page import has_validation_feedback

class RacksPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.racks_url = RACKS_URL

    def navigate(self) -> None:
        self.page.goto(self.racks_url)

    def is_racks_visible(self) -> bool:
        return self.page.get_by_role("button", name="Add Rack").is_visible()

    def add_rack(self, name: str, code: str, branch_name: str | None = None, description: str | None = None) -> None:
        self.page.get_by_role("button", name="Add Rack").click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)

        modal.locator("input[name=\"name\"]").fill(name)
        modal.locator("input[name=\"code\"]").fill(code)

        # Select branch
        modal.locator(".react-select__input-container").click()
        if branch_name:
            self.page.get_by_role("option", name=branch_name).click()
        else:
            # Select the first option if branch_name is not provided
            self.page.locator(".react-select__option").first.click()

        if description:
            try:
                add_desc_btn = modal.get_by_role("button", name="Add Description")
                if add_desc_btn.is_visible():
                    add_desc_btn.click()
            except Exception:
                pass
            modal.locator("textarea[name=\"description\"]").fill(description)

        modal.get_by_role("button", name="Create").click()
        
        toast = self.page.get_by_text("Rack created successfully").first
        toast.wait_for(state="visible", timeout=10000)
        modal.wait_for(state="hidden", timeout=10000)

    def validate_duplicate_rack(self, name: str, code: str, branch_name: str) -> bool:
        self.page.get_by_role("button", name="Add Rack").click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)
        modal.locator('input[name="name"]').fill(name)
        modal.locator('input[name="code"]').fill(code)
        modal.locator(".react-select__input-container").click()
        self.page.get_by_role("option", name=branch_name).click()
        modal.get_by_role("button", name="Create").click()
        return has_validation_feedback(
            self.page,
            r"already been taken",
            r"already exists",
            r"duplicate",
        )

    def search_rack(self, name: str) -> bool:
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

    def view_rack(self, name: str) -> bool:
        self.search_rack(name)
        row = self.page.locator("tr", has=self.page.get_by_text(name, exact=True))
        row.wait_for(state="visible", timeout=5000)

        row.get_by_title("view").click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)

        text_visible = modal.get_by_text(name).is_visible()
        modal.get_by_role("button", name="Back to List").click()
        modal.wait_for(state="hidden", timeout=5000)
        return text_visible

    def edit_rack(self, old_name: str, new_name: str) -> bool:
        self.search_rack(old_name)
        row = self.page.locator("tr", has=self.page.get_by_text(old_name, exact=True))
        row.wait_for(state="visible", timeout=5000)

        row.get_by_title("edit").click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)

        modal.locator("input[name=\"name\"]").fill(new_name)
        modal.get_by_role("button", name="Update").click()

        toast = self.page.get_by_text("Rack updated successfully").first
        try:
            toast.wait_for(state="visible", timeout=5000)
            modal.wait_for(state="hidden", timeout=5000)
            return True
        except Exception:
            return False

    def delete_rack(self, name: str) -> bool:
        self.search_rack(name)
        row = self.page.locator("tr", has=self.page.get_by_text(name, exact=True))
        row.wait_for(state="visible", timeout=5000)

        row.get_by_title("delete").first.click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)

        modal.get_by_role("button", name="Delete Rack").click()

        toast = self.page.get_by_text("Deleted successfully.").first
        try:
            toast.wait_for(state="visible", timeout=5000)
            modal.wait_for(state="hidden", timeout=5000)
            return True
        except Exception:
            return False

    def retrieve_rack(self, name: str) -> bool:
        self.search_rack(name)
        row = self.page.locator("tr", has=self.page.get_by_text(name, exact=True))
        row.wait_for(state="visible", timeout=5000)

        row.get_by_title("delete").first.click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)

        modal.get_by_role("button", name="Retrieve Rack").click()

        toast = self.page.get_by_text("Retrieved successfully.").first
        try:
            toast.wait_for(state="visible", timeout=5000)
            modal.wait_for(state="hidden", timeout=5000)
            return True
        except Exception:
            return False
