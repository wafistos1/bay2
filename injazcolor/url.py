import time
import os
import requests
import re
import logging
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
from fake_useragent import UserAgent
from random import randint
import pandas as pd
import numpy as np

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
# options = Options()
# ua = UserAgent()
# userAgent = ua.random
# logging.info(userAgent)
# options.add_argument(f'user-agent={userAgent}')
# #opti#     driver = webdriver.Firefox()ons.add_argument("--headless")
# driver = webdriver.Firefox(firefox_options=options)

# body=WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.TAG_NAME,'body')))
# r = body.get_attribute('innerHTML')
# soup = BeautifulSoup(r, "html.parser")

def get_data(url):
    logging.info('Url: %s', url)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    cookies = {'session': '134-8225175-0355220'}
    r = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(r.content, "html.parser")
    time.sleep(1)
    products = soup.find_all('div', {'class': 'product-grid-item'})
    
    liens = [product.find('a')['href'] for product in products]
    logging.info('Len products %s', len(liens))
    return soup, liens

def getnextpage(soup):
    page = soup.find('a', {'class': 'next'})
    
    try:
        url2 = str(page['href'])
        return url2
    except:
        logging.info('No Next')
        pass
    return url2 

list_urls = [
    {'cat1': 'Wall coverings', 'cat2': 'Wood alternative', 'cat3': '', 'url': 'https://injazcolor.com/en/product-category/wall-coverings/wood-alternative/'},
    {'cat1': 'Wall coverings', 'cat2': 'Marble alternative', 'cat3': '', 'url': 'https://injazcolor.com/en/product-category/wall-coverings/marble-alternative/'},
    {'cat1': 'Wall coverings', 'cat2': 'Mirrors', 'cat3': '', 'url': 'https://injazcolor.com/en/product-category/wall-coverings/mirrors/'},
    #
    {'cat1': 'Wallpaper', 'cat2': 'إيطالي', 'cat3': '', 'url': 'https://injazcolor.com/en/product-category/wallpaper/%d8%a5%d9%8a%d8%b7%d8%a7%d9%84%d9%8a/'},
    {'cat1': 'Wallpaper', 'cat2': 'Kids designs', 'cat3': '', 'url': 'https://injazcolor.com/en/product-category/wallpaper/kids-designs/'},
    {'cat1': 'Wallpaper', 'cat2': '3D designs', 'cat3': '', 'url': 'https://injazcolor.com/en/product-category/wallpaper/3d-designs/'},
    {'cat1': 'Wallpaper', 'cat2': 'Special designs', 'cat3': '', 'url': 'https://injazcolor.com/en/product-category/wallpaper/special-designs/'},
    {'cat1': 'Wallpaper', 'cat2': 'Oriental designs', 'cat3': '', 'url': 'https://injazcolor.com/en/product-category/wallpaper/oriental-designs/'},
    {'cat1': 'Wallpaper', 'cat2': 'Nature designs', 'cat3': '', 'url': 'https://injazcolor.com/en/product-category/wallpaper/nature-designs/'},
    {'cat1': 'Wallpaper', 'cat2': 'Hotel designs', 'cat3': '', 'url': 'https://injazcolor.com/en/product-category/wallpaper/hotel-designs/'},
    {'cat1': 'Wallpaper', 'cat2': 'Classic designs', 'cat3': '', 'url': 'https://injazcolor.com/en/product-category/wallpaper/classic-designs/'},
    {'cat1': 'Wallpaper', 'cat2': 'Geometric designs', 'cat3': '', 'url': 'https://injazcolor.com/en/product-category/wallpaper/geometric-designs/'},
    {'cat1': 'Wallpaper', 'cat2': 'Marble design', 'cat3': '', 'url': 'https://injazcolor.com/en/product-category/wallpaper/marble-design/'},
    #
    {'cat1': 'Parquet', 'cat2': 'الباركيه الهرمي', 'cat3': '', 'url': 'https://injazcolor.com/en/product-category/parquet/%d8%a7%d9%84%d9%87%d8%b1%d9%85%d9%8a/'},
    {'cat1': 'Parquet', 'cat2': 'باركيه ألماني', 'cat3': '', 'url': 'https://injazcolor.com/en/product-category/parquet/german/'},
    {'cat1': 'Parquet', 'cat2': 'باركيه صيني', 'cat3': '', 'url': 'https://injazcolor.com/en/product-category/parquet/chinese/'},
    {'cat1': 'Parquet', 'cat2': 'باركيه ضد الماء', 'cat3': '', 'url': 'https://injazcolor.com/en/product-category/parquet/waterproof/'},
]

def scrap_url_product(url1):
    
    cat1 = url1['cat1']
    cat2 = url1['cat2']
    cat3 = url1['cat3']
    url = url1['url']
    data = []
    while True:
        soup, urls_list = get_data(url)
        
        for toto in urls_list:
            data.append({
            'url':toto,
            'cat1': cat1,
            'cat2': cat2,
            'cat3': cat3,
            })
        try:
            url = getnextpage(soup)
        except:
            break
    logging.info( 'Scrape Categorie Done --> Next .')
    return data

df = pd.read_excel('injazcolor_url_model.xlsx')
for i, url in enumerate(list_urls):
    logging.info('Count: %s', i)
    data = scrap_url_product(url)
    df1 = pd.DataFrame(data)
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('injazcolor_url_product.xlsx')

