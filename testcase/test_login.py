import unittest
from locator.locators import Locators
from locator.drivers import Drivers
from pages.login_page import LoginPage

class LoginTestCase(unittest.TestCase):
    def setUp(self) -> None:
        dr = Drivers()
        self.l = Locators()
        self.driver = dr.chromeDriver
        self.driver.maximize_window()
        self.driver.get(self.l.url)

    def testlogin(self):
        login = LoginPage(self.driver)
        login.loginPage(self.l.username,self.l.password)


    def tearDown(self) -> None:
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
