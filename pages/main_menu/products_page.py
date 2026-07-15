from __future__ import annotations

from playwright.sync_api import Page
from utils.constants import PRODUCTS_URL
from pages.common.form_page import has_required_field_feedback, has_validation_feedback

class ProductsPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.products_url = PRODUCTS_URL

    def navigate(self) -> None:
        self.page.goto(self.products_url)

    def is_products_visible(self) -> bool:
        return self.page.get_by_role("button", name="Add Product").is_visible() or \
               self.page.get_by_role("textbox", name="Search...").is_visible()

    def _fill_product_form(
        self, modal, name: str, brand_name: str, category_name: str, hsn_code: str, unit_type: str,
        cost_price: str = "100", selling_price: str = "150", gst_percentage: str = "18%", low_stock: str = "5"
    ) -> None:
        modal.locator('input[name="name"]').fill(name)

        for field, option in (
            ("brand_id", brand_name),
            ("category_id", category_name),
        ):
            modal.locator(f"input[name='{field}']").locator("xpath=..").locator(
                ".react-select__input-container"
            ).click()
            self.page.get_by_role("option", name=option).click()

        modal.locator('input[name="cost_price"]').fill(cost_price)
        modal.locator('input[name="selling_price"]').fill(selling_price)

        for field, option in (
            ("gst_percentage", gst_percentage),
            ("gst_code_id", hsn_code),
            ("unit_type_id", unit_type),
        ):
            modal.locator(f"input[name='{field}']").locator("xpath=..").locator(
                ".react-select__input-container"
            ).click()
            self.page.get_by_role("option", name=option).click()

        modal.locator('input[name="low_stock"]').fill(low_stock)

    def add_product(self, name: str, brand_name: str, category_name: str, hsn_code: str, unit_type: str, cost_price: str = "100", selling_price: str = "150", gst_percentage: str = "18%") -> None:
        self.page.get_by_role("button", name="Add Product").click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=15000)

        self._fill_product_form(
            modal, name, brand_name, category_name, hsn_code, unit_type,
            cost_price, selling_price, gst_percentage
        )

        # 10. Create Product
        modal.get_by_role("button", name="Create Product").click()

        # Wait for operation successful toast and modal hidden
        toast = self.page.get_by_text("Operation successful").first
        toast.wait_for(state="visible", timeout=10000)
        modal.wait_for(state="hidden", timeout=10000)

    def validate_invalid_numeric_field(
        self, name: str, brand_name: str, category_name: str, hsn_code: str, unit_type: str, field: str, value: str
    ) -> bool:
        self.page.get_by_role("button", name="Add Product").click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=15000)
        values = {"cost_price": "100", "selling_price": "150", "low_stock": "5"}
        values[field] = value
        self._fill_product_form(
            modal, name, brand_name, category_name, hsn_code, unit_type,
            cost_price=values["cost_price"],
            selling_price=values["selling_price"],
            low_stock=values["low_stock"],
        )
        modal.get_by_role("button", name="Create Product").click()
        return has_validation_feedback(
            modal,
            r"must be.*(?:zero|0|positive|greater)",
            r"(?:negative|invalid).*(?:price|stock|value)",
            r"(?:price|stock).*(?:negative|invalid|positive)",
        )

    def validate_duplicate_product(
        self, name: str, brand_name: str, category_name: str, hsn_code: str, unit_type: str
    ) -> bool:
        self.page.get_by_role("button", name="Add Product").click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=15000)
        self._fill_product_form(
            modal, name, brand_name, category_name, hsn_code, unit_type
        )
        modal.get_by_role("button", name="Create Product").click()
        return has_validation_feedback(
            modal,
            r"product.*already",
            r"name.*already been taken",
            r"duplicate.*product",
        )

    def validate_required_fields(self) -> bool:
        self.page.get_by_role("button", name="Add Product").click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=15000)
        modal.get_by_role("button", name="Create Product").click()
        return has_required_field_feedback(modal)

    def search_product(self, name: str) -> bool:
        search_box = self.page.get_by_role("textbox", name="Search...")
        search_box.fill(name)
        search_box.press("Enter")
        self.page.wait_for_load_state("networkidle", timeout=5000)
        locator = self.page.get_by_text(name, exact=True).first
        try:
            locator.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False

    def view_product(self, name: str) -> bool:
        self.search_product(name)
        row = self.page.locator("tr", has=self.page.get_by_text(name, exact=True))
        row.wait_for(state="visible", timeout=5000)

        row.get_by_title("view").first.click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)

        try:
            modal.get_by_text(name, exact=True).first.wait_for(state="visible", timeout=5000)
            is_visible = True
        except Exception:
            is_visible = False

        modal.get_by_role("button", name="Back to List").click()
        modal.wait_for(state="hidden", timeout=5000)
        return is_visible

    def delete_product(self, name: str) -> bool:
        self.search_product(name)
        row = self.page.locator("tr", has=self.page.get_by_text(name, exact=True))
        row.wait_for(state="visible", timeout=5000)

        row.get_by_title("delete").first.click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)

        delete_btn = modal.get_by_role("button", name="Delete Product")
        try:
            delete_btn.wait_for(state="visible", timeout=3000)
            delete_btn.click()
        except Exception:

            close_btn = modal.locator(".btn-close")
            if close_btn.is_visible():
                close_btn.click()
            elif modal.get_by_role("button", name="Cancel").is_visible():
                modal.get_by_role("button", name="Cancel").click()
            return False

        toast = self.page.get_by_text("Deleted successfully.").first
        try:
            toast.wait_for(state="visible", timeout=5000)
            modal.wait_for(state="hidden", timeout=5000)
            return True
        except Exception:
            return False

    def edit_product(self, old_name: str, new_name: str) -> bool:
        self.search_product(old_name)
        row = self.page.locator("tr", has=self.page.get_by_text(old_name, exact=True))
        row.wait_for(state="visible", timeout=5000)

        row.get_by_title("edit").first.click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)

        modal.locator("input[name=\"name\"]").fill(new_name)
        modal.get_by_role("button", name="Update Product").click()

        try:
            modal.wait_for(state="hidden", timeout=10000)
            return True
        except Exception:
            return False

    def update_opening_stock(self, name: str, branch_name: str, quantity: str, cost_price: str) -> bool:
        self.search_product(name)
        row = self.page.locator("tr", has=self.page.get_by_text(name, exact=True))
        row.wait_for(state="visible", timeout=5000)

        row.get_by_title("Opening Stock Update").first.click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)

        # Select branch
        modal.locator("input[name='branch_id']").locator("xpath=..").locator(".react-select__input-container").click()
        self.page.get_by_role("option", name=branch_name).click()

        # Fill quantity and price
        modal.locator("input[name='lines.0.quantity']").fill(quantity)
        modal.locator("input[name='lines.0.cost_price']").fill(cost_price)

        modal.get_by_role("button", name="Save Opening Stock").click()

        try:
            toast = self.page.get_by_text("Opening stock updated").first
            toast.wait_for(state="visible", timeout=10000)
            modal.wait_for(state="hidden", timeout=10000)
            return True
        except Exception:
            return False

    def retrieve_product(self, name: str) -> bool:
        self.search_product(name)
        row = self.page.locator("tr", has=self.page.get_by_text(name, exact=True))
        row.wait_for(state="visible", timeout=5000)

        row.get_by_title("delete").first.click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)

        modal.get_by_role("button", name="Retrieve Product").click()

        toast = self.page.get_by_text("Retrieved successfully.").first
        try:
            toast.wait_for(state="visible", timeout=5000)
            modal.wait_for(state="hidden", timeout=5000)
            return True
        except Exception:
            return False
