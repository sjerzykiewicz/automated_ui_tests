from selenium.webdriver.common.by import By


class Page:
    def __init__(self, driver):
        self.driver = driver

    user_name = "/html/body/div[1]/div/div[2]/div[1]/div/div/form/div[1]/input"
    password = "/html/body/div[1]/div/div[2]/div[1]/div/div/form/div[2]/input"
    login_button = "/html/body/div[1]/div/div[2]/div[1]/div/div/form/input"

    burger_menu = "/html/body/div[1]/div/div/div[1]/div[1]/div[1]/div/div[1]/div/button"
    logout_btn = (
        "/html/body/div[1]/div/div/div[1]/div[1]/div[1]/div/div[2]/div[1]/nav/a[3]"
    )

    alert_box = "/html/body/div[1]/div/div[2]/div[1]/div/div/form/div[3]/h3"

    items_class = "inventory_item"
    item_name_class = "inventory_item_name"
    item_price_class = "inventory_item_price"
    item_buy_btn_class = "btn_primary"
    shopping_cart_class = "shopping_cart_link"

    checkout_btn = "/html/body/div/div/div/div[2]/div/div[2]/button[2]"
    first_name = "/html/body/div/div/div/div[2]/div/form/div[1]/div[1]/input"
    last_name = "/html/body/div/div/div/div[2]/div/form/div[1]/div[2]/input"
    postal_code = "/html/body/div/div/div/div[2]/div/form/div[1]/div[3]/input"
    continue_btn = "/html/body/div/div/div/div[2]/div/form/div[2]/input"

    subtotal_label_class = "summary_subtotal_label"
    cart_items_class = "cart_item"

    tax_label = "summary_tax_label"
    total_label = "summary_total_label"

    def login(self, user, password):
        self.driver.find_element(By.XPATH, self.user_name).send_keys(user)
        self.driver.find_element(By.XPATH, self.password).send_keys(password)
        self.driver.find_element(By.XPATH, self.login_button).click()

    def logout(self):
        self.driver.find_element(By.XPATH, self.burger_menu).click()
        self.driver.find_element(By.XPATH, self.logout_btn).click()

    def checkout(self):
        self.driver.find_element(By.CLASS_NAME, self.shopping_cart_class).click()
        self.driver.find_element(By.XPATH, self.checkout_btn).click()

    def fill_checkout_form(self):
        self.driver.find_element(By.XPATH, self.first_name).send_keys("test")
        self.driver.find_element(By.XPATH, self.last_name).send_keys("test")
        self.driver.find_element(By.XPATH, self.postal_code).send_keys("12-345")
        self.driver.find_element(By.XPATH, self.continue_btn).click()
