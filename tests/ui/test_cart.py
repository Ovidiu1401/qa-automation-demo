import pytest
from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

@pytest.fixture
def logged_in(page):
    login = LoginPage(page)
    login.open()
    login.login("standard_user", "secret_sauce")
    return InventoryPage(page)

@pytest.mark.ui
def test_inventory_shows_products(logged_in):
    expect(logged_in.items).to_have_count(6)

@pytest.mark.ui
def test_add_and_remove_from_cart(logged_in):
    logged_in.add_to_cart("sauce-labs-backpack")
    expect(logged_in.cart_badge).to_have_text("1")
    logged_in.remove_from_cart("sauce-labs-backpack")
    expect(logged_in.cart_badge).to_have_count(0)