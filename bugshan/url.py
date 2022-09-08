
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


def get_data(url):
    logging.info('URL: %s', url)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    cookies = {'session': '134-8225175-0355220'}
    r = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(r.content, "html.parser")
    time.sleep(1)
    products = soup.find_all('div', {'class': 'product-block'})
    liens = [toto.find('a')['href']  for toto in products]
    print('Len products', len(liens))
    return soup, liens


def getnextpage(soup):
    page = soup.find('a', {'class': 'pagination__next'})
    try:
        url2 = str(page['href'])
        return url2
    except:
        logging.info('No Next')
        pass
    return url2 


list_urls = [
    # {'cat1': 'تلفزيونات', 'cat2': 'تلفزيونات OLED', 'cat3': '', 'url': 'https://bugshan.co/ar/%D8%AA%D9%84%D9%81%D8%B2%D9%8A%D9%88%D9%86%D8%A7%D8%AA-oled/c1344902162'},
    # {'cat1': 'تلفزيونات', 'cat2': 'تلفزيونات NanoCell', 'cat3': '', 'url': 'https://bugshan.co/ar/%D8%AA%D9%84%D9%81%D8%B2%D9%8A%D9%88%D9%86%D8%A7%D8%AA-nanocell/c461705246'},
    # {'cat1': 'تلفزيونات', 'cat2': 'تلفزيونات UHD 4K', 'cat3': '', 'url': 'https://bugshan.co/ar/%D8%AA%D9%84%D9%81%D8%B2%D9%8A%D9%88%D9%86%D8%A7%D8%AA-uhd-4k/c1969372959'},
    
    # {'cat1': 'الفيديو و الأجهزة الصوتية', 'cat2': 'مكبرات الصوت', 'cat3': '', 'url': 'https://bugshan.co/ar/%D9%85%D9%83%D8%A8%D8%B1%D8%A7%D8%AA-%D8%A7%D9%84%D8%B5%D9%88%D8%AA/c711858278'},
    # {'cat1': 'الفيديو و الأجهزة الصوتية', 'cat2': 'أنظمة المسرح المنزلي', 'cat3': '', 'url': 'https://bugshan.co/ar/%D8%A3%D9%86%D8%B8%D9%85%D8%A9-%D8%A7%D9%84%D9%85%D8%B3%D8%B1%D8%AD-%D8%A7%D9%84%D9%85%D9%86%D8%B2%D9%84%D9%8A/c2111538274'},
    
    # {'cat1': 'الاجهزة المنزلية الصغيرة', 'cat2': 'مواقد و أفران صغيرة وميكروويف', 'cat3': '', 'url': 'https://bugshan.co/ar/%D9%85%D9%88%D8%A7%D9%82%D8%AF-%D9%88-%D8%A3%D9%81%D8%B1%D8%A7%D9%86-%D8%B5%D8%BA%D9%8A%D8%B1%D8%A9-%D9%88%D9%85%D9%8A%D9%83%D8%B1%D9%88%D9%88%D9%8A%D9%81/c2075654326'},
    # {'cat1': 'الاجهزة المنزلية الصغيرة', 'cat2': 'مبردات المياه', 'cat3': '', 'url': 'https://bugshan.co/ar/%D9%85%D8%A8%D8%B1%D8%AF%D8%A7%D8%AA-%D8%A7%D9%84%D9%85%D9%8A%D8%A7%D9%87/c1126393010'},
    # {'cat1': 'الاجهزة المنزلية الصغيرة', 'cat2': 'مكانس', 'cat3': '', 'url': 'https://bugshan.co/ar/%D9%85%D9%83%D8%A7%D9%86%D8%B3/c627173510'},
    # {'cat1': 'الاجهزة المنزلية الصغيرة', 'cat2': 'كاويات', 'cat3': '', 'url': 'https://bugshan.co/ar/%D9%83%D8%A7%D9%88%D9%8A%D8%A7%D8%AA/c2001663879'},
    # {'cat1': 'الاجهزة المنزلية الصغيرة', 'cat2': 'فرامات', 'cat3': '', 'url': 'https://bugshan.co/ar/%D9%81%D8%B1%D8%A7%D9%85%D8%A7%D8%AA/c2009921177'},
    # {'cat1': 'الاجهزة المنزلية الصغيرة', 'cat2': 'مطاحن', 'cat3': '', 'url': 'https://bugshan.co/ar/%D9%85%D8%B7%D8%A7%D8%AD%D9%86/c1355849008'},
    # {'cat1': 'الاجهزة المنزلية الصغيرة', 'cat2': 'غلايات', 'cat3': '', 'url': 'https://bugshan.co/ar/%D8%BA%D9%84%D8%A7%D9%8A%D8%A7%D8%AA/c434139249'},
    # {'cat1': 'الاجهزة المنزلية الصغيرة', 'cat2': 'مراوح', 'cat3': '', 'url': 'https://bugshan.co/ar/%D9%85%D8%B1%D8%A7%D9%88%D8%AD/c303942675'},
    # {'cat1': 'الاجهزة المنزلية الصغيرة', 'cat2': 'مصيدة الحشرات', 'cat3': '', 'url': 'https://bugshan.co/ar/%D9%85%D8%B5%D9%8A%D8%AF%D8%A9-%D8%A7%D9%84%D8%AD%D8%B4%D8%B1%D8%A7%D8%AA/c406381952'},
    
    # {'cat1': 'الأجهزة المنزلية الكبيرة', 'cat2': 'ثلاجات', 'cat3': '', 'url': 'https://bugshan.co/ar/%D8%AB%D9%84%D8%A7%D8%AC%D8%A7%D8%AA/c1348294006'},
    # {'cat1': 'الأجهزة المنزلية الكبيرة', 'cat2': 'ثلاجات العرض', 'cat3': '', 'url': 'https://bugshan.co/ar/%D8%AB%D9%84%D8%A7%D8%AC%D8%A7%D8%AA-%D8%A7%D9%84%D8%B9%D8%B1%D8%B6/c1618390107'},
    # {'cat1': 'الأجهزة المنزلية الكبيرة', 'cat2': 'فريزرات', 'cat3': '', 'url': 'https://bugshan.co/ar/%D9%81%D8%B1%D9%8A%D8%B2%D8%B1%D8%A7%D8%AA/c1240314481'},
    # {'cat1': 'الأجهزة المنزلية الكبيرة', 'cat2': 'غسالات الملابس', 'cat3': 'غسالة علوية', 'url': 'https://bugshan.co/ar/%D8%BA%D8%B3%D8%A7%D9%84%D8%A9-%D8%B9%D9%84%D9%88%D9%8A%D8%A9/c1909286'},
    # {'cat1': 'الأجهزة المنزلية الكبيرة', 'cat2': 'غسالات الملابس', 'cat3': 'غسالة حوضين', 'url': 'https://bugshan.co/ar/%D8%BA%D8%B3%D8%A7%D9%84%D8%A9-%D8%AD%D9%88%D8%B6%D9%8A%D9%86/c1576681767'},
    # {'cat1': 'الأجهزة المنزلية الكبيرة', 'cat2': 'غسالات الملابس', 'cat3': 'غسالة امامية', 'url': 'https://bugshan.co/ar/%D8%BA%D8%B3%D8%A7%D9%84%D8%A9-%D8%A7%D9%85%D8%A7%D9%85%D9%8A%D8%A9/c1345917040'},
    # {'cat1': 'الأجهزة المنزلية الكبيرة', 'cat2': 'غسالات الصحون', 'cat3': '', 'url': 'https://bugshan.co/ar/%D8%BA%D8%B3%D8%A7%D9%84%D8%A7%D8%AA-%D8%A7%D9%84%D8%B5%D8%AD%D9%88%D9%86/c466276722'},
    # {'cat1': 'الأجهزة المنزلية الكبيرة', 'cat2': 'أفران', 'cat3': '', 'url': 'https://bugshan.co/ar/%D8%A3%D9%81%D8%B1%D8%A7%D9%86/c527725682'},
    # {'cat1': 'الأجهزة المنزلية الكبيرة', 'cat2': 'مجففات', 'cat3': '', 'url': 'https://bugshan.co/ar/%D9%85%D8%AC%D9%81%D9%81%D8%A7%D8%AA/c2080412528'},
    # {'cat1': 'الأجهزة المنزلية الكبيرة', 'cat2': 'مجففات', 'cat3': '', 'url': 'https://bugshan.co/ar/%D9%85%D8%AC%D9%81%D9%81%D8%A7%D8%AA/c2080412528'},
    
    # {'cat1': 'اجهزة المطبخ', 'cat2': 'اجهزة المشروبات الساخنة', 'cat3': '', 'url': 'https://bugshan.co/ar/%D8%A7%D8%AC%D9%87%D8%B2%D8%A9-%D8%A7%D9%84%D9%85%D8%B4%D8%B1%D9%88%D8%A8%D8%A7%D8%AA-%D8%A7%D9%84%D8%B3%D8%A7%D8%AE%D9%86%D8%A9/c1517138317'},
    # {'cat1': 'اجهزة المطبخ', 'cat2': 'اجهزة تحضير الطعام', 'cat3': '', 'url': 'https://bugshan.co/ar/%D8%A7%D8%AC%D9%87%D8%B2%D8%A9-%D8%AA%D8%AD%D8%B6%D9%8A%D8%B1-%D8%A7%D9%84%D8%B7%D8%B9%D8%A7%D9%85/c102236047'},
    # {'cat1': 'اجهزة المطبخ', 'cat2': 'الخلاطات والعصارات', 'cat3': '', 'url': 'https://bugshan.co/ar/%D8%A7%D9%84%D8%AE%D9%84%D8%A7%D8%B7%D8%A7%D8%AA-%D9%88%D8%A7%D9%84%D8%B9%D8%B5%D8%A7%D8%B1%D8%A7%D8%AA/c1409031816'},
    # {'cat1': 'اجهزة المطبخ', 'cat2': 'القلايات', 'cat3': '', 'url': 'https://bugshan.co/ar/%D8%A7%D9%84%D9%82%D9%84%D8%A7%D9%8A%D8%A7%D8%AA/c769211785'},
    
    {'cat1': 'اجهزة التكييف', 'cat2': 'مكيفات شباك', 'cat3': '', 'url': 'https://bugshan.co/ar/%D9%85%D9%83%D9%8A%D9%81%D8%A7%D8%AA-%D8%B4%D8%A8%D8%A7%D9%83/c777878650'},
    {'cat1': 'اجهزة التكييف', 'cat2': 'مكيفات اسبلت', 'cat3': '', 'url': 'https://bugshan.co/ar/%D9%85%D9%83%D9%8A%D9%81%D8%A7%D8%AA-%D8%A7%D8%B3%D8%A8%D9%84%D8%AA/c2017172347'},
    {'cat1': 'اجهزة التكييف', 'cat2': 'مكيفات دولاب', 'cat3': '', 'url': 'https://bugshan.co/ar/%D9%85%D9%83%D9%8A%D9%81%D8%A7%D8%AA-%D8%AF%D9%88%D9%84%D8%A7%D8%A8/c1241561668'},
    {'cat1': 'اجهزة التكييف', 'cat2': 'مكيفات صحراوية', 'cat3': '', 'url': 'https://bugshan.co/ar/%D9%85%D9%83%D9%8A%D9%81%D8%A7%D8%AA-%D8%B5%D8%AD%D8%B1%D8%A7%D9%88%D9%8A%D8%A9/c1844092488'},
    {'cat1': 'اجهزة التكييف', 'cat2': 'منقي الهواء', 'cat3': '', 'url': 'https://bugshan.co/ar/%D9%85%D9%86%D9%82%D9%8A-%D8%A7%D9%84%D9%87%D9%88%D8%A7%D8%A1/c1469339041'},
    {'cat1': 'اجهزة التكييف', 'cat2': 'ستارة هوائية', 'cat3': '', 'url': 'https://bugshan.co/ar/%D8%B3%D8%AA%D8%A7%D8%B1%D8%A9-%D9%87%D9%88%D8%A7%D8%A6%D9%8A%D8%A9/c1445973671'},
    
    # {'cat1': 'العناية الشخصية', 'cat2': '', 'cat3': '', 'url': 'https://bugshan.co/ar/%D8%A7%D9%84%D8%B9%D9%86%D8%A7%D9%8A%D8%A9-%D8%A7%D9%84%D8%B4%D8%AE%D8%B5%D9%8A%D8%A9/c512851578'},
    
]


def scrap_url_product(url1):
    
    cat1 = url1['cat1']
    cat2 = url1['cat2']
    cat3 = url1['cat3']
    url = url1['url']
    data = []
    while True:
        soup, urls_list = get_data(url)
        
        for url in urls_list:
            data.append({
            'url':url,
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

df = pd.read_excel('bugshan_url_model.xlsx')
for i, url in enumerate(list_urls):
    logging.info('Count: %s', i)
    data = scrap_url_product(url)
    df1 = pd.DataFrame(data)
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('bugshan_url_update.xlsx')
logging.info('Scraping URL Done.')

