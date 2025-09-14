import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class CalculatorPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 60)
        
        # Локаторы
        self.delay_input = (By.ID, "delay")
        self.result_display = (By.CLASS_NAME, "screen")
        
        # Маппинг кнопок
        self.buttons = {
            "0": (By.XPATH, "//span[text()='0']"),
            "1": (By.XPATH, "//span[text()='1']"),
            "2": (By.XPATH, "//span[text()='2']"),
            "3": (By.XPATH, "//span[text()='3']"),
            "4": (By.XPATH, "//span[text()='4']"),
            "5": (By.XPATH, "//span[text()='5']"),
            "6": (By.XPATH, "//span[text()='6']"),
            "7": (By.XPATH, "//span[text()='7']"),
            "8": (By.XPATH, "//span[text()='8']"),
            "9": (By.XPATH, "//span[text()='9']"),
            "+": (By.XPATH, "//span[text()='+']"),
            "-": (By.XPATH, "//span[text()='-']"),
            "*": (By.XPATH, "//span[text()='×']"),
            "/": (By.XPATH, "//span[text()='÷']"),
            "=": (By.XPATH, "//span[text()='=']"),
            "C": (By.XPATH, "//span[text()='C']")
        }

    def open(self):
        self.driver.get("https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html")
        self.wait.until(EC.presence_of_element_located(self.delay_input))
        print("Калькулятор загружен")
        return self

    def set_delay(self, delay_value):
        delay_field = self.wait.until(EC.visibility_of_element_located(self.delay_input))
        delay_field.clear()
        delay_field.send_keys(str(delay_value))
        print(f"Задержка установлена: {delay_value} секунд")
        return self

    def press_button(self, button_text):
        """Нажимает кнопку и проверяет, что она нажалась"""
        if button_text not in self.buttons:
            raise ValueError(f"Кнопка '{button_text}' не найдена")
            
        button_locator = self.buttons[button_text]
        button = self.wait.until(EC.element_to_be_clickable(button_locator))
        
        # Получаем текущий текст дисплея перед нажатием
        current_display = self.get_display_text()
        
        button.click()
        print(f"Нажата кнопка: '{button_text}'")
        
        # Небольшая пауза после нажатия
        time.sleep(0.5)
        
        # Проверяем, что дисплей изменился (для цифр и операторов)
        if button_text in "0123456789+-*/":
            new_display = self.get_display_text()
            if new_display == current_display:
                print(f"Предупреждение: дисплей не изменился после нажатия '{button_text}'")
        
        return self

    def get_display_text(self):
        """Возвращает текущий текст на дисплее"""
        try:
            display = self.driver.find_element(*self.result_display)
            return display.text.strip()
        except:
            return ""

    def wait_for_calculation_result(self, timeout=50):
        """
        Ожидает завершения вычисления и возвращает результат
        Отличается от wait_for_result тем, что ждет именно РЕЗУЛЬТАТ вычисления,
        а не просто изменение текста на дисплее
        """
        print(f"Ожидаем результат вычисления (таймаут: {timeout} секунд)...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                display_text = self.get_display_text()
                print(f"Текущий текст дисплея: '{display_text}'")
                
                # Пропускаем пустые значения и символ ожидания ⏳
                if not display_text or display_text == "⏳":
                    time.sleep(1)
                    continue
                
                # Проверяем, что это РЕЗУЛЬТАТ вычисления, а не ввод
                # Результат должен быть числом (может содержать только цифры)
                if (display_text.replace('.', '').replace('-', '').isdigit() and 
                    display_text != "7+8" and  # исключаем ввод
                    len(display_text) > 0):
                    
                    print(f"Найден числовой результат: '{display_text}'")
                    return display_text
                
                # Если это все еще ввод (например, "7+8"), продолжаем ждать
                time.sleep(1)
                
            except Exception as e:
                print(f"Ошибка при проверке дисплея: {e}")
                time.sleep(1)
        
        # Таймаут истек
        final_text = self.get_display_text()
        print(f"Таймаут истек. Финальный текст: '{final_text}'")
        self.driver.save_screenshot("calculation_timeout.png")
        raise TimeoutError(f"Результат вычисления не появился за {timeout} секунд")

    def perform_calculation(self, expression, expected_delay=45):
        """Выполняет вычисление и возвращает результат"""
        print(f"Выполняем вычисление: {expression}")
        
        # Нажимаем кнопки по очереди
        for char in expression:
            self.press_button(char)
        
        # После нажатия "=" ждем результат вычисления
        if expression.endswith("="):
            result = self.wait_for_calculation_result(timeout=expected_delay + 10)
            return result
        
        return self.get_display_text()

class TestSlowCalculator(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.calculator = CalculatorPage(self.driver)

    def test_7_plus_8_equals_15_with_45s_delay(self):
        """Тест: 7 + 8 = 15 с задержкой 45 секунд"""
        print("=" * 50)
        print("ТЕСТ: 7 + 8 = 15 с задержкой 45 секунд")
        print("=" * 50)
        
        # Открываем калькулятор
        self.calculator.open()
        
        # Устанавливаем задержку
        self.calculator.set_delay(45)
        
        # Выполняем вычисление и получаем результат
        result = self.calculator.perform_calculation("7+8=", expected_delay=45)
        
        print(f"Финальный результат: '{result}'")
        
        # Проверяем результат
        self.assertEqual(result, "15", f"Ожидалось '15', но получено '{result}'")
        print("✅ Тест пройден успешно!")

    def test_quick_debug_2_plus_3(self):
        """Быстрый тест для отладки: 2 + 3 = 5"""
        print("=" * 50)
        print("БЫСТРЫЙ ТЕСТ: 2 + 3 = 5")
        print("=" * 50)
        
        self.calculator.open()
        self.calculator.set_delay(3)  # Короткая задержка
        result = self.calculator.perform_calculation("2+3=", expected_delay=3)
        
        self.assertEqual(result, "5", f"Ожидалось '5', но получено '{result}'")
        print("✅ Быстрый тест пройден!")

    def tearDown(self):
        self.driver.quit()
        print("Браузер закрыт")
        print("=" * 50)

if __name__ == "__main__":
    # Сначала запустим быстрый тест для проверки логики
    print("Запуск тестов калькулятора...")
    
    # Создаем тестовый suite
    suite = unittest.TestSuite()
    
    # Добавляем тесты в нужном порядке
    suite.addTest(TestSlowCalculator('test_quick_debug_2_plus_3'))
    suite.addTest(TestSlowCalculator('test_7_plus_8_equals_15_with_45s_delay'))
    
    # Запускаем
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if result.wasSuccessful():
        print("🎉 Все тесты пройдены успешно!")
    else:
        print("❌ Некоторые тесты не прошли")