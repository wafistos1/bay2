
import time
import os
import requests
import re
import logging
from dataclasses import dataclass, field
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

#pip install requests pandas openpyxl selenium=3.14 fake_useragent bs4
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

def try_except(test):
    try:
        test 
        return test
    except: 
        pass
    
@dataclass
class Product:
    link_url : str = ''
    title: str = ''
    name : str = ''
    position: str = ''
    adresse: str = ''
    phone: str = ''
    email: str = ''
    web_site: str = ''


urls = pd.read_excel('model_url_update.xlsx')
list_urls = []
for index, row in urls.iterrows():
    list_urls.append(
        {
            'url': row['url'],
            'cat1': row['cat1'],
            'cat2': row['cat2'],
            'cat3': row['cat3'],
        }
    )

def scrape_data(url1):
    url = url1['url']
    product = Product()
    
    logging.info('URL: %s', url)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    cookies = {'session': '134-8225175-0355220'}
    r = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(r.content, "html.parser")
    product.link_url = url
    product.title = soup.find('h1', {'class': 'headline'}).text.strip()
    try:
        product.name =soup.find('section', {'class': 'b-main__section--cp-members-list'}).find('h4').text.strip()
    except:
        pass
    try:
        product.position = try_except(soup.find('section', {'class': 'b-main__section--cp-members-list'}).find('h4').next_element.next_element.text.strip())
    except:
        pass
    try:
        product.adresse = soup.find('div', {'class': 'adress-box'}).find('p').text.strip()
    except:
        pass
    try:
        product.phone = soup.find('span', {'class': 'icon--phone'}).find('a').text.strip()
    except:
        pass
    try:
        product.email = soup.find('span', {'class': 'icon--mail'}).find('a').text.strip()
    except:
        pass
    try:
        product.web_site = soup.find('span', {'class': 'icon--url'}).find('a').text.strip()
    except:
        pass
    time.sleep(1)
    
    return product.__dict__
        

df = pd.read_excel('model_product.xlsx')
for i, url in enumerate(list_urls):
    logging.info('Count: %s', i)
    data = scrape_data(url)
    df1 = pd.DataFrame([data])
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('model_product_update.xlsx')
logging.info('Scraping products Done..')
