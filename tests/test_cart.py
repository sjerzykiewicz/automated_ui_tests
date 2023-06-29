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

    global page
    page = Page(driver)

    yield
    driver.close()
    driver.quit()


def test_standard_user_cart_prices(test_setup):
    """
    Test if cart total price is equal to sum of items prices
    """
    driver.get(config["url"])
    page.login(config["standard_user"], config["password"])

    items = driver.find_elements(By.CLASS_NAME, Page.items_class)
    price_total = 0
    for item in items:
        price_total += float(
            item.find_element(By.CLASS_NAME, Page.item_price_class).text[1:]
        )
        item.find_element(By.CLASS_NAME, Page.item_buy_btn_class).click()

    page.checkout()

    page.fill_checkout_form()

    total = float(
        driver.find_element(By.CLASS_NAME, Page.subtotal_label_class).text[13:]
    )

    assert total == price_total


def test_standard_user_cart_items(test_setup):
    """
    Test if cart contains all items added to it
    """
    driver.get(config["url"])
    page.login(config["standard_user"], config["password"])

    items = driver.find_elements(By.CLASS_NAME, Page.items_class)
    total_items = []
    for i, item in enumerate(items):
        if i % 2 == 0:
            total_items.append(
                item.find_element(By.CLASS_NAME, Page.item_name_class).text
            )
            item.find_element(By.CLASS_NAME, Page.item_buy_btn_class).click()

    page.checkout()

    page.fill_checkout_form()

    cart_items = []
    cart_list = driver.find_elements(By.CLASS_NAME, Page.cart_items_class)
    for cart in cart_list:
        cart_items.append(cart.find_element(By.CLASS_NAME, Page.item_name_class).text)

    assert set(total_items) == set(cart_items)
