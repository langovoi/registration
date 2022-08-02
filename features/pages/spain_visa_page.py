import re

from selenium.webdriver.common.by import By

from features.pages.base_page import BasePage

# Inherits from BasePage
from utils import captcha


class SpainVisaPage(BasePage):

    def _verify_page(self):
        pass
        # self.on_this_page(self.FIELD_CAPTCHA)


