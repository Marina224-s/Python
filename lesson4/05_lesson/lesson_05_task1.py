from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def main():
    # Опции для запуска Chrome
    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')

    # Путь к chromedriver, если он не в PATH, укажите явно, например:
    # service = Service('/path/to/chromedriver')
    service = Service()  # если chromedriver в PATH
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Открываем страницу
        driver.get("http://uitestingplayground.com/classattr")

        # Ждем, чтобы страница загрузилась (можно заменить на более умный WebDriverWait)
        time.sleep(2)

        # На странице есть несколько кнопок, синий класс "btn-primary"
        button = driver.find_element(By.CSS_SELECTOR, "button.btn-primary")
        button.click()

        # Можно подождать, если есть какое-то визуальное подтверждение
        time.sleep(2)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
    

