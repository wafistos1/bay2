

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
import re


urls = [
    {'cat1': 'لوحات جدارية قماش كانفاس', 'cat2': '', 'cat3': '', 'url': 'https://afkar-modern.com/category/dwvql'},
    {'cat1': 'لوحات جدارية - مجموعات', 'cat2': '', 'cat3': '', 'url': 'https://afkar-modern.com/category/DGXBKd'},
    {'cat1': 'لوحات باسعار مخفضه - جاهزة للشحن', 'cat2': '', 'cat3': '', 'url': 'https://afkar-modern.com/category/NKPYXD'},
    {'cat1': 'تحف واكسسورات ديكور', 'cat2': '', 'cat3': '', 'url': 'https://afkar-modern.com/category/mQeOlZ'},
    {'cat1': 'ساعات حائط اكريليك 3D', 'cat2': '', 'cat3': '', 'url': 'https://afkar-modern.com/category/OqXgog'},
    {'cat1': 'صواني وأطقم تقديم', 'cat2': '', 'cat3': '', 'url': 'https://afkar-modern.com/category/QdbmVr'},
    {'cat1': 'منتجات تنظيم', 'cat2': '', 'cat3': '', 'url': 'https://afkar-modern.com/category/ewrlX'},
]


def get_data(url):
    count = 1
    liens = []
    url = url + '?page=1'
    while True:
        print('Url:', url)
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        cookies = {'session': '134-8225175-0355220'}
        r = requests.get(url, headers=headers, cookies=cookies)
        soup = BeautifulSoup(r.content, "html.parser")
        time.sleep(1)
        products = soup.find_all('div', {'class': 'product'})
        print(len(products))
        if len(products) == 0:
            break
        time.sleep(1)
        for toto in products:
            liens.append(toto.find('a')['href'])
        count += 1
        url = url.split('?')[0] + f'?page={count}'
    print('Len products', len(liens))
    return soup, liens


def getnextpage(soup):
   
    #Check if next url exist else send None objects
    # Return URL or None
    
    page = soup.find('a', {'class': 'next i-next'})
    # print('Page', page)
    
    try:
        # if next url exist 
        url2 = str(page['href'])
        return url2
        # print('', url2)
    except:
        print('No Next')
        pass
    return url2 


def scrap_url_product(url1):
    cat1 = url1['cat1']
    cat2 = url1['cat2']
    cat3 = url1['cat3']
    url = url1['url']
    data = []
    print(cat1, cat2, cat3)
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
        print( f'Scrape done .')
        return data


df = pd.read_excel('afkar_url_model.xlsx')
for i, url in enumerate(urls):
    print('Count: ', i)
    data = scrap_url_product(url)
    df1 = pd.DataFrame(data)
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('afkar_url_update.xlsx')