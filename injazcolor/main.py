
import time
import os
import requests
import re, logging
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
        try:
            return soup.find('em', text=re.compile(name)).text.replace(name, '').strip()
        except: 
            return soup.find('strong', text=re.compile(name)).text.replace(name, '').strip()
    except: return ''

options = Options()
ua = UserAgent()
userAgent = ua.random
logging.info(userAgent)
options.add_argument(f'user-agent={userAgent}')
#opti#     driver = webdriver.Firefox()ons.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)


urls = pd.read_excel('injazcolor_url_product.xlsx')
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
    logging.info('URL: %s', url)
    driver.get(url)
    body=WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.TAG_NAME,'body')))
    r = body.get_attribute('innerHTML')
    soup = BeautifulSoup(r, "html.parser")
    time.sleep(1)
    # Data extract
    name = soup.find('h1', {'class': 'product_title'}).text.strip()
    sku = name.split(' ')[-1]
    price = soup.find('p', {'class': 'price'}).text.split('لكل')[0].replace('SAR', '').strip()
    price = soup.find('p', {'class': 'price'}).text.split('Per')[0].replace('SAR', '').strip()
    try:
        if soup.find('p', {'class': 'price'}).text.split('Per')[1].strip():
            price_dimension = 'M2'
        else:
            price_dimension = 'M2'
    except:
        price_dimension = '__EMPTY__VALUE__'
    try:
        description = soup.find('div', {'class': 'woocommerce-product-details__short-description'}).text.strip()
    except AttributeError:
        logging.warning('No description find.')
        description = ''
    
    product_size = return_ele('لوح مقاس', soup)
    product_size1 = return_ele('مقاس اللوح', soup)
    images = soup.find('div', {'class': 'owl-stage'}).find_all('img')
    list_images = [img['src'].split('?')[0] for img in images]
    base_image = list_images[0]
    add_images = ','.join(list_images[1: ])
    
    return {
        'sku': sku,
        'name': name,
        'link_url': url,
        'price_dimension': price_dimension,
        'price': price,
        'product_size': product_size,
        'product_size1': product_size1,
        'description': description,
        'base_image': base_image,
        'add_images': add_images,
        'cat1': cat1,
        'cat2': cat2,
        'cat3': cat3,
    }
df = pd.read_excel('injazcolor_product_model.xlsx')
for i, url in enumerate(list_urls):
    logging.info('Count: %s / %s', i, len(list_urls))
    data = scrape_data(url)
    df1 = pd.DataFrame([data])
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('injazcolor_product_update.xlsx')
logging.info('Scrape Products Done.')