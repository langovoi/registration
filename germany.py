import re
from datetime import datetime
from time import sleep

import requests
from bs4 import BeautifulSoup
from utils import captcha, telegram


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


def get_session_id(url):
    s = requests.Session()
    headers = { 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8', 'Connection': 'keep-alive', 'Referer': f'{url}','Sec-Fetch-Dest': 'document','Sec-Fetch-Mode': 'navigate','Sec-Fetch-Site': 'same-origin','Sec-Fetch-User': '?1','Upgrade-Insecure-Requests': '1','User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36','sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"macOS"',}
    s.get(url, headers=headers)
    return s.cookies.get_dict()['JSESSIONID']


class Germany():
    def __init__(self, termin, category, users_dict):
        self.s = requests.Session()
        self.session_id = ''
        self.termin = termin
        self.category = category
        self.users_dict = users_dict
        self.categories = {'373': "Шенген", '2845': "Туризм", '375': "Национальная"}

    def open_login_page(self):
        self.session_id = get_session_id(f'https://service2.diplo.de/rktermin/extern/appointment_showMonth.do?locationCode=mins&realmId=231&categoryId={self.category}')
        # login page
        cookies = {'JSESSIONID': f'JSESSIONID={self.session_id}','KEKS': f'{self.termin[0]}',}
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8', 'Cache-Control': 'max-age=0', 'Connection': 'keep-alive', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'none', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36', 'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"macOS"',}
        params = {'locationCode': 'mins', 'realmId': '231', 'categoryId': f'{self.category}',}
        r = self.s.get('https://service2.diplo.de/rktermin/extern/appointment_showMonth.do', params=params, cookies=cookies, headers=headers)

        soup = BeautifulSoup(r.text,"lxml")
        image = soup.select("captcha > div")
        image= image[0]['style'].split("url('")[1].split("')")[0]
        return captcha.get_code(image), soup

    def get_appointments(self, url, code, session_id):
        cookies = {'JSESSIONID': f'{session_id}','KEKS': f'{self.termin[1]}',}
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'max-age=0', 'Connection': 'keep-alive', 'Origin': 'https://service2.diplo.de', 'Referer': f'https://service2.diplo.de/rktermin/extern/appointment_showMonth.do;jsessionid={session_id}', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36', 'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"macOS"',}
        data = {'captchaText': f'{code}', 'rebooking': 'false', 'token': '', 'lastname': '', 'firstname': '', 'email': '', 'locationCode': 'mins', 'realmId': '231', 'categoryId': f'{self.category}', 'openingPeriodId': '', 'date': '','dateStr': '', 'action:appointment_showMonth': 'Continue',}
        return self.s.post(url, cookies=cookies, headers=headers, data=data).text

    def get_time(self, date):
        cookies = {'JSESSIONID': f'{self.session_id}', 'KEKS': f'{self.termin[1]}',}
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8', 'Connection': 'keep-alive', 'Referer': 'https://service2.diplo.de/rktermin/extern/appointment_showMonth.do', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36', 'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"macOS"',}
        params = {'locationCode': 'mins', 'realmId': '231', 'categoryId': f'{self.category}', 'dateStr': f'{date}',}
        r = self.s.get('https://service2.diplo.de/rktermin/extern/appointment_showDay.do', params=params, cookies=cookies, headers=headers)

        # check if captcha
        for _ in range(3):
            soup = BeautifulSoup(r.text, "lxml")
            if soup.find("captcha"):
                image = soup.select("captcha > div")
                image= image[0]['style'].split("url('")[1].split("')")[0]
                code = captcha.get_code(image)
                headers = {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8', 'Cache-Control': 'max-age=0', 'Connection': 'keep-alive', 'Origin': 'https://service2.diplo.de',
                    'Referer': f'https://service2.diplo.de/rktermin/extern/appointment_showDay.do?locationCode=mins&realmId=231&categoryId={self.category}&dateStr=f{date}',
                    'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
                    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"macOS"',}
                data = {'captchaText': f'{code}',
                    'rebooking': '', 'token': '', 'lastname': '', 'firstname': '', 'email': '', 'locationCode': 'mins', 'realmId': '231',
                    'categoryId': f'{self.category}', 'openingPeriodId': '', 'date': f'{date}', 'dateStr': f'{date}',}
                r = self.s.post('https://service2.diplo.de/rktermin/extern/appointment_showDay.do', cookies=cookies, headers=headers, data=data)
            else:
                break
        else:
            telegram.send_doc('Не разгадал капчу с 3 раз', r.text)
        return r

    def get_users_with_dates(self, dates_list):
        for date in dates_list:
            for i, user in enumerate(self.users_dict):
                date_from = datetime.strptime(user['vc_date_from'] if user['vc_date_from'] else '2022-01-01', '%Y-%m-%d')
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

    def get_dates(self):
        date_slots = []
        code, soup = self.open_login_page()
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
            else:
                if "background:white url('data:image/jpg" in html:
                    # telegram.send_doc(f'⭕ Captcha: Неверный код {code}. Попытка {i+1}', str(soup))
                    soup = BeautifulSoup(html,"lxml")
                    image = soup.select("captcha > div")
                    image= image[0]['style'].split("url('")[1].split("')")[0]
                    code = captcha.get_code(image)
                else:
                    telegram.send_doc('⭕ Ошибка, капча не отображается', str(html))
                sleep(10) # if captcha
        else:
            raise RuntimeError(f'⭕ Не разгадал капчу с 10 попыток для категории {self.categories[str(self.category)]}')
        return date_slots

    def register_users(self, family_list, date_slots): # get time and register
        success_families_list = []
        for index, family in family_list.items(): # check each user
            for date in date_slots:
                is_registered = False
                if date in family[0]['dates']: # get available time
                    response = self.get_time(date)
                    soup = BeautifulSoup(response.text, "lxml")
                    element = soup.find_all("div", {'style': 'margin-left: 20%;'})
                    time_slots = [[re.findall("\d+", link.text)[0], link.find("a")['href'].split('=')[-1]] for link in element if link.find("a")]
                    for time in time_slots:
                        success_users_list = self.fill_fields(family, date, time[1])
                        for member in success_users_list:
                            success_families_list.append(member)
                        if success_users_list:
                            is_registered = True
                            break
                    if is_registered:
                        break
        return success_families_list

    def open_register_page(self, date, time):
        cookies = {'JSESSIONID': f'{self.session_id}', 'KEKS': f'{self.termin[1]}',}
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8', 'Connection': 'keep-alive', 'Referer': f'https://service2.diplo.de/rktermin/extern/appointment_showDay.do?locationCode=mins&realmId=231&categoryId={self.category}&dateStr={date}', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36', 'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"macOS"',}
        params = {'locationCode': 'mins', 'realmId': '231', 'categoryId': f'{self.category}', 'dateStr': f'{date}', 'openingPeriodId': f'{time}',}
        r = self.s.get('https://service2.diplo.de/rktermin/extern/appointment_showForm.do', params=params, cookies=cookies, headers=headers)
        soup = BeautifulSoup(r.text,"lxml")
        image = soup.select("captcha > div")
        image= image[0]['style'].split("url('")[1].split("')")[0]
        return captcha.get_code(image), soup

    def fill_fields(self, family, date, time):
        code, html = self.open_register_page(date, time)
        telegram.send_doc(caption=f'🟢 🇩🇪 Германия {self.categories[self.category]}: Регистрирую ({date}:{time}): {family[0]["vc_surname"]} {family[0]["vc_name"]}({family[0]["vc_mail"]})', html=str(html))
        additional_users = ''
        if len(family) > 1:
            for additional_user in family[1:]:
                user = f"{additional_user['vc_surname']}, {additional_user['vc_name']}, {additional_user['vc_passport']}"
                additional_users = user if not additional_users else f'{additional_users}, {user}'
        cookies = {'JSESSIONID': f'{self.session_id}', 'KEKS': f'{self.termin[0]}',}
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'max-age=0', 'Connection': 'keep-alive', 'Origin': 'https://service2.diplo.de', 'Referer': 'https://service2.diplo.de/rktermin/extern/appointment_showForm.do', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36', 'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"macOS"',}
        data = {
            'lastname': f'{family[0]["vc_surname"]}', 'firstname': f'{family[0]["vc_name"]}', 'email': f'{family[0]["vc_mail"]}', 'emailrepeat': f'{family[0]["vc_mail"]}',
            'fields[0].content': f'{len(family)}', 'fields[0].definitionId': '940', 'fields[0].index': '0',
            'fields[1].content': f'{family[0]["vc_passport"]}', 'fields[1].definitionId': '941', 'fields[1].index': '1',
            'fields[2].content': f'{additional_users}', 'fields[2].definitionId': '942', 'fields[2].index': '2',
            'fields[3].content': f'{family[0]["vc_type"]}', 'fields[3].definitionId': '943', 'fields[3].index': '3',
            'fields[4].content': f'{family[0]["vc_phone"]}', 'fields[4].definitionId': '944', 'fields[4].index': '4',
            'fields[5].content': 'true', '__checkbox_fields[5].content': 'true', 'fields[5].definitionId': '945', 'fields[5].index': '5',
            'captchaText': f'{code}',
            'locationCode': 'mins', 'realmId': '231', 'categoryId': f'{self.category}', 'openingPeriodId': f'{time}', 'date': f'{date}', 'dateStr': f'{date}', 'action:appointment_addAppointment': 'Speichern',}
        # r = self.s.post('https://service2.diplo.de/rktermin/extern/appointment_addAppointment.do', cookies=cookies, headers=headers, data=data)
        # html = BeautifulSoup(r.text,"lxml")
        success_user_list = []
        if html.find("select", {"name" : "fields[0].content"}):
            telegram.send_doc(caption=f'⭕ 🇩🇪 Германия {self.categories[self.category]}: не смог зарегистрировать ({date}:{time}): {family[0]["vc_surname"]} {family[0]["vc_name"]}({family[0]["vc_mail"]})', html=str(html))
        else:
            for member in family:
                success_user_list.append(member)
            telegram.send_doc(caption=f'🟢 🇩🇪 Успешно зарегистрирован: {family[0]["vc_surname"]} {family[0]["vc_name"]}({family[0]["vc_mail"]}) на дату: {date}:{time}', html=str(html))
        return success_user_list
