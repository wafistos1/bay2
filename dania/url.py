

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


# List urls of all categories
list_cats = [
    
    {'cat1': 'ضيافة و تقديم', 'cat2': 'قهوة تركي', 'cat3': '', 'url': 'https://dania.co/category/mQjqNb', },
    {'cat1': 'ضيافة و تقديم', 'cat2': 'اطقم قهوة عربي و شاي', 'cat3': '', 'url': 'https://dania.co/category/onrBVZ', },
    {'cat1': 'ضيافة و تقديم', 'cat2': 'بيالات شاي و صحون', 'cat3': '', 'url': 'https://dania.co/category/YgxBdw', },
    {'cat1': 'ضيافة و تقديم', 'cat2': 'اكواب', 'cat3': '', 'url': 'https://dania.co/category/PdKWmr', },
    {'cat1': 'ضيافة و تقديم', 'cat2': 'ترامس و اباريق', 'cat3': '', 'url': 'https://dania.co/category/jZDQzR', },
    {'cat1': 'ضيافة و تقديم', 'cat2': 'صحون تقديم', 'cat3': '', 'url': 'https://dania.co/category/ydRGPx', },
    {'cat1': 'ضيافة و تقديم', 'cat2': 'تمريات', 'cat3': '', 'url': 'https://dania.co/category/KjrOen', },
    {'cat1': 'ضيافة و تقديم', 'cat2': 'سكريات', 'cat3': '', 'url': 'https://dania.co/category/aevOnR', },
    {'cat1': 'ضيافة و تقديم', 'cat2': 'اطقم كيك', 'cat3': '', 'url': 'https://dania.co/category/RAOrDn', },
    
    {'cat1': 'صواني تقديم', 'cat2': 'صواني ستيل', 'cat3': '', 'url': 'https://dania.co/category/GYpdwz', },
    {'cat1': 'صواني تقديم', 'cat2': 'صواني خشب', 'cat3': '', 'url': 'https://dania.co/category/KjrOQa', },
    {'cat1': 'صواني تقديم', 'cat2': 'صواني رخام', 'cat3': '', 'url': 'https://dania.co/category/Oqvnor', },
    {'cat1': 'صواني تقديم', 'cat2': 'صواني زجاج و بورسلان', 'cat3': '', 'url': 'https://dania.co/category/bRKbln', },
    
    {'cat1': 'مباخر و علب العود', 'cat2': '', 'cat3': '', 'url': 'https://dania.co/category/xAgbPl', },
    
    {'cat1': 'اواني المائدة', 'cat2': 'اطقم سفرة', 'cat3': '', 'url': 'https://dania.co/category/XeDjgB', },
    {'cat1': 'اواني المائدة', 'cat2': 'اطقم ملاعق و سكاكين', 'cat3': '', 'url': 'https://dania.co/category/qQywAd', },
    {'cat1': 'اواني المائدة', 'cat2': 'اطقم شوربة', 'cat3': '', 'url': 'https://dania.co/category/AzGaPP', },
    {'cat1': 'اواني المائدة', 'cat2': 'اطقم جك و كاسات', 'cat3': '', 'url': 'https://dania.co/category/VqnXKK', },
    {'cat1': 'اواني المائدة', 'cat2': 'مستلزمات بوفيه', 'cat3': '', 'url': 'https://dania.co/category/NKdRmv', },
    
    {'cat1': 'أدوات و اكسسوارات المطبخ', 'cat2': 'قدور', 'cat3': '', 'url': 'https://dania.co/category/BrmOPA', },
    {'cat1': 'أدوات و اكسسوارات المطبخ', 'cat2': 'طاوات', 'cat3': '', 'url': 'https://dania.co/category/rAdmQj', },
    {'cat1': 'أدوات و اكسسوارات المطبخ', 'cat2': 'صواني فرن', 'cat3': '', 'url': 'https://dania.co/category/OqvzAR', },
    {'cat1': 'أدوات و اكسسوارات المطبخ', 'cat2': 'اكسسورات المطبخ', 'cat3': '', 'url': 'https://dania.co/category/dPOXBl', },
    
    
    {'cat1': 'تحف و اكسسورات', 'cat2': '', 'cat3': '', 'url': 'https://dania.co/category/zvGRWg', }, 
]


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
    products = soup.find_all('li', {'class': 'item last'})
    
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
    
    page = soup.find('a', {'class': 'next i-next'})
    # print('Page', page)
    
    try:
        # if next url exist 
        url2 = str(page['href'])
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

