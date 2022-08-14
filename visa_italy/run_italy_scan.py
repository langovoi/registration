from datetime import datetime

import requests
import undetected_chromedriver.v2 as uc # Import from seleniumwire

# Create a new instance of the Chrome driver
from visa_italy.italy import Italy

it = Italy('1090')

it.open_page('login')
it.login('sash.kardash@gmail.com', 'Ab123456!')
while True:
    it.open_page('appointments')
    if len(it.driver.find_elements_by_xpath('//input[@id="PrivacyCheck"]')):
        break
html_approintments = it.driver.page_source
it.click_on('//input[@id="PrivacyCheck"]')
it.click_on('//button[@id="btnAvanti"]')
it.confirm_alert()
cookies = it.driver.get_cookies()
s = requests.Session()
for cookie in cookies: s.cookies.set(cookie['name'], cookie['value'])
headers = {'Accept': 'application/json, text/javascript, */*; q=0.01','Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8','Connection': 'keep-alive','Content-Type': 'application/json; charset=UTF-8','Origin': 'https://prenotami.esteri.it','Referer': 'https://prenotami.esteri.it/BookingCalendar?selectedService=Visti%20per%20Motivi%20di%20studio','Sec-Fetch-Dest': 'empty','Sec-Fetch-Mode': 'cors','Sec-Fetch-Site': 'same-origin','User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36','X-Requested-With': 'XMLHttpRequest',}
today = datetime.now().strftime("%d/%m/%Y")
json_data = {'_Servizio': '1090','selectedDay': today,}
r = s.post('https://prenotami.esteri.it/BookingCalendar/RetrieveCalendarAvailability', cookies=s.cookies, headers=headers, json=json_data)
r.json()

json_data = {'selectedDay': '2022-08-31','idService': '163',}
r = s.post('https://prenotami.esteri.it/BookingCalendar/RetrieveTimeSlots', cookies=s.cookies, headers=headers, json=json_data)

headers = {'Accept': 'application/json, text/javascript, */*; q=0.01','Accept-Language': 'en-US,en;q=0.9','Connection': 'keep-alive','Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8','Origin': 'https://prenotami.esteri.it','Referer': 'https://prenotami.esteri.it/BookingCalendar?selectedService=Visti%20per%20Motivi%20di%20studio','Sec-Fetch-Dest': 'empty','Sec-Fetch-Mode': 'cors','Sec-Fetch-Site': 'same-origin','User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36','X-Requested-With': 'XMLHttpRequest','sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"macOS"',}
data = 'idCalendarioGiornaliero=3066762&selectedDay=2022-08-31&selectedHour=11%3A31+-+12%3A00(4)'
# r = s.post('https://prenotami.esteri.it/BookingCalendar/InsertNewBooking', cookies=s.cookies, headers=headers, data=data)


print(s.text)