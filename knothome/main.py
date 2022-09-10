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

options = Options()
ua = UserAgent()
userAgent = ua.random
logging.info(userAgent)
options.add_argument(f'user-agent={userAgent}')
#opti#     driver = webdriver.Firefox()ons.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)

@dataclass
class Product:
    link_url: str = ''
    name: str = ''
    price: str = ''
    special_price: str = ''
    description: str = ''
    raw_materials: str = ''
    images_size: str = ''
    base_image: str =  ''
    add_images: str = ''
    cat1: str = ''
    cat2: str = ''
    cat3: str = ''


def extract_data(driver, url1):
    product = Product()
    product.cat1 = url1['cat1']
    product.cat2 = url1['cat2']
    product.cat3 = url1['cat3']
    url = url1['url']
    logging.info('URL: %s', url)
    driver.get(url)
    time.sleep(2)
    body = WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.TAG_NAME,'body')))
    try:
        body.find_element(By.ID, 'wg-ar').click()
    except:
        pass
    r = driver.page_source
    soup = BeautifulSoup(r, "html.parser")
    product.link_url = url
    product.name = soup.find('div', {'class': 'product__title'}).find('span').text.strip()
    product.price = soup.find('span', {'class': 'money'}).text.strip()
    product.description = soup.find('div', {'class': 'product__text'}).text.strip()
    try:
        product.raw_materials = ', '.join([rw.text for rw in soup.find('button', {'class': 'product__tab-button'}, text=re.compile('المواد')).parent.find_all('li')])
    except:
        pass
    try:
        product.images_size = soup.find('button', {'class': 'product__tab-button'}, text=re.compile('حجم المنتج')).parent.find('img')['src']
    except:
        pass
    images = soup.find_all('div', {'class': 'product__gallery-item'})
    list_images = ['https:' + img.find('img', {'src': re.compile(r'^//cdn.shopify.com/s/files')})['src'].replace('110x110@', '').split('?')[0] for img in images]
    list_images  = list(dict.fromkeys(list_images))
    list_images
    product.base_image = list_images[0]
    product.add_images = ','.join(list_images[1:])
    return product.__dict__


urls = pd.read_csv('knothhome_url_mupdate.csv')
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

def scrape_data(url1, driver):
    data = extract_data(driver, url1)
    return data

df = pd.read_csv('knothhome_product_model.csv')
for i, url in enumerate(list_urls):
    logging.info('Count: %s', i)
    try:
        data = scrape_data(url, driver)
    except:
        continue
    df1 = pd.DataFrame([data])
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('knothhome_product_update.xlsx')

