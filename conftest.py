import os
import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page, Playwright
import allure
import time

#BASE_URL = "https://dev.topklik.online"

# @pytest.fixture(scope="session")
# def browser():
#     # 1. Запуск Playwright
#     with sync_playwright() as p:
#         # 2. Проверка переменной окружения
#         ws_endpoint = os.environ.get("WS_ENDPOINT")
#
#         # 3. Выбор способа запуска браузера
#         if ws_endpoint:
#             # Подключение к удаленному браузеру (Docker, Selenium Grid)
#             browser = p.chromium.connect(ws_endpoint)
#         else:
#             # Локальный запуск браузера
#             browser = p.chromium.launch(headless=False)
#
#         # 4. Передача браузера тестам
#         yield browser # ставим дальнейшее выполнение функции на паузу
#
#         # 5. Закрытие браузера после всех тестов
#         browser.close()
#
# @pytest.fixture
# def page(browser):
#     context = browser.new_context()
#     page = context.new_page()
#     yield page
#     context.close()

@pytest.fixture(scope='session')
def playwright() -> Playwright:
    """Фикстура для инициализации Playwright"""
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope='session')
def browser(playwright: Playwright) -> Browser:
    """Управление браузером"""
    browser = playwright.chromium.launch(headless=True)
    yield browser
    browser.close()

@pytest.fixture(scope='function')
def context(browser: Browser) -> BrowserContext:
    """Управление контекстом браузера"""
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        ignore_https_errors=True
    )
    yield context
    context.close()

@pytest.fixture(scope='function')
def page(context: BrowserContext) -> Page:
    """Управление страницей"""
    page = context.new_page()
    page.set_default_timeout(30000)
    yield page
    page.close()