import clipboard
import undetected_chromedriver as uc
from time import sleep

import os, sys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from driver.base_page import BasePage
from selenium import webdriver


class Facebook(BasePage):
    pass


if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    # options.headless = True
    driver = uc.Chrome(options=options)
    driver.delete_all_cookies()
    driver.get('https://facebook.com')
    f = Facebook(driver)
    f.click_on('//a[@data-testid="open-registration-form-button"]')
    f.type_in('//input[@name="firstname"]', 'Valentin')
    f.type_in('//input[@name="lastname"]', 'Strykalo')
