

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
    {'cat1': 'طاولات وكراسي', 'cat2': 'طاولات', 'cat3': '', 'url': 'https://spring01.com/%D8%B7%D8%A7%D9%88%D9%84%D8%A7%D8%AA/c2022184649'},
    {'cat1': 'طاولات وكراسي', 'cat2': 'كراسي', 'cat3': '', 'url': 'https://spring01.com/%D9%83%D8%B1%D8%A7%D8%B3%D9%8A/c607278283'},
    {'cat1': 'طاولات وكراسي', 'cat2': 'طقم جلسة', 'cat3': '', 'url': 'https://spring01.com/%D8%B7%D9%82%D9%85-%D8%AC%D9%84%D8%B3%D8%A9/c1139118805'},
    
    {'cat1': 'دواليب', 'cat2': 'دواليب مدخل', 'cat3': '', 'url': 'https://spring01.com/%D8%AF%D9%88%D8%A7%D9%84%D9%8A%D8%A8-%D9%85%D8%AF%D8%AE%D9%84/c1873793239'},
    {'cat1': 'دواليب', 'cat2': 'أدراج وصناديق', 'cat3': '', 'url': 'https://spring01.com/%D8%A3%D8%AF%D8%B1%D8%A7%D8%AC-%D9%88%D8%B5%D9%86%D8%A7%D8%AF%D9%8A%D9%82/c1698577874'},
    {'cat1': 'دواليب', 'cat2': 'دواليب جزم', 'cat3': '', 'url': 'https://spring01.com/%D8%AF%D9%88%D8%A7%D9%84%D9%8A%D8%A8-%D8%AC%D8%B2%D9%85/c14711772'},
    
    {'cat1': 'رفوف-ستنادات-فازات', 'cat2': 'رفوف وستاندات', 'cat3': '', 'url': 'https://spring01.com/%D8%B1%D9%81%D9%88%D9%81-%D9%88%D8%B3%D8%AA%D8%A7%D9%86%D8%AF%D8%A7%D8%AA/c1389271773'},
    {'cat1': 'رفوف-ستنادات-فازات', 'cat2': 'فازات', 'cat3': '', 'url': 'https://spring01.com/%D9%81%D8%A7%D8%B2%D8%A7%D8%AA/c334912482'},
    
    {'cat1': 'مفارش-مخدات', 'cat2': 'مفارش أرضية', 'cat3': '', 'url': 'https://spring01.com/%D9%85%D9%81%D8%A7%D8%B1%D8%B4-%D8%A3%D8%B1%D8%B6%D9%8A%D8%A9/c363359312'},
    {'cat1': 'مفارش-مخدات', 'cat2': 'مخدات', 'cat3': '', 'url': 'https://spring01.com/%D9%85%D8%AE%D8%AF%D8%A7%D8%AA/c1735822161'},
    
    {'cat1': 'لوحات وديكورات جدارية', 'cat2': 'لوحات', 'cat3': '', 'url': 'https://spring01.com/%D9%84%D9%88%D8%AD%D8%A7%D8%AA/c331965220'},
    {'cat1': 'لوحات وديكورات جدارية', 'cat2': 'مفارش وستائر جدارية', 'cat3': '', 'url': 'https://spring01.com/%D9%85%D9%81%D8%A7%D8%B1%D8%B4-%D9%88%D8%B3%D8%AA%D8%A7%D8%A6%D8%B1-%D8%AC%D8%AF%D8%A7%D8%B1%D9%8A%D8%A9/c1529278240'},
    {'cat1': 'لوحات وديكورات جدارية', 'cat2': 'ديكورات جدارية', 'cat3': '', 'url': 'https://spring01.com/%D8%AF%D9%8A%D9%83%D9%88%D8%B1%D8%A7%D8%AA-%D8%AC%D8%AF%D8%A7%D8%B1%D9%8A%D8%A9/c889392673'},
    
    {'cat1': 'الساعات والمرايا', 'cat2': 'ساعات', 'cat3': '', 'url': 'https://spring01.com/%D8%B3%D8%A7%D8%B9%D8%A7%D8%AA/c580021036'},
    {'cat1': 'الساعات والمرايا', 'cat2': 'مرايا', 'cat3': '', 'url': 'https://spring01.com/%D9%85%D8%B1%D8%A7%D9%8A%D8%A7/c2088274477'},
    
    {'cat1': 'السلات و أواني التقديم', 'cat2': 'السلات', 'cat3': '', 'url': 'https://spring01.com/%D8%A7%D9%84%D8%B3%D9%84%D8%A7%D8%AA/c404932655'},
    {'cat1': 'السلات و أواني التقديم', 'cat2': 'صحون تقديم', 'cat3': '', 'url': 'https://spring01.com/%D8%B5%D8%AD%D9%88%D9%86-%D8%AA%D9%82%D8%AF%D9%8A%D9%85/c1205138985'},
    
    {'cat1': 'ركن القهوة', 'cat2': 'دواليب وعربات القهوة', 'cat3': '', 'url': 'https://spring01.com/%D8%AF%D9%88%D8%A7%D9%84%D9%8A%D8%A8-%D9%88%D8%B9%D8%B1%D8%A8%D8%A7%D8%AA-%D8%A7%D9%84%D9%82%D9%87%D9%88%D8%A9/c1671312427'},
    {'cat1': 'ركن القهوة', 'cat2': 'اكواب وحامل الاكواب', 'cat3': '', 'url': 'https://spring01.com/%D8%A7%D9%83%D9%88%D8%A7%D8%A8-%D9%88%D8%AD%D8%A7%D9%85%D9%84-%D8%A7%D9%84%D8%A7%D9%83%D9%88%D8%A7%D8%A8/c1031492404'},
    {'cat1': 'ركن القهوة', 'cat2': 'ديكورات القهوة', 'cat3': '', 'url': 'https://spring01.com/%D8%AF%D9%8A%D9%83%D9%88%D8%B1%D8%A7%D8%AA-%D8%A7%D9%84%D9%82%D9%87%D9%88%D8%A9/c1496224054'},
    
    {'cat1': 'فوانيس وشموع ومباخر', 'cat2': 'فوانيس', 'cat3': '', 'url': 'https://spring01.com/%D9%81%D9%88%D8%A7%D9%86%D9%8A%D8%B3/c506034749'},
    {'cat1': 'فوانيس وشموع ومباخر', 'cat2': 'شموع', 'cat3': '', 'url': 'https://spring01.com/%D8%B4%D9%85%D9%88%D8%B9/c1811388734'},
    {'cat1': 'فوانيس وشموع ومباخر', 'cat2': 'مباخر', 'cat3': '', 'url': 'https://spring01.com/%D9%85%D8%A8%D8%A7%D8%AE%D8%B1/c1685281588'},
    
    {'cat1': 'أنتيكات حديد و مجمسات سيراميك', 'cat2': '', 'cat3': '', 'url': 'https://spring01.com/%D8%A3%D9%86%D8%AA%D9%8A%D9%83%D8%A7%D8%AA-%D8%AD%D8%AF%D9%8A%D8%AF-%D9%88-%D9%85%D8%AC%D9%85%D8%B3%D8%A7%D8%AA-%D8%B3%D9%8A%D8%B1%D8%A7%D9%85%D9%8A%D9%83/c987489530'},
    {'cat1': 'منتجات متنوعة', 'cat2': '', 'cat3': '', 'url': 'https://spring01.com/%D9%85%D9%86%D8%AA%D8%AC%D8%A7%D8%AA-%D9%85%D8%AA%D9%86%D9%88%D8%B9%D8%A9/c1172092991'},

]


def get_data(url):
    

    print('Url:', url)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    cookies = {'session': '134-8225175-0355220'}
    r = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(r.content, "html.parser")
    time.sleep(1)
    products = soup.find_all('div', {'class': 'product-block__thumb'})
    
    liens = [pro.find('a')['href']  for pro in products]
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
    
    soup, urls_list = get_data(url)
    
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

df = pd.read_excel('spring_url_model.xlsx')

for i, url in enumerate(urls):
    print('Count: ', i)
    
    data = scrap_url_product(url)
    df1 = pd.DataFrame(data)
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('spring_url_update.xlsx')
    