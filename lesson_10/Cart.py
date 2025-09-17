from selenium.webdriver.common.by import By
import allure


class Cart:
    def __init__(self, driver):
        """
        Конструктор класса Cart.
        :param driver: объект драйвера Selenium
        """
        self.driver = driver

    @allure.step("Нажать кнопку checkout")
    def push_button(self):
        """
        Метод нажимает на кнопку checkout
        :param check: str - текст на кнопке
        """
        checktot = self.driver.find_element(By.ID, "checkout")
        checktot.click()
