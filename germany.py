import json
import logging
import re
import sys
from datetime import datetime
from time import sleep

import requests
from bs4 import BeautifulSoup

from utils import captcha, telegram, users


# National
# termin = ['TERMIN325', 'TERMIN340']
# category = '375'

# Schengen
# termin = ['TERMIN325', 'TERMIN327']
# category = '373'

# Tourism
# termin = ['TERMIN325', 'TERMIN327']
# category = '2845'

# status:0

class Germany():
    def __init__(self, termin, category, vc_type):
        self.s = requests.Session()
        self.session_id = ''
        self.termin = termin
        self.category = category
        self.users_dict = users.get_users(vc_type)
        self.categories = {'373': "Шенген", '2845': "Туризм", '375': "Национальная"}

    def get_session_id(self, url):
        headers = { 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8', 'Connection': 'keep-alive', 'Referer': f'{url}','Sec-Fetch-Dest': 'document','Sec-Fetch-Mode': 'navigate','Sec-Fetch-Site': 'same-origin','Sec-Fetch-User': '?1','Upgrade-Insecure-Requests': '1','User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36','sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"macOS"',}
        r = self.s.get(url, headers=headers)
        if 'JSESSIONID' in self.s.cookies.get_dict():
            return self.s.cookies.get_dict()['JSESSIONID']
        else:
            if 'The server is currently busy' in r.text:
                telegram.send_doc('The server is currently busy', r.text)
                return None
            else:
                error_message = 'JSESSIONID не найден'
                telegram.send_doc(error_message, r.text)
                raise RuntimeError(error_message)

    def open_login_page_get_captcha_code(self):
        html_login_page = code = ''
        logging.warning('open login page')
        for _ in range(3):
            logging.warning(f'{_ + 1} try')
            html_login_page = self.open_page('login').text
            if captcha.is_captcha_displayed(html_login_page):
                code = captcha.get_code(html_login_page, f'login {self.category}')
                if code:
                    break
        else:
            telegram.send_doc(f'Не смог разгадать капчу с 3 раз. code: {code}', html_login_page)
            raise RuntimeError(f'Не смог разгадать капчу с 3 раз. code: {code}')
        logging.warning('code is found')
        return code

    def open_appointments_page_and_get_dates(self, code):
        date_slots = []
        logging.warning('open appointments page')
        for _ in range(3):
            html = self.open_page('appointments', code=code).text
            if 'Unfortunately' in html:
                # telegram.send_message(f"Германия {self.categories[self.category]}: нет дат")
                break
            elif 'Termine sind verfügbar' in html or 'Запись на прием возможна' in html or 'Please select a date' in html:
                soup = BeautifulSoup(html, "lxml")
                element = soup.find_all("div", {'style': 'margin-left: 20%;'})
                date_slots = [link.find("a")['href'].split('=')[-1] for link in element]
                try:
                    telegram.send_message(f'🇩🇪 Германия {self.categories[str(self.category)]}: {date_slots}')
                except Exception:
                    pass
                break
            else:
                if captcha.is_captcha_displayed(html):
                    # telegram.send_doc(f'⭕ Captcha: Неверный код {code}. Попытка {i+1}', str(soup))
                    code = captcha.get_code(html, f'appointments {self.category}')
                    if not code:
                        telegram.send_doc('⭕ Ошибка, не смог решить капчу', html)
                else:
                    telegram.send_doc('⭕ Ошибка, капча не отображается', html)
                sleep(1)  # if captcha
        else:
            raise RuntimeError(f'⭕ Не разгадал капчу с 3 попыток для категории {self.categories[str(self.category)]}')
        return date_slots, code

    def get_time(self, date):
        # try first time without code
        cookies = {'JSESSIONID': f'{self.session_id}', 'KEKS': f'{self.termin[1]}',}
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8', 'Connection': 'keep-alive', 'Referer': 'https://service2.diplo.de/rktermin/extern/appointment_showMonth.do', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36', 'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"macOS"',}
        params = {'locationCode': 'mins', 'realmId': '231', 'categoryId': f'{self.category}', 'dateStr': f'{date}',}
        r = self.s.get('https://service2.diplo.de/rktermin/extern/appointment_showDay.do', params=params, cookies=cookies, headers=headers)
        # check if captcha
        if captcha.is_captcha_displayed(r.text):
            for _ in range(3):
                # try with code
                code = captcha.get_code(r.text, f'time page {self.category}')
                if not code:
                    cookies = {'JSESSIONID': f'{self.session_id}', 'KEKS': f'{self.termin[1]}',}
                    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8', 'Connection': 'keep-alive', 'Referer': 'https://service2.diplo.de/rktermin/extern/appointment_showMonth.do', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36', 'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"macOS"',}
                    params = {'locationCode': 'mins', 'realmId': '231', 'categoryId': f'{self.category}', 'dateStr': f'{date}',}
                    r = self.s.get('https://service2.diplo.de/rktermin/extern/appointment_showDay.do', params=params, cookies=cookies, headers=headers)
                    code = captcha.get_code(r.text, f'time page {self.category}')
                headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8', 'Cache-Control': 'max-age=0', 'Connection': 'keep-alive', 'Origin': 'https://service2.diplo.de', 'Referer': f'https://service2.diplo.de/rktermin/extern/appointment_showDay.do?locationCode=mins&realmId=231&categoryId={self.category}&dateStr=f{date}', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36', 'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"macOS"',}
                data = {'captchaText': f'{code}', 'rebooking': '', 'token': '', 'lastname': '', 'firstname': '', 'email': '', 'locationCode': 'mins', 'realmId': '231', 'categoryId': f'{self.category}', 'openingPeriodId': '', 'date': f'{date}', 'dateStr': f'{date}',}
                r = self.s.post('https://service2.diplo.de/rktermin/extern/appointment_showDay.do', cookies=cookies, headers=headers, data=data)
                if captcha.is_captcha_displayed(r.text):
                    break
            else:
                telegram.send_doc('Не разгадал капчу с 3 раз', r.text)
        soup = BeautifulSoup(r.text, "lxml")
        element = soup.find_all("div", {'style': 'margin-left: 20%;'})
        time_slots = [[re.findall("\d+", link.text)[0], link.find("a")['href'].split('=')[-1]] for link in element if
                      link.find("a")]
        return time_slots

    def get_users_with_dates(self, dates_list, vc_type):
        self.users_dict = users.get_users(vc_type)
        for date in dates_list:
            for i, user in enumerate(self.users_dict):
                date_from = datetime.strptime(user['vc_date_from'] if user['vc_date_from'] else '2022-01-01',
                                              '%Y-%m-%d')
                date_to = datetime.strptime(user['vc_date_to'] if user['vc_date_to'] else '3000-01-01', '%Y-%m-%d')
                actual_date = datetime.strptime(date, '%d.%m.%Y')
                if date_from <= actual_date <= date_to:
                    if not ('dates' in user and date in user['dates']):
                        self.users_dict[i].setdefault("dates", []).append(date)
        available_users = [d for d in self.users_dict if 'dates' in d]
        family_list = {}
        for user in available_users:
            if user['vc_with'] == '0':
                family_list[user['id']] = [user]
            else:
                if user['vc_with'] in family_list:
                    family_list[user['vc_with']].append(user)
                else:
                    family_list[user['vc_with']] = user
        return family_list

    def register_users(self, date_slots, vc_type):  # get time and register
        family_list = self.get_users_with_dates(date_slots, vc_type)
        for index, family in family_list.items():  # check each user
            for date in date_slots:
                is_registered = False
                if date in family[0]['dates']:  # get available time
                    time_slots = self.get_time(date)
                    for time in time_slots:
                        code, soup = self.open_register_page(date, time[1])
                        telegram.send_doc(f'Германия {self.categories[self.category]}: Страница заполнения полей', str(soup))
                        is_registered = self.register_family(family, date, time[1], code, soup)
                        if is_registered:
                            break
                    if is_registered:
                        break

    def open_register_page(self, date, time):
        code = soup = None
        for _ in range(3):
            html = self.open_page('register').text
            if 'An error occured while processing your appointment.' in html:
                telegram.send_doc('An error occured while processing your appointment.', html)
                raise RuntimeError('An error occured while processing your appointment.')
            code = captcha.get_code(html, f'registration {self.category}')
            if not code:
                cookies = {'JSESSIONID': f'{self.session_id}', 'KEKS': f'{self.termin[1]}',}
                headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8', 'Connection': 'keep-alive', 'Referer': f'https://service2.diplo.de/rktermin/extern/appointment_showDay.do?locationCode=mins&realmId=231&categoryId={self.category}&dateStr={date}', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36', 'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"macOS"',}
                params = {'locationCode': 'mins', 'realmId': '231', 'categoryId': f'{self.category}', 'dateStr': f'{date}', 'openingPeriodId': f'{time}',}
                r = self.s.get('https://service2.diplo.de/rktermin/extern/appointment_showForm.do', params=params, cookies=cookies, headers=headers)
                code = captcha.get_code(r.text, f'registration 2 {self.category}')
            soup = BeautifulSoup(html, "lxml")
            if len(soup.find("div", {'style': 'font-weight: bold;'})):
                break
        else:
            telegram.send_doc('⭕ Германия: не смог найти поле email', str(soup))
        return code, soup

    def register_family(self, family, date, time, code, soup):
        time_text = soup.find("div", {'style': 'font-weight: bold;'}).text.strip().replace('\n', ' ').replace('\t\t\t\t', ' ')
        success = False
        for _ in range(3):
            html = self.fill_fields(family, date, time, code)
            soup = BeautifulSoup(html, "lxml")
            if not (soup.find("captcha") or soup.find("div", {"class": "global-error"}) or 'An error occured while processing your appointment' in str(soup)):
                telegram.send_doc(caption=f'🟢 🇩🇪 Германия: Успешно записан: {family[0]["vc_surname"]} {family[0]["vc_name"]}({family[0]["vc_mail"]}) на {str(time_text)}', html=str(html))
                for user in family:
                    users.update_status(url=f'{sys.argv[2]}', id=user["id"], status='4')
                success = True
                break
            elif error := soup.find("div", {"class": "global-error"}):
                if "The entered text was wrong" in error.text:
                    code = captcha.get_code(str(soup), f'The entered text was wrong {self.category}')
                elif "This entry needs to be unique" in error.text:
                    for user in family:
                        users.update_status(url=f'{sys.argv[2]}', id=user["id"], status='4')
                    telegram.send_doc(
                        caption=f'⭕ 🇩🇪 Германия: {self.categories[self.category]}: Уже зарегистрирован ({str(time_text)}): {family[0]["vc_surname"]} {family[0]["vc_name"]}({family[0]["vc_mail"]})\nОшибка: {error.text.strip()}', html=str(soup))
                    success = True
                else:
                    telegram.send_doc(
                        caption=f'⭕ 🇩🇪 Германия {self.categories[self.category]}: Неизвестная ошибка для: ({str(time_text)}): {family[0]["vc_surname"]} {family[0]["vc_name"]}({family[0]["vc_mail"]})\nОшибка: {error.text.strip()}', html=str(soup))
                    success = False
                    break
            else:
                telegram.send_doc(f'Code: {code}. Неизвестная ошибка после ввода всех данных', str(soup))
                raise RuntimeError('')
        return success

    def fill_fields(self, family, date, time, code):
        additional_users = ''
        if len(family) > 1:
            for additional_user in family[1:]:
                user = f"{additional_user['vc_surname']}, {additional_user['vc_name']}, {additional_user['vc_passport']}"
                additional_users = user if not additional_users else f'{additional_users}, {user}'
        cookies = {'JSESSIONID': f'{self.session_id}', 'KEKS': f'{self.termin[0]}',}
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'max-age=0', 'Connection': 'keep-alive', 'Origin': 'https://service2.diplo.de', 'Referer': 'https://service2.diplo.de/rktermin/extern/appointment_showForm.do', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36', 'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"macOS"',}
        inviting = family[0]["vc_inviting"]
        if self.category == '375':
            data = {'lastname': f'{family[0]["vc_surname"]}', 'firstname': f'{family[0]["vc_name"]}', 'email': f'{family[0]["vc_mail"]}', 'emailrepeat': f'{family[0]["vc_mail"]}',
                    'fields[0].content': f'{len(family)}', 'fields[0].definitionId': '940', 'fields[0].index': '0',
                    'fields[1].content': f'{family[0]["vc_passport"]}', 'fields[1].definitionId': '941', 'fields[1].index': '1',
                    'fields[2].content': f'{additional_users}', 'fields[2].definitionId': '942', 'fields[2].index': '2',
                    'fields[3].content': f'{family[0]["vc_type"]}', 'fields[3].definitionId': '943', 'fields[3].index': '3',
                    'fields[4].content': f'{family[0]["vc_phone"].replace("+", "")}', 'fields[4].definitionId': '944', 'fields[4].index': '4',
                    'fields[5].content': 'true', '__checkbox_fields[5].content': 'true', 'fields[5].definitionId': '945', 'fields[5].index': '5',
                    'captchaText': f'{code}',
                    'locationCode': 'mins', 'realmId': '231', 'categoryId': f'{self.category}', 'openingPeriodId': f'{time}', 'date': f'{date}', 'dateStr': f'{date}', 'action:appointment_addAppointment': 'Speichern',}
        elif self.category == '373':
            data = {'lastname': f'{family[0]["vc_surname"]}', 'firstname': f'{family[0]["vc_name"]}', 'email': f'{family[0]["vc_mail"]}', 'emailrepeat': f'{family[0]["vc_mail"]}',
                    'fields[0].content': f'{family[0]["vc_birth"]}', 'fields[0].definitionId': '2005', 'fields[0].index': '0',
                    'fields[1].content': f'{family[0]["vc_passport"]}', 'fields[1].definitionId': '854', 'fields[1].index': '1',
                    'fields[2].content': f'{family[0]["vc_phone"].replace("+", "")}', 'fields[2].definitionId': '856', 'fields[2].index': '2',
                    'fields[3].content': f'{additional_users}', 'fields[3].definitionId': '860', 'fields[3].index': '3',
                    'fields[4].content': f'{len(family)}', 'fields[4].definitionId': '858', 'fields[4].index': '4',
                    'fields[5].content': {inviting if inviting  else "hotel"}, 'fields[5].definitionId': '2007', 'fields[5].index': '5',
                    'fields[6].content': 'Посещение родственников/друзей/знакомых', 'fields[6].definitionId': '855', 'fields[6].index': '6',
                    'captchaText': f'{code}',
                    'locationCode': 'mins', 'realmId': '231', 'categoryId': f'{self.category}', 'openingPeriodId': f'{time}', 'date': f'{date}', 'dateStr': f'{date}', 'action:appointment_addAppointment': 'Submit',}
        else: # elif self.category == '2845':
            data = {'lastname': f'{family[0]["vc_surname"]}', 'firstname': f'{family[0]["vc_name"]}', 'email': f'{family[0]["vc_mail"]}', 'emailrepeat': f'{family[0]["vc_mail"]}',
                    'numVisitors': f'{len(family)}',
                    'fields[0].content': f'{family[0]["vc_birth"]}', 'fields[0].definitionId': '10777', 'fields[0].index': '0',
                    'fields[1].content': f'{family[0]["vc_passport"]}', 'fields[1].definitionId': '10779', 'fields[1].index': '1',
                    'fields[2].content': f'{family[0]["vc_phone"].replace("+", "")}', 'fields[2].definitionId': '10782', 'fields[2].index': '2',
                    'fields[3].content': f'{additional_users}', 'fields[3].definitionId': '10783', 'fields[3].index': '3',
                    'fields[4].content': f'{len(family)}', 'fields[4].definitionId': '10784', 'fields[4].index': '4',
                    'fields[5].content': {inviting if inviting else "hotel"}, 'fields[5].definitionId': '10785', 'fields[5].index': '5',
                    'captchaText': {code},
                    'locationCode': 'mins', 'realmId': '231', 'categoryId': f'{self.category}', 'openingPeriodId': f'{time}',
                    'date': f'{date}', 'dateStr': f'{date}', 'action:appointment_addAppointment': 'Submit',}
        r = self.s.post('https://service2.diplo.de/rktermin/extern/appointment_addAppointment.do', cookies=cookies, headers=headers, data=data)
        return r.text


    def open_page(self, page_name: str, **kwargs):
        if page_name == 'appointments':
            code = kwargs['code']
            cookies = {'JSESSIONID': f'{self.session_id}','KEKS': f'{self.termin[1]}',}
            headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'max-age=0', 'Connection': 'keep-alive', 'Origin': 'https://service2.diplo.de', 'Referer': f'https://service2.diplo.de/rktermin/extern/appointment_showMonth.do;jsessionid={self.session_id}', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36', 'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"macOS"',}
            data = {'captchaText': f'{code}', 'rebooking': 'false', 'token': '', 'lastname': '', 'firstname': '', 'email': '', 'locationCode': 'mins', 'realmId': '231', 'categoryId': f'{self.category}', 'openingPeriodId': '', 'date': '','dateStr': '', 'action:appointment_showMonth': 'Continue',}
            return self.s.post('https://service2.diplo.de/rktermin/extern/appointment_showMonth.do', cookies=cookies, headers=headers, data=data)
        elif page_name == 'login':
            self.session_id = self.get_session_id(f'https://service2.diplo.de/rktermin/extern/appointment_showMonth.do?locationCode=mins&realmId=231&categoryId={self.category}')
            # login page
            cookies = {'JSESSIONID': f'JSESSIONID={self.session_id}','KEKS': f'{self.termin[0]}',}
            headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8', 'Cache-Control': 'max-age=0', 'Connection': 'keep-alive', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'none', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36', 'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"macOS"',}
            params = {'locationCode': 'mins', 'realmId': '231', 'categoryId': f'{self.category}',}
            return self.s.get('https://service2.diplo.de/rktermin/extern/appointment_showMonth.do', params=params, cookies=cookies, headers=headers)
        elif page_name == 'register':
            date = kwargs['date']
            time = kwargs['time']
            cookies = {'JSESSIONID': f'{self.session_id}', 'KEKS': f'{self.termin[1]}',}
            headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8', 'Connection': 'keep-alive', 'Referer': f'https://service2.diplo.de/rktermin/extern/appointment_showDay.do?locationCode=mins&realmId=231&categoryId={self.category}&dateStr={date}', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36', 'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"macOS"',}
            params = {'locationCode': 'mins', 'realmId': '231', 'categoryId': f'{self.category}', 'dateStr': f'{date}', 'openingPeriodId': f'{time}',}
            return self.s.get('https://service2.diplo.de/rktermin/extern/appointment_showForm.do', params=params, cookies=cookies, headers=headers)