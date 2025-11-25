from playwright.sync_api import sync_playwright, Page, expect
from dotenv import load_dotenv
import allure
import os
from pages.main_page import MainPage
from pages.calculator_page import СalculatorPage
from pages.processors_page import ProcessorsPage
from pages.results_page import ResultsPage
import time

load_dotenv()
BASE_URL = os.getenv("BASE_URL")

@allure.suite('4. E2E-сценарий: Сбор заказа -> Расчет итоговой суммы')
@allure.title("E2E-сценарий: Сбор заказа -> Расчет итоговой суммы")
def test_e2e(page: Page) -> None:
    """ Проверить, что работает E2E-сценарий """
    page.goto(BASE_URL, timeout=60000, wait_until='domcontentloaded')
    # Создаем экземпляр класса и вызываем метод
    calculator_page = СalculatorPage(page)
    main_page = MainPage(page)
    processors_page = ProcessorsPage(page)
    # Проверяем исходное состояние:Столешница отображается на экране и Переключатель "Скрыть столешницу" находится в выкл состоянии
    with allure.step("Предусловия: пользователь на странице калькулятора"):
        main_page.attach_screenshot()
        main_page.sign_in()  # Заходим в ЛК
        calculator_page.check_page() # Проверям страницу после авторизации на наличие видимость элементов
    with allure.step("Предусловия: Переключатель 'Скрыть столешницу' находится в ВКЛюченном состоянии"):
        expect(page.locator(СalculatorPage.ACTIVE_TOGGLE)).to_be_visible()

    with allure.step("Собираем заказ"):
        countertop_type = "П-образная"
        stone_material = "N-103 Gray Onix"
        total_cost = "403700.00 ₽"


        calculator_page.switch_to_u_type_countertop() #  Выбираем П-образную столешницу
        calculator_page.choice_of_thickness("4")  # Выбираем толщину столешницы= 4 см
        calculator_page.plinth_minus() # Плинтус: не требуется (выключить)
        calculator_page.island_add() # Добавить Остров
        calculator_page.options_sink_add()  # Добавить проточки для стока воды
        calculator_page.choice_stone_block(stone_material) #Выбираем цвет

    calculator_page.click_calculate_button() # Нажать на кнопку Рассчитать

    # Определяем функцию-фильтр для ожидаемого ответа
    def is_target_response(response):
        return response.url.endswith(
            "/report/generate_calculation_report") and response.status < 300 and response.request.method == "POST"

    # Ожидаем ответ после нажатия кнопки Расчет
    with page.expect_response(is_target_response, timeout=15000) as response_info:
        processors_page.click_report_button()  # Нажать на кнопку Расчет
    # Получаем объект ответа
    response = response_info.value
    # Извлекаем тело ответа в формате JSON
    response_body = response.json()
    # Проверяем статус ответа
    assert response.status == 200, f"Ожидался статус 200, получен {response.status}"

    URL_REPORT = response_body['6']['report_url']
    page.goto(URL_REPORT, timeout=60000, wait_until='domcontentloaded')
    results_page = ResultsPage(page)
    with allure.step(f"Проверяем, что страницы 'Результаты расчета' открылась):"):
        results_page.check_page()

    with allure.step(f"Проверяем материал {stone_material}"):
        stone_material_actual_value = results_page.get_material_value() # выбранная опция в e2e-сценарии
        stone_material_expected_part = stone_material
        assert stone_material_expected_part in stone_material_actual_value, f"Expected '{stone_material_expected_part}' to be in '{stone_material_actual_value}'"
        # делаем скрин блока таблицы "Общие параметры"
        table_basic_parameters = page.locator(ResultsPage.BASIC_PARAMETERS).first
        main_page.attach_screenshot(table_basic_parameters, "Общие параметры")

    with allure.step(f"Проверяем Тип столешницы: {countertop_type}"):
        countertop_type_actual_value = results_page.get_countertop_type_value() # выбранная опция в e2e-сценарии
        assert countertop_type_actual_value == countertop_type
        # делаем скрин блока таблицы "Параметры столешницы"
        table_basic_parameters = page.locator(ResultsPage.BASIC_PARAMETERS).nth(1)
        main_page.attach_screenshot(table_basic_parameters, "Параметры столешницы")

    with allure.step(f"Проверяем Опции: Проточки для стока воды"):
        options_sink_value = results_page.get_options_sink_value() # выбранная опция в e2e-сценарии
        assert "Проточки для стока воды" in options_sink_value, f"Expected 'Проточки для стока воды' to be in '{options_sink_value}'"
        main_page.attach_screenshot(table_basic_parameters, "Параметры столешницы")

    with allure.step(f"Проверяем Итоговую стоимость={total_cost}"):
        print(results_page.get_total_cost_value())
        total_cost_actual_value = results_page.get_total_cost_value()
        assert total_cost_actual_value == total_cost,  f"Ожидалась сумма {total_cost}, получен {total_cost_actual_value}"







