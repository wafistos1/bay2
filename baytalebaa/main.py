
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

name_excel = 'bayalebaa_product_update.xlsx'
options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')
#opti#     driver = webdriver.Firefox()ons.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)

urls_df = pd.read_excel('bayalebaa_url_update1.xlsx')
urls = urls_df['url'].to_list()


def extract_data(driver, url):
    url1 = url.replace('https://baytalebaa.com/products/', 'https://baytalebaa.com/en/product/')
    print('URL: ', url1)
    driver.get(url1)
    time.sleep(2)
    r = driver.find_element_by_tag_name('body').get_attribute('innerHTML')
    soup = BeautifulSoup(r, 'html.parser')
    name = soup.find('h1', {'itemprop': 'name'}).text.strip()
    price = soup.find('p', {'class': 'price'}).find('bdi').text.strip()
    sku = soup.find('span', {'class': 'sku_wrapper'}).text.replace('رمز المنتج:', '').strip()
    short_description = soup.find('table', {'class': 'woocommerce-product-attributes shop_attributes'}).text.strip()
    
    description = soup.find('div', {'id': 'tab-description'}).text.strip()   
    cats = soup.find('nav', {'class': 'woocommerce-breadcrumb'}).find_all('a')

    cat1 = cats[1].text.strip()
    cat2 = cats[2].text.strip()
    try:
        cat3 = cats[3].text.strip()
    except:
        cat3 = ''
    regex = re.compile('^product-image-thumbnail ')
    images = soup.find_all('div', {'class': regex})
    print('Len: ', len(images))
    if len(images) == 0:
        images = soup.find_all('div', {'class': 'product-image-wrap'})
    list_images = [img.find('img')['src']for img in images ]

        
    base_image = list_images[0]
    add_images = ','.join(list_images[1: ])

    data = {
        'name': name,
        'link_url': url,
        'price': price,
        'sku': sku,
        'description': description,
        'short_description': short_description,
        'cat1': cat1,
        'cat2': cat2,
        'cat3': cat3,
        'base_image': base_image,
        'add_images': add_images,
    }
    return data
df = pd.read_excel('bayalebaa_product_model.xlsx')

for i, url in enumerate(urls):
    print('Count: ', i)

    try:
        data = extract_data(driver, url)
    except:
        continue

    df1 = pd.DataFrame([data])
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel(name_excel)