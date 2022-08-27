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





def scrape_product_bs4(toto):
    # create selenium driver
    # options = Options()
    # ua = UserAgent()
    # userAgent = ua.random
    # # print(userAgent)
    # options.add_argument(f'user-agent={userAgent}')
    # options.add_argument("--headless")
    # driver = webdriver.Firefox(firefox_options=options)


    # df = pd.read_excel('Segabrook_model.xlsx')
    # tata = []
    # df1 = pd.read_excel('/home/wafistos/Documents/Projects/scaping_wafi/Amazon sagabrook/packeges/Segabrook_urls_product.xlsx')
    # for index, row in df1.iterrows():
    #     tata.append({'url': row['url'], 'cat1': row['cat1'], 'cat2': row['cat2']})
    # for i, toto in enumerate(tata[:200]):
    # print('Count:', i)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "DNT": "1",
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1",
    }


    # cookies = {'session': '134-8225175-0355220'}   
    # driver.get('https://www.amazon.com//Sagebrook-Home-12495-02-Metal-Accent/dp/B079DRDS3J?ref_=ast_sto_dp')
    # time.sleep(0.5)
    # r = requests.get('https://www.amazon.com//Sagebrook-Home-12495-02-Metal-Accent/dp/B079DRDS3J?ref_=ast_sto_dp', headers=headers, cookies=cookies)
    cookies = {'session': '134-8225175-0355220'}
    r = requests.get(toto['url'],
            headers=headers,
            cookies=cookies
        )
    soup = BeautifulSoup(r.content, "lxml")

    print('URL:', toto['url'])
    
    time.sleep(0.5)

    
    # driver.get('https://www.amazon.com/Sagebrook-Home-11582-Bookshelf-Inches/dp/B01MSVSBUB?ref_=ast_sto_dp')
    

    name = soup.find('span', {'id': 'productTitle'}).text.strip()
    try:
        price = soup.find('div',{'id':'priceblock_ourprice'}).text.replace('$', '').strip()
    except:
        price = ''
    is_in_stock = soup.find('div',{'id':'availability'}).text.strip()
  
        
    
    sku = soup.find(text=re.compile('Item model number')).parent.parent.find('td').text.replace('\u200e', '').strip()


    try:
        raw_material = soup.find(text=re.compile('Material')).parent.parent.find('td').text.replace('\u200e', '').strip()
    except:
        raw_material = ''
    """******************************************
    """
    
    
    try:
        mgs_brand = soup.find(text=re.compile('Brand')).parent.parent.parent.find_all('span')[1].text.strip()
        
    except:
        mgs_brand = ''
    if raw_material == '':
        # print('raw material null')
        try:
            raw_material = soup.find(text=re.compile('Material')).parent.parent.parent.find_all('span')[1].text.strip()

        except:
            pass
    try:
        
        free_colors = soup.find(text=re.compile('Color')).parent.parent.parent.find_all('span')[1].text.strip()
    except:
        free_colors = ''
    short_description = soup.find('div',{'id':'productDescription'}).text.strip()
    description = soup.find('div',{'id':'feature-bullets'}).text.replace('See more product details', '').replace('\n', '').strip()

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
    images_driver = soup.find('div',{'id':'imageBlock'})
    
    images = soup.find_all(src=re.compile(r"https://m.media-amazon.com/images/I/(?P<product_id>[\w-]+)"))
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
    
    return df2
     
