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


def scrap_product(url1):
    url = url1['url']
    cat1 = url1['cat1']
    cat2 = url1['cat2']
    print('URL: ', url)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    cookies = {'session': '134-8225175-0355220'}
    r = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(r.content, "html.parser")
    try:
        sku = soup.find('span', {'class': 'sku'}).text.strip()
    except:
        sku = ''
    name = soup.find('h1', {'class': 'product_title entry-title wd-entities-title'}).text.strip()
    try:
        price = soup.find('p', {'class': 'price'}).find('del').text.replace('ر.س', '').strip()
        special_price = soup.find('p', {'class': 'price'}).find('ins').text.replace('ر.س', '').strip()
    except:
        price = soup.find('p', {'class': 'price'}).text.replace('ر.س', '').strip()
        special_price = 0
    try:
        qty = soup.find('p', {'class': 'stock in-stock'}).text.replace('متوفر في المخزون', '').strip()
    except:
        qty = ''
    type_ = soup.find('span', {'class': 'posted_in'}).text.replace('التصنيف:', '').strip()
    try:
        description = soup.find('div', {'id': 'tab-description'}).text.strip()
    except:
        description = ''
    images = soup.find_all('figure', {'class': 'woocommerce-product-gallery__image'})
    list_img = [img.find('img')['src'] for img in images]
    
    base_images = list_img[0]
    additionnel_images = ','.join(list_img[1:])
    
    data = {
        
        'sku': sku,
        'name': name,
        'price': price,
        'special_price': special_price,
        'link_url': url,
        'qty': qty,
        'type_': type_,
        'description': description,
        'base_images': base_images,
        'additionnel_images': additionnel_images,
        'categories1': cat1,
        'categories2': cat2,
        
    }
    return data

df = pd.read_excel('anssaj_product_model.xlsx')
urls = pd.read_excel('ansaaj_url.xlsx')
list_urls = []
for index, row in urls.iterrows():
    list_urls.append(
        {
            'url': row['url'],
            'cat1': row['cat1'],
            'cat2': row['cat2'],
        }
    )

for i, url in enumerate(list_urls):
    print('Count: ', i)
    data = scrap_product(url)
    df1 = pd.DataFrame([data])
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('anssaj_product_update.xlsx')