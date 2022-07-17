import requests
from datetime import datetime
from bs4 import BeautifulSoup

from selenium import webdriver

from utils import captcha

driver = webdriver.Chrome()
s = requests.Session()


def get_catpcha_code(url):
    driver.get(url)
    session_id = driver.session_id
    # login page
    cookies = {'JSESSIONID': f'JSESSIONID={session_id}','KEKS': 'TERMIN325',}
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8', 'Cache-Control': 'max-age=0', 'Connection': 'keep-alive', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'none', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36', 'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"macOS"',}
    params = {'locationCode': 'mins', 'realmId': '231', 'categoryId': '373',}
    r = s.get('https://service2.diplo.de/rktermin/extern/appointment_showMonth.do', params=params, cookies=cookies, headers=headers)

    soup = BeautifulSoup(r.text,"lxml")
    image = soup.select("captcha > div")
    image= image[0]['style'].split("url('")[1].split("')")[0]
    return captcha.get_code(image), session_id


def get_appointments(url, code, session_id):
    cookies = {'JSESSIONID': f'{session_id}','KEKS': 'TERMIN327',}
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'max-age=0', 'Connection': 'keep-alive', 'Origin': 'https://service2.diplo.de', 'Referer': f'https://service2.diplo.de/rktermin/extern/appointment_showMonth.do;jsessionid={session_id}', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36', 'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"macOS"',}
    data = {'captchaText': f'{code}', 'rebooking': 'false', 'token': '', 'lastname': '', 'firstname': '', 'email': '', 'locationCode': 'mins', 'realmId': '231', 'categoryId': '373', 'openingPeriodId': '', 'date': '','dateStr': '', 'action:appointment_showMonth': 'Continue',}

    return s.post(url, cookies=cookies, headers=headers, data=data).text


code, session_id = get_catpcha_code('https://service2.diplo.de/rktermin/extern/appointment_showMonth.do?locationCode=mins&realmId=231&categoryId=375')
for i in range(10):
    html = get_appointments('https://service2.diplo.de/rktermin/extern/appointment_showMonth.do', code, session_id)
    if 'Unfortunately' in html:
        print('Нет дат')
        break
    elif 'Termine sind verfügbar' in html or 'Запись на прием возможна' in html:
        soup = BeautifulSoup(html,"lxml")
        element = soup.select("div[style='margin-left: 20%;']")
    else:
        print('Не разгадал код с 10 попыток')
else:
    raise RuntimeError('Не залогинился')

