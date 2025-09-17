from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Calculator:
    def __init__(self, driver):
        self.driver = driver

    def input_field(self):
        number = self.driver.find_element(By.CSS_SELECTOR, "#delay")
        number.clear()
        number.send_keys("45")

    def input_symbols(self):
        button = self.driver.find_element(By.CSS_SELECTOR,
                                          "span.btn.btn-outline-primary")
        button.click()

        locator = ("span.operator.btn.btn-outline-success")
        button_plus = self.driver.find_element(By.CSS_SELECTOR, locator)
        button_plus.click()

        button_eight = self.driver.find_element(By.XPATH, "//span[text()='8']")
        button_eight.click()

        button_equal = self.driver.find_element(By.CSS_SELECTOR,
                                                "span.btn.btn-outline-warning")
        button_equal.click()

    def waiting(self):
        wait = WebDriverWait(self.driver, 45)
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,
                                                    "div.screen"), "15"))

    def check(self):
        field = self.driver.find_element(By.CSS_SELECTOR, "div.screen")
        result = field.text
        return result
