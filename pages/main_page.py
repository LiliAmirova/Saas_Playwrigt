import allure
from playwright.sync_api import sync_playwright, Page, expect
import random
import string
import os

class MainPage:
    # перечисляем локаторы
    MAIN_TEXT = "h2:has-text('Войдите в личный кабинет, чтобы начать расчет.')"
    LOGIN_FIELD = "input[name='login']"
    PASSWORD_FIELD = "input[name='pass']"
    LOGIN_BUTTON = "button:has-text('Войти')"
    TOP_CLICK = "[class='style_logo__X+IDS']"
    TELEGRAM_HELP_LINK = "a:has-text('Обратиться за помощью')"
    PHONE_NUMBER = "a:has-text('+7 903 130-54-77')"
    MAIL_INFO = "a:has-text('info@topklik.online')"
    # COPYRIGHT = "div:has-text('Все права защищены')"

    def __init__(self, page: Page):  # передаем page при создании
        self.page = page  # сохраняем локально

    def attach_screenshot(self, target=None, name="скриншот"):
        """Универсальный метод для создания скриншотов"""
        try:
            if target is None:
                screenshot = self.page.screenshot(full_page=True)
            elif isinstance(target, str):
                screenshot = self.page.locator(target).screenshot()
                name = f"{name} ({target})"
            else:
                screenshot = target.screenshot()

            allure.attach(screenshot, name, allure.attachment_type.PNG)
        except Exception as e:
            print(f"Ошибка при создании скриншота: {e}")

    def random_text(self):
        # Генерация случайной строки (10 символов)
        random_text = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        return random_text


    def check_page(self):  # функция проверяет страницу на наличие и видимость элементов по локаторам, которые отображаются и доступны сразу
        """Проверяет видимость элемента с обработкой ошибок"""
        try:
            with allure.step(f'Проверяем наличие и видимость элементов на главное странице:'):
                self.attach_screenshot()
                expect(self.page.locator(MainPage.MAIN_TEXT)).to_be_visible()
                expect(self.page.locator(MainPage.LOGIN_FIELD)).to_be_visible()
                expect(self.page.locator(MainPage.PASSWORD_FIELD)).to_be_visible()
                expect(self.page.locator(MainPage.LOGIN_BUTTON)).to_be_visible()
                expect(self.page.locator(MainPage.TOP_CLICK)).to_be_visible()
                expect(self.page.locator(MainPage.TELEGRAM_HELP_LINK)).to_be_visible()
                expect(self.page.locator(MainPage.PHONE_NUMBER)).to_be_visible()
                expect(self.page.locator(MainPage.MAIL_INFO)).to_be_visible()
                #expect(self.page.locator(MainPage.COPYRIGHT)).to_be_visible()
                return True
        except Exception as e:
            allure.attach(
                f"Элемент не найден: {str(e)}",
                attachment_type=allure.attachment_type.TEXT
            )
            return False

    @allure.step('Заполняем поле логин')
    def type_login(self, login):
        self.page.locator(MainPage.LOGIN_FIELD).fill(login)
        self.attach_screenshot()

    @allure.step('Заполняем поле пароль')
    def type_password(self, password):
        self.page.locator(MainPage.PASSWORD_FIELD).fill(password)
        self.attach_screenshot()

    @allure.step('Нажимаем на кнопку "Войти"')
    def click_login(self):
        self.attach_screenshot()
        self.attach_screenshot("button:has-text('Войти')", "Кнопка Войти")
        self.page.locator(MainPage.LOGIN_BUTTON).click()

    @allure.step('Вход в ЛК')
    def sign_in(self):
        login = os.getenv("TEST_USER_LOGIN")
        password = os.getenv("TEST_USER_PASSWORD")
        self.type_login(login)
        self.type_password(password)
        self.click_login()




