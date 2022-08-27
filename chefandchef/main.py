import time
import os
import re, logging
import pandas as pd
import requests
import pandas as pd
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.firefox.options import Options
# from random import randint
# import numpy as np

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

def return_ele(name, soup):
    try:
        return soup.find('', text=re.compile(name)).replace(name, '').strip()
    except AttributeError:
        print('No found')

urls = pd.read_excel('chefandchef_url_update.xlsx')
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
    url = 'https://chefandchef.com.sa' + url1['url']
    cat1 = url1['cat1']
    cat2 = url1['cat2']
    cat3 = url1['cat3']
    logging.info('URL: %s', url)
    # request url
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    cookies = {'session': '134-8225175-0355220'}
    r = requests.get(url, headers=headers, cookies=cookies)
    time.sleep(2)
    soup = BeautifulSoup(r.content, "html.parser")
    # Scrape Data
    name = soup.find('article', {'class': 'mt-entry_content'}).parent.find('h2').text.strip()
    sku = soup.find('div', {'class':"product-form__item"}).find('b').next_element.next_element.strip()
    price = soup.find('span', {'class':'mt-product_price'}).find('span').text.strip()
    is_in_stock = soup.find('div', {'id': 'variant-inventory'}).text.strip()
    try:
        description = soup.find('article').find('p').text.strip()
    except:
        description = soup.find('article').text.strip()
    prodctst_size = return_ele('الأبعاد:', soup)
    weight = return_ele('الوزن', soup)
    raw_materials = return_ele('مصنوعة من', soup)
    # Scrape images
    images = soup.find_all('img', {'class': 'prd_image'})
    list_images = ['https:' + img['src'] for img in images]
    base_image = list_images[0]
    add_images = ','.join(list_images[1: ])

    data = {
        'sku': sku,
        'name': name,
        'link_url': url,
        'price': price,
        'description': description,
        'is_in_stock': is_in_stock,
        'raw_materials': raw_materials,
        'prodctst_size': prodctst_size,
        'weight': weight,
        'base_image': base_image,
        'add_images': add_images,
        'cat1': cat1,
        'cat2': cat2,
        'cat3': cat3,
    }
    return data

df = pd.read_excel('chefandchef_product_model.xlsx')
for i, url in enumerate(list_urls):
    logging.info('--Count: %s', i)
    data = scrape_data(url)
    df1 = pd.DataFrame([data])
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('chefandchef_product_product.xlsx')
