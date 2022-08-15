from datetime import datetime

import requests
import undetected_chromedriver as uc  # Import from seleniumwire
from selenium.webdriver.support.select import Select


class Italy():
    def __init__(self, vc_type):
        self.driver = uc.Chrome()
        self.vc_type = vc_type
        self.categories = {'1090': 'schengen'}
        self.s = requests.Session()

    def open_page(self, page_name, **kwargs):
        if page_name == 'login':
            self.driver.get('https://prenotami.esteri.it/Home?ReturnUrl=%2fUserArea')
        elif page_name == 'appointments':
            self.driver.get(f'https://prenotami.esteri.it/Services/Booking/{self.vc_type}')

    def login(self, login, password):
        self.driver.find_element_by_xpath('//input[@id="login-email"]').send_keys(login)
        self.driver.find_element_by_xpath('//input[@id="login-password"]').send_keys(password)
        self.driver.find_element_by_xpath('//button[@type="submit"]').click()

    def click_on(self, xpath):
        self.driver.find_element_by_xpath(xpath).click()

    def enter_in(self, xpath, text):
        self.driver.find_element_by_xpath(xpath).send_keys(text)

    def select_from(self, xpath, value):
        select = Select(self.driver.find_element_by_xpath(xpath))
        select.select_by_value(value)

    def confirm_alert(self):
        alert = self.driver.switch_to.alert
        alert.accept()

    def get_dates(self, cookies):
        for cookie in cookies: self.s.cookies.set(cookie['name'], cookie['value'])
        headers = {'Accept': 'application/json, text/javascript, */*; q=0.01','Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8','Connection': 'keep-alive','Content-Type': 'application/json; charset=UTF-8','Origin': 'https://prenotami.esteri.it','Referer': 'https://prenotami.esteri.it/BookingCalendar?selectedService=Visti%20per%20Motivi%20di%20studio','Sec-Fetch-Dest': 'empty','Sec-Fetch-Mode': 'cors','Sec-Fetch-Site': 'same-origin','User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36','X-Requested-With': 'XMLHttpRequest',}
        today = datetime.now().strftime("%d/%m/%Y")
        json_data = {'_Servizio': '1090','selectedDay': today,}
        return self.s.post('https://prenotami.esteri.it/BookingCalendar/RetrieveCalendarAvailability', cookies=self.s.cookies, headers=headers, json=json_data).json()

    def get_times(self, date):
        headers = {'Accept': 'application/json, text/javascript, */*; q=0.01','Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8','Connection': 'keep-alive','Content-Type': 'application/json; charset=UTF-8','Origin': 'https://prenotami.esteri.it','Referer': 'https://prenotami.esteri.it/BookingCalendar?selectedService=Visti%20per%20Motivi%20di%20studio','Sec-Fetch-Dest': 'empty','Sec-Fetch-Mode': 'cors','Sec-Fetch-Site': 'same-origin','User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36','X-Requested-With': 'XMLHttpRequest',}
        json_data = {'selectedDay': f'{date}','idService': self.vc_type,}
        return self.s.post('https://prenotami.esteri.it/BookingCalendar/RetrieveTimeSlots', cookies=self.s.cookies, headers=headers, json=json_data)

    def register_user(self, date, id_calendar, time, slots):
        headers = {'Accept': 'application/json, text/javascript, */*; q=0.01','Accept-Language': 'en-US,en;q=0.9','Connection': 'keep-alive','Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8','Origin': 'https://prenotami.esteri.it','Referer': 'https://prenotami.esteri.it/BookingCalendar?selectedService=Visti%20per%20Motivi%20di%20studio','Sec-Fetch-Dest': 'empty','Sec-Fetch-Mode': 'cors','Sec-Fetch-Site': 'same-origin','User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36','X-Requested-With': 'XMLHttpRequest','sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"macOS"',}
        data = f'idCalendarioGiornaliero={id_calendar}&selectedDay={date}&selectedHour={time}({slots})'
        return self.s.post('https://prenotami.esteri.it/BookingCalendar/InsertNewBooking', cookies=self.s.cookies, headers=headers, data=data)

