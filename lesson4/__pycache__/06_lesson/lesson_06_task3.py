from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

try:
    driver.get("https://bonigarcia.dev/selenium-webdriver-java/loading-images.html")
    
    wait = WebDriverWait(driver, 10)
    
    # Ждём появления минимум 4 картинок
    wait.until(lambda d: len(d.find_elements(By.TAG_NAME, "img")) >= 4)
    
    # После того, как 4 картинки появились, ждём, пока у 4-й картинки загрузится атрибут src
    wait.until(lambda d: d.find_elements(By.TAG_NAME, "img")[3].get_attribute("src") != "")
    
    # Получаем src 3-й картинки
    third_img_src = driver.find_elements(By.TAG_NAME, "img")[2].get_attribute("src")
    
    print(third_img_src)

finally:
    driver.quit()