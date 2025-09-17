from selenium import webdriver
from Calc import Calculator


def test_calc():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    url = "https://bonigarcia.dev/selenium-webdriver-java/" \
        "slow-calculator.html"
    driver.get(url)

    calc = Calculator(driver)
    calc.input_field()
    calc.input_symbols()
    calc.waiting()
    actual = calc.check()
    expected = "15"
    assert actual == expected
