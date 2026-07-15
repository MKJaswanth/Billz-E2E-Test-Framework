from __future__ import annotations

from playwright.sync_api import Page
from utils.constants import DASHBOARD_URL


class DashboardPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.url = DASHBOARD_URL

    def navigate(self) -> None:
        self.page.goto(self.url)

    def is_dashboard_visible(self) -> bool:
        return self.page.get_by_role("heading", name="Dashboard").is_visible()
