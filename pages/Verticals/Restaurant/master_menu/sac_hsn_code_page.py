"""Restaurant adapter for the shared SAC/HSN Code page object."""

from playwright.sync_api import Page

from pages.master_menu.sac_hsn_code_page import (
    SacHsnCodePage as SharedSacHsnCodePage,
)
from utils.res_constants import RESTAURANT_BASE_URL


class SacHsnCodePage(SharedSacHsnCodePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.sac_hsn_url = f"{RESTAURANT_BASE_URL}/gst-codes"
