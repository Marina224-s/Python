import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options as EdgeOptions

@pytest.fixture
def driver():
    options = EdgeOptions()
    options.use_chromium = True
    service = EdgeService()  # Убедитесь, что msedgedriver в PATH
    driver = webdriver.Edge(service=service, options=options)
    driver.maximize_window()
    yield driver
    driver.quit()

def test_fill_form_and_check_validation(driver):
    driver.get("https://bonigarcia.dev/selenium-webdriver-java/data-types.html")

    wait = WebDriverWait(driver, 10)

    # Заполнить форму
    fields = {
        "first-name": "Иван",
        "last-name": "Петров",
        "address": "Ленина, 55-3",
        "email": "test@skypro.com",
        "phone": "+7985899998787",
        # zipCode оставить пустым
        "city": "Москва",
        "country": "Россия",
        "position": "QA",
        "company": "SkyPro"
    }

    for field_id, value in fields.items():
        elem = wait.until(EC.presence_of_element_located((By.ID, field_id)))
        elem.clear()
        elem.send_keys(value)

    # Нажать Submit
    submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    submit_button.click()

    # Проверка подсветки
    def has_red_border(elem):
        return "rgb(220, 53, 69)" in elem.value_of_css_property("border-color") or \
               "rgb(255, 0, 0)" in elem.value_of_css_property("border-color") or \
               "red" in elem.value_of_css_property("border-color")

    def has_green_border(elem):
        return "rgb(40, 167, 69)" in elem.value_of_css_property("border-color") or \
               "rgb(0, 128, 0)" in elem.value_of_css_property("border-color") or \
               "green" in elem.value_of_css_property("border-color")

    # Ждем, пока стили обновятся (ожидания)
    zip_code_field = wait.until(EC.presence_of_element_located((By.ID, "zipCode")))

    # Равномерно проверить, что zip code красная подсветка
    assert has_red_border(zip_code_field), "Zip code должен быть подсвечен красным"

    # Проверить остальные поля (кроме zipCode) на зеленую подсветку
    for fid in fields:
        elem = driver.find_element(By.ID, fid)
        assert has_green_border(elem), f"Поле {fid} не подсвечено зеленым"