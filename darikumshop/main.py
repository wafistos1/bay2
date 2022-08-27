
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


def returnt_ele(name, soup):
    try:
        return soup.find('p', text=re.compile(f'^{name}')).text.replace(':', '').replace(name, '').replace("\xa0", ' ').strip()
    except:
        return ''

name_excel = 'Darikumshop_url_update1.xlsx'
options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')
#opti#     driver = webdriver.Firefox()ons.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)

urls_df = pd.read_excel('/home/wafistos/Documents/Projects/scaping_wafi/darikumshop/Darikumshop_url_update.xlsx')
urls = []
for index, row in urls_df.iterrows():
    urls.append({'url': row['url'], 'cat1': row['cat1'], 'cat2': row['cat2'], 'cat3': row['cat3']})

def return_data(driver, url1):
    url = url1['url']
    cat1 = url1['cat1']
    cat2 = url1['cat2']
    cat3 = url1['cat3']
    r = driver.find_element_by_tag_name('body').get_attribute('innerHTML')
    soup = BeautifulSoup(r, 'html.parser')
    name = soup.find('h1', {'class': 'product-details__title'}).text.strip()
    price = soup.find('span', {'class': 'product-price'}).text.replace('ر.س', '').replace(',', '').strip()
    description = soup.find('div', {'class': 'product-detials__desc'}).text.strip()
    manufacturer = returnt_ele('بلد الصنع', soup)
    product_size = returnt_ele('المقاس', soup)
    raw_material = returnt_ele('المادة', soup)
    time.sleep(2)
    images = soup.find('img', {'class': 'image_first_click product-details__thumb'})['src']
    
    base_images = images
    add_images = ''
    sku = ''
    data  = {
        'sku': sku,
        'name': name,
        'link_url': url,
        'price': price,
        'description': description,
        'manufacturer': manufacturer,
        'product_size': product_size,
        'raw_material': raw_material,
        'base_images': base_images,
        'add_images': add_images,
        'cat1': cat1,
        'cat2': cat2,
        'cat3': cat3
    }
    return data

df = pd.read_excel('/home/wafistos/Documents/Projects/scaping_wafi/darikumshop/Darikumshop_model_product.xlsx')

for i, url1 in enumerate(urls):
    print('Count: ', i)
    url = url1['url']
    print('URL: ', url)
    cat1 = url1['cat1']
    cat2 = url1['cat2']
    cat3 = url1['cat3']
    driver.get(url)
    time.sleep(2)
    sizes = driver.find_elements_by_xpath('//ul[@class="dropdown-menu inner"]//li')
    print('LEN: ', len(sizes))
    if len(sizes) >= 1:
        for i in range(1, len(sizes)):
            try:
                driver.find_element_by_xpath('//span[@class="caret"]').click()
                time.sleep(2)
                driver.find_element_by_xpath(f'//li[@data-original-index="{i}"]').click()
                try:
                    data = return_data(driver, url1)
                except:
                    continue
                df1 = pd.DataFrame([data])
                df = pd.concat([df, df1], ignore_index=True)
                df.to_excel(name_excel)
            except:
                continue
    else:
        time.sleep(2)
        try:
            data = return_data(driver, url1)
        except:
            continue
        df1 = pd.DataFrame([data])
        df = pd.concat([df, df1], ignore_index=True)
        df.to_excel(name_excel)