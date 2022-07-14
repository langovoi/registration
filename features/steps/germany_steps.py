import re
from datetime import datetime

from behave import step, use_step_matcher

from utils import telegram

use_step_matcher('re')


@step("gather germany dates")
def gather_dates(context):
    # check 3 months
    gather_all_dates(context, number_of_months=3)
    # if dates - register
    if 'dates' in context.values and context.values['dates']:
        telegram.send_document(context, caption=f'Появились даты для Германии: context.values["dates"]')
        telegram.send_message(f'Начинаю регистрировать:\n{context.values["available_users"]}')
    else:
        raise RuntimeError('autoretry')


def gather_all_dates(context, number_of_months: int):
    for _ in range(number_of_months):
        for date_slot in context.page.get_elements('dates section'):
            if date_slot.text:
                context.values['dates'].append(date_slot.text.split('\n')[0].split()[1])
        context.page.click_on('next month button')
        if context.page.is_element_displayed('captcha field', timeout=1):
            context.page.type_in('captcha', 'captcha field')
    # get dates from api
    dates_list = context.values['dates']
    users_dict = [{"reason": "Tourism", "surname": "SOBALEVA", "name": "LIUDMILA", "passport_number": "AB3523012",
                   "birth_day": "11/06/1981", "passport_issued": "27/01/2020", "passport_expired": "27/01/2030",
                   "issued_by": "MIA", "phone_number": "298088808", "nationality": "Belarus",
                   "email": "germanvisa@mail.ru",
                   "travel_date": "05/04/2022", "date_from": "13/07/2022", "date_to": "25/08/2022", "family": "1"},
                  {"reason": "Tourism", "surname": "RULIAK", "name": "DARYA", "passport_number": "AB3404045",
                   "birth_day": "26/06/2005", "passport_issued": "31/01/2019", "passport_expired": "31/01/2029",
                   "issued_by": "MIA", "phone_number": "298088808", "nationality": "Belarus",
                   "email": "masha.list.66@mail.ru",
                   "travel_date": "05/04/2022", "date_from": "13/07/2022", "date_to": "25/08/2022", "family": "1"},
                  {"reason": "Tourism", "surname": "KALESNIKAVA", "name": "ANASTASIYA", "passport_number": "MP4156209",
                   "birth_day": "06/07/1987", "passport_issued": "19/04/2018", "passport_expired": "19/04/2028",
                   "issued_by": "MIA", "phone_number": "293652034", "nationality": "Belarus", "email": "lhryb@bk.ru",
                   "travel_date": "30/04/2022", "date_from": "24/07/2022", "date_to": "08/08/2022", "family": "2"},
                  {"reason": "Tourism", "surname": "IVANOVA", "name": "INA", "passport_number": "MP4234204",
                   "birth_day": "03/09/1959", "passport_issued": "16/08/2018", "passport_expired": "16/08/2028",
                   "issued_by": "MIA", "phone_number": "295902233", "nationality": "Belarus",
                   "email": "yulya.maiseyenka@mail.ru",
                   "travel_date": "05/04/2022", "date_from": "13/07/2022", "date_to": "25/08/2022", "family": "3"}]

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
        register_user(context, users[user])
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
                time_link.click()
                # context.page.enter_captcha()
                context.page.type_in('surname field', user[0]['surname'])
                context.page.type_in('name field', user[0]['name'])
                context.page.type_in('email field', user[0]['email'])
                context.page.type_in('confirm email field', user[0]['email'])
                context.page.select_by_text('applicants number dropdown', str(len(user)))
                context.page.type_in('passport number field', user[0]['passport_number'])
                if len(user) > 1:
                    add_users = ''
                    for additional_users in user[1:]:
                        add_users = f'{add_users} {additional_users["surname"]} {additional_users["name"]} {additional_users["passport_number"]}'
                    context.page.type_in('other participants field', add_users)
                context.page.type_in('aim field', user[0]['reason'])
                context.page.type_in('phone number field', user[0]['phone_number'])
                context.page.click_on('confirm checkbox')
                context.page.click_on('captcha field')
                context.page.enter_captcha()
                telegram.send_document(context, caption=f'🇩🇪 {user[0]["surname"]} {user[0]["name"]} записан на {date}')
                context.page.click_on('confirm appointments link')
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
        if int(re.findall("\d+", time.text)[0]) >= len(user):
            times.append(time.find_element_by_xpath('//a'))
    return times


@step("monitor germany")
def monitor(context):
    while True:
        try:
            context.execute_steps(u'''
                When open url: "https://service2.diplo.de/rktermin/extern/appointment_showMonth.do?locationCode=mins&realmId=231&categoryId=373"
                Then page german visa is opened
                When enter "captcha" in captcha field
                When click on continue button
                When clear log
                When gather dates
                When click on next month button
                When gather dates
                When click on next month button
                When send dates
            ''')
        except Exception as e:
            context.bot.send_photo(chat_id=context.config['telegram']['telegram_to'],
                                   photo=context.driver.get_screenshot_as_png(),
                                   caption=f'Unknown exception: {str(e)}')
            with open('page_source.html', 'w') as f:
                f.write(context.driver.page_source)
            telegram.send_document(context, caption=f'Unknown exception: {str(e)}')
        finally:
            context.driver.delete_all_cookies()
