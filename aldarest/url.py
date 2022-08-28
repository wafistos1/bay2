
import time
import os
import requests
import re, logging
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
    logging.info('URL: %s', url)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    cookies = {'session': '134-8225175-0355220'}
    r = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(r.content, "html.parser")
    time.sleep(1)
    products = soup.find_all('div',{'class': 'HU-block_top'})
    
    liens = [toto.find('a')['href']  for toto in products]
    print('Len products', len(liens))
    return soup, liens


def getnextpage(soup):
    page = soup.find('a', {'class': 'next'})
    try:
        url2 = str(page['href'])
        return url2
    except:
        print('No Next')
        pass
    return url2 


list_urls = [
    {'cat1': 'غرفه المعيشة', 'cat2': '', 'cat3': '', 'url': 'https://www.aldarest.sa/product-category/aliving/?filter=1&main=100&vals=729'},
    {'cat1': 'أطفال', 'cat2': '', 'cat3': '', 'url': 'https://www.aldarest.sa/product-category/%d8%a3%d9%81%d8%b6%d9%84-%d8%a7%d9%84%d9%85%d9%86%d8%aa%d8%ac%d8%a7%d8%aa-%d9%81%d9%8a-%d8%a7%d9%84%d8%b1%d8%a6%d9%8a%d8%b3%d9%8a%d8%a9/%d8%a3%d8%b7%d9%81%d8%a7%d9%84/'},
    {'cat1': 'غرف النوم', 'cat2': '', 'cat3': '', 'url': 'https://www.aldarest.sa/product-category/abedroom/'},
    {'cat1': 'غرفة الطعام', 'cat2': '', 'cat3': '', 'url': 'https://www.aldarest.sa/product-category/adining/'},
    # {'cat1': '', 'cat2': '', 'cat3': '', 'url': ''},
    # {'cat1': '', 'cat2': '', 'cat3': '', 'url': ''},
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
df = pd.read_excel('aldarest_url_model.xlsx')
for i, url in enumerate(list_urls):
    logging.info('Count: %s', i)
    data = scrap_url_product(url)
    df1 = pd.DataFrame(data)
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('aldarest_url_update.xlsx')
logging.info('Scraping URL Done.')

