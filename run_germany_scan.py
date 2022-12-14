import logging
import sys
import traceback
from multiprocessing import Pool
from time import sleep
from germany import Germany
from utils import telegram
from copy import deepcopy

termin = ['TERMIN325', sys.argv[3]]
category = sys.argv[4]
vc_type = sys.argv[5]


def register_german_visa(termin, category, vc_type):
    g = Germany(termin=termin, category=category, vc_type=vc_type)
    # get captcha from login_page
    code, html = g.open_login_page_get_captcha_code()
    if code:
        while True:
            date_time_slots, code = g.open_appointments_page_and_get_dates(code)
            print(code)
            if date_time_slots:
                family_list = g.get_users_with_dates(date_time_slots, vc_type=vc_type)
                if family_list:
                    families = [f for i, f in family_list.items()]
                    families.sort(key=len, reverse=True)
                    fam_str = '\n'.join([f'{family[0]["vc_surname"]} {family[0]["vc_name"]} из {len(family)} членов на {family[0]["dates"]}' for family in families])
                    g.message = g.message + f'🟡 Германия {g.categories[category]}: Начинаю регистрировать:\n{fam_str}'
                    with Pool(len(families) if len(families) < 9 else 8) as p:
                        p.map(register, families)
                    if g.message:
                        telegram.send_message(g.message)
                else:
                    sleep(3600 if sys.argv[5] == 'National' else 60)
            else:
                sleep(3600 if sys.argv[5] == 'National' else 60)
                # else:
                #     telegram.send_message(
                #         f'🟡 Германия {g.categories[g.category]}: Нет пользователей для регистрации на {date_slots}')


def register(family):
    g = Germany(termin=termin, category=category, vc_type=vc_type)
    # get captcha from login_page
    date_slots = family[0]['dates']
    for date, time in date_slots:
        code, html = g.open_login_page_get_captcha_code()
        g.open_page('appointments', code=code)
        sleep(1)
        code, soup = g.open_register_page(date, time)
        if None in (code, soup):
            continue
        html = str(soup)
        is_registered = g.register_family(family, date, time, code, soup)
        logging.warning(f'is_registered: {is_registered}')
        html_log = '\n\n'.join(x for x in html.splitlines() if x.strip())
        logging.warning(
            f'========================== Германия {g.categories[g.category]}: Страница заполнения полей:\n'
            f'{html_log}\n'
            f'==========================')
        if is_registered:
            break


if __name__ == "__main__":
    while True:
        try:
            register_german_visa(termin, category, vc_type)
            sleep(3600 if sys.argv[5] == 'National' else 60)
        except Exception as e:
            telegram.send_message(f'⭕ Restart Germany job. Failed with {str(e)}: \n{traceback.format_exc()}')
