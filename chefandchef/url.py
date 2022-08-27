# import os
# import re
# import numpy as np
import logging
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.firefox.options import Options
# from fake_useragent import UserAgent
# from random import randint


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

list_urls = [
    {'cat1': 'الشواء', 'cat2': '', 'cat3': '', 'url': 'https://chefandchef.com.sa/collections/bbq'},
    {'cat1': 'السكاكين', 'cat2': '', 'cat3': '', 'url': 'https://chefandchef.com.sa/collections/cutlery'},
    {'cat1': 'أدوات الشيف', 'cat2': '', 'cat3': '', 'url': 'https://chefandchef.com.sa/collections/chefs-tool'},
    {'cat1': 'مستلزمات الخبز', 'cat2': '', 'cat3': '', 'url': 'https://chefandchef.com.sa/collections/bake-ware'},
    {'cat1': 'أواني الطبخ', 'cat2': '', 'cat3': '', 'url': 'https://chefandchef.com.sa/collections/cook-ware'},
]

def get_data(url):
    logging.info('Url %s', url)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    cookies = {'session': '134-8225175-0355220'}
    r = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(r.content, "html.parser")
    time.sleep(1)
    products = soup.find_all('div', {'class': 'mt-product'})
    liens = [toto.find('a')['href']  for toto in products]
    logging.info('Len products %s', len(liens))
    return soup, liens

def getnextpage(soup):
    page =  soup.find('svg', {'class': 'icon-arrow-right'}).parent.parent.find('a')
    url2 = 'https://chefandchef.com.sa' + str(page['href'])
    return url2

def scrap_url_product(url1):
    cat1 = url1['cat1']
    cat2 = url1['cat2']
    cat3 = url1['cat3']
    url = url1['url']
    data = []
    while True:
        soup, urls_list = get_data(url)

        for toto in urls_list:
            # print(f'URL:', toto)
            data.append({
            'url':toto,
            'cat1': cat1,
            'cat2': cat2,
            'cat3': cat3,
            })
        try:
            url = getnextpage(soup)
#             print('Url dans le while', url)
        except:
            break
    # print(data)
    logging.info( f'Scrape categories done .')
    return data

df = pd.read_excel('homelight_url_model.xlsx')
for i, url in enumerate(list_urls):
    logging.info('--Count: %s', i)
    data = scrap_url_product(url)
    df1 = pd.DataFrame(data)
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('chefandchef_url_update.xlsx')
logging.info('Scraping URL Done.')
