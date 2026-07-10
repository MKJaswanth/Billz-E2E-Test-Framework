import re
from utils.constants import ACCOUNT_GROUPS_URL

class AccountGroupsPage:
    def __init__(self, page):
        self.page = page
        self.account_groups_url = ACCOUNT_GROUPS_URL

    def navigate(self):
        self.page.goto(self.account_groups_url)
        try:
            self.page.get_by_role("button", name="Table").first.click(timeout=2000)
        except Exception:
            try:
                self.page.get_by_text("Table", exact=True).first.click(timeout=2000)
            except Exception:
                pass

    def is_account_group_visible(self):
        return self.page.get_by_role("button", name="Add Account Group").is_visible()

    def add_account_group(self, name, parent_group="Current Assets"):
        self.page.get_by_role("button", name="Add Account Group").click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)

        modal.get_by_role("textbox", name="Enter Account group name").fill(name)
        modal.locator(".react-select__input-container").first.click()
        self.page.get_by_role("option", name=parent_group).click()
        modal.get_by_role("button", name="Create Account Group").click()

        self.page.get_by_text("Account group created").first.wait_for(state="visible", timeout=10000)
        modal.wait_for(state="hidden", timeout=10000)

    def search_account_group(self, name):
        try:
            self.page.get_by_role("button", name="Table").first.click(timeout=2000)
        except Exception:
            pass

        search_box = self.page.get_by_role("textbox", name="Search...")
        search_box.fill(name)
        search_box.press("Enter")

        locator = self.page.get_by_text(name, exact=True).first
        try:
            locator.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False

    def view_account_group(self, name):
        self.search_account_group(name)
        row = self.page.locator("tr", has=self.page.get_by_text(name, exact=True))
        row.wait_for(state="visible", timeout=5000)

        row.get_by_title("view").click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)

        try:
            modal.get_by_text(name, exact=True).first.wait_for(state="visible", timeout=5000)
            is_visible = True
        except Exception:
            is_visible = False

        close_btn = modal.get_by_role("button").filter(has_text=re.compile(r"^$")).first
        if close_btn.is_visible():
            close_btn.click()
        return is_visible

    def edit_account_group(self, old_name, new_name):
        self.search_account_group(old_name)
        row = self.page.locator("tr", has=self.page.get_by_text(old_name, exact=True))
        row.wait_for(state="visible", timeout=5000)

        row.get_by_title("edit").click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)

        modal.get_by_role("textbox", name="Enter Account group name").fill(new_name)
        modal.get_by_role("button", name="Update Account Group").click()

        toast = self.page.get_by_text("Account Group updated").first
        try:
            toast.wait_for(state="visible", timeout=5000)
            modal.wait_for(state="hidden", timeout=5000)
            return True
        except Exception:
            return False

    def delete_account_group(self, name):
        self.search_account_group(name)
        row = self.page.locator("tr", has=self.page.get_by_text(name, exact=True))
        row.wait_for(state="visible", timeout=5000)

        row.get_by_title("delete").first.click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)

        modal.get_by_role("button", name="Delete").click()

        toast = self.page.get_by_text("Deleted successfully.").first
        try:
            toast.wait_for(state="visible", timeout=5000)
            modal.wait_for(state="hidden", timeout=5000)
            return True
        except Exception:
            return False

    def retrieve_account_group(self, name):
        self.search_account_group(name)
        row = self.page.locator("tr", has=self.page.get_by_text(name, exact=True))
        row.wait_for(state="visible", timeout=5000)

        row.get_by_title("delete").first.click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)

        modal.get_by_role("button", name="Retrieve").click()

        toast = self.page.get_by_text("Retrieved successfully.").first
        try:
            toast.wait_for(state="visible", timeout=5000)
            modal.wait_for(state="hidden", timeout=5000)
            return True
        except Exception:
            return False

    def validate_required_fields(self):
        self.page.get_by_role("button", name="Add Account Group").click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)

        modal.get_by_role("button", name="Create Account Group").click()
        name_err = self.page.get_by_text("Name is required")

        try:
            name_err.wait_for(state="visible", timeout=5000)
            is_valid = True
        except Exception:
            is_valid = False

        self.navigate()
        return is_valid
