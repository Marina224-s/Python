from selenium.webdriver.common.by import By


class Auth:
    def __init__(self, driver):
        self.driver = driver

    def input_login(self):
        login = self.driver.find_element(By.CSS_SELECTOR, "#user-name")
        login.send_keys("standard_user")

    def input_password(self):
        password = self.driver.find_element(By.CSS_SELECTOR, "#password")
        password.send_keys("secret_sauce")

    def submit(self):
        button = self.driver.find_element(By.CSS_SELECTOR, "#login-button")
        button.click()


class MainPage:
    def __init__(self, driver):
        self.driver = driver

    def add_goods(self):

        backpack = self.driver.find_element(By.ID,
                                            "add-to-cart-sauce-labs-backpack")
        backpack.click()

        locator = "add-to-cart-sauce-labs-bolt-t-shirt"
        t_shirt = self.driver.find_element(By.ID, locator)
        t_shirt.click()

        onesie = self.driver.find_element(By.ID,
                                          "add-to-cart-sauce-labs-onesie")
        onesie.click()

    def go_to_cart(self):

        cart = self.driver.find_element(By.CSS_SELECTOR,
                                        "a.shopping_cart_link")
        cart.click()


class Cart:
    def __init__(self, driver):
        self.driver = driver

    def push_button(self):
        check = self.driver.find_element(By.ID, "checkout")
        check.click()


class Order:
    def __init__(self, driver):
        self.driver = driver

    def fill_form(self):

        name = self.driver.find_element(By.CSS_SELECTOR,
                                        "#first-name.input_error.form_input")
        name.send_keys("test")

        locator = "#last-name.input_error.form_input"
        last_name = self.driver.find_element(By.CSS_SELECTOR, locator)

        last_name.send_keys("test")

        loc = "#postal-code.input_error.form_input"
        postal = self.driver.find_element(By.CSS_SELECTOR, loc)
        postal.send_keys("195256")

        next = self.driver.find_element(By.ID, "continue")
        next.click()

    def check_cost(self):
        total = self.driver.find_element(By.CSS_SELECTOR,
                                         "div.summary_total_label")
        return total
