from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():
    options = Options()
    service = Service()  # предполагается, что geckodriver в PATH
    driver = webdriver.Firefox(service=service, options=options)

    try:
        driver.get("http://the-internet.herokuapp.com/login")

        wait = WebDriverWait(driver, 10)

        # Ввод username
        username_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
        username_input.send_keys("tomsmith")

        # Ввод password
        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys("SuperSecretPassword!")

        # Нажатие кнопки Login
        login_button = driver.find_element(By.CSS_SELECTOR, "button.radius")
        login_button.click()

        # Ожидание появления зелёной плашки с сообщением
        flash_message = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.flash.success")))
        
        # Вывод текста сообщения (удаляем лишние пробелы и символы новой строки)
        print(flash_message.text.strip())

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
