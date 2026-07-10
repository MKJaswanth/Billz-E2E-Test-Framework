import os

# Load .env file manually if exists to configure local runs
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

DASHBOARD_URL = "https://dev-demo-ccl.devccl-billzweb.crystalbillz.com/dashboard"
CITY_URL = "https://dev-demo-ccl.devccl-billzweb.crystalbillz.com/cities"
BRANCHES_URL = "https://dev-demo-ccl.devccl-billzweb.crystalbillz.com/branches"
ROLES_URL = "https://dev-demo-ccl.devccl-billzweb.crystalbillz.com/roles"
USERS_URL = "https://dev-demo-ccl.devccl-billzweb.crystalbillz.com/users"

CATEGORIES_URL = "https://dev-demo-ccl.devccl-billzweb.crystalbillz.com/categories"
BRANDS_URL = "https://dev-demo-ccl.devccl-billzweb.crystalbillz.com/brands"
UNIT_TYPES_URL = "https://dev-demo-ccl.devccl-billzweb.crystalbillz.com/unit-types"
ATTRIBUTE_KEYS_URL = "https://dev-demo-ccl.devccl-billzweb.crystalbillz.com/attribute-keys"
ATTRIBUTE_VALUES_URL = "https://dev-demo-ccl.devccl-billzweb.crystalbillz.com/attribute-values"
PRODUCT_ATTRIBUTES_URL = "https://dev-demo-ccl.devccl-billzweb.crystalbillz.com/product-unit-attributes"
BANK_ACCOUNTS_URL = "https://dev-demo-ccl.devccl-billzweb.crystalbillz.com/bank-accounts"
ENQUIRY_STAGE_WORKFLOWS_URL = "https://dev-demo-ccl.devccl-billzweb.crystalbillz.com/enquiry-stage-workflows"
ACCOUNT_GROUPS_URL = "https://dev-demo-ccl.devccl-billzweb.crystalbillz.com/account-groups"
  