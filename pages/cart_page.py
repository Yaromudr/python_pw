import re
from typing import Sequence

import allure
from playwright.sync_api import expect

from pages.base_page import BasePage
from pages.checkout_page import CheckoutInfoPage


class CartPage(BasePage):
    path = "/cart.html"

    def __init__(self, page):
        super().__init__(page)
        self.item_names = page.locator('[data-test="inventory-item-name"]')
        self.checkout_button = page.locator('[data-test="checkout"]')

    @allure.step("Проверить, что открыта страница корзины")
    def expect_loaded(self) -> None:
        expect(self.page).to_have_url(re.compile(r"/cart\.html$"))

    @allure.step("Проверить, что товар «{name}» в корзине")
    def expect_item_in_cart(self, name: str) -> None:
        expect(self.item_names.get_by_text(name, exact=True)).to_be_visible()

    @allure.step("Проверить состав корзины: {names}")
    def expect_items_in_cart(self, names: Sequence[str]) -> None:
        expect(self.item_names).to_have_count(len(names))
        for name in names:
            self.expect_item_in_cart(name)

    @allure.step("Перейти к оформлению заказа")
    def checkout(self) -> CheckoutInfoPage:
        self.checkout_button.click()
        return CheckoutInfoPage(self.page)
