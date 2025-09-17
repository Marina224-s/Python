from shop import Auth
from selenium import webdriver
from shop import MainPage
from shop import Cart
from shop import Order


def test_login():
    options = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(options=options)
    driver.get("https://www.saucedemo.com/")

    auth_page = Auth(driver)
    auth_page.input_login()
    auth_page.input_password()
    auth_page.submit()

    main_page = MainPage(driver)
    main_page.add_goods()
    main_page.go_to_cart()

    list = Cart(driver)
    list.push_button()

    buy = Order(driver)
    buy.fill_form()
    total_price = buy.check_cost()
    assert "Total: $58.29" == total_price.text

    driver.quit()
