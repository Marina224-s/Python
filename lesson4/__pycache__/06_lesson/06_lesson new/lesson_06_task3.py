from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://bonigarcia.dev/selenium-webdriver-java/loading-images.html")

wait = WebDriverWait(driver, 15)

# Ждём загрузки всех изображений (минимум 4)
wait.until(lambda d: len(d.find_elements(By.TAG_NAME, "img")) >= 4)

# Ждём, пока у 4-й картинки (индекс 3) появится атрибут src
wait.until(lambda d: d.find_elements(By.TAG_NAME, "img")[3].get_attribute("src"))

# Получаем 4-ю картинку (которая является третьей по заданию)
third_image = driver.find_elements(By.TAG_NAME, "img")[3]
wait.until(EC.text_to_be_present_in_element((By.ID, "loading-bar"), "Done"))

# Выводим src
print(third_image.get_attribute("src"))

driver.quit()