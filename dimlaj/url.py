

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


urls = [
    
    {'cat1': 'Tea & Coffee', 'cat2': 'Arabic Coffee Sets', 'cat3': '', 'url': 'https://dimlaj.com/collections/arabic-coffee-cups'},
    {'cat1': 'Tea & Coffee', 'cat2': 'Turkish Coffee Sets', 'cat3': '', 'url': 'https://dimlaj.com/collections/turkish-coffee-cups'},
    {'cat1': 'Tea & Coffee', 'cat2': 'Tea Sets', 'cat3': '', 'url': 'https://dimlaj.com/collections/tea-sets'},
    {'cat1': 'Tea & Coffee', 'cat2': 'Vacuum Jugs', 'cat3': '', 'url': 'https://dimlaj.com/collections/vacuum-jugs'},
    {'cat1': 'Tea & Coffee', 'cat2': 'Mugs', 'cat3': '', 'url': 'https://dimlaj.com/collections/mugs'},
    {'cat1': 'Tea & Coffee', 'cat2': 'Pots', 'cat3': '', 'url': 'https://dimlaj.com/collections/pots'},
    
    
     {'cat1': 'Tabletop & Accessories', 'cat2': 'Bowls', 'cat3': '', 'url': 'https://dimlaj.com/collections/bowls-1'},
     {'cat1': 'Tabletop & Accessories', 'cat2': 'Platters', 'cat3': '', 'url': 'https://dimlaj.com/collections/platters'},
     {'cat1': 'Tabletop & Accessories', 'cat2': 'Trays & Accessories', 'cat3': '', 'url': 'https://dimlaj.com/collections/trays'},
     {'cat1': 'Tabletop & Accessories', 'cat2': 'Cutlery', 'cat3': '', 'url': 'https://dimlaj.com/collections/cutlery'},
     {'cat1': 'Tabletop & Accessories', 'cat2': 'Cake Platters & Stands', 'cat3': '', 'url': 'https://dimlaj.com/collections/stands'},
     {'cat1': 'Tabletop & Accessories', 'cat2': 'Ice-cream Cups', 'cat3': '', 'url': 'https://dimlaj.com/collections/ice-cream-cups'},
     {'cat1': 'Tabletop & Accessories', 'cat2': 'Jugs & Decanters', 'cat3': '', 'url': 'https://dimlaj.com/collections/jugs-decanters'},
     {'cat1': 'Tabletop & Accessories', 'cat2': 'Bottles', 'cat3': '', 'url': 'https://dimlaj.com/collections/bottles'},
     {'cat1': 'Tabletop & Accessories', 'cat2': 'Dinner Sets', 'cat3': '', 'url': 'https://dimlaj.com/collections/dinner-sets'},
    
    {'cat1': 'Tumblers & Stemware', 'cat2': 'Tumblers', 'cat3': '', 'url': 'https://dimlaj.com/collections/highball-tumblers'},
    {'cat1': 'Tumblers & Stemware', 'cat2': 'Short Tumblers', 'cat3': '', 'url': 'https://dimlaj.com/collections/lowball-tumblers'},
    {'cat1': 'Tumblers & Stemware', 'cat2': 'Goblet Stemware', 'cat3': '', 'url': 'https://dimlaj.com/collections/goblet-stems'},
    {'cat1': 'Tumblers & Stemware', 'cat2': 'Flute Stemware', 'cat3': '', 'url': 'https://dimlaj.com/collections/flute-stems'},
    {'cat1': 'Tumblers & Stemware', 'cat2': 'Shots', 'cat3': '', 'url': 'https://dimlaj.com/collections/shots'},
    {'cat1': 'Tumblers & Stemware', 'cat2': 'Drinksets', 'cat3': '', 'url': 'https://dimlaj.com/collections/drinksets'},
    
    {'cat1': 'Home Décor', 'cat2': 'Vases', 'cat3': '', 'url': 'https://dimlaj.com/collections/vases'},
    {'cat1': 'Home Décor', 'cat2': 'Candles & Holders', 'cat3': '', 'url': 'https://dimlaj.com/collections/candles-holders'},
    {'cat1': 'Home Décor', 'cat2': 'Centerpieces', 'cat3': '', 'url': 'https://dimlaj.com/collections/centerpieces'},
    {'cat1': 'Home Décor', 'cat2': 'Lighting & Table Lamps', 'cat3': '', 'url': 'https://dimlaj.com/collections/lighting-table-lamps'},
    {'cat1': 'Home Décor', 'cat2': 'Storage Boxes', 'cat3': '', 'url': 'https://dimlaj.com/collections/storage-boxes'},
    # {'cat1': '', 'cat2': '', 'cat3': '', 'url': ''},
    # {'cat1': '', 'cat2': '', 'cat3': '', 'url': ''},
]


options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')
#opti#     driver = webdriver.Firefox()ons.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)


def get_data(url):
    
    # Fonction to scrape all urls from itch categories
    # Return Data
    
#     s = HTMLSession()
#     r = s.get(url)
#     r.html.render(timeout= 30, sleep=1)
    print('Url:', url)
    driver.get(url)
    time.sleep(2)
    r = driver.find_element_by_tag_name('body').get_attribute('innerHTML')
    soup = BeautifulSoup(r, "html.parser")
    time.sleep(1)
    products = soup.find_all('div', {'class': 'product-image pr oh lazyloaded'})
    
    liens = ['https://dimlaj.com' + toto.find('a')['href']  for toto in products]
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
    
    page = soup.find('a', {'class': 'next page-numbers'})
    # print('Page', page)
    
    try:
        # if next url exist 
        url2 = 'https://dimlaj.com' + str(page['href'])
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
df = pd.read_excel('dimlaj_model_url.xlsx')
for i , url in enumerate(urls):
    data = scrap_url_product(url)
    df1 = pd.DataFrame(data)
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('dimlaj_update_url.xlsx')
