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


@step("gather germany dates")
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


@step("monitor germany")
def monitor(context):
    while True:
        try:
            context.execute_steps(u'''
                When open url: "https://service2.diplo.de/rktermin/extern/appointment_showMonth.do?locationCode=mins&realmId=231&categoryId=373"
                Then page german visa is opened
                When enter "captcha" in captcha field
                When click on continue button
                When clear log
                When gather dates
                When click on next month button
                When gather dates
                When click on next month button
                When send dates
            ''')
        except Exception as e:
            context.bot.send_photo(chat_id=context.config['telegram']['telegram_to'],
                                   photo=context.driver.get_screenshot_as_png(),
                                   caption=f'Unknown exception: {str(e)}')
            with open('page_source.html', 'w') as f:
                f.write(context.driver.page_source)
            telegram.send_document(
                document_name='page_source.html',
                image=context.driver.get_screenshot_as_png(),
                caption=f'Unknown exception: {str(e)}')
        finally:
            context.driver.delete_all_cookies()
