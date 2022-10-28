import logging
import os
import re
import sys
from time import sleep

import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from utils import telegram

# добавить
from utils.sim import Sim
import pyperclip as pc
from selenium.webdriver.common.alert import Alert
import requests
import re 

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))


def book_thai(driver):

    try:
        name="POP IVA"
        logging.warning("вход в book")
        driver.find_elements(By.XPATH, '//a[contains(@class,"ui-state-default")]')[0].click()
        logging.warning("выбрали дату")
        time = (driver.find_elements(By.XPATH, '//input[@class="radio"]')[0]).get_attribute('value')
        driver.find_elements(By.XPATH, '//input[@class="radio"]/../label[@class="radio-label"]')[0].click()
        driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        logging.warning(f'выбрали время {time}оk')


        for i in range(2):
            s = requests.Session()
            code = None
            latest_code = None
            # баланс
            # r=s.get(f'https://simsms.org/priemnik.php?metod=get_balance&service=opt4&apikey=cmLKsSpxYQewPk6xDk7kRmlqRU5drw')
            # номер
            r = s.get(
                f'https://simsms.org/priemnik.php?metod=get_number&country=TH&service=opt19&apikey=cmLKsSpxYQewPk6xDk7kRmlqRU5drw')
            if r.json()['number']:
                sim_phone = r.json()['number']
                sim_id = r.json()['id']
            logging.warning(sim_phone)

            driver.find_element(By.XPATH, '//input[@id="name-input"]').clear()
            driver.find_element(By.XPATH, '//input[@id="name-input"]').click()
            driver.find_element(By.XPATH, '//input[@id="name-input"]').send_keys(name)
            driver.find_element(By.XPATH, '//div[@class="input-container"]/button[@type="submit" and text()="Done"]').click()
            logging.warning("прописали имя ок")

            driver.find_element(By.XPATH, '//div[@class="selected-dial-code"]').click()
            driver.find_element(By.XPATH, '//span[@class="country-name" and  contains(text(), "Thailand")]').click()
            phone_field = driver.find_element(By.XPATH, '//input[@class="text-box single-line"]')
            phone_field.clear()
            phone_field.send_keys(sim_phone)
            driver.find_element(By.XPATH, '//div[@class="input-container l-c-my-cust-si--input"]/button').click()
            logging.warning("прописали номер ок ждем код")


            for _ in range(5):
                try:
                    s2 = requests.Session()
                    r2 = s2.get(f'https://simsms.org/priemnik.php?metod=get_sms&country=TH&service=opt19&id={sim_id}&apikey=cmLKsSpxYQewPk6xDk7kRmlqRU5drw')
                    sleep(5)
                    if r2.json()['sms']:
                        new_code_str = r2.json()['sms']
                        new_code = re.findall(r'\d+', new_code_str)
                    else:
                        new_code = None
                    if new_code != latest_code:
                        code = new_code
                        logging.warning(code)
                        break
                except Exception as e:
                    logging.warning(f'Сбой кода: {str(e)}')
                sleep(5)
            if code:
                break

            else:
                driver.find_element(By.XPATH, '//a[contains (@href, "https://my.linistry.com/Customer/")]').click()


        driver.find_element(By.XPATH, '//input[@id="Pin"]').clear()
        driver.find_element(By.XPATH, '//input[@id="Pin"]').send_keys(code)
        driver.find_element(By.XPATH, '//button[@type="submit" and text()="Done"]').click()
        try:

        # чегото вылетает тут, но логика можно, чтоб выйти из цикла с этой датой
            if  driver.find_element(By.XPATH, '//li[contains(text(), "Sorry this appointment is already taken"]').is_displayed():
                logging.warning("дата занята")
                raise Exception ("дата недоступна ")
            if driver.find_element(By.XPATH,
                                  '//li[text()="Invalid validation code. Please try again!"]').is_displayed():
                driver.find_element(By.XPATH, '//a[contains (@href, "https://my.linistry.com/Customer/")]').click()
        except:
            pass


        # можно вернуться, выбрать другую дату otp подойдет(новый вводить не нужно)

        try:
            telegram.send_image(driver, f'{name} Зарегестрирован')
            #отмена записи кнопкой ниже альтернатива:
            # actions = ActionChains(driver)
            #
            # element = driver.find_element(By.XPATH, '//div[@class="ticket__bottom-cta-decor"]')
            # try:
            #     actions.move_to_element(element).perform()
            # except Exception:
            #     sleep(2)
            #     actions.move_to_element(element).perform()
            # element.click()

            driver.find_element(By.XPATH, '//button[@id="ticketDropDown"]').click()
            driver.find_element(By.XPATH, '//a[contains(@id, "ticket-copy-link")]').click()
            driver.switch_to.alert.accept()
            link_clipb = pc.paste()
            logging.warning(f'Зарегестрирован. Ссылка для{name}: {link_clipb}')
            telegram.send_message(f'Ссылка для{name}: {link_clipb}')

            # !!!отмена реги!!!варнинг!!
            # driver.find_element(By.XPATH, '//a[contains(@id, "ticket-signout")]').click()
            # driver.switch_to.alert.accept()
            # logging.warning(f'рега для {name}')
        except Exception as exc:
            logging.warning(f'Сбой во время отмены: {str(exc)}')
    except Exception as ex:
        logging.warning(f'Таиланд Неизвестная ошибка при букинге или нет дат: {str(ex)}')






if __name__ == '__main__':
    url_collection = 'https://my.linistry.com/Customer/ReserveTime?b=127&serviceMenuItemId=13929'
    url_application = 'https://my.linistry.com/Customer/ReserveTime?b=127&serviceMenuItemId=1195'
    url_link_test = 'https://my.linistry.com/Customer/Ticket/_ohjbN'

    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    driver = uc.Chrome(options=options)
    driver.implicitly_wait(20)
    driver.delete_all_cookies()
    driver.get(url_application)

    driver.find_element(By.XPATH, '//button[@class="button button--red"]').click()

    book_thai(driver)
