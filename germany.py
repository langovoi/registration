import re
from datetime import datetime
from time import sleep

import requests
from bs4 import BeautifulSoup

from selenium import webdriver

from utils import captcha, telegram


# National
# termin = ['TERMIN325', 'TERMIN340']
# category = '375'

# Schengen
# termin = ['TERMIN325', 'TERMIN327']
# category = '373'

# Tourism
# termin = ['TERMIN325', 'TERMIN327']
# category = '373'

# status:0
# users_dict = [
#     {"status": 0, "reason": "Посещение родственников/друзей/знакомых", "surname": "IVANTSOV", "name": "VALERY",
#      "email": "sash.kardash@gmail.ru",
#      "passport_number": "AB2680952", "birth_day": "07/06/2001", "passport_issued": "13/04/2021",
#      "passport_expired": "13/4/2031", "issued_by": "MIA", "phone_number": "375295497118", "nationality": "Belarus",
#      "travel_date": "05/11/2022", "date_from": "13/07/2022", "date_to": "25/10/2022", "family": "1"},
#     {"status": 0, "reason": "Посещение родственников/друзей/знакомых", "surname": "NOVIKAU", "name": "ALIAKSANDR",
#      "email": "n-pestretsov@mail.ru",
#      "passport_number": "BM2183681", "birth_day": "02/02/1989", "passport_issued": "05/04/2022",
#      "passport_expired": "5/4/2032", "issued_by": "MIA", "phone_number": "375295023120", "nationality": "Belarus",
#      "travel_date": "05/11/2022", "date_from": "13/07/2022", "date_to": "25/10/2022", "family": "1"},
#     {"status": 0, "reason": "Посещение родственников/друзей/знакомых", "surname": "BAKUNOVICH", "name": "DZMITRY",
#      "email": "dobrushin.2021@mail.ru",
#      "passport_number": "PD0039632", "birth_day": "18/11/1972", "passport_issued": "29/08/2017",
#      "passport_expired": "29/08/2027", "issued_by": "MIA", "phone_number": "375336374028",
#      "nationality": "Belarus", "travel_date": "05/11/2022", "date_from": "13/10/2022", "date_to": "25/08/2022",
#      "family": "3"},
#     {"status": 0, "reason": "Посещение родственников/друзей/знакомых", "surname": "TRAFIMCHYK", "name": "MARYIAEVIALINA",
#      "email": "yevgeniya.chekulova@mail.ru", "passport_number": "MC3428596", "birth_day": "08/07/2010",
#      "passport_issued": "20/08/2020",
#      "passport_expired": "20/08/2030", "issued_by": "MIA", "phone_number": "375333582710",
#      "nationality": "Belarus", "travel_date": "05/11/2022", "date_from": "13/07/2022", "date_to": "25/10/2022",
#      "family": "4"},
#     {"status": 0, "reason": "Посещение родственников/друзей/знакомых", "surname": "HUSAK", "name": "LIZAVETA",
#      "email": "karolina.rytik.rytko@mail.ru",
#      "passport_number": "MP4280922", "birth_day": "15/03/2011", "passport_issued": "15/09/2027",
#      "passport_expired": "15/09/2027", "issued_by": "MIA", "phone_number": "375291205453",
#      "nationality": "Belarus", "travel_date": "05/11/2022", "date_from": "13/07/2022", "date_to": "25/10/2022",
#      "family": "5"}]


