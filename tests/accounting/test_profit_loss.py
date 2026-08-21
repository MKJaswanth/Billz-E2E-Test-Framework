"""End-to-end coverage for the non-restaurant Profit / Loss report."""
from datetime import date, timedelta
from decimal import Decimal

import pytest
from playwright.sync_api import expect

from pages.accounting.create_voucher_page import CreateVoucherPage
from pages.accounting.profit_loss_page import ProfitLossPage


@pytest.fixture(scope="module")
def profit_loss_known_state(module_page, voucher_funded_state):
    """Measure a known 30.00 expense journal's exact effect on Profit / Loss."""
    today = date.today().isoformat()
    report_page = ProfitLossPage(module_page)
    report_page.navigate()
    before = report_page.apply_filters(today, today)

    voucher = CreateVoucherPage(module_page)
    voucher.create_journal_voucher(
        [
            {"ledger": "Expense Ledger", "type": "debit", "amount": "30"},
            {"ledger": "Cash Ledger", "type": "credit", "amount": "30"},
        ],
        remarks="Profit loss known expense",
    )
    assert voucher.wait_for_redirect_to_history()

    report_page.navigate()
    after = report_page.apply_filters(today, today)
    return {"before": before, "after": after, **voucher_funded_state}


class TestProfitLossStructure:
    def test_page_loads_and_report_is_requested(self, logged_in_page):
        page = ProfitLossPage(logged_in_page)
        report = page.navigate()
        assert page.is_page_visible()
        assert page.last_status == 200
        assert {"income", "expense", "net_profit", "is_profit"} <= report.keys()

    def test_default_date_range_ends_today(self, logged_in_page):
        page = ProfitLossPage(logged_in_page)
        page.navigate()
        assert page.to_date.input_value() == date.today().isoformat()
        assert page.from_date.input_value() < page.to_date.input_value()

    def test_income_and_expense_tables_have_expected_headers(self, logged_in_page):
        page = ProfitLossPage(logged_in_page)
        page.navigate()
        assert page.table_headers() == [
            ["Ledger", "Branch", "Amount"],
            ["Ledger", "Branch", "Amount"],
        ]


class TestProfitLossFilters:
    def test_reversed_date_range_is_rejected_in_form(self, logged_in_page):
        page = ProfitLossPage(logged_in_page)
        page.navigate()
        today = date.today()
        page.submit_invalid_range(today.isoformat(), (today - timedelta(days=1)).isoformat())
        expect(page.date_validation_error()).to_be_visible()

    def test_future_period_has_zero_totals(self, logged_in_page):
        page = ProfitLossPage(logged_in_page)
        page.navigate()
        report = page.apply_filters("2099-12-31", "2099-12-31")
        assert Decimal(str(report["income"]["total"])) == 0
        assert Decimal(str(report["expense"]["total"])) == 0
        assert Decimal(str(report["net_profit"])) == 0

    def test_branch_filter_returns_only_selected_branch_ledgers(
        self, logged_in_page, profit_loss_known_state
    ):
        page = ProfitLossPage(logged_in_page)
        page.navigate()
        today = date.today()
        report = page.apply_filters(
            (today - timedelta(days=1)).isoformat(),
            today.isoformat(),
            profit_loss_known_state["branch"],
        )
        assert str(report["branch_id"]) not in {"", "None"}
        rows = page.section_rows("Income") + page.section_rows("Expense")
        assert rows
        assert all(row["branch"] == profit_loss_known_state["branch"] for row in rows)

    def test_funded_branch_sales_are_in_branch_income(
        self, logged_in_page, profit_loss_known_state
    ):
        page = ProfitLossPage(logged_in_page)
        page.navigate()
        today = date.today()
        report = page.apply_filters(
            (today - timedelta(days=1)).isoformat(),
            today.isoformat(),
            profit_loss_known_state["branch"],
        )
        assert Decimal(str(report["income"]["total"])) >= Decimal("1000")


class TestProfitLossAccounting:
    def test_known_journal_increases_expense_by_exact_amount(self, profit_loss_known_state):
        before = Decimal(str(profit_loss_known_state["before"]["expense"]["total"]))
        after = Decimal(str(profit_loss_known_state["after"]["expense"]["total"]))
        assert after - before == Decimal("30.00")

    def test_known_expense_does_not_change_income(self, profit_loss_known_state):
        before = Decimal(str(profit_loss_known_state["before"]["income"]["total"]))
        after = Decimal(str(profit_loss_known_state["after"]["income"]["total"]))
        assert after == before

    def test_net_profit_equals_income_minus_expense(
        self, logged_in_page, profit_loss_known_state
    ):
        page = ProfitLossPage(logged_in_page)
        page.navigate()
        today = date.today().isoformat()
        report = page.apply_filters(today, today)
        income = Decimal(str(report["income"]["total"]))
        expense = Decimal(str(report["expense"]["total"]))
        assert Decimal(str(report["net_profit"])) == income - expense

    def test_rendered_rows_sum_to_section_totals(
        self, logged_in_page, profit_loss_known_state
    ):
        page = ProfitLossPage(logged_in_page)
        page.navigate()
        today = date.today().isoformat()
        report = page.apply_filters(today, today)
        income_sum = sum((row["amount"] for row in page.section_rows("Income")), Decimal("0"))
        expense_sum = sum((row["amount"] for row in page.section_rows("Expense")), Decimal("0"))
        assert income_sum == Decimal(str(report["income"]["total"]))
        assert expense_sum == Decimal(str(report["expense"]["total"]))

    def test_summary_cards_match_api_totals(self, logged_in_page, profit_loss_known_state):
        page = ProfitLossPage(logged_in_page)
        page.navigate()
        today = date.today().isoformat()
        report = page.apply_filters(today, today)
        assert page.summary_amount("Total Income") == Decimal(str(report["income"]["total"]))
        assert page.summary_amount("Total Expense") == Decimal(str(report["expense"]["total"]))
        assert page.summary_amount(page.net_label()) == Decimal(str(report["net_profit"]))

    def test_profit_or_loss_label_matches_sign(self, logged_in_page, profit_loss_known_state):
        page = ProfitLossPage(logged_in_page)
        page.navigate()
        today = date.today().isoformat()
        report = page.apply_filters(today, today)
        expected = "Net Profit" if report["is_profit"] else "Net Loss"
        assert page.net_label() == expected
