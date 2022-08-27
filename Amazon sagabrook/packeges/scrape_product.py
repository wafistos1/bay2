import pandas as pd
import numpy as np
import re
from requests_html import HTMLSession
from bs4 import BeautifulSoup

import requests
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
import time
import os
from fake_useragent import UserAgent
import random


def scrape_product(toto):
    # create selenium driver
    options = Options()
    ua = UserAgent()
    userAgent = ua.random
    # print(userAgent)
    options.add_argument(f'user-agent={userAgent}')
    options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_options=options)


    # df = pd.read_excel('Segabrook_model.xlsx')
    # tata = []
    # df1 = pd.read_excel('/home/wafistos/Documents/Projects/scaping_wafi/Amazon sagabrook/packeges/Segabrook_urls_product.xlsx')
    # for index, row in df1.iterrows():
    #     tata.append({'url': row['url'], 'cat1': row['cat1'], 'cat2': row['cat2']})
    # for i, toto in enumerate(tata[:200]):
    # print('Count:', i)
    print('URL:', toto['url'])
    driver.get(toto['url'])
    time.sleep(0.5)

    
    # driver.get('https://www.amazon.com/Sagebrook-Home-11582-Bookshelf-Inches/dp/B01MSVSBUB?ref_=ast_sto_dp')
    

    name = driver.find_element_by_id('productTitle').text.strip()
    try:
        price = driver.find_element_by_id('priceblock_ourprice').text.replace('$', '').strip()
    except:
        price = ''
    is_in_stock = driver.find_element_by_id('availability').text.strip()
        # print(is_in_stock)
    try:
        details = driver.find_element_by_id('productDetails_techSpec_section_1').get_attribute('innerHTML')
    except:
        details = driver.find_element_by_id('productDetails_detailBullets_sections1').get_attribute('innerHTML')
        
    soup = BeautifulSoup(details, 'html.parser')
    sku = soup.find(text=re.compile('Item model number')).parent.parent.find('td').text.replace('\u200e', '').strip()


    try:
        raw_material = soup.find(text=re.compile('Material')).parent.parent.find('td').text.replace('\u200e', '').strip()
    except:
        raw_material = ''
    """******************************************
    """
    details2 =driver.find_element_by_id('productOverview_feature_div').get_attribute('innerHTML')
    soup2 = BeautifulSoup(details2, 'html.parser')
    try:
        mgs_brand = soup2.find(text=re.compile('Brand')).parent.parent.parent.find_all('span')[1].text.strip()
        
    except:
        mgs_brand = ''
    if raw_material == '':
        # print('raw material null')
        try:
            raw_material = soup2.find(text=re.compile('Material')).parent.parent.parent.find_all('span')[1].text.strip()

        except:
            pass
    try:
        
        free_colors = soup2.find(text=re.compile('Color')).parent.parent.parent.find_all('span')[1].text.strip()
    except:
        free_colors = ''
    short_description = driver.find_element_by_id('productDescription').text.strip()
    description = driver.find_element_by_id('feature-bullets').text.replace('See more product details', '').replace('\n', '').strip()

    try:
        weight = soup.find(text=re.compile('Item Weight')).parent.parent.find('td').text.replace('\u200e', '').strip()
    except:
        weight = ''
    try:    
        manufacturer  = soup.find(text=re.compile('Manufacturer')).parent.parent.find('td').text.replace('\u200e', '').strip()
    except:
        manufacturer = ''
    try:
        dimension = soup.find(text=re.compile('Product Dimensions')).parent.parent.find('td').text.strip()
    except:
        dimension = ''

    # Scrape images 
    images_driver = driver.find_element_by_id('imageBlock').get_attribute('innerHTML')
    sp = BeautifulSoup(images_driver, 'html.parser')
    images = sp.find_all(src=re.compile(r"https://m.media-amazon.com/images/I/(?P<product_id>[\w-]+)"))
    regex = re.compile(r"https://m.media-amazon.com/images/I/(?P<product_id>.+)")
    list_images = []
    for img in images:
        url = img['src']
        match = regex.match(url)

        if match != None:
            # print(url)
            titi = match['product_id'].split('.')[0]

            list_images.append('https://m.media-amazon.com/images/I/'+titi + '._AC_SS450_.jpg')

    # print('Len images',len(list_images))
    base_image = list_images[0]
    additional_image = ",".join(list_images)
    data = {
        'sku': sku,
        'store_view_code': '',
        'attribute_set_code': '',
        'product_websites': '',
        'product_type': '',
        'name': name,
        'description': description,
        'short_description': short_description,
        'url_key': '',
        'link_url': toto['url'],
        'cost': '',
        'price': price,
        'special_price': '',
        'categories1': toto['cat1'],
        'categories2': toto['cat2'],
        'categories3': '',
        'categories': '',
        'free_colors': free_colors,
        'raw_materials':  raw_material,
        'weight': weight,
        'mgs_brand': mgs_brand,
        'product_size': dimension,
        'base_image': base_image,
        'small_image': base_image,
        'swatch_image': base_image,
        'thumbnail_image': base_image,
        'additional_images': additional_image,
        'is_in_stock': is_in_stock,
        'product_online': '',
        'qty': '',
        'out_of_stock_qty': '',
        'allow_backorders': '',
        'visibility': '',
        'tax_class_name': '',
        'manufacturer': manufacturer,
        'news_from_date': '',
        'news_to_date': '',
        'estimated_delivery_enable': '',
        'estimated_delivery_text': '',
        'supplier': '',

    }
    df2 = pd.DataFrame(data,  index=[0])
    # df = pd.concat([df, df2], ignore_index=True)
    # df.to_excel('Segabrook_urls_product_amazon.xlsx')
    driver.quit()
    return df2
    print(f'Scrap url product done with {len(data)} products')