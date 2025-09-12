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
        return ProductsPage(self.driver)

# Класс для главной страницы магазина
class ProductsPage:
    def __init__(self, driver):
        self.driver = driver
        self.cart_icon = (By.CLASS_NAME, "shopping_cart_link")
        self.cart_badge = (By.CLASS_NAME, "shopping_cart_badge")

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
        return self

    def go_to_cart(self):
        cart_icon = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.cart_icon)
        )
        cart_icon.click()
        return CartPage(self.driver)

    def get_cart_count(self):
        try:
            badge = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.cart_badge)
            )
            return int(badge.text)
        except:
            return 0

# Класс для страницы корзины
class CartPage:
    def __init__(self, driver):
        self.driver = driver
        self.checkout_button = (By.ID, "checkout")
        self.remove_buttons = (By.CSS_SELECTOR, "button.cart_button")
        self.continue_shopping_btn = (By.ID, "continue-shopping")
        self.cart_items = (By.CLASS_NAME, "inventory_item_name")

    def click_checkout(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.checkout_button)
        ).click()
        return CheckoutPage(self.driver)

    def get_cart_items(self):
        items = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(self.cart_items)
        )
        return [el.text for el in items]

    def clear_cart_if_needed(self):
        """Очищает корзину, если в ней есть товары"""
        try:
            remove_buttons = WebDriverWait(self.driver, 5).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.cart_button"))
            )
            for button in remove_buttons:
                if button.text == "REMOVE":
                    button.click()
                    time.sleep(0.3)
            print("Корзина очищена")
        except:
            print("Корзина уже пуста")
        return self

    def continue_shopping(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.continue_shopping_btn)
        ).click()
        return ProductsPage(self.driver)

# Класс для страницы оформления заказа
class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver
        self.first_name_input = (By.ID, "first-name")
        self.last_name_input = (By.ID, "last-name")
        self.postal_code_input = (By.ID, "postal-code")
        self.continue_button = (By.ID, "continue")
        self.total_price_label = (By.CLASS_NAME, "summary_total_label")
        self.finish_button = (By.ID, "finish")

    def fill_info(self, first_name, last_name, postal_code):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.first_name_input)
        ).send_keys(first_name)
        
        self.driver.find_element(*self.last_name_input).send_keys(last_name)
        self.driver.find_element(*self.postal_code_input).send_keys(postal_code)
        
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.continue_button)
        ).click()
        return self

    def get_total(self):
        total_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.total_price_label)
        )
        total_text = total_element.text
        # пример текста: "Total: $58.29"
        return total_text.split("$")[1].strip()

    def finish_checkout(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.finish_button)
        ).click()
        return self

class SauceDemoTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.saucedemo.com/")
        self.driver.maximize_window()

    def test_purchase_flow(self):
        # Авторизация
        login_page = LoginPage(self.driver)
        products_page = login_page.login("standard_user", "secret_sauce")

        # Ждем загрузки главной страницы
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
        )

        # Проверяем корзину и очищаем если нужно
        cart_count = products_page.get_cart_count()
        if cart_count > 0:
            print(f"В корзине уже есть {cart_count} товаров, очищаем...")
            cart_page = products_page.go_to_cart()
            cart_page.clear_cart_if_needed()
            products_page = cart_page.continue_shopping()
            # Ждем обновления страницы
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
            )

        # Добавляем товары в корзину
        products_to_add = ["Sauce Labs Backpack", "Sauce Labs Bolt T-Shirt", "Sauce Labs Onesie"]
        
        for product in products_to_add:
            products_page.add_product_to_cart(product)
            time.sleep(0.5)

        # Проверяем количество товаров в корзине
        cart_count = products_page.get_cart_count()
        print(f"Товаров в корзине после добавления: {cart_count}")
        self.assertEqual(cart_count, 3, f"В корзине должно быть 3 товара, но найдено {cart_count}")
        
        # Переходим в корзину
        cart_page = products_page.go_to_cart()
        
        # Проверяем товары в корзине
        expected_items = ["Sauce Labs Backpack", "Sauce Labs Bolt T-Shirt", "Sauce Labs Onesie"]
        actual_items = cart_page.get_cart_items()
        
        print(f"Ожидаемые товары: {expected_items}")
        print(f"Фактические товары: {actual_items}")
        
        # Сортируем списки для сравнения
        self.assertEqual(sorted(expected_items), sorted(actual_items), "В корзине не все ожидаемые товары")
        
        # Переходим к оформлению заказа
        checkout_page = cart_page.click_checkout()
        checkout_page.fill_info("Имя", "Фамилия", "12345")
        
        # Получаем итоговую сумму
        total = checkout_page.get_total()
        print(f"Итоговая стоимость: ${total}")

        # Проверяем итоговую сумму
        self.assertEqual(total, "58.29", "Итоговая сумма не равна $58.29")
        
        # Завершаем заказ
        checkout_page.finish_checkout()
        print("Заказ успешно оформлен!")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()