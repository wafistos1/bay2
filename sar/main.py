
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


name_excel = 'sar99_product_update.xlsx'
options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')
#opti#     driver = webdriver.Firefox()ons.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)

urls_df = pd.read_excel('sar_url_update.xlsx')

urls = []

for ind, row in urls_df.iterrows():
    urls.append(
        {'url': row['url'], 'cat1': row['cat1'],  'cat2': row['cat2'],  'cat3': row['cat3' ]},
    )

def return_ele(text, soup):
    try:
        return soup.find('li', text=re.compile(f'^{text}')).text.replace(text, '').strip()
        
    except:
        return ''

def return_attribute(text, soup):
    try:
        return soup.find('span', text=re.compile(f'^{text}')).text.replace(text, '').strip()
        
    except:
        return ''


def extract_data(url1, driver):
    url = url1['url']
    cat1 = url1['cat1']
    cat2 = url1['cat2']
    cat3 = url1['cat3']
    print('URL: ', url)
    driver.get(url)
    r = driver.find_element_by_tag_name('body').get_attribute('innerHTML')
    soup = BeautifulSoup(r, 'html.parser')
    name = soup.find('h1').text.strip()
    type_ = return_ele('النوع :', soup)
    is_in_stock = return_ele('حالة التوفر :', soup)
    price = soup.find('ul', {'class': 'list-unstyled price-pro'}).find('h3').text.replace('ريال سعودي', '').strip()
    description = soup.find('div', {'id': 'tab-description'}).text.strip()
    depth = return_attribute('العمق:', soup).replace('سم-', '').strip()
    width = return_attribute('العرض:', soup).replace('سم-', '').strip()
    height = return_attribute('الارتفاع:', soup).replace('سم-', '').strip()
    images = soup.find('div', {'class': 'slick-track'}).find_all('img')
    len(images)
    regex = re.compile(r'-(?P<length>\d*\.?\d*)x(?P<height>\d*\.?\d*).jpg')
    list_images = []
    for img in images:
        p = re.search(regex, img['src'])
        if p != None:
            list_images.append(img['src'].replace('/cache', '').replace(p[0], '.jpg'))
        else:
            list_images.append(img['src'].replace('/cache', ''))
    base_images = list_images[0]
    add_images = ','.join(list_images[1:])

    data = {
        'name':name,
        'link_url': url, 
        'type_':type_, 
        'is_in_stock':is_in_stock, 
        'price':price, 
        'description':description, 
        'depth':depth, 
        'width':width, 
        'height':height, 
        'base_image':base_images, 
        'add_images':add_images,
        'cat1': cat1,
        'cat2': cat2,
        'cat3': cat3,
    }
    return data

df = pd.read_excel('sar_product_model.xlsx')

for i, url in enumerate(urls):
    print('Count: ', i)

    try:
        data = extract_data(url, driver)
    except:
        continue

    df1 = pd.DataFrame([data])
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel(name_excel)



