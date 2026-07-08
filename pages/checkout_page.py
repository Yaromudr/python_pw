import re

import allure
from playwright.sync_api import expect

from pages.base_page import BasePage


class CheckoutInfoPage(BasePage):
    """Шаг 1: данные покупателя (checkout-step-one.html)."""

    path = "/checkout-step-one.html"

    def __init__(self, page):
        super().__init__(page)
        self.first_name_input = page.locator('[data-test="firstName"]')
        self.last_name_input = page.locator('[data-test="lastName"]')
        self.postal_code_input = page.locator('[data-test="postalCode"]')
        self.continue_button = page.locator('[data-test="continue"]')

    @allure.step("Заполнить данные покупателя: {first_name} {last_name}, индекс {postal_code}")
    def fill_info(self, first_name: str, last_name: str, postal_code: str) -> "CheckoutInfoPage":
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)
        return self

    @allure.step("Перейти к сводке заказа")
    def continue_to_overview(self) -> "CheckoutOverviewPage":
        self.continue_button.click()
        return CheckoutOverviewPage(self.page)


class CheckoutOverviewPage(BasePage):
    """Шаг 2: итоговая сводка заказа (checkout-step-two.html)."""

    path = "/checkout-step-two.html"

    def __init__(self, page):
        super().__init__(page)
        self.total_label = page.locator('[data-test="total-label"]')
        self.finish_button = page.locator('[data-test="finish"]')

    @allure.step("Проверить, что открыта сводка заказа")
    def expect_loaded(self) -> None:
        expect(self.page).to_have_url(re.compile(r"/checkout-step-two\.html$"))

    @allure.step("Подтвердить заказ")
    def finish(self) -> "CheckoutCompletePage":
        self.finish_button.click()
        return CheckoutCompletePage(self.page)


class CheckoutCompletePage(BasePage):
    """Шаг 3: подтверждение заказа (checkout-complete.html)."""

    path = "/checkout-complete.html"

    def __init__(self, page):
        super().__init__(page)
        self.complete_header = page.locator('[data-test="complete-header"]')

    @allure.step("Проверить, что заказ оформлен")
    def expect_order_completed(self) -> None:
        expect(self.page).to_have_url(re.compile(r"/checkout-complete\.html$"))
        expect(self.complete_header).to_have_text("Thank you for your order!")
