from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("http://uitestingplayground.com/ajax")
driver.find_element(By.ID, "ajaxButton").click()

wait = WebDriverWait(driver, 20)

# Проверка наличия элемента
elems = driver.find_elements(By.CLASS_NAME, "bg-success")
print(f"Найдено элементов с классом bg-success до ожидания: {len(elems)}")

try:
    text_element = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "bg-success"))
    )
    print("Текст:", text_element.text)
except Exception as e:
    print("Ошибка ожидания элемента:", e)

driver.quit()