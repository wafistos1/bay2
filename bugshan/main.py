
import time
import os
import requests
import re
import logging
from dataclasses import dataclass, field, asdict
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
from typing import List, Optional
from pydantic import BaseModel

#pip install requests pandas openpyxl selenium=3.14 fake_useragent bs4
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

def return_ele(name, soup):
    try:
        return soup.find('article', {'class': 'article article--main article--product-details mb-50'}).find('', text=re.compile(name)).text.replace(name, '').replace('\u200e', '').strip()
    except:
        return ''

@dataclass
class Product:
    link_url : str = ''
    name : str = ''
    price : str = ''
    special_price : str = ''
    description : str = ''
    base_image : str =  ''
    add_images: str = ''
    brand: str = ''
    product_size1: str = ''
    # guarant: str = ''
    manufacturer: str = ''
    capacity: str = ''
    power: str = ''
    lenght: str = ''
    free_colors: str = ''
    product_size: str = ''
    raw_materials: str = ''
    list_columns: str = ''
    cat1 : str = ''
    cat2 : str = ''
    cat3 : str = ''

urls = pd.read_excel('bugshan_url_update.xlsx')
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
    time.sleep(2)
    soup = BeautifulSoup(r.content, "html.parser")
    
    try:
        product.sku = soup.find('div', {'class': 'list--table-view__cell value text-unicode'}).text.strip()
    except:
        pass
    product.name  = soup.find('h1', {'class': 'title'}).text.strip()
    try:
        product.special_price = soup.find('div', {'price-wrapper-info'}).find('span', {'color-danger'}).text.replace('ر.س', '').strip()
        product.price = soup.find('div', {'price-wrapper-info'}).find('small').text.replace('ر.س', '').strip()
    except:
        product.special_price = ''
        product.price = soup.find('div', {'price-wrapper-info'}).text.replace('ر.س', '').strip()
    product.description = soup.find('article', {'class': 'article--product-details'}).text.strip()
    product.free_colors = return_ele('اللون\u200e:', soup)
    product.brand = return_ele('العلامة التجارية:', soup)
    product.product_size = return_ele('أبعاد المنتج:', soup)
    product.raw_materials = return_ele('المادة:', soup)
    product.product_size1 = return_ele('الأبعاد:', soup)
    # product.guarantee = return_ele('ضمان', soup)
    product.manufacturer = return_ele('بلد الصنع:', soup)
    product.capacity = return_ele('الحجم:', soup)
    product.power = return_ele('الجهد:', soup)
    product.lenght = return_ele('العرض:', soup)
    columns = soup.find('article', {'class': 'article article--main article--product-details mb-50'}).find_all('p')
    _columns = [column.text.strip() for column in columns if column.text.strip() != '']
    if len(_columns) > 7:
        _columns = _columns[:8]
    product.list_columns = '///'.join(_columns)

    images  = soup.find_all('li', {'class': 'splide__slide'})
    len(images)
    list_images = [img.find('img')['data-splide-lazy'] for img in images if img.find('img')]
    product.base_image = list_images[0]
    product.add_images = ','.join(list_images[1: ])
    return  product.__dict__


df = pd.read_excel('bugshan_product_model.xlsx')
for i, url in enumerate(list_urls):
    logging.info('Count: %s', i)
    data = scrape_data(url)
    df1 = pd.DataFrame([data])
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('bugshan_product_update_tv.xlsx')
logging.info('Scraping products Done..')

