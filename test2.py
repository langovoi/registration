import json
import os
from google.oauth2.service_account import Credentials

from selenium import webdriver

appState = {
    "recentDestinations": [
        {
            "id": "Save as PDF",
            "origin": "local"
        }
    ],
    "selectedDestinationId": "Save as PDF",
    "version": 2
}

profile = {"printing.print_preview_sticky_settings.appState": json.dumps(appState),
           'savefile.default_directory': "/Users/alexandrkardash/Documents"}
profile["download.prompt_for_download"] = False
profile["profile.default_content_setting_values.notifications"] = 2
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('prefs', profile)
chrome_options.add_argument('--kiosk-printing')
# chrome_options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get('https://www.google.com/')

driver.execute_script("document.title = 'hello'")
driver.execute_script('window.print();')

scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

gs_key_file = config.create_json('email_key')
creds = Credentials.from_service_account_file(gs_key_file, scopes=scope)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = gs_key_file




# gs = gsheets.GoogleSheets('germany_registered')
#
# family = [{'id': '160', 'vc_status': '2', 'vc_city': 'Schengenvisa', 'vc_type': 'Inviting', 'vc_mail': 'pasichnik.miroslav@bk.ru', 'vc_inviting': 'MALLER ALEXEJ', 'vc_inviting_address': '', 'vc_passport': 'KH2779704', 'vc_birth': '1964-12-07', 'vc_passport_from': '2018-04-10', 'vc_passport_to': '2028-04-10', 'vc_passport_by': 'MIA', 'vc_name': 'NATALLIA', 'vc_surname': 'SHUNDRYK', 'vc_phone': '+375336867715', 'vc_date_first_travel': '2022-10-01', 'vc_date_from': '2022-09-20', 'vc_date_to': '2022-09-30', 'vc_with': '0', 'vc_comment': 'даты подачи|pasichnik.miroslav@bk.ru|', 'vc_first': '0', 'vc_today': '0', 'vc_before_visit': '0', 'dates': [['22.09.2022', '29296'], ['27.09.2022', '29285'], ['28.09.2022', '29271'], ['29.09.2022', '29257']]}, {'id': '161', 'vc_status': '2', 'vc_city': 'Schengenvisa', 'vc_type': 'Inviting', 'vc_mail': 'pavlov.karim@internet.ru', 'vc_inviting': 'MALLER ALEXEJ', 'vc_inviting_address': '', 'vc_passport': 'KH2652324', 'vc_birth': '1961-08-17', 'vc_passport_from': '2017-01-12', 'vc_passport_to': '2027-01-12', 'vc_passport_by': 'MIA', 'vc_name': 'SIARHEI', 'vc_surname': 'SHUNDRYK', 'vc_phone': '+375336867715', 'vc_date_first_travel': '2022-10-01', 'vc_date_from': '2022-09-20', 'vc_date_to': '2022-09-30', 'vc_with': '160', 'vc_comment': 'даты подачи|pavlov.karim@internet.ru|', 'vc_first': '1', 'vc_today': '0', 'vc_before_visit': '0'}, {'id': '163', 'vc_status': '2', 'vc_city': 'Schengenvisa', 'vc_type': 'Inviting', 'vc_mail': 'arkhipov.roman00@mail.ru', 'vc_inviting': 'MALLER ALEXANDER', 'vc_inviting_address': '', 'vc_passport': 'KH3116964', 'vc_birth': '2016-12-16', 'vc_passport_from': '2022-08-02', 'vc_passport_to': '2027-08-02', 'vc_passport_by': 'MIA', 'vc_name': 'YEVA', 'vc_surname': 'TSESTA', 'vc_phone': '+375336867715', 'vc_date_first_travel': '2022-10-01', 'vc_date_from': '2022-09-20', 'vc_date_to': '2022-09-30', 'vc_with': '160', 'vc_comment': 'даты подачи|arkhipov.roman00@mail.ru|', 'vc_first': '0', 'vc_today': '0', 'vc_before_visit': '0'}, {'id': '164', 'vc_status': '2', 'vc_city': 'Schengenvisa', 'vc_type': 'Inviting', 'vc_mail': 'ivashchenko.georgii@mail.ru', 'vc_inviting': 'MALLER ALEXANDER', 'vc_inviting_address': '', 'vc_passport': 'KH2544241', 'vc_birth': '1988-02-18', 'vc_passport_from': '2015-11-05', 'vc_passport_to': '2025-11-05', 'vc_passport_by': 'MIA', 'vc_name': 'INHA', 'vc_surname': 'TSESTA', 'vc_phone': '+375336867715', 'vc_date_first_travel': '2022-10-01', 'vc_date_from': '2022-09-20', 'vc_date_to': '2022-09-30', 'vc_with': '160', 'vc_comment': 'даты подачи|ivashchenko.georgii@mail.ru|', 'vc_first': '0', 'vc_today': '0', 'vc_before_visit': '0'}]
# for member in family:
#     i = len(gs.ws.get_all_values()) + 1
#     cell_list = gs.ws.range(f'B{i}:H{i}')
#     cell_list[0].value = f'{member["id"]}, {member["vc_name"]}, {member["vc_surname"]}, {member["vc_passport"]}'
#     cell_list[1].value = member['vc_mail']
#     cell_list[2].value = datetime.today().date()
#     cell_list[3].value = datetime.today().date()
#     cell_list[4].value =
#     self.gs.ws.update_cells(cell_list)


