import gspread
from google.oauth2.service_account import Credentials

from utils import cfg


class GoogleSheets:
    gs_key_file = cfg.create_json('email_key')
    data_columns = {'id': 'A',
                    'email': 'B',
                    'password': 'C',
                    'used_germany': 'D'}

    def __init__(self, name):
        self.ws = self.authorize(name)

    def authorize(self, work_sheet):
        scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file(self.gs_key_file, scopes=scope)
        gs = gspread.authorize(creds).open_by_key('1aYR6tN9BygDJLOVmKkXKAxDkJtxuH1nh6J6pjmHPBNo')
        return gs.worksheet(work_sheet)

    def find_item_by_id(self, visa_item_id):
        cell = self.ws.row_values(visa_item_id + 1)
        return cell

    def update_visa_item_by_id(self, id, column, value):
        self.ws.update_acell("{}{}".format(self.data_columns[column], int(id) + 1), value)
