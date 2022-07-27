import json
import re
import traceback
from time import sleep
import sys

import requests
from bs4 import BeautifulSoup

from germany import Germany
from utils import telegram, captcha


def get_germany_users(vc_type):
    s = requests.Session()
    s.auth = ('rest_user', sys.argv[1])
    users = s.get(sys.argv[2])
    users = [user for user in json.loads(users.text) if user["vc_type"] == vc_type]
    return users  # test users [{'id': '1', 'vc_status': '2', 'vc_city': 'Schengenvisa', 'vc_type': 'Inviting', 'vc_mail': 'sash.kardash@gmail.com', 'vc_inviting': 'Grigory Fray', 'vc_passport': 'MP8338818', 'vc_birth': '1965-10-16', 'vc_passport_from': '2021-07-20', 'vc_passport_to': '2031-07-20', 'vc_passport_by': 'MIA', 'vc_name': 'Valery', 'vc_surname': 'Vetlitcky', 'vc_phone': '+375256062209', 'vc_date_first_travel': '2022-08-15', 'vc_date_from': '2022-07-24', 'vc_date_to': '', 'vc_with': '0', 'vc_comment': '', 'vc_first': '1', 'vc_today': '1', 'vc_before_visit': '0'}, {'id': '3', 'vc_status': '2', 'vc_city': 'Schengenvisa', 'vc_type': 'Inviting', 'vc_mail': 'sash.kardash@gmail.com', 'vc_inviting': 'Grigory Fray', 'vc_passport': 'MP8338818', 'vc_birth': '1965-10-16', 'vc_passport_from': '2021-07-20', 'vc_passport_to': '2031-07-20', 'vc_passport_by': 'MIA', 'vc_name': 'Valery', 'vc_surname': 'Vetlitcky', 'vc_phone': '+375256062209', 'vc_date_first_travel': '2022-08-15', 'vc_date_from': '2022-07-24', 'vc_date_to': '', 'vc_with': '0', 'vc_comment': '', 'vc_first': '1', 'vc_today': '1', 'vc_before_visit': '0'}]


def register_german_visa(termin, category, users_dict):
    g = Germany(termin=termin, category=category, users_dict=users_dict)
    # get captcha from login_page
    code = g.open_login_page_get_captcha_code()
    date_slots = g.open_appointments_page_and_get_dates(code)
    if date_slots and g.users_dict:
        # # get registration page
        # response = g.get_time(date_slots[0])
        # soup = BeautifulSoup(response.text, "lxml")
        # element = soup.find_all("div", {'style': 'margin-left: 20%;'})
        # time_slots = [[re.findall("\d+", link.text)[0], link.find("a")['href'].split('=')[-1]] for link in element if link.find("a")]
        # code, html = g.open_register_page(date_slots[0], time_slots[0][1])
        # telegram.send_doc(caption='!!!!!!!!!!!!!!!!!!!!!!!! Страниц регистрации: ', html=str(html))
        family_list = g.get_users_with_dates(date_slots)
        if family_list:
            telegram.send_message(
                f'🇩🇪 Подходящие клиенты: {[[(user["vc_passport"], user["vc_surname"], user["vc_name"]) for user in family_list[family]] for family in family_list]}')
            g.register_users(family_list, date_slots)
        else:
            telegram.send_message(
                f'🟡 Германия {g.categories[g.category]}: Нет пользователей для регистрации на {date_slots}')


while True:
    try:
        # National
        # termin = ['TERMIN325', 'TERMIN340']
        # category = '375'
        # register_german_visa(termin, category, users_dict=get_germany_users('Inviting'))

        # Schengen
        termin = ['TERMIN325', 'TERMIN327']
        category = '373'
        register_german_visa(termin, category, users_dict=get_germany_users('Inviting'))

        # Tourism
        termin = ['TERMIN325', 'TERMIN327']
        category = '2845'
        register_german_visa(termin, category, users_dict=get_germany_users('Tourism'))
        sleep(300)
    except Exception as e:
        telegram.send_message(f'⭕ Germany job failed: {str(e)}: {traceback.format_exc()}')
