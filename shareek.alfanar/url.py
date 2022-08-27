

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
import time
import os
# from fake_useragent import UserAgent
from random import randint
import pandas as pd
import numpy as np
import requests
import pandas as pd
import re

urls = [
    
    # {'cat1': 'لوحات التوزيع والتحكم بالطاقة', 'cat2': 'لوحة توزيع الفنار - ريسان', 'url': 'https://shareek.alfanar.com/aedb2b/alfanarAedB2b/ar/%D9%84%D9%88%D8%AD%D8%A7%D8%AA-%D8%A7%D9%84%D8%AA%D9%88%D8%B2%D9%8A%D8%B9-%D9%88%D8%A7%D9%84%D8%AA%D8%AD%D9%83%D9%85-%D8%A8%D8%A7%D9%84%D8%B7%D8%A7%D9%82%D8%A9/%D9%84%D9%88%D8%AD%D8%A9-%D8%AA%D9%88%D8%B2%D9%8A%D8%B9-%D8%A7%D9%84%D9%81%D9%86%D8%A7%D8%B1---%D8%B1%D9%8A%D8%B3%D8%A7%D9%86/c/ALFANAR_RAYSAN'},
    # {'cat1': 'لوحات التوزيع والتحكم بالطاقة', 'cat2': 'Eletra LA لوحة التوزيع الأمريكية', 'url': 'https://shareek.alfanar.com/aedb2b/alfanarAedB2b/ar/%D9%84%D9%88%D8%AD%D8%A7%D8%AA-%D8%A7%D9%84%D8%AA%D9%88%D8%B2%D9%8A%D8%B9-%D9%88%D8%A7%D9%84%D8%AA%D8%AD%D9%83%D9%85-%D8%A8%D8%A7%D9%84%D8%B7%D8%A7%D9%82%D8%A9/Eletra-LA-%D9%84%D9%88%D8%AD%D8%A9-%D8%A7%D9%84%D8%AA%D9%88%D8%B2%D9%8A%D8%B9-%D8%A7%D9%84%D8%A3%D9%85%D8%B1%D9%8A%D9%83%D9%8A%D8%A9/c/ELETRA_LA'},
    {'cat1': 'لوحات التوزيع والتحكم بالطاقة', 'cat2': 'Eletra LD لوحة التوزيع الأوربية', 'url': 'https://shareek.alfanar.com/aedb2b/alfanarAedB2b/ar/%D9%84%D9%88%D8%AD%D8%A7%D8%AA-%D8%A7%D9%84%D8%AA%D9%88%D8%B2%D9%8A%D8%B9-%D9%88%D8%A7%D9%84%D8%AA%D8%AD%D9%83%D9%85-%D8%A8%D8%A7%D9%84%D8%B7%D8%A7%D9%82%D8%A9/Eletra-LD-%D9%84%D9%88%D8%AD%D8%A9-%D8%A7%D9%84%D8%AA%D9%88%D8%B2%D9%8A%D8%B9-%D8%A7%D9%84%D8%A3%D9%88%D8%B1%D8%A8%D9%8A%D8%A9/c/ELETRA_LD'},
    # # {'cat1': 'لوحات التوزيع والتحكم بالطاقة', 'cat2': '', 'url': ''},
    # {'cat1': 'لوحات التوزيع والتحكم بالطاقة', 'cat2': '', 'url': ''},
    # {'cat1': '', 'cat2': '', 'url': ''},
    # {'cat1': '', 'cat2': '', 'url': ''},
    # {'cat1': '', 'cat2': '', 'url': ''},
    
]


def get_data(url):
    print('URL: ', url)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    cookies = {'session': '134-8225175-0355220'}
    r = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(r.content, "html.parser")
    time.sleep(1)
    products = soup.find_all('a', {'class': 'product__list--thumb'})
    
    liens = ['https://shareek.alfanar.com'  + toto['href']  for toto in products]
    print('Len products', len(liens))
    list_liens = []
    return soup, liens


def getnextpage(soup):
   
    #Check if next url exist else send None objects
    # Return URL or None
    
    page = soup.find('a', {'rel': 'next'})
    # print('Page', page)
    
    try:
        # if next url exist 
        url2 = str('https://shareek.alfanar.com' + page['href'])
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
    url = url1['url']
    data = []
   
    while True:
        soup, urls_list = get_data(url)
        
        for toto in urls_list:

            # print(f'URL:', toto)
            data.append({
            'url':toto,
            'cat1': cat1,
            'cat2': cat2,
            })

        try:
            url = getnextpage(soup)
            if url == 'https://shareek.alfanar.com#':
                break
#             print('Url dans le while', url)
        except:
            break
    # print(data)
    print( f'Scrape done .')
    return data

df = pd.read_excel('shreek_url_model.xlsx')


for i, url1 in enumerate(urls):
    print('Count: ', i)
    
    data = scrap_url_product(url1)
    df1 = pd.DataFrame(data)
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('shareek_update_urls.xlsx')
