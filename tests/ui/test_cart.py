import pytest
from playwright.sync_api import Page

from config.settings import settings
from pages.login_page import LoginPage


@pytest.mark.parametrize("product_name", settings.products)
def test_add_product_to_cart_from_details_page(page: Page, product_name: str):
    login_page = LoginPage(page).open()
    inventory_page = login_page.login(settings.login, settings.password)
    inventory_page.expect_loaded()

    product_page = inventory_page.open_product(product_name)
    product_page.expect_loaded(product_name)

    product_page.add_to_cart()

    product_page.expect_cart_count(1)
