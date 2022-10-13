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
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from multiprocessing import Pool


class Hungary(BasePage):
    pass



def register(thread):
    time = datetime(2022, 10, 12, 22, 00, tzinfo=timezone.utc)
    # time = datetime(2022, 10, 12, 16, 53, tzinfo=timezone.utc)
    options = webdriver.ChromeOptions()
    options.headless = True

    # driver = webdriver.Firefox(options=options)
    # sleep(5)


    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # driver.maximize_window()

    # driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    # driver = uc.Chrome(options=options, use_subprocess=True)
    driver = uc.Chrome(options=options)
    driver.delete_all_cookies()

    # driver.maximize_window()
    driver.get('https://konzinfoidopont.mfa.gov.hu/')
    f = Hungary(driver)
    print('Создали драйвер. Открыли сайт')
    f.click_on_while('//button[@id="langSelector"]')
    while True:
        if f.is_element_displayed('//div[@class="dropdown-menu language show"]//img[@alt="Русский"]'):
            f.click_on('//img[@alt="Русский"]')
            print('Выбрали язык')
            break
        else:
            print('Глюк селектора выбора языка.Еще заход')
            f.click_on('//button[@id="langSelector"]')

    # sleep(1)
    # driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.ID, 'toptowindow'))
    while True:
        try:
            f.click_on('//label[text()="Место предоставления услуги"]/..//button[text()="Выбор места"]')
            break
        except Exception as e:
            sleep(0.1)
    while True:
        try:
            f.type_in('//input[@placeholder="Поиск"]', 'Беларусь')
            break
        except Exception as e:
            sleep(0.1)
    f.click_on_while('//label[text()="Беларусь - Минск"]')
    print('Выбрали Беларусь')
    f.click_on_while('//label[text()="Тип дела"]/..//button[text()="Добавление типа услуги"]')
    f.type_in('//h5[text()="Типы дел"]/../..//input[@placeholder="Поиск"]', 'D')
    f.click_on_while('//label[contains(text(),"разрешение на проживание - D")]')

    # f.type_in('//h5[text()="Типы дел"]/../..//input[@placeholder="Поиск"]', 'типа С')
    # f.click_on_while('//label[contains(text(),"Заявление о выдаче визы (краткосрочная шенгенская виза типа С)")]')
    f.click_on_while('Сохранить')
    print('Выбрали Тип услуги')
    f.type_in('//input[@id="label4"]', 'BOJARCHUK SERGEY')
    print('Ввод имя')
    f.type_in('//input[@id="birthDate"]', '02/12/1988')
    print('Ввод рождение')
    # element2 = driver.find_element(By.ID, 'label9')
    # driver.execute_script("arguments[0].scrollIntoView();", element2)
    # sleep(2)
    f.type_in('//input[@id="label9"]', '+375298239958')
    print('Ввод телефон')
    f.type_in('//input[@id="label10"]', 'sergei_bojarchuk@mail.ru')
    print('Ввод почта')
    f.type_in('//input[@id="label1000"]', 'MC9756323')
    print('Ввод паспорт')
    # driver.execute_script("arguments[0].scrollIntoView();",
    #                       driver.find_element(By.XPATH, '//button[text()="Перейти  к выбору времени"]'))
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
    print('Поставили галки')
    # sleep(3)
    while True:
        while True:
            try:
                f.click_on('//button[text()="Перейти  к выбору времени"]')
                break
            except Exception as e:
                sleep(0.1)
        print('Нажали выбор даты')
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
            # element3 = driver.find_element(By.ID, 'nextTo3')
            # driver.execute_script("arguments[0].scrollIntoView();", element3)
            print('Выбрали дату')
            while True:
                try:
                    f.click_on('//button[@id="nextTo3"]')
                    break
                except Exception as e:
                    sleep(0.1)
            # element4 = driver.find_element(By.XPATH, '//button[text()="Завершение бронирования"]')
            # driver.execute_script("arguments[0].scrollIntoView();", element4)
            print('Нажали далее')
            while True:
                try:
                    # telegram.send_message(f'{thread}: {datetime.now()}')
                    f.click_on('Завершение бронирования')
                    print('ЗАПИСАН(ИМЯ):', datetime.now(tz=timezone.utc))
                    telegram.send_doc('Венгрия: успешно зарегистрирован(ИМЯ)', driver.page_source)
                    break
                except Exception as e:
                    sleep(0.1)
        else:
            telegram.send_doc('Венгрия: нет дат', driver.page_source)
            if f.is_element_displayed('//button[text()="Хорошо"]'):
                while True:
                    try:
                        f.click_on('//button[text()="Хорошо"]')
                        break
                    except Exception as e:
                        sleep(0.1)


if __name__ == "__main__":
    register('1')
    # with Pool(4) as p:
    #     p.map(register, ['1', '2', '3', '4'])
        # register('1')
        # pool.close()
        # pool.join()
