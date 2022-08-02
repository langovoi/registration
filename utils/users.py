import json
import sys

import requests

s = requests.Session()
s.auth = ('rest_user', sys.argv[1])


def get_users(vc_type):
    users = s.get(sys.argv[2])
    users = [user for user in json.loads(users.text) if user["vc_type"] == vc_type]
    return users  # test users [{'id': '1', 'vc_status': '2', 'vc_city': 'Schengenvisa', 'vc_type': 'Inviting', 'vc_mail': 'sash.kardash@gmail.com', 'vc_inviting': 'Grigory Fray', 'vc_passport': 'MP8338818', 'vc_birth': '1965-10-16', 'vc_passport_from': '2021-07-20', 'vc_passport_to': '2031-07-20', 'vc_passport_by': 'MIA', 'vc_name': 'Valery', 'vc_surname': 'Vetlitcky', 'vc_phone': '+375256062209', 'vc_date_first_travel': '2022-08-15', 'vc_date_from': '2022-07-24', 'vc_date_to': '', 'vc_with': '0', 'vc_comment': '', 'vc_first': '1', 'vc_today': '1', 'vc_before_visit': '0'}, {'id': '3', 'vc_status': '2', 'vc_city': 'Schengenvisa', 'vc_type': 'Inviting', 'vc_mail': 'sash.kardash@gmail.com', 'vc_inviting': 'Grigory Fray', 'vc_passport': 'MP8338818', 'vc_birth': '1965-10-16', 'vc_passport_from': '2021-07-20', 'vc_passport_to': '2031-07-20', 'vc_passport_by': 'MIA', 'vc_name': 'Valery', 'vc_surname': 'Vetlitcky', 'vc_phone': '+375256062209', 'vc_date_first_travel': '2022-08-15', 'vc_date_from': '2022-07-24', 'vc_date_to': '', 'vc_with': '0', 'vc_comment': '', 'vc_first': '1', 'vc_today': '1', 'vc_before_visit': '0'}]


def update_status(url, id, status):
    s.post(url=f'{url}/{id}', params={"vc_status": f"{status}"})
