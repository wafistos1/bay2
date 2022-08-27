import time
import os
import logging
import requests
import re
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



logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

# body=WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.TAG_NAME,'body')))
# r = body.get_attribute('innerHTML')
# soup = BeautifulSoup(r, "html.parser")



urls = pd.read_excel('salla_url_update.xlsx')
list_urls = []
for index, row in urls.iterrows():
    list_urls.append({
            'url': row['url'],
            'cat1': row['cat1'],
            'cat2': row['cat2'],
            'cat3': row['cat3'],
        })

def scrape_data(url1):
    cat1 = url1['cat1']
    cat2 = url1['cat2']
    cat3 = url1['cat3']
    url = url1['url']
    logging.info('URL: %s', url)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    cookies = {'session': '134-8225175-0355220'}
    r = requests.get(url, headers=headers, cookies=cookies)
    time.sleep(2)
    soup = BeautifulSoup(r.content, "html.parser")
    # Scraping Data
    name = soup.find('h1', {'class': 'product-details__title'}).text.strip()
    price = soup.find('span', {'class': 'product-price'}).text.replace('ر.س', '').strip()
    images = soup.find('div', {'class': 'owl-carousel'}).find_all('img')
    list_images = [img['src'] for img in images]
    base_image = list_images[0]
    add_images = ','.join(list_images[1: ])
    return {
        'link_url': url,
        'name': name,
        'price': price,
        'base_image': base_image,
        'add_images': add_images,
        'cat1': cat1,
        'cat2': cat2,
        'cat3': cat3,
        }
df = pd.read_excel('salla_product_model.xlsx')
for i, url in enumerate(list_urls):
    logging.info('Count: %s', i)
    data = scrape_data(url)
    df1 = pd.DataFrame([data])
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('salla_product_update.xlsx')
logging.info('Scraping Products Done.')
