import os
import sys
from time import sleep

import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from utils import telegram

def monitor_thai():
    sleep(1)
    driver.find_element(By.XPATH, '//button[@class="button button--red"]').click()
    soup = BeautifulSoup(driver.page_source, "lxml")
    dates = soup.find_all("a", {'class': 'ui-state-default'})
    dates_str = [d.text for d in dates]
    date_time_dict = []
    for date in dates_str:
        driver.find_element(By.XPATH, f'//a[text() = "{date}"]').click()
        sleep(1)
        times = [time.get_attribute('value').replace('T', ' ') for time in
                 driver.find_elements(By.XPATH, '//input[@class="radio"]')]
        date_time_dict = date_time_dict + times
    return date_time_dict


if __name__ == '__main__':
    time_dict_collection = []
    time_dict_application = []
    url_collection = 'https://my.linistry.com/Customer/ReserveTime?b=127&serviceMenuItemId=13929'
    url_application = 'https://my.linistry.com/Customer/ReserveTime?b=127&serviceMenuItemId=1195'
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = uc.Chrome(use_subprocess=True, options=options)
    driver.implicitly_wait(20)

    while True:
        driver.delete_all_cookies()
        driver.get(url_collection)
        date_time_dict = monitor_thai()
        if date_time_dict != time_dict_collection:
            message = '\n'.join(date_time_dict)
            telegram.send_message(f'🇹🇭Таиланд даты collection:\n {message}')
            time_dict_collection = date_time_dict
        driver.delete_all_cookies()
        driver.get(url_application)
        date_time_dict = monitor_thai()
        if date_time_dict != time_dict_application:
            message = '\n'.join(date_time_dict)
            telegram.send_message(f'🇹🇭Таиланд даты application:\n {message}')
            time_dict_application = date_time_dict
        sleep(10)
