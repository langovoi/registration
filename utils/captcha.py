import logging
from datetime import datetime
from time import sleep

import firebase_admin
from bs4 import BeautifulSoup
from firebase_admin import credentials, db
from twocaptcha import TwoCaptcha

from utils import telegram

API_KEY = "8a00f7c0d525e77ea27b8430ce1810f6"
default_app = firebase_admin.initialize_app(credentials.Certificate('captcha.json'), {'databaseURL': 'https://captcha-d3bd4-default-rtdb.europe-west1.firebasedatabase.app/captcha'})


def get_code(html: str, page='not set') -> str:
    logging.warning(f'{datetime.now().strftime("%H:%M:%S")}: captcha page {page}')
    logging.warning(f'1')
    soup = BeautifulSoup(html, "lxml")
    logging.warning(f'2')
    image = soup.select("captcha > div")
    logging.warning(f'3')
    image = image[0]['style'].split("url('")[1].split("')")[0]
    logging.warning(f'4')
    image_base64 = image.split(',')[1]
    logging.warning(f'5')
    datetime_start = datetime.now()
    logging.warning(f'6')
    ref = db.reference("/captcha")
    logging.warning(f'7')
    captcha_json = ref.get()
    logging.warning(f'8')
    for key, value in captcha_json.items():
        if value['image'] == image_base64:
            code = key
            telegram.send_doc(f'Капча найдена в базе: {image_base64}', str(soup))
            break
    else:
        logging.warning(f'9')
        if (datetime.now() - datetime_start).total_seconds() > 60:
            telegram.send_message('🟡 Поиск капчи в базе занимает больше 60 секунд')
        try:
            logging.warning(f'10')
            code = str(TwoCaptcha(API_KEY).normal(image)['code'])
            logging.warning(f'11')
            ref.push().set({'code': code, 'image': image_base64})
            logging.warning(f'12')
        except Exception as e:
            logging.warning(f'13')
            logging.warning(f'captcha error')
            if 'ERROR_ZERO_BALANCE' in str(e):
                telegram.send_message(f'Ошибка TwoCaptcha: Timeout 5 минут: {str(e)}')
                sleep(300)
            else:
                telegram.send_message(f'Ошибка TwoCaptcha: {str(e)}')
    return code


def is_captcha_displayed(html: str):
    soup = BeautifulSoup(html, "lxml")
    image = soup.select("captcha > div")
    try:
        image = image[0]['style'].split("url('")[1].split("')")[0]
        result = True
    except IndexError:
        image = image[0]['style'].split("url('")[1].split("')")[0]
        telegram.send_doc("Не могу найти картинку капчи", str(soup))
        result = False
    return result
