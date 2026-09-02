"""Restaurant adapter for the shared Cities page object."""

from playwright.sync_api import Page

from pages.master_menu.cities_page import CitiesPage as SharedCitiesPage
from utils.res_constants import RESTAURANT_BASE_URL


class CitiesPage(SharedCitiesPage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.city_url = f"{RESTAURANT_BASE_URL}/cities"
