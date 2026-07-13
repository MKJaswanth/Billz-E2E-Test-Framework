import re

from utils.constants import SALES_URL


class SalesPage:
    def __init__(self, page):
        self.page = page
        self.url = SALES_URL

    def navigate(self):
        return self.page.goto(self.url)

    def is_sales_visible(self):
        try:
            self.page.get_by_role("textbox", name="Search...").wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False

    def _select_customer(self, customer_name):
        self.page.locator(".react-select__input-container").first.click()
        # Customer options render as "<name> - <extra info>"; substring match
        # avoids needing to know the exact trailing text.
        self.page.get_by_role("option", name=f"{customer_name} -").click()

    def _select_branch(self, branch_name):
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

    def _select_address(self, address_text):
        """Select a specific address from the customer's saved addresses.
        The field is labelled "Billing Address" but the dropdown lists ALL
        of the customer's addresses (billing and delivery) by their full
        formatted text - pass the exact address text to pick a delivery one
        instead of whatever is selected by default."""
        self.page.locator(
            ".react-select__control.react-select__control--is-focused "
            "> .react-select__value-container > .react-select__input-container"
        ).click()
        self.page.get_by_role("option", name=address_text).click()

    def _select_product_in_row(self, row_idx, product_name):
        row_locator = self.page.locator(f"tr:nth-child({row_idx}) > td:nth-child(2)")
        try:
            row_locator.locator(".react-select__input-container").click()
        except Exception:
            self.page.locator(
                f"tr:nth-child({row_idx}) > td:nth-child(2) > .mb-3 > .css-b62m3t-container "
                f"> .react-select__control > .react-select__value-container > .react-select__input-container"
            ).click()
        self.page.get_by_role("option", name=product_name).click()

    def _select_payment_method(self, payment_method):
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
        self, customer_name, branch_name, paid_amount, price,
        product_name=None, quantity=None, address_text=None, payment_method="Cash",
    ):
        self.page.goto(f"{self.url}/add")
        self.page.wait_for_load_state("networkidle")

        self._select_customer(customer_name)
        self._select_branch(branch_name)

        if address_text:
            self._select_address(address_text)

        if product_name:
            self._select_product_in_row(1, product_name)
        if quantity is not None:
            self.page.locator("tr:nth-child(1)").get_by_placeholder("Quantity").fill(str(quantity))

        self.page.get_by_placeholder("Price").first.fill(str(price))
        self.page.locator('input[name="paid_amount"]').fill(str(paid_amount))

        self._select_payment_method(payment_method)

        self.page.get_by_role("button", name="Create").click()
        # A confirmation dialog sometimes follows the first Create click.
        try:
            self.page.get_by_role("button", name="Create").click(timeout=3000)
        except Exception:
            pass

        toast = self.page.get_by_text(re.compile(r"Sale (created|added) successfully", re.IGNORECASE))
        try:
            toast.wait_for(state="visible", timeout=10000)
        except Exception:
            pass
        self.page.wait_for_load_state("networkidle")
