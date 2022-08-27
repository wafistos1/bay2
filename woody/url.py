

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
    {'cat1': 'غرف المعيشة', 'cat2': 'كنب فردي', 'cat3': '',  'url': 'https://woody.com.sa/product-tag/%d9%83%d9%86%d8%a8-%d9%81%d8%b1%d8%af%d9%8a/?per_page=36'},
    {'cat1': 'غرف المعيشة', 'cat2': 'كنب ثلاثي', 'cat3': '',  'url': 'https://woody.com.sa/product-tag/%d9%83%d9%86%d8%a8-%d8%ab%d9%84%d8%a7%d8%ab%d9%8a/?per_page=36'},
    {'cat1': 'غرف المعيشة', 'cat2': 'كنب زاوية', 'cat3': '',  'url': 'https://woody.com.sa/product-tag/%d9%83%d9%86%d8%a8-%d8%b2%d8%a7%d9%88%d9%8a%d8%a9/?per_page=36'},
    {'cat1': 'غرف المعيشة', 'cat2': 'كنب راحة', 'cat3': '',  'url': 'https://woody.com.sa/product-tag/cozy/?per_page=36'},
    {'cat1': 'غرف المعيشة', 'cat2': 'جلسات خارجيه', 'cat3': '',  'url': 'https://woody.com.sa/product-tag/outdoorandgarden/?per_page=36'},
    {'cat1': 'غرف المعيشة', 'cat2': 'طاولة كونسول', 'cat3': '',  'url': 'https://woody.com.sa/product-tag/%d8%b7%d8%a7%d9%88%d9%84%d8%a9-%d9%83%d9%88%d9%86%d8%b3%d9%88%d9%84/?per_page=36'},
    {'cat1': 'غرف المعيشة', 'cat2': 'طاولات شاي', 'cat3': '',  'url': 'https://woody.com.sa/product-tag/%d8%a7%d9%84%d8%b7%d8%a7%d9%88%d9%84%d8%a7%d8%aa/?per_page=36'},
    {'cat1': 'غرف المعيشة', 'cat2': 'مكتبات التلفزيون', 'cat3': '',  'url': 'https://woody.com.sa/product-tag/%d9%85%d9%83%d8%aa%d8%a8%d8%a7%d8%aa-%d8%a7%d9%84%d8%aa%d9%84%d9%81%d8%b2%d9%8a%d9%88%d9%86/?per_page=36'},
    # {'cat1': 'غرف المعيشة', 'cat2': ' ', 'cat3': '',  'url': ''},
    # {'cat1': 'غرف المعيشة', 'cat2': ' ', 'cat3': '',  'url': ''},
    {'cat1': 'غرف طعام', 'cat2': 'غرف طعام', 'cat3': '',  'url': 'https://woody.com.sa/%D8%AA%D8%B5%D9%86%D9%8A%D9%81-%D8%A7%D9%84%D9%85%D9%86%D8%AA%D8%AC%D8%A7%D8%AA/dining-rooms/?per_page=36'},
    {'cat1': 'غرف طعام', 'cat2': 'طاولة طعام', 'cat3': '',  'url': 'https://woody.com.sa/product-tag/%d8%b7%d8%a7%d9%88%d9%84%d8%a9-%d8%b7%d8%b9%d8%a7%d9%85/?per_page=36'},
    {'cat1': 'غرف طعام', 'cat2': 'كرسي طعام', 'cat3': '',  'url': 'https://woody.com.sa/product-tag/%d9%83%d8%b1%d8%b3%d9%8a-%d8%b7%d8%b9%d8%a7%d9%85/?per_page=36'},
    {'cat1': 'غرف طعام', 'cat2': 'بوفيه', 'cat3': '',  'url': 'https://woody.com.sa/product-tag/%d8%a8%d9%88%d9%81%d9%8a%d9%87/?per_page=36'},
    # {'cat1': '', 'cat2': '', 'cat3': '',  'url': ''},
    
    {'cat1': 'غرف النوم', 'cat2': 'غرف النوم المزدوجة', 'cat3': '',  'url': 'https://woody.com.sa/product-tag/%d8%ba%d8%b1%d9%81-%d8%a7%d9%84%d9%86%d9%88%d9%85-%d8%a7%d9%84%d9%85%d8%b2%d8%af%d9%88%d8%ac%d8%a9/?per_page=36'},
    {'cat1': 'غرف النوم', 'cat2': 'غرف نوم شبابية', 'cat3': '',  'url': 'https://woody.com.sa/product-tag/%d8%ba%d8%b1%d9%81-%d9%86%d9%88%d9%85-%d8%b4%d8%a8%d8%a7%d8%a8%d9%8a%d8%a9/?per_page=36'},
    {'cat1': 'غرف النوم', 'cat2': 'مرتبة سرير', 'cat3': '',  'url': 'https://woody.com.sa/product-tag/%d9%85%d8%b1%d8%aa%d8%a8%d8%a9-%d8%b3%d8%b1%d9%8a%d8%b1/?per_page=36'},
    {'cat1': 'غرف النوم', 'cat2': 'دواليب', 'cat3': '',  'url': 'https://woody.com.sa/product-tag/%d8%af%d9%88%d8%a7%d9%84%d9%8a%d8%a8/?per_page=36'},
    
    
    
    
    {'cat1': 'أثاث مكتبي', 'cat2': 'المكاتب', 'cat3': '',  'url': 'https://woody.com.sa/product-tag/desk/?per_page=36'},
    {'cat1': 'أثاث مكتبي', 'cat2': 'كرسي مكتب', 'cat3': '',  'url': 'https://woody.com.sa/product-tag/office-chair/?per_page=36'},
    {'cat1': 'أثاث مكتبي', 'cat2': 'طاولات مكتبيه', 'cat3': '',  'url': 'https://woody.com.sa/product-tag/%d8%b7%d8%a7%d9%88%d9%84%d8%a7%d8%aa-%d9%85%d9%83%d8%aa%d8%a8%d9%8a%d9%87/?per_page=36'},
    {'cat1': 'أثاث مكتبي', 'cat2': 'كنب مكتبي', 'cat3': '',  'url': 'https://woody.com.sa/product-tag/%d9%83%d9%86%d8%a8-%d9%85%d9%83%d8%aa%d8%a8%d9%8a/?per_page=36'},
    {'cat1': 'أثاث مكتبي', 'cat2': 'قواطع مكتبية', 'cat3': '',  'url': 'https://woody.com.sa/product-tag/%d9%82%d9%88%d8%a7%d8%b7%d8%b9-%d9%85%d9%83%d8%aa%d8%a8%d9%8a%d8%a9/?per_page=36'},
    {'cat1': 'أثاث مكتبي', 'cat2': 'دولاب مكتبي', 'cat3': '',  'url': 'https://woody.com.sa/product-tag/%d8%af%d9%88%d9%84%d8%a7%d8%a8-%d9%85%d9%83%d8%aa%d8%a8%d9%8a/?per_page=36'},
    {'cat1': 'أثاث مكتبي', 'cat2': 'طاولات اجتماعات', 'cat3': '',  'url': 'https://woody.com.sa/product-tag/meeting-tables/?per_page=36'},
    
    
    
    {'cat1': 'إكسسوارات منزلية', 'cat2': 'سجاد', 'cat3': '',  'url': 'https://woody.com.sa/product-tag/%d8%b3%d8%ac%d8%a7%d8%af/?per_page=36'},
    {'cat1': 'إكسسوارات منزلية', 'cat2': 'التحف', 'cat3': '',  'url': 'https://woody.com.sa/product-tag/%d8%a7%d9%84%d8%aa%d8%ad%d9%81/?per_page=36'},
    {'cat1': 'إكسسوارات منزلية', 'cat2': 'لوحات جدارية', 'cat3': '',  'url': 'https://woody.com.sa/product-tag/%d9%84%d9%88%d8%ad%d8%a7%d8%aa-%d8%ac%d8%af%d8%a7%d8%b1%d9%8a%d8%a9/?per_page=36'},
    {'cat1': 'إكسسوارات منزلية', 'cat2': 'الإضاءة', 'cat3': '',  'url': 'https://woody.com.sa/product-tag/lighting/?per_page=36'},
   
        
        
        
        ]

name_excel = 'sar99_product_update.xlsx'
options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')
#opti#     driver = webdriver.Firefox()ons.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)

def get_data(url, driver):
    # rand_int = randint(10000, 99999)
    driver.get(url)
    r = driver.find_element_by_tag_name('body').get_attribute('innerHTML')
    soup = BeautifulSoup(r, 'html.parser')
    print('Url:', url)
    # headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    # cookies = {'session': f'134-8225175-{rand_int}'}
    # r = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(r, "html.parser")
    time.sleep(1)
    products = soup.find_all('a', {'class': 'product-image-link'})
    
    liens = [pro['href'] for pro in products]
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
        soup, urls_list = get_data(url, driver)
        
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

df = pd.read_excel('woody_url_model.xlsx')


for i, url1 in enumerate(urls):
    print('Count: ', i)
    
    data = scrap_url_product(url1)
    df1 = pd.DataFrame(data)
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('woody_update_urls.xlsx')
