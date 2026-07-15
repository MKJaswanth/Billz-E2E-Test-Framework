from __future__ import annotations

from playwright.sync_api import Page
from utils.constants import SUPPLIERS_URL
from pages.common.form_page import has_required_field_feedback, has_validation_feedback

class SuppliersPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.url = SUPPLIERS_URL

    def navigate(self) -> None:
        self.page.goto(self.url)

    def is_suppliers_visible(self) -> bool:
        return self.page.get_by_role("button", name="Add Supplier").is_visible()

    def _fill_supplier_form(
        self, name: str, contact_person: str, email: str, phone: str, gst_number: str,
        state_name: str, city_name: str, postal_code: str, address: str, notes: str | None = None
    ) -> None:
        self.page.locator('input[name="name"]').fill(name)
        self.page.locator('input[name="contact_person"]').fill(contact_person)
        self.page.locator('input[name="email"]').fill(email)
        self.page.get_by_role("textbox", name="Enter 10 digit phone number").fill(phone)
        self.page.get_by_role("textbox", name="Enter 15-character GST number").fill(gst_number)

        state_select = self.page.locator("input[name='state_id']").locator(
            "xpath=.."
        ).locator(".react-select__input-container")
        state_select.wait_for(state="visible", timeout=5000)
        state_select.click()
        self.page.get_by_role("option", name=state_name).click()

        city_select = self.page.locator("input[name='city_id']").locator(
            "xpath=.."
        ).locator(".react-select__input-container")
        city_select.wait_for(state="visible", timeout=5000)
        city_select.click()
        self.page.get_by_role("option", name=city_name).click()

        self.page.locator('input[name="postal_code"]').fill(postal_code)
        self.page.locator('textarea[name="address"]').fill(address)

        if notes:
            self.page.get_by_role("button", name="Add Notes").click()
            self.page.locator('textarea[name="notes"]').fill(notes)

    def add_supplier(self, name: str, contact_person: str, email: str, phone: str, gst_number: str,
                     state_name: str = "Tamil Nadu", city_name: str = "Udumalpet_edit",
                     postal_code: str = "621212", address: str = "", notes: str | None = None) -> None:
        self.page.get_by_role("button", name="Add Supplier").click()
        self.page.wait_for_load_state("networkidle")

        self._fill_supplier_form(
            name, contact_person, email, phone, gst_number, state_name,
            city_name, postal_code, address, notes
        )

        self.page.get_by_role("button", name="Create").click()

        toast = self.page.get_by_text("Suppliers created")
        toast.wait_for(state="visible", timeout=10000)
        self.page.wait_for_load_state("networkidle")

    def validate_invalid_field(self, data: dict[str, str], field: str, value: str) -> bool:
        self.page.get_by_role("button", name="Add Supplier").click()
        self.page.wait_for_load_state("networkidle")
        invalid_data = {**data, field: value}
        self._fill_supplier_form(**invalid_data)
        self.page.get_by_role("button", name="Create").click()

        patterns = {
            "email": (r"email.*(?:invalid|valid|format|domain)", r"invalid.*email"),
            "phone": (r"phone.*(?:invalid|valid|10|digits|start)",),
            "gst_number": (r"gst.*(?:invalid|valid|format|15|characters)",),
            "postal_code": (r"postal.*(?:invalid|valid|6|digits)", r"pincode.*(?:invalid|valid|6|digits)"),
        }
        return has_validation_feedback(self.page, *patterns[field])

    def validate_duplicate_supplier(self, data: dict[str, str]) -> bool:
        self.page.get_by_role("button", name="Add Supplier").click()
        self.page.wait_for_load_state("networkidle")
        self._fill_supplier_form(**data)
        self.page.get_by_role("button", name="Create").click()
        return has_validation_feedback(
            self.page,
            r"supplier.*already",
            r"(?:email|gst).*(?:already|duplicate|taken)",
            r"duplicate.*supplier",
        )

    def search_supplier(self, name: str) -> bool:
        search_box = self.page.get_by_role("textbox", name="Search supplier...")
        search_box.fill(name)
        search_box.press("Enter")
        self.page.wait_for_load_state("networkidle", timeout=5000)
        locator = self.page.get_by_text(name, exact=True).first
        try:
            locator.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False

    def view_supplier(self, name: str) -> bool:
        self.search_supplier(name)
        row = self.page.locator("tr", has=self.page.get_by_text(name, exact=True))
        row.wait_for(state="visible", timeout=5000)

        row.get_by_title("view").click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)

        try:
            modal.get_by_text(name, exact=True).first.wait_for(state="visible", timeout=5000)
            is_visible = True
        except Exception:
            is_visible = False

        self.page.get_by_role("button", name="Back to List").click()
        modal.wait_for(state="hidden", timeout=5000)
        return is_visible

    def edit_supplier(self, old_name: str, new_name: str) -> bool:
        self.search_supplier(old_name)
        row = self.page.locator("tr", has=self.page.get_by_text(old_name, exact=True))
        row.wait_for(state="visible", timeout=5000)

        row.get_by_title("edit").click()
        self.page.locator("input[name=\"name\"]").fill(new_name)
        self.page.get_by_role("button", name="Update").click()

        toast = self.page.get_by_text("Suppliers updated successfully")
        try:
            toast.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False

    def delete_supplier(self, name: str) -> bool:
        self.search_supplier(name)
        row = self.page.locator("tr", has=self.page.get_by_text(name, exact=True))
        row.wait_for(state="visible", timeout=5000)

        row.get_by_title("delete").first.click()
        self.page.get_by_role("button", name="Delete Supplier").click()

        toast = self.page.get_by_text("Deleted successfully.")
        try:
            toast.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False

    def retrieve_supplier(self, name: str) -> bool:
        self.search_supplier(name)
        row = self.page.locator("tr", has=self.page.get_by_text(name, exact=True))
        row.wait_for(state="visible", timeout=5000)

        row.get_by_title("delete").first.click()
        self.page.get_by_role("button", name="Retrieve Supplier").click()

        toast = self.page.get_by_text("Retrieved successfully.")
        try:
            toast.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False

    def validate_required_fields(self) -> bool:
        self.page.get_by_role("button", name="Add Supplier").click()
        self.page.wait_for_load_state("networkidle")
        modal = self.page.get_by_role("dialog")
        modal.get_by_role("button", name="Create").click()
        return has_required_field_feedback(modal)
