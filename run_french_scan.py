from time import sleep

from germany import Germany
from utils import telegram

from selenium import webdriver

driver = webdriver.Chrome()
driver.get('https://pastel.diplomatie.gouv.fr/rdvinternet/html-4.02.00/frameset/frameset.html?lcid=1&sgid=196&suid=1')
from selenium.webdriver.common.action_chains import ActionChains
elem = driver.find_element_by_xpath("(//frame)[2]")
ac = ActionChains(driver)
ac.move_to_element(elem).move_by_offset(10, 10).click().perform()

driver.find_element_by_id()