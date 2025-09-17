from selenium.webdriver.common.by import By
import allure


class Auth:
    def __init__(self, driver):
        """
        Конструктор класса Cart.
        :param driver: объект драйвера Selenium
        """
        self.driver = driver

    @allure.step("Заполнить логин {login}")
    def input_login(self, login):
        """
        Метод заполняет поле "Логин"
        :param login: str - значение логина
        """
        log = self.driver.find_element(By.CSS_SELECTOR, "#user-name")
        log.send_keys(login)

    @allure.step("Заполнить пароль {password}")
    def input_password(self, password):
        """
        Метод заполняет поле "Пароль"
        :param password: str - значение пароля
        """
        pass_word = self.driver.find_element(By.CSS_SELECTOR, "#password")
        pass_word.send_keys(password)

    @allure.step("Нажать ккнопку Submit")
    def submit(self):
        """
        Нажимает кнопку Submit
        """
        button = self.driver.find_element(By.CSS_SELECTOR, "#login-button")
        button.click()
