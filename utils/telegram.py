# Remember to use your own values from my.telegram.org!
from configparser import ConfigParser
from telethon import TelegramClient, events

parser = ConfigParser()
parser.read('behave.ini')
config = parser

client = TelegramClient(
    'any_name',
    config['telegram']['api_id'],
    config['telegram']['api_hash'])


@client.on(events.NewMessage(chats=1339855416))
async def my_event_handler(event):
    print(event.text)


client.start()
client.run_until_disconnected()
