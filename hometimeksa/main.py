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
import re
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup
import requests


def extract_data(driver, cat1, cat2, cat3):
            text = driver.find_element_by_xpath('//div[@class="app d-flex flex-column visible"]').get_attribute('innerHTML')
            soup = BeautifulSoup(text, 'html.parser')
            sku =  soup.find('div', {'class': 'product-sku'}).text.strip()
            try:
                free_color = color.text.strip()
            except:
                free_color = ''
            
            name = soup.find('section').find('h1').text.strip()
            price = soup.find('del', {'class': 'product-formatted-price-old'}).text.replace('ر.س', '').strip()
            if price != '':
                special_price = soup.find('h1', {'class': 'product-formatted-price theme-text-primary'}).text.replace('ر.س', '').strip()
            else:
                price = soup.find('h1', {'class': 'product-formatted-price theme-text-primary'}).text.replace('ر.س', '').strip()
                special_price = ''
                
            try:
                qty = len(soup.find('select', {'id': 'product-quantity'}).find_all('option'))
            except:
                qty = '0'
            try:
                description = soup.find('div', {'class':'description-paragrah text-justify description-text-clear'}).text.replace('xa0', ' ').strip()
            except:
                description = ''
            images = soup.find('div', {'class': 'col-12 col-product-image-wrapper'}).find_all('img')
            
            list_images = [img['src'] for img in images if '770x770' in img['src']]

            ts_dimensions_height = return_element('الطول:', soup)
            diameter = return_element('القطر:', soup)
            base_size = return_element('قطر القاعدة:', soup)
            amper = return_element('حجم البطارية :', soup)
            rechargeable = return_element('مدة شحن المصباح :', soup)
            product_accessories = return_element('الملحقات :', soup)
            usage_time = return_element('وقت الاستخدام:', soup)
            try:
                ty = type_.text.strip()
            except:
                ty = ''  
            try:
                sz = sz.text.strip()
            except:
                sz = ''    
            data = {
                'sku': sku,
                'link_url': url,
                'name': name,
                'price': price,
                'special_price': special_price,
                'qty': qty,
                'free_colors': free_color,
                'ts_dimensions_height': ts_dimensions_height, 
                'diameter': diameter, 
                'base_size': base_size, 
                'amper': amper,
                'type_': ty,
                'size': sz,
                'rechargeable': rechargeable, 
                'product_accessories': product_accessories, 
                'usage_time': usage_time, 
                'description': description,
                'base_image': list_images[0],
                'additionnel_images': ','.join(list_images[1:]),
                'categories1': cat1,
                'categories2': cat2,
                'categories3': cat3,
            }
            return data

options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')
#options.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)
#     driver = webdriver.Firefox()
def return_element(name, soup):
    try:
        ele = soup.find('p', text=re.compile(f'{name}')).text.replace(name, '').strip()
    except:
        ele = None
    return ele

df = pd.read_excel('/home/wafistos/Documents/Projects/scaping_wafi/hometimeksa/Hometimeksa .product_model.xlsx')
toto = pd.read_excel('/home/wafistos/Documents/Projects/scaping_wafi/hometimeksa/Home_urls.xlsx')

df['categories'] = ''
list_urls = []
for index, row in toto.iterrows():
    list_urls.append({'url': row['url'],  'categories1': row['cat1'], 'categories2': row['cat2'], 'categories3': row['cat3'], })
   

two_month = datetime.now() + timedelta(days=60)
two_month = two_month.strftime("%m/%d/%Y")
today = datetime.today().strftime("%m/%d/%Y")
name_excel = 'Hometimeksa_test1.xlsx'



for i, url1 in enumerate(list_urls):
    print('Count: ', i)
    print('URL: ', url1['url'])
    
    url = url1['url']
    cat1 = url1['categories1']
    cat2 = url1['categories2']
    cat3 = url1['categories3']
    driver.get(url)
    list_colors = driver.find_elements_by_xpath('//ul[@name="اللون"]//li[@onclick="productOptionListItemClicked(event)"]')
    if len(list_colors) > 1:
    
        for color in list_colors:
            color.click()
            time.sleep(0.5)
            data = extract_data(driver, cat1, cat2, cat3)
            df1 = pd.DataFrame([data])
            df = pd.concat([df, df1], ignore_index=True)
            df.to_excel(name_excel)

    type_a = driver.find_elements_by_xpath('//ul[@name="الصنف"]//li[@onclick="productOptionListItemClicked(event)"]')
    
    if len(type_a) > 1:
        for type_ in type_a:
            type_.click()
            time.sleep(0.5)
            data = extract_data(driver, cat1, cat2, cat3)
            df1 = pd.DataFrame([data])
            df = pd.concat([df, df1], ignore_index=True)
            df.to_excel(name_excel)
    size = driver.find_elements_by_xpath('//ul[@name="الحجم "]//li[@onclick="productOptionListItemClicked(event)"]')
    
    if len(size) > 1:
        for sz in size:
            sz.click()
            time.sleep(0.5)
            data = extract_data(driver, cat1, cat2, cat3)
            df1 = pd.DataFrame([data])
            df = pd.concat([df, df1], ignore_index=True)
            df.to_excel(name_excel)
    else:
        data = extract_data(driver, cat1, cat2, cat3)
        df1 = pd.DataFrame([data])
        df = pd.concat([df, df1], ignore_index=True)
        df.to_excel(name_excel)    
    