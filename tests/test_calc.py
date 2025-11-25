from playwright.sync_api import sync_playwright, Page, expect
from dotenv import load_dotenv
import allure
import os
from pages.main_page import MainPage
from pages.calculator_page import СalculatorPage
import time

load_dotenv()
BASE_URL = os.getenv("BASE_URL")

@allure.suite('2.Проверить, что работает переключатель "Скрыть столешницу" – столешница не отображается')
@allure.sub_suite("Позитивные тесты")
@allure.title("Проверка включения переключателя 'Скрыть столешницу' ")
def test_calc_toggle_switch(page: Page) -> None:
    """ Проверить, что работает переключатель "Скрыть столешницу" – столешница не отображается """
    page.goto(BASE_URL)
    # Создаем экземпляр класса и вызываем метод
    calculator_page = СalculatorPage(page)
    main_page = MainPage(page)
    # Проверяем исходное состояние:Столешница отображается на экране и Переключатель "Скрыть столешницу" находится в выкл состоянии
    with allure.step("Предусловия: пользователь на странице калькулятора"):
        main_page.attach_screenshot()
        main_page.sign_in()  # Заходим в ЛК
        calculator_page.check_page() # Проверям страницу после авторизации на наличие видимость элементов
    with allure.step('Предусловия: проверить начальное состояние'):
        with allure.step("Переключатель 'Скрыть столешницу' находится в ВКЛюченном состоянии"):
            expect(page.locator(СalculatorPage.ACTIVE_TOGGLE)).to_be_visible()
            main_page.attach_screenshot(СalculatorPage.ACTIVE_TOGGLE, "Переключатель ВКЛючен")
        with allure.step("Столешница отображается на экране"):
            expect(page.locator(СalculatorPage.SHOW_COUNTERTOP_BUTTON)).not_to_be_visible()  # т.е не отображается кнопка "Показать столешницу"
            expect(page.locator(СalculatorPage.COUNTERTOP_STRAIGHT_1)).to_be_visible()     # отображается линиия столешницы
            expect(page.locator(СalculatorPage.COUNTERTOP_STRAIGHT_2)).to_be_visible()
            expect(page.locator(СalculatorPage.COUNTERTOP_STRAIGHT_3)).to_be_visible()
            expect(page.locator(СalculatorPage.COUNTERTOP_STRAIGHT_4)).to_be_visible()
            main_page.attach_screenshot(СalculatorPage.COUNTERTOP, "Столешница")
        with allure.step("Задана прямая форма столешницы"):
            expect(page.locator(СalculatorPage.STRAIGHT_COUNTERTOP_TYPE)).to_be_visible()
            main_page.attach_screenshot(СalculatorPage.STRAIGHT_COUNTERTOP_TYPE, "Форма столешницы")

    with allure.step("Нажать на переключатель 'Скрыть столешницу'"):
        page.locator(СalculatorPage.ACTIVE_TOGGLE).click()
        main_page.attach_screenshot()
        with allure.step("Проверить, что переключатель 'Скрыть столешницу' находится в ВЫКЛюченном состоянии"):
            expect(page.locator(СalculatorPage.INACTIVE_TOGGLE)).to_be_visible()
            main_page.attach_screenshot(СalculatorPage.INACTIVE_TOGGLE, "Переключатель ВЫКЛючен")
        with allure.step("Проверить, что столешница  скрыта"):
            expect(page.locator(СalculatorPage.COUNTERTOP_STRAIGHT_1)).not_to_be_visible()
            expect(page.locator(СalculatorPage.COUNTERTOP_STRAIGHT_2)).not_to_be_visible()
            expect(page.locator(СalculatorPage.COUNTERTOP_STRAIGHT_3)).not_to_be_visible()
            expect(page.locator(СalculatorPage.COUNTERTOP_STRAIGHT_4)).not_to_be_visible()
            main_page.attach_screenshot(СalculatorPage.COUNTERTOP, "Столешница")
        with allure.step('Проверить, что появилась кнопка "Показать столешницу"'):
            expect(page.locator(СalculatorPage.SHOW_COUNTERTOP_BUTTON)).to_be_visible()
            main_page.attach_screenshot(СalculatorPage.SHOW_COUNTERTOP_BUTTON, "Столешница")
        with allure.step('Проверить, что сохранился параметр о форме столешницы'):
            # Здесь можно добавить проверки сохранения размеров и параметров
            expect(page.locator(СalculatorPage.STRAIGHT_COUNTERTOP_TYPE)).to_be_visible()
            main_page.attach_screenshot(СalculatorPage.STRAIGHT_COUNTERTOP_TYPE, "Форма столешницы")


