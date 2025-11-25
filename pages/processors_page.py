import allure
from pages.main_page import MainPage
from pages.results_page import ResultsPage
from playwright.sync_api import sync_playwright, Page, expect
import time
import pytest

class ProcessorsPage:
    # перечисляем локаторы, которые всегда присутствуют на странице
    HEADER_PAGE = "h1:has-text('Обработчики')"
    #BLOCK_PROCESSORS = '[id="calc"]:has(h1:has-text("Обработчики"))' #"div:has(h1:has-text(\"Обработчики\"))"  #'[id="calc"]:has(h1:has-text("Обработчики"))'
    BLOCK_PROCESSORS = '[id="calc"]:has(h1:has-text("Обработчики")):has-text("ОбработчикиИзготовление")'
    BLOCK_MAIN = '[data-testid="price-container"]'
    BLOCK_MAIN_PHOTO = '[data-testid="photo-block"]'
    BLOCK_MAIN_PRICE = '[data-testid="price-button"]'
    BLOCK_MAIN_REPORT_BUTTON = '[data-testid="open-report-button"]:has(h4:has-text("Расчет"))'
    BLOCK_MAIN_CREATE_ORDER_BUTTON = '[data-testid="create-order-button"]:has(h4:has-text("Создать КП"))'

    ORDER_BLOCK = '[data-testid="price-button"]'
    ORDER_LIST = '[data-testid="order-list"]'
    COMMENT = 'textarea[placeholder="Комментарий к заказу"]'
    CALC_BUTTON = '[data-testid="edit-button"]:has(h4:has-text("Редактировать"))'  # Кнопка "Рассчитать"

    # Локаторы, которые появляются ПОСЛЕ нажатия

    def __init__(self, page: Page):  # передаем page при создании
        self.page = page  # сохраняем локально
        self.main_page = MainPage(page)  # Создаем экземпляр MainPage
        self.results_page = ResultsPage(page)

    def check_page(self): # функция проверяет страницу на наличие и видимость элементов по локаторам, которые отображаются и доступны сразу
        with allure.step('Проверяем наличие элементов на странице "Обработчики":'):
            expect(self.page.locator(ProcessorsPage.HEADER_PAGE)).to_be_visible()
            expect(self.page.locator(ProcessorsPage.BLOCK_MAIN)).to_be_visible()
            expect(self.page.locator(ProcessorsPage.BLOCK_MAIN_PHOTO)).to_be_visible()
            expect(self.page.locator(ProcessorsPage.BLOCK_MAIN_PRICE)).to_be_visible()
            expect(self.page.locator(ProcessorsPage.BLOCK_MAIN_REPORT_BUTTON)).to_be_visible()
            expect(self.page.locator(ProcessorsPage.BLOCK_MAIN_CREATE_ORDER_BUTTON)).to_be_visible()

            self.main_page.attach_screenshot()

    def click_report_button(self):
        with allure.step("Нажать кнопку 'Расчет'"):
            # Подождать и проверить
            try:
                self.page.locator(ProcessorsPage.BLOCK_MAIN_REPORT_BUTTON).wait_for(state="visible", timeout=10000)
                expect(self.page.locator(ProcessorsPage.BLOCK_MAIN_REPORT_BUTTON)).to_be_visible()
                element_processors = self.page.locator(ProcessorsPage.BLOCK_PROCESSORS).last
                self.main_page.attach_screenshot(element_processors, "Обработчики")
            except:
                pytest.fail("Кнопка не появилась в течение 10 секунд")

            self.main_page.attach_screenshot(ProcessorsPage.BLOCK_MAIN_REPORT_BUTTON, "Кнопка 'Расчет'")
            self.page.locator(ProcessorsPage.BLOCK_MAIN_REPORT_BUTTON).click()


