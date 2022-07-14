from selenium.webdriver.common.by import By

from features.pages.base_page import BasePage

# Inherits from BasePage
from utils import captcha


class ItalyEmbassyPage(BasePage):
    IMAGE_CAPTCHA = By.XPATH, '//captcha/div'
    FIELD_CAPTCHA = By.NAME, 'captchaText'
    BUTTON_CONTINUE = By.ID, 'appointment_captcha_month_appointment_showMonth'
    BUTTON_NEXT_MONTH = By.XPATH, '//img[@src="images/go-next.gif"]/..'
    MESSAGE_ERROR = By.ID, 'message'
    MESSAGE_UNFORTUNATELY = By.XPATH, '//div[@id="content"]/div/h2[1]'
    SECTION_DATES = By.XPATH, '//div[@id="content"]//div[@style="width: 100%;"]'

    # register page
    FIELD_SURNAME = By.NAME, 'lastname'
    FIELD_NAME = By.NAME, 'firstname'
    FIELD_EMAIL = By.NAME, 'email'
    FIELD_CONFIRM_EMAIL = By.NAME, 'emailrepeat'
    DROPDOWN_APPLICANTS_NUMBER = By.XPATH, '//select[@id="appointment_newAppointmentForm_fields_0__content"]'
    FIELD_PASSPORT_NUMBER = By.XPATH, '//input[@id="appointment_newAppointmentForm_fields_1__content"]'
    FIELD_OTHER_PARTICIPANTS = By.XPATH, '//input[@id="appointment_newAppointmentForm_fields_2__content"]'
    FIELD_AIM = By.XPATH, '//input[@id="appointment_newAppointmentForm_fields_3__content"]'
    FIELD_PHONE_NUMBER = By.XPATH, '//input[@id="appointment_newAppointmentForm_fields_4__content"]'
    CHECKBOX_CONFIRM = By.XPATH, '//input[@id="appointment_newAppointmentForm_fields_5__content"]'
    BUTTON_SAVE = By.XPATH, '//input[@id="appointment_newAppointmentForm_appointment_addAppointment"]'

    # confirmation page
    LINK_CONFIRM_APPOINTMENT = By.XPATH, '//a[contains(@href, "confirmation_appointment.do")]'
    LINK_CANCEL_APPOINTMENT = By.XPATH, '//a[contains(@href, "cancellation_form.do")]'

    def _verify_page(self):
        self.on_this_page(self.FIELD_CAPTCHA)
