from __future__ import annotations

import re
from playwright.sync_api import Page
from utils.constants import PURCHASES_URL

class PurchasesPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.url = PURCHASES_URL

    def navigate(self) -> None:
        self.page.goto(self.url)

    def is_purchases_visible(self) -> bool:
        try:
            self.page.get_by_placeholder("Search Purchases...").wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False

    def add_purchase(self, supplier: str, branch: str, reference_no: str, paid_amount: str, purchase_type: str, bank_account: str | None = None, products_data: list[dict[str, str | int]] | None = None) -> None:
        self.page.goto(f"{self.url}/add")
        self.page.wait_for_load_state("networkidle")

        # 1. Select Supplier
        self.page.locator("input[name='supplier_id']").locator("xpath=..").locator(".react-select__input-container").click()
        self.page.get_by_role("option", name=supplier).click()

        # 2. Select Branch
        self.page.locator("input[name='branch_id']").locator("xpath=..").locator(".react-select__input-container").click()
        self.page.get_by_role("option", name=branch).click()

        # 3. Fill Reference Number
        if reference_no:
            self.page.locator("input[name='reference_no']").fill(reference_no)

        # 4. Fill Paid Amount
        self.page.locator("input[name='paid_amount']").fill(str(paid_amount))
        self.page.wait_for_timeout(500)

        # 5. Select Purchase Type (Cash / Bank Account) if paid_amount > 0
        if float(paid_amount) > 0:
            self.page.locator("input[name='purchase_type']").locator("xpath=..").locator(".react-select__input-container").click()
            self.page.get_by_role("option", name=purchase_type).click()
            self.page.wait_for_timeout(500)

            # 6. If Bank Account, select bank
            if purchase_type == "Bank Account" and bank_account:
                self.page.locator("input[name='bank_account_id']").locator("xpath=..").locator(".react-select__input-container").click()
                self.page.get_by_role("option", name=bank_account).click()

        # 7. Add Product Lines
        # products_data is list of dicts: [{"product": name, "quantity": qty, "price": val}]
        if products_data:
            for i, item in enumerate(products_data):
                if i > 0:
                    self.page.get_by_role("button", name="+ Add Item").click()
                
                # Select product
                self.page.locator(f"input[name='items.{i}.product_selector']").locator("xpath=..").locator(".react-select__input-container").click()
                self.page.get_by_role("option", name=item["product"]).click()

                # Fill Quantity
                self.page.locator(f"input[name='items.{i}.quantity']").fill(str(item["quantity"]))

                # Fill Price/Rate if provided
                if "price" in item:
                    self.page.locator(f"input[name='items.{i}.purchase_price']").fill(str(item["price"]))

        # Click Create
        self.page.get_by_role("button", name="Create", exact=True).click()
        self.page.wait_for_timeout(1000)

        # A confirmation dialog/modal sometimes follows the first Create click (similar to Sales)
        try:
            confirm_btn = self.page.locator("div.modal-footer button, div[role='dialog'] button").filter(has_text=re.compile(r"^Create$", re.IGNORECASE))
            if confirm_btn.count() > 0:
                confirm_btn.first.click()
        except Exception:
            pass

        # Wait for toast
        toast = self.page.get_by_text("Purchase created successfully.")
        toast.wait_for(state="visible", timeout=10000)
        try:
            toast.wait_for(state="hidden", timeout=5000)
        except Exception:
            pass
        self.navigate()
        self.page.wait_for_load_state("networkidle")

    def search_purchase(self, reference_no: str) -> bool:
        search_box = self.page.get_by_placeholder("Search Purchases...")
        search_box.fill(reference_no)
        search_box.press("Enter")
        self.page.wait_for_load_state("networkidle", timeout=5000)
        try:
            self.page.locator("table tbody tr").filter(has_text=reference_no).first.wait_for(
                state="visible", timeout=5000
            )
            return True
        except Exception:
            return False

    def initiate_return(self, reference_no: str) -> None:
        self.search_purchase(reference_no)
        row = self.page.locator("table tbody tr").filter(has_text=reference_no).first
        row.get_by_title("purchase return").click()
        self.page.wait_for_load_state("networkidle")
