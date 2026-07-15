from __future__ import annotations

from playwright.sync_api import Page

from utils.constants import SAC_HSN_URL
from pages.common.form_page import has_validation_feedback

class SacHsnPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.sac_hsn_url = SAC_HSN_URL

    def navigate(self) -> None:
        self.page.goto(self.sac_hsn_url)

    def is_sac_hsn_visible(self) -> bool: 
        return self.page.get_by_role("button", name="Add SAC/HSN Code").is_visible()

    def add_sac_hsn_code(self, type_choice: str, code: str, description: str | None = None) -> None:
        self.page.get_by_role("button", name="Add SAC/HSN Code").click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)

        modal.locator(".react-select__input-container").first.click()
        self.page.get_by_role("option", name=type_choice).click()

        modal.locator("input[name=\"code\"]").fill(code)

        if description:
            try:
                # If there's an Add Description button to toggle description visibility
                add_desc_btn = modal.get_by_role("button", name="Add Description")
                if add_desc_btn.is_visible():
                    add_desc_btn.click()
            except Exception:
                pass
            modal.locator("textarea[name=\"description\"]").fill(description)

        modal.get_by_role("button", name="Create").click()
        modal.wait_for(state="hidden", timeout=10000)

    def search_sac_hsn_code(self, code: str) -> bool:
        search_box = self.page.get_by_role("textbox", name="Search...")
        search_box.fill(code)
        search_box.press("Enter")
        self.page.wait_for_load_state("networkidle", timeout=5000)
        locator = self.page.get_by_text(code, exact=True).first
        try:
            locator.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False

    def view_sac_hsn_code(self, code: str) -> bool:
        self.search_sac_hsn_code(code)
        row = self.page.locator("tr", has=self.page.get_by_text(code, exact=True))
        row.wait_for(state="visible", timeout=5000)

        row.get_by_title("view").first.click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)

        text_visible = modal.get_by_text(code).is_visible()
        modal.get_by_role("button", name="Back").click()
        modal.wait_for(state="hidden", timeout=5000)
        return text_visible

    def edit_sac_hsn_code(self, old_code: str, new_code: str) -> bool:
        self.search_sac_hsn_code(old_code)
        row = self.page.locator("tr", has=self.page.get_by_text(old_code, exact=True))
        row.wait_for(state="visible", timeout=5000)

        row.get_by_title("edit").first.click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)

        modal.locator("input[name=\"code\"]").fill(new_code)
        modal.get_by_role("button", name="Update").click()

        toast = self.page.get_by_text("GST Code updated successfully").first
        try:
            toast.wait_for(state="visible", timeout=5000)
            modal.wait_for(state="hidden", timeout=5000)
            return True
        except Exception:
            return False

    def delete_sac_hsn_code(self, code: str) -> bool:
        self.search_sac_hsn_code(code)
        row = self.page.locator("tr", has=self.page.get_by_text(code, exact=True))
        row.wait_for(state="visible", timeout=5000)

        row.get_by_title("delete").first.click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)

        modal.get_by_role("button", name="Delete Code").click()

        toast = self.page.get_by_text("Deleted successfully.").first
        try:
            toast.wait_for(state="visible", timeout=5000)
            modal.wait_for(state="hidden", timeout=5000)
            return True
        except Exception:
            return False

    def retrieve_sac_hsn_code(self, code: str) -> bool:
        self.search_sac_hsn_code(code)
        row = self.page.locator("tr", has=self.page.get_by_text(code, exact=True))
        row.wait_for(state="visible", timeout=5000)

        row.get_by_title("delete").first.click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)

        modal.get_by_role("button", name="Retrieve Code").click()

        toast = self.page.get_by_text("Retrieved successfully.").first
        try:
            toast.wait_for(state="visible", timeout=5000)
            modal.wait_for(state="hidden", timeout=5000)
            return True
        except Exception:
            return False

    def validate_invalid_code(self, code: str, type_choice: str = "SAC") -> bool:
        self.page.get_by_role("button", name="Add SAC/HSN Code").click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)
        modal.locator(".react-select__input-container").first.click()
        self.page.get_by_role("option", name=type_choice).click()
        modal.locator('input[name="code"]').fill(code)
        modal.get_by_role("button", name="Create").click()

        return has_validation_feedback(
            self.page,
            r"code.*(?:invalid|valid|numeric|digits|length|characters|required)",
            r"invalid.*code",
        )

    def validate_duplicate_sac_hsn_code(self, code: str, type_choice: str = "SAC") -> bool:
        self.page.get_by_role("button", name="Add SAC/HSN Code").click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)
        modal.locator(".react-select__input-container").first.click()
        self.page.get_by_role("option", name=type_choice).click()
        modal.locator('input[name="code"]').fill(code)
        modal.get_by_role("button", name="Create").click()
        
        return has_validation_feedback(
            self.page,
            r"already been taken",
            r"already exists",
            r"duplicate",
        )

