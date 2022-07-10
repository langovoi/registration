from selenium.webdriver.common.by import By

from features.pages.base_page import BasePage

# Inherits from BasePage
from utils import captcha


class GermanVisaPage(BasePage):
    IMAGE_CAPTCHA = By.XPATH, '//form[@id="appointment_captcha_month"]//captcha/div'
    FIELD_CAPTCHA = By.NAME, 'captchaText'
    BUTTON_CONTINUE = By.ID, 'appointment_captcha_month_appointment_showMonth'
    BUTTON_NEXT_MONTH = By.XPATH, '//img[@src="images/go-next.gif"]/..'
    MESSAGE_ERROR = By.ID, 'message'
    MESSAGE_UNFORTUNATELY = By.XPATH, '//div[@id="content"]/div/h2[1]'
    SECTION_DATES = By.XPATH, '//div[@id="content"]//div[@style="width: 100%;"]'

    def _verify_page(self):
        self.on_this_page(self.FIELD_CAPTCHA)

    def click_on(self, element_name, section=None):
        super(GermanVisaPage, self).click_on(element_name, section)
        if element_name == 'continue button':
            for _ in range(10):
                if not self.is_element_displayed(self.MESSAGE_ERROR, timeout=5):
                    break
                else:
                    self.get_captcha_image("visa_captcha.png")
                    super(GermanVisaPage, self).type_in('captcha field', captcha.get_code("visa_captcha.png").lower())
                    super(GermanVisaPage, self).click_on(element_name, section)
            else:
                raise RuntimeError("Unable to enter captcha")

    def type_in(self, field_name, text):
        if text == 'captcha':
            self.get_captcha_image("visa_captcha.png")
            super(GermanVisaPage, self).type_in('captcha field', captcha.get_code("visa_captcha.png").lower())
        else:
            super(GermanVisaPage, self).type_in(field_name, text)
        print()

    def get_captcha_image(self, file_name):
        self.get_element('captcha image').screenshot(file_name)
