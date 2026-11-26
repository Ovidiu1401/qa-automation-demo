from tkinter.font import names

import pytest
from playwright.sync_api import expect
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage 


PASSWORD = "secret_sauce"
STANDARD_PRICES = ["$29.99", "$9.99", "$15.99", "$49.99", "$7.99", "$15.99"]

def login_as(page, user):
    login = LoginPage(page)
    login.open()
    login.login(user, PASSWORD)
    return InventoryPage(page)

#1
@pytest.mark.ui
@pytest.mark.xfail(reason="BUG-001: all products show the same image", strict=True)
def test_bug001_each_product_has_its_own_image(page):
    login_as(page, "problem_user")
    sources = page.locator(".inventory_item img").evaluate_all("imgs => imgs.map(i => i.getAttribute('src'))")
    assert len(set(sources)) == 6, f"distinct images: {set(sources)}"
    


#2
@pytest.mark.ui
@pytest.mark.xfail(reason="BUG-002: sorting Name (Z to A) does nothing", strict=True)
def test_bug002_sort_name_z_to_a(page):
    login_as(page, "problem_user")
    page.select_option("[data-test='product-sort-container']", "za")
    names = page.locator(".inventory_item_name").all_inner_texts()
    assert names == sorted(names, reverse=True)
    
    
#3
@pytest.mark.ui
@pytest.mark.xfail(reason="BUG-003: 'Add to cart' does nothing for some products", strict=True)
def test_bug003_add_to_cart_works_for_every_product(page):
    inventory = login_as(page, "problem_user")
    for product in ["sauce-labs-backpack", "sauce-labs-bolt-t-shirt"]:
        inventory.add_to_cart(product)
    expect(inventory.cart_badge).to_have_text("2", timeout=2000)
    
    
#4
@pytest.mark.ui
@pytest.mark.xfail(reason="BUG-004: 'Remove' on the products page does not remove the item",
strict=True)
def test_bug004_remove_from_products_page(page):
    inventory = login_as(page, "problem_user")
    inventory.add_to_cart("sauce-labs-backpack")
    inventory.add_to_cart("sauce-labs-bike-light")
    inventory.remove_from_cart("sauce-labs-backpack")
    expect(inventory.cart_badge).to_have_text("1", timeout=2000)