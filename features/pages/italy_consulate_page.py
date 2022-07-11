from selenium.webdriver.common.by import By

from features.pages.base_page import BasePage

# Inherits from BasePage
from utils import captcha


class ItalyConsulatePage(BasePage):

    LINK_LANGUAGE_EN = By.XPATH, '//a[contains(@href, "/Language/ChangeLanguage?lang=2")]'
    FIELD_EMAIL = By.ID, 'login-email'
    FIELD_PASSWORD = By.ID, 'login-password'
    BUTTON_FORWARD = By.XPATH, '//button[@data-callback="onSubmit"]'
    TAB_MY_APPOINTMENTS = By.XPATH, '//a[contains(@href, "/Reservation")]'
    TAB_BOOK = By.XPATH, '//a[contains(@href, "/Services")]'
     # = By., ''
     # = By., ''
     # = By., ''
     # = By., ''
     # = By., ''
     # = By., ''
     # = By., ''
     # = By., ''

    def _verify_page(self):
        self.on_this_page(self.LINK_LANGUAGE_EN)


