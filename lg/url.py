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

options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')
#opti#     driver = webdriver.Firefox()ons.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)


def get_data(url, driver, count, first=0):
    
    # Fonction to scrape all urls from itch categories
    # Return Data
    
#     s = HTMLSession()
#     r = s.get(url)
#     r.html.render(timeout= 30, sleep=1)
    
    print('Url:', url)
    if first != 1:
        driver.get(url)
        
        
    r = driver.find_element_by_tag_name('body').get_attribute('innerHTML')
    soup = BeautifulSoup(r, "html.parser")
    time.sleep(1)
    products = soup.find_all('div', {'class': 'products-info'}) # Tvs

    #products = soup.find('a', {'class': 'visual'})
    
    liens = ['https://www.lg.com' + toto.find('a')['href']  for toto in products]
    #liens = [toto['href']  for toto in products]
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


def getnextpage(driver):
   
    #Check if next url exist else send None objects
    # Return URL or None
    
    
    # print('Page', page)
    
    try:
        page = driver.find_element_by_xpath('//button[text()="التالي"]')
        try:
            driver.execute_script("arguments[0].removeAttribute('disabled')",page) 
        except:
            pass
        page.click()
        return 1
        
        # print('', url2)
    except:
        print('No Next')
        return 0
    


list_urls = []


def scrap_url_product(url1):
    
    # cat1 = 'وحدات التكييف'
    # cat2 = 'مكيفات سبليت الاستوائية'
    cat1 = 'الأجهزة الكهربائية'
    cat2 = 'غسالات'
    cat3 = ''
    url = url1
    data = []
    print(cat1, cat2, cat3)
    count = 1
    first = 0
    while True:
        time.sleep(5)
        soup, urls_list = get_data(url, driver, count, first)
        # Salut
        for toto in urls_list:

            # print(f'URL:', toto)
            data.append({
            'url':toto,
            'cat1': cat1,
            'cat2': cat2,
            'cat3': cat3,
            })
        print('Count: ', count)
        if count == 1:
            count = getnextpage(driver)
            first = 1
#             print('Url dans le while', url)
        else:
            first = 0
            break
    # print(data)
    print( f'Scrape done .')
    return data
df = pd.read_excel('lg_url_model.xlsx')
# url2 = 'https://www.lg.com/ae_ar/tropical-split-air-conditioners'
#url2 = 'https://www.lg.com/ae_ar/refrigerators'
url2 = 'https://www.lg.com/ae_ar/washing-machines'
data = scrap_url_product(url2)
df1 = pd.DataFrame(data)
df = pd.concat([df, df1], ignore_index=True)
df.to_excel('lg_update_url_frigo.xlsx')