# from utils.gsheets import GoogleSheets
#
# data_worksheet = GoogleSheets().authorize('Data')
# print(data_worksheet.get('A1'))
from datetime import timezone, time, datetime, timedelta
from time import sleep

from utils.dt import is_time_between



def is_current_time_different(current_time, mins) -> bool:
    return current_time < datetime.utcnow() - timedelta(seconds=mins)


print(datetime.utcnow())
