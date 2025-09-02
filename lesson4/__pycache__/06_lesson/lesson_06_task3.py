from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://bonigarcia.dev/selenium-webdriver-java/loading-images.html")

wait = WebDriverWait(driver, 15)

# Ждём появления как минимум 3-х элементов img
wait.until(lambda d: len(d.find_elements(By.TAG_NAME, "img")) >= 3)

# Ждём, пока у всех трёх картинок не появится атрибут src и он будет не пустой
wait.until(lambda d: all(
    img.get_attribute("src") for img in d.find_elements(By.TAG_NAME, "img")[:3]
))

# Получаем 3-ю картинку
third_image = driver.find_elements(By.TAG_NAME, "img")[2]

# Выводим src
print(third_image.get_attribute("src"))

driver.quit()

