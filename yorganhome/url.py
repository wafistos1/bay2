

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
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

list_urls = [
    
    {'cat1': 'القطن العضوي', 'cat2': '', 'cat3': '', 'url': 'https://yorganhome.com/%D8%A7%D9%84%D9%82%D8%B7%D9%86-%D8%A7%D9%84%D8%B9%D8%B6%D9%88%D9%8A/c1442360439'},
    {'cat1': 'القطن المصري', 'cat2': '', 'cat3': '', 'url': 'https://yorganhome.com/%D8%A7%D9%84%D9%82%D8%B7%D9%86-%D8%A7%D9%84%D9%85%D8%B5%D8%B1%D9%8A/c2014547318'},
    {'cat1': 'مقاس سوبر كينج', 'cat2': '', 'cat3': '', 'url': 'https://yorganhome.com/%D9%85%D9%82%D8%A7%D8%B3-%D8%B3%D9%88%D8%A8%D8%B1-%D9%83%D9%8A%D9%86%D8%AC/c1766491502'},
    {'cat1': 'مقاس كينج', 'cat2': '', 'cat3': '', 'url': 'https://yorganhome.com/%D9%85%D9%82%D8%A7%D8%B3-%D9%83%D9%8A%D9%86%D8%AC/c527197805'},
    {'cat1': 'مقاس كوين', 'cat2': '', 'cat3': '', 'url': 'https://yorganhome.com/%D9%85%D9%82%D8%A7%D8%B3-%D9%83%D9%88%D9%8A%D9%86/c1941583971'},
    {'cat1': 'مقاس مفرد', 'cat2': '', 'cat3': '', 'url': 'https://yorganhome.com/%D9%85%D9%82%D8%A7%D8%B3-%D9%85%D9%81%D8%B1%D8%AF/c352109416'},
    {'cat1': 'اطفال', 'cat2': '', 'cat3': '', 'url': 'https://yorganhome.com/%D8%A7%D8%B7%D9%81%D8%A7%D9%84/c1550339956'},
    {'cat1': 'مواليد', 'cat2': '', 'cat3': '', 'url': 'https://yorganhome.com/%D9%85%D9%88%D8%A7%D9%84%D9%8A%D8%AF/c42147947'},
    {'cat1': 'مناشف', 'cat2': 'مناشف اطفال', 'cat3': '', 'url': 'https://yorganhome.com/%D9%85%D9%86%D8%A7%D8%B4%D9%81-%D8%A7%D8%B7%D9%81%D8%A7%D9%84/c1447515486'},
    {'cat1': 'مناشف', 'cat2': 'اطقم مناشف', 'cat3': '', 'url': 'https://yorganhome.com/%D8%A7%D8%B7%D9%82%D9%85-%D9%85%D9%86%D8%A7%D8%B4%D9%81/c539784287'},
    {'cat1': 'مناشف', 'cat2': 'مناشف يد مع سله', 'cat3': '', 'url': 'https://yorganhome.com/%D9%85%D9%86%D8%A7%D8%B4%D9%81-%D9%8A%D8%AF-%D9%85%D8%B9-%D8%B3%D9%84%D9%87/c1008088077'},
    {'cat1': 'بروتكتر حامي المرتبه - المخدات', 'cat2': '', 'cat3': '', 'url': 'https://yorganhome.com/%D8%A8%D8%B1%D9%88%D8%AA%D9%83%D8%AA%D8%B1-%D8%AD%D8%A7%D9%85%D9%8A-%D8%A7%D9%84%D9%85%D8%B1%D8%AA%D8%A8%D9%87-%D8%A7%D9%84%D9%85%D8%AE%D8%AF%D8%A7%D8%AA/c250341714'},
    {'cat1': 'فيتد شيت', 'cat2': '', 'cat3': '', 'url': 'https://yorganhome.com/%D9%81%D9%8A%D8%AA%D8%AF-%D8%B4%D9%8A%D8%AA/c1487931475'},
    {'cat1': 'حشوات', 'cat2': '', 'cat3': '', 'url': 'https://yorganhome.com/%D8%AD%D8%B4%D9%88%D8%A7%D8%AA/c714938204خداديات'},
    {'cat1': 'خداديات', 'cat2': '', 'cat3': '', 'url': 'https://yorganhome.com/%D8%AE%D8%AF%D8%A7%D8%AF%D9%8A%D8%A7%D8%AA/c1256002792'},
    {'cat1': 'ثرو', 'cat2': '', 'cat3': '', 'url': 'https://yorganhome.com/%D8%AB%D8%B1%D9%88/c75118173'},
    {'cat1': 'القطع الاخيرة', 'cat2': '', 'cat3': '', 'url': 'https://yorganhome.com/%D8%A7%D9%84%D9%82%D8%B7%D8%B9-%D8%A7%D9%84%D8%A7%D8%AE%D9%8A%D8%B1%D8%A9/c1133447538'},
    {'cat1': 'اطقم سفرة', 'cat2': '', 'cat3': '', 'url': 'https://yorganhome.com/%D8%A7%D8%B7%D9%82%D9%85-%D8%B3%D9%81%D8%B1%D8%A9/c1990185201'},

]

options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')
#opti#     driver = webdriver.Firefox()ons.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)

def get_data(url):

    print('Url:', url)
    driver.get(url)
    r = driver.find_element_by_tag_name('body').get_attribute('innerHTML')
    soup = BeautifulSoup(r, "html.parser")
    time.sleep(1)
    products = soup.find_all('div', {'class': 'product contain'})
    
    liens = [toto.find('a')['href']  for toto in products]
    print('Len products', len(liens))
    list_liens = []
    
    for t in liens:
        list_liens.append(t)
    data = {
        'url':list_liens,
        }
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


def scrap_url_product(url1):
    
    cat1 = url1['cat1']
    cat2 = url1['cat2']
    cat3 = url1['cat3']
    url = url1['url']
    data = []
    soup, urls_list = get_data(url)
    
    for toto in urls_list:
        data.append({
        'url':toto,
        'cat1': cat1,
        'cat2': cat2,
        'cat3': cat3,
        })

    # print(data)
    print( f'Scrape done .')
    return data


df = pd.read_excel('yorganhome_url_model.xlsx')
for i, url in enumerate(list_urls):
    logging.info(f'Count: {i}')
    data = scrap_url_product(url)
    df1 = pd.DataFrame(data)
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('yorganhome_url_update.xlsx')
