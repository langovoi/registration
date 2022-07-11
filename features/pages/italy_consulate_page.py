from selenium.webdriver.common.by import By

from features.pages.base_page import BasePage

# Inherits from BasePage
from utils import captcha


class ItalyConsulatePage(BasePage):


    def _verify_page(self):
        self.on_this_page(self.FIELD_CAPTCHA)


