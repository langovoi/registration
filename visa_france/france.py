import logging
import random

import undetected_chromedriver as uc
from time import sleep

import os, sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from utils import telegram
from driver.base_page import BasePage

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

class France(BasePage):
    pass


if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    driver = uc.Chrome(options=options)
    while True:
        try:
            options.headless = True
            driver.delete_all_cookies()
            driver.get('https://consulat.gouv.fr/ru/ambassade-de-france-a-minsk/appointment')
            f = France(driver)
            if 'Bad Gateway' not in driver.page_source:
                f.click_on('Доступ к услугам')
                if f.is_element_displayed('//button[text()="Нет"]'):
                    f.click_on('//button[text()="Нет"]')
                f.click_on('Подтвердить')
                f.click_on('Я прочитал')
                f.click_on('Назначить встречу')
                if not f.is_element_displayed('На сегодня нет свободных мест.'):
                    sleep(5)
                    telegram.send_doc('Франия: Есть даты!', driver.page_source, debug=False)
                logging.warning('Франция нет дат')
            else:
                telegram.send_doc('Франция: Ошибка 502', driver.page_source, debug=False)
        except Exception as e:
            try:
                telegram.send_doc('Франция: Неизвестная ошибка', driver.page_source, debug=False)
            except Exception:
                telegram.send_message('Франция: Неизвестная ошибка', debug=False)
        sleep(random.randint(100, 120))