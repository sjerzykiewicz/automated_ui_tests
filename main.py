from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait

url = "https://www.saucedemo.com/"
options = Options()
driver = webdriver.Firefox(options=options)

driver.maximize_window()

wait = WebDriverWait(driver, 60)

driver.get(url)
