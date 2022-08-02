import logging
from datetime import datetime
from time import sleep

from bs4 import BeautifulSoup
from twocaptcha import TwoCaptcha

from utils import telegram

API_KEY = "8a00f7c0d525e77ea27b8430ce1810f6"

def get_code(html: str, page='not set') -> str:
    logging.warning(f'{datetime.now().strftime("%H:%M:%S")}: captcha page {page}')
    logging.warning(f'1')
    soup = BeautifulSoup(html, "lxml")
    logging.warning(f'2')
    image = soup.select("captcha > div")
    logging.warning(f'3')
    image = image[0]['style'].split("url('")[1].split("')")[0]
    logging.warning(f'4')
    try:
        logging.warning(f'5')
        code = str(TwoCaptcha(API_KEY).normal(image)['code'])
        logging.warning(f'6')
        # ref.push().set({'code': code, 'image': image_base64})
        logging.warning(f'7')
    except Exception as e:
        logging.warning(f'8')
        logging.warning(f'captcha error')
        if 'ERROR_ZERO_BALANCE' in str(e):
            telegram.send_message(f'Ошибка TwoCaptcha: Timeout 5 минут: {str(e)}')
            sleep(300)
        else:
            telegram.send_message(f'Ошибка TwoCaptcha: {str(e)}')
        code = None
    return code


def is_captcha_displayed(html: str):
    soup = BeautifulSoup(html, "lxml")
    image = soup.select("captcha > div")
    try:
        image = image[0]['style'].split("url('")[1].split("')")[0]
        result = True
    except IndexError:
        telegram.send_doc("Не могу найти картинку капчи, хотя captcha > div отображается", str(soup))
        result = False
    return result
