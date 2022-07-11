from selenium.webdriver.common.by import By

from features.pages.base_page import BasePage

# Inherits from BasePage
from utils import captcha


class GermanVisaPage(BasePage):
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
    DROPDOWN_APLICANTS_NUMBER = By.XPATH, '//select[@id="appointment_newAppointmentForm_fields_0__content"]'
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
        if 'appointment button' in element_name:
            # link: href="extern/appointment_showDay.do?locationCode=mins&realmId=231&categoryId=375&dateStr=15.08.2022"
            available_dates = self.driver.find_elements_by_xpath(f'//div/a[contains(@href, "dateStr")]')
            expected_dates_list = self.context.values['expected_dates']
            for date in available_dates:
                str_date = date.get_attribute('href').split('=')[-1]
                # 15.08.2022
                if str_date in expected_dates_list:
                    # 15.08.2022
                    date.click()
                    # link: href="extern/appointment_showForm.do?locationCode=mins&realmId=231&categoryId=375&dateStr=15.08.2022&openingPeriodId=29239"
                    available_times = self.driver.find_elements_by_xpath(
                        '//div/a[contains(@href, "openingPeriodId=")]/..')
                    for time in available_times:
                        slots = self.get_text(time).split()[-1]
                        if int(slots) >= int(self.context.values['number_of_appointments']):
                            time.find_element_by_xpath('//a').click()
                            break

    def type_in(self, field_name, text):
        if text == 'captcha':
            self.get_captcha_image("visa_captcha.png")
            super(GermanVisaPage, self).type_in('captcha field', captcha.get_code("visa_captcha.png").lower())
        else:
            super(GermanVisaPage, self).type_in(field_name, text)
        print()

    def get_captcha_image(self, file_name):
        self.get_element('captcha image').screenshot(file_name)
