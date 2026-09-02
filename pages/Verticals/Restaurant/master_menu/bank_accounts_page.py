"""Restaurant adapter for the shared Bank Accounts page object."""

from playwright.sync_api import Page

from pages.master_menu.bank_accounts_page import BankAccountPage
from utils.res_constants import RESTAURANT_BASE_URL


class BankAccountsPage(BankAccountPage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.bank_account_url = f"{RESTAURANT_BASE_URL}/bank-accounts"
