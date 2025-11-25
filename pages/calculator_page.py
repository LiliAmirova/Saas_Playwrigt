import allure
from pages.processors_page import ProcessorsPage
from pages.main_page import MainPage
from playwright.sync_api import sync_playwright, Page, expect
import time

class СalculatorPage:
    # перечисляем локаторы, которые всегда присутствуют на странице
    USER_BAR= "h2:has-text('Tester')"
    LOGOUT_BUTTON = "button:has-text('Выйти')"
    CALC_TEXT = "h1:has-text('Калькулятор столешниц')" # Заголовок страницы
    MAIN_SECTION = "h3:has-text('Основная часть')"
    COUNTERTOP ='[data-testid="countertop"]'  # чертеж столешницы
    COUNTERTOP_TYPE = '[data-testid="countertop-type"]' # параметр форм столешницы

    TOGGLE_SWITCH = 'img[alt="toggle"]' # переключатель столешницы
    ORDER_LIST = '[data-testid="order-list"]' # Справа расчет
    COMMENT ='textarea[placeholder="Комментарий к заказу"]'
    CALC_BUTTON = '[data-testid="calc-button"]' # Кнопка "Рассчитать"
    TOP_CLICK = 'div[class="style_logo__X+IDS"]'  # надпись "ТопКлик" слева снизу
    # Кнопки ниже столешницы
    TOP_BUTTON_1 =  "button[data-testid='top-button'] :has-text('Прямая 1')"

    TOP_BUTTON_2 = "button[data-testid='top-button'] :has-text('Стеновая панель')"

    TOP_BUTTON_3 = "button[data-testid='top-button'] :has-text('Плинтус')"  #   Зеленая Плашка для вкл и выключения Плинтуса
    TOP_BUTTON_3_OK_GREEN_ICON = 'img[src*="ok-green"][alt="ok-green"]'  # На плашке "Плинтус" галочка зеленая для включения и исключения плинтуса в рассчета
    TOP_BUTTON_3_PLUS_GREEN = 'img[src*="plus-green"][alt="plus-green"]' #  ??? Эти локаторы появляются не сразу

    PLINTH_ELEMENT_PLUS = 'div.plinth.line'
    PLINTH_ELEMENT_MINUS = 'div.dotted.line' # плинтус отсутсвует в элемнтах столешницы

    MENU_BUTTON = "button[data-testid='top-button']" # кнопки меню внизу столешницы три кнопки

    BUTTON_ISLAND ='[data-testid="product-item"][style*="island"]:has(h4:has-text("Остров")) ' # кнопка добавить остов
    BUTTON_ISLAND_TEXT='[data-testid="product-item"] p.p14:has-text("многофункциональный стол в центре кухни")'
    BUTTON_ISLAND_PLUS = '[data-testid="product-item"][style*="island"] img[alt="plus-blue"]' # плюс на кнопке "Добавить остров"
    BUTTON_ISLAND_MINUS = '[data-testid="product-item"][style*="island"] img[alt="ok-white"]'  # Удалить Остров Локаторы которые появляются ПОСЛЕ нажатия
    ISLAND='[data-testid="island"]'

    OPTIONS_SINK = 'div[data-testid="options-item"][style*="sink"]' # Проточки для стока воды
    OPTIONS_SINK_TEXT = 'div[data-testid="options-item"][style*="sink"]:has(h4:has-text("Проточки для стока воды")):has(p:has-text("устраняют скапливание влаги в районе мойки"))'  # Проточки для стока воды
    OPTIONS_SINK_PLUS = 'div[data-testid="options-item"][style*="sink"] img[alt="plus-blue"]'
    OPTIONS_SINK_MINUS = 'div[data-testid="options-item"][style*="sink"] img[alt="ok-white"]'

    # Локаторы, которые появляются ПОСЛЕ нажатия

    INACTIVE_TOGGLE = 'img[src*="inactive"][alt="toggle"]' # Локатор для неактивного состояния
    ACTIVE_TOGGLE = 'img[src*="active"][alt="toggle"]'  # Локатор для активного состояния (если есть отдельное изображение)
    SHOW_COUNTERTOP_BUTTON = '[data-testid="show-main"]'  # Локатор наличия/отсутствия кнопки "Показать столешницу"

    THICKNESS_LABEL = 'label.pm14'
    SELECT_THICKNESS = '[data-testid="select-thickness"] button .inputDigital'  # Селектор Толщины :has-text("Толщина")
    SIZE_CONTROL_300 = '[data-testid="size-control"] input[inputmode="numeric"][value="300"]'  # размер панели
    SIZE_CONTROL_150 = '[data-testid="size-control"] input[inputmode="numeric"][value="150"]'  # размер панели

    STRAIGHT_COUNTERTOP_TYPE = '[data-testid="countertop-type-q"]'  # прямая столешница
    COUNTERTOP_STRAIGHT_1 = "[class='line c-Q-outerMiddle dotted']"  # линия прямой столешницы
    COUNTERTOP_STRAIGHT_2 = "[class='line c-Q-outerLeft dotted']"  # линия прямой столешницы
    COUNTERTOP_STRAIGHT_3 = "[class='line c-Q-outerBottom edge']"  # линия прямой столешницы

    COUNTERTOP_STRAIGHT_4 = "[class='line c-Q-outerRight plinth']"  # линия прямой столешницы

    G_COUNTERTOP_TYPE = '[data-testid="countertop-type-l"]'  # Г-образная столешница

    U_COUNTERTOP_TYPE = '[data-testid="countertop-type-u"]'  # П-образная столешница
    COUNTERTOP_U_1 = "[class='line c-U-outerMiddle dotted']"  # линия П-образной столешницы
    COUNTERTOP_U_2 = "[class='line c-U-outerLeft plinth']"  # линия П-образной столешницы
    COUNTERTOP_U_3 = "[class='line c-U-outerLeftBottom edge']"  # линия П-образной столешницы
    COUNTERTOP_U_4 = "[class='line c-U-innerLeft edge']"  # линия П-образной столешницы
    COUNTERTOP_U_5 = "[class='line c-U-innerMiddle edge']"  # линия П-образной столешницы
    COUNTERTOP_U_6 = "[class='line c-U-innerRight edge']"  # линия П-образной столешницы
    COUNTERTOP_U_7 = "[class='line c-U-outerRightBottom edge']"  # линия П-образной столешницы
    COUNTERTOP_U_8 = "[class='line c-U-outerRight plinth']"  # линия П-образной столешницы

    def __init__(self, page: Page):  # передаем page при создании
        self.page = page  # сохраняем локально
        self.main_page = MainPage(page)  # Создаем экземпляр MainPage
        self.processors_page = ProcessorsPage(page)

    def check_page(self): # функция проверяет страницу на наличие и видимость элементов по локаторам, которые отображаются и доступны сразу
        with allure.step('Проверяем наличие элементов на странице "Калькулятор столешниц":'):
            expect(self.page.locator(СalculatorPage.USER_BAR)).to_be_visible()
            expect(self.page.locator(СalculatorPage.LOGOUT_BUTTON)).to_be_visible()
            expect(self.page.locator(СalculatorPage.CALC_TEXT)).to_be_visible()
            expect(self.page.locator(СalculatorPage.TOP_CLICK)).to_be_visible()
            expect(self.page.locator(СalculatorPage.TOGGLE_SWITCH)).to_be_visible()
            expect(self.page.locator(СalculatorPage.MAIN_SECTION)).to_be_visible()
            expect(self.page.locator(СalculatorPage.COUNTERTOP)).to_be_visible()
            expect(self.page.locator(СalculatorPage.COUNTERTOP_TYPE)).to_be_visible()
            expect(self.page.locator(СalculatorPage.STRAIGHT_COUNTERTOP_TYPE)).to_be_visible()
            expect(self.page.locator(СalculatorPage.G_COUNTERTOP_TYPE)).to_be_visible()
            expect(self.page.locator(СalculatorPage.U_COUNTERTOP_TYPE)).to_be_visible()
            expect(self.page.locator(СalculatorPage.TOP_BUTTON_1)).to_be_visible()
            expect(self.page.locator(СalculatorPage.TOP_BUTTON_2)).to_be_visible()
            expect(self.page.locator(СalculatorPage.TOP_BUTTON_3)).to_be_visible()
            expect(self.page.locator(СalculatorPage.TOP_BUTTON_3_OK_GREEN_ICON)).to_be_visible()
            expect(self.page.locator(СalculatorPage.BUTTON_ISLAND)).to_be_visible()
            expect(self.page.locator(СalculatorPage.BUTTON_ISLAND_TEXT)).to_be_visible()
            expect(self.page.locator(СalculatorPage.BUTTON_ISLAND_PLUS)).to_be_visible()
            expect(self.page.locator(СalculatorPage.OPTIONS_SINK)).to_be_visible()
            expect(self.page.locator(СalculatorPage.OPTIONS_SINK_TEXT)).to_be_visible()
            expect(self.page.locator(СalculatorPage.OPTIONS_SINK_PLUS)).to_be_visible()

            self.main_page.attach_screenshot()

    def switch_to_u_type_countertop(self):
        with allure.step('Выбираем форму столешницы:кликаем на кнопку П-образная'):
            self.page.locator(СalculatorPage.U_COUNTERTOP_TYPE).click()
            self.main_page.attach_screenshot()

    def choice_of_thickness(self, value):
        """Выбрать толщину из выпадающего списка"""
        with allure.step(f'Выбираем толщину столешницы="{value}"'):
            # 1. Кликнуть на селектор, чтобы открыть выпадающий список
            element = self.page.locator(СalculatorPage.SELECT_THICKNESS).first
            self.main_page.attach_screenshot(СalculatorPage.COUNTERTOP, "Исходное состояние селектора выбора толщины")
            element.click()
            self.main_page.attach_screenshot(СalculatorPage.COUNTERTOP, "Состояние  после клика:  выпадающий список")

            # 2. Подождать пока откроется выпадающий список
            self.page.wait_for_selector('[data-testid="select-thickness"] button .inputDigital', state='visible')
            # 3. Выбрать нужное значение
            self.page.locator(f'span.selectTitle:has-text("{value}")').click()
            self.main_page.attach_screenshot(СalculatorPage.COUNTERTOP,"Состояние  после выбора толщины=4")
            # 4. Проверить, что значение установилось
            expect(element).to_have_text(value)

    def plinth_minus(self):
        """Исключаем плинтус из расчета заказа"""
        with allure.step("Плинтус: не требуется (выключить)"):
            with allure.step("Проверяем изначальное состояние кнопки"):
                expect(self.page.locator(СalculatorPage.TOP_BUTTON_3_OK_GREEN_ICON)).to_be_visible() # Проверяем изначальное состояние кнопки
                element = self.page.locator(СalculatorPage.MENU_BUTTON).last
                self.main_page.attach_screenshot(element, "Плинтус включен")
            with allure.step("Кликаем на кнопку Плинтус"):
                self.page.locator(СalculatorPage.TOP_BUTTON_3_OK_GREEN_ICON).click()
            with allure.step("Проверяем измененное состояние кнопки после клика"):
                expect(self.page.locator(СalculatorPage.TOP_BUTTON_3_PLUS_GREEN)).to_be_visible() # Проверяем измененное состояние кнопки после клика
                self.main_page.attach_screenshot(element, "Плинтус выключен")

            # Цикл проверки отсутсвия всех плинтусов в элементах столешницы
            plinth_elements = self.page.locator(СalculatorPage.PLINTH_ELEMENT_MINUS)
            element_count = plinth_elements.count()

            with allure.step(f"Проверяем отсутствие {element_count} элементов плинтуса в столшнице"):
                for i in range(element_count):
                    expect(plinth_elements.nth(i)).to_be_visible()
                    allure.attach(
                        plinth_elements.nth(i).screenshot(),
                        name=f"plinth_element_{i + 1}",
                        attachment_type=allure.attachment_type.PNG
                    )
                    
    def island_add(self):
        with allure.step("Добавить Остров"):
            with allure.step("Проверяем изначальное состояние кнопки"):
                expect(self.page.locator(СalculatorPage.BUTTON_ISLAND_PLUS)).to_be_visible() # Проверяем наличие кнопки плюса на плашке "Добавить остров"
                self.main_page.attach_screenshot(СalculatorPage.BUTTON_ISLAND, "Исходное состояние  плашки 'Остров'")
            with allure.step("Кликаем на плашке 'Остров' на плюс"):
                self.page.locator(СalculatorPage.BUTTON_ISLAND_PLUS).click()
            with allure.step("Проверяем состояние кнопки после клика"):
                expect(self.page.locator(СalculatorPage.BUTTON_ISLAND_MINUS)).to_be_visible()  # Проверяем наличие кнопки плюса на плашке "Добавить остров"
                self.main_page.attach_screenshot(СalculatorPage.BUTTON_ISLAND,"Измененное состояние  плашки 'Остров' после клика")
            with allure.step("Проверяем, что появился блок 'Остров'"):
                expect(self.page.locator(СalculatorPage.ISLAND)).to_be_visible()
                self.main_page.attach_screenshot(СalculatorPage.ISLAND,"Блок Остров")

    def options_sink_add(self):
        with allure.step("Добавить проточки для стока воды"):
            with allure.step("Проверяем изначальное состояние кнопки"):
                expect(self.page.locator(СalculatorPage.OPTIONS_SINK)).to_be_visible()  # Проверяем наличие кнопки плюса на плашке "Добавить остров"
                expect(self.page.locator(СalculatorPage.OPTIONS_SINK_PLUS)).to_be_visible()
                self.main_page.attach_screenshot(СalculatorPage.OPTIONS_SINK, "Исходное состояние  плашки")
            with allure.step("Кликаем на плюс"):
                self.page.locator(СalculatorPage.OPTIONS_SINK_PLUS).click()
            with allure.step("Проверяем состояние кнопки после клика"):
                expect(self.page.locator(СalculatorPage.OPTIONS_SINK_MINUS)).to_be_visible()  # Проверяем наличие кнопки плюса на плашке "Добавить остров"
                self.main_page.attach_screenshot(СalculatorPage.OPTIONS_SINK,"Измененное состояние после клика")

    def choice_stone_block(self, name):
        with allure.step(f"Выбор цвета столешницы {name}"):
            with allure.step("Проверяем наличие выбранного цвета"):
                name_snake_case = name.replace(" ", "_").replace("-", "_")
                STONE_NAME_TEXT = f'[data-testid="stone-block"] div.stoneName:has-text("{name}")' # название материала
                STONE_NAME = f'.style_circle__2HuHY[style*="{name_snake_case}"]'
                # 2. Как соседний элемент (братский)
                STONE_NAME_CHECK_ICON = f'.style_circle__2HuHY[style*="{name_snake_case}"] ~ img[alt="ok-blue"]'
                # 3. Как следующий соседний элемент
                #STONE_NAME_CHECK_ICON = f'.style_circle__2HuHY[style*="{name_snake_case}"] + .style_ok__z07Qz'

                expect(self.page.locator(STONE_NAME)).to_be_visible()
                expect(self.page.locator(STONE_NAME_TEXT)).to_be_visible()
                self.main_page.attach_screenshot(STONE_NAME, "Выбранный цвет")
                self.main_page.attach_screenshot(STONE_NAME_TEXT, "Надпись выбранного цвета")
            with allure.step("Кликаем на выбранный цвет"):
                self.page.locator(STONE_NAME).click()
            with allure.step("Проверяем, что на выбранном элементе появилась галочка"):
                expect(self.page.locator(STONE_NAME_CHECK_ICON)).to_be_visible()
                self.main_page.attach_screenshot(STONE_NAME_CHECK_ICON, "Галочка")
                self.main_page.attach_screenshot(STONE_NAME, "Отмечен выбранный цвет")
                self.main_page.attach_screenshot(STONE_NAME_TEXT, "Надпись выбранного цвета")

    def click_calculate_button(self):
        with allure.step("Нажать кнопку 'Рассчитать'"):
            expect(self.page.locator(СalculatorPage.CALC_BUTTON)).to_be_visible()
            self.main_page.attach_screenshot()
            self.main_page.attach_screenshot(СalculatorPage.CALC_BUTTON, "Кнопка 'Рассчитать'")
            self.page.locator(СalculatorPage.CALC_BUTTON).click()
            self.main_page.attach_screenshot()
        #with allure.step("Проверяем, что открылась страница с заголовком 'Обработчики'"):
        #    self.processors_page.check_page()




