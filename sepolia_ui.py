from time import sleep
import sys

import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from utils import telegram

if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = uc.Chrome(options=options)
    driver.get('https://faucet-sepolia.rockx.com/')
    driver.find_element(By.XPATH, '//input[@placeholder="Paste the tweet URL here"]').send_keys(sys.argv[1])
    driver.find_element(By.XPATH, '//button[text()="Send Me ETH"]').click()
    locator = By.XPATH, '//div[contains(@class, "arco-message-wrapper-top")]'
    expected_condition = ec.presence_of_element_located(locator)
    try:
        print(WebDriverWait(driver, 10).until(expected_condition, message=f'Не могу найти').text)
    except Exception:
        driver.save_screenshot('screenshot.png')
        telegram.send_image('screenshot.png', 'No message')
    #'Funding request accepted'
