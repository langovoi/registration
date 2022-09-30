
import undetected_chromedriver as uc
from time import sleep

import os, sys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from driver.base_page import BasePage
from selenium import webdriver


class Facebook(BasePage):
    pass


if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    # options.headless = True
    driver = uc.Chrome(options=options)
    driver.delete_all_cookies()
    driver.get('https://facebook.com')
    f = Facebook(driver)
    f.click_on('//a[@data-testid="open-registration-form-button"]')
    f.type_in('//input[@name="firstname"]', 'Volga')
    f.type_in('//input[@name="lastname"]', 'Struna')
    f.type_in('//input[@name="reg_email__"]', '+79913974763')
    f.type_in('//input[@name = "reg_passwd__"]', 'Ab123456!')
    # #дата рождения по умолчанию сегодня
    f.select_by_text('//select[@id="day"]', '10')
    f.select_by_text('//select[@id="month"]', '10')
    f.select_by_text('//select[@id="year"]', '1979')
    #пол женщина по умолчанию
    f.click_on('//input[@value="1"]')
    #зарегестрировать
    f.click_on('//button[@name="websubmit"]')
    # #вводится код, может приходить смс минуты 3-5
    f.type_in('//input[@id = "code_in_cliff"]', '92726')
    f.click_on('//button[@name="confirm"]')
    sleep(10000)

    #f.click_on('//a[contains (@class, "layerCancel")]')
    #(@ class, "vkuiButton__in")] /..')

    #восстановить пароль по ссылке забыл пароль
    # driver.get('https://https://www.facebook.com/recover/initiate/')
    # #ввести код (проверить на следующем разе)
    # f.type_in('//input[@name="n"]', '1111')
    # f.click_on('//button[@name="reset_action"]')


    print()