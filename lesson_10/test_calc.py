from selenium import webdriver
from Calculator import Calculator
import allure
import pytest


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    url = "https://bonigarcia.dev/selenium-webdriver-java/" \
        "slow-calculator.html"
    driver.get(url)
    yield driver
    driver.quit()


@pytest.mark.parametrize("num1, operation, num2, expected_result, delay",
                         [
                             ("7", "+", "8", "15", "45")
                         ])
@allure.title("Тестирование калькулятора: {num1} {operation} {num2} "
              "= {expected_result}")
@allure.description("Тест проверяет корректность работы калькулятора "
                    "с опрецией сложения.")
@allure.feature("Калькулятор")
@allure.severity(allure.severity_level.CRITICAL)
def test_calculator(num1, operation, num2, expected_result, delay, driver):
    """
    Тест проверяет работу калькулятора с операцией +.

    :param driver: WebDriver — объект драйвера, переданный фикстурой.
    :param num1: str — первое число для операции.
    :param operation: str — операция (+).
    :param num2: str — второе число для операции.
    :param expected_result: str — ожидаемый результат операции.
    :param delay: int — задержка в секундах для выполнения операции.
    """
    calc = Calculator(driver)
    with allure.step(f"Установка задержки {delay} секунд"):
        calc.set_delay(delay)
    with allure.step(f"Нажатие кнопок: {num1}, {operation}, {num2}, '='"):
        calc.click_buttons([num1, operation, num2, "="])
    with allure.step(f"Ожидание результата {expected_result}"):
        calc.waiting_for_result(expected_result, delay)
    with allure.step("Проверка результата"):
        assert calc.get_result() == expected_result, \
            (f"Ожидаемый результат: {expected_result}, "
             f"но получен: {calc.get_result()}")
