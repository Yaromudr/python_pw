from playwright.sync_api import Page

from config.settings import settings
from pages.login_page import LoginPage


def test_successful_login(page: Page):
    login_page = LoginPage(page).open()

    inventory_page = login_page.login(settings.login, settings.password)

    inventory_page.expect_loaded()
