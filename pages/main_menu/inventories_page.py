from __future__ import annotations

import re

from playwright.sync_api import Page

from utils.constants import INVENTORIES_URL


class InventoriesPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.url = INVENTORIES_URL

    def navigate(self) -> None:
        self.page.goto(self.url)
        self.page.wait_for_load_state("networkidle")

    def is_inventories_visible(self) -> bool:
        """Verify the inventory overview page loaded (title + table present)."""
        try:
            self.page.get_by_text("Inventory Overview").first.wait_for(
                state="visible", timeout=5000
            )
            return True
        except Exception:
            return False

    # ─── Search ────────────────────────────────────────────────────────────────

    def search_inventory(self, product_name: str) -> bool:
        """Search for a product in the inventory list and return True if found."""
        search_box = self.page.get_by_placeholder("Search inventory...")
        search_box.fill(product_name)
        search_box.press("Enter")
        self.page.wait_for_load_state("networkidle", timeout=5000)
        try:
            self.page.locator("table tbody tr").filter(
                has_text=product_name
            ).first.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False

    # ─── Read Stock Values ─────────────────────────────────────────────────────

    def get_stock_values(self, product_name: str) -> dict:
        """Search for product and return its stock values from the table row.

        Returns dict with keys: total_stock, available_stock, status.
        Values are strings exactly as displayed.
        """
        self.search_inventory(product_name)
        row = self.page.locator("table tbody tr").filter(
            has_text=product_name
        ).first
        row.wait_for(state="visible", timeout=5000)

        # Read all cells in the row
        cells = row.locator("td").all()
        values = {}

        # Status badge
        try:
            badge = row.locator(".badge").first
            values["status"] = badge.text_content().strip()
        except Exception:
            values["status"] = ""

        # Total Stock and Available Stock columns
        # Columns: Product Name | Branch | Category | Status | Total Stock | Available Stock | Unit Values | Actions
        # Index:   0            | 1      | 2        | 3      | 4           | 5              | 6           | 7
        try:
            values["total_stock"] = cells[4].text_content().strip() if len(cells) > 4 else ""
            values["available_stock"] = cells[5].text_content().strip() if len(cells) > 5 else ""
        except Exception:
            values["total_stock"] = ""
            values["available_stock"] = ""

        return values

    def get_available_stock_number(self, product_name: str) -> int:
        """Get available stock as an integer for arithmetic assertions."""
        values = self.get_stock_values(product_name)
        stock_str = values.get("available_stock", "0")
        # Extract leading digits (stock value may have unit suffix like "10 pcs")
        match = re.match(r"(\d+)", stock_str)
        return int(match.group(1)) if match else 0

    def get_total_stock_number(self, product_name: str) -> int:
        """Get total stock as an integer for arithmetic assertions."""
        values = self.get_stock_values(product_name)
        stock_str = values.get("total_stock", "0")
        match = re.match(r"(\d+)", stock_str)
        return int(match.group(1)) if match else 0

    # ─── Filters ───────────────────────────────────────────────────────────────

    def expand_filters(self) -> None:
        """Expand the filters panel if collapsed."""
        try:
            toggle_btn = self.page.get_by_role("button", name=re.compile(r"filter", re.IGNORECASE))
            if toggle_btn.is_visible():
                toggle_btn.click()
                self.page.wait_for_timeout(500)
        except Exception:
            pass

    def filter_by_branch(self, branch_name: str) -> None:
        """Apply branch filter from the filters panel."""
        self.expand_filters()
        self.page.locator("input[name='branch_id']").locator(
            "xpath=.."
        ).locator(".react-select__input-container").click()
        self.page.get_by_role("option", name=branch_name).click()
        self.page.get_by_role("button", name="Filter", exact=True).click()
        self.page.wait_for_load_state("networkidle", timeout=5000)

    def filter_by_category(self, category_name: str) -> None:
        """Apply category filter from the filters panel."""
        self.expand_filters()
        self.page.locator("input[name='category_id']").locator(
            "xpath=.."
        ).locator(".react-select__input-container").click()
        self.page.get_by_role("option", name=category_name).click()
        self.page.get_by_role("button", name="Filter", exact=True).click()
        self.page.wait_for_load_state("networkidle", timeout=5000)

    def toggle_low_stock_filter(self) -> None:
        """Toggle the 'Low Stock Only' checkbox and apply filter."""
        self.expand_filters()
        self.page.locator("input[name='low_stock_only']").check()
        self.page.get_by_role("button", name="Filter", exact=True).click()
        self.page.wait_for_load_state("networkidle", timeout=5000)

    def clear_filters(self) -> None:
        """Click the Clear Filters button to reset all filters."""
        self.expand_filters()
        try:
            self.page.get_by_text("Clear Filters").click()
            self.page.wait_for_load_state("networkidle", timeout=5000)
        except Exception:
            pass

    def is_table_empty(self) -> bool:
        """Return True if the inventory table shows the empty state message."""
        try:
            self.page.get_by_text("No inventory found.").wait_for(
                state="visible", timeout=3000
            )
            return True
        except Exception:
            return False

    def is_product_in_table(self, product_name: str) -> bool:
        """Return True if the product name is visible anywhere in the table body."""
        try:
            self.page.locator("table tbody tr").filter(
                has_text=product_name
            ).first.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False

    # ─── Detail View (Drawer) ──────────────────────────────────────────────────

    def view_inventory_detail(self, product_name: str) -> bool:
        """Click the view action on a product row and verify detail drawer opens."""
        self.search_inventory(product_name)
        row = self.page.locator("table tbody tr").filter(
            has_text=product_name
        ).first
        row.wait_for(state="visible", timeout=5000)

        row.get_by_title("view").first.click()

        # Wait for the drawer/card to appear with batch info
        try:
            self.page.get_by_text("Batches").first.wait_for(
                state="visible", timeout=5000
            )
            # Verify batch table columns are visible
            self.page.get_by_text("Batch Number").first.wait_for(
                state="visible", timeout=3000
            )
            return True
        except Exception:
            return False

    def close_detail_drawer(self) -> None:
        """Close the inventory detail drawer if open."""
        try:
            self.page.locator(".btn-close").first.click()
        except Exception:
            try:
                self.page.keyboard.press("Escape")
            except Exception:
                pass

    # ─── Export ────────────────────────────────────────────────────────────────

    def export_inventory_pdf(self, filter_type: str = "all") -> str | None:
        """Open export modal, select filter, download PDF, return file path."""
        self.page.get_by_role("button", name="Export").click()

        # Wait for export modal
        self.page.get_by_text("Export Inventory").wait_for(
            state="visible", timeout=5000
        )

        # Select the stock filter option if not "all"
        if filter_type != "all":
            self.page.locator("input[name='stock']").locator(
                "xpath=.."
            ).locator(".react-select__input-container").click()
            label_map = {
                "all": "All",
                "low_stock": "Low Stock",
                "empty_stock": "No Stock",
            }
            self.page.get_by_role(
                "option", name=label_map.get(filter_type, "All")
            ).click()

        # Click Filter/Download button inside the modal
        with self.page.expect_download(timeout=15000) as download_info:
            self.page.locator("div.modal-content, div[role='dialog']").get_by_role(
                "button", name="Filter"
            ).click()

        download = download_info.value
        return download.path()
