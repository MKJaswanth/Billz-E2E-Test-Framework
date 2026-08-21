from __future__ import annotations

import re

from playwright.sync_api import Page, Response

from pages.common.form_page import has_validation_feedback
from utils.constants import (
    ATTRIBUTE_VALUES_URL,
    LIST_TIMEOUT,
    SETTLED_TIMEOUT,
    UI_TIMEOUT,
)


DELETE_ICON_BUTTON = 'button[title="delete"]:has(i.bi-trash)'
RETRIEVE_ICON_BUTTON = 'button[title="delete"]:has(i.bi-arrow-clockwise)'


class AttributeValuesPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.attribute_values_url = ATTRIBUTE_VALUES_URL

    @property
    def add_button(self):
        return self.page.get_by_role("button", name="Add Attribute Values")

    @property
    def dialog(self):
        return self.page.get_by_role("dialog")

    @property
    def search_box(self):
        return self.page.get_by_role("textbox", name="Search...")

    @property
    def value_input(self):
        return self.dialog.locator('input[name="items.0.value"]')

    @property
    def description_input(self):
        return self.dialog.locator('textarea[name="items.0.description"]')

    @staticmethod
    def _is_list_response(response: Response) -> bool:
        return (
            response.request.method == "GET"
            and response.request.resource_type in {"fetch", "xhr"}
            and re.search(r"/attribute-values(?:\?|$)", response.url)
            is not None
        )

    @staticmethod
    def _is_create_response(response: Response) -> bool:
        return (
            response.request.method == "POST"
            and re.search(r"/attribute-values(?:\?|$)", response.url)
            is not None
        )

    @staticmethod
    def _is_update_response(response: Response) -> bool:
        return (
            response.request.method in {"PUT", "PATCH", "POST"}
            and re.search(r"/attribute-values/\d+", response.url) is not None
        )

    @staticmethod
    def _is_delete_response(response: Response) -> bool:
        return (
            response.request.method == "DELETE"
            and re.search(r"/attribute-values/\d+", response.url) is not None
        )

    def navigate(self) -> None:
        with self.page.expect_response(
            self._is_list_response, timeout=LIST_TIMEOUT
        ):
            self.page.goto(self.attribute_values_url)
        self.add_button.wait_for(state="visible", timeout=UI_TIMEOUT)

    def is_attribute_values_visible(self) -> bool:
        return self.add_button.is_visible()

    def _row(self, name: str):
        return self.page.locator("tbody tr").filter(
            has=self.page.get_by_text(name, exact=True)
        ).first

    def is_attribute_value_active(self, name: str) -> bool:
        if not self.search_attribute_value(name):
            return False
        row = self._row(name)
        delete_btn = row.locator(DELETE_ICON_BUTTON)
        try:
            delete_btn.wait_for(state="visible", timeout=SETTLED_TIMEOUT)
            return True
        except Exception:
            return False

    def search_attribute_value(self, value: str) -> bool:
        if self.search_box.input_value() != value:
            with self.page.expect_response(
                self._is_list_response, timeout=LIST_TIMEOUT
            ):
                self.search_box.fill(value)
        try:
            self._row(value).wait_for(
                state="visible", timeout=SETTLED_TIMEOUT
            )
            return True
        except Exception:
            return False

    def _select_key(self, key_name: str) -> None:
        control = self.dialog.locator(".react-select__control").first
        control.click()

        input_elem = control.locator("input").first
        if input_elem.is_visible():
            input_elem.fill(key_name)

        option = self.page.locator(
            ".react-select__option, div[class*='-option']"
        ).filter(has=self.page.get_by_text(key_name, exact=True)).first

        try:
            option.wait_for(state="visible", timeout=SETTLED_TIMEOUT)
            option.click()
        except Exception:
            self.page.keyboard.press("Enter")

    def add_attribute_value(
        self, key_name: str, value: str, description: str | None = None
    ) -> None:
        self.add_button.click()
        modal = self.dialog
        modal.wait_for(state="visible", timeout=UI_TIMEOUT)

        self._select_key(key_name)
        self.value_input.fill(value)

        if description:
            add_notes_btn = modal.get_by_role("button", name="Add Notes")
            if add_notes_btn.is_visible():
                add_notes_btn.click()
            self.description_input.fill(description)

        with self.page.expect_response(
            self._is_create_response, timeout=LIST_TIMEOUT
        ) as response_info:
            modal.get_by_role("button", name="Create").click()

        assert response_info.value.status in (200, 201)
        modal.wait_for(state="hidden", timeout=UI_TIMEOUT)

    def view_attribute_value(
        self, value: str, expected_description: str | None = None
    ) -> bool:
        if not self.search_attribute_value(value):
            return False

        row = self._row(value)
        row.wait_for(state="visible", timeout=UI_TIMEOUT)

        row.get_by_title("view").click()
        modal = self.dialog
        modal.wait_for(state="visible", timeout=UI_TIMEOUT)

        try:
            modal.get_by_text(value, exact=True).first.wait_for(
                state="visible", timeout=UI_TIMEOUT
            )
            if expected_description:
                modal.get_by_text(expected_description, exact=False).first.wait_for(
                    state="visible", timeout=UI_TIMEOUT
                )
            is_visible = True
        except Exception:
            is_visible = False

        close_btn = modal.locator(".btn-close")
        if not close_btn.is_visible():
            close_btn = modal.get_by_role("button", name="Close")
        if not close_btn.is_visible():
            close_btn = modal.get_by_role("button", name="Back to List")
        if close_btn.is_visible():
            close_btn.click()
        modal.wait_for(state="hidden", timeout=UI_TIMEOUT)
        return is_visible

    def edit_attribute_value(
        self, old_value: str, new_value: str, new_description: str | None = None
    ) -> bool:
        if not self.search_attribute_value(old_value):
            return False

        row = self._row(old_value)
        row.wait_for(state="visible", timeout=UI_TIMEOUT)

        row.get_by_title("edit").click()
        modal = self.dialog
        modal.wait_for(state="visible", timeout=UI_TIMEOUT)

        try:
            modal.locator(".spinner-border").wait_for(
                state="hidden", timeout=SETTLED_TIMEOUT
            )
        except Exception:
            pass

        self.value_input.fill(new_value)
        if new_description is not None:
            add_notes_btn = modal.get_by_role("button", name="Add Notes")
            if add_notes_btn.is_visible():
                add_notes_btn.click()
            if self.description_input.is_visible():
                self.description_input.fill(new_description)

        with self.page.expect_response(
            self._is_update_response, timeout=LIST_TIMEOUT
        ) as response_info:
            modal.get_by_role("button", name="Update").click()

        if response_info.value.status not in (200, 204):
            return False
        modal.wait_for(state="hidden", timeout=UI_TIMEOUT)
        return True

    def delete_attribute_value(self, value: str) -> bool:
        if not self.search_attribute_value(value):
            return False

        row = self._row(value)
        row.wait_for(state="visible", timeout=UI_TIMEOUT)

        row.locator(DELETE_ICON_BUTTON).click()
        modal = self.dialog
        modal.wait_for(state="visible", timeout=UI_TIMEOUT)

        with self.page.expect_response(
            self._is_delete_response, timeout=LIST_TIMEOUT
        ) as response_info:
            modal.get_by_role(
                "button", name="Delete Attribute Value"
            ).click()

        if response_info.value.status not in (200, 204):
            return False
        modal.wait_for(state="hidden", timeout=UI_TIMEOUT)
        return True

    def retrieve_attribute_value(self, value: str) -> bool:
        if not self.search_attribute_value(value):
            return False

        row = self._row(value)
        row.wait_for(state="visible", timeout=UI_TIMEOUT)

        retrieve_btn = row.locator(RETRIEVE_ICON_BUTTON)
        retrieve_btn.wait_for(state="visible", timeout=UI_TIMEOUT)
        retrieve_btn.click()

        modal = self.dialog
        modal.wait_for(state="visible", timeout=UI_TIMEOUT)

        modal.get_by_role(
            "button", name="Retrieve Attribute Value"
        ).click()

        toast = self.page.get_by_text("Retrieved successfully.").first
        try:
            toast.wait_for(state="visible", timeout=UI_TIMEOUT)
            modal.wait_for(state="hidden", timeout=UI_TIMEOUT)
            return True
        except Exception:
            return False

    def validate_required_fields(self) -> bool:
        self.add_button.click()
        modal = self.dialog
        modal.wait_for(state="visible", timeout=UI_TIMEOUT)

        requests: list[str] = []
        listener = lambda request: requests.append(request.url)
        self.page.on("request", listener)
        try:
            modal.get_by_role("button", name="Create").click()
            has_error = has_validation_feedback(
                self.page,
                r"Value is required",
                r"Attribute Value is required",
                r"field is required",
                r"required",
            )
            api_calls = [
                url
                for url in requests
                if re.search(r"/attribute-values(?:\?|$)", url)
            ]
            is_valid = has_error and len(api_calls) == 0
        finally:
            self.page.remove_listener("request", listener)

        modal.get_by_role("button", name="Cancel").click()
        modal.wait_for(state="hidden", timeout=UI_TIMEOUT)
        return is_valid

    def validate_duplicate_value(self, key_name: str, value: str) -> bool:
        self.add_button.click()
        modal = self.dialog
        modal.wait_for(state="visible", timeout=UI_TIMEOUT)

        self._select_key(key_name)
        self.value_input.fill(value)

        with self.page.expect_response(
            self._is_create_response, timeout=LIST_TIMEOUT
        ) as response_info:
            modal.get_by_role("button", name="Create").click()

        rejected = response_info.value.status in (400, 409, 422)
        has_error = has_validation_feedback(
            self.page,
            r"already been taken",
            r"already exists",
            r"duplicate",
        )
        modal.get_by_role("button", name="Cancel").click()
        modal.wait_for(state="hidden", timeout=UI_TIMEOUT)
        return rejected and has_error
