from utils.constants import ENQUIRY_STAGE_WORKFLOWS_URL

VOUCHER_TYPES_URL = ENQUIRY_STAGE_WORKFLOWS_URL.replace("enquiry-stage-workflows", "voucher-types")

class VoucherTypesPage:
    def __init__(self, page):
        self.page = page
        self.voucher_types_url = VOUCHER_TYPES_URL

    def navigate(self):
        return self.page.goto(self.voucher_types_url)

    def is_voucher_types_visible(self):
        try:
            self.page.get_by_text("Payment Voucher").first.wait_for(state="visible", timeout=3000)
            return True
        except Exception:
            return False

    def edit_voucher_type(self, name, new_prefix):
        row = self.page.locator("tr", has=self.page.get_by_text(name, exact=True))
        row.wait_for(state="visible", timeout=5000)

        row.get_by_title("edit").click()
        modal = self.page.get_by_role("dialog")
        modal.wait_for(state="visible", timeout=5000)
        modal.locator(".spinner-border").wait_for(state="hidden", timeout=10000)

        modal.locator("input[name=\"prefix\"]").fill(new_prefix)
        modal.get_by_role("button", name="Save").click()

        toast = self.page.get_by_text("successfully").first
        try:
            toast.wait_for(state="visible", timeout=5000)
            modal.wait_for(state="hidden", timeout=5000)
            return True
        except Exception:
            return False
