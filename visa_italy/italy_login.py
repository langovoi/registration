import requests
from selenium import webdriver

driver = webdriver.Chrome()

driver.get('https://prenotami.esteri.it/Home')

cookies = driver.get_cookies()

s = requests.Session()

response = s.get('https://prenotami.esteri.it/Home')

print(response)

