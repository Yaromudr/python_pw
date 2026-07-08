import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


def _bool(value: str) -> bool:
    return value.strip().lower() in ("1", "true", "yes", "on")


@dataclass(frozen=True)
class Settings:
    base_url: str = os.getenv("BASE_URL", "")

    # chromium | firefox | webkit
    browser_engine: str = os.getenv("BROWSER_ENGINE", "chromium")

    # chrome | msedge | "" (пусто - встроенный Chromium вместо реального Chrome)
    browser_channel: str = os.getenv("BROWSER_CHANNEL", "chrome")

    headless: bool = _bool(os.getenv("HEADLESS", "true"))
    slow_mo: int = int(os.getenv("SLOW_MO", "0"))

    viewport_width: int = int(os.getenv("VIEWPORT_WIDTH", "1920"))
    viewport_height: int = int(os.getenv("VIEWPORT_HEIGHT", "1080"))

    default_timeout: int = int(os.getenv("DEFAULT_TIMEOUT", "15000"))

    login: str = os.getenv("LOGIN", "")
    password: str = os.getenv("PASSWORD", "")

    # Названия товаров через запятую — используются в тестах корзины/заказа
    products: tuple = tuple(
        name.strip()
        for name in os.getenv("PRODUCTS", "Sauce Labs Backpack,Sauce Labs Bike Light").split(",")
        if name.strip()
    )


settings = Settings()