class Germany():
    def __init__(self, termin, category, users_dict=None):
        self.driver = webdriver.Chrome()
        self.s = requests.Session()
        self.termin = termin
        self.category = category
        self.users_dict = users_dict
        self.driver.get(f'https://service2.diplo.de/rktermin/extern/appointment_showMonth.do?locationCode=mins&realmId=231&categoryId={category}')
        self.session_id = self.driver.session_id
        self.categories = {'373': "Шенген", '2845': "Туризм", '375': "Национальная"}

    def open_login_page(self):
        # login page
        cookies = {'JSESSIONID': f'JSESSIONID={self.session_id}','KEKS': f'{self.termin[0]}',}
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8', 'Cache-Control': 'max-age=0', 'Connection': 'keep-alive', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'none', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36', 'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"macOS"',}
        params = {'locationCode': 'mins', 'realmId': '231', 'categoryId': f'{self.category}',}
        r = self.s.get('https://service2.diplo.de/rktermin/extern/appointment_showMonth.do', params=params, cookies=cookies, headers=headers)

        soup = BeautifulSoup(r.text,"lxml")
        image = soup.select("captcha > div")
        image= image[0]['style'].split("url('")[1].split("')")[0]
        self.driver.quit()
        return captcha.get_code(image)

    def get_appointments(self, url, code, session_id):
        cookies = {'JSESSIONID': f'{session_id}','KEKS': f'{self.termin[1]}',}
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'max-age=0', 'Connection': 'keep-alive', 'Origin': 'https://service2.diplo.de', 'Referer': f'https://service2.diplo.de/rktermin/extern/appointment_showMonth.do;jsessionid={session_id}', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36', 'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"macOS"',}
        data = {'captchaText': f'{code}', 'rebooking': 'false', 'token': '', 'lastname': '', 'firstname': '', 'email': '', 'locationCode': 'mins', 'realmId': '231', 'categoryId': f'{self.category}', 'openingPeriodId': '', 'date': '','dateStr': '', 'action:appointment_showMonth': 'Continue',}
        return self.s.post(url, cookies=cookies, headers=headers, data=data).text

    def get_time(self, date):
        cookies = {'JSESSIONID': f'{self.session_id}', 'KEKS': f'{self.termin[1]}',}
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8', 'Connection': 'keep-alive', 'Referer': 'https://service2.diplo.de/rktermin/extern/appointment_showMonth.do', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36', 'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"macOS"',}
        params = {'locationCode': 'mins', 'realmId': '231', 'categoryId': f'{self.category}', 'dateStr': f'{date}',}
        return self.s.get('https://service2.diplo.de/rktermin/extern/appointment_showDay.do', params=params, cookies=cookies, headers=headers)

    def get_users_with_dates(self, dates_list):
        for date in dates_list:
            for i, user in enumerate(self.users_dict):
                date_from = datetime.strptime(user['date_from'] if user['date_from'] else '01/01/2022', '%d/%m/%Y')
                date_to = datetime.strptime(user['date_to'] if user['date_to'] else '01/01/3000', '%d/%m/%Y')
                actual_date = datetime.strptime(date, '%d.%m.%Y')
                if date_from < actual_date <= date_to:
                    self.users_dict[i].setdefault("dates", []).append(date)
        available_users = [d for d in self.users_dict if 'dates' in d]
        family_list = {}
        for user in available_users:
            if user['family'] not in family_list:
                family_list[user['family']] = [user]
            else:
                family_list[user['family']].append(user)
        return family_list

    def get_dates(self):
        date_slots = []
        code = self.open_login_page()
        for _ in range(10):
            html = self.get_appointments('https://service2.diplo.de/rktermin/extern/appointment_showMonth.do', code, self.session_id)
            if 'Unfortunately' in html:
                telegram.send_message(f"Германия {self.categories[self.category]}: нет дат")
                break
            elif 'Termine sind verfügbar' in html or 'Запись на прием возможна' in html or 'Please select a date' in html:
                soup = BeautifulSoup(html, "lxml")
                element = soup.find_all("div", {'style': 'margin-left: 20%;'})
                date_slots = [link.find("a")['href'].split('=')[-1] for link in element]
                telegram.send_message(f'🇩🇪 Германия {self.categories[str(self.category)]}: {date_slots}')
                break
            elif "background:white url('data:image/jpg" in html:
                sleep(10) # if captcha
        else:
            raise RuntimeError(f'⭕ Не разгадал капчу с 10 попыток для категории {self.categories[str(self.category)]}')
        return date_slots
        # family_list = self.get_users_with_dates(date_slots)

    def register_users(self, family_list, date_slots): # get time and register
        for index, family in family_list.items(): # check each user
            for date in date_slots:
                if date in family[0]['dates']: # get available time
                    response = self.get_time(date)
                    soup = BeautifulSoup(response.text, "lxml")
                    element = soup.find_all("div", {'style': 'margin-left: 20%;'})
                    time_slots = [[re.findall("\d+", link.text)[0], link.find("a")['href'].split('=')[-1]] for link in element if link.find("a")]
                    for time in time_slots:
                        if int(time[0]) >= len(family):
                            self.register_national(family, date, time[1])
                            print() # register user

    def open_register_page(self, date, time):
        cookies = {'JSESSIONID': f'{self.session_id}', 'KEKS': f'{self.termin[0]}',}
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8', 'Connection': 'keep-alive', 'Referer': f'https://service2.diplo.de/rktermin/extern/appointment_showDay.do?locationCode=mins&realmId=231&categoryId={category}&dateStr={date}', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36', 'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"macOS"',}
        params = {'locationCode': 'mins', 'realmId': '231', 'categoryId': f'{self.category}', 'dateStr': f'{date}', 'openingPeriodId': f'{time}',}
        r = self.s.get('https://service2.diplo.de/rktermin/extern/appointment_showForm.do', params=params, cookies=cookies, headers=headers)
        soup = BeautifulSoup(r.text,"lxml")
        image = soup.select("captcha > div")
        image= image[0]['style'].split("url('")[1].split("')")[0]
        return captcha.get_code(image), soup

    def register_national(self, family, date, time):
        code, html = self.open_register_page(date, time)

        additional_users = ''
        if len(family) > 1:
            for additional_user in family[1:]:
                user = f"{additional_user['surname']}, {additional_user['name']}, {additional_user['passport_number']}"
                additional_users = user if not additional_users else f'{additional_users}, {user}'
        cookies = {'JSESSIONID': f'{self.session_id}', 'KEKS': f'{self.termin[0]}',}
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'max-age=0', 'Connection': 'keep-alive', 'Origin': 'https://service2.diplo.de', 'Referer': 'https://service2.diplo.de/rktermin/extern/appointment_showForm.do', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36', 'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"macOS"',}
        data = {
            'lastname': f'{family[0]["surname"]}', 'firstname': f'{family[0]["name"]}', 'email': f'{family[0]["email"]}', 'emailrepeat': f'{family[0]["email"]}',
            'fields[0].content': f'{len(family)}', 'fields[0].definitionId': '940', 'fields[0].index': '0',
            'fields[1].content': f'{family[0]["passport_number"]}', 'fields[1].definitionId': '941', 'fields[1].index': '1',
            'fields[2].content': f'{additional_users}', 'fields[2].definitionId': '942', 'fields[2].index': '2',
            'fields[3].content': f'{family[0]["reason"]}', 'fields[3].definitionId': '943', 'fields[3].index': '3',
            'fields[4].content': f'{family[0]["phone_number"]}', 'fields[4].definitionId': '944', 'fields[4].index': '4',
            'fields[5].content': 'true', '__checkbox_fields[5].content': 'true', 'fields[5].definitionId': '945', 'fields[5].index': '5',
            'captchaText': f'{code}',
            'locationCode': 'mins', 'realmId': '231', 'categoryId': f'{self.category}', 'openingPeriodId': f'{time}', 'date': f'{date}', 'dateStr': f'{date}', 'action:appointment_addAppointment': 'Speichern',}
        r = self.s.post('https://service2.diplo.de/rktermin/extern/appointment_addAppointment.do', cookies=cookies, headers=headers, data=data)
        soup = BeautifulSoup(r.text,"lxml")
        print(soup)

    # register_users(family_list, date_slots)