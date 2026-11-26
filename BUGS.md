# Known bugs: saucedemo.com
Found by exploratory testing, compared against `standard_user` as the reference.
Each bug has an automated xfail test in `tests/ui/test_known_bugs.py`.

| ID | Title | User | Severity |
|----|-------|------|----------|
| BUG-001 | All products show the same image | problem_user | Medium |
| BUG-002 | Sorting Name (Z to A) does nothing | problem_user | Medium |
| BUG-003 | "Add to cart" does nothing for some products | problem_user | High |
| BUG-004 | "Remove" on the products page does not remove the item | problem_user | Medium |
| BUG-005 | Product name link opens a different product | problem_user | High |
| BUG-006 | Typing the last name overwrites the first name in checkout | problem_user | Critical |
| BUG-007 | "Finish" does not complete the order | error_user | Critical |
| BUG-008 | Product prices differ from the real ones | visual_user | High |

**Environment for all bugs:** saucedemo.com, Chrome [your version], Windows 11; automated tests run in Chromium through Playwright. Password for every user: `secret_sauce`.

## BUG-001: All products show the same image
- **Severity:** Medium (products cannot be told apart by picture; no data loss)
- **User:** `problem_user`
- **Steps to reproduce:**
  1. Open https://www.saucedemo.com
  2. Log in as `problem_user`
  3. Look at the product images on the Products page
- **Expected result:** each product shows its own image, as for `standard_user`
- **Actual result:** all 6 products show the same image (a dog picture)
- **Evidence:** `docs/bug-001.png`; test `test_bug001_each_product_has_its_own_image` (xfail)

## BUG-002: Sorting Name (Z to A) does nothing
- **Severity:** Medium (the catalogue can still be browsed; only the ordering is wrong)
- **User:** `problem_user`
- **Steps to reproduce:**
  1. Log in as `problem_user`
  2. Open the sort menu in the top-right corner of the Products page
  3. Select "Name (Z to A)"
- **Expected result:** products are listed in reverse alphabetical order, starting with "Test.allTheThings() T-Shirt (Red)"
- **Actual result:** the order stays A to Z; the price sort options do not reorder the list either
- **Evidence:** `docs/bug-002.png`; test `test_bug002_sort_name_z_to_a` (xfail)

## BUG-003: "Add to cart" does nothing for some products
- **Severity:** High (three products cannot be bought at all)
- **User:** `problem_user`
- **Steps to reproduce:**
  1. Log in as `problem_user`
  2. Click "Add to cart" on each of the 6 products, one at a time
  3. Watch the number on the cart icon after every click
- **Expected result:** the cart count goes up by 1 after each click (1, 2, 3, 4, 5, 6)
- **Actual result:** the count goes 1, 2, 2, 2, 3, 3; "Sauce Labs Bolt T-Shirt", "Sauce Labs Fleece Jacket" and "Test.allTheThings() T-Shirt (Red)" are never added
- **Evidence:** `docs/bug-003.png`; test `test_bug003_add_to_cart_works_for_every_product` (xfail)

## BUG-004: "Remove" on the products page does not remove the item
- **Severity:** Medium (workaround: the item can still be removed from the Cart page)
- **User:** `problem_user`
- **Steps to reproduce:**
  1. Log in as `problem_user`
  2. Add "Sauce Labs Backpack" and "Sauce Labs Bike Light" to the cart (the cart shows 2)
  3. On the Products page, click "Remove" under "Sauce Labs Backpack"
- **Expected result:** the cart count drops to 1
- **Actual result:** the cart count stays at 2 and the backpack remains in the cart
- **Evidence:** `docs/bug-004.png`; test `test_bug004_remove_from_products_page` (xfail)

## BUG-005: Product name link opens a different product
- **Severity:** High (the user can end up buying a product they did not choose)
- **User:** `problem_user`
- **Steps to reproduce:**
  1. Log in as `problem_user`
  2. Click the name "Sauce Labs Backpack" on the Products page
- **Expected result:** the details page of "Sauce Labs Backpack" opens
- **Actual result:** the details page of "Sauce Labs Fleece Jacket" opens instead
- **Evidence:** `docs/bug-005.png`; test `test_bug005_product_link_opens_the_right_product` (xfail)

## BUG-006: Typing the last name overwrites the first name in checkout
- **Severity:** Critical (the order cannot be placed)
- **User:** `problem_user`
- **Steps to reproduce:**
  1. Log in as `problem_user` and add "Sauce Labs Backpack" to the cart
  2. Open the cart and click "Checkout"
  3. Type "Ana" in First Name, then type "Pop" in Last Name, one letter at a time
  4. Click "Continue"
- **Expected result:** First Name shows "Ana", Last Name shows "Pop", and the overview page opens
- **Actual result:** each letter typed in Last Name replaces the First Name field, which ends up as "p"; Last Name stays empty, so "Continue" shows "Error: Last Name is required"
- **Evidence:** `docs/bug-006.png`; test `test_bug006_checkout_form_keeps_both_names` (xfail)

## BUG-007: "Finish" does not complete the order
- **Severity:** Critical (the purchase can never be completed)
- **User:** `error_user`
- **Steps to reproduce:**
  1. Log in as `error_user` and add "Sauce Labs Backpack" to the cart
  2. Open the cart, click "Checkout", fill in First Name, Last Name and Zip Code, click "Continue"
  3. On the overview page, click "Finish"
- **Expected result:** the "Thank you for your order!" page opens (`checkout-complete.html`)
- **Actual result:** nothing happens; the user stays on the overview page (`checkout-step-two.html`)
- **Evidence:** `docs/bug-007.png`; test `test_bug007_finish_completes_order` (xfail)

## BUG-008: Product prices differ from the real ones
- **Severity:** High (the customer sees a wrong price before buying)
- **User:** `visual_user`
- **Steps to reproduce:**
  1. Log in as `standard_user` and note the prices: $29.99, $9.99, $15.99, $49.99, $7.99, $15.99 (default A to Z order)
  2. Log out, log in as `visual_user` and compare the prices on the Products page
  3. Refresh the page and compare again
- **Expected result:** the same prices as for `standard_user`
- **Actual result:** the prices are different, and they change again after every refresh
- **Evidence:** `docs/bug-008.png`; test `test_bug008_prices_match_catalogue` (xfail)
