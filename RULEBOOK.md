# 📘 Playwright Python Test Automation Rulebook

This rulebook defines the mandatory architecture, coding standards, performance rules, and execution standards for every test module in the `billz` repository.

---

## 📑 Core Principles & Standards

### Rule 1: Handling Known Application Defects (`xfail` vs `skip`)
* **Mandatory Rule**: Use `@pytest.mark.xfail(reason="Bug #...: Description")` for all active application bugs.
* **Prohibited**: **Never use `@pytest.mark.skip` for known defects.**
* **Rationale**: Skipped tests are completely ignored during test runs. `xfail` keeps tests active in the pipeline without breaking CI builds, and automatically alerts QA with an `XPASS` status the moment a developer fix is deployed.

```python
# ✅ CORRECT PATTERN
@pytest.mark.xfail(reason="Bug #104: Phone numbers starting outside 6-9 are accepted")
def test_reject_invalid_branch_phone(logged_in_page):
    branches_page = BranchesPage(logged_in_page)
    branches_page.navigate()
    assert branches_page.validate_invalid_phone("1234567890")
```

---

### Rule 2: Teardown Performance & Cleanup Optimization
* **Mandatory Rule**: When a test function explicitly deletes a record (e.g. `delete_branch`), remove the item name from the cleanup list immediately (`cleanup.remove(item_name)`).
* **Rationale**: Prevents teardown fixtures from searching for already-deleted items and incurring 15-second Playwright locator timeout delays.

```python
# ✅ CORRECT PATTERN
def test_branch_crud_lifecycle(logged_in_page, branch_cleanup):
    branches_page = BranchesPage(logged_in_page)
    branch_name = branches_page.add_branch()
    branch_cleanup.append(branch_name)

    # If deletion succeeds, remove from cleanup list to prevent teardown timeout
    if branches_page.delete_branch(branch_name):
        branch_cleanup.remove(branch_name)
```

---

### Rule 3: Single End-to-End CRUD Lifecycle Pattern
* **Mandatory Rule**: Combine happy-path entity management operations (Roles, Cities, Branches, Users, Categories, Racks, Products) into **one single End-to-End CRUD test** (`test_<entity>_crud_lifecycle`).
* **Sequence**: Create $\rightarrow$ Search $\rightarrow$ View $\rightarrow$ Edit $\rightarrow$ Delete $\rightarrow$ Restore.
* **Rationale**: Achieves a **3x–5x speedup** by creating only 1 record per module instead of 5 separate records, and handles cleanup naturally at the end of the flow.

### Rule 3A: Mandatory Soft Delete & Restore Contract
* **Mandatory Rule**: Modules that support soft deletion must verify both deletion and restoration using state-specific, row-scoped locators.
* **Rationale**: The same action button changes behavior after deletion. Generic button locators can target the wrong state or act before the transition completes.
* **Soft Delete Action**: Target `button[title="delete"]:has(i.bi-trash)` on the active target row.
* **Restore / Retrieve Action**: Target `button[title="delete"]:has(i.bi-arrow-clockwise)` on the soft-deleted target row.
* **Waiting Requirement**: Before restoring, explicitly wait for `i.bi-arrow-clockwise` to become visible on the soft-deleted row.
* **Verification Requirement**: Verify the persisted state through the refreshed list, show API, or reopened record. A success toast alone is insufficient.

```python
# ✅ CORRECT PATTERN
def test_city_crud_lifecycle(logged_in_page):
    cities_page = CitiesPage(logged_in_page)
    cities_page.navigate()

    city_name = cities_page.add_city()               # 1. Create
    assert cities_page.search_city(city_name)        # 2. Search
    assert cities_page.view_city(city_name)          # 3. View
    
    edited_name = city_name + "_edited"
    assert cities_page.edit_city(city_name, edited_name) # 4. Edit
    assert cities_page.delete_city(edited_name)      # 5. Delete
    assert cities_page.retrieve_city(edited_name)    # 6. Restore
```

---

### Rule 4: Two-Level Form Validation Assertions
* **Mandatory Rule**: Form validation tests MUST assert **both** visible UI error messages and confirm the network API request was rejected (not HTTP 200/201).
* **Prohibited**: Do not use page-wide regular expression text searches (e.g. `page.get_by_text("Error")`) as they match unrelated labels or placeholders.

