from time import sleep

import requests

from utils import telegram


def open_page_get_session_id():
    s = requests.Session()
    headers = {'authority': 'blsspain-russia.com', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'accept-language': 'en-US,en;q=0.9', 'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"macOS"', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'none', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1', 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36', }
    r = s.get('https://blsspain-russia.com/moscow/apply_for.php', headers=headers)
    if 'записи на подачу документов полностью забронированы' not in r.text:
        telegram.send_doc('🟢 Испания: Загрузилась не страница с ошибкой', r.text)
    return


open_page_get_session_id()

class Spain():
    def __init__(self):
        pass


