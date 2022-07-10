import gspread
from google.oauth2.service_account import Credentials


class GoogleSheets:
    data_columns = {
        'Time': 'A',
        'Pair': 'B',
        'First': 'C',
        'Second': 'D',
        'Result': 'E'
    }

    def authorize(self, work_sheet):
        scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file("utils/gsheets.json", scopes=scope)
        gs = gspread.authorize(creds).open_by_key("1CVN2VoxOri99Zex2rhZ5ejR3JKd5B1oozS1R7CCvyO4")
        return gs.worksheet(work_sheet)
