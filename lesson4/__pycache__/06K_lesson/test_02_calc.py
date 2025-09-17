import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    service = Service()  # Можно указать путь к chromedriver, если он не в PATH
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()

def test_slow_calculator(driver):
    # 1. Открыть страницу
    driver.get("https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html")

    # 2. Ввести 45 в поле #delay
    delay_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#delay"))
    )
    delay_input.clear()
    delay_input.send_keys("45")

    # 3. Нажать кнопки '7', '+', '8', '='
    driver.find_element(By.CSS_SELECTOR, "button[data-value='7']").click()
    driver.find_element(By.CSS_SELECTOR, "button[data-value='+']").click()
    driver.find_element(By.CSS_SELECTOR, "button[data-value='8']").click()
    driver.find_element(By.CSS_SELECTOR, "button[data-value='=']").click()

    # 4. Проверить, что через 45 сек появится результат 15
    result = WebDriverWait(driver, 60).until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#screen"), "15")
    )
    assert result, "Результат не равен 15 после вычисления"
