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
    if "GITHUB_TOKEN" in os.environ:
        options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    driver.maximize_window()

    yield
    driver.close()
    driver.quit()


def test_standard_user_cart_prices(test_setup):
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

    total = float(
        driver.find_element(By.CLASS_NAME, "summary_subtotal_label").text[13:]
    )

    assert total == price_total


def test_standard_user_cart_items(test_setup):
    driver.get(config["url"])
    driver.find_element(By.ID, "user-name").send_keys(config["standard_user"])
    driver.find_element(By.ID, "password").send_keys(config["password"])
    driver.find_element(By.ID, "login-button").click()

    items = driver.find_elements(By.CLASS_NAME, "inventory_item")
    total_items = []
    for i, item in enumerate(items):
        if i % 2 == 0:
            total_items.append(
                item.find_element(By.CLASS_NAME, "inventory_item_name").text
            )
            item.find_element(By.CLASS_NAME, "btn_primary").click()

    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    driver.find_element(By.ID, "checkout").click()

    driver.find_element(By.ID, "first-name").send_keys(config["standard_user"])
    driver.find_element(By.ID, "last-name").send_keys("test")
    driver.find_element(By.ID, "postal-code").send_keys("12-345")
    driver.find_element(By.ID, "continue").click()

    cart_items = []
    cart_list = driver.find_elements(By.CLASS_NAME, "cart_item")
    for cart in cart_list:
        cart_items.append(cart.find_element(By.CLASS_NAME, "inventory_item_name").text)

    assert set(total_items) == set(cart_items)
