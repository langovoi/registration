from datetime import datetime
from time import sleep

import requests
import undetected_chromedriver.v2 as uc # Import from seleniumwire

# Create a new instance of the Chrome driver
from utils import telegram
from visa_italy.italy import Italy

if __name__ == "__main__":
    html_approintments = html_fields = html = ''
    while True:
        try:
            it = Italy('1090')
            it.open_page('login')
            it.login('sash.kardash@gmail.com', 'Ab123456!')
            while True:
                it.open_page('appointments')
                if len(it.driver.find_elements_by_xpath('//input[@id="PrivacyCheck"]')):
                    break
                else:
                    sleep(5)
            html = html_approintments = it.driver.page_source
            it.select_from('//select[@data-index ="2"]', '42')
            it.click_on('//input[@id="PrivacyCheck"]')
            it.click_on('//button[@id="btnAvanti"]')
            it.confirm_alert()
            html = html_confirm = it.driver.page_source
        except Exception as e:
            telegram.send_doc(f'Ошибка Италия: {str(e)}', html)
        finally:
            if html_approintments:
                telegram.send_doc(f'Ошибка Италия(Appointments):', html_approintments)
            if html_confirm:
                telegram.send_doc(f'Ошибка Италия(Fields):', html_confirm)


