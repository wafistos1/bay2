
import time
import os
import requests
import re, logging
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
from fake_useragent import UserAgent
from random import randint
import pandas as pd
import numpy as np

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


def get_data(url):
    logging.info('URL: %s', url)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    cookies = {'session': '134-8225175-0355220'}
    r = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(r.content, "html.parser")
    time.sleep(1)
    products = soup.find_all('div', {'class': 'product'})
    
    liens = [toto.find('a')['href']  for toto in products]
    logging.info('Len products', len(liens))
    return liens

list_urls = [
    {'cat1': 'طاولات', 'cat2': 'طاولات كاملة', 'cat3': '', 'url': 'https://silla.sa/%D8%B7%D8%A7%D9%88%D9%84%D8%A7%D8%AA-%D9%83%D8%A7%D9%85%D9%84%D8%A9/c1020947514'},
    {'cat1': 'طاولات', 'cat2': 'طاولات قهوة', 'cat3': '', 'url': 'https://silla.sa/%D8%B7%D8%A7%D9%88%D9%84%D8%A7%D8%AA-%D9%82%D9%87%D9%88%D8%A9/c1952017985https://silla.sa/%D8%A3%D8%B3%D8%B7%D8%AD-%D8%B7%D8%A7%D9%88%D9%84%D8%A7%D8%AA/c990912935'},
    {'cat1': 'طاولات', 'cat2': 'أسطح طاولات', 'cat3': '', 'url': 'https://silla.sa/%D8%A3%D8%B3%D8%B7%D8%AD-%D8%B7%D8%A7%D9%88%D9%84%D8%A7%D8%AA/c990912935'},
    {'cat1': 'طاولات', 'cat2': 'أسطح خشب', 'cat3': '', 'url': 'https://silla.sa/%D8%A3%D8%B3%D8%B7%D8%AD-%D8%AE%D8%B4%D8%A8/c599398067'},
    {'cat1': 'طاولات', 'cat2': 'أسطح HPL ', 'cat3': '', 'url': 'https://silla.sa/%D8%A3%D8%B3%D8%B7%D8%AD-hpl/c2106013116'},
    {'cat1': 'طاولات', 'cat2': 'أسطح رخام', 'cat3': '', 'url': 'https://silla.sa/%D8%A3%D8%B3%D8%B7%D8%AD-%D8%B1%D8%AE%D8%A7%D9%85/c1332499645'},
    {'cat1': 'طاولات', 'cat2': 'قواعد طاولات ', 'cat3': '', 'url': 'https://silla.sa/%D9%82%D9%88%D8%A7%D8%B9%D8%AF-%D8%B7%D8%A7%D9%88%D9%84%D8%A7%D8%AA/c424244158'},
    {'cat1': 'الأرائك', 'cat2': 'مفرده', 'cat3': '', 'url': 'https://silla.sa/%D9%85%D9%81%D8%B1%D8%AF%D9%87/c1557750000'},
    {'cat1': 'الأرائك', 'cat2': 'ثنائيه', 'cat3': '', 'url': 'https://silla.sa/%D8%AB%D9%86%D8%A7%D8%A6%D9%8A%D9%87/c782733297'},
    {'cat1': 'أثاث خارجي', 'cat2': 'جلسات خارجية ', 'cat3': '', 'url': 'https://silla.sa/%D8%AC%D9%84%D8%B3%D8%A7%D8%AA-%D8%AE%D8%A7%D8%B1%D8%AC%D9%8A%D8%A9/c1209109291'},
    {'cat1': 'أثاث خارجي', 'cat2': 'كراسي خارجية ', 'cat3': '', 'url': 'https://silla.sa/%D9%83%D8%B1%D8%A7%D8%B3%D9%8A-%D8%AE%D8%A7%D8%B1%D8%AC%D9%8A%D8%A9/c449228598'},
    {'cat1': 'أثاث خارجي', 'cat2': 'كراسي إسترخاء ', 'cat3': '', 'url': 'https://silla.sa/%D9%83%D8%B1%D8%A7%D8%B3%D9%8A-%D8%A5%D8%B3%D8%AA%D8%B1%D8%AE%D8%A7%D8%A1/c686982413'},
    {'cat1': 'أثاث خارجي', 'cat2': 'مظلات خارجية', 'cat3': '', 'url': 'https://silla.sa/%D9%85%D8%B8%D9%84%D8%A7%D8%AA-%D8%AE%D8%A7%D8%B1%D8%AC%D9%8A%D8%A9/c165964092'},
    {'cat1': 'اكسسوارات', 'cat2': 'اكسسوار', 'cat3': '', 'url': 'https://silla.sa/%D8%A7%D9%83%D8%B3%D8%B3%D9%88%D8%A7%D8%B1/c1981493233'},
    {'cat1': 'اكسسوارات', 'cat2': 'بوف', 'cat3': '', 'url': 'https://silla.sa/%D8%A8%D9%88%D9%81/c357898472'},
]


def scrap_url_product(url1):
    
    cat1 = url1['cat1']
    cat2 = url1['cat2']
    cat3 = url1['cat3']
    url = url1['url']
    data = []
    count = 1
    while True:
        urls_list = get_data(url)
        for toto in urls_list:
            data.append({
            'url':toto,
            'cat1': cat1,
            'cat2': cat2,
            'cat3': cat3,
            })
        if len(urls_list) != 0:
            count += 1
            url = url.split('?')[0] + f'?page={count}'
        else:
            logging.info( 'Scrape Categorie Done --> Next .')
            break
    return data

df = pd.read_excel('silla_url_models.xlsx')
for i, url in enumerate(list_urls):
    logging.info('Count: %s', i)
    data = scrap_url_product(url)
    df1 = pd.DataFrame(data)
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('silla_url_update.xlsx')
logging.info('Scraping URL Done.')

