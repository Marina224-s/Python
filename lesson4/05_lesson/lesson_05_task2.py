from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():
    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')
    service = Service()  # Если chromedriver в PATH

    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get("http://uitestingplayground.com/dynamicid")

        wait = WebDriverWait(driver, 10)
        # Кнопка на странице меняет id, невозможно ориентироваться на id,
        # ищем кнопку по классам и тексту.
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-primary') and text()='Button']")))
        button.click()

        # Для наглядности можно подождать, например 2 секунды
        wait.until(EC.staleness_of(button))
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
