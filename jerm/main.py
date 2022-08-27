#imports here
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
import re
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup

import requests



def return_ele(name, soup):
    try:
        return soup.find('td', text=re.compile(f'^{name}')).next_sibling.next_sibling.text.strip()
    except:
        return ''

urls = pd.read_excel('jerm_update_url.xlsx')

list_urls = []

for indx, row in urls.iterrows():
    list_urls.append(
        {'url': row['url'], 'cat1': row['cat1'], 'cat2': row['cat2'], 'cat3': row['cat3']}
    )

df = pd.read_excel('jerm_product_model.xlsx')

for i, url1 in enumerate(list_urls):
    print('Count: ', i)
    url = 'https://jerm.online' + url1['url']
    cat1 = url1['cat1']
    cat2 = url1['cat2']
    cat3 = url1['cat3']
    print('URL: ', url)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    cookies = {'session': '134-8225175-0355220'}
    r = requests.get(url, headers=headers, cookies=cookies)
    time.sleep(2)
    soup1 = BeautifulSoup(r.content, 'html.parser')
    
    name = soup1.find('h1', {'itemprop': 'name'}).text.strip()
    price = soup1.find('s', {'class': 'product-single__sale-price'}).text.strip()
    special_price = soup1.find('span', {'class': 'product-single__price'}).text.strip()
    prices = soup1.find('div', {'class': 'product-single__prices'}).find_all('span', {'class': 'money'})
    price = prices[1].text.strip()
    special_price = prices[0].text.strip()
    if price == '0 SR':
        price = prices[0].text.strip()
        special_price = 0
    try:
        description = soup1.find('section', {'class': 'productAccordion'}).text.strip()
    except:
        try:
            description = soup1.find('div', {'itemprop': 'description'}).text.strip()
        except:
            description = ''
    sku = return_ele('SKU', soup1)
    products_size = return_ele('Size', soup1)
    manufacturer = return_ele('Handmade in', soup1)
    free_colors = return_ele('Some Field Color', soup1)
    images = soup1.find_all('img', {'class': 'product-single__image'})
    list_images = ['https:' + img['data-src'].replace('{width}x', 'grande').split('?')[0] for img in images]
    base_image = list_images[0]
    add_images = ','.join(list_images[1:])
    
    
    data = {
        'sku': sku,
        'name': name,
        'link_url': url,
        'price': price,
        'special_price': special_price,
        'products_size': products_size,
        'manufacturer': manufacturer,
        'free_colors': free_colors,
        'description': description,
        'base_image': base_image,
        'add_images': add_images,
        'cat1': cat1,
        'cat2': cat2,
        'cat3': cat3,
        
    }
    
    df1 = pd.DataFrame([data])
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('jerm_product_update.xlsx')
