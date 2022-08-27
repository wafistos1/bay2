
from operator import mod
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


urls = pd.read_excel('test1.xlsx')

url_product = [{'url': row['url'], 'cat1': row['cat1'],'cat2': row['cat2'],'cat3': row['cat3'], } for index, row in urls.iterrows()]

def extract_ele(name, soup, all=False):
    try:
        if all:
            return soup.find('p', text=re.compile(name)).text.strip()
        return soup.find('p', text=re.compile(name)).text.replace(name, '').replace('مكون من', '').replace(':', '').strip()
    except:
        return ''

def scrape_data(url1):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36', 
    'Accept-Encoding': 'gzip, deflate', 
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8', 
    'Connection': 'keep-alive', 
    'Accept-Language': 'en-US,en;q=0.5', 
    'Upgrade-Insecure-Requests': '1', 
    'Pragma': 'no-cache', 
    'Cache-Control': 'no-cache'
    }
    url = url1['url']
    cat1 = url1['cat1']
    cat2 = url1['cat2']
    cat3 = url1['cat3']
    print('URL:', url)
    
    r = requests.get(str(url), headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    #Scrape Data
    name = soup.find('h1', {'class': 'product-details__title'}).text.strip()

    try:
        price = soup.find('span', {'class': 'price-before'}).text.replace('ر.س', '').strip()
        special_price = soup.find('span', {'class': 'price-after'}).text.replace('ر.س', '').strip()
    except:
        price = soup.find('span', {'class': 'product-price'}).text.replace('ر.س', '').strip()
        special_price = 0
    try:
        model = soup.find('span', text=re.compile('رقم الموديل')).next_element.next_element.next_element.next_element.text.strip()
    except:
        model = ''
    sku = model
    description = soup.find('div', {'class': 'product-detials__desc'}).text.strip()
    images = soup.find_all('img', {'class': 'image_first_click product-details__thumb'})
    list_img = [img['src'] for img in images]
    list_img
    list_img = list(dict.fromkeys(list_img))
    images_base = list_img[0]
    add_images = ','.join(list_img[1:])
    
    raw_materials = extract_ele('مصنوع من', soup)
    free_colors = extract_ele('لون', soup)

    number_pieces = extract_ele('مقاس', soup, all=True)
    capacite =  extract_ele('سعة', soup, all=True)
    
    
    #is_in_stock = soup.find('div', {'class': 'product-info-stock-sku'}).text.replace('حالة التوفر :', '').strip()

    data = {
        'sku': sku,
        'link_url': url,
        'name': name,
        'price': price,
        'special_price': special_price,
        'model': model,
        'raw_materials': raw_materials,
        'free_colors': free_colors,
        'number_pieces': number_pieces,
        'capacite': capacite,
        'description': description,
        'images_base': images_base,
        'add_images': add_images,
        'cat1': cat1,
        'cat2': cat2,
        'cat3': cat3,
    }
    return data

df = pd.read_excel('dania_model1.xlsx')
for i, url in enumerate(url_product):
    logging.info(f'Count: {i}')
    data = scrape_data(url)
    df1 = pd.DataFrame([data])
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('dania_update_products1.xlsx')
