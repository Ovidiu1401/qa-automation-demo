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
    inventory = InventoryPage(page)
    # Wait until all 6 products are on the page, otherwise we may read an empty list
    expect(inventory.items).to_have_count(6)
    return inventory

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
    
    
#5
@pytest.mark.ui
@pytest.mark.xfail(reason="BUG-005: product name link opens a different product", strict=True)
def test_bug005_product_link_opens_the_right_product(page):
    login_as(page, "problem_user")
    page.get_by_text("Sauce Labs Backpack", exact=True).click()
    expect(page.locator(".inventory_details_name")).to_have_text("Sauce Labs Backpack", timeout=2000)
    
    

#6
@pytest.mark.ui
@pytest.mark.xfail(reason="BUG-006: typing the last name overwrites the first name in checkout",
strict=True)
def test_bug006_checkout_form_keeps_both_names(page):
    inventory = login_as(page, "problem_user")
    inventory.add_to_cart("sauce-labs-backpack")
    page.goto("/checkout-step-one.html")
    page.locator("[data-test='firstName']").press_sequentially("Ana")
    page.locator("[data-test='lastName']").press_sequentially("Pop")
    expect(page.locator("[data-test='firstName']")).to_have_value("Ana", timeout=2000)
    expect(page.locator("[data-test='lastName']")).to_have_value("Pop", timeout=2000)
    
    
    
#7
@pytest.mark.ui
@pytest.mark.xfail(reason="BUG-007: 'Finish' does not complete the order for error_user", strict=True)
def test_bug007_finish_completes_order(page):
    inventory = login_as(page, "error_user")
    inventory.add_to_cart("sauce-labs-backpack")
    page.goto("/checkout-step-one.html")
    page.locator("[data-test='firstName']").fill("Ana")
    page.locator("[data-test='lastName']").fill("Pop")
    page.locator("[data-test='postalCode']").fill("012345")
    page.click("[data-test='continue']")
    page.click("[data-test='finish']")
    expect(page).to_have_url("https://www.saucedemo.com/checkout-complete.html", timeout=2000)
    
    
    
#8
@pytest.mark.ui
@pytest.mark.xfail(reason="BUG-008: visual_user sees prices that differ from the real ones",
strict=True)
def test_bug008_prices_match_catalogue(page):
    login_as(page, "visual_user")
    assert page.locator(".inventory_item_price").all_inner_texts() == STANDARD_PRICES
    
    
    
@pytest.mark.ui
def test_control_standard_user_has_none_of_these_bugs(page):
    inventory = login_as(page, "standard_user")
    sources = page.locator(".inventory_item img").evaluate_all("imgs => imgs.map(i => i.getAttribute('src'))")
    assert len(set(sources)) == 6
    assert page.locator(".inventory_item_price").all_inner_texts() == STANDARD_PRICES
    inventory.add_to_cart("sauce-labs-backpack")
    inventory.add_to_cart("sauce-labs-bolt-t-shirt")
    expect(inventory.cart_badge).to_have_text("2")
    inventory.remove_from_cart("sauce-labs-backpack")
    expect(inventory.cart_badge).to_have_text("1")
    page.select_option("[data-test='product-sort-container']", "za")
    names = page.locator(".inventory_item_name").all_inner_texts()
    assert names == sorted(names, reverse=True)