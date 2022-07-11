# Remember to use your own values from my.telegram.org!


def send_document(bot, chat_id, document_name, image_name, caption):
    bot.send_document(chat_id=chat_id, document=open(document_name, 'rb'), filename=image_name, caption=caption)
