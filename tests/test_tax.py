import os

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from automated_ui_tests.config import config
from automated_ui_tests.page_objects.page import Page


@pytest.fixture()
def test_setup():
    global driver
    options = Options()
    if "GITHUB_TOKEN" in os.environ:
        options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    driver.maximize_window()

    yield
    driver.close()
    driver.quit()


def test_standard_user_tax(test_setup):
    """
    Test if tax is calculated correctly and if total price is correct
    """
    driver.get(config["url"])
    driver.find_element(By.XPATH, Page.user_name).send_keys(config["standard_user"])
    driver.find_element(By.XPATH, Page.password).send_keys(config["password"])
    driver.find_element(By.XPATH, Page.login_button).click()

    items = driver.find_elements(By.CLASS_NAME, Page.items_class)
    price_total = 0
    for item in items:
        price_total += float(
            item.find_element(By.CLASS_NAME, Page.item_price_class).text[1:]
        )
        item.find_element(By.CLASS_NAME, Page.item_buy_btn_class).click()

    driver.find_element(By.CLASS_NAME, Page.shopping_cart_class).click()
    driver.find_element(By.XPATH, Page.checkout_btn).click()

    driver.find_element(By.XPATH, Page.first_name).send_keys(config["standard_user"])
    driver.find_element(By.XPATH, Page.last_name).send_keys("test")
    driver.find_element(By.XPATH, Page.postal_code).send_keys("12-345")
    driver.find_element(By.XPATH, Page.continue_btn).click()

    tax = float(driver.find_element(By.CLASS_NAME, Page.tax_label).text[6:])
    total = float(driver.find_element(By.CLASS_NAME, Page.total_label).text[8:])

    assert (tax == round(price_total * 0.08, 2)) and (price_total + tax == total)
