import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

from automated_ui_tests.config import config


@pytest.fixture()
def test_setup():
    global driver
    driver = webdriver.Firefox()

    driver.maximize_window()

    yield
    driver.close()
    driver.quit()


def test_standard_user_login(test_setup):
    driver.get(config["url"])
    driver.find_element(By.ID, "user-name").send_keys(config["standard_user"])
    driver.find_element(By.ID, "password").send_keys(config["password"])
    driver.find_element(By.ID, "login-button").click()

    cookies = driver.get_cookies()
    cookies_dict = {}
    for cookie in cookies:
        cookies_dict[cookie["name"]] = cookie["value"]

    assert cookies_dict["session-username"] == config["standard_user"]


def test_locked_out_user_login(test_setup):
    driver.get(config["url"])
    driver.find_element(By.ID, "user-name").send_keys(config["locked_out_user"])
    driver.find_element(By.ID, "password").send_keys(config["password"])
    driver.find_element(By.ID, "login-button").click()

    assert (
        driver.find_element(
            By.XPATH,
            '//*[@id="login_button_container"]/div/form/div[3]/h3',
        ).text
        == "Epic sadface: Sorry, this user has been locked out."
    )
