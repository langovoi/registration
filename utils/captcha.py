from twocaptcha import TwoCaptcha

from utils import telegram

API_KEY = "8a00f7c0d525e77ea27b8430ce1810f6"


def get_code(file_name: str) -> str:
    try:
        return str(TwoCaptcha(API_KEY).normal(file_name)['code'])
    except Exception:
        telegram.send_message('Не смог решить капчу')