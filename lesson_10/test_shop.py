from selenium import webdriver
from MainPage import MainPage
from Cart import Cart
from Order import Order
from Auth import Auth
import allure
import pytest


@pytest.fixture
def driver():
    driver = webdriver.Firefox()
    driver.get("https://www.saucedemo.com/")
    yield driver
    driver.quit()


@pytest.mark.parametrize(
    "login, password, name, last_name, postal, total, next",
    [
        (
            "standard_user",
            "secret_sauce",
            "тест",
            "тест",
            "195256",
            "Total: $58.29",
            "continue",
        )
    ],
)
@allure.title(
    """Тестирование магазина: {login} {password}
    {name} {last_name} {postal} {total} {next}"""
)
@allure.description("Тест проверяет корректность работы магазина")
@allure.feature("Магазин")
@allure.severity(allure.severity_level.CRITICAL)
def test_shop(login, password, name, last_name, postal, total, next, driver):
    """
    Тест проверяет работу магазина: добавление в корзину товаров
    Возвращение итоговой суммы
    :param login: str - значение логина
    :param password: str - значение пароля
    :param name: str - значение имени
    :param last_name: str - значение фамилии
    :param postal: str - почтовый индекс
    :param total: str - значение итоговой суммы
    """
    auth_page = Auth(driver)
    with allure.step(f"Введение логина {login}"):
        auth_page.input_login(login)
    with allure.step(f"Введение пароля {password}"):
        auth_page.input_password(password)
    with allure.step("Нажатие на кнопку 'submit'"):
        auth_page.submit()

    main_page = MainPage(driver)
    with allure.step("Добавление товаров"):
        main_page.add_goods()
    with allure.step("Переход в корзину"):
        main_page.go_to_cart()

    list = Cart(driver)
    with allure.step("Нажатие на кнопку checkout"):
        list.push_button()

    buy = Order(driver)
    with allure.step(f"Заполнение формы {name} {last_name} {postal} {next}"):
        buy.fill_form(name, last_name, postal, next)
    with allure.step("Проверка итоговой суммы {total}"):
        assert buy.check_cost(total) == total, \
            (f"ожидаемый результат: {total}, "
             f"но получен: {buy.check_cost(total)}")
