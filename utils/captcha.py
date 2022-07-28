import logging
from time import sleep

from bs4 import BeautifulSoup
from twocaptcha import TwoCaptcha

from utils import telegram

API_KEY = "8a00f7c0d525e77ea27b8430ce1810f6"


def get_code(html: str, page='not set') -> str:
    logging.info(f'captcha page {page}')
    soup = BeautifulSoup(html, "lxml")
    image = soup.select("captcha > div")
    image = image[0]['style'].split("url('")[1].split("')")[0]
    try:
        return str(TwoCaptcha(API_KEY).normal(image)['code'])
    except Exception as e:
        if 'ERROR_ZERO_BALANCE' in str(e):
            telegram.send_message(f'Ошибка TwoCaptcha: Timeout 5 минут: {str(e)}')
            sleep(300)
        else:
            telegram.send_message(f'Ошибка TwoCaptcha: {str(e)}')



def is_captcha_displayed(html: str):
    soup = BeautifulSoup(html, "lxml")
    image = soup.select("captcha > div")
    return True if image else False
