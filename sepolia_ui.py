import sys

import telebot
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    # options.headless = True
    driver = uc.Chrome(options=options)
    try:
        driver.get('https://faucet-sepolia.rockx.com/')
        driver.find_element(By.XPATH, '//input[@placeholder="Paste the tweet URL here"]').send_keys(sys.argv[1])
        driver.find_element(By.XPATH, '//button[text()="Send Me ETH"]').click()
        locator = By.XPATH, '//div[contains(@class, "arco-message-wrapper-top")]'
        expected_condition = ec.presence_of_element_located(locator)
        print(WebDriverWait(driver, 20).until(expected_condition, message=f'Не могу найти').text)
    except Exception:
        driver.find_element(By.XPATH, '//input[@placeholder="Paste the tweet URL here"]').send_keys(sys.argv[1])
        driver.find_element(By.XPATH, '//button[text()="Send Me ETH"]').click()
        try:
            locator = By.XPATH, '//div[contains(@class, "arco-message-wrapper-top")]'
            expected_condition = ec.presence_of_element_located(locator)
            print(WebDriverWait(driver, 20).until(expected_condition, message=f'Не могу найти').text)
        except Exception:
            bot = telebot.TeleBot("1275523107:AAF_5t_r80J55Pl-JcVeLcVVOsl7kadqAc4")
            chat_id = -745819635
            bot.send_photo(chat_id=chat_id, photo=driver.get_screenshot_as_png(), caption='Fail')
            bot.stop_bot()
            #'Funding request accepted'
