from utils.constants import BRANDS_URL

class BrandPage:
    def __init__(self, page ):
        self.page = page
        self.brabd_url = BRANDS_URL

    def navigate(self):
        self.page.goto(self.brabd_url)

    def is_brands_visible(self):
        return self.page.get_by_role("button", name="Add Brand").is_visible()

    def search_brand(self, brand_name):
        search_input = self.page.get_by_role("textbox", name="Search...")
        search_input.fill(brand_name)
        search_input.press("Enter")
        
        brand_locator = self.page.get_by_text(brand_name, exact=True).first
        try:
            brand_locator.wait_for(state="visible", timeout=15000)
            return True
        except Exception:
            return False
        

    def add_brand(self, name, description):
        self.page.get_by_role("button", name="Add Brand").click()
        self.page.locator("input[name='name']").fill(name)
        self.page.locator("textarea[name=\"description\"]").fill(description)
        self.page.locator("button[type='submit']").click()
        self.page.get_by_text("Brand created successfully").wait_for(state="visible" , timeout=3000)

        return name

    def edit_brand(self, old_name, new_name):
        self.search_brand(old_name)
        category_row = self.page.locator("tr", has=self.page.get_by_text(old_name, exact=True))
        category_row.wait_for(state="visible", timeout=15000)
        
        category_row.get_by_title("edit").click()
        self.page.locator("input[name=\"name\"]").fill(new_name)
        self.page.get_by_role("button", name="Update").click()
        
        toast = self.page.get_by_text("Brand updated successfully")
        try:
            toast.wait_for(state="visible", timeout=15000)
            return True
        except Exception:
            return False  

    def view_brand(self , name):
        self.search_brand(name)
        category_row = self.page.locator("tr", has=self.page.get_by_text(name, exact=True))
        category_row.wait_for(state="visible", timeout=15000)
        
        category_row.get_by_title("view").click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=15000)
        name_locator = modal.get_by_text(name, exact=True).first
        try:
            name_locator.wait_for(state="visible", timeout=13000)
            is_name_visible = True
        except Exception:
            is_name_visible = False
            
    
        self.page.get_by_role("button", name="Back to List").click()
        return is_name_visible


    def delete_brand(self , brand_name):
        self.search_brand(brand_name)
        category_row = self.page.locator("tr", has=self.page.get_by_text(brand_name, exact=True))
        category_row.wait_for(state="visible", timeout=15000)
        
        category_row.get_by_title("delete").click()
        self.page.get_by_role("button", name="Delete Brand").click()
        toast = self.page.get_by_text("Deleted successfully.")
        try:
            toast.wait_for(state="visible", timeout=15000)
            return True
        except Exception:
            return False  

    def retrieve_brand(self , brand_name):
        self.search_brand(brand_name)
        brand_row = self.page.locator("tr", has=self.page.get_by_text(brand_name, exact=True))
        brand_row.wait_for(state="visible", timeout=15000)
        
        brand_row.get_by_title("delete").click()
        self.page.get_by_role("button", name="Delete Brand").click()
        brand_row.get_by_title("delete").click()
        self.page.get_by_role("button", name="Retrieve Brand").click()
        toast = self.page.get_by_text("Deleted successfully.")
        try:
            toast.wait_for(state="visible", timeout=15000)
            return True
        except Exception:
            return False  

    def validate_required_fields(self):
        self.page.get_by_role("button", name="Add Brand").click()
        self.page.get_by_role("button", name="Create").click()
        
        error_locator = self.page.get_by_text("Brand Name is required")
        try:
            error_locator.wait_for(state="visible", timeout=15000)
            is_valid = True
        except Exception:
            is_valid = False
            
        self.navigate()
        return is_valid




