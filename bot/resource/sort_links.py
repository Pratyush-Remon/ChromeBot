from typing import KeysView
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from time import sleep



def init_driver():
    options = Options()
    driver = uc.Chrome()
    return driver

driver = init_driver()

driver.get('https://opensource.saucelabs.com/')

sleep(8)

driver.find_element(By.TAG_NAME,'body').send_keys(Keys.CONTROL + 't')

sleep(2)



