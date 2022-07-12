from datetime import datetime
from time import sleep

from selenium.webdriver.common.by import By

from features.pages.base_page import BasePage

# Inherits from BasePage
from utils import captcha, telegram


class ItalyConsulatePage(BasePage):

    LINK_LANGUAGE_EN = By.XPATH, '//a[contains(@href, "/Language/ChangeLanguage?lang=2")]'
    FIELD_EMAIL = By.ID, 'login-email'
    FIELD_PASSWORD = By.ID, 'login-password'
    BUTTON_LOGIN = By.XPATH, '//button[@data-callback="onSubmit"]'
    TAB_MY_APPOINTMENTS = By.XPATH, '//a[contains(@href, "/Reservation")]'
    TAB_BOOK = By.XPATH, '//a[contains(@href, "/Services")]'
    FIELD_SEARCH = By.ID, 'myInputTextField'
    BUTTON_BOOK_SCHENGEN = By.XPATH, '//a[contains(@href, "/Services/Booking/1090")]'
    BUTTON_BOOK_STYDY = By.XPATH, '//a[contains(@href, "/Services/Booking/163")]'
    DIALOG_NO_DATES = By.XPATH, '//div[@role="dialog"]'
    BUTTON_CLOSE_DIALOG = By.XPATH, '//div[@role="dialog"]//button'
    CHECKBOX_PRIVACY = By.NAME, 'PrivacyCheck'
    BUTTON_FORWARD = By.ID, 'btnAvanti'
     # = By., ''
     # = By., ''
     # = By., ''
     # = By., ''
     # = By., ''
     # = By., ''

    def _verify_page(self):
        self.on_this_page(self.LINK_LANGUAGE_EN)

    def click_on(self, element_name, section=None):
        if element_name == 'privacy checkbox':
            while True:
                if self.is_element_displayed('no dates dialog'):
                    # telegram.send_message(message=f'Нет итальянских дат')
                    self.click_on(self.BUTTON_CLOSE_DIALOG)
                    self.click_on(self.FIELD_SEARCH)
                    if self.is_element_displayed(self.FIELD_SEARCH):
                        self.type_in(self.FIELD_SEARCH, 'Schengen')
                        self.click_on(self.BUTTON_BOOK_SCHENGEN)
                    elif self.is_element_displayed(self.FIELD_EMAIL):
                        self.context.execute_steps(u'''
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
                    else:
                        self.context.scenario.mark_skipped()
                else:
                    break
        elif element_name == 'search field':
            if self.is_element_displayed(self.BUTTON_BOOK_STYDY, timeout=200):
                pass
        super(ItalyConsulatePage, self).click_on(element_name, section)
