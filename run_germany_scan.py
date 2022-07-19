from time import sleep

from germany import Germany
from utils import telegram

user_dict = [
    {"status": 0,
     "reason": "Invitig",
     "surname": "ZHUK",
     "name": "VASILI",
     "email": "barkar.nastya@bk.ru",
     "passport_number": "MC3095945",
     "birth_day": "25/11/1963",
     "phone_number": "375291438870",
     "nationality": "Belarus",
     "travel_date": "01/08/2022",
     "date_from": "25/07/2022",
     "date_to": "",
     "family": "6"},
    {"status": 0,
     "reason": "Invitig",
     "surname": "ZHUK",
     "name": "MARYNA",
     "email": "barkar.nastya@bk.ru",
     "passport_number": "MC2813268",
     "birth_day": "23/12/1971",
     "phone_number": "375447651221",
     "nationality": "Belarus",
     "travel_date": "01/08/2022",
     "date_from": "25/07/2022",
     "date_to": "",
     "family": "6"}, ]


def register_german_visa(termin, category, reason):
    ready_to_register_users = [user for user in user_dict if user['status'] == 0 and user['reason'] == reason]
    g = Germany(termin=termin, category=category, users_dict=user_dict)
    date_slots = g.get_dates()
    if date_slots:
        if ready_to_register_users:
            family_list = g.get_users_with_dates(date_slots)
            success_families_list = g.register_users(family_list, date_slots)
            for i, user in enumerate(ready_to_register_users):
                for family_user in success_families_list:
                    if user['surname'] == family_user['surname'] and \
                            user['name'] == family_user['name'] and \
                            user['passport_number'] == family_user['passport_number']:
                        user_dict[i]['status'] = 1
        else:
            telegram.send_message(
                f'🟡 Германия {g.categories[g.category]}: Нет пользователей для регистрации на {date_slots}')


while True:
    try:
        # National
        termin = ['TERMIN325', 'TERMIN340']
        category = '375'
        register_german_visa(termin, category, 'National')

        # Schengen
        termin = ['TERMIN325', 'TERMIN327']
        category = '373'
        register_german_visa(termin, category, 'Invitig')

        # Tourism
        termin = ['TERMIN325', 'TERMIN327']
        category = '2845'
        register_german_visa(termin, category, 'Tourism')


        sleep(60)
    except Exception as e:
        telegram.send_message(f'⭕ Germany job failed: {str(e)}')
        sleep(60)
