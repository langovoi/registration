from datetime import datetime, timezone, timedelta, time
from time import sleep

from behave import step, use_step_matcher
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from telethon import TelegramClient, events
from selenium.webdriver.common.alert import Alert

import pages
from utils import telegram
from utils.dt import is_time_between

use_step_matcher('re')


@step("gather italy consulate dates")
def gather_dates(context):
    # check context
    for date_slot in context.page.get_elements('dates section'):
        if date_slot.text:
            context.values['dates'].append(date_slot.text)
    # check Unfortunately message
    expected_message = 'Unfortunately, there are no appointments available at this time'
    if not context.page.is_element_displayed('unfortunately message') or expected_message not in context.page.get_text(
            'unfortunately message'):
        with open("page_source.html", "w") as f:
            f.write(context.driver.page_source)
        try:
            telegram.send_document(
                document_name='page_source.html',
                image=context.driver.get_screenshot_as_png(),
                caption="Unfortunately message is not displayed or changed")
        except Exception:
            raise RuntimeError('gather dates step')


@step("send italy dates")
def send_dates(context):
    with open('page_source.html', 'w') as f:
        f.write(context.driver.page_source)
    telegram.send_document(
        document_name='page_source.html',
        image=context.driver.get_screenshot_as_png(),
        caption=f'🇮🇹 Итальянские даты найдены 🇮🇹')
    raise RuntimeError('autoretry')
