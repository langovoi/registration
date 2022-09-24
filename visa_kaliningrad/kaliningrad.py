import random
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta


import undetected_chromedriver as uc
from time import sleep

import os, sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from driver.base_page import BasePage
from utils import telegram, gmm
from selenium import webdriver


class Kaliningrad(BasePage):
    pass


if __name__ == "__main__":
    while True:
        options = webdriver.ChromeOptions()
        options.headless = True
        driver = uc.Chrome(options=options)
        driver.delete_all_cookies()
        driver.get('https://appt.ruserv.visametric.com')
        try:
            # todo - получить email
            email = 'belov.ludvig@mail.ru'
            password = '0SuDKq5g6zThCyaqM7pk'
            f = Kaliningrad(driver)
            f.click_on('//button[@value="ru"]')
            f.type_in('//input', email)
            f.click_on('//span[text()="продолжить"]/..')
            f.click_on('//span[text()="запросить проверочный код"]/..')

            code = ''
            datetime_start = datetime.now()
            while (datetime.now() - datetime_start).total_seconds() / 60.00 < 5:
                soup = gmm.find_regex_in_email_with_title(email, password, 'Проверочный код')
                if soup:
                    break
                sleep(10)
            else:
                telegram.send_doc(f'Калининград: Письмо не пришло {email}', driver.page_source)
            for s in soup:
                text = s.get_text(strip=True)
                code = re.findall("код:(.*?)Игнорируйте", text)[0]

            f.type_in('//input', code)
            f.type_in('//div[@class="v-select__slot"]/input[@type="text"]', 'Калининград')
            f.click_on('//span[@class="v-list-item__mask"]')
            f.click_on('(//input[@type="checkbox"]/..)[1]')
            f.click_on('(//input[@type="checkbox"]/..)[2]')
            f.click_on('//div[@class="v-card__actions"]/button[@type="button"]')
            f.click_on('//div[@class="v-card__actions"]/button[@type="button"]')

            date = ''
            dates = [f"01/{(datetime.today()+ relativedelta(months=m)).strftime('%m/%Y')}" for m in [1, 2]]
            while True:
                try:
                    for d in dates:
                        f.type_in('//div[@class="v-text-field__slot"]/input', d)
                        f.is_element_displayed('//div[@role="progressbar"]//circle')
                        f.is_element_invisible('//div[@role="progressbar"]//circle')
                        alert = f.get_text('//div[@role="alert"]')
                        if 'Ближайшая доступная дата для записи: ' in alert:
                            date = alert.split(": ")[1]
                            telegram.send_doc(f'Калининград: Есть дата: {date}', driver.page_source)
                            break
                        elif 'Нет доступной даты/слота для записи указанного количества заявителей.' in alert:
                            sleep(random.randint(10,60))
                        f.click_on('//div[@class="v-text-field__slot"]/..//button')
                    else:
                        telegram.send_doc('Калининград: Нет дат', driver.page_source)
                        print('sleep 10')
                        sleep(random.randint(60, 120))
                except Exception as e:
                    telegram.send_doc(f'Калининград ошибка: {str(e)}', driver.page_source)
        except Exception as e:
            telegram.send_message(f'Калининград ошибка: {str(e)}')
