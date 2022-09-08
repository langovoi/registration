from time import sleep

import undetected_chromedriver as uc
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from utils import gsheets
from utils.sim import Sim


def register_vk(user):
    driver = uc.Chrome()
    driver.delete_all_cookies()
    driver.implicitly_wait(30)
    driver.get('https://vk.com')
    driver.find_element(By.XPATH, '//button[contains(@class,"VkIdForm__signUpButton")]').click()
    for _ in range(6):
        phone_field = driver.find_element(By.XPATH, '//input[@name="phone"]')
        sim = Sim('russia', 'vkontakte')
        sim_id, sim_phone = sim.sim_id, sim.sim_phone.replace('+', '')
        print(sim_phone)
        bl = gsheets.GoogleSheets('vk_blacklist')
        black_list = bl.ws.get_all_values()
        if [sim_phone] in black_list:
            sim.ban_sim()
            driver.quit()
            return None, None
        phone_field.click()
        phone_field.clear()
        phone_field.click()
        phone_field.send_keys(Keys.BACKSPACE)
        phone_field.send_keys(sim_phone)
        driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        # TODO решить капчу
        if "SMS" not in driver.find_element(By.XPATH, '//span[@data-key="time"]/..').text:
            sleep(125)
            driver.find_element(By.XPATH, '//button[@data-test-id="confirmPhoneResendCodeLink"]').click()
        # получить номер из 5sim в simphone
        code = sim.get_new_code()
        if code:
            break
        else:
            sim.ban_sim()
            driver.quit()
            return None, None
    else:
        raise RuntimeError('')
    driver.find_element(By.XPATH, '//input[@id="otp"]').send_keys(code)
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()

    user_id, user_surname, user_name, user_dob, user_phone, user_password = user
    if len(driver.find_elements(By.XPATH, '//input[@name="first_name"]')) == 0:
        bl.ws.update_acell(f'A{len(black_list)+1}', sim_phone)
        return user_id, None
    driver.find_element(By.XPATH, '//input[@name="first_name"]').send_keys(user_name)
    driver.find_element(By.XPATH, '//input[@name="last_name"]').send_keys(user_surname)
    sleep(2)
    driver.find_element(By.XPATH, '//input[@name="birthday"]').send_keys(user_dob)
    sleep(4)
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    try:
        driver.find_element(By.XPATH, '//button[@class="flat_button button_big_text"]').click()  # не нажимает
    except Exception as e:
        bd = driver.find_element(By.XPATH, '//input[@name="birthday"]')
        bd.click()
        bd.send_keys(Keys.BACKSPACE)
        bd.send_keys(user_dob[-1])
        sleep(2)
        driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        driver.find_element(By.XPATH, '//button[@class="flat_button button_big_text"]').click()  # не нажимает
    driver.find_element(By.XPATH, '//a[@class="join_skip_link"]').click()
    driver.find_element(By.XPATH, '//a[@class="join_skip_link"]').click()
    # указать почту
    # driver.find_element(By.XPATH, '//input[@id="pedit_email"]').send_keys('test@test.com')
    # class="flat_button button_big_text button_disabled"
    driver.find_element(By.XPATH, '//a[@class="join_skip_link"]').click()
    sleep(2)
    driver.get('https://id.vk.com/account/#/password-change')
    driver.find_element(By.XPATH, '//span[contains(@class, "vkuiButton__in")]/..').click()
    sleep(2)
    driver.find_element(By.XPATH, '//span[contains(@class, "vkuiButton__in")]/..').click()
    code = sim.get_new_code(code)
    if code == None:
        code = sim.get_new_code()
    driver.find_element(By.XPATH, '//input[@type="text"]').send_keys(code)
    driver.find_element(By.XPATH, '//span[contains(@class, "vkuiButton__in")]/..').click()
    driver.find_element(By.XPATH, '//input[@name="new_password"]').send_keys('Ab123456!')
    driver.find_element(By.XPATH, '//input[@name="new_password_repeat"]').send_keys('Ab123456!')
    sleep(2)
    driver.find_element(By.XPATH, '//span[contains(@class, "vkuiButton__in")]/..').click()
    driver.find_element(By.XPATH, '//h2[text()="Password set"]').is_displayed()
    sleep(2)
    driver.quit()
    return user_id, sim_phone


if __name__ == "__main__":
    for i in range(9):
        gs = gsheets.GoogleSheets('vk')
        users = gs.ws.get_all_values()[1:]
        users = [user for user in users if not user[4]]
        user_id, sim_phone = register_vk(users[0])
        if sim_phone:
            gs.ws.update_acell(f'E{int(user_id) + 1}', f"'{sim_phone}")
