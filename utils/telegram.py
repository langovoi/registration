# Remember to use your own values from my.telegram.org!
from configparser import ConfigParser
from time import sleep

import telebot
from urllib3 import HTTPSConnectionPool

parser = ConfigParser()
parser.read('behave.ini')
config = parser


def send_document(document_name, image, caption):
    bot = telebot.TeleBot(config['telegram']['telegram_token'])
    chat_id = config['telegram']['telegram_to']
    bot.send_photo(chat_id=chat_id, photo=image)
    bot.send_document(chat_id=chat_id, document=open(document_name, "rb"), caption=caption)


def send_message(message):
    for _ in range(3):
        try:
            bot = telebot.TeleBot(config['telegram']['telegram_token'])
            bot.send_message(chat_id=config['telegram']['telegram_to'], text=message)
            break
        except Exception:
            sleep(30)