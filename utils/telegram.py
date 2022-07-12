# Remember to use your own values from my.telegram.org!
from configparser import ConfigParser
from time import sleep

import telebot

parser = ConfigParser()
parser.read('behave.ini')
config = parser


def send_document(context, caption, document_name='page_source.html', ):
    image = context.driver.get_screenshot_as_png()
    bot = telebot.TeleBot(config['telegram']['telegram_token'])
    chat_id = config['telegram']['telegram_to']
    bot.send_photo(chat_id=chat_id, photo=image)
    bot.send_document(chat_id=chat_id, document=open(document_name, "rb"), caption=caption)
    bot.stop_bot()


def send_message(message):
    for _ in range(3):
        try:
            bot = telebot.TeleBot(config['telegram']['telegram_token'])
            bot.send_message(chat_id=config['telegram']['telegram_to'], text=message)
            bot.stop_bot()
            break
        except Exception:
            sleep(30)