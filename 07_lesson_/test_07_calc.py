from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest

class CalculatorPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 60)
        self.delay_input_locator = (By.CSS_SELECTOR, "#delay")
        self.result_locator = (By.CSS_SELECTOR, "#result")

    def set_delay(self, seconds):
        delay_input = self.wait.until(EC.visibility_of_element_located(self.delay_input_locator))
        delay_input.clear()
        delay_input.send_keys(str(seconds))

    def press_button(self, button_text):
        button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//span[text()='{button_text}']")
        ))
        button.click()

    def get_result_text(self):
        result = self.wait.until(EC.visibility_of_element_located(self.result_locator))
        return result.text

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()  # или другой драйвер
        self.driver.get("https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html")
        self.calc_page = CalculatorPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_calculation(self):
        self.calc_page.set_delay(45)  # Пример: выставляем задержку 2 секунды
        self.calc_page.press_button("7")
        self.calc_page.press_button("+")
        self.calc_page.press_button("8")
        self.calc_page.press_button("=")

        result = self.calc_page.get_result_text()
        self.assertEqual(result, "15")  # ожидаемый результат

if __name__ == "__main__":
    unittest.main()
