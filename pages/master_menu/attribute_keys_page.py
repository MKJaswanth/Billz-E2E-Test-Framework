from utils.constants import ATTRIBUTE_KEYS_URL

class AttributeKeysPage:
    def __init__(self, page):
        self.page = page
        self.attribute_keys_url = ATTRIBUTE_KEYS_URL
        
    def navigate(self):
        return self.page.goto(self.attribute_keys_url)
        
    def is_attribute_keys_visible(self):
        return self.page.get_by_role("button", name="Add Attribute Keys").is_visible()
        
    def add_attribute_key(self, name, sort_order=None, description=None):
        self.page.get_by_role("button", name="Add Attribute Keys").click()
        self.page.locator("input[name=\"name\"]").fill(name)
        if sort_order:
            self.page.locator("input[name=\"sort_order\"]").fill(str(sort_order))
        if description:
            self.page.get_by_role("button", name="Add Description").click()
            self.page.locator("textarea[name=\"description\"]").fill(description)
        self.page.get_by_role("button", name="Create").click()
        
    def search_attribute_key(self, name):
        search_box = self.page.get_by_role("textbox", name="Search...")
        search_box.fill(name)
        search_box.press("Enter")
        
        locator = self.page.get_by_text(name, exact=True).first
        try:
            locator.wait_for(state="visible", timeout=3000)
            return True
        except Exception:
            return False

    def view_attribute_key(self, name):
        self.search_attribute_key(name)
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
            
        self.page.get_by_role("button", name="Back to List").click()
        return is_visible

    def edit_attribute_key(self, old_name, new_name):
        self.search_attribute_key(old_name)
        row = self.page.locator("tr", has=self.page.get_by_text(old_name, exact=True))
        row.wait_for(state="visible", timeout=5000)
        
        row.get_by_title("edit").click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)
        
        self.page.locator("input[name=\"name\"]").fill(new_name)
        self.page.get_by_role("button", name="Update").click()
        
        toast = self.page.get_by_text("Attribute key updated")
        try:
            toast.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False

    def delete_attribute_key(self, name):
        self.search_attribute_key(name)
        row = self.page.locator("tr", has=self.page.get_by_text(name, exact=True))
        row.wait_for(state="visible", timeout=5000)
        
        row.get_by_title("delete").first.click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)
        
        modal.get_by_role("button", name="Delete Attribute Key").click()
        
        toast = self.page.get_by_text("Deleted successfully.")
        try:
            toast.wait_for(state="visible", timeout=10000)
            return True
        except Exception:
            return False

    def retrieve_attribute_key(self, name):
        self.search_attribute_key(name)
        row = self.page.locator("tr", has=self.page.get_by_text(name, exact=True))
        row.wait_for(state="visible", timeout=5000)
        
        row.get_by_title("delete").first.click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)
        
        modal.get_by_role("button", name="Retrieve Attribute Key").click()
        
        toast = self.page.get_by_text("Retrieved successfully.")
        try:
            toast.wait_for(state="visible", timeout=10000)
            return True
        except Exception:
            return False

    def validate_required_fields(self):
        self.page.get_by_role("button", name="Add Attribute Keys").click()
        self.page.get_by_role("button", name="Create").click()
        
        error_locator = self.page.get_by_text("Name is required")
        try:
            error_locator.wait_for(state="visible", timeout=5000)
            is_valid = True
        except Exception:
            is_valid = False
            
        self.navigate()
        return is_valid
