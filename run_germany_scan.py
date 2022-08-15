import sys
import traceback
from multiprocessing import Pool
from time import sleep
from germany import Germany
from utils import telegram


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
                    # # get registration page
                    # response = g.get_time(date_slots[0])
                    # soup = BeautifulSoup(response.text, "lxml")
                    # element = soup.find_all("div", {'style': 'margin-left: 20%;'})
                    # time_slots = [[re.findall("\d+", link.text)[0], link.find("a")['href'].split('=')[-1]] for link in element if link.find("a")]
                    # code, html = g.open_register_page(date_slots[0], time_slots[0][1])
                    # telegram.send_doc(caption='!!!!!!!!!!!!!!!!!!!!!!!! Страниц регистрации: ', html=str(html))
                    family = [f for i, f in family_list.items()]
                    family.sort(key=len, reverse=True)
                    with Pool(len(family) if len(family) < 9 else 8) as p:
                        p.map(register, family)
            else:
                sleep(60)
                # else:
                #     telegram.send_message(
                #         f'🟡 Германия {g.categories[g.category]}: Нет пользователей для регистрации на {date_slots}')


def register(family):
    try:
        g = Germany(termin=['TERMIN325', sys.argv[3]], category=sys.argv[4], vc_type=sys.argv[5])
        # get captcha from login_page
        code, html = g.open_login_page_get_captcha_code()
        date_slots = [x for x in family[0]['dates'][::-1]]
        telegram.send_message(f'Регистрирую семью {family[0]["vc_surname"]} {family[0]["vc_name"]} из {len(family)} членов на {date_slots}')
        for date, time in date_slots:
            g.open_page('appointments', code=code)
            code, soup = g.open_register_page(date, time)
            html = str(soup)
            telegram.send_doc(f'Германия {g.categories[g.category]}: Страница заполнения полей', html)
            is_registered = g.register_family(family, date, time, code, soup)
            if is_registered:
                break
        else:
            raise RuntimeError(f'Не удалось зарегистрировать семью: {family}')
    except Exception as e:
        raise RuntimeError(f'Ошибка {str(e)} при регистрации семьи: {family}')


if __name__ == "__main__":
    while True:
        try:
            termin = ['TERMIN325', sys.argv[3]]
            category = sys.argv[4]
            register_german_visa(termin, category, sys.argv[5])
            sleep(300 if sys.argv[5] == 'Inviting' else 60)
        except Exception as e:
            telegram.send_message(f'⭕ Restart Germany job. Failed with {str(e)}: \n{traceback.format_exc()}')
