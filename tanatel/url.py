

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
    
    {'cat1': 'غرفة نوم', 'cat2': 'أطقم غرف النوم', 'cat3': '',  'url': 'https://tanatel.sa/index.php?route=product/category&path=64_65_66'},
    {'cat1': 'غرفة نوم', 'cat2': 'رأسية السرير ، بوكس منجد', 'cat3': '',  'url': 'https://tanatel.sa/index.php?route=product/category&path=64_65_75'},
    {'cat1': 'غرفة نوم', 'cat2': 'كمدينة', 'cat3': '',  'url': 'https://tanatel.sa/index.php?route=product/category&path=64_65_76'},
    {'cat1': 'غرفة نوم', 'cat2': 'التسريحة', 'cat3': '',  'url': 'https://tanatel.sa/index.php?route=product/category&path=64_65_77'},
    {'cat1': 'غرفة نوم', 'cat2': 'شفنيرة', 'cat3': '',  'url': 'https://tanatel.sa/index.php?route=product/category&path=64_65_78'},
    {'cat1': 'غرفة نوم', 'cat2': 'دولاب الملابس', 'cat3': '',  'url': 'https://tanatel.sa/index.php?route=product/category&path=64_65_79'},
    {'cat1': 'غرفة نوم', 'cat2': 'أريكة شيزلونج', 'cat3': '',  'url': 'https://tanatel.sa/index.php?route=product/category&path=64_65_80'},
    {'cat1': 'غرفة نوم', 'cat2': ' غرف نوم الأطفال', 'cat3': 'اطقم غرف نوم الاطفال',  'url': 'https://tanatel.sa/index.php?route=product/category&path=64_65_67_68'},
    {'cat1': 'غرفة نوم', 'cat2': ' غرف نوم الأطفال', 'cat3': 'سرير مفرد',  'url': 'https://tanatel.sa/index.php?route=product/category&path=64_65_67_82'},
    {'cat1': 'غرفة نوم', 'cat2': ' غرف نوم الأطفال', 'cat3': 'خزائن الملابس',  'url': 'https://tanatel.sa/index.php?route=product/category&path=64_65_67_86'},
    {'cat1': 'غرفة نوم', 'cat2': ' غرف نوم الأطفال', 'cat3': 'مكاتب الدراسة',  'url': 'https://tanatel.sa/index.php?route=product/category&path=64_65_67_85'},
    
    
    
    {'cat1': 'غرفة المعيشة', 'cat2': 'أطقم الكنب', 'cat3': '',  'url': 'https://tanatel.sa/index.php?route=product/category&path=64_69_101'},
    {'cat1': 'غرفة المعيشة', 'cat2': 'أطقم الزاوية', 'cat3': '',  'url': 'https://tanatel.sa/index.php?route=product/category&path=64_69_70'},
    {'cat1': 'غرفة المعيشة', 'cat2': 'كنبة ثلاثة مقاعد', 'cat3': '',  'url': 'https://tanatel.sa/index.php?route=product/category&path=64_69_105'},
    {'cat1': 'غرفة المعيشة', 'cat2': 'كنبة مقعدين', 'cat3': '',  'url': 'https://tanatel.sa/index.php?route=product/category&path=64_69_106'},
    {'cat1': 'غرفة المعيشة', 'cat2': 'كراسي مفردة', 'cat3': '',  'url': 'https://tanatel.sa/index.php?route=product/category&path=64_69_88'},
    {'cat1': 'غرفة المعيشة', 'cat2': 'ميني صوفا', 'cat3': '',  'url': 'https://tanatel.sa/index.php?route=product/category&path=64_69_112'},
    {'cat1': 'غرفة المعيشة', 'cat2': 'أطقم طاولات القهوة', 'cat3': '',  'url': 'https://tanatel.sa/index.php?route=product/category&path=64_69_89'},
    
    {'cat1': 'غرفة الطعام', 'cat2': 'اطقم طاولات الطعام', 'cat3': '',  'url': 'https://tanatel.sa/index.php?route=product/category&path=64_91_92'},
    {'cat1': 'غرفة الطعام', 'cat2': 'طاولات الطعام', 'cat3': '',  'url': 'https://tanatel.sa/index.php?route=product/category&path=64_91_94'},
    {'cat1': 'غرفة الطعام', 'cat2': 'كراسى طاولة الطعام', 'cat3': '',  'url': 'https://tanatel.sa/index.php?route=product/category&path=64_91_95'},
    {'cat1': 'غرفة الطعام', 'cat2': 'البوفية', 'cat3': '',  'url': 'https://tanatel.sa/index.php?route=product/category&path=64_91_96'},
    {'cat1': 'غرفة الطعام', 'cat2': 'كونسول', 'cat3': '',  'url': 'https://tanatel.sa/index.php?route=product/category&path=64_91_110'},
    {'cat1': 'الإكسسوارات', 'cat2': '', 'cat3': '',  'url': 'https://tanatel.sa/index.php?route=product/category&path=108'},
    # {'cat1': '', 'cat2': '', 'cat3': '',  'url': ''},
    # {'cat1': '', 'cat2': '', 'cat3': '',  'url': ''},
    # {'cat1': '', 'cat2': '', 'cat3': '',  'url': ''},
    # {'cat1': '', 'cat2': '', 'cat3': '',  'url': ''},
    # {'cat1': '', 'cat2': '', 'cat3': '',  'url': ''},
    # {'cat1': '', 'cat2': '', 'cat3': '',  'url': ''},
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
    products = soup.find_all('div', {'class': 'grid-item'})
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
    
    page = soup.find('a', text=re.compile('>'))
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
df = pd.read_excel('tanatel_model_url.xlsx')

for i, url in enumerate(urls):
    print('Count: ', i)
    data = scrap_url_product(url)
    df1 = pd.DataFrame(data)
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('tanatel_update_url.xlsx')
    

