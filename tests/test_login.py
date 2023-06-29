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


def test_users_login(test_setup):
    driver.get(config["url"])
    result = True
    for user in ["standard_user", "problem_user", "performance_glitch_user"]:
        driver.find_element(By.XPATH, Page.user_name).send_keys(config[user])
        driver.find_element(By.XPATH, Page.password).send_keys(config["password"])
        driver.find_element(By.XPATH, Page.login_button).click()

        cookies = driver.get_cookies()
        cookies_dict = {}
        for cookie in cookies:
            cookies_dict[cookie["name"]] = cookie["value"]

        result = cookies_dict["session-username"] == config[user]

        driver.find_element(By.XPATH, Page.burger_menu).click()
        driver.find_element(By.XPATH, Page.logout).click()
    assert result


def test_locked_out_user_login(test_setup):
    driver.get(config["url"])
    driver.find_element(By.XPATH, Page.user_name).send_keys(config["locked_out_user"])
    driver.find_element(By.XPATH, Page.password).send_keys(config["password"])
    driver.find_element(By.XPATH, Page.login_button).click()

    assert (
        driver.find_element(
            By.XPATH,
            Page.alert_box,
        ).text
        == "Epic sadface: Sorry, this user has been locked out."
    )
