import shutil
import sys
from pathlib import Path

import allure
import pytest

from config.settings import settings

ALLURE_RESULTS_DIR = Path("allure-results")


def pytest_configure(config: pytest.Config) -> None:
    """Позволяет управлять движком браузера через .env (BROWSER_ENGINE),
    если он не передан явно флагом --browser в командной строке."""
    if "--browser" not in " ".join(sys.argv):
        config.option.browser = [settings.browser_engine]

    # Чистим allure-results сами, а не флагом --clean-alluredir: под pytest-xdist
    # pytest_configure вызывается в каждом воркере, а allure-pytest чистит папку
    # без блокировки (shutil.rmtree внутри AllureFileLogger) — параллельные
    # воркеры могут снести уже записанные результаты друг друга. Чистим один раз,
    # до того как xdist вообще порождает воркеров (у воркеров есть config.workerinput).
    if not hasattr(config, "workerinput") and ALLURE_RESULTS_DIR.exists():
        shutil.rmtree(ALLURE_RESULTS_DIR)


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: dict) -> dict:
    args = {**browser_type_launch_args, "slow_mo": settings.slow_mo}
    # --headed передан явно в CLI — не перебиваем его настройкой из .env
    if "--headed" not in " ".join(sys.argv):
        args["headless"] = settings.headless
    if settings.browser_engine == "chromium" and settings.browser_channel:
        args["channel"] = settings.browser_channel
    return args


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    args = {
        **browser_context_args,
        "viewport": {
            "width": settings.viewport_width,
            "height": settings.viewport_height,
        },
        "ignore_https_errors": True,
    }
    if settings.base_url:
        args["base_url"] = settings.base_url
    return args


@pytest.fixture(autouse=True)
def _default_timeout(page):
    page.set_default_timeout(settings.default_timeout)
    yield


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> None:
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture(autouse=True)
def _attach_screenshot_on_failure(request: pytest.FixtureRequest, page):
    yield
    failed_call = getattr(request.node, "rep_call", None)
    if failed_call is not None and failed_call.failed:
        allure.attach(
            page.screenshot(full_page=True),
            name="screenshot-on-failure",
            attachment_type=allure.attachment_type.PNG,
        )
