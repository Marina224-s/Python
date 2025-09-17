from selenium.webdriver.common.by import By
import allure


class MainPage:
    def __init__(self, driver):
        """
        Конструктор класса MainPage.
        :param driver: объект драйвера Selenium
        """
        self.driver = driver

    @allure.step("Добавить товары в корзину")
    def add_goods(self):
        """
        Метод добавляет товары в корзину
        """

        backpack = self.driver.find_element(By.ID,
                                            "add-to-cart-sauce-labs-backpack")
        backpack.click()

        locator = "add-to-cart-sauce-labs-bolt-t-shirt"
        t_shirt = self.driver.find_element(By.ID, locator)
        t_shirt.click()

        onesie = self.driver.find_element(By.ID,
                                          "add-to-cart-sauce-labs-onesie")
        onesie.click()

    @allure.step("Перейти в корзину")
    def go_to_cart(self):
        """
        Метод осуществляет переход в корзину
        """
        cart = self.driver.find_element(By.CSS_SELECTOR,
                                        "a.shopping_cart_link")
        cart.click()
