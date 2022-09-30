

import logging
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
        logging.warning('1')
        options = webdriver.ChromeOptions()
        driver = uc.Chrome(options=options)
        driver.delete_all_cookies()
        driver.get('https://appt.ruserv.visametric.com')
        logging.warning('2')
        try:
            # todo - получить email
            email = 'pavlov.karim@internet.ru'
            password = 'ntFswbuh4wAv1gje4WAk'
            f = Kaliningrad(driver)
            logging.warning('3')
            f.click_on('//button[@value="ru"]')
            f.type_in('//input', email)
            f.click_on('//span[text()="продолжить"]/..')
            f.click_on('//span[text()="запросить проверочный код"]/..')
            if not f.is_element_invisible('//span[text()="запросить проверочный код"]/..'):
                f.click_on('//span[text()="запросить проверочный код"]/..')
            code = ''
            datetime_start = datetime.now()
            logging.warning('4')
            while (datetime.now() - datetime_start).total_seconds() / 60.00 < 5:
                soup = gmm.find_regex_in_email_with_title(email, password, 'Проверочный код')
                if soup:
                    break
                sleep(10)
            else:
                telegram.send_doc(f'Калининград: Письмо не пришло {email}', driver.page_source)
                telegram.send_image(driver, 'Калининград ошибка')
            for s in soup:
                text = s.get_text(strip=True)
                code = re.findall("код:(.*?)Игнорируйте", text)[0]
            logging.warning('5')
            f.type_in('//input', code)
            f.type_in('//div[@class="v-select__slot"]/input[@type="text"]', 'Свердловск')
            f.click_on('//span[@class="v-list-item__mask"]')
            f.click_on('(//input[@type="checkbox"]/..)[1]')
            f.click_on('(//input[@type="checkbox"]/..)[2]')
            f.click_on('//div[@class="v-card__actions"]/button[@type="button"]')
            f.click_on('Шенгенская виза')
            f.click_on('//div[@class="v-card__actions"]/button[@type="button"]')
            logging.warning('6')
            f.type_in('//div[@class="v-select__slot"]//input[@type="text"]', 'Екатеринбург')
            f.click_on('//div[@role="option"]')
            date = ''
            while True:
                dates = [f"01/{(datetime.today() + relativedelta(months=m)).strftime('%m/%Y')}" for m in [1, 2]]
                try:
                    for d in dates:
                        f.type_in('//div[@class="v-text-field__slot"]/input', d)
                        f.is_element_displayed('//div[@role="progressbar"]//circle')
                        f.is_element_invisible('//div[@role="progressbar"]//circle')
                        alert = f.get_text('//div[@role="alert"]')
                        if 'Ближайшая доступная дата' in alert:
                            date = '/'.join(re.findall('(\d+)', alert))
                            telegram.send_doc(f'Калининград: Есть дата: {date}', driver.page_source)
                            new_date = datetime.strptime(date, '%d/%m/%Y') + relativedelta(days=1)
                            date=new_date.strftime('%d/%m/%Y')
                            f.click_on('//div[@class="v-text-field__slot"]/..//button')
                            f.type_in('//div[@class="v-text-field__slot"]/input', date)
                            f.click_on('Далее')
                            f.click_on('Добавить заявителя')
                            # второй запрос кода после далее
                            f.type_in('(//label[text()="Фамилия"]/../input)[1]', 'KOZLOV')
                            f.type_in('(//label[text()="Имя"]/../input)[1]', 'IVAN')
                            f.type_in('//label[text()="Дата рождения"]/../input', '01/05/1988')
                            f.type_in('//label[text()="Номер заграничного паспорта"]/../input', '832167699')
                            f.type_in('//label[text()="Номер телефона"]/../input', '9633994141')
                            f.type_in('//label[text()="E-mail"]/../input', email)
                            f.type_in('(//label[text()="Фамилия"]/../input)[2]', 'Козлов')
                            f.type_in('(//label[text()="Имя"]/../input)[2]', 'Иван')
                            f.type_in('//label[text()="Отчество"]/../input', 'Иванович')
                            f.click_on('//button[text()="Добавить"]')
                            f.click_on('Далее')
                            sleep(10)
                            f.type_in('//input', email)
                            f.click_on('//span[text()="продолжить"]/..')
                            f.click_on('//span[text()="запросить проверочный код"]/..')
                            if not f.is_element_invisible('//span[text()="запросить проверочный код"]/..'):
                                f.click_on('//span[text()="запросить проверочный код"]/..')
                            code = ''
                            datetime_start = datetime.now()
                            logging.warning('4')
                            while (datetime.now() - datetime_start).total_seconds() / 60.00 < 5:
                                soup = gmm.find_regex_in_email_with_title(email, password, 'Проверочный код')
                                if soup:
                                    break
                                sleep(10)
                            else:
                                telegram.send_doc(f'Калининград: Письмо не пришло {email}', driver.page_source)
                                telegram.send_image(driver, 'Калининград ошибка')
                            for s in soup:
                                text = s.get_text(strip=True)
                                code = re.findall("код:(.*?)Игнорируйте", text)[0]
                            logging.warning('5')
                            f.type_in('//input', code)
                            f.type_in('//div[@class="v-select__slot"]//input[@type="text"]', 'Козлов')
                            f.click_on('//div[@role="option"]')
                            f.type_in('//label[text()="Номер общегражданского паспорта"]/../input', '732167999')
                            f.type_in('//label[text()="Дата выдачи"]/../input', '01/05/2022')
                            f.type_in('//label[text()="Выдан"]/../textarea', 'ровд')
                            f.type_in('//label[text()="Адрес регистрации"]/../textarea', "Москва, 15, 15")
                            f.click_on('Далее')
                            f.click_on('//button[not(contains(@class,"--disabled"))]/div/..')
                            f.click_on('//div[contains(@class,"d-flex flex-wrap")]/button[not(contains(@class,"--disabled"))]')
                            f.click_on('Далее')
                            f.click_on('Далее')
                            f.click_on('Оформить запись')



                            break
                        elif 'Нет доступной даты' in alert:
                            sleep(random.randint(10,60))
                        f.click_on('//div[@class="v-text-field__slot"]/..//button')
                    else:
                        telegram.send_doc('Калининград: Нет дат', driver.page_source)
                        logging.warning('Калининград: Нет дат')
                        sleep(random.randint(60, 120))

                except Exception as e:
                    telegram.send_doc(f'Калининград ошибка: {str(e)}', driver.page_source)
        except Exception as e:
            telegram.send_image(driver, 'Калининград ошибка')
            telegram.send_message(f'Калининград ошибка: {str(e)}')
