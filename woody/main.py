
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

options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')
driver = webdriver.Firefox(firefox_options=options)


def return_ele(name, soup):
    try:
        return soup.find('li', text=re.compile(f'^{name}')).text.replace(name, '').replace('%', '').replace(':', '').strip()
    except:
        return ''


urls_df = pd.read_excel('woody_update_urls.xlsx')
urls = []
for index, row in urls_df.iterrows():
    urls.append({'url': row['url'], 'cat1': row['cat1'], 'cat2': row['cat2'], 'cat3': row['cat3']})


def extract_data(url1, driver):
    cat1 = url1['cat1']
    cat2 = url1['cat2']
    cat3 = url1['cat3']
    url = url1['url']
    print('URL: ', url)
    driver.get(url)
    time.sleep(2)
    r = driver.find_element_by_tag_name('body').get_attribute('innerHTML')
    soup = BeautifulSoup(r, 'html.parser')
    
    
    sku = soup.find('span', {'class': 'sku'}).text.strip()
    name = soup.find('h1', {'itemprop': 'name'}).text.strip()
    prices = soup.find('p', {'class': 'price'}).find_all('span', {'class': 'woocommerce-Price-amount amount'})
    price = prices[0].text.replace('ر.س', '').replace(',', '').strip()
    try:
        special_price = prices[1].text.replace('ر.س', '').replace(',', '').strip()
    except:
        special_price = ''
    description = soup.find('div', {'class': 'woocommerce-product-details__short-description'}).text.strip()

    free_colors = return_ele('اللون', soup)
    product_size = return_ele('المقاس', soup)
    product_type = return_ele('نوع الخامة', soup)
    manufacturer = return_ele('صنع في', soup)
    garanter =  return_ele('الضمان', soup)
    try:
        is_in_stock = soup.find('p', {'class': 'stock in-stock' }).text.strip()
    except: 
        is_in_stock = 0
        
    images = soup.find('figure').find_all('img')

    list_images = [img['src'].split('?')[0] for img in images ]
    base_image = list_images[0]
    add_images = ','.join(list_images[1:])
    
    data = {
        'sku': sku,
        'name': name,
        'link_url': url,
        'price': price,
        'is_in_stock': is_in_stock,
        'special_price': special_price,
        'description': description,
        'free_colors': free_colors,
        'product_size': product_size,
        'product_type': product_type,
        'manufacturer': manufacturer,
        'guarante': garanter,
        'base_image': base_image,
        'add_images': add_images,
        'cat1': cat1,
        'cat2': cat2,
        'cat3': cat3,
    }
    return data    
    
df = pd.read_excel('woody_product_model.xlsx')

for i, url1 in enumerate(urls):
    print('Count: ', i)
    
    data = extract_data(url1, driver)
    df1 = pd.DataFrame([data])
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('woody_update_prod.xlsx')
    