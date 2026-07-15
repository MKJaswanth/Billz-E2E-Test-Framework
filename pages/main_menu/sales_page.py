from __future__ import annotations

import re
from playwright.sync_api import Page
from utils.constants import SALES_URL

class SalesPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.url = SALES_URL

    def navigate(self) -> None:
        self.page.goto(self.url)

    def is_sales_visible(self) -> bool:
        try:
            self.page.get_by_role("textbox", name="Search...").wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False

    def _select_customer(self, customer_name: str) -> None:
        self.page.locator(".react-select__input-container").first.click()
        # Customer options render as "<name> - <extra info>"; substring match
        # avoids needing to know the exact trailing text.
        self.page.get_by_role("option", name=f"{customer_name} -").click()

    def _select_branch(self, branch_name: str) -> None:
        try:
            self.page.locator(
                ".col-md-4 > .mb-3 > .css-b62m3t-container > .react-select__control "
                "> .react-select__value-container > .react-select__input-container"
            ).first.click()
        except Exception:
            self.page.locator(".react-select__input-container").nth(1).click()

        try:
            self.page.get_by_role("option", name=branch_name).click(timeout=5000)
        except Exception:
            try:
                self.page.locator(".react-select__option").filter(has_text=branch_name).first.click(timeout=5000)
            except Exception:
                # Absolute fallback to div match if needed
                self.page.locator("div").filter(has_text=re.compile(rf"^{re.escape(branch_name)}$")).nth(2).click()

    def _select_address(self, address_text: str) -> None:
        """Select a specific address from the customer's saved addresses.
        The field is labelled "Billing Address" but the dropdown lists ALL
        of the customer's addresses (billing and delivery) by their full
        formatted text - pass the exact address text to pick a delivery one
        instead of whatever is selected by default."""
        try:
            self.page.locator("input[name='billing_address_id']").locator("xpath=..").locator(".react-select__input-container").click(timeout=3000)
        except Exception:
            self.page.locator(
                ".react-select__control > .react-select__value-container > .react-select__input-container"
            ).nth(3).click()
        try:
            self.page.get_by_role("option", name=address_text, exact=False).first.click(timeout=3000)
        except Exception:
            self.page.locator(".react-select__option").filter(has_text=address_text).first.click()

    def _select_product_in_row(self, row_idx: int, product_name: str) -> None:
        row_locator = self.page.locator(f"tr:nth-child({row_idx}) > td:nth-child(2)")
        try:
            row_locator.locator(".react-select__input-container").click()
        except Exception:
            self.page.locator(
                f"tr:nth-child({row_idx}) > td:nth-child(2) > .mb-3 > .css-b62m3t-container "
                f"> .react-select__control > .react-select__value-container > .react-select__input-container"
            ).click()
        self.page.get_by_role("option", name=product_name).click()

    def _select_payment_method(self, payment_method: str) -> None:
        """payment_method is either "Cash" or the exact name of a Bank
        Account (Master > Bank Accounts) - selecting a bank account here is
        what credits the paid_amount into that account's balance."""
        # 1. Wait for dynamic Sale type field to render after entering paid_amount
        self.page.get_by_text(re.compile(r"^Sale type \*")).wait_for(state="visible", timeout=5000)

        # 2. Select sale type: "Cash" or "Bank Account"
        target_sale_type = "Cash" if payment_method == "Cash" else "Bank Account"
        self.page.locator("input[name='sale_type']").locator("xpath=..").locator(".react-select__input-container").click()
        self.page.get_by_role("option", name=target_sale_type).click()

        # 3. If it's a bank payment, select the specific bank account
        if target_sale_type == "Bank Account":
            # Wait for dynamic Bank Account * field to render
            self.page.get_by_text(re.compile(r"^Bank Account \*")).wait_for(state="visible", timeout=5000)
            
            # Click bank_account_id input container
            self.page.locator("input[name='bank_account_id']").locator("xpath=..").locator(".react-select__input-container").click()
            
            # Wait for menu to appear
            try:
                self.page.locator(".react-select__menu").wait_for(state="visible", timeout=3000)
            except Exception:
                pass

            # Select the option (substring-safe)
            try:
                self.page.get_by_role("option", name=payment_method, exact=False).click(timeout=5000)
            except Exception:
                try:
                    self.page.locator(".react-select__option").filter(has_text=payment_method).first.click(timeout=5000)
                except Exception:
                    try:
                        self.page.locator("div[role='option']").filter(has_text=payment_method).first.click(timeout=5000)
                    except Exception:
                        self.page.get_by_role("option", name=payment_method).click()

    def add_sale(
        self, customer_name: str, branch_name: str, paid_amount: str, price: str,
        product_name: str | None = None, quantity: int | None = None, address_text: str | None = None, payment_method: str = "Cash",
        salesperson_name: str | None = None
    ) -> None:
        self.page.goto(f"{self.url}/add")
        self.page.wait_for_load_state("networkidle")

        self._select_customer(customer_name)
        self._select_branch(branch_name)

        if salesperson_name:
            try:
                self.page.locator("input[name='employee_id']").locator("xpath=..").locator(".react-select__input-container").click(timeout=3000)
            except Exception:
                self.page.locator("div:nth-child(3) > .mb-3 > .css-b62m3t-container > .react-select__control > .react-select__value-container > .react-select__input-container").click()
            self.page.get_by_role("option", name=salesperson_name).click()
            self.page.wait_for_timeout(500)

        if address_text:
            self._select_address(address_text)

        if product_name:
            self._select_product_in_row(1, product_name)
        if quantity is not None:
            self.page.locator("tr:nth-child(1)").get_by_placeholder("Quantity").fill(str(quantity))

        self.page.get_by_placeholder("Price").first.fill(str(price))
        self.page.locator('input[name="paid_amount"]').fill(str(paid_amount))

        # Only select payment method if paid_amount > 0
        if float(paid_amount) > 0:
            self._select_payment_method(payment_method)

        self.page.get_by_role("button", name="Create").click()
        # A confirmation dialog sometimes follows the first Create click.
        try:
            self.page.get_by_role("button", name="Create").click(timeout=3000)
        except Exception:
            pass

        toast = self.page.get_by_text(re.compile(r"Sale created successfully", re.IGNORECASE))
        toast.wait_for(state="visible", timeout=10000)
        
        # Click Sales List or navigate
        try:
            self.page.get_by_role("button", name="Sales List").click(timeout=3000)
        except Exception:
            self.navigate()
        self.page.wait_for_load_state("networkidle")

    def search_sale(self, query: str) -> bool:
        search_box = self.page.get_by_role("textbox", name="Search...")
        search_box.fill(query)
        search_box.press("Enter")
        self.page.wait_for_load_state("networkidle", timeout=5000)
        try:
            self.page.locator("table tbody tr").filter(has_text=query).first.wait_for(
                state="visible", timeout=5000
            )
            return True
        except Exception:
            return False

    def filter_sales(self, salesperson_name: str | None = None, branch_name: str | None = None) -> None:
        self.navigate()
        self.page.wait_for_load_state("networkidle")

        try:
            expand_btn = self.page.get_by_role("button", name="Expand filters")
            if expand_btn.is_visible():
                expand_btn.click()
        except Exception:
            pass

        if salesperson_name:
            try:
                self.page.locator("input[name='employee_id']").locator("xpath=..").locator(".react-select__input-container").click(timeout=3000)
            except Exception:
                try:
                    self.page.locator("input[name='user_id']").locator("xpath=..").locator(".react-select__input-container").click(timeout=3000)
                except Exception:
                    try:
                        self.page.locator("div").filter(has_text=re.compile(r"^Select\.\.\.$")).nth(2).click()
                    except Exception:
                        self.page.locator(".react-select__input-container").last.click()
            self.page.get_by_role("option", name=salesperson_name).click()
            self.page.wait_for_timeout(500)

        if branch_name:
            try:
                self.page.locator("input[name='branch_id']").locator("xpath=..").locator(".react-select__input-container").click(timeout=3000)
            except Exception:
                self.page.locator(".react-select__input-container").first.click()
            self.page.get_by_role("option", name=branch_name).click()
            self.page.wait_for_timeout(500)

        self.page.get_by_role("button", name="Filter", exact=True).click()
        self.page.wait_for_load_state("networkidle")

    def view_sale(self, query: str, branch_name: str, salesperson_name: str) -> bool:
        self.search_sale(query)
        row = self.page.locator("table tbody tr").filter(has_text=query).first
        row.click()
        row.get_by_title("view").first.click()

        dialog = self.page.get_by_role("dialog")
        dialog.wait_for(state="visible", timeout=5000)

        # Verify details
        dialog.get_by_text(query).first.wait_for(state="visible", timeout=5000)
        dialog.get_by_text(branch_name).first.wait_for(state="visible", timeout=5000)
        dialog.get_by_text(salesperson_name).first.wait_for(state="visible", timeout=5000)

        # Close dialog
        try:
            self.page.locator(".btn-close").click()
        except Exception:
            dialog.get_by_role("button").filter(has_text=re.compile(r"^$")).first.click()
        dialog.wait_for(state="hidden", timeout=5000)
        return True

    def edit_sale(self, query: str, new_quantity: str | int) -> None:
        self.search_sale(query)
        row = self.page.locator("table tbody tr").filter(has_text=query).first
        row.get_by_title("Edit").first.click()

        # Update Quantity
        qty_input = self.page.get_by_placeholder("Quantity").first
        qty_input.click()
        qty_input.fill(str(new_quantity))

        # Click Update
        self.page.get_by_role("button", name="Update").click()
        
        toast = self.page.get_by_text("Sale updated successfully.")
        toast.wait_for(state="visible", timeout=10000)
        
        # Click Sales List or navigate
        try:
            self.page.get_by_role("button", name="Sales List").click(timeout=3000)
        except Exception:
            self.navigate()
        self.page.wait_for_load_state("networkidle")

    def initiate_sale_return(self, query: str) -> None:
        self.search_sale(query)
        row = self.page.locator("table tbody tr").filter(has_text=query).first
        row.get_by_title("Sale Return").first.click()
        self.page.wait_for_load_state("networkidle")

    def download_invoice(self, query: str) -> str | None:
        self.search_sale(query)
        row = self.page.locator("table tbody tr").filter(has_text=query).first
        
        with self.page.expect_download() as download_info:
            row.get_by_title("Download").first.click()
        download = download_info.value
        return download.path()
