from utils.constants import CATEGORIES_URL

class CategoriesPage:
    def __init__(self, page):
        self.page = page
        self.categories_url = CATEGORIES_URL
        
    def navigate(self):
        return self.page.goto(self.categories_url)
        
    def is_categories_visible(self):
        return self.page.get_by_role("button", name="Add Category").is_visible()
        
    def add_category(self, name, sort_order=None, description=None):
        self.page.get_by_role("button", name="Add Category").click()
        self.page.locator("input[name=\"name\"]").fill(name)
        if sort_order:
            self.page.locator("input[name=\"sort_order\"]").fill(str(sort_order))
        if description:
            self.page.locator("textarea[name=\"description\"]").fill(description)
        self.page.get_by_role("button", name="Create").click()
        
    def search_category(self, category_name):
        search_box = self.page.get_by_role("textbox", name="Search...")
        search_box.fill(category_name)
        search_box.press("Enter")
        
        category_locator = self.page.get_by_text(category_name, exact=True).first
        try:
            category_locator.wait_for(state="visible", timeout=3000)
            return True
        except Exception:
            return False

    def view_category(self, category_name):
        self.search_category(category_name)
        category_row = self.page.locator("tr", has=self.page.get_by_text(category_name, exact=True))
        category_row.wait_for(state="visible", timeout=5000)
        
        category_row.get_by_title("view").click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)
        
        try:
            modal.get_by_text(category_name, exact=True).first.wait_for(state="visible", timeout=10000)
            is_visible = True
        except Exception:
            is_visible = False
            
        self.page.get_by_role("button", name="Back to List").click()
        return is_visible

    def edit_category(self, old_name, new_name):
        self.search_category(old_name)
        category_row = self.page.locator("tr", has=self.page.get_by_text(old_name, exact=True))
        category_row.wait_for(state="visible", timeout=5000)
        
        category_row.get_by_title("edit").click()
        self.page.locator("input[name=\"name\"]").fill(new_name)
        self.page.get_by_role("button", name="Update").click()
        
        toast = self.page.get_by_text("Category updated successfully")
        try:
            toast.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False

    def delete_category(self, category_name):
        self.search_category(category_name)
        category_row = self.page.locator("tr", has=self.page.get_by_text(category_name, exact=True))
        category_row.wait_for(state="visible", timeout=5000)
        
        category_row.get_by_title("delete").first.click()
        self.page.get_by_role("button", name="Delete Category").click()
        
        toast = self.page.get_by_text("Deleted successfully.")
        try:
            toast.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False

    def retrieve_category(self, category_name):
        self.search_category(category_name)
        category_row = self.page.locator("tr", has=self.page.get_by_text(category_name, exact=True))
        category_row.wait_for(state="visible", timeout=5000)
        
        category_row.get_by_title("delete").first.click()
        self.page.get_by_role("button", name="Retrieve Category").click()
        
        toast = self.page.get_by_text("Retrieved successfully.")
        try:
            toast.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False

    def validate_required_fields(self):
        self.page.get_by_role("button", name="Add Category").click()
        self.page.get_by_role("button", name="Create").click()
        
        error_locator = self.page.get_by_text("Category Name is required")
        try:
            error_locator.wait_for(state="visible", timeout=5000)
            is_valid = True
        except Exception:
            is_valid = False
            
        self.navigate()
        return is_valid

