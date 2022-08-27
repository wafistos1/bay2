
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

def return_ele(name, soup):
    try:
        return soup.find('p', text=re.compile(name)).text.replace(name, '').replace(':', '').strip()
    except:
        return ''

urls = pd.read_excel('yorganhome_url_update.xlsx')
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
    driver.get(url)
    time.sleep(2)
    try:
        btn_detail = driver.find_element_by_xpath('//button[@class="btn btn-default expand-toggle"]')
        btn_detail.click()
    except:
        pass
    
    r = driver.find_element_by_tag_name('body').get_attribute('innerHTML')
    soup = BeautifulSoup(r, "html.parser")
    try:
        sku = soup.find('div', {'class': 'list--table-view__cell value'}).text.strip()
    except:
        sku = ''
    name = soup.find('h1', {'class':'product-details__title brand-title'}).text.strip()
    price = soup.find('span', {'class': 'product-price'}).text.replace( 'ر.س', '').strip()
    try:
        description = soup.find('div', {'class': 'product-detials__desc pd-exp'}).text.strip()
    except:
        try:
            description = soup.find('div', {'class': 'product-detials__desc pd-exp expanded'}).text.strip()
        except:
            description = soup.find('div', {'class': 'product-detials__desc'}).text.strip()
    try:
        charchif = soup.find('p', text=re.compile('شرشف السرير')).text.strip()
    except:
        charchif = ''
    try:
        size_lehaf = soup.find('u', text=re.compile('بدون حشوة :')).next_element.next_element.next_element.next_element
    except:
        size_lehaf = return_ele('بيت اللحاف', soup)
    pillows = return_ele('المخدات', soup)
    organic_cotton = return_ele('قطن عضوي', soup)
    
    # images
    images = soup.find_all('img', {'class': 'image_first_click product-details__thumb'})
    len(images)
    list_images = [img['src'] for img in images]
    base_image = list_images[0]
    add_images = ','.join(list_images[1: ])
    
    data = {
        'sku': sku,
        'name': name,
        'price': price,
        'link_url': url,
        'description': description,
        'charchif': charchif,
        'pillows': pillows,
        'organic_cotton': organic_cotton,
        'size_lehaf': size_lehaf,
        'base_images': base_image,
        'add_images': add_images,
        'cat1': cat1,
        'cat2': cat2,
        'cat3': cat3,
    }
    return data

# Start firefoxe
options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')
#opti#     driver = webdriver.Firefox()ons.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)

df = pd.read_excel('yorganhome_product_model.xlsx')
for i, url in enumerate(list_urls):
    logging.info('--Count: %s', i)
    data = scrape_data(url)
    df1 = pd.DataFrame([data])
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('yorganhome_product_update.xlsx')
