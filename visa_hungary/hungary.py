import logging
from datetime import datetime, timezone

import undetected_chromedriver as uc
from time import sleep

import os, sys

from selenium.webdriver import DesiredCapabilities, ActionChains

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from utils import telegram, gsheets
from driver.base_page import BasePage
from selenium import webdriver
from selenium.webdriver.common.by import By


class Hungary(BasePage):
    pass

gs = gsheets.GoogleSheets('hungary')

user = int(sys.argv[2])

id_email, email, password, name, date, phone, passport, used, count_person, date_min, date_max = gs.ws.get_all_values()[user]

def register(key):
    try:
        logging.warning(sys.argv[1])
        logging.warning(user)
        start_time_dict = {'1': '21/59/57.0', '2': '21/59/57.5', '3': '21/59/58.0', '4': '21/59/58.5', '5': '21/59/59.0', '6': '21/59/59.5', '7': '22/00/00.0', '8': '22/00/00.5', '9': '21/59/58.5', '10': '21/59/58.9'}
        time = datetime.strptime(f'{datetime.utcnow().date().strftime("%m/%d/%Y")}/{start_time_dict[key]}', '%m/%d/%Y/%H/%M/%S.%f')
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument('--blink-settings=imagesEnabled=false')
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "none"
        driver = webdriver.Chrome(desired_capabilities=caps, options=options)
        driver.delete_all_cookies()
        driver.get('https://konzinfoidopont.mfa.gov.hu/')
        f = Hungary(driver)
        logging.warning('Создали драйвер. Открыли сайт')
        for i in range(3):
            if not f.is_element_displayed('//button[@id="langSelector"]') or not f.is_element_displayed(
                    '//input[@id="birthDate"]'):
                driver.refresh()
                sleep(3)
            else:
                break
        else:
            telegram.send_doc(caption=f'{name} Не прогрузился язык или дата', html=driver.page_source)
            raise RuntimeError(f'Не прогрузился язык или дата {name}')
        f.click_on_while('//button[@id="langSelector"]')
        while True:
            if f.is_element_displayed('//div[@class="dropdown-menu language show"]//img[@alt="Русский"]'):
                f.click_on('//img[@alt="Русский"]')
                logging.warning('Выбрали язык')
                break
            else:
                logging.warning('Глюк селектора выбора языка.Еще заход')
                f.click_on('//button[@id="langSelector"]')

        while True:
            try:
                f.click_on('//label[text()="Место предоставления услуги"]/..//button[text()="Выбор места"]')
                break
            except Exception as e:
                sleep(0.1)
        while True:
            try:
                f.type_in('//input[@placeholder="Поиск"]', 'Беларусь')
                break
            except Exception as e:
                sleep(0.1)
        f.click_on_while('//label[text()="Беларусь - Минск"]')
        logging.warning('Выбрали Беларусь')
        f.click_on_while('//label[text()="Тип дела"]/..//button[text()="Добавление типа услуги"]')

        f.type_in('//h5[text()="Типы дел"]/../..//input[@placeholder="Поиск"]', 'типа С')
        f.click_on_while('//label[contains(text(),"Заявление о выдаче визы (краткосрочная шенгенская виза типа С)")]')
        # f.type_in('//h5[text()="Типы дел"]/../..//input[@placeholder="Поиск"]', 'D')
        # f.click_on_while('//label[contains(text(),"разрешение на проживание - D")]')

        f.click_on_while('Сохранить')
        logging.warning('Выбрали Тип услуги')
        f.type_in('//input[@id="label4"]', name)
        logging.warning(f'Ввод имя: {name}')
        f.type_in('//input[@id="birthDate"]', date.replace('.', '/'))
        logging.warning('Ввод рождение')
        f.type_in_clear('//input[@id="label6"]', count_person)
        logging.warning('Ввод количество заявителей')
        f.type_in('//input[@id="label9"]', phone)
        logging.warning('Ввод телефон')
        f.type_in('//input[@id="label10"]', email)
        logging.warning('Ввод почта')
        f.type_in('//input[@id="label1000"]', passport)
        logging.warning('Ввод паспорт')
        sleep(2)
        while True:
            try:
                f.click_on('//input[@id="slabel13"]')
                break
            except Exception as e:
                sleep(0.1)
        actions = ActionChains(driver)
        element = driver.find_element(By.XPATH, '//button[@class="btn btn-primary w-100"]')
        try:
            actions.move_to_element(element).perform()
        except Exception:
            sleep(2)
            actions.move_to_element(element).perform()
        while True:
            try:
                f.click_on('//input[@id="label13"]')
                break
            except Exception as e:
                sleep(0.1)
        logging.warning('Поставили галки')
        logging.warning('Жду время')
        while True:
            dt = datetime.strptime(datetime.now(tz=timezone.utc).strftime('%m/%d/%Y/%H/%M/%S.%f'), '%m/%d/%Y/%H/%M/%S.%f')
            if time <= dt:
                logging.warning(f'dt:{dt}')
                break
        while True:
            try:
                f.click_on('//button[text()="Перейти  к выбору времени"]')
                break
            except Exception as e:
                sleep(0.1)
        click_span = int(key)
        dt = datetime.strptime(datetime.now(tz=timezone.utc).strftime('%m/%d/%Y/%H/%M/%S.%f'), '%m/%d/%Y/%H/%M/%S.%f')
        logging.warning(f'Нажали выбор даты:{dt}')
        if f.is_element_displayed('//span[text()="Свободно"]'):
            count_span = len(driver.find_elements(By.XPATH,'//span[text()="Свободно"]'))
            source = driver.page_source
            if count_span < int(key) :
                click_span = count_span
                logging.warning(f'меняем дату на слот {count_span} ')
            for i in range(25):
                try:
                    f.click_on(f'(//span[text()="Свободно"])[{click_span}]')
                    break
                except Exception as e:
                    logging.warning('click')
                    sleep(0.1)
            else:
                raise RuntimeError("Не нажимается дата")
            logging.warning(f"Выбрали дату в {datetime.strptime(datetime.now(tz=timezone.utc).strftime('%m/%d/%Y/%H/%M/%S.%f'), '%m/%d/%Y/%H/%M/%S.%f')}")
            while True:
                try:
                    f.click_on('//button[@id="nextTo3"]')
                    break
                except Exception as e:
                    sleep(0.1)
            logging.warning(f"Нажали далее в {datetime.strptime(datetime.now(tz=timezone.utc).strftime('%m/%d/%Y/%H/%M/%S.%f'), '%m/%d/%Y/%H/%M/%S.%f')}")
            # telegram.send_message(f'{thread}: {datetime.now()}')
            telegram.send_doc(f'Венгрия. Даты {name}, {start_time_dict[key]}', source)
            sleep(90)
            telegram.send_doc(f'Венгрия. Перед завершением бронирования {name}', driver.page_source)
            f.click_on_while('Завершение бронирования')
            dt = datetime.strptime(datetime.now(tz=timezone.utc).strftime('%m/%d/%Y/%H/%M/%S.%f'), '%m/%d/%Y/%H/%M/%S.%f')
            logging.warning(f'ЗАПИСАН:({name}): {dt}')
            sleep(10)
            telegram.send_doc(f'🟩Венгрия: в {dt} успешно зарегистрирован({name} {start_time_dict[key]})', driver.page_source)
        else:
            if f.is_element_displayed(
                    '//div[text()="Обращаем Ваше внимание, что у Вас уже есть действующая запись для решения данного вопроса."]'):
                telegram.send_doc(f'⭕Венгрия {name} уже зареген другим сеансом {start_time_dict[key]}', driver.page_source)
                logging.warning('Уже зареген')
                driver.close()
            else:
                telegram.send_doc(f'⭕Венгрия для:{name} нет дат {start_time_dict[key]}', driver.page_source)
                logging.warning(f'Нет дат: {start_time_dict[key]}')
                if f.is_element_displayed('//button[text()="Хорошо"]'):
                    for i in range(20):
                        try:
                            f.click_on('//button[text()="Хорошо"]')
                            break
                        except Exception as e:
                            logging.warning('click Хорошо для {name} нет дат {start_time_dict[key]} ')
                            sleep(0.1)
                    else:
                        raise RuntimeError("Не нажимается хорошо")
    except Exception as e:
        try:
            telegram.send_image(driver, f'Венгрия неизвестная ошибка {str(e)} {start_time_dict[key]}')
        except Exception:
            telegram.send_message(f'Венгрия неизвестная ошибка. {str(e)}')


if __name__ == "__main__":
    register(sys.argv[1])
