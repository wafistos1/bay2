
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
import re, logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

urls = [
    
    {'cat1': 'قسم الخيام', 'cat2': '', 'cat3': '', 'url': 'https://kzoutdoors.com/%D9%82%D8%B3%D9%85-%D8%A7%D9%84%D8%AE%D9%8A%D8%A7%D9%85/c1430154079'},
    {'cat1': 'الكراسي والطاولات', 'cat2': '', 'cat3': '', 'url': 'https://kzoutdoors.com/%D8%A7%D9%84%D9%83%D8%B1%D8%A7%D8%B3%D9%8A-%D9%88%D8%A7%D9%84%D8%B7%D8%A7%D9%88%D9%84%D8%A7%D8%AA/c654608984'},
    {'cat1': 'قسم المظلات', 'cat2': '', 'cat3': '', 'url': 'https://kzoutdoors.com/%D9%82%D8%B3%D9%85-%D8%A7%D9%84%D9%85%D8%B8%D9%84%D8%A7%D8%AA/c493895020'},
    {'cat1': 'مستلزمات النوم', 'cat2': '', 'cat3': '', 'url': 'https://kzoutdoors.com/%D9%85%D8%B3%D8%AA%D9%84%D8%B2%D9%85%D8%A7%D8%AA-%D8%A7%D9%84%D9%86%D9%88%D9%85/c519717264'},
    {'cat1': 'مستلزمات التخييم', 'cat2': '', 'cat3': '', 'url': 'https://kzoutdoors.com/%D9%85%D8%B3%D8%AA%D9%84%D8%B2%D9%85%D8%A7%D8%AA-%D8%A7%D9%84%D8%AA%D8%AE%D9%8A%D9%8A%D9%85/c1719610096'},
    {'cat1': 'معدات الهايكينج', 'cat2': '', 'cat3': '', 'url': 'https://kzoutdoors.com/%D9%85%D8%B9%D8%AF%D8%A7%D8%AA-%D8%A7%D9%84%D9%87%D8%A7%D9%8A%D9%83%D9%8A%D9%86%D8%AC/c1011714233'},
    {'cat1': 'شنط الرحلات', 'cat2': '', 'cat3': '', 'url': 'https://kzoutdoors.com/%D8%B4%D9%86%D8%B7-%D8%A7%D9%84%D8%B1%D8%AD%D9%84%D8%A7%D8%AA/c168729350'},
    {'cat1': 'مطبخ الرحلات', 'cat2': '', 'cat3': '', 'url': 'https://kzoutdoors.com/%D9%85%D8%B7%D8%A8%D8%AE-%D8%A7%D9%84%D8%B1%D8%AD%D9%84%D8%A7%D8%AA/c1041152616'},
    {'cat1': 'الكشافات', 'cat2': '', 'cat3': '', 'url': 'https://kzoutdoors.com/%D8%A7%D9%84%D9%83%D8%B4%D8%A7%D9%81%D8%A7%D8%AA/c903665028'},
    {'cat1': 'حافظات المياه والقهوة', 'cat2': '', 'cat3': '', 'url': 'https://kzoutdoors.com/%D8%AD%D8%A7%D9%81%D8%B8%D8%A7%D8%AA-%D8%A7%D9%84%D9%85%D9%8A%D8%A7%D9%87-%D9%88%D8%A7%D9%84%D9%82%D9%87%D9%88%D8%A9/c241284293'},
    
]


def get_data(url):
    logging.info(f'Url: {url}')
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    # cookies = {'session': '134-8225175-0355220'}
    r = requests.get(url, headers=headers)#, cookies=cookies)
    soup = BeautifulSoup(r.content, "html.parser")
    time.sleep(1)
    products = soup.find_all('div', {'class': 'product'})
    liens = [toto.find('a')['href']  for toto in products]
    logging.info(f'Len products {len(liens)}')
    list_liens = []
    for t in liens:
        list_liens.append(t)
    return liens

def getnextpage(soup):
    page = soup.find('a', {'class': 'next i-next'})
    try:
        # if next url exist 
        url2 = str(page['href'])
        return url2
        # print('', url2)
    except:
        print('No Next')
        pass
    return url2 

def scrap_url_product(url1):
    
    cat1 = url1['cat1']
    cat2 = url1['cat2']
    cat3 = url1['cat3']
    url = url1['url']
    data = []
    urls_list = get_data(url)
    for toto in urls_list:
        # print(f'URL:', toto)
        data.append({
        'url':toto,
        'cat1': cat1,
        'cat2': cat2,
        'cat3': cat3,
        })
    # print(data)
    print( f'Scrape done .')
    return data
df = pd.read_excel('kzoutdoors_url_model.xlsx')

for i, url in enumerate(urls[86:]):
    logging.info('Count: %s', i)
    data = scrap_url_product(url)
    df1 = pd.DataFrame(data)
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('kzoutdoors_url_update.xlsx')
logging.info('Scraping url Done.')

