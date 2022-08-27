import pandas as pd
import numpy as np
import re
from datetime import datetime, time
from datetime import timedelta
from bs4 import BeautifulSoup
from .scrape_cat import PROXY_LIST
import requests
import time


# https://htttpbin.org/ip --- > r.json() ---> return ip of proxy 
def scrape_product(toto):
    print("URL:", toto['url'])
    for tt in PROXY_LIST:     
        try:
            r = requests.get(toto['url'], proxies={'http': tt, 'https': tt}, timeout=10 )
            if r.status_code == 200:
                print(r.status_code)
                break
        except:
            pass
    manufacturer = ''
    soup  = BeautifulSoup(r.text, 'html.parser')
    #soup.find('', {'': ''}).text.strip()
    sku = soup.find('span', {'class': 'sku'}).text.strip()
    name = soup.find('h1', {'class': 'product_title entry-title'}).text.strip()
    prices = soup.find('p', {'class': 'price'})
    print('len', len(prices))
    price = prices.text.split('ر.س')[1].strip()
    try:
        special_price = prices.text.split('ر.س')[2].strip()
    except:
        special_price = ''

    list_images = []
    
    images_papa = soup.find_all('div', {'class': 'woocommerce-product-gallery__image'})
    print('len images', len(images_papa))
    for tt in images_papa:
        list_images.append(tt.find('a')['href'].split('?')[0])
    
    base_image = list_images[0]
    try:
        additional_image = ','.join(list_images[1:])
    except:
        additional_image = ''

    try:
        description = soup.find('div', {'class': 'woocommerce-product-details__short-description'}).text.strip()
    except:
        description = ''
    try:
        short_description = soup.find('div', {'id': 'tab-description'}).text
    except:
        short_description = description
    is_in_stock = ''
    try:
        out_of_qty = soup.find('p', {'class': 'stock in-stock'}).text.replace('Status:', '').strip()
    except:
        out_of_qty = soup.find('p', {'class': 'stock out-of-stock'}).text.replace('Status:', '').strip()
    try:
        mgs_brand = soup.find('li', {'class': 'meta-brand'}).text.strip()
    except:
        mgs_brand = ''
    try:
        details = soup.find('div', {'id': 'tab-description'}).text
        details1 =details.split('\n')
        free_colors = [toto.replace('اللون', '').replace(':', '').strip() for toto in details1 if 'اللون' in toto][0]
        
        manufacturer = [toto.replace('صنع في', '').replace(':', '').strip() for toto in details1 if 'صنع في' in toto][0]
    except:
        details1 =description.split('\n')
        try:
            manufacturer = [toto.replace('صنع في', '').replace(':', '').strip() for toto in details1 if 'صنع في' in toto][0]
        except:
            manufacturer = ''
        try:
            free_colors = [toto.replace('اللون', '').replace(':', '').strip() for toto in details1 if 'اللون' in toto][0]
        except:
            free_colors = ''
            
    # print(details1)
    dimension = soup.find_all('td', {'class': 'woocommerce-product-attributes-item__value'})
    
    print('len dimension', len(dimension))
    weight = ''
    product_size = ''
    
    for dim in dimension:
        if 'kg' in dim.text:
            weight = dim.text.replace('kg', '').strip()
        elif 'cm' in dim.text:
            product_size = dim.text.replace('cm', '').strip()
    
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
        'special_price': special_price,
        'categories1': toto['cat1'],
        'categories2': toto['cat2'],
        'categories3': toto['cat3'],
        'categories': '',
        'free_colors': free_colors,
        'raw_materials': '',
        'weight': weight,
        'mgs_brand': mgs_brand,
        'product_size': product_size,
        'base_image': base_image,
        'small_image': base_image,
        'swatch_image': base_image,
        'thumbnail_image': base_image,
        'additional_images': additional_image,
        'is_in_stock': '',
        'product_online': '',
        'qty': '',
        'out_of_stock_qty': out_of_qty,
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
    return data