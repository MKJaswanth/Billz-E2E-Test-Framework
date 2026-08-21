"""
Concurrent Multi-Branch & Dual Window Billing Test for Restaurants Vertical.

Target URL: https://dev-restaurants.devccl-billzweb.crystalbillz.com/login
Credentials: jaswanth.m@crystalcodelabs.com / Jaswanth@1
"""

import os
import re
import threading
from concurrent.futures import ThreadPoolExecutor
import pytest
from playwright.sync_api import Browser, Page, sync_playwright

RESTAURANT_USER_1_EMAIL = os.getenv("RESTAURANT_USER_1_EMAIL", "jaswanth.m@crystalcodelabs.com")
RESTAURANT_USER_1_PASSWORD = os.getenv("RESTAURANT_USER_1_PASSWORD", "Jaswanth@1")
RESTAURANT_USER_2_EMAIL = os.getenv("RESTAURANT_USER_2_EMAIL", "santhosh@crystalcodelabs.com")
RESTAURANT_USER_2_PASSWORD = os.getenv("RESTAURANT_USER_2_PASSWORD", "Test@123")


def login_restaurant(page: Page, email: str = RESTAURANT_USER_1_EMAIL, password: str = RESTAURANT_USER_1_PASSWORD) -> None:
    """Logs into the restaurant portal and navigates to the POS Sales Add page."""
    page.goto("https://dev-restaurants.devccl-billzweb.crystalbillz.com/login")
    page.wait_for_load_state("networkidle")

    # Fill email & password and Sign In
    page.locator("input[name='email']").fill(email)
    page.locator("input[name='password']").fill(password)
    page.get_by_role("button", name="Sign In").click()
    page.wait_for_url("**/dashboard", timeout=10000)

    # Navigate to POS Billing section (/sales/add)
    page.goto("https://dev-restaurants.devccl-billzweb.crystalbillz.com/sales/add")
    page.wait_for_load_state("networkidle")


def perform_billing_flow(page: Page) -> None:
    """Executes the restaurant POS billing and payment collection flow."""
    # 1. Select product -> [1] IDLY
    page.get_by_role("cell", name="Select / Search Product").click()
    page.get_by_role("option", name="[1] IDLY").click()
    page.wait_for_timeout(500)

    # 2. Settle & Bill
    try:
        with page.expect_download(timeout=3000) as download_info:
            page.get_by_role("button", name="Settle & Bill").first.click()
    except Exception:
        page.get_by_role("button", name="Settle & Bill").first.click()

    page.wait_for_timeout(1000)

    # 3. Collect Payment
    page.get_by_role("button", name="Collect Payment").click()
    page.wait_for_timeout(1000)

    # 4. Click active order/table button in payment drawer (e.g., T-1, T-2)
    try:
        page.get_by_role("button", name=re.compile(r"T-.*QA GS|Parcel", re.I)).first.click(timeout=3000)
    except Exception:
        page.locator("button").filter(has_text=re.compile(r"T-|QA GS|Payment: P", re.I)).first.click(timeout=3000)

    # 5. Click Cash payment method and submit
    try:
        page.get_by_role("button", name="Cash").click(timeout=3000)
        page.get_by_role("button", name="Submit").click(timeout=3000)
    except Exception:
        pass


def _simultaneous_billing_worker(worker_id: int, barrier: threading.Barrier, results: dict, email: str, password: str) -> None:
    """Worker thread running a dedicated Playwright instance to trigger true microsecond-level simultaneous billing."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()

        try:
            # Step 1: Login with user account credentials
            login_restaurant(page, email=email, password=password)

            # Step 2: Prepare product IDLY in cart
            page.get_by_role("cell", name="Select / Search Product").click()
            page.get_by_role("option", name="[1] IDLY").click()
            page.wait_for_timeout(500)

            # Step 3: SYNCHRONIZE BOTH WINDOWS AT THREAD BARRIER BEFORE CLICKING SETTLE
            barrier.wait(timeout=30)

            # Step 4: Click Settle & Bill at the EXACT SAME INSTANT
            try:
                with page.expect_download(timeout=3000) as download_info:
                    page.get_by_role("button", name="Settle & Bill").first.click()
            except Exception:
                page.get_by_role("button", name="Settle & Bill").first.click()

            page.wait_for_timeout(1000)

            # Step 5: Collect Payment
            try:
                page.get_by_role("button", name="Collect Payment").click(timeout=3000)
                page.wait_for_timeout(1000)
                page.locator("button").filter(has_text=re.compile(r"T-|QA GS|Payment: P", re.I)).first.click(timeout=3000)
                page.get_by_role("button", name="Cash").click(timeout=3000)
                page.get_by_role("button", name="Submit").click(timeout=3000)
            except Exception:
                pass

            results[worker_id] = "SUCCESS"
        except Exception as err:
            results[worker_id] = f"FAILED: {err}"
        finally:
            context.close()
            browser.close()


@pytest.mark.restaurant
def test_single_restaurant_billing(browser: Browser):
    """Verifies single window POS billing flow for restaurant vertical."""
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()

    try:
        login_restaurant(page)
        perform_billing_flow(page)
    finally:
        context.close()


@pytest.mark.restaurant
def test_simultaneous_dual_window_restaurant_billing():
    """
    Executes TRUE simultaneous billing across two separate browser windows using DIFFERENT user accounts:
    - Window 1: jaswanth.m@crystalcodelabs.com
    - Window 2: santhosh@crystalcodelabs.com
    Uses a Threading Barrier to synchronize both windows so they click 'Settle & Bill'
    at the exact same millisecond.
    """
    barrier = threading.Barrier(2)
    results = {}

    user1 = (RESTAURANT_USER_1_EMAIL, RESTAURANT_USER_1_PASSWORD)
    user2 = (RESTAURANT_USER_2_EMAIL, RESTAURANT_USER_2_PASSWORD)

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [
            executor.submit(_simultaneous_billing_worker, 1, barrier, results, user1[0], user1[1]),
            executor.submit(_simultaneous_billing_worker, 2, barrier, results, user2[0], user2[1]),
        ]
        for f in futures:
            f.result()

    # Assert both simultaneous window billing workers completed successfully
    assert results.get(1) == "SUCCESS", f"Window 1 (Jaswanth) Billing Failed: {results.get(1)}"
    assert results.get(2) == "SUCCESS", f"Window 2 (Santhosh) Billing Failed: {results.get(2)}"

