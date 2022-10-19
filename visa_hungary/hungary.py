import logging
from datetime import datetime, timezone

import undetected_chromedriver as uc
from time import sleep

import os, sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from utils import telegram
from driver.base_page import BasePage
from selenium import webdriver


class Hungary(BasePage):
    pass


users = [
    {'name': 'DOVATOD SERGEY', 'date': '01/01/1986', 'phone': '+375298222998', 'email': 'igor_fomin00@bk.ru',
     'passport': 'AB9756323'},
    {'name': 'PAEEROV VALERY', 'date': '01/10/1999', 'phone': '+375293239918', 'email': 'nikonov.gordei@mail.ru',
     'passport': 'MC1280954', },
    {'name': 'SIDOROV IRYNA', 'date': '10/10/2000', 'phone': '+375296669948', 'email': 'likhachev.yaromir@mail.ru',
     'passport': 'MC3480933', },
    {'name': 'USACHEV VALERY', 'date': '01/10/1999', 'phone': '+375293239957', 'email': 'nikonov.gordei@mail.ru',
     'passport': 'AB5480944', },
    {'name': 'DAVIDOV ANASTASYA', 'date': '01/10/1999', 'phone': '+375256239328', 'email': 'arkhipov.roman00@mail.ru',
     'passport': 'PD3454476', },
    {'name': 'IVANOVA ANASTASYA', 'date': '01/11/1989', 'phone': '+375446444978',
     'email': 'ivashchenko.georgii@mail.ru',
     'passport': 'PD3450976', },
    {'name': 'DOVATOVA ANASTASYA', 'date': '05/12/1999', 'phone': '+375446239118', 'email': 'pogomii.timofei@mail.ru',
     'passport': 'AB3220976', },
    {'name': 'SHPAK ELENA', 'date': '01/10/1999', 'phone': '+375259239985', 'email': 'shufrich.yakov@mail.ru',
     'passport': 'PD3120976', },
    {'name': 'PRIVET ELENA', 'date': '22/10/1999', 'phone': '+375297636758', 'email': 'isaev.andrei00@mail.ru',
     'passport': 'PD3340976', },
    {'name': 'KOKTYSH ANASTASYA', 'date': '11/10/1999', 'phone': '+375297638912', 'email': 'geletei.renata@mail.ru',
     'passport': 'PD3432976', }
]

name, date, phone, email, passport = users[int(sys.argv[1])].values()


def register(thread):
    time = datetime.strptime(f'{datetime.utcnow().date().strftime("%m/%d/%Y")}/13/30','%m/%d/%Y/%H/%M')
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument('--blink-settings=imagesEnabled=false')
    driver = uc.Chrome(options=options)
    driver.delete_all_cookies()

    driver.get('https://konzinfoidopont.mfa.gov.hu/')
    f = Hungary(driver)
    logging.warning('Создали драйвер. Открыли сайт')
    for i in range(3):
        if not f.is_element_displayed('//button[@id="langSelector"]') or not f.is_element_displayed('//input[@id="birthDate"]'):
            driver.refresh()
            sleep(3)
        else:
            break
    else:
        telegram.send_doc(caption=f'{name} Не прогрузился язык или дата', html=driver.page_source)
        raise  RuntimeError(f'Не прогрузился язык или дата {name}')

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
    f.click_on_while('Сохранить')
    logging.warning('Выбрали Тип услуги')
    f.type_in('//input[@id="label4"]', name)
    logging.warning(f'Ввод имя: {name}')
    f.type_in('//input[@id="birthDate"]', date)
    logging.warning('Ввод рождение')
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
    try:
        f.click_on('//button[text()="Перейти  к выбору времени"]')
    except Exception:
        pass
    while True:
        try:
            f.click_on('//input[@id="label13"]')
            break
        except Exception as e:
            sleep(0.1)
    logging.warning('Поставили галки')
    logging.warning('Жду время')
    while True:
        dt = datetime.strptime(datetime.now(tz=timezone.utc).strftime('%m/%d/%Y/%H/%M'), '%m/%d/%Y/%H/%M')
        if time <= dt:
            logging.warning(f'dt:{dt}')
            break
    while True:
        try:
            f.click_on('//button[text()="Перейти  к выбору времени"]')
            break
        except Exception as e:
            sleep(0.1)
    dt = datetime.strptime(datetime.now(tz=timezone.utc).strftime('%m/%d/%Y/%H/%M'), '%m/%d/%Y/%H/%M')
    logging.warning(f'Нажали выбор даты:{dt}')
    if f.is_element_displayed('//span[text()="Свободно"]'):
        while True:
            try:
                f.click_on('(//span[text()="Свободно"])[last()]')
                break
            except Exception as e:
                logging.warning('click')
                sleep(0.1)
        # тут похоже начинает работать бан, кнопка не всегда работает, нужно переключать ip
        # может попробовать рандомом кликать по элементам, перемотка вроде помогает немного
        # element3 = driver.find_element(By.ID, 'nextTo3')
        # driver.execute_script("arguments[0].scrollIntoView();", element3)
        logging.warning('Выбрали дату')
        while True:
            try:
                f.click_on('//button[@id="nextTo3"]')
                break
            except Exception as e:
                sleep(0.1)
        logging.warning('Нажали далее')
        # telegram.send_message(f'{thread}: {datetime.now()}')
        telegram.send_doc(f'Венгрия.Перед завершением бронирования {name}',driver.page_source)
        sleep(60)
        f.click_on_while('Завершение бронирования')
        dt = datetime.strptime(datetime.now(tz=timezone.utc).strftime('%m/%d/%Y/%H/%M'), '%m/%d/%Y/%H/%M')
        logging.warning(f'ЗАПИСАН:({name}): {dt}')
        sleep(10)
        telegram.send_doc(f'Венгрия: в {dt} успешно зарегистрирован({name})', driver.page_source)


    else:
        if f.is_element_displayed('//div[text()="Обращаем Ваше внимание, что у Вас уже есть действующая запись для решения данного вопроса."]'):
            telegram.send_doc(f'Венгрия {name} уже зареген другим сеансом', driver.page_source)
            logging.warning('Уже зареген')
            driver.close()
        else:
            telegram.send_doc('Венгрия для:{name} нет дат', driver.page_source)
            if f.is_element_displayed('//button[text()="Хорошо"]'):
                while True:
                    try:
                        f.click_on('//button[text()="Хорошо"]')
                        break
                    except Exception as e:
                        sleep(0.1)


if __name__ == "__main__":
    register('1')
