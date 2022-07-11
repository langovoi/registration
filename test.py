# from utils.gsheets import GoogleSheets
#
# data_worksheet = GoogleSheets().authorize('Data')
# print(data_worksheet.get('A1'))
import configparser
from datetime import timezone, time, datetime, timedelta
from time import sleep

import telebot
from selenium import webdriver

from utils import telegram
from utils.dt import is_time_between

parser = configparser.ConfigParser()
parser.read('behave.ini')
config = parser

file = open('page_source.html', 'rb')

driver = webdriver.Chrome()

driver.get('https://google.com')

bot = telebot.TeleBot(config['telegram']['telegram_token'])
print(driver.get_screenshot_as_file('screenshot.png'))

with open("page_source.html", "w") as f:
    f.write(driver.page_source)

telegram.send_document(
    bot=bot,
    chat_id=config['telegram']['telegram_to'],
    document_name="page_source.html",
    image=driver.get_screenshot_as_png(),
    caption='some action')
