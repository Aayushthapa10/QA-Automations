import unittest
from locator.locators import Locators
from locator.drivers import Drivers
from pages.login_page import LoginPage
from pages.product_page import ProductPage

class BaseTestCase(unittest.TestCase):
    def setUp(self) -> None:
        dr = Drivers()
        self.l = Locators()
        self.driver = dr.chromeDriver
        self.driver.maximize_window()
        self.driver.get(self.l.url)

    def tearDown(self) -> None:
        self.driver.quit()

class LoginTestCase(BaseTestCase):
    def testlogin(self):
        login = LoginPage(self.driver)
        login.loginPage(self.l.username, self.l.password)

class AddProductToCartTestCase(BaseTestCase):
    def test_add_product_to_cart(self):
        product_page = ProductPage(self.driver)

        # Select a product (this could be by name, image, etc.)
        product_page.select_product(self.l.product_name)

        # Add to cart
        product_page.add_to_cart(self.l.add_to_cart_button)

        # Optionally, go to cart to verify
        product_page.go_to_cart(self.l.cart_button)

        # Example: Verify product is in cart (check cart page for the product)
        # cart_items = self.driver.find_elements(By.CSS_SELECTOR, "cart item locator")
        # self.assertTrue(len(cart_items) > 0, "Product is not in cart.")

if __name__ == '__main__':
    unittest.main()
