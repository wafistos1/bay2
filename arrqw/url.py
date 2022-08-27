

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


urls = [
    # {'cat1': 'مكيفات هواء', 'cat2': 'مكيفات شباك', 'cat3': '', 'url': 'https://www.arrqw.com/ar/shop/category/air-conditioning-window-ac-8'},
    {'cat1': 'مكيفات هواء', 'cat2': 'مكيفات سبيلت', 'cat3': '', 'url': 'https://www.arrqw.com/ar/shop/category/air-conditioning-split-ac-7'},
    # {'cat1': 'مكيفات هواء', 'cat2': 'دولابي ومركزية', 'cat3': '', 'url': 'https://www.arrqw.com/ar/shop/category/air-conditioning-floor-standing-9'},
    # {'cat1': 'مكيفات هواء', 'cat2': 'مكيفات كاسيت', 'cat3': '', 'url': 'https://www.arrqw.com/ar/shop/category/air-conditioning-cassette-ac-10'},
    # {'cat1': 'مكيفات هواء', 'cat2': 'مكيفات مخفية', 'cat3': '', 'url': 'https://www.arrqw.com/ar/shop/category/air-conditioning-duct-concealing-11'},
    # {'cat1': 'مكيفات هواء', 'cat2': 'ستائر هوائية', 'cat3': '', 'url': 'https://www.arrqw.com/ar/shop/category/air-conditioning-air-curtain-13'},
    # {'cat1': 'مكيفات هواء', 'cat2': 'مكيفات متنقلة', 'cat3': '', 'url': 'https://www.arrqw.com/ar/shop/category/air-conditioning-portable-ac-14'},
    # {'cat1': 'مكيفات هواء', 'cat2': 'مكيفات صحراوية', 'cat3': '', 'url': 'https://www.arrqw.com/ar/shop/category/air-conditioning-desert-ac-15'},
    # # {'cat1': 'مكيفات هواء', 'cat2': '', 'cat3': '', 'url': ''},
    # # {'cat1': 'مكيفات هواء', 'cat2': '', 'cat3': '', 'url': ''},
    
    
    
    # {'cat1': 'أجهزة كبيرة', 'cat2': 'أفران  وبوتجازات وميكرويف', 'cat3': '', 'url': 'https://www.arrqw.com/ar/shop/category/jhz-kbyr-frn-wbwtjzt-wmykrwyf-17'},
    # {'cat1': 'أجهزة كبيرة', 'cat2': 'غسالات ونشافات', 'cat3': '', 'url': 'https://www.arrqw.com/ar/shop/category/arge-appliances-washers-dryers-18'},
    # {'cat1': 'أجهزة كبيرة', 'cat2': 'ثلاجات', 'cat3': '', 'url': 'https://www.arrqw.com/ar/shop/category/refrigerators-19'},
    # {'cat1': 'أجهزة كبيرة', 'cat2': 'فريزرات', 'cat3': '', 'url': 'https://www.arrqw.com/ar/shop/category/large-appliances-freezers-20'},
    # # {'cat1': 'أجهزة كبيرة', 'cat2': '', 'cat3': '', 'url': ''},
    # # {'cat1': 'أجهزة كبيرة', 'cat2': '', 'cat3': '', 'url': ''},
    # # {'cat1': 'أجهزة كبيرة', 'cat2': '', 'cat3': '', 'url': ''},
    
    
    # {'cat1': 'تلفزيونات', 'cat2': 'تلفزيونات جوجل', 'cat3': 'تلفزيونات 4 كيه', 'url': 'https://www.arrqw.com/ar/shop/category/tlfzywnt-tlfzywnt-jwjl-tlfzywnt-4-kyh-3'},
    # {'cat1': 'تلفزيونات', 'cat2': 'تلفزيونات جوجل', 'cat3': 'تلفزيونات كيو ليد', 'url': 'https://www.arrqw.com/ar/shop/category/tlfzywnt-tlfzywnt-jwjl-tlfzywnt-kyw-lyd-4'},
    # {'cat1': 'تلفزيونات', 'cat2': 'تلفزيونات  اندرويد AOSP', 'cat3': '', 'url': 'https://www.arrqw.com/ar/shop/category/tlfzywnt-tlfzywnt-ndrwyd-aosp-43'},
    # {'cat1': 'تلفزيونات', 'cat2': 'تلفزيونات فيدا', 'cat3': '', 'url': 'https://www.arrqw.com/ar/shop/category/tlfzywnt-tlfzywnt-fyd-44'},



    # {'cat1': 'أجهزة صغيرة', 'cat2': 'مكانس', 'cat3': '', 'url': 'https://www.arrqw.com/ar/shop/category/jhz-sgyr-mkns-22'},
    # {'cat1': 'أجهزة صغيرة', 'cat2': 'مبردات مياة', 'cat3': '', 'url': 'https://www.arrqw.com/ar/shop/category/jhz-sgyr-mbrdt-my-23'},
    # {'cat1': 'أجهزة صغيرة', 'cat2': 'مكاوى', 'cat3': '', 'url': 'https://www.arrqw.com/ar/shop/category/jhz-sgyr-mkw-24'},
    # {'cat1': 'أجهزة صغيرة', 'cat2': 'غلايات مياه', 'cat3': '', 'url': 'https://www.arrqw.com/ar/shop/category/jhz-sgyr-glyt-myh-25'},
    # {'cat1': 'أجهزة صغيرة', 'cat2': 'صواعق حشرات', 'cat3': '', 'url': 'https://www.arrqw.com/ar/shop/category/jhz-sgyr-sw-q-hshrt-26'},
    # {'cat1': 'أجهزة صغيرة', 'cat2': 'حلل الطهي بالبخار', 'cat3': '', 'url': 'https://www.arrqw.com/ar/shop/category/jhz-sgyr-hll-lthy-blbkhr-27'},
    # {'cat1': 'أجهزة صغيرة', 'cat2': 'Heater', 'cat3': '', 'url': 'https://www.arrqw.com/ar/shop/category/jhz-sgyr-heater-39'},
    # {'cat1': 'أجهزة صغيرة', 'cat2': 'الأجهزة الصغيرة-محضر الطعام', 'cat3': '', 'url': 'https://www.arrqw.com/ar/shop/category/jhz-sgyr-ljhz-lsgyr-mhdr-lt-m-40'},
    
    # {'cat1': 'أجهزة طبية', 'cat2': '', 'cat3': '', 'url': 'https://www.arrqw.com/ar/shop/category/jhz-tby-34'},

]


