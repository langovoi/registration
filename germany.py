import json
import logging
import http.client
import re
import sys
from datetime import datetime, timedelta
from operator import itemgetter
from time import sleep

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

from utils import captcha, telegram, users, gsheets, gmm


# National
# termin = ['TERMIN325', 'TERMIN340']
# category = '375'

# Schengen
# termin = ['TERMIN325', 'TERMIN327']
# category = '373'

# Tourism
# termin = ['TERMIN325', 'TERMIN344']
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
        self.errors = []
        self.gs = gsheets.GoogleSheets('germany')
        self.gs_registered = gsheets.GoogleSheets('germany_registered')


    def get_session_id(self, url):
        self.s = requests.Session()
        self.s.cookies.clear()
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
        return code, html_login_page

    def open_appointments_page_and_get_dates(self, code):
        date_time_slots = []
        logging.warning('open appointments page')
        for _ in range(10):
            html = self.open_page('appointments', code=code).text
            if 'Unfortunately' in html:
                # telegram.send_message(f"Германия {self.categories[self.category]}: нет дат")
                break
            elif 'Termine sind verfügbar' in html or 'Запись на прием возможна' in html or 'Please select a date' in html:
                soup = BeautifulSoup(html, "lxml")
                element = soup.find_all("div", {'style': 'margin-left: 20%;'})
                date_slots = [link.find("a")['href'].split('=')[-1] for link in element]
                for date in date_slots:
                    date_time_slots.extend(self.get_time(date))
                telegram.send_message(f'🇩🇪 Германия {self.categories[str(self.category)]}: {date_time_slots}')
                break
            elif captcha.is_captcha_displayed(html):
                code = captcha.get_code(html, f'appointments {self.category}')
                if code is None:
                    code, html = self.open_login_page_get_captcha_code()
                sleep(1)
            else:
                code, html = self.open_login_page_get_captcha_code()
                sleep(1)
        else:
            telegram.send_doc(f'⭕ Не разгадал капчу с 10 попыток для категории {self.categories[str(self.category)]}', html)
            raise RuntimeError(f'⭕ Не разгадал капчу с 10 попыток для категории {self.categories[str(self.category)]}')
        return date_time_slots, code

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
                if code is None:
                    cookies = {'JSESSIONID': f'{self.session_id}', 'KEKS': f'{self.termin[1]}',}
                    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8', 'Connection': 'keep-alive', 'Referer': 'https://service2.diplo.de/rktermin/extern/appointment_showMonth.do', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36', 'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"macOS"',}
                    params = {'locationCode': 'mins', 'realmId': '231', 'categoryId': f'{self.category}', 'dateStr': f'{date}',}
                    r = self.s.get('https://service2.diplo.de/rktermin/extern/appointment_showDay.do', params=params, cookies=cookies, headers=headers)
                    code = captcha.get_code(r.text, f'time page {self.category}')
                headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8', 'Cache-Control': 'max-age=0', 'Connection': 'keep-alive', 'Origin': 'https://service2.diplo.de', 'Referer': f'https://service2.diplo.de/rktermin/extern/appointment_showDay.do?locationCode=mins&realmId=231&categoryId={self.category}&dateStr=f{date}', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36', 'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"macOS"',}
                data = {'captchaText': f'{code}', 'rebooking': '', 'token': '', 'lastname': '', 'firstname': '', 'email': '', 'locationCode': 'mins', 'realmId': '231', 'categoryId': f'{self.category}', 'openingPeriodId': '', 'date': f'{date}', 'dateStr': f'{date}',}
                r = self.s.post('https://service2.diplo.de/rktermin/extern/appointment_showDay.do', cookies=cookies, headers=headers, data=data)
                if not captcha.is_captcha_displayed(r.text):
                    break
            else:
                telegram.send_doc('Не разгадал капчу с 3 раз', r.text)
        soup = BeautifulSoup(r.text, "lxml")
        element = soup.find_all("div", {'style': 'margin-left: 20%;'})
        time_slots = [[link.find("a")['href'].split('=')[-1], int(re.findall("\d+", link.text)[0])] for link in element if
                      link.find("a")]
        date_time_slots = []
        for time in time_slots:
            for _ in range(time[1]):
                date_time_slots.append([date, time[0]])
        return date_time_slots

    def get_users_with_dates(self, date_time_slots, vc_type):
        self.update_users_emails(vc_type)
        family_list = {}
        # get families
        for user in self.users_dict:
            if user['vc_with'] == '0':
                family_list[user['id']] = [user]
            else:
                if user['vc_with'] in family_list:
                    family_list[user['vc_with']].append(user)
                else:
                    for u in self.users_dict:
                        if u['id'] == user['vc_with']:
                            user['vc_with'] = u['vc_with'] if u['vc_with'] != '0' else user['vc_with']
                            family_list[user['vc_with']].append(user)
                            break
                    else:
                        family_list[user['vc_with']] = [user]
        # remove families without dates
        users = list(family_list.keys())
        while (len(users)):
            for i in users:
                user = family_list[i][0]
                for date in date_time_slots:
                    date_from = datetime.strptime(user['vc_date_from'] if user['vc_date_from'] else '2022-01-01', '%Y-%m-%d').date()
                    date_shift = user['vc_before_visit']
                    date_shift = int(date_shift) if date_shift else 0
                    min_date = datetime.today().date() + timedelta(days=date_shift+1)
                    date_from = date_from if date_from >= min_date else min_date
                    date_to = datetime.strptime(user['vc_date_to'] if user['vc_date_to'] else '3000-01-01', '%Y-%m-%d').date()
                    actual_date = datetime.strptime(date[0], '%d.%m.%Y').date()
                    if date_from <= actual_date <= date_to:
                        if not ('dates' in user and date[0] in user['dates']):
                            family_list[i][0].setdefault("dates", []).append(date)
                            date_time_slots.remove(date)
                            break
                else:
                    users.remove(i)
        family_list = {k: v for k, v in family_list.items() if 'dates' in v[0]}
        return family_list

    def update_users_emails(self, vc_type):
        self.users_dict = users.get_users(vc_type)
        all_emails = self.gs.ws.get_all_values()
        all_emails = [email for email in all_emails if email[4] == '0']
        all_emails = sorted(all_emails, key=itemgetter(3))
        users_without_email_assigned = [user for user in self.users_dict if ('|' not in user['vc_comment'] and user['vc_with'] == '0')]
        # add email to comment in agent
        for i, user in enumerate(users_without_email_assigned):
            users.update_fields(url=f'{sys.argv[2]}', id=user['id'], body={'vc_comment': f'{user["vc_comment"]}|{all_emails[i][1]}|'})
            try:
                self.gs.ws.update_acell(f'E{int(all_emails[i][0])+1}', '1')
            except Exception:
                sleep(0.5)
                self.gs.ws.update_acell(f'E{int(all_emails[i][0])+1}', '1')
        self.users_dict = users.get_users(vc_type)
        for i, user in enumerate(self.users_dict):
            if '|' in user['vc_comment']:
                self.users_dict[i]['vc_mail'] = user['vc_comment'].split('|')[1]

    def open_register_page(self, date, time):
        http.client._MAXLINE = 655360
        code = soup = None
        for _ in range(3):
            html = self.open_page('register', date=date, time=time).text
            if 'An error occured while processing your appointment.' in html:
                telegram.send_doc('⭕ Германия - An error occured while processing your appointment.', html)
                break
            code = captcha.get_code(html, f'registration {self.category}')
            if code is None:
                cookies = {'JSESSIONID': f'{self.session_id}', 'KEKS': f'{self.termin[1]}', }
                headers = {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8', 'Connection': 'keep-alive',
                    'Referer': f'https://service2.diplo.de/rktermin/extern/appointment_showDay.do?locationCode=mins&realmId=231&categoryId={self.category}&dateStr={date}',
                    'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'same-origin',
                    'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
                    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
                    'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"macOS"', }
                params = {'locationCode': 'mins', 'realmId': '231', 'categoryId': f'{self.category}',
                          'dateStr': f'{date}', 'openingPeriodId': f'{time}', }
                r = self.s.get('https://service2.diplo.de/rktermin/extern/appointment_showForm.do', params=params,
                               cookies=cookies, headers=headers)
                code = captcha.get_code(r.text, f'registration 2 {self.category}')
            soup = BeautifulSoup(html, "lxml")
            if len(soup.find("div", {'style': 'font-weight: bold;'})):
                break
        else:
            telegram.send_doc('⭕ Германия: не смог найти поле email', str(soup))
        return code, soup

    def register_family(self, family, date, time, code, soup):
        time_text = soup.find("div", {'style': 'font-weight: bold;'}).text.strip().replace('\n', ' ').replace(
            '\t\t\t\t', ' ')
        success = False
        headers = cookies = data = ''
        logging.warning(f'Register family:{family}\n{date} {time}')
        for _ in range(3):
            html, headers, cookies, data = self.fill_fields(family, date, time, code, soup)
            telegram.send_doc('Fill fields page:', str(soup))
            logging.warning(f'Fill fields:{html}')
            soup = BeautifulSoup(html, "lxml")
            if not (soup.find("captcha") or soup.find("div", {"class": "global-error"}) or 'An error occured while processing your appointment' in str(soup)):
                telegram.send_doc(caption=f'🟢 🇩🇪 Германия {self.categories[self.category]}: Успешно записан: {family[0]["vc_surname"]} {family[0]["vc_name"]}({family[0]["vc_mail"]}) на {str(time_text)}\nЖду письмо... ', html=str(html), debug=False)
                # for user in family:
                #     users.update_status(url=f'{sys.argv[2]}', id=user["id"], status='3')
                all_emails = self.gs.ws.get_all_values()
                email = [email for email in all_emails if email[1] == family[0]["vc_mail"]][0]
                # Select a range
                self.gs.ws.update_acell(f'F{int(email[0]) + 1}', int(email[5]) + 1)
                break
            elif error := soup.find("div", {"class": "global-error"}):
                logging.warning(f"Error: {error.text}")
                if "The entered text was wrong" in error.text:
                    code = captcha.get_code(str(soup), f'The entered text was wrong {self.category}')
                elif "This entry needs to be unique" in error.text:
                    # for user in family:
                    #     users.update_status(url=f'{sys.argv[2]}', id=user["id"], status='3')
                    telegram.send_doc(
                        caption=f'⭕ 🇩🇪 Германия: {self.categories[self.category]}: Уже зарегистрирован ({str(time_text)}): {family[0]["vc_surname"]} {family[0]["vc_name"]}({family[0]["vc_mail"]})\nОшибка: {error.text.strip()}', html=str(soup), debug=False)
                    success = True
                elif "There are no available Appointments for the chosen period" in error.text:
                    telegram.send_doc(
                        caption=f'⭕ 🇩🇪 Германия {self.categories[self.category]}: Дата ушла: ({str(time_text)}): {family[0]["vc_surname"]} {family[0]["vc_name"]}({family[0]["vc_mail"]})', html=str(soup), debug=False)
                    success = False
                    break
                else:
                    telegram.send_doc(
                        caption=f'⭕ 🇩🇪 Германия {self.categories[self.category]}: Неизвестная ошибка для: ({str(time_text)}): {family[0]["vc_surname"]} {family[0]["vc_name"]}({family[0]["vc_mail"]})\nОшибка: {error.text.strip()}', html=str(soup), debug=False)
                    success = False
                    break
            else:
                telegram.send_doc(f'Неизвестная ошибка после ввода всех данных', str(soup))
                success = False
        logging.warning(f'Success: {success}')
        return success

    def fill_fields(self, family, date, time, code, soup):
        additional_users = ''
        if len(family) > 1:
            for additional_user in family[1:]:
                user = f"{additional_user['vc_surname']}, {additional_user['vc_name']}, {additional_user['vc_passport']}"
                additional_users = user if additional_users == '' else f'{additional_users}, {user}'
        cookies = {'JSESSIONID': f'{self.session_id}', 'KEKS': f'{self.termin[0]}',}
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'max-age=0', 'Connection': 'keep-alive', 'Origin': 'https://service2.diplo.de', 'Referer': 'https://service2.diplo.de/rktermin/extern/appointment_showForm.do', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36', 'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"macOS"',}
        inviting = family[0]["vc_inviting"]
        field_id_map = [{match.get('value'): match.get('name').split('[')[1].split(']')[0]}  for match in soup.find_all(id=re.compile("definitionId"), type='hidden')]
        if self.category == '375':
            text_fields = {'940': f'{len(family)}', '941': family[0]["vc_passport"], '942': additional_users, '943': family[0]["vc_type"], '944': family[0]["vc_phone"].replace("+", "").replace(" ", ""), '945': 'true'}
            data = {'lastname': f'{family[0]["vc_surname"]}', 'firstname': f'{family[0]["vc_name"]}', 'email': f'{family[0]["vc_mail"]}', 'emailrepeat': f'{family[0]["vc_mail"]}', 'captchaText': f'{code}', 'locationCode': 'mins', 'realmId': '231', 'categoryId': f'{self.category}', 'openingPeriodId': f'{time}', 'date': f'{date}', 'dateStr': f'{date}', 'action:appointment_addAppointment': 'Submit',}
            if 'numVisitors' in str(soup): data['numVisitors'] = f'{len(family)}'
        elif self.category == '373':
            text_fields = {'854': family[0]["vc_passport"], '2005': family[0]["vc_birth"], '856': family[0]["vc_phone"].replace("+", "").replace(" ", ""), '860': additional_users, '858': f'{len(family)}', '855': 'Geschäft' if family[0]["vc_type"] == 'Buisness' else 'Посещение родственников/друзей/знакомых', '2007': inviting if inviting  else "hotel"}
            data = {'lastname': f'{family[0]["vc_surname"]}', 'firstname': f'{family[0]["vc_name"]}', 'email': f'{family[0]["vc_mail"]}', 'emailrepeat': f'{family[0]["vc_mail"]}',
                    'captchaText': f'{code}', 'locationCode': 'mins', 'realmId': '231', 'categoryId': f'{self.category}', 'openingPeriodId': f'{time}', 'date': f'{date}', 'dateStr': f'{date}', 'action:appointment_addAppointment': 'Submit',}
            if 'numVisitors' in str(soup): data['numVisitors'] = f'{len(family)}'
        elif self.category == '2845' : # elif self.category == '2845':
            text_fields = {'10784': f'{len(family)}', '10782': family[0]["vc_phone"].replace("+", "").replace(" ", ""), '10777': family[0]["vc_birth"], '10779': family[0]["vc_passport"], '10783': additional_users, '10807': inviting if inviting else "hotel", '10785': inviting if inviting else "hotel"}
            data = {'lastname': f'{family[0]["vc_surname"]}', 'firstname': f'{family[0]["vc_name"]}', 'email': f'{family[0]["vc_mail"]}', 'emailrepeat': f'{family[0]["vc_mail"]}',
                    'captchaText': {code}, 'date': f'{date}', 'dateStr': f'{date}', 'action:appointment_addAppointment': 'Submit', 'locationCode': 'mins', 'realmId': '231', 'categoryId': f'{self.category}', 'openingPeriodId': f'{time}'}
        else:
            raise RuntimeError(f'Неизвестная категория: {self.category}')

        for i, definition in enumerate(field_id_map):
            (id, index), = definition.items()
            if id == '945': # checkbox
                data.update({f'fields[{index}].content': 'true', f'__checkbox_fields[{index}].content': 'true', f'fields[{index}].definitionId': id, f'fields[{index}].index': index})
            elif id in text_fields.keys(): # text field and dropdowns
                data.update({f'fields[{index}].content': text_fields[id], f'fields[{index}].definitionId': id, f'fields[{index}].index': index,})
            else:
                telegram.send_doc(f'Неизвестное поле({id}) для категории {self.categories[self.category]}', str(soup))
        r = self.s.post('https://service2.diplo.de/rktermin/extern/appointment_addAppointment.do', cookies=cookies, headers=headers, data=data).text
        return r, headers, cookies, data

    def open_page(self, page_name: str, **kwargs):
        if page_name == 'login':
            self.session_id = self.get_session_id(f'https://service2.diplo.de/rktermin/extern/appointment_showMonth.do?locationCode=mins&realmId=231&categoryId={self.category}')
            # login page
            cookies = {'JSESSIONID': f'JSESSIONID={self.session_id}','KEKS': f'{self.termin[0]}',}
            headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8', 'Cache-Control': 'max-age=0', 'Connection': 'keep-alive', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'none', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36', 'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"macOS"',}
            params = {'locationCode': 'mins', 'realmId': '231', 'categoryId': f'{self.category}',}
            return self.s.get('https://service2.diplo.de/rktermin/extern/appointment_showMonth.do', params=params, cookies=cookies, headers=headers)
        elif page_name == 'appointments':
            code = kwargs['code']
            cookies = {'JSESSIONID': f'{self.session_id}','KEKS': f'{self.termin[1]}',}
            headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'max-age=0', 'Connection': 'keep-alive', 'Origin': 'https://service2.diplo.de', 'Referer': f'https://service2.diplo.de/rktermin/extern/appointment_showMonth.do;jsessionid={self.session_id}', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36', 'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"macOS"',}
            data = {'captchaText': f'{code}', 'rebooking': 'false', 'token': '', 'lastname': '', 'firstname': '', 'email': '', 'locationCode': 'mins', 'realmId': '231', 'categoryId': f'{self.category}', 'openingPeriodId': '', 'date': '','dateStr': '', 'action:appointment_showMonth': 'Continue',}
            return self.s.post('https://service2.diplo.de/rktermin/extern/appointment_showMonth.do', cookies=cookies, headers=headers, data=data)
        elif page_name == 'register':
            date = kwargs['date']
            time = kwargs['time']
            cookies = {'JSESSIONID': f'{self.session_id}', 'KEKS': f'{self.termin[1]}',}
            headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8', 'Connection': 'keep-alive', 'Referer': f'https://service2.diplo.de/rktermin/extern/appointment_showDay.do?locationCode=mins&realmId=231&categoryId={self.category}&dateStr={date}', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36', 'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"macOS"',}
            params = {'locationCode': 'mins', 'realmId': '231', 'categoryId': f'{self.category}', 'dateStr': f'{date}', 'openingPeriodId': f'{time}',}
            return self.s.get('https://service2.diplo.de/rktermin/extern/appointment_showForm.do', params=params, cookies=cookies, headers=headers)
        elif page_name == 'refresh_captcha':
            import requests
            cookies = {'JSESSIONID': f'{self.session_id}', 'KEKS': f'{self.termin[1]}',}
            headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9','Accept-Language': 'en-US,en;q=0.9,ru;q=0.8', 'Cache-Control': 'max-age=0', 'Connection': 'keep-alive', 'Origin': 'https://service2.diplo.de', 'Referer': 'https://service2.diplo.de/rktermin/extern/appointment_showMonth.do', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate','Sec-Fetch-Site': 'same-origin','Sec-Fetch-User': '?1','Upgrade-Insecure-Requests': '1','User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36','sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"macOS"',}
            data = {'action:appointment_refreshCaptchamonth': 'Load another picture', 'locationCode': 'mins', 'realmId': '231', 'categoryId': f'{self.category}'}
            return self.s.post(f'https://service2.diplo.de/rktermin/extern/appointment_refreshCaptchamonth.do;jsessionid={self.session_id}', cookies=cookies, headers=headers, data=data)