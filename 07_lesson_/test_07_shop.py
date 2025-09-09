from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time

# Класс для страницы авторизации
class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_input = (By.ID, "user-name")
        self.password_input = (By.ID, "password")
        self.login_button = (By.ID, "login-button")

    def login(self, username, password):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.username_input)
        ).send_keys(username)
        
        self.driver.find_element(*self.password_input).send_keys(password)
        self.driver.find_element(*self.login_button).click()

# Класс для главной страницы магазина
class ProductsPage:
    def __init__(self, driver):
        self.driver = driver
        self.cart_icon = (By.CLASS_NAME, "shopping_cart_link")
        self.cart_badge = (By.CLASS_NAME, "shopping_cart_badge")
        self.menu_button = (By.ID, "react-burger-menu-btn")
        self.reset_link = (By.ID, "reset_sidebar_link")
        self.close_menu = (By.ID, "react-burger-cross-btn")

    def add_product_to_cart(self, product_name):
        # Правильные ID кнопок добавления в корзину
        product_id_map = {
            "Sauce Labs Backpack": "add-to-cart-sauce-labs-backpack",
            "Sauce Labs Bolt T-Shirt": "add-to-cart-sauce-labs-bolt-t-shirt", 
            "Sauce Labs Onesie": "add-to-cart-sauce-labs-onesie"
        }
        
        if product_name in product_id_map:
            add_button = (By.ID, product_id_map[product_name])
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(add_button)
            ).click()
            print(f"Добавлен товар: {product_name}")
        else:
            raise ValueError(f"Товар {product_name} не найден в маппинге")

    def go_to_cart(self):
        cart_icon = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.cart_icon)
        )
        cart_icon.click()

    def get_cart_count(self):
        try:
            badge = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.cart_badge)
            )
            return int(badge.text)
        except:
            return 0

    def reset_app_state(self):
        # Открываем меню
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.menu_button)
        ).click()
        
        # Сбрасываем состояние приложения
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.reset_link)
        ).click()
        
        # Ждем завершения сброса
        time.sleep(2)
        
        # Закрываем меню (если видимо)
        try:
            close_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.close_menu)
            )
            close_btn.click()
        except:
            pass

    def continue_shopping(self):
        continue_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "continue-shopping"))
        )
        continue_btn.click()

# Класс для страницы корзины
class CartPage:
    def __init__(self, driver):
        self.driver = driver
        self.checkout_button = (By.ID, "checkout")
        self.remove_buttons = (By.CSS_SELECTOR, ".cart_button")
        self.continue_shopping_btn = (By.ID, "continue-shopping")

    def click_checkout(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.checkout_button)
        ).click()

    def get_cart_items(self):
        items = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item_name"))
        )
        return [el.text for el in items]

    def clear_cart(self):
        # Удаляем все товары из корзины
        remove_buttons = self.driver.find_elements(*self.remove_buttons)
        for button in remove_buttons:
            if button.text == "REMOVE":
                button.click()
                time.sleep(0.5)

    def continue_shopping(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.continue_shopping_btn)
        ).click()

# Класс для страницы оформления заказа
class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver
        self.first_name_input = (By.ID, "first-name")
        self.last_name_input = (By.ID, "last-name")
        self.postal_code_input = (By.ID, "postal-code")
        self.continue_button = (By.ID, "continue")
        self.total_price_label = (By.CLASS_NAME, "summary_total_label")

    def fill_info(self, first_name, last_name, postal_code):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.first_name_input)
        ).send_keys(first_name)
        
        self.driver.find_element(*self.last_name_input).send_keys(last_name)
        self.driver.find_element(*self.postal_code_input).send_keys(postal_code)
        
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.continue_button)
        ).click()

    def get_total(self):
        total_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.total_price_label)
        )
        total_text = total_element.text
        # пример текста: "Total: $58.29"
        return total_text.split("$")[1].strip()

class SauceDemoTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.saucedemo.com/")
        self.driver.maximize_window()

    def test_purchase_flow(self):
        login_page = LoginPage(self.driver)
        login_page.login("standard_user", "secret_sauce")

        # Ждем загрузки главной страницы
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
        )

        products_page = ProductsPage(self.driver)
        
        # Сбрасываем состояние приложения перед началом теста
        print("Сбрасываем состояние приложения...")
        products_page.reset_app_state()
        
        # Ждем обновления страницы после сброса
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
        )
        
        # Проверяем, что корзина пуста
        initial_cart_count = products_page.get_cart_count()
        print(f"Товаров в корзине после сброса: {initial_cart_count}")
        
        # Добавляем товары в корзину
        products_to_add = ["Sauce Labs Backpack", "Sauce Labs Bolt T-Shirt", "Sauce Labs Onesie"]
        
        for product in products_to_add:
            products_page.add_product_to_cart(product)
            time.sleep(1)  # Пауза для стабильности
        
        # Проверяем, что добавлено правильное количество товаров
        cart_count = products_page.get_cart_count()
        print(f"Товаров в корзине после добавления: {cart_count}")
        self.assertEqual(cart_count, 3, f"В корзине должно быть 3 товара, но найдено {cart_count}")
        
        products_page.go_to_cart()

        cart_page = CartPage(self.driver)
        
        # Проверяем товары в корзине
        expected_items = ["Sauce Labs Backpack", "Sauce Labs Bolt T-Shirt", "Sauce Labs Onesie"]
        actual_items = cart_page.get_cart_items()
        
        print(f"Ожидаемые товары: {expected_items}")
        print(f"Фактические товары: {actual_items}")
        
        # Сортируем списки для сравнения
        self.assertEqual(sorted(expected_items), sorted(actual_items), "В корзине не все ожидаемые товары")
        
        cart_page.click_checkout()

        checkout_page = CheckoutPage(self.driver)
        checkout_page.fill_info("Имя", "Фамилия", "12345")
        
        # Ждем появления итоговой суммы
        total = checkout_page.get_total()
        print(f"Итоговая стоимость: ${total}")

        # Проверяем, что итоговая сумма равна 58.29
        self.assertEqual(total, "58.29", "Итоговая сумма не равна $58.29")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()