from playwright.sync_api import sync_playwright, Page, expect
from dotenv import load_dotenv
import allure
import os
from pages.main_page import MainPage
from pages.calculator_page import СalculatorPage
import time

# Загружаем переменные из .env файла
load_dotenv()
BASE_URL = os.getenv("BASE_URL")

@allure.suite('1.Успешная авторизация')
@allure.sub_suite("Позитивные тесты")
@allure.title("Проверка успешной авторизации с валидными логином и паролем")
def test_auth_login_and_password_valid(page: Page) -> None:
    page.goto(BASE_URL)
    # Создаем экземпляр класса и вызываем метод
    main_page = MainPage(page)
    main_page.check_page()
    # Получаем переменные из окружения
    login = os.getenv("TEST_USER_LOGIN")
    password = os.getenv("TEST_USER_PASSWORD")

    # Определяем функцию-фильтр для ожидаемого ответа
    def is_target_response(response):
        return response.url.endswith("/login") and response.status < 300 and response.request.method == "POST"

    # Ожидаем ответ на запрос авторизации
    with page.expect_response(is_target_response, timeout=15000) as response_info:
        # Заполняем поля
        main_page.type_login(login)
        main_page.type_password(password)
        # Кликаем на кнопку "Войти"
        main_page.click_login()
    # Получаем объект ответа
    response = response_info.value

    # Извлекаем тело ответа в формате JSON
    response_body = response.json()

    # Добавляем проверку успешной авторизации: проверка URL после авторизации
    with allure.step("Проверяем успешность авторизации"):
        with allure.step("Проверяем URL страницы"):
            expect(page).to_have_url(f"{BASE_URL}")
            allure.attach(
                f"Ожидаемый URL: {BASE_URL}\nФактический URL: {page.url}",
                name="Проверка URL",
                attachment_type=allure.attachment_type.TEXT
            )
    # Проверка наличия  и видимости  элемента на странице после успешной авторизации:
    # expect(page.locator(СalculatorPage.USER_BAR)).to_be_visible()
        with allure.step("Проверяем наличие элементов на странице после успешной авторизации"):
            expect(page.locator(СalculatorPage.USER_BAR)).to_be_visible()
            main_page.attach_screenshot()

    with allure.step("Проверяем в devtools: ответ API"):
        # Проверяем статус ответа
        assert response.status == 200, f"Ожидался статус 200, получен {response.status}"
        # Проверяем содержимое ответа
        assert response_body['success'] == True, f"Ожидалось:{response_body['success']}"
        assert response_body['name'] == "Tester", f"Ожидалось:{response_body['name']}"
        # # Дополнительные проверки структуры ответа
        # assert 'detail' in response_body, "В ответе отсутствует поле 'detail'"
        # assert isinstance(response_body['detail'], str), "Поле 'detail' должно быть строкой"


@allure.suite('1.Успешная авторизация')
@allure.sub_suite("Негативные тесты")
@allure.title("Проверка авторизации при пустом логине и пароле")
def test_auth_empty_login_and_password(page: Page) -> None:
    page.goto(BASE_URL)
    # Создаем экземпляр класса и вызываем метод
    main_page = MainPage(page)
    main_page.check_page()
    # Кликаем на кнопку "Войти"
    main_page.click_login()

    # Проверка URL после неуспешной авторизации
    with allure.step("Проверяем, что переход на другую страницу не произошел"):
        with allure.step("Проверяем URL страницы"):
            expect(page).to_have_url(f"{BASE_URL}")
            allure.attach(
                f"Ожидаемый URL: {BASE_URL}\nФактический URL: {page.url}",
                name="Проверка URL",
                attachment_type=allure.attachment_type.TEXT
            )
    # Проверка наличия и видимости элементов на странице после неуспешной авторизации:
        with allure.step("Проверяем, что остались на главной странице со всеми элементами"):
            main_page.check_page()


@allure.suite('1.Успешная авторизация')
@allure.sub_suite("Негативные тесты")
@allure.title("Проверка авторизации при НЕвалидных логине и пароле")
def test_auth_not_valid_login_and_password(page: Page) -> None:
    """ интеграционный тест, который проверяет полный цикл авторизации от UI до API ответ"""
    page.goto(BASE_URL)
    # Создаем экземпляр класса и вызываем метод
    main_page = MainPage(page)
    main_page.check_page()

    # Определяем функцию-фильтр для ожидаемого ответа
    def is_target_response(response):
        return response.url.endswith("/login") and response.status == 401 and response.request.method == "POST"

    # Ожидаем ответ на запрос авторизации
    with page.expect_response(is_target_response, timeout=15000) as response_info:
       # Заполняем поля
        with allure.step("Генерим рандомные логин и пароль и  пытаемся с ними авторизоваться"):
            login_random = main_page.random_text()
            password_random = main_page.random_text()

            main_page.type_login(login_random)
            main_page.type_password(password_random)
            # Кликаем на кнопку "Войти"
            main_page.click_login()

    # Получаем объект ответа
    response = response_info.value

    # Извлекаем тело ответа в формате JSON
    response_body = response.json()

    # Проверка URL после неуспешной авторизации
    with allure.step("Проверяем UI после неуспешной авторизации "):
        with allure.step("Проверяем URL страницы: перехода на другую страницу не произшел"):
            expect(page).to_have_url(f"{BASE_URL}")
            allure.attach(
                f"Ожидаемый URL: {BASE_URL}\nФактический URL: {page.url}",
                name="Проверка URL",
                attachment_type=allure.attachment_type.TEXT
            )
        # Проверка наличия и видимости элементов на странице после неуспешной авторизации:
        with allure.step("Проверяем, что остались на главной странице со всеми элементами, в том числе с видимостью формы авторизации"):
            main_page.check_page()

        with allure.step("Проверяем, что поля не очистились автоматически"):
            # Получаем значения из полей ввода  page.locator(СalculatorPage.USER_BAR
            actual_login = page.locator(MainPage.LOGIN_FIELD).input_value()
            actual_password = page.locator(MainPage.PASSWORD_FIELD).input_value()
            #actual_login = page.locator("input[type='text']").input_value()
            #actual_password = page.locator("input[type='password']").input_value()

            assert actual_login == login_random, f"Поле логина очистилось. Ожидалось: {login_random}, получено: {actual_login}"
            assert actual_password == password_random, f"Поле пароля очистилось. Ожидалось: {password_random}, получено: {actual_password}"

    with allure.step("Проверяем в devtools: ответ API"):
        # Проверяем статус ответа
        assert response.status == 401, f"Ожидался статус 401, получен {response.status}"
        # Проверяем содержимое ответа
        assert response_body['detail'] == 'Incorrect username or password', f"Неверное сообщение об ошибке: {response_body.get('detail')}"
        # Дополнительные проверки структуры ответа
        assert 'detail' in response_body, "В ответе отсутствует поле 'detail'"
        assert isinstance(response_body['detail'], str), "Поле 'detail' должно быть строкой"

