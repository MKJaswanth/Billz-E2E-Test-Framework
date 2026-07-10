from utils.constants import PRODUCT_ATTRIBUTES_URL

class ProductAttributesPage:
    def __init__(self, page):
        self.page = page
        self.product_attributes_url = PRODUCT_ATTRIBUTES_URL
        
    def navigate(self):
        return self.page.goto(self.product_attributes_url)
        
    def is_product_attributes_visible(self):
        return self.page.get_by_role("button", name="Add Product Unit Attribute").is_visible()
        
    def add_product_attribute(self, name, sort_order=None, unique=False, description=None):
        self.page.get_by_role("button", name="Add Product Unit Attribute").click()
        
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)
        
        modal.locator("input[name=\"name\"]").fill(name)
        
        if sort_order is not None:
            modal.locator("input[name=\"sort_order\"]").fill(str(sort_order))
            
        if unique:
            modal.locator("input[name=\"unique\"]").check()
        if description:
            modal.get_by_role("button", name="Add Description").click()
            modal.locator("textarea[name=\"notes\"]").fill(description)
            
        modal.get_by_role("button", name="Create").click()
        
    def search_product_attribute(self, name):
        search_box = self.page.get_by_role("textbox", name="Search...")
        search_box.fill(name)
        search_box.press("Enter")
        
        locator = self.page.get_by_text(name, exact=True).first
        try:
            locator.wait_for(state="visible", timeout=3000)
            return True
        except Exception:
            return False

    def view_product_attribute(self, name):
        self.search_product_attribute(name)
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
            
        modal.locator(".btn-close").click()
        return is_visible

    def edit_product_attribute(self, old_name, new_name):
        self.search_product_attribute(old_name)
        row = self.page.locator("tr", has=self.page.get_by_text(old_name, exact=True))
        row.wait_for(state="visible", timeout=5000)
        
        row.get_by_title("edit").click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)
        
        try:
            modal.locator(".spinner-border").wait_for(state="hidden", timeout=5000)
        except Exception:
            pass
            
        modal.locator("input[name=\"name\"]").fill(new_name)
        modal.get_by_role("button", name="Update").click()
        
        toast = self.page.get_by_text("successfully")
        try:
            toast.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False

    def delete_product_attribute(self, name):
        self.search_product_attribute(name)
        row = self.page.locator("tr", has=self.page.get_by_text(name, exact=True))
        row.wait_for(state="visible", timeout=5000)
        
        row.get_by_title("delete").first.click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)
        
        modal.get_by_role("button", name="Delete").first.click()
        
        toast = self.page.get_by_text("Deleted successfully.")
        try:
            toast.wait_for(state="visible", timeout=10000)
            return True
        except Exception:
            return False

    def retrieve_product_attribute(self, name):
        self.search_product_attribute(name)
        row = self.page.locator("tr", has=self.page.get_by_text(name, exact=True))
        row.wait_for(state="visible", timeout=5000)
        
        row.get_by_title("delete").first.click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)
        
        modal.get_by_role("button", name="Retrieve").first.click()
        
        toast = self.page.get_by_text("Retrieved successfully.")
        try:
            toast.wait_for(state="visible", timeout=10000)
            return True
        except Exception:
            return False

    def validate_required_fields(self):
        self.page.get_by_role("button", name="Add Product Unit Attribute").click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)
        
        modal.get_by_role("button", name="Create").click()
        
        error_locator = self.page.get_by_text("Name is required")
        try:
            error_locator.wait_for(state="visible", timeout=5000)
            is_valid = True
        except Exception:
            is_valid = False
            
        self.navigate()
        return is_valid
