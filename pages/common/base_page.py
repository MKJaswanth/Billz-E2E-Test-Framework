import re

class BasePage:
    def __init__(self, page):
        self.page = page
        self.url = ""

    def navigate(self):
        if hasattr(self, 'url') and self.url:
            self.page.goto(self.url)
            self.page.wait_for_load_state("networkidle")

    def select_dropdown_option(self, input_name, option_text, click_index=0):
        """Centralized helper to interact with React-Select dropdowns.
        Locates the field by its bound form input name and selects the option.
        Falls back to DOM index if the input element is hidden or detached."""
        try:
            self.page.locator(f"input[name='{input_name}']").locator("xpath=..").locator(".react-select__input-container").click(timeout=3000)
        except Exception:
            self.page.locator(".react-select__input-container").nth(click_index).click()
        
        try:
            self.page.get_by_role("option", name=option_text, exact=False).first.click(timeout=3000)
        except Exception:
            self.page.locator(".react-select__option").filter(has_text=option_text).first.click()