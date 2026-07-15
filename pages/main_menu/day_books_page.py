from pages.common.base_page import BasePage
from utils.constants import DAY_BOOKS_URL

class DayBooksPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url = DAY_BOOKS_URL
