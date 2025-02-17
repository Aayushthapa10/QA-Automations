import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locator.locators import Locators

class ProductPage:
    def __init__(self, driver):
        self.driver = driver
        self.l = Locators()

    def select_product(self):
        # Wait for the product element to be clickable before selecting
        product = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.l.product_name))
        )
        product.click()

    def add_to_cart(self):
        # Wait for the "Add to Cart" button to be clickable before clicking it
        add_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.l.add_to_cart_button))
        )
        add_button.click()

    def go_to_cart(self):
        # Wait for the cart button to be clickable
        cart_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.l.cart_button))
        )
        cart_button.click()