```python
# ✅ CORRECT PATTERN
def test_reject_blank_role_name(logged_in_page):
    roles_page = RolesPage(logged_in_page)
    roles_page.navigate()

    with logged_in_page.expect_response(lambda r: "/roles" in r.url and r.request.method == "POST") as resp_info:
        roles_page.submit_blank_role()

    assert resp_info.value.status == 422
    assert roles_page.get_name_field_error() == "The role name field is required."
```

---

### Rule 5: Page Object Model `@property` Locators
* **Mandatory Rule**: Use `@property` getters for element locators in Page Object classes (`pages/`).
* **Rationale**: Ensures locators are re-evaluated dynamically against the live DOM on every access, avoiding stale element exceptions and keeping test code clean (`page.from_date.fill(...)`).

```python
# ✅ CORRECT PATTERN
class DayBookPage:
    @property
    def from_date(self):
        return self.page.locator("label", has_text="From").first.locator("xpath=..").locator("input")
```

---

### Rule 6: Role-Based Access Control (RBAC) 3-Layer Testing
* **Mandatory Rule**: RBAC test modules must cover 3 security layers:
  1. **Route & Menu Layer**: Verify unauthorized menu links are hidden and direct URL navigation triggers a 403 or redirect.
  2. **UI Action Layer**: Verify `Add`, `Edit`, and `Delete` buttons are hidden/disabled for read-only roles.
  3. **API Security Layer**: Verify direct `POST`, `PUT`, or `DELETE` API requests return HTTP `403 Forbidden`.

---

### Rule 7: Parallel Worker Execution (`pytest-xdist`)
* **Mandatory Rule**: When running tests in parallel, always use `python -m pytest ... -n <workers> --dist loadfile`.
* **Rationale**: Ensures all test functions within a single file run on the same worker, preventing shared-data state conflicts across parallel execution threads.

```bash
# Recommended Command:
python -m pytest tests/master_menu/ -n 4 --dist loadfile -v
```

---

### Rule 8: Financial & Mathematical Invariants
* **Mandatory Rule**: In accounting and financial report modules (*Day Book, Cash Flow, P&L, Balance Sheet, Ledger*), assert exact mathematical relationships using Python's `Decimal` module:
  * `Net Profit = Total Income - Total Expense`
  * `Closing Cash = Opening Cash + Net Cash Flow`
  * `Closing Balance = Last Running Balance`

---

### Rule 9: Test Data Safety & Cleanup Ownership
* **Mandatory Rule**: Never send update or delete requests to hardcoded record IDs such as `/users/1` or `/branches/1`.
* Create a disposable record, capture its actual ID, and perform destructive checks only against that record.
* Every test that creates data must register it for cleanup immediately. Explicit deletion transfers cleanup ownership back to the test and requires removal from the cleanup list as described in Rule 2.
* **Prohibited**: Tests must never modify or delete pre-existing tenant data unless the test explicitly created and owns that data.

---

### Rule 10: Deterministic Waiting & Synchronization
* **Prohibited**: Do not use `time.sleep()` or `page.wait_for_timeout()` to synchronize tests.
* **Mandatory Rule**: Wait for an observable application event such as:
  * a Playwright `expect(...)` assertion,
  * a specific API response,
  * a URL transition,
  * a loading indicator to disappear, or
  * a target element state.
* Use `networkidle` only when it represents a meaningful application state; background polling can prevent it from completing reliably.
* Prefer waiting for a specific API response, disappearance of the relevant loading skeleton/spinner, expected table row, modal state, toast, or URL transition instead of `networkidle`.
* **Timeout Standard**:
  * Use `10 seconds` as the normal maximum for UI assertions and element-state waits.
  * Use up to `20–30 seconds` only for known slow API, report, import, or export operations.
  * Any timeout above `30 seconds` requires a short code comment explaining the operation and reason.
  * Never increase a timeout merely to conceal a flaky locator, missing synchronization event, or application performance defect.

---

### Rule 11: Parallel-Test Isolation
* Test data must use a unique worker-safe suffix such as a timestamp, UUID fragment, or `worker_id`.
* Tests must not depend on execution order, another test's data, or mutable shared state.
* Module/session fixtures may share expensive dependencies only when those records are immutable during the tests that consume them.
* Every test file must remain reliable under `-n <workers> --dist loadfile`.

---

