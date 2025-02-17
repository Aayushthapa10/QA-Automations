from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
class Drivers:
    chromeDriver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))