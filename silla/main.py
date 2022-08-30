
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

@dataclass
class Product:
    link_url : str = ''
    name : str = ''
    price : str = ''
    description : str = ''
    base_image : str =  ''
    add_image: str = '' 
    cat1 : str = ''
    cat2 : str = ''
    cat3 : str = ''

urls = pd.read_excel('silla_url_update.xlsx')
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
    soup = BeautifulSoup(r.content, "html.parser")
    time.sleep(2)
    product.name = soup.find('h1', {'class': 'product-details__title'}).text.strip()
    images = soup.find_all('img', {'class': 'product-details__thumb'})
    list_images = [img['src'] for img in images]
    product.base_image = list_images[0]
    product.add_images = ','.join(list_images[1: ])
        
    return product.__dict__

df = pd.read_excel('silla_product_model.xlsx')
for i, url in enumerate(list_urls):
    logging.info('Count: %s', i)
    data = scrape_data(url)
    df1 = pd.DataFrame([data])
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('silla_product_update.xlsx')
    
logging.info('Scraping products Done..')

