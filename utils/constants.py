import os

env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
if os.path.exists(env_path):
    with open(env_path, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ[key.strip()] = val.strip().strip('"').strip("'")

BASE_URL = os.getenv("BASE_URL", "https://dev-demo-ccl.devccl-billzweb.crystalbillz.com")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

DASHBOARD_URL = f"{BASE_URL}/dashboard"
CITY_URL = f"{BASE_URL}/cities"
BRANCHES_URL = f"{BASE_URL}/branches"
ROLES_URL = f"{BASE_URL}/roles"
USERS_URL = f"{BASE_URL}/users"
CUSTOMERS_URL = f"{BASE_URL}/customers"

CATEGORIES_URL = f"{BASE_URL}/categories"
BRANDS_URL = f"{BASE_URL}/brands"
UNIT_TYPES_URL = f"{BASE_URL}/unit-types"
ATTRIBUTE_KEYS_URL = f"{BASE_URL}/attribute-keys"
ATTRIBUTE_VALUES_URL = f"{BASE_URL}/attribute-values"
PRODUCT_ATTRIBUTES_URL = f"{BASE_URL}/product-unit-attributes"
BANK_ACCOUNTS_URL = f"{BASE_URL}/bank-accounts"
ENQUIRY_STAGE_WORKFLOWS_URL = f"{BASE_URL}/enquiry-stage-workflows"
ACCOUNT_GROUPS_URL = f"{BASE_URL}/account-groups"
EXPENSE_CATEGORIES_URL = f"{BASE_URL}/expense-categories"
ENQUIRY_TYPES_URL = f"{BASE_URL}/enquiry-types"
SAC_HSN_URL = f"{BASE_URL}/gst-codes"
RACKS_URL = f"{BASE_URL}/racks"
PRODUCTS_URL = f"{BASE_URL}/products"
SUPPLIERS_URL = f"{BASE_URL}/suppliers"
PURCHASE_REQUESTS_URL = f"{BASE_URL}/purchase-requests"