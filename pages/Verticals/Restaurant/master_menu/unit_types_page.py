"""Restaurant adapter for the shared Unit Types page object."""

from playwright.sync_api import Page

from pages.master_menu.unit_types_page import UnitTypesPage as SharedUnitTypesPage
from utils.res_constants import RESTAURANT_BASE_URL


class UnitTypesPage(SharedUnitTypesPage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.unit_types_url = f"{RESTAURANT_BASE_URL}/unit-types"
