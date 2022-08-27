
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
import time
import os
#from fake_useragent import UserAgent
from random import randint
import pandas as pd
import numpy as np
import requests
import pandas as pd
import re

urls = pd.read_excel('spring_url_update.xlsx')
list_urls = urls['url'].to_list()



def extract_data(url):
    print('URL: ', url)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    cookies = {'session': '134-8225175-035522023'}
    r = requests.get(url, headers=headers, cookies=cookies)
    time.sleep(2)
    soup = BeautifulSoup(r.content, "html.parser")
    try:
        name = soup.find('h1', {'class': 'title title--xx-large mb-10'}).text.replace('\u200e', '').strip()
    except:
        name = soup.find('h1', {'class': 'title title--xx-large mb-0'}).text.replace('\u200e', '').strip()
    prices = soup.find('div', {'class': 'price-wrapper-info price-wrapper--large'})
    try:
        price  = prices.find('span', {'class': 'price-wrapper'}).text.replace('ر.س', '').strip()
        special_price = prices.find('span', {'class': 'color-danger'}).text.replace('ر.س', '').strip()
    except:
        price = prices.find('span').text.replace('ر.س', '').strip()
        special_price = ''
    try:
        sku = soup.find('div', {'class': 'list--table-view__cell value text-unicode'}).text.strip()
    except:
        sku = ''
    description = soup.find('article', {'class': 'article article--main article--product-details mb-50'}).text.strip()
    images = soup.find('div', {'id': 'product_main_slider'}).find_all('img')
    list_images = [img['data-splide-lazy'] for img in images]
    base_image = list_images[0]
    add_images = ','.join(list_images[1: ])
    cats = soup.find('section', {'class': 'breadcrumb'}).find_all('a')

    cat1 = cats[1].text.strip()
    try:
        cat2 = cats[2].text.strip()
    except:
        cat2 = ''
    
    data = {
        'sku': sku,
        'name': name,
        'price': price,
        'special_price': special_price,
        'link_url': url,
        'description': description,
        'base_image': base_image,
        'add_images': add_images,
        'cat1': cat1,
        'cat2': cat2,
    }
    return data
df = pd.read_excel('spring_model1.xlsx')
for i, url in enumerate(list_urls):
    print('Count: ', i)
    data = extract_data(url)
    df1 = pd.DataFrame([data])
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('spring_product_update2.xlsx')
    