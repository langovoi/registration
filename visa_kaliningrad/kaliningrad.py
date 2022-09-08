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
from utils import telegram
from selenium import webdriver


class Kaliningrad(BasePage):
    pass


if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    # options.headless = True
    driver = uc.Chrome(options=options)
    try:
        driver.get('https://temp-mail.org')
        driver.find_element(By.XPATH, '//div').send_keys()
        driver.find_element(By.XPATH, '//div').click()
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@data-clipboard-action="copy"]'))).click()
        Copy = driver.find_element_by_xpath('//*[@id="click-to-copy"]')
        Copy.click()
        email = clipboard.paste()
        driver.get('https://ruserv.visametric.com/apsys/')
        k = Kaliningrad(driver)
        k.is_element_invisible('Data Loading...', timeout=360)
        k.click_on('ru')
        # get email
        k.type_in('//input[@type="text"]', 'Калининградская область')
        k.type_in('//input[@id="input-59"]', 'Калининградская область')
        k.click_on('//span[text()="Калининградская область"]')
        sleep(1)
        k.click_on('//input[@id="input-64"]/..')
        k.click_on('//input[@id="input-69"]/..')
        k.click_on('Далее')
        k.click_on('Далее')

        k.type_in('//input[@id="input-178"]', 'Калининград')
        k.click_on('//div[@id="list-item-200-0"]')
        available_date = False
        dates = ['01/10/2022', '01/12/2022']
        for i in range(len(dates)):
            k.type_in('//input[@id="input-190"]', dates[i])
            k.is_element_invisible('Проверка ближайшей доступной даты подачи документов', timeout=120)
            if k.is_element_displayed('Нет доступной даты', timeout=60):
                sleep(5)
                k.click_on('//input[@id="input-190"]/../..//button[@aria-label="clear icon"]')
            else:
                telegram.send_doc(f'Калининград: Есть дата', driver.page_source)
                break
    except Exception as e:
        telegram.send_doc(f'Калининград: Ошибка {str(e)}', driver.page_source)
    driver.quit()
