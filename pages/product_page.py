import re

import allure
from playwright.sync_api import expect

from pages.base_page import BasePage


class ProductPage(BasePage):
    """Карточка товара с полным описанием (inventory-item.html)."""

    def __init__(self, page):
        super().__init__(page)
        self.product_name = page.locator('[data-test="inventory-item-name"]')
        self.add_to_cart_button = page.locator('[data-test="add-to-cart"]')
        self.back_to_products_button = page.locator('[data-test="back-to-products"]')

    @allure.step("Проверить, что открыта карточка товара «{name}»")
    def expect_loaded(self, name: str) -> None:
        expect(self.page).to_have_url(re.compile(r"/inventory-item\.html"))
        expect(self.product_name).to_have_text(name)

    @allure.step("Добавить товар в корзину")
    def add_to_cart(self) -> "ProductPage":
        self.add_to_cart_button.click()
        return self

    @allure.step("Вернуться в каталог товаров")
    def back_to_products(self):
        from pages.inventory_page import InventoryPage

        self.back_to_products_button.click()
        return InventoryPage(self.page)
