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
    while True:
        try:
            options = webdriver.ChromeOptions()
            options.headless = True
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
            driver.delete_all_cookies()
            driver.get('https://consulat.gouv.fr/ru/ambassade-de-france-a-minsk/appointment')
            f = France(driver)
            while True:
                f.click_on('Доступ к услугам')
                if f.is_element_displayed('//button[text()="Нет"]'):
                    f.click_on('//button[text()="Нет"]')
                f.click_on('Подтвердить')
                f.click_on('Я прочитал')
                f.click_on('Назначить встречу')
                if f.is_element_displayed('На сегодня нет свободных мест.'):
                    sleep(5)
                    telegram.send_doc('Франция: Нет дат', driver.page_source)
                else:
                    sleep(5)
                    telegram.send_doc('Франия: Есть даты!', driver.page_source, debug=False)
                logging.warning('Франция нет дат')
                sleep(random.randint(100, 120))
                driver.refresh()
        except Exception as e:
            sleep(5)
            try:
                telegram.send_doc(f'Франция ошибка: {str(e)}', driver.page_source)
                driver.quit()
            except Exception:
                pass
            sleep(10)
