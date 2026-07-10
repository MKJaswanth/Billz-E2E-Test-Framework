from utils.constants import BANK_ACCOUNTS_URL

class BankAccountPage:
    def __init__(self, page):
        self.page = page 
        self.bank_account_url = BANK_ACCOUNTS_URL

    def navigate(self):
        return self.page.goto(self.bank_account_url)

    def is_bank_account_visible(self):
        return self.page.get_by_role("button", name="Add Bank Account").is_visible()

    def add_bank_account(self, bank_name, branch, account_number, ifsc_code):
        self.page.get_by_role("button", name="Add Bank Account").click()
        
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)
        
        modal.locator("input[name=\"bank_name\"]").fill(bank_name)
        modal.locator("input[name=\"branch\"]").fill(branch)
        modal.locator("input[name=\"account_number\"]").fill(account_number)
        modal.locator("input[name=\"ifsc_code\"]").fill(ifsc_code)
        
        modal.get_by_role("button", name="Create").click()

    def search_bank_account(self, bank_name):
        search_box = self.page.get_by_role("textbox", name="Search...")
        search_box.fill(bank_name)
        search_box.press("Enter")
        
        locator = self.page.get_by_text(bank_name, exact=True).first
        try:
            locator.wait_for(state="visible", timeout=3000)
            return True
        except Exception:
            return False

    def view_bank_account(self, bank_name):
        self.search_bank_account(bank_name)
        row = self.page.locator("tr", has=self.page.get_by_text(bank_name, exact=True))
        row.wait_for(state="visible", timeout=5000)
        
        row.get_by_title("view").click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)
        
        try:
            modal.get_by_text(bank_name, exact=True).first.wait_for(state="visible", timeout=5000)
            is_visible = True
        except Exception:
            is_visible = False
            
        close_btn = modal.locator(".btn-close")
        if close_btn.count() > 0:
            close_btn.click()
        else:
            modal.get_by_role("button").filter(has_text="").first.click()
            
        return is_visible

    def edit_bank_account(self, old_name, new_name):
        self.search_bank_account(old_name)
        row = self.page.locator("tr", has=self.page.get_by_text(old_name, exact=True))
        row.wait_for(state="visible", timeout=5000)
        
        row.get_by_title("edit").click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)
        
        modal.locator("input[name=\"bank_name\"]").fill(new_name)
        modal.get_by_role("button", name="Update").click()
        
        try:
            modal.wait_for(state="hidden", timeout=5000)
            return True
        except Exception:
            try:
                self.page.get_by_text("updated").wait_for(state="visible", timeout=2000)
                return True
            except Exception:
                return False

    def delete_bank_account(self, bank_name):
        self.search_bank_account(bank_name)
        row = self.page.locator("tr", has=self.page.get_by_text(bank_name, exact=True))
        row.wait_for(state="visible", timeout=5000)
        
        row.get_by_title("delete").first.click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)
        
        modal.get_by_role("button", name="Delete Account").click()
        
        toast = self.page.get_by_text("Deleted successfully.")
        try:
            toast.wait_for(state="visible", timeout=10000)
            return True
        except Exception:
            return False

    def retrieve_bank_account(self, bank_name):
        self.search_bank_account(bank_name)
        row = self.page.locator("tr", has=self.page.get_by_text(bank_name, exact=True))
        row.wait_for(state="visible", timeout=5000)
        
        row.get_by_title("delete").first.click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)
        
        modal.get_by_role("button", name="Retrieve Account").click()
        
        toast = self.page.get_by_text("Retrieved successfully.")
        try:
            toast.wait_for(state="visible", timeout=10000)
            return True
        except Exception:
            return False

    def validate_required_fields(self):
        self.page.get_by_role("button", name="Add Bank Account").click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)
        
        modal.get_by_role("button", name="Create").click()
        
        error_locator = self.page.get_by_text("Bank Name is required")
        try:
            error_locator.wait_for(state="visible", timeout=5000)
            is_valid = True
        except Exception:
            is_valid = False
            
        self.navigate()
        return is_valid