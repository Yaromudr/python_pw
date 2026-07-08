from playwright.sync_api import Page

from config.settings import settings
from pages.login_page import LoginPage


def test_checkout_completes_order(page: Page):
    login_page = LoginPage(page).open()
    inventory_page = login_page.login(settings.login, settings.password)
    inventory_page.expect_loaded()

    inventory_page = inventory_page.add_products_to_cart(settings.products)
    inventory_page.expect_cart_count(len(settings.products))

    cart_page = inventory_page.open_cart()
    cart_page.expect_loaded()
    cart_page.expect_items_in_cart(settings.products)

    checkout_info_page = cart_page.checkout()
    checkout_overview_page = checkout_info_page.fill_info(
        "John", "Doe", "12345"
    ).continue_to_overview()
    checkout_overview_page.expect_loaded()

    checkout_complete_page = checkout_overview_page.finish()
    checkout_complete_page.expect_order_completed()
