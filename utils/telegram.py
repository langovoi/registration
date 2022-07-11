# Remember to use your own values from my.telegram.org!
from configparser import ConfigParser
from telethon import TelegramClient, events


def send_document(bot, chat_id, document_name, image, caption):
    bot.send_photo(chat_id=chat_id, photo=image)
    bot.send_document(chat_id=chat_id, document=open(document_name, "rb"), caption=caption)
