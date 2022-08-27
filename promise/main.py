

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


def return_details(name, soup):
    try:
        elements = soup.find_all('li')
        for ele in elements:
            if name in ele.text:
                return ele.text.replace(name, '').replace(':', '').strip()
    except:
        return None   



def scrap_products(urls, driver):
    url = urls['url']
    cat1 = urls['categories1']
    cat2 = urls['categories2']
    cat3 = urls['categories3']
    driver.get(url)
    time.sleep(2)
    try:
        driver.find_element_by_class_name('pd-expand-wrapper').click()
    except:
        pass
    text = driver.find_element_by_tag_name('body').get_attribute('innerHTML')
    soup = BeautifulSoup(text, "html.parser")
    try:
        sku = soup.find('span', text=re.compile('رقم الموديل')).next_element.next_element.next_element.next_element.text.strip()
    except:
        sku = ''
    name = soup.find('h1', {'class':'product-details__title brand-title'}).text.strip()
    try:
        price = soup.find('span', {'price-before'}).text.replace('ر.س', '').strip()
        special_price = soup.find('span', {'price-after'}).text.replace('ر.س', '').strip()
    except:
        price = soup.find('span', {'class': 'product-price'}).text.replace('ر.س', '').strip()
        special_price = ''
    description = soup.find('div', {'class': 'product-detials__desc'}).text.strip()
    images = soup.find('div', {'id': 'sp-slider-cont'}).find_all('img')
    len(images)
    list_images = [img['src'] for img in images]
    cats = soup.find('ol', {'class': 'breadcrumb'}).find_all('li')
    len(cats)

    details = soup.find('div', {'class': 'product-detials__desc pd-exp expanded'})
    
    if details == None:
        details = soup.find('div', {'class': 'product-detials__desc'})
    manufacturer = return_details('بلد الصنع', details)
    type_1 = return_details('نوع القماش', details)
    type_2 = return_details('نوع الحشوة', details)
    number_pieces = return_details('عدد القطع', details)
    free_colors = return_details('اللون', details)
    try:
        washing_instruction = details.find('strong', text=re.compile(r'إرشادات الغسيل :')).next_element.next_element.text.strip()
    except:
        washing_instruction = ''
    try:
        product_size = details.find('p', text=re.compile('^الطول')).text.strip()
    except:
        product_size = ''
    data = {
        'sku': sku,
        'link_url': url,
        'name': name,
        'price': price,
        'special_price': special_price,
        'description': description,
        'images': list_images,
        'categories1': cat1,
        'categories2': cat2,
        'categories3': cat3,
        'manufacturer': manufacturer,
        'Type_1': type_1,
        'Type_2': type_2,
        'number_pieces': number_pieces,
        'washing_instruction': washing_instruction,
        'free_colors': free_colors,
        'product_size': product_size,
    }
    return data

options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')
#opti#     driver = webdriver.Firefox()ons.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)

df = pd.read_excel('model_product.xlsx')
urls = pd.read_excel('/home/wafistos/Documents/Projects/scaping_wafi/promise/Promise_url.xlsx')
list_urls = []
for index, row in urls.iterrows():
    list_urls.append(
        {
            'url': row['url'],
            'categories1': row['categories1'],
            'categories2': row['categories2'],
            'categories3': row['categories3'],
        }
    )

for i, url in enumerate(list_urls):
    print('Count: ', i)
    print('URL: ', url['url'])
    data = scrap_products(url, driver)
    df1 = pd.DataFrame(data)
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('Promise_product_update-05-04.xlsx')

