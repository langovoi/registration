
import undetected_chromedriver as uc
from time import sleep

import os, sys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import telegram

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from driver.base_page import BasePage
from selenium import webdriver


class France(BasePage):
    pass


if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    # options.headless = True
    driver = uc.Chrome(options=options)
    driver.delete_all_cookies()
    driver.get('https://consulat.gouv.fr/ru/ambassade-de-france-a-minsk/appointment')
    f = France(driver)
    f.click_on('//button[@class="fr-btn fr-btn--primary fr-icon-check-line fr-btn--icon-left "]')
    label: refresh
    if f.is_element_displayed('//button[@class="btn btn-primary btn-md"]'):
        f.get_click_on('//button[@class="btn btn-primary btn-md"]')
    f.click_on('//button[@class="fr-btn fr-btn--primary fr-icon-check-line fr-btn--icon-left "]')
    f.click_on('//label[@class="custom-control-label"]')
    f.click_on('//button[@class="fr-btn fr-btn--primary fr-icon-check-line fr-btn--icon-left "]')
    if f.is_element_displayed('//p[@class="fr-text--lg text-secondary col-md-10 offset-md-1 mt-5 mb-5 text-center"]'):
        sleep(120)
        # refresh и goto refresh
    else:
        telegram.send_doc('Франия: Есть даты!', driver.page_source)


    sleep(10000)
    print()