from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():
    firefox_options = Options()
    firefox_options.add_argument('--start-maximized')
    service = Service()  # Если geckodriver в PATH

    driver = webdriver.Firefox(service=service, options=firefox_options)

    try:
        driver.get("http://the-internet.herokuapp.com/inputs")

        wait = WebDriverWait(driver, 10)
        input_field = wait.until(EC.presence_of_element_located((By.TAG_NAME, "input")))

        input_field.send_keys("Sky")
        input_field.clear()
        input_field.send_keys("Pro")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
