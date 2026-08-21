from __future__ import annotations

import re

from playwright.sync_api import Page, Response, expect

from utils.constants import (
    USERS_URL,
    LIST_TIMEOUT,
    SETTLED_TIMEOUT,
    UI_TIMEOUT,
)
from pages.common.form_page import has_validation_feedback


DELETE_ICON_BUTTON = 'button[title="delete"]:has(i.bi-trash)'
RETRIEVE_ICON_BUTTON = 'button[title="delete"]:has(i.bi-arrow-clockwise)'


class UsersPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.users_url = USERS_URL

    @property
    def add_user_button(self):
        return self.page.get_by_role("button", name="Add User")

    @property
    def search_box(self):
        return self.page.get_by_role("textbox", name="Search users...")

    @property
    def user_dialog(self):
        return self.page.get_by_role("dialog")

    @property
    def user_name_input(self):
        return self.user_dialog.locator('input[name="name"]')

    @staticmethod
    def _is_list_response(response: Response) -> bool:
        return (
            response.request.method == "GET"
            and response.request.resource_type in {"fetch", "xhr"}
            and re.search(r"/users(?:\?|$)", response.url) is not None
        )

    @staticmethod
    def _is_create_response(response: Response) -> bool:
        return (
            response.request.method == "POST"
            and re.search(r"/users(?:\?|$)", response.url) is not None
        )

    @staticmethod
    def _is_show_response(response: Response) -> bool:
        return (
            response.request.method == "GET"
            and re.search(r"/users/\d+(?:\?|$)", response.url) is not None
        )

    @staticmethod
    def _is_update_response(response: Response) -> bool:
        return (
            response.request.method == "PUT"
            and re.search(r"/users/\d+(?:\?|$)", response.url) is not None
        )

    @staticmethod
    def _is_delete_response(response: Response) -> bool:
        return (
            response.request.method == "DELETE"
            and re.search(r"/users/\d+", response.url) is not None
        )

    def _row(self, user_name: str):
        return self.page.locator("tbody tr").filter(
            has=self.page.get_by_text(user_name, exact=True)
        ).first

    def navigate(self) -> None:
        with self.page.expect_response(
            self._is_list_response, timeout=LIST_TIMEOUT
        ):
            self.page.goto(self.users_url)
        self.add_user_button.wait_for(state="visible", timeout=UI_TIMEOUT)

    def is_user_visible(self) -> bool:
        return self.add_user_button.is_visible()

    def search_user(self, user_name: str) -> bool:
        if self.search_box.input_value() != user_name:
            with self.page.expect_response(
                self._is_list_response, timeout=LIST_TIMEOUT
            ):
                self.search_box.fill(user_name)
        try:
            self._row(user_name).wait_for(
                state="visible", timeout=SETTLED_TIMEOUT
            )
            return True
        except Exception:
            return False

    def add_user(
        self,
        name: str,
        email: str,
        password: str,
        branch_name: str,
        role_name: str,
    ) -> None:
        self.add_user_button.click()
        self.user_dialog.wait_for(state="visible", timeout=UI_TIMEOUT)

        self.user_name_input.fill(name)
        self.user_dialog.locator('input[name="email"]').fill(email)
        self.user_dialog.locator('input[name="password"]').fill(password)

        branch_container = self.page.locator(".react-select__value-container.react-select__value-container--is-multi > .react-select__input-container")
        branch_container.click()
        self.page.keyboard.type(branch_name)
        self.page.get_by_role("option", name=branch_name, exact=False).first.click()

        role_container = self.page.locator("div:nth-child(6) > .mb-3 > .css-b62m3t-container > .react-select__control > .react-select__value-container > .react-select__input-container")
        role_container.click()
        self.page.keyboard.type(role_name)
        self.page.get_by_role("option", name=role_name, exact=False).first.click()

        with self.page.expect_response(
            self._is_create_response, timeout=LIST_TIMEOUT
        ) as response_info:
            self.user_dialog.get_by_role("button", name="Create").click()
        assert response_info.value.status in (200, 201), (
            f"User create API returned {response_info.value.status}"
        )
        self.page.get_by_text("User created successfully").wait_for(
            state="visible", timeout=UI_TIMEOUT
        )

    def edit_user(
        self,
        old_name: str,
        new_name: str,
        new_email: str | None = None,
    ) -> bool:
        if not self.search_user(old_name):
            return False

        user_row = self._row(old_name)
        with self.page.expect_response(
            self._is_show_response, timeout=LIST_TIMEOUT
        ):
            user_row.get_by_title("edit").click()

        self.user_dialog.wait_for(state="visible", timeout=UI_TIMEOUT)
        expect(self.user_name_input).to_have_value(
            old_name, timeout=LIST_TIMEOUT
        )
        self.user_name_input.fill(new_name)
        if new_email is not None:
            self.user_dialog.locator('input[name="email"]').fill(new_email)

        with self.page.expect_response(
            self._is_update_response, timeout=LIST_TIMEOUT
        ) as response_info:
            self.user_dialog.get_by_role("button", name="Update").click()

        if response_info.value.status not in (200, 204):
            return False

        self.page.get_by_text("User updated successfully").wait_for(
            state="visible", timeout=UI_TIMEOUT
        )
        return True

    def view_user(
        self,
        user_name: str,
        *,
        expected_email: str | None = None,
        expected_branch: str | None = None,
    ) -> bool:
        if not self.search_user(user_name):
            return False

        with self.page.expect_response(
            self._is_show_response, timeout=LIST_TIMEOUT
        ):
            self._row(user_name).get_by_title("view").click()

        modal = self.user_dialog
        modal.wait_for(state="visible", timeout=UI_TIMEOUT)

        try:
            modal.get_by_text(user_name, exact=True).first.wait_for(
                state="visible", timeout=LIST_TIMEOUT
            )
            if expected_email is not None:
                modal.get_by_text(
                    expected_email, exact=True
                ).first.wait_for(state="visible", timeout=UI_TIMEOUT)
            if expected_branch is not None:
                modal.get_by_text(
                    expected_branch, exact=True
                ).first.wait_for(state="visible", timeout=UI_TIMEOUT)
            is_visible = True
        except Exception:
            is_visible = False

        modal.get_by_role("button", name="Back to List").click()
        return is_visible

    def delete_user(self, user_name: str) -> bool:
        if not self.search_user(user_name):
            return False

        self._row(user_name).locator(DELETE_ICON_BUTTON).click()
        with self.page.expect_response(
            self._is_delete_response, timeout=LIST_TIMEOUT
        ) as response_info:
            self.page.get_by_role("button", name="Delete User").click()

        if response_info.value.status not in (200, 204):
            return False

        self.page.get_by_text("Deleted successfully.").wait_for(
            state="visible", timeout=UI_TIMEOUT
        )
        return True

    def retrieve_user(self, user_name: str) -> bool:
        if not self.search_user(user_name):
            return False

        self._row(user_name).locator(RETRIEVE_ICON_BUTTON).click()
        with self.page.expect_response(
            self._is_delete_response, timeout=LIST_TIMEOUT
        ) as response_info:
            self.page.get_by_role("button", name="Retrieve User").click()

        if response_info.value.status not in (200, 204):
            return False

        self.page.get_by_text("Retrieved successfully.").wait_for(
            state="visible", timeout=UI_TIMEOUT
        )
        return True

    def is_user_active(self, user_name: str) -> bool:
        if not self.search_user(user_name):
            return False
        try:
            self._row(user_name).locator(DELETE_ICON_BUTTON).wait_for(
                state="visible", timeout=SETTLED_TIMEOUT
            )
            return True
        except Exception:
            return False

    def validate_user_required_fields(self) -> bool:
        self.page.get_by_role("button", name="Add User").click()
        self.page.get_by_role("button", name="Create").click()
        
        name_err = self.page.get_by_text("Name is required")
        email_err = self.page.get_by_text("Email is required")
        password_err = self.page.get_by_text("Password is required")
        
        try:
            name_err.wait_for(state="visible", timeout=5000)
            email_err.wait_for(state="visible", timeout=5000)
            password_err.wait_for(state="visible", timeout=5000)
            is_valid = True
        except Exception:
            is_valid = False
            
        self.navigate()
        return is_valid

    def validate_invalid_user_field(
        self, name: str, email: str, password: str, branch_name: str, role_name: str, field: str
    ) -> bool:
        self.page.get_by_role("button", name="Add User").click()
        self.page.locator('input[name="name"]').fill(name)
        self.page.locator('input[name="email"]').fill(email)
        self.page.locator('input[name="password"]').fill(password)

        branch_container = self.page.locator(
            ".react-select__value-container.react-select__value-container--is-multi "
            "> .react-select__input-container"
        )
        branch_container.click()
        self.page.keyboard.type(branch_name)
        self.page.get_by_role("option", name=branch_name, exact=False).first.click()

        role_container = self.page.locator(
            "div:nth-child(6) > .mb-3 > .css-b62m3t-container "
            "> .react-select__control > .react-select__value-container "
            "> .react-select__input-container"
        )
        role_container.click()
        self.page.keyboard.type(role_name)
        self.page.get_by_role("option", name=role_name, exact=False).first.click()
        self.page.get_by_role("button", name="Create").click()

        patterns = {
            "email": (
                r"invalid email",
                r"valid email",
                r"email.*format",
            ),
            "password": (
                r"password.*(?:at least|minimum|uppercase|lowercase|number|special|weak)",
                r"(?:at least|minimum).*password",
            ),
        }
        return has_validation_feedback(self.page, *patterns[field])

    def validate_duplicate_email(self, name: str, email: str, password: str, branch_name: str, role_name: str) -> bool:
        self.page.get_by_role("button", name="Add User").click()
        self.page.locator('input[name="name"]').fill(name)
        self.page.locator('input[name="email"]').fill(email)
        self.page.locator('input[name="password"]').fill(password)

        branch_container = self.page.locator(
            ".react-select__value-container.react-select__value-container--is-multi "
            "> .react-select__input-container"
        )
        branch_container.click()
        self.page.keyboard.type(branch_name)
        self.page.get_by_role("option", name=branch_name, exact=False).first.click()

        role_container = self.page.locator(
            "div:nth-child(6) > .mb-3 > .css-b62m3t-container "
            "> .react-select__control > .react-select__value-container "
            "> .react-select__input-container"
        )
        role_container.click()
        self.page.keyboard.type(role_name)
        self.page.get_by_role("option", name=role_name, exact=False).first.click()
        self.page.get_by_role("button", name="Create").click()

        return has_validation_feedback(
            self.page,
            r"email.*already been taken",
            r"email.*already exists",
            r"duplicate.*email",
        )
