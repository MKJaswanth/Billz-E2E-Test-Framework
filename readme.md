# Crystal Billz Test Automation Framework

A professional, enterprise-grade test automation suite built with **Playwright (Python)** and **pytest** for verifying the functionality of the **Crystal Billz** application. This framework is designed to be highly reliable, maintainable, and readable for development and QA teams.

---

## 🏗️ Architectural Design & Design Rationale

The framework utilizes the **Page Object Model (POM)** pattern. This architectural choice is driven by the following principles:

### 1. Separation of Concerns (POM vs. Tests)
* **Pages (`pages/`)**: Handle **how** to interact with the UI. They contain element selectors and wrapper functions for UI workflows (e.g., clicking dropdowns, filling inputs). They do not perform assertions.
* **Tests (`tests/`)**: Handle **what** to assert. They use page object methods to perform actions and assert results (e.g., verifying a toast message appears). 
* *Rationale*: If a UI selector changes (e.g., an input ID changes), only the page object needs an update. The tests themselves remain unchanged.

### 2. Module-Based Test Classification
* Test directories match the main sections of the Billz application (`master_menu`, `main_menu`, `accounting`).
* *Rationale*: Grouping tests by menu module allows targeting specific sections of the app (e.g., running Setup configuration tests independently from daily Transaction flows).

### 3. Stateless Test Execution & Custom Rollbacks
* Staging and development database environments are shared. Hardcoding data or leaving test records in the database leads to duplicate name errors and database clutter.
* *Rationale*: Every test module uses custom teardown fixtures that dynamically identify and delete created records (active or soft-deleted) at the end of the execution, leaving the database exactly as it was.

---

## 📁 File Structure & Component Overview

Below is the detailed file structure mapping out the repository and the purpose of each component:

```
playwright-python-tests/
│
├── pages/                                # PAGE OBJECTS LAYER
│   ├── auth/                             # Authentication page wrappers
│   │   └── login_page.py                 # Handles login fields, error messages, and password toggle
│   │
│   ├── master_menu/                      # Master Settings pages (Setup configurations)
│   │   ├── branches_page.py              # Selects and inputs branch details
│   │   ├── roles_page.py                 # Configures user roles and system privileges
│   │   ├── users_page.py                 # Selects branches/roles via custom react-select controls
│   │   ├── bank_accounts_page.py         # Configures company bank account details
│   │   ├── account_groups_page.py        # Manages accounting groups with Tree/Table view toggle
│   │   ├── voucher_types_page.py         # Updates seeded voucher definitions (automatic/manual)
│   │   └── enquiry_stage_workflows_page.py # [New Page Object] Workflow & Stage management
│   │
│   └── common/                           # Shared Page Components
│       └── base_page.py                  # Base class with shared page actions
│
├── tests/                                # TESTS LAYER (Asserts logic & controls workflows)
│   ├── master_menu/                      # Master Menu automated validation test suites
│   │   ├── test_branches.py              # Verifies branch visibility, creation, edit, and cleanup
│   │   ├── test_account_groups.py        # Validates group additions, tree lists, and deletions
│   │   └── test_voucher_types.py         # Tests seeded voucher edits and verifies rollback
│   │
│   ├── main_menu/                        # Transactions, inventory, and inventory batch tests
│   └── accounting/                       # Ledger, Profit & Loss, and Balance Sheet tests
│
├── utils/                                # SHARED UTILITIES LAYER
│   ├── constants.py                      # Stores system URL constants and handles .env loader
│   ├── helpers.py                        # Common action helpers (e.g., navigation delays)
│   └── random_data.py                    # Generates unique, non-colliding emails, passwords, and names
│
├── test_data/                            # JSON templates for static and mock test inputs
├── MILESTONES.md                         # Progress status check sheets
├── skipped.md                            # Centralized log of currently skipped tests and reasons
├── requirements.txt                      # Declares python library dependencies
├── pytest.ini                            # pytest framework runner options
└── readme.md                             # Global framework manual
```

---

## 📜 Coding Conventions & Naming Standards

To maintain a clean and standardized codebase, developers must adhere to the following rules:
- **PEP 8 Compliance**: Follow standard Python conventions (snake_case for variables/functions, PascalCase for classes).
- **Comment Style**: **Do NOT use `//` comments anywhere** in Python files. Use standard Python `#` comments or multi-line docstrings (`"""`).
- **Data Isolation**: Never use static names for creating test records. Always use `generate_random_name("auto_*")` or similar from the `random_data` utility.
- **Credential Protection**: Hardcoded credentials must not be committed to Git. All secrets must reside in the local, untracked `.env` file.

---

## ⚙️ Setup & Execution

### 1. Installation
Install python dependencies and download Playwright browser binaries:
```bash
pip install -r requirements.txt
playwright install
```

### 2. Configure Local Credentials
Create a `.env` file in the project root:
```env
ADMIN_EMAIL=your_email@domain.com
ADMIN_PASSWORD=your_secure_password
```

### 3. Running Tests
Run the entire Master Menu suite:
```bash
python -m pytest tests/master_menu/
```

Run a specific test in headed mode with visual slowdown:
```bash
python -m pytest tests/master_menu/test_account_groups.py --headed --slowmo 400
```