import json
import multiprocessing
from datetime import datetime

users_dict =[
    {"email": "96456259@mail.ru", "password": "Viza2020!", "surname": "RYVINA", "name": "ELVIRA", "date_from": "09/06/2022", "date_to": "04/07/2022"},
    {"email": "barkar.nastya@bk.ru", "password": "Viza2020!", "surname": "LISKOVICH", "name": "ALINA", "date_from": "09/06/2022", "date_to": "30/07/2022"},
    {"email": "germanvisa@mail.ru", "password": "Visa2020!", "surname": "SAFONAVA", "name": "TATSIANA", "date_from": "", "date_to": "15/08/2022"},
    {"email": "masha.list.66@mail.ru", "password": "Vl6689563*", "surname": "SHPAKAVA", "name": "MARYIA", "date_from": "05/06/2022", "date_to": "24/08/2022"},
    {"email": "igor.epshteyn@bk.ru", "password": "Viza2020!", "surname": "ASTRAUSKENE", "name": "LARYSA", "date_from": "20/06/2022", "date_to": "15/08/2022"},
    {"email": "lhryb@bk.ru", "password": "Visa2020!", "surname": "GNATENKO", "name": "YEKATERINA", "date_from": "14/07/2022", "date_to": "22/08/2022"},
    {"email": "yulya.maiseyenka@mail.ru", "password": "Visa2020!", "surname": "PIATRUSHKA", "name": "VITALI", "date_from": "14/07/2022", "date_to": "22/08/2022"},
    {"email": "kkotiki25@yandex.by", "password": "Visa2020!", "surname": "PASIUKEVICH", "name": "YURY", "date_from": "10/08/2022", "date_to": "20/08/2022"},
    {"email": "shary.u@yandex.by", "password": "Visa2020!", "surname": "PASIUKEVICH", "name": "LARYSA", "date_from": "10/08/2022", "date_to": "20/08/2022"}
]
family_list = {}
available_users = [{'reason': 'Tourism', 'surname': 'SOBALEVA', 'name': 'LIUDMILA', 'passport_number': 'AB3523012', 'birth_day': '11/06/1981', 'passport_issued': '27/01/2020', 'passport_expired': '27/01/2030', 'issued_by': 'MIA', 'phone_number': '298088808', 'nationality': 'Belarus', 'travel_date': '05/04/2022', 'date_from': '13/07/2022', 'date_to': '25/08/2022', 'family': '1', 'dates': ['14.07.2022']}, {'reason': 'Tourism', 'surname': 'RULIAK', 'name': 'DARYA', 'passport_number': 'AB3404045', 'birth_day': '26/06/2005', 'passport_issued': '31/01/2019', 'passport_expired': '31/01/2029', 'issued_by': 'MIA', 'phone_number': '298088808', 'nationality': 'Belarus', 'travel_date': '05/04/2022', 'date_from': '13/07/2022', 'date_to': '25/08/2022', 'family': '1', 'dates': ['14.07.2022']}, {'reason': 'Tourism', 'surname': 'IVANOVA', 'name': 'INA', 'passport_number': 'MP4234204', 'birth_day': '03/09/1959', 'passport_issued': '16/08/2018', 'passport_expired': '16/08/2028', 'issued_by': 'MIA', 'phone_number': '295902233', 'nationality': 'Belarus', 'travel_date': '05/04/2022', 'date_from': '13/07/2022', 'date_to': '25/08/2022', 'family': '3', 'dates': ['14.07.2022']}]
for user in available_users:
    if user['family'] not in family_list:
        family_list[user['family']] = [user]
    else:
        family_list[user['family']].append(user)

user = ['1', '2', '3']
print(user[1:])
    # if not any(d['family'] == user['family'] for d in family_list):
    #     family_list.append(user)
    # else:
    #     index = next((index for (index, d) in enumerate(family_list) if d["family"] == user["family"]), None)
    #     family_list[index].extend(user)

dates_list = ['14.07.2022', '15.07.2022']

available_dates = {}
# ['14.07.2022', '15.07.22']
for date in dates_list:
    for i, user in enumerate(users_dict):
        date_from = datetime.strptime(user['date_from'] if user['date_from'] else '01/01/2022', '%d/%m/%Y')
        date_to = datetime.strptime(user['date_to'] if user['date_to'] else '01/01/3000', '%d/%m/%Y')
        actual_date = datetime.strptime(date, '%d.%m.%Y')
        if date_from < actual_date < date_to:
            users_dict[i].setdefault("dates",[]).append(date)

print([d for d in users_dict if 'dates' in d])

pool = multiprocessing.Pool(4)
out1, out2, out3 = zip(*pool.map(calc_stuff, range(0, 10 * offset, offset)))





# print(available_days)