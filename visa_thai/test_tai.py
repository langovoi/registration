import logging
import os
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

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))


def book_thai(driver):

    try:
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

        name="POPOV IVAN"
        logging.warning("вход в book")
        driver.find_elements(By.XPATH, '//a[contains(@class,"ui-state-default")]')[0].click()
        logging.warning("выбрали дату")
        time = (driver.find_elements(By.XPATH, '//input[@class="radio"]')[0]).get_attribute('value')
        driver.find_elements(By.XPATH, '//input[@class="radio"]/../label[@class="radio-label"]')[0].click()
        driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        logging.warning(f'выбрали время {time}оk')


        for i in range(2):
            driver.find_element(By.XPATH, '//input[@id="name-input"]').clear()
            driver.find_element(By.XPATH, '//input[@id="name-input"]').send_keys(name)
            driver.find_element(By.XPATH, '//div[@class="input-container"]/button[@type="submit" and text()="Done"]').click()
            logging.warning("прописали имя ок")
            phone_field = driver.find_element(By.XPATH, '//input[@class="text-box single-line"]')
            phone_field.clear()
            phone_field.send_keys(sim_phone)
            driver.find_element(By.XPATH, '//div[@class="input-container l-c-my-cust-si--input"]/button').click()
            logging.warning("прописали номер ок ждем код")
            for i in range(2):

                # sim = Sim('malaysia', 'other')
                # sim_phone="297982678"
                # code ="1234"
                # sim_id, sim_phone = sim.sim_id, sim.sim_phone.replace('+60', '')
                # logging.warning(sim_phone)


                # bl = gsheets.GoogleSheets('vk_blacklist')
                # black_list = bl.ws.get_all_values()
                # if [sim_phone] in black_list:
                #     sim.ban_sim()
                #     driver.quit()
                #     return None, None
                # phone_field.send_keys(Keys.BACKSPACE)
                # получить номер из 5sim в simphone
                # code = sim.get_new_code()
                # simsms sms

                for _ in range(5):
                    try:
                        sleep(10)
                        r2 = s.get(
                            f'https://simsms.org/priemnik.php?metod=get_sms&country=th&service=opt19&id= {sim_id}&apikey=cmLKsSpxYQewPk6xDk7kRmlqRU5drw')
                        if r.json()['sms']:
                            new_code = r.json()['sms']
                        else:
                            new_code = None
                        if new_code != latest_code:
                            code = new_code
                            break
                    except Exception:
                        pass
                    sleep(10)
                sleep(3)
                if code:
                    break
                else:
                    driver.find_element(By.XPATH, '//a[contains (@href, "https://my.linistry.com/Customer/")]').click()

                #     sim.ban_sim()
                #
                # driver.quit()

            else:
                raise RuntimeError('otp')
            driver.find_element(By.XPATH, '//input[@id="Pin"]').clear()
            driver.find_element(By.XPATH, '//input[@id="Pin"]').send_keys(code)
            driver.find_element(By.XPATH, '//button[@type="submit" and text()="Done"]').click()
            # чегото вылетает тут, но логика, чтоб выйти из цикла break с этой датой
            # if  driver.find_element(By.XPATH, '//li[contains(text(), "Sorry this appointment is already taken"]').is_displayed():
            #     logging.warning("дата занята")
            #     raise Exception ("дата недоступна ")
            if driver.find_element(By.XPATH,
                                   '//li[text()="Invalid validation code. Please try again!"]').is_displayed():

                driver.find_element(By.XPATH, '//a[contains (@href, "https://my.linistry.com/Customer/")]').click()

            # можно вернуться, выбрать другую дату otp подойдет(новый вводить не нужно)
            else:
                try:
                    #telegram.send_image(driver, f'{name} Зарегестрирован')
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
                    # telegram.send_message(f'Ссылка для{name}: {link_clipb}')

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
