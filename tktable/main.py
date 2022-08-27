

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



def scrap_products(urls, driver):
    url1 = urls['url']
    cat1 = urls['categories1']
    cat2 = urls['categories2']
    print('URL: ', url1)
    driver.get(url1)
    text = driver.find_element_by_tag_name('body').get_attribute('innerHTML')
    soup = BeautifulSoup(text, "html.parser")
    name = soup.find('h1', {'class': 'h2 space-bottom-half product-title'}).text.strip()
    price = soup.find('span', {'id': 'product-price'}).text.replace('ر.س', '').strip()
    sku = soup.find('div', {'class': 'product-sku'}).find('span').text.strip()
    try:
        wight = soup.find('strong', text='الوزن: ').next_sibling.next_sibling.text.strip()
    except:
        wight = ''
    list_images = []
    try:
        images = driver.find_elements_by_xpath('//div[@class="owl-stage-outer"]//div[@class="owl-item active"]')
        description = soup.find('div', {'id': 'description-tab'}).text.strip()
        len(images)
        for img in images:
            try:
                img.click()
                image = driver.find_element_by_xpath('//img[@id="main-img"]').get_attribute('src')
                list_images.append(image)
                time.sleep(1)
            except:
                pass
            
        base_image = list_images[0]
        additionnel_images = ','.join(list_images[1:])
    except:
        base_image = driver.find_element_by_xpath('//img[@id="main-img"]').get_attribute('src')
        additionnel_images = ''
    data = {
        'link_url': url1,
        'name': name,
        'sku': sku,
        'price': price,
        'wight': wight,
        'description': description,
        'base_image': base_image,
        'additionnel_images': additionnel_images,
        'categories1': cat1,
        'categories2': cat2,
        
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
urls = pd.read_excel('tktable_url1.xlsx')
list_urls = []
for index, row in urls.iterrows():
    list_urls.append(
        {
            'url': row['url'],
            'categories1': row['categories1'],
            'categories2': row['categories2'],
        }
    )
    
    
for i, url in enumerate(list_urls):
    print('Count: ', i)
    data = scrap_products(url, driver)
    df1 = pd.DataFrame([data])
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('tktable_product_update1.xlsx')