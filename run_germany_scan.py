import json
import os
import re
from time import sleep

import requests
from bs4 import BeautifulSoup

from germany import Germany
from utils import telegram


def get_germany_users(vc_type):
    s = requests.Session()
    s.auth = ('rest_user', os.environ['REST_PASSWORD'])
    users = s.get(os.environ['GERMANY_REST_URL'])
    users = [user for user in json.loads(users.text) if user["vc_type"] == vc_type]
    for i, user in enumerate(users):
        if 'vc_status' not in user or user['vc_status'] != 1:
            users[i]['vc_status'] = 0
    return users


def register_german_visa(termin, category, users_dict):
    g = Germany(termin=termin, category=category, users_dict=users_dict)
    ready_to_register_users = [user for user in g.users_dict if user['vc_status'] == 0]
    date_slots = g.get_dates()
    if date_slots:

        # get registration page
        response = g.get_time(date_slots[0])
        soup = BeautifulSoup(response.text, "lxml")
        element = soup.find_all("div", {'style': 'margin-left: 20%;'})
        time_slots = [[re.findall("\d+", link.text)[0], link.find("a")['href'].split('=')[-1]] for link in element if link.find("a")]
        code, html = g.open_register_page(date_slots[0], time_slots[0][1])
        telegram.send_doc(caption='!!!!!!!!!!!!!!!!!!!!!!!! Страниц регистрации: ', html=str(html))

        if ready_to_register_users:
            family_list = g.get_users_with_dates(date_slots)
            telegram.send_message(
                f'🇩🇪 Подходящие клиенты: {[[(user["vc_passport"], user["vc_surname"], user["vc_name"]) for user in family_list[family]] for family in family_list]}')
            return # remove
            success_families_list = g.register_users(family_list, date_slots)
            # check status = 1 and update user_dict with only not registered users(status = 0)
            for i, user in enumerate(ready_to_register_users):
                for family_user in success_families_list:
                    if user['vc_surname'] == family_user['vc_surname'] and \
                            user['vc_name'] == family_user['vc_name'] and \
                            user['vc_passport'] == family_user['vc_passport']:
                        g.users_dict[i]['vc_status'] = 1
        else:
            telegram.send_message(
                f'🟡 Германия {g.categories[g.category]}: Нет пользователей для регистрации на {date_slots}')
    return g.users_dict


n_user_dict = get_germany_users('National')
s_user_dict = get_germany_users('Inviting')
t_user_dict = get_germany_users('Tourism')

while True:
    try:
        # National
        termin = ['TERMIN325', 'TERMIN340']
        category = '375'
        n_user_dict = register_german_visa(termin, category, users_dict=n_user_dict)

        # Schengen
        termin = ['TERMIN325', 'TERMIN327']
        category = '373'
        s_user_dict = register_german_visa(termin, category, users_dict=s_user_dict)

        # Tourism
        termin = ['TERMIN325', 'TERMIN327']
        category = '2845'
        t_user_dict = register_german_visa(termin, category, users_dict=t_user_dict)
        sleep(300)
    except Exception as e:
        telegram.send_message(f'⭕ Germany job failed: {str(e)}')
