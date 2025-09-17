from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


class Calculator:
    def __init__(self, driver):
        """
        Конструктор класса Calculator.
        :param driver: объект драйвера Selenium
        """
        self.driver = driver

    @allure.step("Найти поле ожидания по локатору")
    @allure.step("Отправить в поле {delay} значение")
    def set_delay(self, delay) -> None:
        """
        Находит по локатору поле ожидания
        Отправляет в него число
        :param time: int - время задержки в секундах
        """
        delay_element = self.driver.find_element(By.CSS_SELECTOR, "#delay")
        delay_element.clear()
        delay_element.send_keys(delay)

    @allure.step("Кликнуть по кнопкам '{button}'")
    def click_buttons(self, button):
        """
        Нажимает на кнопки калькулятора по очереди.
        :param buttons: list[str] — список текстов на кнопках,
        которые нужно нажать.
        """
        button = self.driver.find_element(By.CSS_SELECTOR,
                                          "span.btn.btn-outline-primary")
        button.click()

        locator = ("span.operator.btn.btn-outline-success")
        button = self.driver.find_element(By.CSS_SELECTOR, locator)
        button.click()

        button = self.driver.find_element(By.XPATH, "//span[text()='8']")
        button.click()

        button = self.driver.find_element(By.CSS_SELECTOR,
                                          "span.btn.btn-outline-warning")
        button.click()

    @allure.step("Ожидание результата {expected_result}")
    def waiting_for_result(self, expected_result, delay):
        """
        Задает время ожидания
        :param delay: int - время задержки в секундах
        :param expected_result:
        """
        wait = WebDriverWait(self.driver, delay)
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,
                                                    "div.screen"),
                                                    expected_result))

    @allure.step("Получить результат")
    def get_result(self):
        """
        Возвращает текст результата поля
        :param result: str - выводимый результат
        """
        field = self.driver.find_element(By.CSS_SELECTOR, "div.screen")
        result = field.text
        return result
