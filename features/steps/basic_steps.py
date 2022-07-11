from datetime import datetime, timezone, timedelta, time
from time import sleep

from behave import step, use_step_matcher
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from telethon import TelegramClient, events
from urllib3 import HTTPSConnectionPool

import pages
from utils import telegram
from utils.dt import is_time_between

use_step_matcher('re')


@step('click on (?P<element_name>[^"]*?)(?: in "(?P<section>[^"]*?)")?')
def click_on(context, element_name, section=None):
    sleep(0.5)
    if section:
        section_xpath = context.page.get_element_by_name(section)[1]
        element = context.page.get_element_by_name(element_name)
        if element[0] == 'xpath':
            try:
                context.driver.find_element_by_xpath(f'{section_xpath}{element[1]}').click()
            except NoSuchElementException:
                raise RuntimeError(f'Не могу кликнуть {element_name} в {section}')
        else:
            raise RuntimeError(f'Используй XPATH для локатора {element_name}')
    else:
        context.page.click_on(element_name)


@step('enter "(?P<text>[^"]*)" in (?P<field_name>[^"]*)(?: in "(?P<section>[^"]*?)")?')
def enter_in(context, text, field_name, section=None):
    sleep(0.5)
    if 'generated' in text:
        time = datetime.now(timezone.utc) + timedelta(hours=3)
        context.values[text] = text = text.replace("generated", f'{time.strftime("%d.%m.%Y %H:%M:%S")}')
    if section:
        section_xpath = context.page.get_element_by_name(section)[1]
        element = context.page.get_element_by_name(field_name)
        if element[0] == 'xpath':
            try:
                element = context.driver.find_element_by_xpath(f'{section_xpath}{element[1]}')
                element.clear()
                element.send_keys(text)
            except NoSuchElementException:
                raise RuntimeError(f'Не могу найти {field_name} в {section}. With xpath {section_xpath}{element[1]}')
        else:
            raise RuntimeError(f'Используй XPATH для локатора {field_name}')
    else:
        context.page.type_in(field_name, text)


@step('select "(?P<option>.*)" in (?P<dropdown>.*)')
def select_from_dropdown(context, option, dropdown):
    context.page.select_by_text(dropdown, option)


@step('text "(?P<text>.*)" in (?P<element>.*) is displayed')
def text_in_element_is_state(context, text, element):
    element_text = context.page.get_text(element)
    if text not in element_text:
        raise RuntimeError(f'Текст для элемента {element}: "{element_text}". Ожидаемый: {text}')


@step('text "(?P<text>.*)" is displayed')
def text_is_state(context, text):
    element = (By.TAG_NAME, 'body')
    WebDriverWait(context.driver, 10).until(
        ec.text_to_be_present_in_element(element, text), f'Unable to find text: {text}')


@step('page (?P<page_name>.*) is opened')
def init_screen(context, page_name):
    """Instantiating verifies that we're on that page"""
    page_class = pages.factory(page_name)
    context.page = page_class(context)


@step('open url: "(?P<url>.*)"')
def open_url(context, url):
    context.driver.get(url) if url.startswith('http') else context.driver.get(f'https://{url}')


@step('open (?P<page_name>.*) page')
def open_page(context, page_name):
    context.page_name = page_name
    open_url(context, page_name)
    page_class = pages.factory(page_name)
    context.page = page_class(context.driver)


@step('remember (?P<key>.*) as "(?P<value>.*)"')
def remember(context, key, value):
    context.values[value] = context.page.get_text(key)


def replace_with_context_values(context, text):
    for value in context.values:
        if value in text:
            text = text.replace(value, context.values[value])
    return text


@step("wait (?P<seconds>.*) sec")
def step_impl(context, seconds):
    sleep(int(seconds))


@step("open last tab")
def step_impl(context):
    context.driver.switch_to_window(context.driver.window_handles[-1])


@step("run monitoring")
def run_monitoring(context):
    # telegram
    client = TelegramClient(
        'any_name',
        context.config['telegram']['api_id'],
        context.config['telegram']['api_hash'])

    @client.on(events.NewMessage(chats=1339855416))
    async def my_event_handler(event):
        save_data(context, event.text)
        print(event.text)

    client.start()
    client.run_until_disconnected()


def save_data(context, text):
    context.time = (datetime.now(timezone.utc) + timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')
    context.data_worksheet.insert_rows(values=[[context.time, text]], row=2)


@step("clear log")
def clear_log(context):
    context.log = ''


@step("gather dates")
def gather_dates(context):
    # check context
    for date_slot in context.page.get_elements('dates section'):
        if date_slot.text:
            context.log = f'{context.log}\n{date_slot.text}'
    # check Unfortunately message
    expected_message = 'Unfortunately, there are no appointments available at this time'
    if not context.page.is_element_displayed('unfortunately message') or expected_message not in context.page.get_text(
            'unfortunately message'):
        with open("page_source.html", "w") as f:
            f.write(context.driver.page_source)
        try:
            telegram.send_document(
                chat_id=context.config['telegram']['telegram_to'],
                document_name='page_source.html',
                image=context.driver.get_screenshot_as_png(),
                caption="Unfortunately message is not displayed or changed")
        except Exception:
            raise RuntimeError('gather dates step')


@step("send dates")
def send_dates(context):
    message = context.log if context.log else f'{datetime.utcnow()}: No dates'
    telegram.send_message(message=message)
    # from 02:15 to 23:45 check every 5 minutes
    if not is_time_between(time(20, 55), time(23, 15)):
        sleep(300)  # default: 300
    else:
        sleep(60)  # default: 60
    raise RuntimeError('autoretry')


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
                chat_id=context.config['telegram']['telegram_to'],
                document_name='page_source.html',
                image=context.driver.get_screenshot_as_png(),
                caption=f'Unknown exception: {str(e)}')
        finally:
            context.driver.delete_all_cookies()


@step("get user info")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: When get user info')
