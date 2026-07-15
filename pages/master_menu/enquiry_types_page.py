from __future__ import annotations

from playwright.sync_api import Page

from utils.constants import ENQUIRY_TYPES_URL

class EnquiryTypesPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.enquiry_types_url = ENQUIRY_TYPES_URL

    def navigate(self) -> None:
        self.page.goto(self.enquiry_types_url)

    def is_enquiry_types_visible(self) -> bool:
        return self.page.get_by_role("button", name="Add Enquiry Type").is_visible()

    def add_enquiry_type(self, name: str, notes: str | None = None) -> None:
        self.page.get_by_role("button", name="Add Enquiry Type").click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)

        modal.locator("input[name=\"name\"]").fill(name)

        if notes:
            modal.locator("textarea[name=\"notes\"]").fill(notes)

        modal.get_by_role("button", name="Create").click()
        modal.wait_for(state="hidden", timeout=10000)

    def search_enquiry_type(self, name: str) -> bool:
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

    def view_enquiry_type(self, name: str) -> bool:
        self.search_enquiry_type(name)
        row = self.page.locator("tr", has=self.page.get_by_text(name, exact=True))
        row.wait_for(state="visible", timeout=5000)

        row.get_by_title("view").click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)

        # Verify element is visible in the view dialog
        text_visible = modal.get_by_text(name).is_visible()
        modal.get_by_role("button", name="Back to List").click()
        modal.wait_for(state="hidden", timeout=5000)
        return text_visible

    def edit_enquiry_type(self, old_name: str, new_name: str) -> bool:
        self.search_enquiry_type(old_name)
        row = self.page.locator("tr", has=self.page.get_by_text(old_name, exact=True))
        row.wait_for(state="visible", timeout=5000)

        row.get_by_title("edit").click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)

        modal.locator("input[name=\"name\"]").fill(new_name)
        modal.get_by_role("button", name="Update").click()

        try:
            modal.wait_for(state="hidden", timeout=10000)
            return True
        except Exception:
            return False

    def delete_enquiry_type(self, name: str) -> bool:
        self.search_enquiry_type(name)
        row = self.page.locator("tr", has=self.page.get_by_text(name, exact=True))
        row.wait_for(state="visible", timeout=5000)

        row.get_by_title("delete").first.click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)

        modal.get_by_role("button", name="Delete Enquiry").click()

        toast = self.page.get_by_text("Deleted successfully.").first
        try:
            toast.wait_for(state="visible", timeout=5000)
            modal.wait_for(state="hidden", timeout=5000)
            return True
        except Exception:
            return False

    def retrieve_enquiry_type(self, name: str) -> bool:
        self.search_enquiry_type(name)
        row = self.page.locator("tr", has=self.page.get_by_text(name, exact=True))
        row.wait_for(state="visible", timeout=5000)

        row.get_by_title("delete").first.click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)

        modal.get_by_role("button", name="Retrieve Enquiry").click()

        toast = self.page.get_by_text("Retrieved successfully.").first
        try:
            toast.wait_for(state="visible", timeout=5000)
            modal.wait_for(state="hidden", timeout=5000)
            return True
        except Exception:
            return False
