

from cgitb import text
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


def get_data(url):
    
    # Fonction to scrape all urls from itch categories
    # Return Data
    
#     s = HTMLSession()
#     r = s.get(url)
#     r.html.render(timeout= 30, sleep=1)
    print('Url:', url)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    cookies = {'session': '134-8225175-0355220'}
    r = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(r.content, "html.parser")
    time.sleep(1)
    products = soup.find_all('div', {'class': 'product-thumb'})
    
    liens = [toto.find('a')['href']  for toto in products]
    print('Len products', len(liens))
    list_liens = []
    
    for t in liens:
        list_liens.append(t)
#     print('list_cat1', list_cat1)
    data = {
        'url':list_liens,
        }
    # df = pd.DataFrame(data)
#     print(df)
#         print('Href: ', t['href'])
#     print("Soup get_data")
    return soup, list_liens


def getnextpage(soup):
   
    #Check if next url exist else send None objects
    # Return URL or None
    
    page = soup.find('li', text='>')
    # print('Page', page)
    
    try:
        # if next url exist 
        url2 = str(page.find('a')['href'])
        return url2
        # print('', url2)
    except:
        print('No Next')
        pass
    return url2 


list_urls = []


def scrap_url_product(url1):
    
    cat1 = url1['cat1']
    cat2 = url1['cat2']
    cat3 = url1['cat3']
    url = url1['url']
    data = []
    print(cat1, cat2, cat3)
    while True:
        soup, urls_list = get_data(url)
        
        for toto in urls_list:

            # print(f'URL:', toto)
            data.append({
            'url':toto,
            'cat1': cat1,
            'cat2': cat2,
            'cat3': cat3,
            })

        try:
            url = getnextpage(soup)
#             print('Url dans le while', url)
        except:
            break
    # print(data)
    print( f'Scrape done .')
    return data


list_cat = [
    
    {'cat1': 'طاولات تلفزيون', 'cat2': '', 'cat3': '','url': 'https://www.99sar.com/ar/%D8%B7%D8%A7%D9%88%D9%84%D8%A7%D8%AA-%D9%88%D9%85%D9%83%D8%AA%D8%A8%D8%A7%D8%AA-%D8%AA%D9%84%D9%81%D8%B2%D9%8A%D9%88%D9%86'},
    {'cat1': 'طقم طاولات','cat2': '', 'cat3': '','url': 'https://www.99sar.com/ar/%D8%B7%D9%82%D9%85-%D8%B7%D8%A7%D9%88%D9%84%D8%A7%D8%AA'},
    {'cat1': 'ركن القهوة','cat2': '', 'cat3': '','url': 'https://www.99sar.com/ar/%D8%B1%D9%83%D9%86-%D8%A7%D9%84%D9%82%D9%87%D9%88%D8%A9'},
    {'cat1': 'طاولات قهوة وخدمة','cat2': '', 'cat3': '','url': 'https://www.99sar.com/ar/%D8%B7%D8%A7%D9%88%D9%84%D8%A7%D8%AA-%D9%82%D9%87%D9%88%D8%A9-%D9%88%D8%AE%D8%AF%D9%85%D8%A9'},
    {'cat1': 'طاولات متعددة الاستخدام','cat2': '', 'cat3': '','url': 'https://www.99sar.com/ar/%D8%B7%D8%A7%D9%88%D9%84%D8%A7%D8%AA-%D9%85%D8%AA%D8%B9%D8%AF%D8%AF%D8%A9-%D8%A7%D9%84%D8%A7%D8%B3%D8%AA%D8%AE%D8%AF%D8%A7%D9%85'},
    {'cat1': 'مداخل وجزامات','cat2': '', 'cat3': '','url': 'https://www.99sar.com/ar/%D9%85%D8%AF%D8%A7%D8%AE%D9%84-%D9%88%D8%AC%D8%B2%D8%A7%D9%85%D8%A7%D8%AA'},
    {'cat1': 'لوحات ومناظر مطبوعة','cat2': '', 'cat3': '','url': 'https://www.99sar.com/ar/%D9%84%D9%88%D8%AD%D8%A7%D8%AA-%D9%88%D9%85%D9%86%D8%A7%D8%B8%D8%B1-%D8%AC%D8%AF%D8%A7%D8%B1%D9%8A%D8%A9'},
    {'cat1': 'لوحات ركن القهوة','cat2': '', 'cat3': '','url': 'https://www.99sar.com/ar/%D9%84%D9%88%D8%AD%D8%A7%D8%AA-%D8%B9%D8%B1%D9%88%D8%B6-%D8%AA%D8%AE%D9%81%D9%8A%D8%B6%D8%A7%D8%AA-%D8%B1%D9%83%D9%86-%D9%82%D9%87%D9%88%D8%A9'},
    {'cat1': 'لوحات محفورة','cat2': '', 'cat3': '','url': 'https://www.99sar.com/ar/%D9%84%D9%88%D8%AD%D8%A7%D8%AA%20%D8%AC%D8%AF%D8%A7%D8%B1%D9%8A%D8%A9%20%D8%AD%D9%81%D8%B1%20%D9%88%D9%82%D8%B5'},
    # {'cat1': '','cat2': '', 'cat3': '','url': ''},
    
    
]

df = pd.read_excel('sar_url_model.xlsx')

for i, url1 in enumerate(list_cat):
    data = scrap_url_product(url1)
    df1 = pd.DataFrame(data)
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('sar_url_update.xlsx')
    
