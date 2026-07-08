import re
from typing import Sequence

import allure
from playwright.sync_api import expect

from pages.base_page import BasePage
from pages.product_page import ProductPage


class InventoryPage(BasePage):
    path = "/inventory.html"

    def __init__(self, page):
        super().__init__(page)
        self.page_title = page.locator(".title")
        self.inventory_list = page.locator(".inventory_list")
        self.item_names = page.locator(".inventory_item_name")

    @allure.step("Проверить, что каталог товаров загружен")
    def expect_loaded(self) -> None:
        expect(self.page).to_have_url(re.compile(r"/inventory\.html$"))
        expect(self.page_title).to_have_text("Products")
        expect(self.inventory_list).to_be_visible()

    @allure.step("Открыть карточку товара «{name}»")
    def open_product(self, name: str) -> ProductPage:
        self.item_names.get_by_text(name, exact=True).click()
        return ProductPage(self.page)

    @allure.step("Добавить в корзину товары через их карточки: {names}")
    def add_products_to_cart(self, names: Sequence[str]) -> "InventoryPage":
        inventory_page = self
        for name in names:
            product_page = inventory_page.open_product(name)
            product_page.expect_loaded(name)
            product_page.add_to_cart()
            inventory_page = product_page.back_to_products()
        return inventory_page
