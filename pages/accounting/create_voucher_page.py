from __future__ import annotations

from playwright.sync_api import Page

from utils.constants import BASE_URL


CONTRA_VOUCHER_URL = f"{BASE_URL}/vouchers/contra/create"


class CreateVoucherPage:
    """Page object for the Contra Voucher creation form.

    Route: /vouchers/contra/create

    The form uses native <select> elements (no React-Select) and has no
    name attributes.  Fields are identified by position:
      - select[0]: Preset (cash_to_bank | bank_to_cash | bank_to_bank | custom)
      - select[1]: Debit ledger (receives) — the account money goes INTO
      - select[2]: Credit ledger (source) — the account money comes FROM
      - input[type=number]: Amount
      - input[type=date]: Date (defaults to today)
      - textarea: Remarks / narration
      - button[type=submit]: "Create contra"
    """

    def __init__(self, page: Page) -> None:
        self.page = page

    def navigate(self) -> None:
        self.page.goto(CONTRA_VOUCHER_URL)
        self.page.wait_for_load_state("networkidle")
        self.page.locator("form").wait_for(state="visible", timeout=10000)

    # ------------------------------------------------------------------
    # Locators (by position since no name attributes exist)
    # ------------------------------------------------------------------

    @property
    def _preset_select(self):
        return self.page.locator("form select").nth(0)

    @property
    def _debit_ledger_select(self):
        return self.page.locator("form select").nth(1)

    @property
    def _credit_ledger_select(self):
        return self.page.locator("form select").nth(2)

    @property
    def _amount_input(self):
        return self.page.locator("form input[type='number']")

    @property
    def _date_input(self):
        return self.page.locator("form input[type='date']")

    @property
    def _remarks_textarea(self):
        return self.page.locator("form textarea")

    @property
    def _submit_button(self):
        return self.page.get_by_role("button", name="Create contra")

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def create_contra_voucher(
        self,
        debit_ledger: str,
        credit_ledger: str,
        amount: str,
        *,
        preset: str = "custom",
        remarks: str = "",
    ) -> None:
        """Create a Contra Voucher.

        Args:
            debit_ledger: Display name (option text) of the ledger receiving funds.
            credit_ledger: Display name (option text) of the ledger sourcing funds.
            amount: Transfer amount as a string.
            preset: One of cash_to_bank, bank_to_cash, bank_to_bank, custom.
                    Defaults to 'custom' so both ledgers can be manually selected.
            remarks: Optional narration/remarks.
        """
        # 1. Select preset first — this controls whether ledger selects are enabled
        self._preset_select.select_option(preset)
        self.page.wait_for_timeout(500)

        # 2. Select debit ledger (receives)
        if self._debit_ledger_select.get_attribute("disabled") is None:
            self._debit_ledger_select.select_option(label=debit_ledger)
        # If disabled (preset auto-selected), skip — it's already set

        # 3. Select credit ledger (source)
        if self._credit_ledger_select.get_attribute("disabled") is None:
            self._credit_ledger_select.select_option(label=credit_ledger)
        # If disabled (preset auto-selected), skip

        # 4. Fill amount
        self._amount_input.fill(amount)

        # 5. Date defaults to today — leave as-is unless overridden in future

        # 6. Remarks (optional)
        if remarks:
            self._remarks_textarea.fill(remarks)

        # 7. Submit
        self._submit_button.click()

        # Success: the form redirects to /vouchers/history
        self.page.wait_for_url(
            lambda url: "/vouchers/history" in url or "/vouchers/contra/create" not in url,
            timeout=15000,
        )

    def fund_first_bank(self, amount: str = "5000") -> str:
        """Fund the first available bank using cash_to_bank preset.

        Returns the name of the bank that was funded (auto-selected by preset).
        """
        self.navigate()
        self._preset_select.select_option("cash_to_bank")
        self.page.wait_for_timeout(500)

        # Read which bank was auto-selected
        bank_name = self._debit_ledger_select.evaluate(
            "el => el.options[el.selectedIndex]?.text || ''"
        )

        self._amount_input.fill(amount)
        self._submit_button.click()

        self.page.wait_for_url(
            lambda url: "/vouchers/history" in url,
            timeout=15000,
        )
        return bank_name

    def fund_bank_account(self, bank_name: str, amount: str = "5000") -> None:
        """Deposit cash into a bank account using the cash_to_bank preset.

        The cash_to_bank preset auto-selects the first available bank as debit
        and Cash Ledger as credit — both disabled. We then change to custom
        to pick our specific bank.

        If selecting by name fails, falls back to using cash_to_bank with
        whatever bank is auto-selected.
        """
        self.navigate()

        # Try custom preset first (allows selecting specific bank)
        self._preset_select.select_option("custom")
        self.page.wait_for_timeout(500)

        # Try to select our bank
        try:
            self._debit_ledger_select.select_option(label=bank_name)
            self.page.wait_for_timeout(300)
        except Exception:
            # Bank not found by label — fall back to cash_to_bank preset
            self._preset_select.select_option("cash_to_bank")
            self.page.wait_for_timeout(500)
            self._amount_input.fill(amount)
            self._submit_button.click()
            self.page.wait_for_url(
                lambda url: "/vouchers/history" in url,
                timeout=15000,
            )
            return

        # Select first Cash Ledger by value
        credit_options = self._credit_ledger_select.locator("option").all()
        cash_value = None
        for opt in credit_options:
            if opt.text_content() == "Cash Ledger":
                cash_value = opt.get_attribute("value")
                break
        if cash_value:
            self._credit_ledger_select.select_option(value=cash_value)
        else:
            self._credit_ledger_select.select_option(label="Cash Ledger")
        self.page.wait_for_timeout(300)

        # Fill amount and submit
        self._amount_input.fill(amount)
        self._remarks_textarea.fill(f"Fund {bank_name} with {amount}")
        self._submit_button.click()

        # Wait for redirect or check if it stays (validation error)
        try:
            self.page.wait_for_url(
                lambda url: "/vouchers/history" in url,
                timeout=10000,
            )
        except Exception:
            # Custom didn't work — try with cash_to_bank as fallback
            self.navigate()
            self._preset_select.select_option("cash_to_bank")
            self.page.wait_for_timeout(500)
            self._amount_input.fill(amount)
            self._submit_button.click()
            self.page.wait_for_url(
                lambda url: "/vouchers/history" in url,
                timeout=15000,
            )
