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

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

class Hungary(BasePage):
    pass


if __name__ == "__main__":
    # try:

    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    # driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    # driver = uc.Chrome(options=options)
    driver.delete_all_cookies()
    driver.get('https://konzinfoidopont.mfa.gov.hu/')
    f = Hungary(driver)
    sleep(6)
    f.click_on('//button[@id="langSelector"]')
    f.click_on('//img[@alt="Русский"]')
    element = driver.find_element(By.ID, 'toptowindow')
    driver.execute_script("arguments[0].scrollIntoView();", element)
    sleep(2)
    f.click_on('//label[text()="Место предоставления услуги"]/..//button[text()="Выбор места"]')
    f.type_in('//input[@placeholder="Поиск"]', 'Беларусь')
    f.click_on('//label[text()="Беларусь - Минск"]')
    f.click_on('//label[text()="Тип дела"]/..//button[text()="Добавление типа услуги"]')
    f.type_in('//h5[text()="Типы дел"]/../..//input[@placeholder="Поиск"]', 'D')
    f.click_on('//label[contains(text(),"Заявление о выдаче визы")]')
    f.click_on('Сохранить')
    f.type_in('//input[@id="label4"]', 'PETROV')
    f.type_in('//input[@id="birthDate"]', '19/10/1990')
    element2 = driver.find_element(By.ID, 'label9')
    driver.execute_script("arguments[0].scrollIntoView();", element2)
    sleep(2)
    f.type_in('//input[@id="label9"]', '+375298035458')
    f.type_in('//input[@id="label10"]', 'qwe123@bk.ru')
    f.type_in('//input[@id="label1000"]', 'MC4665923')
    f.click_on('//input[@id="slabel13"]')
    f.click_on('//input[@id="label13"]')
    f.click_on('//button[text()="Перейти  к выбору времени"]')
    sleep(3)
    if f.is_element_displayed('//span[text()="Свободно"]'):
        f.click_on('(//span[text()="Свободно"])[1]')
        # тут похоже начинает работать бан, кнопка не всегда работает, нужно переключать ip
        # может попробовать рандомом кликать по элементам , перемотка вроде помогает немного
        element3 = driver.find_element(By.ID, 'nextTo3')
        element30 = driver.find_element(By.XPATH, '//h2[text()="Полезная информация"]')
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.execute_script("arguments[0].scrollIntoView();", element3)
        driver.execute_script("arguments[0].scrollIntoView();", element30)
        driver.execute_script("arguments[0].scrollIntoView();", element3)
        sleep(3)
        f.click_on('//button[@id="nextTo3"]')

        sleep(5)
        element4 = driver.find_element(By.XPATH, '//button[text()="Завершение бронирования"]')
        driver.execute_script("arguments[0].scrollIntoView();", element4)
        driver.execute_script("arguments[0].scrollIntoView();", element30)
        driver.execute_script("arguments[0].scrollIntoView();", element4)
        sleep(3)
        f.click_on('Завершение бронирования')
        sleep(5)
        # отмена записи для теста не забывать отменять
        # f.click_on('Отмена записи')
        # f.click_on('Хорошо')
    else:
        logging.warning('Венгрия нет дат')

    print()