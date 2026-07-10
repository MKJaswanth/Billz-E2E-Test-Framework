from playwright.sync_api import expect
from utils.constants import BASE_URL
import re 
class LoginPage:  
        
    def __init__(self, page):
        self.page = page
        self.username_input = page.locator('input[name="email"]')
        self.password_input = page.locator('input[name="password"]')
        self.login_button = page.locator('button[type="submit"]')
    def navigate(self):
        self.page.goto(BASE_URL)  

    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        
    def verify_invalid_credentials_message(self):
        expect(self.page.locator('div.alert-danger')).to_be_visible()
    
    def toggle_password_visibility(self):
        self.page.get_by_role("button").filter(has_text=re.compile(r"^$")).click()

        
    