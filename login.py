from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as b
import time

class Login:
    def __init__(self, driver, email, password):
        self.driver=driver
        self.email=email
        self.password=password
        
    def signin(self):
        print('\nOpen the login page...')
        self.driver.get('https://www.facebook.com/')
        print('Open the login page SUCCEED!')
        uid = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#email')))
        uid.click()
        uid.send_keys(self.email)
        pswd=self.driver.find_element_by_css_selector('#pass')
        pswd.click()
        pswd.send_keys(self.password)
        btn=self.driver.find_element_by_css_selector('#u_0_b')
        btn.click()
