
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

options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')
#opti#     driver = webdriver.Firefox()ons.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)

urls = pd.read_excel('dimlaj_update_url.xlsx')
list_urls = []

for indx, row in urls.iterrows():
    list_urls.append(
        {'url': row['url'], 'cat1': row['cat1'], 'cat2': row['cat2'], 'cat3': row['cat3']},
    )
def repalce_ele(name, dimensions):
    try:
        for dim in dimensions:
            if name in dim:
                return dim.replace(name, '').strip()
        
    except:
        return ''

def return_spec(name, soup):
    try:
        return soup.find('strong', text=re.compile(name)).next_element.next_element.strip()
    except:
        return ''

def extract_data(driver, url1):

    print('URL', url1)
    driver.get(url1)
    time.sleep(2)
    # click correct currency
    click_1 = driver.find_element_by_xpath('//div[@class="nt_currency pr cg currencies wsn dib  cur_stt_0"]').click()
    click_currency = driver.find_element_by_xpath('//a[@data-currency="SAR"]')
    time.sleep(1)
    click_currency.click()
    # refresh page
    time.sleep(1)
    r = driver.find_element_by_tag_name('body').get_attribute('innerHTML')
    soup = BeautifulSoup(r, "html.parser")
    # data 
    name = soup.find('h1', {'class': 'product_title entry-title'}).text.strip()
    price = soup.find('span', {'class','money'}).text.strip()
    sku = soup.find('span', {'id': 'pr_sku_ppr'}).text.strip()
    vendor = soup.find('span', {'id': 'product-vendor_ppr'}).text.strip()
    is_in_stock = soup.find('span', {'class': 'js_in_stock'}).text.strip()
    try:
        description = soup.find('div', {'class': 'sp-tab-content'}).find('p').text.strip()
    except:
        description = ''        
    brand = return_spec('Brand:', soup)
    precious_materials = return_spec('Precious Materials:', soup)
    raw_materials = return_spec('Material:', soup)
    weight = return_spec('Weight:', soup)
    collection = return_spec('Collection:', soup)
    number_of_pieces = return_spec('No. of Pcs:', soup)
    packing_type = return_spec('Packing Type:', soup)
    try:
        dimensions = soup.find('strong', text=re.compile('Dimensions')).next_element.next_element.text.split(',')
    except:
        dimensions = ''
    diameter = repalce_ele('Diameter:', dimensions)
    height = repalce_ele('Height:', dimensions)
    width = repalce_ele('Width:', dimensions)
    length = repalce_ele('Length:', dimensions)
    capacity_ = repalce_ele(': Capacity:', dimensions)

    
    # images
    images = soup.find_all('span', {'class': 'nt_bg_lz lazyloaded'})
    
    list_images = []
    for img in images:
        list_images.append(str(re.findall(r'(https?://\S+)', img['style'])).replace("['", '').replace("']", '').replace(';', '').replace(')', '').replace('_180x.jpg', '.jpg').replace('"', ''))
    list_images
    base_image = list_images[0]
    add_images = ','.join(list_images[1:])
    
    data = {
        'name': name,
        'price': price,
        'sku': sku,
        'link_url': url,
        'vendor': vendor,
        'is_in_stock': is_in_stock,
        'description': description,
        'brand': brand,
        'precious_materials': precious_materials,
        'raw_materials': raw_materials,
        'diameter': diameter,
        'height': height,
        'width': width,
        'length': length,
        'capacity_': capacity_,
        'weight': weight,
        'collection': collection,
        'number_of_pieces': number_of_pieces,
        'packing_type': packing_type,
        'base_image': base_image,
        'add_images': add_images,
    }
    
    return data


df = pd.read_excel('dimlaj_product_model.xlsx')

for i, url1 in enumerate(list_urls[114: ]):
    print('Count: ', i)
    
    url = url1['url']
    cat1 = url1['cat1']
    cat2 = url1['cat2']
    cat3 = url1['cat3']
    try:
        data = extract_data(driver, url)
    except:
        continue
    df1 = pd.DataFrame([data])
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('dimlaj_product_update_all1.xlsx')