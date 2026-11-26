import re
import pytest
from playwright.sync_api import expect
from pages.login_page import LoginPage

PASSWORD = "secret_sauce"

@pytest.mark.ui
def test_login_valid(page):
    login = LoginPage(page)
    login.open()
    login.login("standard_user", PASSWORD)
    expect(page).to_have_url(re.compile(r".*/inventory\.html"))

@pytest.mark.ui
def test_login_locked_out_user(page):
    login = LoginPage(page)
    login.open()
    login.login("locked_out_user", PASSWORD)
    expect(login.error).to_contain_text("locked out")

@pytest.mark.ui
@pytest.mark.parametrize("user, password", [
    ("standard_user", "wrong"),
    ("", PASSWORD),
    ("nobody", "nothing"),
])
def test_login_invalid(page, user, password):
    login = LoginPage(page)
    login.open()
    login.login(user, password)
    expect(login.error).to_be_visible()