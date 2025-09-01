import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--width=1200")
    options.add_argument("--height=800")
    service = Service()  # Если нужно, укажите путь к geckodriver
    driver = webdriver.Firefox(service=service, options=options)
    yield driver
    driver.quit()

def test_saucedemo_checkout(driver):
    wait = WebDriverWait(driver, 10)

    # Открыть сайт
    driver.get("https://www.saucedemo.com/")

    # Авторизация стандартным пользователем
    wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    # Добавление товаров в корзину
    wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))).click()
    driver.find_element(By.ID, "add-to-cart-sauce-labs-bolt-t-shirt").click()
    driver.find_element(By.ID, "add-to-cart-sauce-labs-onesie").click()

    # Переход в корзину
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

    # Нажать Checkout
    wait.until(EC.element_to_be_clickable((By.ID, "checkout"))).click()

    # Заполнить форму
    wait.until(EC.visibility_of_element_located((By.ID, "first-name"))).send_keys("Иван")
    driver.find_element(By.ID, "last-name").send_keys("Иванов")
    driver.find_element(By.ID, "postal-code").send_keys("123456")

    # Нажать Continue
    driver.find_element(By.ID, "continue").click()

    # Прочитать итоговую стоимость (Total)
    total_label = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "summary_subtotal_label")))
    total_text = total_label.text  # Пример: "Item total: $58.29"

    # Закрывать браузер будет фикстура

    # Проверка суммы
    assert "$58.29" in total_text, f"Ожидалась сумма $58.29, но получена: {total_text}"

