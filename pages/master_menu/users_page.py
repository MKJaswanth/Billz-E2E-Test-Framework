from utils.constants import USERS_URL 

class UsersPage:
    def __init__(self, page):
        self.page = page
        self.users_url = USERS_URL
        
    def navigate(self):
        return self.page.goto(self.users_url)
    
    def is_user_visible(self):
        return self.page.get_by_role("button", name="Add User").is_visible()
    
    def search_user(self, user_name):
        search_box = self.page.get_by_role("textbox", name="Search users...")
        search_box.fill(user_name)
        search_box.press("Enter")
        
        user_locator = self.page.get_by_text(user_name, exact=True)
        try: 
            user_locator.wait_for(state="visible", timeout=1000)
            return True
        except Exception:
            return False
        
    def add_user(self, name, email, password, branch_name, role_name):
        self.page.get_by_role("button", name="Add User").click()
        
        self.page.locator("input[name=\"name\"]").fill(name)
        self.page.locator("input[name=\"email\"]").fill(email)
        self.page.locator("input[name=\"password\"]").fill(password)
        
        self.page.locator(".react-select__value-container.react-select__value-container--is-multi > .react-select__input-container").click()
        self.page.get_by_role("option", name=branch_name).click()
        
        self.page.locator("div:nth-child(6) > .mb-3 > .css-b62m3t-container > .react-select__control > .react-select__value-container > .react-select__input-container").click()
        self.page.get_by_role("option", name=role_name).click()
        
        self.page.get_by_role("button", name="Create").click()
        self.page.get_by_text("User created successfully").wait_for(state="visible", timeout=10000)
        
    def edit_user(self, old_name, new_name):
        self.search_user(old_name)
        
        user_row = self.page.locator("tr", has=self.page.get_by_text(old_name, exact=True))
        user_row.wait_for(state="visible", timeout=5000)
        
        user_row.get_by_title("edit").click()
        self.page.locator("input[name=\"name\"]").fill(new_name)
        self.page.get_by_role("button", name="Update").click()
        
        toast = self.page.get_by_text("User updated successfully")
        try:
            toast.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False
    
    def view_user(self, user_name):
        self.search_user(user_name)
        
        user_row = self.page.locator("tr", has=self.page.get_by_text(user_name, exact=True))
        user_row.wait_for(state="visible", timeout=5000)
        
        user_row.get_by_title("view").click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)
        
        try:
            modal.get_by_text(user_name, exact=True).first.wait_for(state="visible", timeout=10000)
            is_visible = True
        except Exception:
            is_visible = False
        
        self.page.get_by_role("button", name="Back to List").click()
        return is_visible

    def delete_user(self, user_name):
        self.search_user(user_name)
        
        user_row = self.page.locator("tr", has=self.page.get_by_text(user_name, exact=True))
        user_row.wait_for(state="visible", timeout=5000)
        
        user_row.get_by_title("delete").first.click()
        self.page.get_by_role("button", name="Delete User").click()
        
        toast = self.page.get_by_text("Deleted successfully.")
        try:
            toast.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False

    def retrieve_user(self, user_name):
        self.search_user(user_name)
        
        user_row = self.page.locator("tr", has=self.page.get_by_text(user_name, exact=True))
        user_row.wait_for(state="visible", timeout=5000)
        
        user_row.get_by_title("delete").first.click()
        self.page.get_by_role("button", name="Retrieve User").click()
        
        toast = self.page.get_by_text("Retrieved successfully.")
        try:
            toast.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False

    def validate_user_required_fields(self):
        self.page.get_by_role("button", name="Add User").click()
        self.page.get_by_role("button", name="Create").click()
        
        name_err = self.page.get_by_text("Name is required")
        email_err = self.page.get_by_text("Email is required")
        password_err = self.page.get_by_text("Password is required")
        
        try:
            name_err.wait_for(state="visible", timeout=5000)
            email_err.wait_for(state="visible", timeout=5000)
            password_err.wait_for(state="visible", timeout=5000)
            is_valid = True
        except Exception:
            is_valid = False
            
        self.navigate()
        return is_valid
