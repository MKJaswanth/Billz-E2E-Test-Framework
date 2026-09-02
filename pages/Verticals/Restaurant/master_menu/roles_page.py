"""Restaurant adapter for the shared Roles page object."""
from __future__ import annotations

from playwright.sync_api import Page
from pages.master_menu.roles_page import RolesPage as BaseRolesPage
from utils.res_constants import RESTAURANT_BASE_URL


class RolesPage(BaseRolesPage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.roles_url = f"{RESTAURANT_BASE_URL}/roles"
