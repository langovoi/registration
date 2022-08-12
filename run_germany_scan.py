import sys
import traceback
from time import sleep
from germany import Germany
from utils import telegram


def register_german_visa(termin, category, vc_type):
    g = Germany(termin=termin, category=category, vc_type=vc_type)
    # get captcha from login_page
    code, html = g.open_login_page_get_captcha_code()
    if code:
        while True:
            date_slots, code = g.open_appointments_page_and_get_dates(code, html)
            print(code)
            if date_slots and g.users_dict:
                # # get registration page
                # response = g.get_time(date_slots[0])
                # soup = BeautifulSoup(response.text, "lxml")
                # element = soup.find_all("div", {'style': 'margin-left: 20%;'})
                # time_slots = [[re.findall("\d+", link.text)[0], link.find("a")['href'].split('=')[-1]] for link in element if link.find("a")]
                # code, html = g.open_register_page(date_slots[0], time_slots[0][1])
                # telegram.send_doc(caption='!!!!!!!!!!!!!!!!!!!!!!!! Страниц регистрации: ', html=str(html))
                family_list = g.get_users_with_dates(date_slots, vc_type=vc_type)
                if family_list:
                    telegram.send_message(
                        f'🇩🇪 Подходящие клиенты: {[[(user["vc_passport"], user["vc_surname"], user["vc_name"]) for user in family_list[family]] for family in family_list]}')
                    g.register_users(date_slots, vc_type)
                # else:
                #     telegram.send_message(
                #         f'🟡 Германия {g.categories[g.category]}: Нет пользователей для регистрации на {date_slots}')
            sleep(60)



while True:
    try:
        termin = ['TERMIN325', sys.argv[3]]
        category = sys.argv[4]
        register_german_visa(termin, category, sys.argv[5])
        sleep(300 if sys.argv[5] == 'Inviting' else 120)
    except Exception as e:
        telegram.send_message(f'⭕ Restart Germany job. Failed with {str(e)}: \n{traceback.format_exc()}')
