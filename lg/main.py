
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

def return_spec(name, soup):
    try:
        return soup.find('dt', text=re.compile(name)).parent.find('dd').text.strip()
    except:
        return ''


def return_ele(name, soup):
    print('Name : ', name)
    try:
        return soup.find('li', text=re.compile(f'^{name}')).text.replace(name, '').strip()
    except:
        return ''

# urls = pd.read_excel('lg_update_url2.xlsx')
urls = pd.read_excel('lg_update_url_frigo.xlsx') # Tvs
list_urls = []

for indx, row in urls.iterrows():
    list_urls.append(
        {'url': row['url'], 'cat1': row['cat1'], 'cat2': row['cat2'], 'cat3': row['cat3']},
    )

def return_data(driver, url1):
    url = url1['url']
    cat1 = url1['cat1']
    cat2 = url1['cat2']
    cat3 = url1['cat3']
    print('URL: ', url)
    
    driver.get(url)
    r = driver.find_element_by_tag_name('body').get_attribute('innerHTML')
    soup = BeautifulSoup(r, "html.parser")
    name = soup.find('h1', {'class': 'model-title'}).text.strip()
    sku = soup.find('div', {'model-name'}).text.strip()
    description = soup.find('div', {'class': 'feature-area'}).text.strip()

    garante = return_ele('ضمان', soup)
    capacite = return_spec('السعة', soup)
    add_benefits = return_spec('المزايا الإضافية', soup)
    products_size = return_spec('الأبعاد', soup)
    wifi = return_spec('التقنية الرئيسية', soup)
    tv_size = return_spec('حجم الشاشة', soup)
    precision = return_spec('الدقة', soup)
    tech_1 = return_spec('التقنية الرئيسية', soup)

    
    try:
        link_price = soup.find('div', {'id': 'coljrfziuue'}).find('li', {'class': 'item slick-slide slick-current slick-active'}).find('a')['href']
    except:
        link_price = ''
    list_images = []
    
    try:
        images_btn = driver.find_element_by_xpath('//span[@class="count"]')
        images_btn.click()
        time.sleep(10)
        r = driver.find_element_by_tag_name('body').get_attribute('innerHTML')
        soup = BeautifulSoup(r, "html.parser")
    except:
        pass
    images = driver.find_elements_by_xpath('//div[@class="modal-body"]//img')
    len(images)
    for img in images:
        try:
            if 'https://www.lg.com/ae_ar/' in img.get_attribute('src'):
                list_images.append(img.get_attribute('src'))
        except:
            pass
    base_image = list_images[0]
    add_images = ','.join(list_images[1:])
    totos = soup.find('div', {'class': 'tech-spacs-contents'}).find_all('dt')
    # freeze = totos[1].parent.find('dd').text.strip()
    # chaleur = totos[3].parent.find('dd').text.strip()
    
    
    data = {
        'name': name,
        'link_url': url,
        'sku':sku,
        'link_price': link_price,
        'description':description,
        'guarante':garante,
        'capacite':capacite,
        'add_benefits':add_benefits,
        'products_size':products_size,
        'wifi':wifi,
        'precision': precision,
        'tv_size': tv_size,
        'tech_': tech_1,
        'freeze': '',
        'chaleur': '',
        'base_image':base_image,
        'add_images':add_images,
        'cat1': cat1,
        'cat2': cat2,
        'cat3': cat3,
    }
    
    return data


df = pd.read_excel('lg_product_model.xlsx')
for i, url in enumerate(list_urls):
    print('Count: ', i)
    try:
        data = return_data(driver, url)
    except:
        continue
    df1 = pd.DataFrame([data])
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('lg_update_product.frigo_data.xlsx')
    


