import time
import logging
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
from fake_useragent import UserAgent
# from random import randint
# import numpy as np
# import requests


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

options = Options()
ua = UserAgent()
userAgent = ua.random
logging.info(userAgent)
options.add_argument(f'user-agent={userAgent}')
#opti#     driver = webdriver.Firefox()ons.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)

def get_data(url):
    '''
    '''
    logging.info('URL: %s', (url,))
    driver.get(url)
    while True:
        time.sleep(4)
        try:
            driver.find_element_by_xpath('//a[@class="btn btn--padded btn--primary btn--oval pagination__next mt-10"]').click()
        except:
            logging.info('Next page..')
            break

    body=WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.TAG_NAME,'body')))
    r = body.get_attribute('innerHTML')
    soup = BeautifulSoup(r, "html.parser")
    time.sleep(1)
    products = soup.find_all('div', {'class': 'product-block'})
    len(products)
    liens = [toto.find('a')['href']  for toto in products]
    print('Len products', len(liens))
    return   liens

list_urls = [
    {'cat1': 'انارة خارجية', 'cat2': '', 'cat3': '', 'url': 'https://homelight.sa/category/QdzZmr'},
    {'cat1': 'انارة داخلية', 'cat2': 'ثريات', 'cat3': '', 'url': 'https://homelight.sa/category/NKYDRg'},
    {'cat1': 'انارة داخلية', 'cat2': 'علاقي', 'cat3': '', 'url': 'https://homelight.sa/category/NKYDRg'},
    {'cat1': 'انارة داخلية', 'cat2': 'اضاءة جدارية داخلية', 'cat3': '', 'url': 'https://homelight.sa/category/VqbPXO'},
    {'cat1': 'انارة داخلية', 'cat2': 'كرات ليد LED', 'cat3': '', 'url': 'https://homelight.sa/category/wWjEzz'},
    {'cat1': 'ابجورات', 'cat2': '', 'cat3': '', 'url': 'https://homelight.sa/category/YglDBo'},
    {'cat1': 'اضاءة خطية', 'cat2': '', 'cat3': '', 'url': 'https://homelight.sa/category/zveGVE'},
    {'cat1': 'انارة مرايا و لوحات', 'cat2': '', 'cat3': '', 'url': 'https://homelight.sa/category/PdQOZG'},
    {'cat1': 'لمبات', 'cat2': 'لمبات فيلمنت Filament', 'cat3': '', 'url': 'https://homelight.sa/category/mQWeyl'},
    {'cat1': 'لمبات', 'cat2': 'لمبات ليد LED', 'cat3': '', 'url': 'https://homelight.sa/category/NKQYWV'},
    {'cat1': 'اضاءة الزينة و الجلسات الخارجية', 'cat2': '', 'cat3': '', 'url': 'https://homelight.sa/category/qQRwWY'},
    {'cat1': 'اضاءة جدارية بالبطارية', 'cat2': '', 'cat3': '', 'url': 'https://homelight.sa/category/RAVGbY'},
    {'cat1': 'اطقم', 'cat2': '', 'cat3': '', 'url': 'https://homelight.sa/category/NKGVZm'},

]

def scrap_url_product(url1):
    '''
    '''
    cat1 = url1['cat1']
    cat2 = url1['cat2']
    cat3 = url1['cat3']
    url = url1['url']
    data = []
    urls_list = get_data(url)
    for toto in urls_list:
        data.append({
        'url':toto,
        'cat1': cat1,
        'cat2': cat2,
        'cat3': cat3,
        })
    logging.info( f'Scrape done .')
    return data

df = pd.read_excel('homelight_url_model.xlsx')
for i, url in enumerate(list_urls):
    logging.info('--Count: %s', i)
    data = scrap_url_product(url)
    df1 = pd.DataFrame(data)
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('homelight_url_update.xlsx')