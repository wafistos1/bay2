import time
import logging
# import os
import re
import requests
import pandas as pd
# import numpy as np
# from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
from fake_useragent import UserAgent
# from random import randint
# from datetime import datetime
# from datetime import timedelta
from bs4 import BeautifulSoup

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')
#opti#     driver = webdriver.Firefox()ons.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)

def return_ele(name, soup):
    try:
        return soup.find('span', text=re.compile(name)).next_element.next_element.next_element.next_element.text.strip()
    except:
        return ''

def extract(name, soup):
    try:
        return soup.find('th', text=re.compile(name)).next_element.next_element.next_element.text.strip()

    except:
        return ''

def extract_data(url1):
    url = url1['url']
    cat1 = url1['cat1']
    cat2 = url1['cat2']
    cat3 = url1['cat3']
    logging.info('URL %s', url)
    driver.get(url)
    body=WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.TAG_NAME,'body')))
    time.sleep(3)
    r = body.get_attribute('innerHTML')
    soup = BeautifulSoup(r, "html.parser")

    try:
        name = soup.find('span', {'id': 'productTitle'}).text.strip()
    except:
        headers = {'User-Agent': userAgent}
        cookies = {'session': '134-8225175-0355220'+ str(i)}
        time.sleep(3)
        r = requests.get(url, headers=headers, cookies=cookies)
        time.sleep(1)
        soup = BeautifulSoup(r.text, "html.parser")
        name = soup.find('span', {'id': 'productTitle'}).text.strip()

    price1 = soup.find('span', {'class': 'a-price-whole'}).text.strip().split('.')[0]

    price2 = soup.find('span', {'class': 'a-price-fraction'}).text.strip()
    price = price1 + '.'+  price2
    free_colors = return_ele('اللون', soup)
    raw_materials = return_ele('المادة', soup)
    brand = return_ele('العلامة التجارية', soup)
    style = return_ele('النمط', soup)
    spec = extract('الخصائص', soup)
    products_size = extract('أبعاد الشحنة', soup)
    included_ingredients = extract('المكونات المشمولة', soup)
    free_colors1 = return_ele('نوع اللمسة النهائية', soup)
    try:
        product_details = soup.find('table', {'id': 'productDetails_techSpec_section_1'}).text.strip()
    except:
        product_details = ''

    is_in_stock = soup.find('div', {'id': 'availability'}).find('span').text.strip()

    try:
        description = soup.find('div', {'id': 'featurebullets_feature_div'}).text.strip()
    except AttributeError:
        description = ''

    try:
        images = soup.find('div', {'id': 'altImages'}).find_all('img', )
        len(images)
    except AttributeError:
        images = soup.find('div', {'id': 'imageBlock'}).find_all('img', )


    list_images = []
    for img in images[:-1]:
        # print(img['src'].split('_'))
        list_images.append(''.join([img['src'].split('_')[0], img['src'].split('_')[-1].replace('.', '')] ))

    base_image = list_images[0]
    add_images = ','.join(list_images[1:])
    data = {
        'name': name,
        'link_url': url,
        'price': price,
        'free_colors': free_colors,
        'raw_materials': raw_materials,
        'brand': brand,
        'style': style,
        'included_ingredients': included_ingredients,
        'free_colors1': free_colors1,
        'spec': spec,
        'products_size': products_size,
        'product_details': product_details,
        'is_in_stock': is_in_stock,
        'description': description,
        'base_image': base_image,
        'add_images': add_images,
        'cat1': cat1,
        'cat2': cat2,
        'cat3': cat3,
    }
    return data


urls = pd.read_excel('amz_update_url.xlsx')
list_urls = []

for indx, row in urls.iterrows():
    list_urls.append(
        {'url': row['url'], 'cat1': row['cat1'], 'cat2': row['cat2'], 'cat3': row['cat3']},
    )

df = pd.read_excel('amz_product_model.xlsx')

for i, url1 in enumerate(list_urls):
    logging.info('Count: %s', i)
    try:
        data = extract_data(url1)
    except IndexError:
        continue
        
    df1 = pd.DataFrame([data])
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('amz_update_products02.xlsx')