### Rule 12: Locator Priority & Scope
* Prefer locators in this order: `get_by_role`, `get_by_label`, stable `data-testid`, then scoped CSS selectors.
* Avoid fragile XPath, positional selectors such as `.first`/`.nth()` without a stable container, and generic page-wide text matches.
* Table actions must be scoped to the matching row. Modal fields and validation messages must be scoped to the active modal or form.
* Locators must describe user-visible intent and remain stable if unrelated rows or controls are added.
* **Selector Change Protocol**:
  * First determine whether the failure is an application regression, an intentional UI contract change, or an automation-only locator defect.
  * Update the shared Page Object locator instead of patching individual tests with duplicate selectors.
  * Request a stable `data-testid` when no reliable role, label, or scoped semantic locator exists.
  * Run every module that consumes the changed Page Object or shared component.
  * Record the selector change and its cause in the handoff summary; do not silently patch a broken selector without identifying why it changed.

---

### Rule 13: UI, API & Persistence Verification
* Successful CRUD actions must verify the visible result and the corresponding successful API response or persisted state after reload/search.
* **Mandatory post-edit verification**: After every successful edit, the lifecycle test MUST reopen the persisted record through View. If the module has no View action, reopen Edit or fetch the owned record through its show API.
* The reopened record MUST be compared against every field changed by the test. A renamed row, successful response, or toast alone does not prove that the remaining edited fields persisted.
* Edit coverage SHOULD change at least two meaningful fields when the form supports them, such as name plus description, email, code, address, parent, or account details.
* Relational fields that are expected to remain unchanged during an edit, such as a User's Branch or an Account Group's Parent, SHOULD also be checked when they are visible in View.
* Invalid submissions must verify a field-specific UI error and one of the following:
  * the API rejects the request with a non-success status, normally `422` or `403`; or
  * client-side validation prevents the request from being sent at all.
* RBAC coverage must include all three layers from Rule 6: menu/direct route, UI actions, and API authorization.
* **Prohibited**: A toast message alone is not sufficient proof that data was saved correctly.

---

### Rule 14: Failure, Retry & Diagnostic Artifact Policy
* The default retry count is zero. Retries must not be used to hide unstable tests or application defects.
* A maximum of one retry may be enabled in CI only for a confirmed transient infrastructure, browser-startup, or network-transport failure.
* Assertion, validation, locator, and reproducible application failures must never receive an automatic retry.
* Preserve the original failure trace, screenshot, video, and request/response evidence whenever a retry occurs.
* Every retried test must remain visible in the CI report and be recorded for investigation as flaky, even when the retry passes.
* Final failures must retain useful diagnostics such as the Playwright trace, screenshot, video, and relevant request/response details where configured.
* Broad `try/except` blocks that convert failures into passes are prohibited.

---

### Rule 15: Module Completion & Tracker Synchronization
* A module is complete only after its applicable coverage is verified:
  * lifecycle or transactional flow,
  * positive and negative validation,
  * dependency restrictions,
  * RBAC,
  * filtering/pagination where applicable,
  * calculations/export for reports, and
  * final cleanup.
* Tracker status must be updated from the latest verified execution:
  * `Pass` for verified passing behavior,
  * `Fail` for an active product defect represented by `xfail`, and
  * `Not Executed` only when the scenario has not been run.
* Remove an `xfail` immediately after the defect is fixed and the test passes normally.

---

## 🛠️ Summary Checklist for Every New/Updated Test Module

- [ ] Does happy-path testing use a single `test_<entity>_crud_lifecycle` flow?
- [ ] Are known application defects marked with `@pytest.mark.xfail(reason="Bug #...: ...")`?
- [ ] Do deleted records call `cleanup.remove(item_name)`?
- [ ] Are update/delete operations limited to disposable records created by the test?
- [ ] Do Page Objects use `@property` for dynamic locators?
- [ ] Are locators semantic, stable, and scoped to the correct row/modal/form?
- [ ] Are fixed sleeps and `page.wait_for_timeout()` absent?
- [ ] Are form validation failures verified through UI errors and API rejection/no request?
- [ ] After edit, is the persisted record reopened and every changed field compared with the submitted value?
- [ ] Does RBAC cover menu/route, UI controls, and API authorization?
- [ ] Is test data unique, independent, and safe for parallel workers?
- [ ] Are retries, flaky results, and failure artifacts handled according to Rule 14?
- [ ] Does the module satisfy the completion criteria in Rule 15?
- [ ] Can the test file run cleanly in parallel using `-n 4 --dist loadfile`?
