import os

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from automated_ui_tests.config import config


@pytest.fixture()
def test_setup():
    global driver
    options = Options()
    if os.environ["PIPELINE"] == "actions":
        options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    driver.maximize_window()

    yield
    driver.close()
    driver.quit()


def test_standard_user_tax(test_setup):
    driver.get(config["url"])
    driver.find_element(By.ID, "user-name").send_keys(config["standard_user"])
    driver.find_element(By.ID, "password").send_keys(config["password"])
    driver.find_element(By.ID, "login-button").click()

    items = driver.find_elements(By.CLASS_NAME, "inventory_item")
    price_total = 0
    for item in items:
        price_total += float(
            item.find_element(By.CLASS_NAME, "inventory_item_price").text[1:]
        )
        item.find_element(By.CLASS_NAME, "btn_primary").click()

    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    driver.find_element(By.ID, "checkout").click()

    driver.find_element(By.ID, "first-name").send_keys(config["standard_user"])
    driver.find_element(By.ID, "last-name").send_keys("test")
    driver.find_element(By.ID, "postal-code").send_keys("12-345")
    driver.find_element(By.ID, "continue").click()

    tax = float(driver.find_element(By.CLASS_NAME, "summary_tax_label").text[6:])
    total = float(driver.find_element(By.CLASS_NAME, "summary_total_label").text[8:])

    assert (tax == round(price_total * 0.08, 2)) and (price_total + tax == total)
