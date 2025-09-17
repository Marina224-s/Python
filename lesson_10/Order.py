from selenium.webdriver.common.by import By
import allure


class Order:
    def __init__(self, driver):
        """
        Конструктор класса Order.
        :param driver: объект драйвера Selenium
        """
        self.driver = driver

    @allure.step("Заполнить форму {name}, {last_name}, {postal}, {next}")
    def fill_form(self, name, last_name, postal, next):
        """
        Метод заполняет форму данными и нажимает кнопку 'continue'
        :param name: str - значение имени
        :param last_name: str - значение фамилии
        :param postal: str - значение почтового индекса
        :param next: str - текст кнопки, которую нужно нажать
        """

        name_1 = self.driver.find_element(By.CSS_SELECTOR,
                                          "#first-name.input_error.form_input")
        name_1.send_keys(name)

        locator = "#last-name.input_error.form_input"
        last = self.driver.find_element(By.CSS_SELECTOR, locator)

        last.send_keys(last_name)

        loc = "#postal-code.input_error.form_input"
        post = self.driver.find_element(By.CSS_SELECTOR, loc)
        post.send_keys(postal)

        next = self.driver.find_element(By.ID, next)
        next.click()

    @allure.step("Вернуть значение суммы {total}")
    def check_cost(self, total):
        """
        Метод возвращает итоговую сумму корзины
        :param total: str - текст итоговой суммы
        """
        total = self.driver.find_element(By.CSS_SELECTOR,
                                         "div.summary_total_label")
        return total.text
