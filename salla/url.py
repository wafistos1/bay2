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

list_urls = [
    {'cat1': 'بطاقات الإهداء', 'cat2': '', 'cat3': '', 'url': 'https://salla.sa/lavishdecor/%D8%A8%D8%B7%D8%A7%D9%82%D8%A7%D8%AA-%D8%A7%D9%84%D8%A5%D9%87%D8%AF%D8%A7%D8%A1/c529304946'},
    {'cat1': 'الحشوات', 'cat2': '', 'cat3': '', 'url': 'https://salla.sa/lavishdecor/%D8%A7%D9%84%D8%AD%D8%B4%D9%88%D8%A7%D8%AA/c787335213'},
    {'cat1': 'أغلفة الخداديات', 'cat2': '', 'cat3': '', 'url': 'https://salla.sa/lavishdecor/%D8%A3%D8%BA%D9%84%D9%81%D8%A9-%D8%A7%D9%84%D8%AE%D8%AF%D8%A7%D8%AF%D9%8A%D8%A7%D8%AA/c968273973'},
    {'cat1': 'تحف', 'cat2': '', 'cat3': '', 'url': 'https://salla.sa/lavishdecor/%D8%AA%D8%AD%D9%81/c203415161'},
]

def get_data(url):
    
    logging.info('Url: %s', url)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    cookies = {'session': '134-8225175-0355220'}
    r = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(r.content, "html.parser")
    time.sleep(1)
    products = soup.find_all('div', {'class': 'product'})
    liens = [toto.find('a')['href']  for toto in products]
    logging.info('Len products: %s', len(liens))
    return liens

def scrap_url_product(url1):
    cat1 = url1['cat1']
    cat2 = url1['cat2']
    cat3 = url1['cat3']
    url = url1['url']
    data = []
    count = 1
    while True:
        url_list = get_data(url)
        for toto in url_list:
            data.append({
            'url':toto,
            'cat1': cat1,
            'cat2': cat2,
            'cat3': cat3,
            })
        if url_list == []:
            break
        count += 1
        url = url.split('?')[0] + f'?page={count}'
    print( f'Scrape Categories Done .')
    return data

df = pd.read_excel('salla_url_model.xlsx')
logging.info('Scraping Salla Started..')
for i, url in enumerate(list_urls):
    logging.info('Count: %s', i)
    data = scrap_url_product(url)
    df1 = pd.DataFrame(data)
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('salla_url_update.xlsx')
logging.info('Scraping Done')