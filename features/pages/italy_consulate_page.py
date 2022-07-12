from time import sleep

from selenium.webdriver.common.by import By

from features.pages.base_page import BasePage

# Inherits from BasePage
from utils import telegram


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
                        sleep(30)
                        self.type_in(self.FIELD_SEARCH, 'Schengen')
                        self.click_on(self.BUTTON_BOOK_SCHENGEN)
                elif self.is_element_displayed(self.FIELD_EMAIL):
                    self.context.execute_steps(u'''
                    Then enter "stelmashuk_vova@mail.ru" in email field
                    Then enter "Visa2020!" in password field
                    Then click on login button
                    When click on book tab
                    When click on search field
                    When enter "Schengen" in search field
                    When click on book schengen button
                    When click on privacy checkbox
                    When click on forward button
                    When accept alert
                    When send italy dates
                    ''')
                else:
                    break
        elif element_name == 'search field':
            if not self.is_element_displayed(self.BUTTON_BOOK_STYDY, timeout=200):
                telegram.send_document(self.context, caption='Недоступна кнопка BOOK')
        super(ItalyConsulatePage, self).click_on(element_name, section)
