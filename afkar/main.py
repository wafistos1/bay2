
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
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

def extract_ele(name, soup):
    try:
        return soup.find('strong', text=re.compile(name)).next_element.next_element.strip()
    except:
        return ''

def select_text(text):
    soup = BeautifulSoup(text, 'html.parser')
    return soup.find('input')['data-field_value']

def scrap_data(driver,url1, t=None):
    time.sleep(2)
    url = url1['url']
    cat1 = url1['cat1']
    cat2 = url1['cat2']
    cat3 = url1['cat3']
    r = driver.find_element_by_tag_name('body').get_attribute('innerHTML')
    soup = BeautifulSoup(r, 'html.parser')
    # Details
    name = soup.find('h1', {'class': 'product-details__title'}).text.strip()
    try:
        details = soup.find('h4', {'class': 'product-details__subtitle'}).text.strip()
    except:
        details = soup.find('div', {'class': 'product-detials__desc'}).text.strip()
    try:
        price = soup.find('span', {'class': 'price-before'}).text.strip()
    except:
        
        price = soup.find('span', {'class': 'product-price'}).text.strip()
    try:
        special_price = soup.find('span', {'class': 'price-after'}).text.strip()
    except:
        special_price = ''
    description = soup.find('div', {'class': 'product-detials__desc'}).text.strip()
    raw_materials = extract_ele('مادة الصنع', soup)
    qualite_materials = extract_ele('جودة المواد', soup)
    color_exter_cadre = extract_ele('لون الاطار الخارجي', soup)
    try:
        product_size = soup.find('strong', text=re.compile('المقاسات')).next_element.next_element.text.strip()
    except:
        product_size = ''
    
    type_ = t
    data = {
        'name': name,
        'link_url': url,
        'details': details,
        'price': price,
        'special_price': special_price,
        'description': description,
        'raw_materials': raw_materials,
        'qualite_materials': qualite_materials,
        'color_exter_cadre': color_exter_cadre,
        'product_size': product_size,
        'type_': type_,
        'cat1': cat1,
        'cat2': cat2,
        'cat3': cat3,
    }
    time.sleep(2)
    return data

# Open Firefox
options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')
#opti#     driver = webdriver.Firefox()ons.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)

list_product  = pd.read_excel('/home/wafistos/Documents/Projects/scaping_wafi/afkar/afkar_url_update.xlsx')
list_to_products = []

for index, row in list_product.iterrows():
    list_to_products.append( {'url': row['url'], 'cat1': row['cat1'], 'cat2': row['cat2'], 'cat3': row['cat3'] } , )
    
    
df = pd.read_excel('afkar_product_model.xlsx')
for i, url in enumerate(list_to_products):
    print('Count: ', i)
    driver.get(url['url'])
    try:
        time.sleep(2)
        logging.info('Je suis dans le try')
        selected_btn_up = driver.find_element_by_xpath('//span[@class="filter-option pull-left"]')
        selected_btn_down = driver.find_element_by_xpath('//button[@class="btn dropdown-toggle btn-default"]')
        selected_btn_up.click()
        
        # selected_price_size = driver.find_elements_by_xpath('//span[@class="text"]')# All choices اختر مايناسبك ليظهر لك المقاسات والأسعار 
        find_all_product = driver.find_elements_by_xpath('//ul[@class="dropdown-menu inner"]//li')
        print(len(find_all_product))
        list_toto = []
        for t in find_all_product:
            if t.text:
                list_toto.append(t.text)
        print('list: ', list_toto)
        for product in list_toto:#  main forloop
            driver.find_element_by_xpath(f'//span[contains(text(),"{product}")]').click()# First foorloop select المقاسات والأسعا
            time.sleep(1)
            select_input_size = driver.find_elements_by_xpath('//div[@class="checker border-info-600 text-info-800"]')
            for ckeck in select_input_size:#  forloop of peintures
                time.sleep(3)
                ckeck.click()# Show
                type_ =  select_text(ckeck.get_attribute('innerHTML'))
                data = scrap_data(driver, url, type_)
                df1 = pd.DataFrame([data])
                df = pd.concat([df, df1], ignore_index=True)
                df.to_excel('afkar_product_update.xlsx')
                time.sleep(2)
                ckeck.click()# Unshow
            selected_btn_down = driver.find_element_by_xpath('//button[@class="btn dropdown-toggle btn-default"]')
            selected_btn_down.click()
    except:
        logging.info('Je suis dans le except')
        
        data = scrap_data(driver, url)
        df1 = pd.DataFrame([data])
        df = pd.concat([df, df1], ignore_index=True)
        df.to_excel('afkar_product_update.xlsx')
