import sys
from datetime import datetime
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver

from utils import gsheets, users, gmm

# username = 'belov.ludvig@mail.ru'
#


gs = gsheets.GoogleSheets('germany')
# emails = gs.ws.get_all_values()
# email = [email for email in emails if email[1] == username][0]
# gs.ws.update_acell(f'D{int(email[0])+1}', int(email[3])+1)

all_emails = gs.ws.get_all_values()
email = [email for email in all_emails if email[1] == 'nikonov.gordei@mail.ru'][0]
row, email, password, used, wait, date, family = email
i = int(row) + 1
# Select a range
cell_list = gs.ws.range(f'E{i}:G{i}')
cell_list[0].value = int(wait) - 1
cell_list[1].value = datetime.now().strftime("%d-%m-%Y")
cell_list[2].value = "family"*100000

# Update in batch
gs.ws.update_cells(cell_list)
