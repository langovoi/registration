import configparser
from datetime import datetime

from sys import platform

from utils import dt, telegram
from utils.gsheets import GoogleSheets

import allure
from selenium import webdriver
from behave.contrib.scenario_autoretry import patch_scenario_with_autoretry
import telebot


# context attributes on https://behave.readthedocs.io/en/latest/context_attributes.html#user-attributes


def before_all(context):
    args = ['headless', 'window-size=1920,1080'] if platform != 'darwin' else []
    caps = {
        # -- Chrome Selenoid options
        'browserName': 'chrome',
        'version': '87.0',
        'selenoid:options':
            {
                'enableVNC': True,
                'enableVideo': False
            },
        # -- Chrome browser mobile emulation and headless options
        'goog:chromeOptions': {
            # 'mobileEmulation': {'deviceName': 'iPhone X'},
            # 'window-size': ['1920,1080'],
            'args': args
        }
    }
    '''
        -- Android browser Selenoid options
        "browserName": "android",
        "version": "9.0",
        'selenoid:options': {
            'enableVNC': True,
            'enableVideo': True
        }
    
        -- Android native app Selenoid options
        'deviceName': 'android',  # not browserName
        'version': '9.0',
        'app': 'path/to/instagram.apk',
        'appActivity': 'com.instagram.mainactivity.LauncherActivity',
        'appPackage': 'com.instagram.android',
        'selenoid:options': {
            'enableVNC': True,
            'enableVideo': False
        }
    '''

    # -- Local driver
    context.driver = webdriver.Chrome(desired_capabilities=caps)

    # -- Remote driver
    # context.driver = webdriver.Remote(command_executor='http://67.207.88.128:4444/wd/hub', desired_capabilities=caps)

    context.driver.implicitly_wait(10)
    context.driver.maximize_window()
    # read config
    parser = configparser.ConfigParser()
    parser.read('behave.ini')
    context.config = parser
    context.values = {'start_time': datetime.utcnow()}

    # google sheets
    # context.data_worksheet = GoogleSheets().authorize('Data')


def before_feature(context, feature):
    # retry failures
    print('Feature started:', feature.name)
    for scenario in feature.scenarios:
        for tag in scenario.effective_tags:
            if 'retry' in tag:
                patch_scenario_with_autoretry(scenario, max_attempts=int(tag[5:]))


def before_scenario(context, scenario):
    # context.driver.delete_all_cookies()
    print(f'Scenario started: {scenario.name}')
    context.driver.delete_all_cookies()


def after_step(context, step) -> None:
    print('step started:', step.name)
    try:
        allure.attach(context.driver.get_screenshot_as_png(),
                      name=f'screenshot',
                      attachment_type=allure.attachment_type.PNG)
    except Exception:
        pass
    if step.status == 'failed' and str(step.exception) != 'autoretry':
        try:
            # send page_source.html to telegram
            with open("page_source.html", "w") as f:
                f.write(context.driver.page_source)
            telegram.send_document(
                document_name='page_source.html',
                image=context.driver.get_screenshot_as_png(),
                caption=str(step.exception))
        except Exception as e:
            print(f'after step failed!!: {str(e)}')


def after_all(context):
    context.driver.quit()
