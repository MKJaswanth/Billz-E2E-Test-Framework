"""Restaurant adapter for the shared Categories page object."""

from playwright.sync_api import Page

from pages.master_menu.categories_page import CategoriesPage
from utils.res_constants import RESTAURANT_BASE_URL


class FoodCategoriesPage(CategoriesPage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.categories_url = f"{RESTAURANT_BASE_URL}/categories"
