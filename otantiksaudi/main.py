
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


def return_ele(name, soup):
    try:
        return soup.find('span', text=re.compile(name)).next_element.next_element.next_element.next_element.text.strip()
    except:
        return ''


options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')
#opti#     driver = webdriver.Firefox()ons.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)


urls = pd.read_excel('otantiksaudi_update_url.xlsx')
list_urls = []

for indx, row in urls.iterrows():
    list_urls.append(
        {'url': row['url'], 'cat1': row['cat1'], 'cat2': row['cat2'], 'cat3': row['cat3']},
    )



df = pd.read_excel('otantiksaudi_model_product.xlsx')

for i, url1 in enumerate(list_urls):
    print('Count: ', i)
    url = url1['url'].replace('https://www.otantiksaudi.com/en/', 'https://www.otantiksaudi.com/ar/')
    cat1 = url1['cat1']
    cat2 = url1['cat2']
    cat3 = url1['cat3']
    print('URL: ', url)
    driver.get(url)
    time.sleep(2)
    r = driver.find_element_by_tag_name('body').get_attribute('innerHTML')
    soup = BeautifulSoup(r, 'html.parser')

    name = soup.find('h1', {'itemprop': 'name'}).text.strip()
    price = soup.find('span', {'class': 'oe_currency_value'}).text.strip()
    time.sleep(1)
    regex = '^availability_message'
    is_in_stock = soup.find('div', {'class': re.compile(regex)}).text.replace('في المخزون', 'x').replace('الوحدات متاح', '').strip()
    sku  = soup.find('div', {'itemprop': 'sku'}).text.strip()
    description = soup.find('div', {'id': 'product_details'}).find('p').text.strip()
    time.sleep(2.5)
    try:
        images = soup.find('div', {'id': 'thumbnailSlider'}).find_all('img', {'alt': 'Product image'})
        list_images = ['https://www.otantiksaudi.com' + img['data-src'].replace('image_128', 'image_1024') for img in images if img['src'] != '']
        base_image = list_images[0]
        add_images = ','.join(list_images[1:])
    except:
        images = soup.find('div', {'id': 'mainSlider'}).find_all('img', {'alt': 'Product image'})
        list_images = ['https://www.otantiksaudi.com' + img['data-src'].replace('image_128', 'image_1024') for img in images if img['src'] != '']
        base_image = list_images[0]
        add_images = ''
    
    free_colors = return_ele('اللون', soup)
    capacity = return_ele('السعة / القياسات', soup)
    style = return_ele('التصميم', soup)
    raw_materials = return_ele('الخامة', soup)
    num_pieces = return_ele('عدد القطع', soup)
    group = return_ele('المجموعة', soup)


    data = {
        'sku': sku,
        'name': name,
        'link_url': url,
        'price': price,
        'free_colors': free_colors,
        'capacity': capacity,
        'style': style,
        'raw_materials': raw_materials,
        'num_pieces': num_pieces,
        'group': group,
        'is_in_stock': is_in_stock,
        'description': description,
        'base_image': base_image,
        'add_images': add_images,
        'cat1': cat1,
        'cat2': cat2,
        'cat3': cat3,
    }
    df1 = pd.DataFrame([data])
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('otantiksaudi_update_products_ar1.xlsx')