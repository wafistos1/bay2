
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


urls = pd.read_excel('astore_url_update.xlsx')
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
    name = soup.find('section').find('h1').text.strip()
    price = soup.find('del', {'class': 'product-formatted-price-old'}).text.replace('ر.س', '').strip()
    special_price = soup.find('h1', {'class': 'product-formatted-price'}).text.replace('ر.س', '').strip()
    sku = soup.find('div', {'class': 'product-sku'}).text.strip()
    description = soup.find('div', {'class': 'description-paragrah'}).find('p').text.strip()
    images = soup.find('div', {'class': 'product-images-carousel-thumbs'}).find_all('img')
    list_images = [img['src'].replace('-thumbnail-370x370-70.jpg', '-thumbnail-770x770-70.jpg') for img in images]
    base_image = list_images[0]
    add_images = ','.join(list_images[1:])
    data = {
        
        'sku': sku,
        'name': name,
        'price': price,
        'link_url': url,
        'special_price': special_price,
        'description': description,
        'base_image': base_image,
        'add_images': add_images,
        'cat1': cat1,
        'cat2': cat2,
        'cat3': cat3,
    }
    return data
df = pd.read_excel('astore_product_model.xlsx')
for i, url in enumerate(list_urls):
    logging.info(f'--Count: {i}')
    data = scrape_data(url)
    df1 = pd.DataFrame([data])
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('astore_product_update.xlsx')
