import time
import os
from fake_useragent import UserAgent
from random import randint
import pandas as pd
import numpy as np
import requests
import pandas as pd
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
import logging
logging.basicConfig( level=logging.INFO)


def extract_ele(name, soup):
    try:
        search = f'^{name}'
        return soup.find('li', text=re.compile(r'^{}'.format(name))).text.replace(name, '').replace(':', '').strip()
        
    except:
        return ''

urls = pd.read_excel('fanos_url_update.xlsx')
list_urls = []

for indx, row in urls.iterrows():
    list_urls.append(
        {'url': row['url'], 'cat1': row['cat1'], 'cat2': row['cat2'], 'cat3': row['cat3']},
    )


def extract_data(url1):
    url = url1['url']
    cat1 = url1['cat1']
    cat2 = url1['cat2']
    cat3 = url1['cat3']
    #print('URL: ', url)
    logging.info('URL: %s', url)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    cookies = {'session': '134-8225175-0355220'}
    r = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(r.content, "html.parser")
    time.sleep(1)
    try:
        sku = soup.find('div', {'class': 'list--table-view__cell value text-unicode'}).text.strip()
    except:
        sku = ''
    try:
        name = soup.find('h1', {'class': 'title title--xx-large mb-10'}).text.strip()
    except:
        name = soup.find('h1', {'class': 'title title--xx-large mb-0'}).text.strip()
    
    price = soup.find('div', {'class': 'price-wrapper-info price-wrapper--large'}).find('span').text.strip()
    try:
        short_description = soup.find('article', {'class': 'article article--main article--product-details mb-50'}).find('p').text.strip()
    except:
        short_description = ''
    description = soup.find('article', {'class': 'article article--main article--product-details mb-50'}).text.strip()

    size = extract_ele('الأبعاد', soup)
    volt = extract_ele('الفولت', soup)
    form = extract_ele('الشكل', soup)
    light_type = extract_ele('نوع الإنارة', soup)
    product_size = extract_ele('المقاس', soup)
    free_colors = extract_ele('اللون', soup)
    number_s = extract_ele('عدد اللمبات', soup)
    fonction = extract_ele('الاستخدام', soup)
    duration = extract_ele('العمر الافتراضي', soup)
    elec_power = extract_ele('الجهد الكهربائي', soup)
    light_power = extract_ele('قوة الضوء', soup)
    watt_consumption = extract_ele('استهلاك الكهرباء', soup)
    electricity = extract_ele('القدرة الكهربائية', soup)
    color_temperature = extract_ele('درجة حرارة اللون', soup)
    raw_materials = extract_ele('المواد المصنعة', soup)
    if raw_materials == '':
        raw_materials = extract_ele('مادة التصنيع', soup)
    images = soup.find_all('a', {'data-fancybox': 'product-details'})
    len(images)
    list_images = [img['href'] for img in images]
    base_images = list_images[0]
    add_images = ','.join(list_images[1: ])
    data = {
        'sku': sku,
        'name': name,
        'price': price,
        'link_url': url,
        'short_description': short_description,
        'description': description,
        'size': size,
        'light_power': light_power,
        'watt_consumption': watt_consumption,
        'volt': volt,
        'form': form,
        'light_type': light_type,
        'product_size': product_size,
        'free_colors': free_colors,
        'number_s': number_s,
        'fonction': fonction,
        'duration': duration,
        'elec_power': elec_power,
        'electricity': electricity,
        'color_temperature': color_temperature,
        'raw_materials': raw_materials,
        'base_images': base_images,
        'add_images': add_images,
        'cat1': cat1,
        'cat2': cat2,
        'cat3': cat3,
    }
    return data

logging.info('Sraping Strated..')
df = pd.read_excel('fanos_product_model.xlsx')
for i, url1 in enumerate(list_urls[2523: ]):
    #print('Count: ', i)
    #logging.warning('Count: ', i)  # will print a message to the console
    logging.info('Count: %s', i)
    data = extract_data(url1)
    df1 = pd.DataFrame([data])
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('fanos_product_update_test3.xlsx.xlsx')
logging.info('Sraping Done..')