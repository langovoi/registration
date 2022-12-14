import sys
from datetime import datetime
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver

from utils import gsheets, users, gmm


gs = gsheets.GoogleSheets('germany')
all_emails = gs.ws.get_all_values()

us = users.get_users('Inviting')

us = [u for u in us if '|' in u['vc_comment']]


for user in us:
    email = user["vc_comment"].split("|")[1]
    users.update_fields(url=f'{sys.argv[2]}', id=user['id'], body={'vc_comment': f'{user["vc_comment"].replace(f"|{email}|", "")}'})
# row, email, password, used, wait, date, family = email
# i = int(row) + 1
# # Select a range
# cell_list = gs.ws.range(f'E{i}:G{i}')
# cell_list[0].value = int(wait) - 1
# cell_list[1].value = datetime.now().strftime("%d-%m-%Y")
# cell_list[2].value = "family"*100000
#
# # Update in batch
# gs.ws.update_cells(cell_list)
