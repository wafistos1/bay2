
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

def return_content(soup, start, end):
    details = soup.find('div', {'class': 'product-detials__desc'}).find_all('p')
    if details:
        content = []
        scrap = False
        for detail in details:
            
            if detail.text == start: #and detail.text != end:
                scrap = True
            elif detail.text == end:
                scrap = False
            if scrap:
                if detail.text != '':
                    content.append(detail.text)
                    start_content = True
        if content:
            return ','.join(content)
        return '__EMPTY__VALUE__'
    return '__EMPTY__VALUE__'

@dataclass
class Product:
    sku : str = ''
    link_url : str = ''
    name : str = ''
    price : str = ''
    product_size : str = ''
    size : str = ''
    manufacturer: str = ''
    cotton: str = ''
    content : str = ''
    content1 : str = ''
    content2 : str = ''
    washing_instructions : str = ''
    capacity: str = ''
    description : str = ''
    base_image : str =  ''
    add_images : str = ''
    cat1 : str = ''
    cat2 : str = ''
    cat3 : str = ''

urls = pd.read_excel('karacahomesa_url_update.xlsx')
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
    url = url1['url'] + '?currency=SAR'
    logging.info('URL: %s', url)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    cookies = {'session': '134-8225175-0355220'}
    r = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(r.content, "html.parser")
    # Extract data
    product = Product()
    product.link_url = url
    product.name = soup.find('h1', {'class': 'product-details__title'}).text.strip()
    try:
        product.sku = soup.find('div', {'class': 'value'}).text.strip()
    except AttributeError:
        logging.warning('No SKU found.')
        product.name = ''
    product.price = soup.find('span', {'class': 'product-price'}).text.replace('ر.س', '').strip()
    product.description = soup.find('div', {'class': 'product-detials__desc'}).text.strip()
    product.content2 = return_content(soup, 'المحتويات:', 'تعليمات الغسيل:')
    product.content1 = return_content(soup,'مزايا مجموعات أغطية اللحاف القطنية: ', 'المحتويات:')
    product.content = return_content(soup,'طقم مفارش مفرد (نفر ونص) 4 قطع', 'مزايا مجموعات أغطية اللحاف القطنية: ')
    try:
        product.capacity = soup.find('div', {'class': 'product-detials__desc'}).find('', string=re.compile('الحجم')).next_element.text.strip()
    except:
        pass
    try:
        product.size = soup.find('div', {'class': 'product-detials__desc'}).find('', text=re.compile('القياس:')).next_element.text.strip()
    except:
        pass
    try:
        product.cotton = soup.find('div', {'class': 'product-detials__desc'}).find('', text=re.compile('قطن'))
    except:
        pass
    try:
        product.manufacturer = soup.find('div', {'class': 'product-detials__desc'}).find('', text=re.compile('صناعة'))
    except:
        pass
    # Scrap details product
    try:
        product.washing_instructions  = soup.find('p', text=re.compile('تعليمات الغسيل:')).next_element.next_element.next_element.text.strip()
    except:
        product.washing_instructions = ''
    # Scrap Images
    images = soup.find_all('a', {'data-fancybox': 'product-images'})
    if images == []:
        product.base_image = ''
        product.add_images = ''
    else:
        list_images = [img.find('img')['src'] for img in images]
        product.base_image = list_images[0]
        product.add_images = ','.join(list_images[1: ]) 
    product.cat1 = cat1
    product.cat2 = cat2
    product.cat3 = cat3
    
    return product.__dict__

df = pd.read_excel('karacahomesa_product_model.xlsx')
for i, url in enumerate(list_urls):
    logging.info('Count: %s', i)
    data = scrape_data(url)
    time.sleep(1)
    df1 = pd.DataFrame([data])
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('karacahomesa_product_update2.xlsx')
logging.info('Scraping Products Done..')
