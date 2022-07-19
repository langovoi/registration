import re

from selenium.webdriver.common.by import By

from features.pages.base_page import BasePage

# Inherits from BasePage
from utils import captcha


class FrenchVisaPage(BasePage):

    BUTTON_BOOK_APPOINTMENTS = By.XPATH, '//div[contains(text(), "Booking an appointment")]'

    def _verify_page(self):
        self.driver.switch_to.frame('BODY_WIN')
        self.on_this_page(self.BUTTON_BOOK_APPOINTMENTS)
