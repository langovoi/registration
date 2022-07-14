from multiprocessing import Pool
from selenium import webdriver


def merge_names(name):
    driver = webdriver.Chrome()
    driver.get(name)


if __name__ == '__main__':
    names = ['https://google.com', 'https://ya.ru', 'https://dev.by']
    with Pool(processes=3) as p:
        p.map(merge_names, names)
