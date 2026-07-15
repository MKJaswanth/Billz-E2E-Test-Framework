import re
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(storage_state="auth_state.json")
    page = context.new_page()
    page.goto("https://testing001.devccl-billzweb.crystalbillz.com/sales")
    page.wait_for_timeout(3000)
    
    print("URL:", page.url)
    
    # Locate all action elements/titles in the table
    rows = page.locator("table tbody tr").all()
    print(f"Total rows found: {len(rows)}")
    if len(rows) > 0:
        first_row = rows[0]
        text_safe = first_row.text_content().strip().encode('ascii', 'ignore').decode('ascii')
        print("First row text:", text_safe)
        
        # Check all child buttons and links in the first row
        children = first_row.locator("a, button, [title]").all()
        for idx, child in enumerate(children):
            tag = child.evaluate("el => el.tagName")
            title = child.get_attribute("title") or ""
            title_safe = title.encode('ascii', 'ignore').decode('ascii')
            text = child.text_content().strip()
            text_safe = text.encode('ascii', 'ignore').decode('ascii')
            print(f"Action {idx}: tag={tag}, title={title_safe}, text={text_safe}")
            
    browser.close()
