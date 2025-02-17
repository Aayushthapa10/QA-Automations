import time

from selenium.webdriver.common.by import By
from locator.locators import Locators

class LoginPage:
    def __init__(self,driver):
        self.l = Locators()
        self.driver = driver

    def loginPage(self,username,password):
        driver = self.driver
        l = self.l
        driver.find_element(By.ID, l.nav_login_id).click()
        driver.implicitly_wait(10)
        driver.find_element(By.ID, l.textbox_username_id).send_keys(username)
        driver.find_element(By.ID, l.textbox_password_id).send_keys(password)
        driver.find_element(By.XPATH, l.button_login_xpath).click()
        time.sleep(10)
