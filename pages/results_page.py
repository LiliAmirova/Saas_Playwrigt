import allure
from pages.main_page import MainPage
from playwright.sync_api import sync_playwright, Page, expect
import time

class ResultsPage:
    # перечисляем локаторы, которые всегда присутствуют на странице
    HEADER_PAGE = "h1:has-text('Результаты расчета')"
    ALERT_DANGER = '.alert.alert-danger:has-text("Конфиденциально: только для сотрудников ТопКлик и компании-обработчика")'

    # Локатор для ячейки с "Материал"
    MATERIAL_CELL = "td:has-text('Материал')"
    # Локатор для значения материала (следующая ячейка)
    MATERIAL_VALUE = "//td[text()='Материал']/following-sibling::td[1]"

    BASIC_PARAMETERS = 'table.table-bordered tbody'

    COUNTERTOP_TYPE_VALUE = "//td[text()='Тип столешницы']/following-sibling::td[1]"
    OPTIONS_SINK_VALUE = "//td[text()='Опции']/following-sibling::td[1]"
    TOTAL_COST_VALUE = "//td[text()='Стоимость итоговая']/following-sibling::td[3]"

    # Локаторы, которые появляются ПОСЛЕ нажатия

    def __init__(self, page: Page):  # передаем page при создании
        self.page = page  # сохраняем локально
        self.main_page = MainPage(page)  # Создаем экземпляр MainPage

    def check_page(self): # функция проверяет страницу на наличие и видимость элементов по локаторам, которые отображаются и доступны сразу
        with allure.step('Проверяем наличие элементов на странице "Результаты расчета":'):
            expect(self.page.locator(ResultsPage.HEADER_PAGE)).to_be_visible()
            expect(self.page.locator(ResultsPage.ALERT_DANGER)).to_be_visible()
            #expect(self.page.locator(ResultsPage.BASIC_PARAMETERS)).to_be_visible()

            self.main_page.attach_screenshot()

    def get_material_value(self):
        return self.page.locator(self.MATERIAL_VALUE).text_content()

    def check_material_exists(self):
        expect(self.page.locator(self.MATERIAL_CELL)).to_be_visible()

    def get_countertop_type_value(self):
        return self.page.locator(self.COUNTERTOP_TYPE_VALUE).text_content()

    def get_options_sink_value(self):
        return self.page.locator(self.OPTIONS_SINK_VALUE).text_content()

    def get_total_cost_value(self):
        return self.page.locator(self.TOTAL_COST_VALUE).text_content()
