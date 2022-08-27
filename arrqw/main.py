
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


def return_element(name, soup):
    try:
        try:
            return soup.find('li', text=re.compile(name)).text.replace(name, '').strip()
        except:
            return soup.find('span', text=re.compile(name)).text.replace(name, '').strip()
    except:
        return ''

urls = pd.read_excel('arrqw_url_update.xlsx')
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
    url = url1['url']
    cat1 = url1['cat1']
    cat2 = url1['cat2']
    cat3 = url1['cat3']
    logging.info('--URL: %s', url)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    cookies = {'session': '134-8225175-0355220'}
    r = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(r.content, "html.parser")
    
    #Data
    name = soup.find('h1', {'itemprop': 'name'}).text.strip()
    price = soup.find('div', {'id': 'product_details'}).find('span', {'class': 'oe_currency_value'}).text.replace(',', '').strip()
    try:
        sku = soup.find('div', {'id': 'product_details'}).find('span', {'itemprop': 'sku'}).text.replace(',', '').strip()
    except:
        sku = ''
    description = soup.find('ul', {'style': 'margin-right: 0px; margin-bottom: 10px; margin-left: 25px; padding: 0px;'}).text.strip()  
    model_number = return_element('رقم الموديل:', soup)
    free_colors = return_element('اللون', soup)
    brands = return_element('الماركة:', soup)
    freeze_powers = return_element('قدرة التبريد', soup)
    products_size = return_element('الأبعاد الصافية', soup)
    weight = return_element('الوزن الصافي', soup)
    
    #Scrape images
    images = soup.find_all('img', {'alt': 'Product image'})

    if len(images) == 1:
        list_images = 'https://www.arrqw.com' +  soup.find('img', {'itemprop': 'image'})['data-src']
    else:
        
        list_images = ['https://www.arrqw.com' + img['data-src'].replace('image_128', 'image_1024') for img in images]
    
    if len(images) != 1:
        base_image = list_images[0]
        add_images = ','.join(list_images[1: ])
    else:
        base_image = list_images
        add_images = ''    
    
    data = {
        'sku': sku,
        'name': name,
        'link_url': url,
        'price': price,
        'description': description,
        'model_number': model_number,
        'free_colors': free_colors,
        'brands': brands,
        'freeze_powers': freeze_powers,
        'products_size': products_size,
        'weight': weight,
        'base_image': base_image,
        'add_images': add_images,
        'cat1': cat1,
        'cat2': cat2,
        'cat3': cat3,        
    }
    return data

df = pd.read_excel('arrqw_product_model.xlsx')
for i, url in enumerate(list_urls):
    logging.info('--Count: %s', i)
    try:
        data = scrape_data(url)
    except:
        continue
    df1 = pd.DataFrame([data])
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('arrqw_product_update.xlsx')