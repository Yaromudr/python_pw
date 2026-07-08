import allure
from playwright.sync_api import expect

from pages.base_page import BasePage
from pages.inventory_page import InventoryPage


class LoginPage(BasePage):
    path = "/"

    def __init__(self, page):
        super().__init__(page)
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator('[data-test="error"]')

    @allure.step("Авторизоваться под пользователем {username}")
    def login(self, username: str, password: str) -> InventoryPage:
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        return InventoryPage(self.page)

    @allure.step("Проверить сообщение об ошибке: {text}")
    def expect_error(self, text: str) -> None:
        expect(self.error_message).to_contain_text(text)
