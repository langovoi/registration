from time import sleep

from germany import Germany
from utils import telegram

while True:
    try:
        # Schengen
        Germany(['TERMIN325', 'TERMIN327'], '373').get_dates()
        sleep(10)
        # Tourism
        Germany(['TERMIN327', 'TERMIN340'], '2845').get_dates()
        # National
        # Germany(['TERMIN325', 'TERMIN340'], '375').get_dates()
        sleep(300)
    except Exception as e:
        telegram.send_message(f'⭕ Germany job failed: {str(e)}')