@allure.suite('3.Переключение на П-образную столешницу – отображается П-образная столешница')
@allure.sub_suite("Позитивные тесты")
@allure.title("Проверка: При переключение на П-образную столешницу – отображается П-образная столешница ' ")
def test_calc_switch_to_u_type_countertop(page: Page) -> None:
    """ Проверить, что при переключении на П-образную столешницу – отображается П-образная столешница """
    page.goto(BASE_URL)
    # Создаем экземпляр класса и вызываем метод
    calculator_page = СalculatorPage(page)
    main_page = MainPage(page)
    # Проверяем исходное состояние:Столешница отображается на экране и Переключатель "Скрыть столешницу" находится в выкл состоянии
    with allure.step("Предусловия: пользователь на странице калькулятора"):
        main_page.attach_screenshot()
        main_page.sign_in()  # Заходим в ЛК
        calculator_page.check_page() # Проверям страницу после авторизации на наличие видимость элементов, в т.ч. три варианта: "Прямая", "Г-образная", "П-образная"
    with allure.step("Предусловия: Переключатель 'Скрыть столешницу' находится в ВКЛюченном состоянии"):
        expect(page.locator(СalculatorPage.ACTIVE_TOGGLE)).to_be_visible()
        main_page.attach_screenshot(СalculatorPage.ACTIVE_TOGGLE, "Переключатель ВКЛючен")
    with allure.step('Предусловия: П-образная столешница НЕ активна'):
        expect(page.locator(СalculatorPage.U_COUNTERTOP_TYPE)).not_to_have_class("active")

    with allure.step('Выбираем форму столешницы:кликаем на кнопку П-образная'):
        page.locator(СalculatorPage.U_COUNTERTOP_TYPE).click()
        main_page.attach_screenshot()
        with allure.step("Проверить, что отображается П-образная столешница"):
            expect(page.locator(СalculatorPage.COUNTERTOP_U_1)).to_be_visible()
            expect(page.locator(СalculatorPage.COUNTERTOP_U_2)).to_be_visible()
            expect(page.locator(СalculatorPage.COUNTERTOP_U_3)).to_be_visible()
            expect(page.locator(СalculatorPage.COUNTERTOP_U_4)).to_be_visible()
            expect(page.locator(СalculatorPage.COUNTERTOP_U_5)).to_be_visible()
            expect(page.locator(СalculatorPage.COUNTERTOP_U_6)).to_be_visible()
            expect(page.locator(СalculatorPage.COUNTERTOP_U_7)).to_be_visible()
            expect(page.locator(СalculatorPage.COUNTERTOP_U_8)).to_be_visible()
            main_page.attach_screenshot(СalculatorPage.COUNTERTOP, "Столешница")
        with allure.step("Проверить, что отображается три панели с размерами: 300x60, 150x60, 150x60"):
            expect(page.locator(СalculatorPage.SIZE_CONTROL_300).first).to_be_visible()
            expect(page.locator(СalculatorPage.SIZE_CONTROL_150).nth(0)).to_be_visible()
            expect(page.locator(СalculatorPage.SIZE_CONTROL_150).nth(1)).to_be_visible()
        with allure.step("Проверить, что отображается селектор толщины со значением '2'"):
            expect(page.locator(СalculatorPage.SELECT_THICKNESS).first).to_have_text('2')
            expect(page.locator(СalculatorPage.SELECT_THICKNESS).first).to_be_visible()
            main_page.attach_screenshot(page.locator(СalculatorPage.SELECT_THICKNESS).first, "В селекторе выбрана цифра 2")

            expect(page.locator(СalculatorPage.THICKNESS_LABEL)).to_have_text('Толщина')
            expect(page.locator(СalculatorPage.THICKNESS_LABEL)).to_be_visible()
            main_page.attach_screenshot(СalculatorPage.THICKNESS_LABEL, "Слово 'Толщина' над селектором")
            #element = page.locator(СalculatorPage.SELECT_THICKNESS).first
            main_page.attach_screenshot(page.locator('[data-testid="select-thickness"] button').first, "Кнопка селектора толщины")



