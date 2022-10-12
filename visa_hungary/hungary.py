import logging
import random
from datetime import datetime, timezone

import undetected_chromedriver as uc
from time import sleep

import os, sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from utils import telegram
from driver.base_page import BasePage
from selenium import webdriver

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


class Hungary(BasePage):
    pass


def register(thread):
    time = datetime(2022, 10, 12, 22, 00, tzinfo=timezone.utc)
    # time = datetime(2022, 10, 12, 16, 53, tzinfo=timezone.utc)
    options = webdriver.ChromeOptions()
    # options.headless = True
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # driver.maximize_window()
    # driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver = uc.Chrome(options=options, use_subprocess=True)
    driver.delete_all_cookies()
    driver.get('https://konzinfoidopont.mfa.gov.hu/')
    f = Hungary(driver)
    # sleep(6)
    f.click_on('//button[@id="langSelector"]')
    f.click_on('//img[@alt="Русский"]')
    #
    # sleep(2)
    driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.ID, 'toptowindow'))
    while True:
        try:
            f.click_on('//label[text()="Место предоставления услуги"]/..//button[text()="Выбор места"]')
            break
        except Exception as e:
            sleep(0.1)
    f.type_in('//input[@placeholder="Поиск"]', 'Беларусь')
    f.click_on('//label[text()="Беларусь - Минск"]')
    f.click_on('//label[text()="Тип дела"]/..//button[text()="Добавление типа услуги"]')
    f.type_in('//h5[text()="Типы дел"]/../..//input[@placeholder="Поиск"]', 'типа С')
    f.click_on('//label[contains(text(),"Заявление о выдаче визы (краткосрочная шенгенская виза типа С)")]')
    f.click_on('Сохранить')
    f.type_in('//input[@id="label4"]', 'VALSADDINOV')
    f.type_in('//input[@id="birthDate"]', '02/11/1981')
    element2 = driver.find_element(By.ID, 'label9')
    driver.execute_script("arguments[0].scrollIntoView();", element2)
    # sleep(2)
    f.type_in('//input[@id="label9"]', '+375222235458')
    f.type_in('//input[@id="label10"]', 'qwe1232@bk.ru')
    f.type_in('//input[@id="label1000"]', 'AB4123323')
    driver.execute_script("arguments[0].scrollIntoView();",
                          driver.find_element(By.XPATH, '//button[text()="Перейти  к выбору времени"]'))
    sleep(2)
    while True:
        try:
            f.click_on('//input[@id="slabel13"]')
            break
        except Exception as e:
            sleep(0.1)
    while True:
        try:
            f.click_on('//input[@id="label13"]')
            break
        except Exception as e:
            sleep(0.1)
    while True:
        dt = datetime.now(tz=timezone.utc)
        if time <= dt:
            print('dt:', dt)
            break

    # sleep(3)
    while True:
        while True:
            try:
                f.click_on('//button[text()="Перейти  к выбору времени"]')
                break
            except Exception as e:
                sleep(0.1)
        if f.is_element_displayed('//span[text()="Свободно"]'):
            while True:
                try:
                    f.click_on('(//span[text()="Свободно"])[last()]')
                    break
                except Exception as e:
                    print('click')
                    sleep(0.1)
            # тут похоже начинает работать бан, кнопка не всегда работает, нужно переключать ip
            # может попробовать рандомом кликать по элементам, перемотка вроде помогает немного
            element3 = driver.find_element(By.ID, 'nextTo3')
            driver.execute_script("arguments[0].scrollIntoView();", element3)
            while True:
                try:
                    f.click_on('//button[@id="nextTo3"]')
                    break
                except Exception as e:
                    sleep(0.1)
            element4 = driver.find_element(By.XPATH, '//button[text()="Завершение бронирования"]')
            driver.execute_script("arguments[0].scrollIntoView();", element4)
            while True:
                try:
                    # telegram.send_message(f'{thread}: {datetime.now()}')
                    f.click_on('Завершение бронирования')
                    telegram.send_doc('Венгрия: успешно зарегистрирован', driver.page_source)
                    break
                except Exception as e:
                    sleep(0.1)
        else:
            telegram.send_doc('Венгрия: успешно зарегистрирован', driver.page_source)
            if f.is_element_displayed('//button[text()="Хорошо"]'):
                while True:
                    try:
                        f.click_on('//button[text()="Хорошо"]')
                        break
                    except Exception as e:
                        sleep(0.1)


if __name__ == "__main__":
    register('1')
