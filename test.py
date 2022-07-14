from multiprocessing import Pool
from selenium import webdriver



driver = webdriver.Chrome()
driver.get('file:///Users/alexandrkardash/Downloads/page_source%20(4).html')
element = driver.find_element_by_xpath('//div/a[contains(@href, "openingPeriodId=")]')
print(element.get_attribute('href'))
