import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture()
def test_setup():
    global driver
    driver = webdriver.Firefox()

    driver.maximize_window()

    yield
    driver.close()
    driver.quit()


def test_login(test_setup):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
