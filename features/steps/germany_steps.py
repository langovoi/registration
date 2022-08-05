import re
import subprocess
import traceback
from datetime import datetime
from multiprocessing import Pool
from time import sleep

from behave import step, when, then, use_step_matcher
from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains

from utils import telegram, captcha, users

use_step_matcher('re')


@step("monitor germany dates")
def gather_dates(context):
    # check 3 months
    gather_all_dates(context, number_of_months=3)
    # if dates - register
    if 'dates' in context.values and context.values['dates']:
        telegram.send_message(f'Начинаю регистрировать:\n{context.values["available_users"]}')
    else:
        raise RuntimeError('autoretry')


def gather_all_dates(context, number_of_months: int):
    for _ in range(number_of_months):
        for date_slot in context.page.get_elements('dates section'):
            if date_slot.text and date_slot.text.split('\n')[0].split()[1] != '':
                date = date_slot.text.split('\n')[0].split()[1]
                if date not in context.values['dates']:
                    context.values['dates'].append(date)
        context.page.click_on('next month button')
        context.page.enter_captcha()
        if context.page.is_element_displayed('captcha field', timeout=1):
            context.page.type_in('captcha', 'captcha field')
    if context.values['dates']:
        telegram.send_document(context, caption=f"🇩🇪 Появились даты для Германии:{context.values['dates']} 🇩🇪")
    # get dates from api
    dates_list = context.values['dates']
    users_dict = [
        {"reason": "Посещение родственников/друзей/знакомых", "surname": "TSIUKHAI", "name": "DZIANIS",
         "email": "ivan_lorkin@mail.ru",
         "passport_number": "MP4753020", "birth_day": "07/06/2001", "passport_issued": "13/04/2021",
         "passport_expired": "13/4/2031", "issued_by": "MIA", "phone_number": "375295497118", "nationality": "Belarus",
         "travel_date": "05/11/2022", "date_from": "13/07/2022", "date_to": "25/10/2022", "family": "1"},
        {"reason": "Посещение родственников/друзей/знакомых", "surname": "NOVIKAU", "name": "ALIAKSANDR",
         "email": "n-pestretsov@mail.ru",
         "passport_number": "BM2183681", "birth_day": "02/02/1989", "passport_issued": "05/04/2022",
         "passport_expired": "5/4/2032", "issued_by": "MIA", "phone_number": "375295023120", "nationality": "Belarus",
         "travel_date": "05/11/2022", "date_from": "13/07/2022", "date_to": "25/10/2022", "family": "2"},
        {"reason": "Посещение родственников/друзей/знакомых", "surname": "BAKUNOVICH", "name": "DZMITRY",
         "email": "dobrushin.2021@mail.ru",
         "passport_number": "PD0039632", "birth_day": "18/11/1972", "passport_issued": "29/08/2017",
         "passport_expired": "29/08/2027", "issued_by": "MIA", "phone_number": "375336374028",
         "nationality": "Belarus", "travel_date": "05/11/2022", "date_from": "13/10/2022", "date_to": "25/08/2022",
         "family": "3"},
        {"reason": "Посещение родственников/друзей/знакомых", "surname": "TRAFIMCHYK", "name": "MARYIAEVIALINA",
         "email": "yevgeniya.chekulova@mail.ru", "passport_number": "MC3428596", "birth_day": "08/07/2010",
         "passport_issued": "20/08/2020",
         "passport_expired": "20/08/2030", "issued_by": "MIA", "phone_number": "375333582710",
         "nationality": "Belarus", "travel_date": "05/11/2022", "date_from": "13/07/2022", "date_to": "25/10/2022",
         "family": "4"},
        {"reason": "Посещение родственников/друзей/знакомых", "surname": "HUSAK", "name": "LIZAVETA",
         "email": "karolina.rytik.rytko@mail.ru",
         "passport_number": "MP4280922", "birth_day": "15/03/2011", "passport_issued": "15/09/2027",
         "passport_expired": "15/09/2027", "issued_by": "MIA", "phone_number": "375291205453",
         "nationality": "Belarus", "travel_date": "05/11/2022", "date_from": "13/07/2022", "date_to": "25/10/2022",
         "family": "5"}]

    # ['14.07.2022', '15.07.22']
    for date in dates_list:
        for i, user in enumerate(users_dict):
            date_from = datetime.strptime(user['date_from'] if user['date_from'] else '01/01/2022', '%d/%m/%Y')
            date_to = datetime.strptime(user['date_to'] if user['date_to'] else '01/01/3000', '%d/%m/%Y')
            actual_date = datetime.strptime(date, '%d.%m.%Y')
            if date_from < actual_date <= date_to:
                users_dict[i].setdefault("dates", []).append(date)
    available_users = [d for d in users_dict if 'dates' in d]
    family_list = {}
    for user in available_users:
        if user['family'] not in family_list:
            family_list[user['family']] = [user]
        else:
            family_list[user['family']].append(user)
    context.values["available_users"] = family_list