@allure.suite('1.Успешная авторизация')
@allure.sub_suite("Негативные тесты")
@allure.title("Проверка авторизации при пустом логине и пароле")
def test_auth_empty_login_and_password(page: Page) -> None:
    page.goto(BASE_URL)
    # Создаем экземпляр класса и вызываем метод
    main_page = MainPage(page)
    main_page.check_page()
    # Кликаем на кнопку "Войти"
    main_page.click_login()

    # Проверка URL после неуспешной авторизации
    with allure.step("Проверяем, что переход на другую страницу не произошел"):
        with allure.step("Проверяем URL страницы"):
            expect(page).to_have_url(f"{BASE_URL}")
            allure.attach(
                f"Ожидаемый URL: {BASE_URL}\nФактический URL: {page.url}",
                name="Проверка URL",
                attachment_type=allure.attachment_type.TEXT
            )
    # Проверка наличия и видимости элементов на странице после неуспешной авторизации:
        with allure.step("Проверяем, что остались на главной странице со всеми элементами"):
            main_page.check_page()


@allure.suite('1.Успешная авторизация')
@allure.sub_suite("Негативные тесты")
@allure.title("Проверка авторизации при валидном логине и  НЕвалидном пароле")
def test_auth_valid_login_and_not_valid_password(page: Page) -> None:
    """ интеграционный тест, который проверяет полный цикл авторизации от UI до API ответ"""
    page.goto(BASE_URL)
    # Создаем экземпляр класса и вызываем метод
    main_page = MainPage(page)
    main_page.check_page()
    # Получаем переменные из окружения
    login = os.getenv("TEST_USER_LOGIN")

    # Определяем функцию-фильтр для ожидаемого ответа
    def is_target_response(response):
        return response.url.endswith("/login") and response.status == 401 and response.request.method == "POST"

    # Ожидаем ответ на запрос авторизации
    with page.expect_response(is_target_response, timeout=15000) as response_info:
       # Заполняем поля
        with allure.step("Генерим рандомный пароль и  пытаемся с ним авторизоваться"):
            password_random = main_page.random_text()

            main_page.type_login(login)
            main_page.type_password(password_random)
            # Кликаем на кнопку "Войти"
            main_page.click_login()

    # Получаем объект ответа
    response = response_info.value

    # Извлекаем тело ответа в формате JSON
    response_body = response.json()

    # Проверка URL после неуспешной авторизации
    with allure.step("Проверяем UI после неуспешной авторизации "):
        with allure.step("Проверяем URL страницы: перехода на другую страницу не произшел"):
            expect(page).to_have_url(f"{BASE_URL}")
            allure.attach(
                f"Ожидаемый URL: {BASE_URL}\nФактический URL: {page.url}",
                name="Проверка URL",
                attachment_type=allure.attachment_type.TEXT
            )
        # Проверка наличия и видимости элементов на странице после неуспешной авторизации:
        with allure.step("Проверяем, что остались на главной странице со всеми элементами, в том числе с видимостью формы авторизации"):
            main_page.check_page()

        with allure.step("Проверяем, что поля не очистились автоматически"):
            # Получаем значения из полей ввода
            actual_login = page.locator(MainPage.LOGIN_FIELD).input_value()
            actual_password = page.locator(MainPage.PASSWORD_FIELD).input_value()

            assert actual_login == login, f"Поле логина очистилось. Ожидалось: {login}, получено: {actual_login}"
            assert actual_password == password_random, f"Поле пароля очистилось. Ожидалось: {password_random}, получено: {actual_password}"

    with allure.step("Проверяем в devtools: ответ API"):
        # Проверяем статус ответа
        assert response.status == 401, f"Ожидался статус 401, получен {response.status}"
        # Проверяем содержимое ответа
        assert response_body['detail'] == 'Incorrect username or password', f"Неверное сообщение об ошибке: {response_body.get('detail')}"
        # Дополнительные проверки структуры ответа
        assert 'detail' in response_body, "В ответе отсутствует поле 'detail'"
        assert isinstance(response_body['detail'], str), "Поле 'detail' должно быть строкой"









