from __future__ import annotations

from playwright.sync_api import Page

from utils.constants import ENQUIRY_STAGE_WORKFLOWS_URL

class EnquiryStageWorkflowsPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.url = ENQUIRY_STAGE_WORKFLOWS_URL

    def navigate(self) -> None:
        self.page.goto(self.url)

    def is_workflows_visible(self) -> bool:
        return self.page.get_by_role("button", name="Add Workflow").is_visible()

    def add_workflow(self, workflow_name: str, workflow_type: str = "Enquiry Type Override", trigger_name: str = "auto_mate1") -> None:
        self.page.get_by_role("button", name="Add Workflow").click()
        
        # Select workflow type
        self.page.locator(".react-select__input-container").first.click()
        self.page.get_by_role("option", name=workflow_type).click()
        
        # Select trigger name / override option
        self.page.locator(".react-select__input-container").nth(1).click()
        self.page.get_by_role("option", name=trigger_name).click()
        
        # Fill workflow name
        self.page.locator("input[name=\"workflow_name\"]").fill(workflow_name)
        self.page.get_by_role("button", name="Create").click()
        
        # Wait for list page load/toast/etc if needed, or wait for load state
        self.page.wait_for_load_state("networkidle")

    def search_workflow(self, name: str) -> bool:
        search_box = self.page.get_by_role("textbox", name="Search workflows...")
        search_box.fill(name)
        search_box.press("Enter")
        self.page.wait_for_load_state("networkidle", timeout=5000)
        locator = self.page.get_by_text(name, exact=True).first
        try:
            locator.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False

    def edit_workflow_name(self, old_name: str, new_name: str) -> None:
        self.search_workflow(old_name)
        row = self.page.locator("tr", has=self.page.get_by_text(old_name, exact=True))
        row.wait_for(state="visible", timeout=5000)
        
        row.get_by_title("manage").click()
        self.page.get_by_role("button", name="Edit Workflow").click()
        
        textbox = self.page.get_by_role("textbox")
        textbox.wait_for(state="visible", timeout=5000)
        textbox.fill(new_name)
        
        self.page.get_by_role("button", name="Update").click()
        self.page.get_by_role("link", name="Back to Workflows").click()
        self.page.wait_for_load_state("networkidle")

    def edit_workflow_active(self, name: str, active: bool = True) -> bool:
        self.search_workflow(name)
        row = self.page.locator("tr", has=self.page.get_by_text(name, exact=True))
        row.wait_for(state="visible", timeout=5000)
        
        row.get_by_title("edit").first.click()
        
        checkbox = self.page.get_by_role("checkbox", name="Active")
        checkbox.wait_for(state="visible", timeout=5000)
        if active:
            checkbox.check()
        else:
            checkbox.uncheck()
            
        self.page.get_by_role("button", name="Update").click()
        
        toast = self.page.get_by_text("Enquiry stage workflow updated successfully")
        try:
            toast.wait_for(state="visible", timeout=5000)
            # wait for toast to be gone or click it
            toast.click()
            return True
        except Exception:
            return False

    def delete_workflow(self, name: str) -> bool:
        self.search_workflow(name)
        row = self.page.locator("tr", has=self.page.get_by_text(name, exact=True))
        row.wait_for(state="visible", timeout=5000)
        
        row.get_by_title("delete").first.click()
        self.page.get_by_role("button", name="Delete Workflow").click()
        
        toast = self.page.get_by_text("Deleted successfully.")
        try:
            toast.wait_for(state="visible", timeout=5000)
            toast.click()
            return True
        except Exception:
            return False

    def restore_workflow(self, name: str) -> bool:
        self.search_workflow(name)
        row = self.page.locator("tr", has=self.page.get_by_text(name, exact=True))
        row.wait_for(state="visible", timeout=5000)
        
        row.get_by_title("delete").first.click()
        self.page.get_by_role("button", name="Restore Workflow").click()
        
        toast = self.page.get_by_text("Retrieved successfully.")
        try:
            toast.wait_for(state="visible", timeout=5000)
            toast.click()
            return True
        except Exception:
            return False
