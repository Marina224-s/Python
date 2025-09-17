import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class CalculatorPage:
    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get("https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html")
        time.sleep(2)

    def set_delay(self, delay_value):
        delay_field = self.driver.find_element(By.ID, "delay")
        delay_field.clear()
        delay_field.send_keys(str(delay_value))

    def press_button(self, button_text):
        button = self.driver.find_element(By.XPATH, f"//span[text()='{button_text}']")
        button.click()
        time.sleep(0.5)

    def get_result(self):
        """Просто ждет 46 секунд и возвращает результат"""
        time.sleep(46)
        display = self.driver.find_element(By.CLASS_NAME, "screen")
        return display.text.strip()

class TestSlowCalculator(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.calc = CalculatorPage(self.driver)

    def test_7_plus_8_equals_15_with_45s_delay(self):
        # Открываем калькулятор
        self.calc.open()
        
        # Устанавливаем задержку
        self.calc.set_delay(15)
        
        # Нажимаем кнопки
        self.calc.press_button("7")
        self.calc.press_button("+")
        self.calc.press_button("8")
        self.calc.press_button("=")
        
        # Ждем результат
        result = self.calc.get_result()
        
        # Проверяем
        self.assertEqual(result, "15")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()