@step("register germany")
def register_germany(context):
    # [{'email': 'barkar.nastya@bk.ru', 'password': 'Viza2020!', 'surname': 'LISKOVICH', 'name': 'ALINA', 'date_from': '09/06/2022', 'date_to': '30/07/2022', 'dates': ['14.07.2022']}, {'email': 'germanvisa@mail.ru', 'password': 'Visa2020!', 'surname': 'SAFONAVA', 'name': 'TATSIANA', 'date_from': '', 'date_to': '15/08/2022', 'dates': ['14.07.2022']}, {'email': 'masha.list.66@mail.ru', 'password': 'Vl6689563*', 'surname': 'SHPAKAVA', 'name': 'MARYIA', 'date_from': '05/06/2022', 'date_to': '24/08/2022', 'dates': ['14.07.2022']}, {'email': 'igor.epshteyn@bk.ru', 'password': 'Viza2020!', 'surname': 'ASTRAUSKENE', 'name': 'LARYSA', 'date_from': '20/06/2022', 'date_to': '15/08/2022', 'dates': ['14.07.2022']}]
    users = context.values['available_users']
    for user in users:
        try:
            register_user(context, users[user])
        except Exception:
            pass
    # # register all users
    # with Pool(processes=3) as p:
    #     p.map(merge_names, names)


def register_user(context, user):
    # {'email': 'barkar.nastya@bk.ru', 'password': 'Viza2020!', 'surname': 'LISKOVICH', 'name': 'ALINA', 'date_from': '09/06/2022', 'date_to': '30/07/2022', 'dates': ['14.07.2022']}
    dates = user[0]['dates']
    for date in dates:
        success = False
        context.driver.get(
            f'https://service2.diplo.de/rktermin/extern/appointment_showDay.do?locationCode=mins&realmId=231&categoryId=373&dateStr={date}')
        context.page.enter_captcha()
        time_links = get_available_time(context, user)
        for time_link in time_links:
            try:
                context.driver.find_element_by_xpath(f'//a[contains(@href, "{time_link}")]').click()
                # context.page.enter_captcha()
                context.page.type_in('surname field', user[0]['surname'])
                context.page.type_in('name field', user[0]['name'])
                context.page.type_in('email field', user[0]['email'])
                context.page.type_in('confirm email field', user[0]['email'])
                context.page.select_by_text('applicants number dropdown', str(len(user)))
                context.page.type_in('passport number field', user[0]['passport_number'])
                context.page.type_in('birth day field', user[0]['birth_day'])
                if len(user) > 1:
                    add_users = ''
                    for additional_users in user[1:]:
                        add_users = f'{add_users} {additional_users["surname"]} {additional_users["name"]} {additional_users["passport_number"]}'
                    context.page.type_in('other participants field', add_users)
                # context.page.type_in('aim field', user[0]['reason'])
                context.page.select_by_text('aim dropdown', user[0]['reason'])
                context.page.type_in('host name field', 'Eugen Fridrich')
                context.page.type_in('phone number field', user[0]['phone_number'])
                if context.page.is_element_displayed('confirm checkbox', timeout=0):
                    context.page.click_on('confirm checkbox')
                context.page.click_on('captcha field')
                context.page.enter_captcha()
                if context.page.is_element_displayed('confirm appointments link', timeout=1):
                    context.page.click_on('confirm appointments link')
                    telegram.send_document(
                        context, caption=f'🇩🇪 {user[0]["surname"]} {user[0]["name"]} записан на {date}')
                else:
                    telegram.send_document(
                        context,
                        caption=f'Не удалось зарегистрировать пользователя, после ввода данных: {user[0]["surname"]} {user[0]["name"]} на {date}')
                success = True
                break
            except Exception:
                pass
        if success: break
    else:
        raise RuntimeError(f'Не удалось записать пользователя на {dates}: {user[0]["surname"]} {user[0]["name"]}')


