from utils.constants import DASHBOARD_URL
class DashboardPage:
    def __init__(self, page):
        self.page = page
        self.dashboard_url = DASHBOARD_URL
        
    def navigate(self):
        return self.page.goto(self.dashboard_url)
    
    def status(self):
        return self.page.evaluate("() => document.readyState === 'complete' ? 200 : 500")
    
    def is_dashboard_visible(self):
        return self.page.get_by_role("heading", name="Dashboard").is_visible()
