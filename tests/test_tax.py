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


def test_standard_user_tax(test_setup):
    """
    Test if tax is calculated correctly and if total price is correct
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

    tax = float(driver.find_element(By.CLASS_NAME, Page.tax_label).text[6:])
    total = float(driver.find_element(By.CLASS_NAME, Page.total_label).text[8:])

    assert (tax == round(price_total * 0.08, 2)) and (price_total + tax == total)
