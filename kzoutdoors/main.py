
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
import convert_numbers

def convert_price(price):
    try:
        
        return    str(convert_numbers.hindi_to_english(price.split('٫')[0])) + '.' +  str(convert_numbers.hindi_to_english(price.split('٫')[1]))
    except:
        return   str(convert_numbers.hindi_to_english(price))


def return_element(name, soup):
    try:
        try:
            return soup.find('span', text=re.compile(name)).next_element.next_element.next_element.next_element.text.strip()
        except:
            return soup.find('li', text=re.compile(name)).text.replace(name, '').replace(':', '').strip()
    except:
        return ''

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


urls = pd.read_excel('kzoutdoors_url_update.xlsx')
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
    
    cat1 = url1['cat1']
    cat2 = url1['cat2']
    cat3 = url1['cat3']
    url = url1['url']
    logging.info(f'URL: {url}')
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    cookies = {'session': '134-8225175-0355220'}
    r = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(r.content, "html.parser")
    name = soup.find('h1', {'class': 'product-details__title'}).text.replace('|', '').strip()
    try:
        ms_brands = soup.find('h4', {'class': 'product-details__subtitle'}).text.split('|')[0].strip()
    except:
        ms_brands = ''
    price = soup.find('span', {'class': 'product-price'}).text.replace('ر.س', '').strip()
    price1 = convert_price(price)
    description = soup.find('div', {'class': 'product-detials__desc'}).text.strip()
    sku = return_element('رقم الموديل', soup)
    product_size = return_element('الأبعاد', soup)
    weight = return_element('الوزن', soup)
    height = return_element('حجم الشنطة', soup)
    bag_capacite = return_element('تتسع لـ', soup)
    bag_dimensions = return_element('أبعاد الشنطة', soup)
    if bag_dimensions == '':
        bag_dimensions = return_element('أبعاد شنطة الخيمة', soup)
    if bag_dimensions == '':
            bag_dimensions = return_element('أبعاد الحقيبة', soup)     
    capacity_tent = return_element('الإرتفاع', soup)
    canopy_dimensions = return_element('أبعاد المظلة', soup)
    weight = return_element('الوزن', soup)
    
    images = soup.find('div', {'id': 'sp-slider-cont'}).find_all('img')
    len(images)

    list_images = [img['src'] for img in images]
    base_image = list_images[0]
    add_images = ','.join(list_images[1: ])
    data = {
        'sku': sku,
        'name': name,
        'price': price,
        'price1': price1,
        'link_url': url,
        'ms_brands': ms_brands,
        'description': description,
        'product_size': product_size,
        'weight': weight,
        'height': height,
        'bag_capacite': bag_capacite,
        'capacity_tent': capacity_tent,
        'bag_dimensions': bag_dimensions,
        'canopy_dimensions': canopy_dimensions,
        'base_image': base_image,
        'add_images': add_images,
        'cat1': cat1,
        'cat2': cat2,
        'cat3': cat3,
    }
    return data

df = pd.read_excel('kzoutdoors_product_model.xlsx')

for i, url in enumerate(list_urls[180: ]):
    logging.info('Count: %s / %s', i, len(list_urls))
    data = scrape_data(url)
    df1 = pd.DataFrame([data])
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('kzoutdoors_product_update2.xlsx')
    
logging.info('Scraping Products Done.')
