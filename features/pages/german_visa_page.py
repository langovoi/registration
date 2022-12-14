import re
from multiprocessing import Pool

from selenium.webdriver.common.by import By

from features.pages.base_page import BasePage

# Inherits from BasePage
from utils import captcha


class GermanVisaPage(BasePage):
    categories = {'373': {"type": "Inviting", "name": "Шенген"},
                  '2845': {"type": "Tourism", "name": "Туризм"},
                  '375': {"type": "National", "name": "Национальная"}}

    IMAGE_CAPTCHA = By.XPATH, '//captcha/div'
    FIELD_CAPTCHA = By.NAME, 'captchaText'
    BUTTON_CONTINUE = By.XPATH, '//input[@id="appointment_captcha_day_appointment_showDay" or @id="appointment_captcha_month_appointment_showMonth" or @id="appointment_newAppointmentForm_appointment_addAppointment"]'
    BUTTON_NEXT_MONTH = By.XPATH, '//img[@src="images/go-next.gif"]/..'
    MESSAGE_ERROR = By.ID, 'message'
    MESSAGE_UNFORTUNATELY = By.XPATH, '//div[@id="content"]/div/h2[1]'
    SECTION_DATES = By.XPATH, '//div[@id="content"]//div[@style="width: 100%;"]'

    # register page
    FIELD_SURNAME = By.NAME, 'lastname'
    FIELD_NAME = By.NAME, 'firstname'
    FIELD_EMAIL = By.NAME, 'email'
    FIELD_CONFIRM_EMAIL = By.NAME, 'emailrepeat'
    DROPDOWN_APPLICANTS_NUMBER = By.XPATH, '(//label[contains(text(), "Anzahl der Antragsteller")]/../..//select | //label[contains(text(), "Количество заявителей")]/../..//select)'
    FIELD_PASSPORT_NUMBER = By.XPATH, '(//label[contains(text(), "Passnummer des Visumbewerbers")]/../..//input | //label[contains(text(), "Номер паспорта")]/../..//input)'
    FIELD_OTHER_PARTICIPANTS = By.XPATH, '(//label[contains(text(), "Ggfs. Name, Vorname, Passnummer weiterer Antragsteller:")]/../..//input | //label[contains(text(), "других заявителей")]/../..//input)'
    FIELD_HOST_NAME = By.XPATH, '(//label[contains(text(), "Name des Einladers")]/../..//input | //label[contains(text(), "приглашающего")]/../..//input)'
    DROPDOWN_AIM = By.XPATH, '(//label[contains(text(), "Grund der Reise")]/../..//select | //label[contains(text(), "Цель")]/../..//select)'
    FIELD_AIM = By.XPATH, '//input[@id="appointment_newAppointmentForm_fields_3__content"]'
    FIELD_PHONE_NUMBER = By.XPATH, '(//label[contains(text(), "Telefonnummer des Visumbewerbers")]/../..//input | //label[contains(text(), "Номер телефона")]/../..//input)'
    FIELD_BIRTH_DAY = By.XPATH, '(//label[contains(text(), "Geburtsdatum")]/../..//input | //label[contains(text(), "Дата рождения")]/../..//input)'
    CHECKBOX_CONFIRM = By.XPATH, '//div/input[@type="checkbox"]'
    BUTTON_SAVE = By.XPATH, '//input[@id="appointment_newAppointmentForm_appointment_addAppointment"]'

    # confirmation page
    LINK_CONFIRM_APPOINTMENT = By.XPATH, '//a[contains(@href, "confirmation_appointment.do")]'
    LINK_CANCEL_APPOINTMENT = By.XPATH, '//a[contains(@href, "cancellation_form.do")]'

    def _verify_page(self):
        self.on_this_page(self.FIELD_CAPTCHA)

    def click_on(self, element_name, section=None):
        super(GermanVisaPage, self).click_on(element_name)
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
                        slots = re.findall("\d+", time.text)[0]
                        if int(slots) >= int(self.context.values['number_of_appointments']):
                            time.find_element_by_xpath('//a').click()
                            break

    def enter_captcha(self):
        if self.is_element_displayed('captcha field', timeout=1):
            for _ in range(10):
                self.get_captcha_image("visa_captcha.png")
                super(GermanVisaPage, self).type_in('captcha field', captcha.get_code("visa_captcha.png").lower())
                super(GermanVisaPage, self).click_on('continue button')
                if not self.is_element_displayed(self.MESSAGE_ERROR, timeout=2):
                    break
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
