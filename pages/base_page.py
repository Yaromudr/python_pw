import allure
from playwright.sync_api import Page, expect


class BasePage:
    """Базовый класс для Page Object'ов."""

    path: str = "/"

    def __init__(self, page: Page):
        self.page = page
        self.cart_badge = page.locator('[data-test="shopping-cart-badge"]')
        self.cart_link = page.locator('[data-test="shopping-cart-link"]')

    def open(self) -> "BasePage":
        with allure.step(f"Открыть страницу {self.path}"):
            self.page.goto(self.path)
        return self

    def title(self) -> str:
        return self.page.title()

    def url(self) -> str:
        return self.page.url

    @allure.step("Проверить количество товаров в корзине: {count}")
    def expect_cart_count(self, count: int) -> None:
        expect(self.cart_badge).to_have_text(str(count))

    @allure.step("Перейти в корзину")
    def open_cart(self) -> "CartPage":
        from pages.cart_page import CartPage

        self.cart_link.click()
        return CartPage(self.page)
