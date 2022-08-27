
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

# options = Options()
# ua = UserAgent()
# userAgent = ua.random
# print(userAgent)
# options.add_argument(f'user-agent={userAgent}')
# #opti#     driver = webdriver.Firefox()ons.add_argument("--headless")
# driver = webdriver.Firefox(firefox_options=options)

urls = pd.read_excel('tanatel_update_url.xlsx')
list_urls = []

for indx, row in urls.iterrows():
    list_urls.append(
        {'url': row['url'], 'cat1': row['cat1'], 'cat2': row['cat2'], 'cat3': row['cat3']},
    )

def return_ele(name, soup):
    try:
        return soup.find('span', text=re.compile(f'{name}')).text.replace(name, '').replace(':', '').replace('-', '').strip()

    except:
        return ''


def extract_data(url1):

    url = url1['url']
    cat1 = url1['cat1']
    cat2 = url1['cat2']
    cat3 = url1['cat3']
    print('URL: ', url)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    cookies = {'session': '134-8225175-0355220'}
    r = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(r.content, "html.parser")
    
    # DATA
    
    name = soup.find('div', {'class': 'productpage-head'}).find('h1').text.strip()
    try:
        price = soup.find('ul', {'class': 'list-unstyled list-inline prodprices'}).find('h3', {'class': 'old-price'}).text.strip()
        special_price = soup.find('ul', {'class': 'list-unstyled list-inline prodprices'}).find('h2').text.strip()
    except:
        price = soup.find('ul', {'class': 'list-unstyled list-inline prodprices'}).find('h2').text.strip()
        special_price = 0
    try:
        estimated_delivery_text = soup.find('span', text=re.compile('عدد ايام الشحن ')).next_element.next_element.replace('\t', '')
    except:
        estimated_delivery_text = ''
    try:
        is_in_stock = soup.find('span', text=re.compile('حالة التوفر ')).next_element.next_element.replace('\t', '')
    except:
        is_in_stock = ''
    images =[t.find('img')['src'].replace('80x80', '500x500') for t in  soup.find_all('a', {'class': 'thumbnail'})]
    base_image = images[0]
    add_images = ','.join(images[1: ])
    free_colors = return_ele('اللون', soup)
    base_ = return_ele('القاعدة', soup)
    style = return_ele('التصميم', soup)
    fabrics = return_ele('الأقمشة', soup)
    the_wood = return_ele('الخشب', soup)
    guarantee = return_ele('الضمان', soup)
    paint_quality = return_ele('الطلاء', soup)

    description = soup.find('div', {'class': 'tab-content proddtls'}).text.strip()
    products_size = []
    firstElem = soup.find('b', text=re.compile('الأبعاد'))
    if not firstElem:
        firstElem = soup.find('font', text=re.compile('الأبعاد'))
    if not firstElem:
        firstElem =  soup.find('', text=re.compile('الأبعاد'))
    lastElem = soup.find('div', {'id': 'tab-review'})
    p_tags = []
    next = firstElem.next_element
    while next != lastElem:   
        p_tags.append(next)
        next = next.next_element
        for t in p_tags:
            try:
                if t.text != '':
                    products_size.append(t.text.replace('\xa0', '').replace('*', '-').strip())
            except:
                continue
    products_size = list(dict.fromkeys(products_size))

    data = {
        'name': name,
        'link_url': url,
        'price': price, 
        'special_price': special_price, 
        'estimated_delivery_text': estimated_delivery_text, 
        'is_in_stock': is_in_stock, 
        'add_images': add_images, 
        'free_colors': free_colors, 
        'base_': base_, 
        'style': style, 
        'fabrics': fabrics, 
        'the_wood': the_wood, 
        'guarantee': guarantee, 
        'paint_quality': paint_quality, 
        'description': description, 
        'products_size': products_size,
        'base_image': base_image,
        'add_images': add_images,
        'cat1': cat1,
        'cat2': cat2,
        'cat3': cat3,
    }
    return data
df = pd.read_excel('tanatel_product_model.xlsx')

for i, url1 in enumerate(list_urls):
    print('Count: ', i)
    try:
        data = extract_data(url1)
    except:
        continue
    time.sleep(1)
    df1 = pd.DataFrame([data])
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('tanetel_product_update_all.xlsx')