import random
import pytest
from pages.master_menu.bank_accounts_page import BankAccountPage
from utils.random_data import generate_random_name

@pytest.fixture
def bank_account_cleanup(logged_in_page):
    created_accounts = []
    yield created_accounts
    bank_page = BankAccountPage(logged_in_page)
    for name in created_accounts:
        try:
            bank_page.navigate()
            if bank_page.search_bank_account(name):
                row = bank_page.page.locator("tr", has=bank_page.page.get_by_text(name, exact=True))
                if row.get_by_title("delete").first.is_visible():
                    bank_page.delete_bank_account(name)
        except Exception as e:
            print(f"Teardown: Failed to delete bank account {name}: {e}")

def test_bank_accounts_visibility(logged_in_page):
    page_obj = BankAccountPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    assert page_obj.is_bank_account_visible()

def test_add_bank_account(logged_in_page, bank_account_cleanup):
    page_obj = BankAccountPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    
    bank_name = generate_random_name("bank")
    branch = generate_random_name("branch")
    acc_num = str(random.randint(100000000000, 999999999999))
    ifsc = "IDFC0000899"
    
    page_obj.add_bank_account(bank_name, branch, acc_num, ifsc)
    bank_account_cleanup.append(bank_name)
    assert page_obj.search_bank_account(bank_name)

def test_search_bank_account(logged_in_page, bank_account_cleanup):
    page_obj = BankAccountPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    
    bank_name = generate_random_name("bank")
    branch = generate_random_name("branch")
    acc_num = str(random.randint(100000000000, 999999999999))
    ifsc = "IDFC0000899"
    
    page_obj.add_bank_account(bank_name, branch, acc_num, ifsc)
    bank_account_cleanup.append(bank_name)
    assert page_obj.search_bank_account(bank_name)

def test_view_bank_account(logged_in_page, bank_account_cleanup):
    page_obj = BankAccountPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    
    bank_name = generate_random_name("bank")
    branch = generate_random_name("branch")
    acc_num = str(random.randint(100000000000, 999999999999))
    ifsc = "IDFC0000899"
    
    page_obj.add_bank_account(bank_name, branch, acc_num, ifsc)
    bank_account_cleanup.append(bank_name)
    assert page_obj.search_bank_account(bank_name)
    assert page_obj.view_bank_account(bank_name)

def test_edit_bank_account(logged_in_page, bank_account_cleanup):
    page_obj = BankAccountPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    
    bank_name = generate_random_name("bank")
    branch = generate_random_name("branch")
    acc_num = str(random.randint(100000000000, 999999999999))
    ifsc = "IDFC0000899"
    
    page_obj.add_bank_account(bank_name, branch, acc_num, ifsc)
    bank_account_cleanup.append(bank_name)
    assert page_obj.search_bank_account(bank_name)
    
    new_name = generate_random_name("bank1")
    bank_account_cleanup.append(new_name)
    assert page_obj.edit_bank_account(bank_name, new_name)
    assert page_obj.search_bank_account(new_name)

def test_delete_bank_account(logged_in_page, bank_account_cleanup):
    page_obj = BankAccountPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    
    bank_name = generate_random_name("bank")
    branch = generate_random_name("branch")
    acc_num = str(random.randint(100000000000, 999999999999))
    ifsc = "IDFC0000899"
    
    page_obj.add_bank_account(bank_name, branch, acc_num, ifsc)
    bank_account_cleanup.append(bank_name)
    assert page_obj.search_bank_account(bank_name)
    assert page_obj.delete_bank_account(bank_name)

def test_retrieve_bank_account(logged_in_page, bank_account_cleanup):
    page_obj = BankAccountPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    
    bank_name = generate_random_name("bank")
    branch = generate_random_name("branch")
    acc_num = str(random.randint(100000000000, 999999999999))
    ifsc = "IDFC0000899"
    
    page_obj.add_bank_account(bank_name, branch, acc_num, ifsc)
    bank_account_cleanup.append(bank_name)
    assert page_obj.search_bank_account(bank_name)
    assert page_obj.delete_bank_account(bank_name)
    assert page_obj.retrieve_bank_account(bank_name)
    assert page_obj.search_bank_account(bank_name)

def test_validate_bank_account(logged_in_page):
    page_obj = BankAccountPage(logged_in_page)
    page_obj.navigate()
    logged_in_page.wait_for_load_state("networkidle")
    assert page_obj.validate_required_fields()