def get_available_time(context, user):
    available_times = context.driver.find_elements_by_xpath('//div/a[contains(@href, "openingPeriodId=")]/..')
    times = []
    for time in available_times:
        link = re.findall("href=\"(.*?)\"", time.get_attribute('innerHTML'))[0][::1].replace("&amp;", "&")
        # 'extern/appointment_showForm.do?locationCode=mins&amp;realmId=231&amp;categoryId=373&amp;dateStr=27.09.2022&amp;openingPeriodId=8809'
        times.append(link)
    return times



def register_family(args):
    user_id, members = args
    print(args)

@step('get german dates for "(?P<category>.*)" category')
def step_impl(context, category):
    soup = BeautifulSoup(context.driver.page_source, "lxml")
    type = context.page.categories[str(category)]['type']
    type = 'Inviting'
    name = context.page.categories[str(category)]['name']
    name = 'Шенген'
    while True:
        # enter captcha
        if captcha.is_captcha_displayed(str(soup)):
            for _ in range(3):
                code = captcha.get_code(str(soup))
                if code:
                    break
                else:
                    context.driver.refresh()
                    soup = BeautifulSoup(context.driver.page_source, "lxml")
            else:
                telegram.send_doc('Не смог ввести капчу c 3 раз', str(soup))
                raise RuntimeError('Не смог ввести капчу с 3 раз')
            context.page.type_in('captcha field', code)
            context.page.click_on('continue button')
            soup = BeautifulSoup(context.driver.page_source, "lxml")
            if captcha.is_captcha_displayed(str(soup)):
                sleep(10)
                continue
        # check if dates
        soup = BeautifulSoup(context.driver.page_source, "lxml")
        if 'Unfortunately' in str(soup) or 'ERR_ADDRESS_UNREACHABLE' in str(soup) or 'ERR_TIMED_OUT' in str(soup) or 'The server is currently busy' in str(soup):
            # no dates - refresh page
            sleep(10)
            context.driver.refresh()
            soup = BeautifulSoup(context.driver.page_source, "lxml")
        elif 'Termine sind verfügbar' in str(soup) or 'Запись на прием возможна' in str(soup) or 'Please select a date' in str(soup):
            element = soup.find_all("div", {'style': 'margin-left: 20%;'})
            dates_list = [link.find("a")['href'].split('=')[-1] for link in element]
            dates = [{'date': datetime.strptime(date, '%d.%m.%Y')} for date in dates_list]
            all_users = users.get_users(type)
            families = {}

            # create families
            for user in all_users:
                if user['vc_with'] == '0':
                    families[user['id']] = {'members': [user]}
                else:
                    if user['vc_with'] in families:
                        families[user['vc_with']]['members'].append(user)
                    else:
                        families[user['vc_with']]['members'] = user
            # assign dates
            for user_id, family in families.items():
                date_from = datetime.strptime(family['members'][0]['vc_date_from'] if family['members'][0]['vc_date_from'] else '2022-01-01', '%Y-%m-%d')
                date_to = datetime.strptime(family['members'][0]['vc_date_to'] if family['members'][0]['vc_date_to'] else '3000-01-01', '%Y-%m-%d')
                for date in dates:
                    if date_from <= date['date'] <= date_to:
                        families[user_id].setdefault("dates", []).append(date)
            context.values['eligible_families'] = eligible_families = {k: v for k, v in families.items() if 'dates' in v}
            subprocess.call(f'python3 behave-parallel.py --tags=register_family --processes=2', shell=True)
            # short_families = {k: [v['members'][0]['vc_name'], v['members'][0]['vc_surname'], f'кол-во: {len(v["members"])}'] for k, v in eligible_families.items()}
            # telegram.send_message(f'🇩🇪 Германия {name}: {dates_list}\nПодходящие: {short_families}')
        else:
            telegram.send_doc('Неизвестная ошибка на странице дат', str(soup))
            raise RuntimeError('Неизвестная ошибка на странице дат')


@when("register_family")
def step_impl(context):
    import configparser
