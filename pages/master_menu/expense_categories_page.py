from __future__ import annotations

from playwright.sync_api import Page

from utils.constants import EXPENSE_CATEGORIES_URL
from pages.common.form_page import has_validation_feedback

class ExpenseCategoriesPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.expense_categories_url = EXPENSE_CATEGORIES_URL

    def navigate(self) -> None:
        self.page.goto(self.expense_categories_url)

    def is_expense_categories_visible(self) -> bool:
        return self.page.get_by_role("button", name="Add Expense Category").is_visible()

    def add_expense_category(self, name: str, description: str | None = None) -> None:
        self.page.get_by_role("button", name="Add Expense Category").click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)

        modal.locator("input[name=\"name\"]").fill(name)

        if description:
            modal.locator("textarea[name=\"description\"]").fill(description)

        modal.get_by_role("button", name="Create").click()

        self.page.get_by_text("Expense category created").first.wait_for(state="visible", timeout=10000)
        modal.wait_for(state="hidden", timeout=10000)

    def search_expense_category(self, name: str) -> bool:
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

    def edit_expense_category(self, old_name: str, new_name: str) -> bool:
        self.search_expense_category(old_name)
        row = self.page.locator("tr", has=self.page.get_by_text(old_name, exact=True))
        row.wait_for(state="visible", timeout=5000)

        row.get_by_title("edit").click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)

        modal.locator("input[name=\"name\"]").fill(new_name)
        modal.get_by_role("button", name="Update").click()

        toast = self.page.get_by_text("Expense category updated").first
        try:
            toast.wait_for(state="visible", timeout=5000)
            modal.wait_for(state="hidden", timeout=5000)
            return True
        except Exception:
            return False

    def delete_expense_category(self, name: str) -> bool:
        self.search_expense_category(name)
        row = self.page.locator("tr", has=self.page.get_by_text(name, exact=True))
        row.wait_for(state="visible", timeout=5000)

        row.get_by_title("delete").first.click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)

        modal.get_by_role("button", name="Delete Category").click()

        toast = self.page.get_by_text("Deleted successfully.").first
        try:
            toast.wait_for(state="visible", timeout=5000)
            modal.wait_for(state="hidden", timeout=5000)
            return True
        except Exception:
            return False

    def retrieve_expense_category(self, name: str) -> bool:
        self.search_expense_category(name)
        row = self.page.locator("tr", has=self.page.get_by_text(name, exact=True))
        row.wait_for(state="visible", timeout=5000)

        row.get_by_title("delete").first.click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)

        modal.get_by_role("button", name="Retrieve Category").click()

        toast = self.page.get_by_text("Retrieved successfully.").first
        try:
            toast.wait_for(state="visible", timeout=5000)
            modal.wait_for(state="hidden", timeout=5000)
            return True
        except Exception:
            return False

    def validate_duplicate_category(self, name: str) -> bool:
        self.page.get_by_role("button", name="Add Expense Category").click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)
        modal.locator('input[name="name"]').fill(name)
        modal.get_by_role("button", name="Create").click()
        return has_validation_feedback(
            self.page,
            r"already been taken",
            r"already exists",
            r"duplicate",
        )
