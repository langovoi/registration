# Remember to use your own values from my.telegram.org!
from configparser import ConfigParser

import telebot

parser = ConfigParser()
parser.read('behave.ini')
config = parser


def send_document(chat_id, document_name, image, caption):
    bot = telebot.TeleBot(config['telegram']['telegram_token'])
    bot.send_photo(chat_id=chat_id, photo=image)
    bot.send_document(chat_id=chat_id, document=open(document_name, "rb"), caption=caption)


def send_message(message):
    bot = telebot.TeleBot(config['telegram']['telegram_token'])
    bot.send_message(chat_id=config['telegram']['telegram_to'], text=message)
