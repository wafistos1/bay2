from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
import time
import os
from fake_useragent import UserAgent
from random import randint
import pandas as pd
import numpy as np
import requests
import pandas as pd
import re, logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

urls = [
    {'cat1': 'لوحات جدارية', 'cat2': '', 'cat3': '', 'url':'https://astore-alanar.com/categories/387013/'},
    {'cat1': 'اطقم كنب', 'cat2': '', 'cat3': '', 'url':'https://astore-alanar.com/categories/350703/'},
    {'cat1': 'طاولات طعام', 'cat2': '', 'cat3': '', 'url':'https://astore-alanar.com/categories/350681/'},
    {'cat1': 'جلسات خشب الزان', 'cat2': '', 'cat3': '', 'url':'https://astore-alanar.com/categories/331554/'},
    {'cat1': 'جلسات خشب', 'cat2': '', 'cat3': '', 'url':'https://astore-alanar.com/categories/301743/'},
    {'cat1': 'جلسات حديد وخشب', 'cat2': '', 'cat3': '', 'url':'https://astore-alanar.com/categories/301745/'},
    {'cat1': 'اغطية حماية', 'cat2': '', 'cat3': '', 'url':'https://astore-alanar.com/categories/315518/'},
    {'cat1': 'كراسي وطاولات', 'cat2': '', 'cat3': '', 'url':'https://astore-alanar.com/categories/303576/'},
    # {'cat1': '', 'cat2': '', 'cat3': '', 'url':''},
]

def get_data(url):

    logging.info(f'Url:{url}')
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    cookies = {'session': '134-8225175-0355220'}
    r = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(r.content, "html.parser")
    time.sleep(1)
    products = soup.find_all('div', {'class': 'product-item'})
    liens = ['https://astore-alanar.com' + toto.find('a')['href']  for toto in products]
    logging.info(f'Len products: {len(liens)}')
    list_liens = []
    
    for t in liens:
        list_liens.append(t)
#     print('list_cat1', list_cat1)
    data = {
        'url':list_liens,
        }
    # df = pd.DataFrame(data)
#     print(df)
#         print('Href: ', t['href'])
#     print("Soup get_data")
    return soup, list_liens


def getnextpage(soup):
    #Check if next url exist else send None objects
    # Return URL or None
    page = soup.find('a', text=re.compile('التالي'))

    try:
        url2 = str(page['href'])
        return url2
    except:
        print('No Next')
        pass
    return url2 

list_urls = []


def scrap_url_product(url1):
    
    cat1 = url1['cat1']
    cat2 = url1['cat2']
    cat3 = url1['cat3']
    url = url1['url']
    data = []
    
    while True:
        soup, urls_list = get_data(url)
        
        for toto in urls_list:
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
    logging.info( f'Scrape done .')
    return data
df = pd.read_excel('astore_url_model.xlsx')

for i, url in enumerate(urls):
    logging.info(f'--Count: {i}')
    data = scrap_url_product(url)
    df1 = pd.DataFrame(data)
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('astore_url_update.xlsx')