def get_data(url):
    logging.info('--URL: %s', url)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    cookies = {'session': '134-8225175-0355220'}
    r = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(r.content, "html.parser")
    time.sleep(1)
    products = soup.find_all('a', {'itemprop': 'url'})
    
    liens = ['https://www.arrqw.com' + toto['href']  for toto in products]
    logging.info('Len products %s', len(liens))
    list_liens = []
    
    for t in liens:
        list_liens.append(t)
    return soup, list_liens


def getnextpage(soup):
    try:
        page = soup.find('a', text=re.compile('التالي'))
        print()
        url2 = str(page['href'])
    except:
        url2 = ''
    return url2 

list_urls = []


def scrap_url_product(url1):
    cat1 = url1['cat1']
    cat2 = url1['cat2']
    cat3 = url1['cat3']
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
            'cat3': cat3,
            })

        url = getnextpage(soup)
        if url == '':
            break
        url = 'https://www.arrqw.com' + url 
    # print(data)
    logging.info('Scrape Done next elements.')
    return data

df = pd.read_excel('arrqw_url_model.xlsx')
for i, url in enumerate(urls):
    logging.info('Count: %s', i)
    data = scrap_url_product(url)
    df1 = pd.DataFrame(data)
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('arrqw_url_update.xlsx')

