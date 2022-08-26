from time import sleep

from selenium.webdriver import Keys
import undetected_chromedriver as uc

emails = ["negoda.semen@mail.ru", "timofeev.ustin@internet.ru", "moiseev.bronislav@internet.ru", "kabanov.stanislav00@mail.ru", "kozlov.svyatoslav@internet.ru", "shufrich.marat@mail.ru", "fadeev.savva@internet.ru", "zimin.marat@internet.ru", "navalnyi.ilya@mail.ru", "orekhov.bronislav@internet.ru", "komarov.ostin@mail.ru", "gorbachev.orlando@mail.ru", "sidorov.dmitrii@internet.ru", "gaichuk.rafail@mail.ru", "dzuba.lukillyan@mail.ru", "andreev.feliks@internet.ru", "dzuba.boris@bk.ru", "savelev.lenar@internet.ru", "vygovskii.maksim@bk.ru", "uvarov.khariton@internet.ru", "tyagai.leonid@mail.ru", "khokhlov.lev@internet.ru", "efremov.ostin@mail.ru", "popov.kuzma00@bk.ru", "odintsov.leopold@internet.ru", "nekrasov.feliks@internet.ru", "gusev.kim@internet.ru", "fedotov.matvei@inbox.ru", "frolov.eduard00@mail.ru", "fedunkiv.filipp@mail.ru", "samsonov.tit@inbox.ru", "tsvetkov.miroslav@internet.ru", "vasilev.dominik@internet.ru", "predybailo.ulii@mail.ru", "samoilov.bronislav@bk.ru", "bogdanov.filipp@internet.ru", "vygovskii.gennadii@mail.ru", "mikhailov.prokhor@internet.ru", "mishin.david@internet.ru", "lytkin.spartak@mail.ru", "filatov.mark00@mail.ru", "gordeev.petr00@mail.ru", "solovev.eduard00@mail.ru", "kondratev.lubomir@list.ru", "kondratiev.valery@bk.ru", "bogdanov.nikolai@internet.ru", "polyakov.valeryan@internet.ru", "frolov.valeryan@internet.ru", "pilipeiko.vlad@mail.ru", "trublaevskii.dinar@mail.ru", "sazonov.tit@internet.ru", "kotov.maksim00@bk.ru", "chumak.elisei@mail.ru", "karpov.fedor00@bk.ru", "dyachkov.nikita00@mail.ru", "teterin.efim@internet.ru", "romanov.ulyan@internet.ru", "gusev.trofim00@mail.ru", "nesterov.platon@internet.ru"]

driver = uc.Chrome()
driver.implicitly_wait(1000)

for email in emails:
    driver.delete_all_cookies()
    driver.get('https://e.mail.ru/inbox/')
    driver.find_element_by_xpath('//input[@name="username"]').send_keys(email)
    sleep(1)
    driver.find_element_by_xpath('//button[@data-test-id = "next-button"]').click()
    sleep(1)
    driver.find_element_by_xpath('//input[@name="password"]').send_keys('Ab_1505_1369')
    sleep(1)
    driver.find_element_by_xpath('//button[@data-test-id = "submit-button"]').click()
    sleep(4)
    driver.find_element_by_xpath(f'//div[@aria-label="{email}"]')

    driver.get('https://id.mail.ru/contacts?open-add-phone=1')
    sleep(1)
    driver.find_element_by_xpath('//input[@data-test-id="phone-input"]').click()
    driver.find_element_by_xpath('//input[@data-test-id="phone-input"]').send_keys('9523794606')
    sleep(1)
    driver.find_element_by_xpath('//button[@data-test-id="recovery-addPhone-submit"]').click()
    driver.find_element_by_xpath('//button[@data-test-id="recovery-success-close"]').click()

    driver.get('https://account.mail.ru/user/2-step-auth/passwords')
    driver.find_element_by_xpath('//a[@data-name="add-button"]').click()
    driver.find_element_by_xpath('//input[@name="name"]').send_keys('python')
    driver.find_element_by_xpath('//button[@data-name="submit"]').click()
    driver.find_element_by_xpath('//input[@name="password"]').send_keys('Ab_1505_1369')
    sleep(1)
    print(email, driver.find_element_by_class_name('view_dialog__password').text)

