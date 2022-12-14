
import time
import os
import requests
import re
import logging
from dataclasses import dataclass, field
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

#pip install requests pandas openpyxl selenium=3.14 fake_useragent bs4
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

def return_ele(name, soup):
    try:
        return soup.find('th', text=re.compile(name)).parent.find('td').text.strip()
    except:
        return ''

@dataclass
class Product:
    sku: str = ''
    link_url: str = ''
    name: str = ''
    price: str = ''
    special_price: str = ''
    free_colors: str = ''
    manufacturer: str = ''
    style: str = ''
    raw_materials: str = ''
    product_size: str = ''
    description: str = ''
    base_image: str =  ''
    add_images: str = ''
    cat1: str = ''
    cat2: str = ''
    cat3: str = ''

urls = pd.read_excel('aldarest_url_update.xlsx')
list_urls = []
for index, row in urls.iterrows():
    list_urls.append(
        {
            'url': row['url'],
            'cat1': row['cat1'],
            'cat2': row['cat2'],
            'cat3': row['cat3'],
        }
    )

def scrape_data(url1):
    product = Product()
    product.cat1 = url1['cat1']
    product.cat2 = url1['cat2']
    product.cat3 = url1['cat3']
    url = url1['url']
    product.link_url = url
    logging.info('URL: %s', url)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    cookies = {'session': '134-8225175-0355220'}
    r = requests.get(url, headers=headers, cookies=cookies)
    
    time.sleep(1)
    soup = BeautifulSoup(r.content, "html.parser")
    try:
        product.sku = soup.find('span', {'sku'}).text.strip()
    except:
        pass
    product.name = soup.find('h1', {'class': 'product_title'}).text.strip()
    try:
        product.price = soup.find('del').find('span', {'class': 'woocommerce-Price-amount'}).text.strip()
    except:
        product.price = soup.find('span', {'class': 'woocommerce-Price-amount'}).text.strip()
    try:
        product.special_price = soup.find('span', {'class': 'special-price'}).text.strip()
    except:
        pass
    try:
        product.description = soup.find('div', {'class': 'woocommerce-product-details__short-description'}).text.strip()
    except:
        pass
    images = soup.find('figure', {'class': 'woocommerce-product-gallery__wrapper'}).find_all('img')
    list_images = [img['src'].replace('-100x100', '') for img in images]
    product.base_image = list_images[0]
    product.add_images = ','.join(list_images[1: ])
    product.free_colors = return_ele('??????????????', soup)
    product.manufacturer = return_ele('??????????????', soup)
    product.style = return_ele('??????????', soup)
    product.raw_materials = return_ele('????????????', soup)
    product.product_size = return_ele('?????????????? ??????????????????', soup)
    
    
    return product.__dict__

df = pd.read_excel('aldarest_product_model.xlsx')
for i, url in enumerate(list_urls):
    logging.info('Count: %s', i)
    data = scrape_data(url)
    df1 = pd.DataFrame([data])
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('aldarest_product_update.xlsx')

