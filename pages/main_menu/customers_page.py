from __future__ import annotations

from playwright.sync_api import Page
from utils.constants import CUSTOMERS_URL
from pages.common.form_page import has_required_field_feedback, has_validation_feedback
from utils.random_data import generate_random_name, generate_random_email, generate_random_phone, generate_random_postal_code, generate_random_address

class CustomersPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.url = CUSTOMERS_URL

    def navigate(self) -> None:
        self.page.goto(self.url)

    def is_customers_visible(self) -> bool:
        return self.page.get_by_role("button", name="Add Customer").is_visible()

    def _fill_customer_form(
        self, name: str, customer_type: str, email: str, phone: str, notes: str | None, contact_person: str,
        address_line1: str, address_line2: str, state_name: str, city_name: str, postal_code: str,
        default_address: bool = True
    ) -> None:
        self.page.locator('input[name="name"]').fill(name)

        if notes:
            self.page.get_by_role("button", name="Add Notes").click()
            self.page.locator('textarea[name="notes"]').fill(notes)

        # Select Customer Type (Person/Company)
        try:
            self.page.locator("input[name='type']").locator("xpath=..").locator(
                ".react-select__input-container"
            ).first.click()
        except Exception:
            self.page.locator(".react-select__input-container").first.click()
        self.page.get_by_role("option", name=customer_type).click()

        self.page.locator('input[name="email"]').fill(email)
        self.page.get_by_role("textbox", name="Enter 10-digit phone number").fill(phone)

        self.page.locator('input[name="addresses.0.contact_person"]').fill(contact_person)
        self.page.locator('input[name="addresses.0.address_line1"]').fill(address_line1)
        self.page.locator('input[name="addresses.0.address_line2"]').fill(address_line2)

        # Select State
        try:
            state_select = self.page.locator("input[name='addresses.0.state_id']").locator(
                "xpath=.."
            ).locator(".react-select__input-container")
            state_select.click()
        except Exception:
            self.page.locator(
                "div:nth-child(6) > .mb-3 > .css-b62m3t-container > .react-select__control "
                "> .react-select__value-container > .react-select__input-container"
            ).click()
        self.page.get_by_role("option", name=state_name).click()

        # Select City
        try:
            city_select = self.page.locator("input[name='addresses.0.city_id']").locator(
                "xpath=.."
            ).locator(".react-select__input-container")
            city_select.click()
        except Exception:
            self.page.locator(
                "div:nth-child(7) > .mb-3 > .css-b62m3t-container > .react-select__control "
                "> .react-select__value-container > .react-select__input-container"
            ).click()
        self.page.get_by_role("option", name=city_name).click()

        self.page.locator('input[name="addresses.0.postal_code"]').fill(postal_code)

        if default_address:
            self.page.get_by_role("checkbox", name="Default Address").check()

    def add_customer(
        self, name: str, customer_type: str = "Person", email: str | None = None, phone: str | None = None, notes: str = "automated customer notes",
        contact_person: str = "Contact Auto", address_line1: str = "Line 1", address_line2: str = "Line 2",
        state_name: str = "Tamil Nadu", city_name: str | None = None, postal_code: str | None = None, default_address: bool = True
    ) -> str:
        from pages.master_menu.cities_page import CitiesPage
        from utils.random_data import generate_random_code

        # 1. Create a dynamic city if not provided
        if not city_name:
            cities_page = CitiesPage(self.page)
            cities_page.navigate()
            city_name = f"AutoCity_{generate_random_code('C')}"
            cities_page.add_city(city_name)

        # 2. Go back to customers page and add customer
        self.navigate()
        
        email = email or generate_random_email("customer")
        phone = phone or generate_random_phone()
        postal_code = postal_code or generate_random_postal_code()

        self.page.get_by_role("button", name="Add Customer").click()
        self.page.get_by_role("dialog").wait_for(state="visible", timeout=5000)

        self._fill_customer_form(
            name, customer_type, email, phone, notes, contact_person,
            address_line1, address_line2, state_name, city_name, postal_code,
            default_address
        )

        self.page.get_by_role("button", name="Create").click()
        
        toast = self.page.get_by_text("Customer created successfully").first
        toast.wait_for(state="visible", timeout=10000)
        self.page.wait_for_load_state("networkidle")
        return city_name  # Return created city name so tests can clean it up

    def search_customer(self, name: str) -> bool:
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

    def view_customer(self, name: str) -> bool:
        self.search_customer(name)
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

        self.page.get_by_role("button", name="Back to List").click()
        modal.wait_for(state="hidden", timeout=5000)
        return is_visible

    def edit_customer(self, old_name: str, new_name: str) -> bool:
        self.search_customer(old_name)
        row = self.page.locator("tr", has=self.page.get_by_text(old_name, exact=True))
        row.wait_for(state="visible", timeout=5000)

        row.get_by_title("edit").first.click()
        
        self.page.locator("input[name=\"name\"]").fill(new_name)
        self.page.get_by_role("button", name="Update").click()

        toast = self.page.get_by_text("Customer updated successfully").first
        try:
            toast.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False

    def delete_customer(self, name: str) -> bool:
        self.search_customer(name)
        row = self.page.locator("tr", has=self.page.get_by_text(name, exact=True))
        row.wait_for(state="visible", timeout=5000)

        row.get_by_title("delete").first.click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)

        modal.get_by_role("button", name="Delete Customer").click()

        toast = self.page.get_by_text("Deleted successfully.").first
        try:
            toast.wait_for(state="visible", timeout=5000)
            modal.wait_for(state="hidden", timeout=5000)
            return True
        except Exception:
            return False

    def retrieve_customer(self, name: str) -> bool:
        self.search_customer(name)
        row = self.page.locator("tr", has=self.page.get_by_text(name, exact=True))
        row.wait_for(state="visible", timeout=5000)

        row.get_by_title("delete").first.click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)

        modal.get_by_role("button", name="Retrieve Customer").click()

        toast = self.page.get_by_text("Retrieved successfully.").first
        try:
            toast.wait_for(state="visible", timeout=5000)
            modal.wait_for(state="hidden", timeout=5000)
            return True
        except Exception:
            return False

    def validate_invalid_field(self, name: str, customer_type: str, email: str, phone: str, notes: str, contact_person: str,
                               address_line1: str, address_line2: str, state_name: str, city_name: str, postal_code: str,
                               field: str, value: str) -> bool:
        self.page.get_by_role("button", name="Add Customer").click()
        self.page.get_by_role("dialog").wait_for(state="visible", timeout=5000)
        
        args = {
            "name": name, "customer_type": customer_type, "email": email, "phone": phone, "notes": notes,
            "contact_person": contact_person, "address_line1": address_line1, "address_line2": address_line2,
            "state_name": state_name, "city_name": city_name, "postal_code": postal_code
        }
        args[field] = value
        self._fill_customer_form(**args)
        
        self.page.get_by_role("button", name="Create").click()

        patterns = {
            "email": (r"email.*(?:invalid|valid|format|domain|already|taken|exists)", r"invalid.*email", r"already.*(?:taken|exist)"),
            "phone": (r"phone.*(?:invalid|valid|10|digits|start)",),
            "postal_code": (r"postal.*(?:invalid|valid|6|digits)", r"pincode.*(?:invalid|valid|6|digits)", r"postal code must be"),
        }
        return has_validation_feedback(self.page, *patterns[field])

    def validate_duplicate_customer(self, name: str, customer_type: str, email: str, phone: str, notes: str, contact_person: str,
                                    address_line1: str, address_line2: str, state_name: str, city_name: str, postal_code: str) -> bool:
        self.page.get_by_role("button", name="Add Customer").click()
        self.page.get_by_role("dialog").wait_for(state="visible", timeout=5000)
        self._fill_customer_form(
            name, customer_type, email, phone, notes, contact_person,
            address_line1, address_line2, state_name, city_name, postal_code
        )
        self.page.get_by_role("button", name="Create").click()
        return has_validation_feedback(
            self.page,
            r"customer.*already",
            r"(?:email|phone).*(?:already|duplicate|taken|exists)",
            r"duplicate.*customer",
        )

    def validate_required_fields(self) -> bool:
        self.page.get_by_role("button", name="Add Customer").click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)
        modal.get_by_role("button", name="Create").click()
        return has_required_field_feedback(modal)

    def delete_customer_expect_fail(self, name: str) -> bool:
        self.search_customer(name)
        row = self.page.locator("tr", has=self.page.get_by_text(name, exact=True))
        row.wait_for(state="visible", timeout=5000)

        row.get_by_title("delete").first.click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)

        modal.get_by_role("button", name="Delete Customer").click()
        
        # We expect a failure/error toast or the modal remaining open with an error
        # In either case, the customer row should still exist in the table listing after a reload
        self.page.wait_for_timeout(2000)
        self.navigate()
        return self.search_customer(name)

