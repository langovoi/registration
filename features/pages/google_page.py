from selenium.webdriver.common.by import By

from features.pages.base_page import BasePage


# Inherits from BasePage
class GooglePage(BasePage):
    FIELD_SEARCH = By.NAME, 'q'

    def _verify_page(self):
        self.on_this_page(self.FIELD_SEARCH)
