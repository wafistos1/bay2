from bs4 import BeautifulSoup
from selenium.webdriver.support import ui
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
    {'cat1': 'ثريات', 'cat2': 'ثريات مودرن', 'cat3': '', 'url': 'https://fanos.com.sa/%D8%AB%D8%B1%D9%8A%D8%A7%D8%AA-%D9%85%D9%88%D8%AF%D8%B1%D9%86/c1256552134'}, 
    {'cat1': 'ثريات', 'cat2': ' ثريات ستايل أوروبي', 'cat3': '', 'url': 'https://fanos.com.sa/%D8%AB%D8%B1%D9%8A%D8%A7%D8%AA-%D8%B3%D8%AA%D8%A7%D9%8A%D9%84-%D8%A3%D9%88%D8%B1%D9%88%D8%A8%D9%8A/c1601071093'}, 
     {'cat1': ' ثريات', 'cat2': 'ثريات سقف كلاسيك', 'cat3': '', 'url': 'https://fanos.com.sa/%D8%AB%D8%B1%D9%8A%D8%A7%D8%AA-%D8%B3%D9%82%D9%81-%D9%83%D9%84%D8%A7%D8%B3%D9%8A%D9%83/c651944945'}, 
     {'cat1': ' ثريات', 'cat2': 'ثريات مداخل', 'cat3': '', 'url': 'https://fanos.com.sa/%D8%AB%D8%B1%D9%8A%D8%A7%D8%AA-%D9%85%D8%AF%D8%A7%D8%AE%D9%84/c1143810714'}, 
     {'cat1': ' ثريات', 'cat2': 'ثريات خشبية', 'cat3': '', 'url': 'https://fanos.com.sa/ثريات-خشبية/c1425982704'}, 
     {'cat1': ' ثريات', 'cat2': 'ثريات ريفية', 'cat3': '', 'url': 'https://fanos.com.sa/%D8%AB%D8%B1%D9%8A%D8%A7%D8%AA-%D8%B1%D9%8A%D9%81%D9%8A%D8%A9/c1628564004'}, 
     {'cat1': ' ثريات', 'cat2': 'ثريات قبب', 'cat3': '', 'url': 'https://fanos.com.sa/%D8%AB%D8%B1%D9%8A%D8%A7%D8%AA-%D9%82%D8%A8%D8%A8/c1889534706'}, 
     {'cat1': ' ثريات', 'cat2': 'ثريات تراثية', 'cat3': '', 'url': 'https://fanos.com.sa/%D8%AB%D8%B1%D9%8A%D8%A7%D8%AA-%D8%AA%D8%B1%D8%A7%D8%AB%D9%8A%D8%A9/c2064754167'}, 
     {'cat1': ' ثريات', 'cat2': 'ثريات لطش', 'cat3': '', 'url': 'https://fanos.com.sa/%D8%AB%D8%B1%D9%8A%D8%A7%D8%AA-%D9%84%D8%B7%D8%B4/c1116545523'}, 
     {'cat1': ' ثريات', 'cat2': 'ثريات غرف نوم', 'cat3': '', 'url': 'https://fanos.com.sa/%D8%AB%D8%B1%D9%8A%D8%A7%D8%AA-%D8%BA%D8%B1%D9%81-%D9%86%D9%88%D9%85/c691308278'}, 
     {'cat1': ' ثريات', 'cat2': 'ثريات مفرد', 'cat3': '', 'url': 'https://fanos.com.sa/%D8%AB%D8%B1%D9%8A%D8%A7%D8%AA-%D9%85%D9%81%D8%B1%D8%AF/c476725500'}, 
 
    
    {'cat1': 'لمبات', 'cat2': 'لمبات ديكور - فيلمونت', 'cat3': '', 'url': 'https://fanos.com.sa/%D9%84%D9%85%D8%A8%D8%A7%D8%AA-%D8%AF%D9%8A%D9%83%D9%88%D8%B1-%D9%81%D9%8A%D9%84%D9%85%D9%88%D9%86%D8%AA/c1570592366'}, 
    {'cat1': 'لمبات', 'cat2': 'لمبات ليد - فيلمونت', 'cat3': '', 'url': 'https://fanos.com.sa/%D9%84%D9%85%D8%A8%D8%A7%D8%AA-%D9%84%D9%8A%D8%AF-%D9%81%D9%8A%D9%84%D9%85%D9%88%D9%86%D8%AA/c644406558'}, 
    {'cat1': 'لمبات', 'cat2': 'لمبات كروية', 'cat3': '', 'url': 'https://fanos.com.sa/%D9%84%D9%85%D8%A8%D8%A7%D8%AA-%D9%83%D8%B1%D9%88%D9%8A%D8%A9/c1006208166'}, 
    {'cat1': 'لمبات', 'cat2': 'لمبات مستودعات كبيرة', 'cat3': '', 'url': 'https://fanos.com.sa/%D9%84%D9%85%D8%A8%D8%A7%D8%AA-%D9%85%D8%B3%D8%AA%D9%88%D8%AF%D8%B9%D8%A7%D8%AA-%D9%83%D8%A8%D9%8A%D8%B1%D8%A9/c473319076'}, 
    
    {'cat1': 'إنارة جدارية', 'cat2': 'اضاءات جدارية مودرن', 'cat3': '', 'url': 'https://fanos.com.sa/%D8%A7%D8%B6%D8%A7%D8%A1%D8%A7%D8%AA-%D8%AC%D8%AF%D8%A7%D8%B1%D9%8A%D8%A9-%D9%85%D9%88%D8%AF%D8%B1%D9%86/c1749597679'}, 
    {'cat1': 'إنارة جدارية', 'cat2': 'إنارة جدارية كلاسيك', 'cat3': '', 'url': 'https://fanos.com.sa/%D8%A5%D9%86%D8%A7%D8%B1%D8%A9-%D8%AC%D8%AF%D8%A7%D8%B1%D9%8A%D8%A9-%D9%83%D9%84%D8%A7%D8%B3%D9%8A%D9%83/c1283817453https://fanos.com.sa/%D8%A5%D9%86%D8%A7%D8%B1%D8%A9-%D8%AC%D8%AF%D8%A7%D8%B1%D9%8A%D8%A9-%D8%A7%D9%88%D8%B1%D9%88%D8%A8%D9%8A/c1458967266'}, 
    {'cat1': 'إنارة جدارية', 'cat2': 'إنارة جدارية اوروبي', 'cat3': '', 'url': 'https://fanos.com.sa/%D8%A5%D9%86%D8%A7%D8%B1%D8%A9-%D8%AC%D8%AF%D8%A7%D8%B1%D9%8A%D8%A9-%D8%A7%D9%88%D8%B1%D9%88%D8%A8%D9%8A/c1458967266'}, 
    {'cat1': 'إنارة جدارية', 'cat2': 'اضاءة خشبية', 'cat3': '', 'url': 'https://fanos.com.sa/%D8%A7%D8%B6%D8%A7%D8%A1%D8%A9-%D8%AE%D8%B4%D8%A8%D9%8A%D8%A9/c86635489'}, 
    {'cat1': 'إنارة جدارية', 'cat2': 'إنارة مغاسل ومداخل', 'cat3': '', 'url': 'https://fanos.com.sa/%D8%A5%D9%86%D8%A7%D8%B1%D8%A9-%D9%85%D8%BA%D8%A7%D8%B3%D9%84-%D9%88%D9%85%D8%AF%D8%A7%D8%AE%D9%84/c509845230'}, 
    {'cat1': 'إنارة جدارية', 'cat2': 'إنارة تراثية', 'cat3': '', 'url': 'https://fanos.com.sa/%D8%A5%D9%86%D8%A7%D8%B1%D8%A9-%D8%AA%D8%B1%D8%A7%D8%AB%D9%8A%D8%A9/c550711779'}, 
    {'cat1': 'إنارة جدارية', 'cat2': 'إنارة غرف نوم', 'cat3': '', 'url': 'https://fanos.com.sa/%D8%A5%D9%86%D8%A7%D8%B1%D8%A9-%D8%BA%D8%B1%D9%81-%D9%86%D9%88%D9%85/c726455520'}, 
    {'cat1': 'إنارة جدارية', 'cat2': 'إنارة زجاجية', 'cat3': '', 'url': 'https://fanos.com.sa/%D8%A5%D9%86%D8%A7%D8%B1%D8%A9-%D8%B2%D8%AC%D8%A7%D8%AC%D9%8A%D8%A9/c1924681964'}, 
    
    {'cat1': 'إنارة داخلية', 'cat2': 'أبجورات', 'cat3': '', 'url': 'https://fanos.com.sa/%D8%A3%D8%A8%D8%AC%D9%88%D8%B1%D8%A7%D8%AA/c1675061476'}, 
    {'cat1': 'إنارة داخلية', 'cat2': 'إنارة مكاتب', 'cat3': '', 'url': 'https://fanos.com.sa/%D8%A7%D9%86%D8%A7%D8%B1%D8%A9---%D8%AE%D8%B7%D9%8A%D8%A9/c1812954177'}, 
    {'cat1': 'إنارة داخلية', 'cat2': 'إضاءة توجيه', 'cat3': '', 'url': 'https://fanos.com.sa/%D8%A5%D8%B6%D8%A7%D8%A1%D8%A9-%D8%AA%D9%88%D8%AC%D9%8A%D9%87/c585759703'}, 
    {'cat1': 'إنارة داخلية', 'cat2': 'إنارة درج', 'cat3': '', 'url': 'https://fanos.com.sa/%D8%A7%D9%86%D8%A7%D8%B1%D8%A9-%D8%AF%D8%B1%D8%AC/c1050183536'}, 
    {'cat1': 'إنارة داخلية', 'cat2': 'شريط زينة', 'cat3': '', 'url': 'https://fanos.com.sa/%D8%B4%D8%B1%D9%8A%D8%B7-%D8%B2%D9%8A%D9%86%D8%A9/c287805120'}, 
    {'cat1': 'إنارة داخلية', 'cat2': 'أسلاك قماشية', 'cat3': '', 'url': 'https://fanos.com.sa/%D8%A3%D8%B3%D9%84%D8%A7%D9%83-%D9%82%D9%85%D8%A7%D8%B4%D9%8A%D8%A9/c293231856'}, 
    
    {'cat1': 'إنارة خارجية', 'cat2': 'إنارة حدائق', 'cat3': '', 'url': 'https://fanos.com.sa/%D8%A5%D9%86%D8%A7%D8%B1%D8%A9-%D8%AD%D8%AF%D8%A7%D8%A6%D9%82/c410774680'}, 
    {'cat1': 'إنارة خارجية', 'cat2': 'إنارة جدارية خارجية', 'cat3': '', 'url': 'https://fanos.com.sa/%D8%A5%D9%86%D8%A7%D8%B1%D8%A9-%D8%AC%D8%AF%D8%A7%D8%B1%D9%8A%D8%A9-%D8%AE%D8%A7%D8%B1%D8%AC%D9%8A%D8%A9/c1837529598'}, 
    {'cat1': 'إنارة خارجية', 'cat2': 'كشافات خارجية', 'cat3': '', 'url': 'https://fanos.com.sa/%D9%83%D8%B4%D8%A7%D9%81%D8%A7%D8%AA-%D8%AE%D8%A7%D8%B1%D8%AC%D9%8A%D8%A9/c1782582169'}, 
    
    {'cat1': 'سبوت لايت', 'cat2': 'سبوت لايت ليد', 'cat3': '', 'url': 'https://fanos.com.sa/%D8%B3%D8%A8%D9%88%D8%AA-%D9%84%D8%A7%D9%8A%D8%AA-%D9%84%D9%8A%D8%AF/c605300743'}, 
    {'cat1': 'سبوت لايت', 'cat2': 'فريم سبوت لايت', 'cat3': '', 'url': 'https://fanos.com.sa/%D9%81%D8%B1%D9%8A%D9%85-%D8%B3%D8%A8%D9%88%D8%AA-%D9%84%D8%A7%D9%8A%D8%AA/c1246693638'}, 
    {'cat1': 'سبوت لايت', 'cat2': 'لمبات سبوت لايت', 'cat3': '', 'url': 'https://fanos.com.sa/%D9%84%D9%85%D8%A8%D8%A7%D8%AA-%D8%B3%D8%A8%D9%88%D8%AA-%D9%84%D8%A7%D9%8A%D8%AA/c784343649'}, 
    {'cat1': 'سبوت لايت', 'cat2': 'فريم ضد التوهج - المنيوم', 'cat3': '', 'url': 'https://fanos.com.sa/%D9%81%D8%B1%D9%8A%D9%85-%D8%B6%D8%AF-%D8%A7%D9%84%D8%AA%D9%88%D9%87%D8%AC-%D8%A7%D9%84%D9%85%D9%86%D9%8A%D9%88%D9%85/c1945599595'}, 
    {'cat1': 'سبوت لايت', 'cat2': 'فريم ضد التوهج - بلاستيك', 'cat3': '', 'url': 'https://fanos.com.sa/%D9%81%D8%B1%D9%8A%D9%85-%D8%B6%D8%AF-%D8%A7%D9%84%D8%AA%D9%88%D9%87%D8%AC-%D8%A8%D9%84%D8%A7%D8%B3%D8%AA%D9%8A%D9%83/c780520196'}, 
    
    
    {'cat1': 'مفاتيح و أفياش', 'cat2': 'برلنت أسود', 'cat3': '', 'url': 'https://fanos.com.sa/%D8%A8%D8%B1%D9%84%D9%86%D8%AA-%D8%A3%D8%B3%D9%88%D8%AF/c616797639'}, 
    {'cat1': 'مفاتيح و أفياش', 'cat2': 'برلنت ذهبي', 'cat3': '', 'url': 'https://fanos.com.sa/%D8%A8%D8%B1%D9%84%D9%86%D8%AA-%D8%B0%D9%87%D8%A8%D9%8A/c1990767808'}, 
    {'cat1': 'مفاتيح و أفياش', 'cat2': 'برلنت رمادي', 'cat3': '', 'url': 'https://fanos.com.sa/%D8%A8%D8%B1%D9%84%D9%86%D8%AA-%D8%B1%D9%85%D8%A7%D8%AF%D9%8A/c1081463745'}, 
    {'cat1': 'مفاتيح و أفياش', 'cat2': 'برلنت لؤلؤي', 'cat3': '', 'url': 'https://fanos.com.sa/%D8%A8%D8%B1%D9%84%D9%86%D8%AA-%D9%84%D8%A4%D9%84%D8%A4%D9%8A/c307425986'}, 
    {'cat1': 'مفاتيح و أفياش', 'cat2': 'فانوس ذهبي', 'cat3': '', 'url': 'https://fanos.com.sa/%D9%81%D8%A7%D9%86%D9%88%D8%B3-%D8%B0%D9%87%D8%A8%D9%8A/c1816072643'}, 
    {'cat1': 'مفاتيح و أفياش', 'cat2': 'شفاطات', 'cat3': '', 'url': 'https://fanos.com.sa/%D8%B4%D9%81%D8%A7%D8%B7%D8%A7%D8%AA/c69288671'}, 
    
    {'cat1': 'الإنارة المخفية', 'cat2': 'شريط الإنارة LED', 'cat3': '', 'url': 'https://fanos.com.sa/%D8%B4%D8%B1%D9%8A%D8%B7-%D8%A7%D9%84%D8%A5%D9%86%D8%A7%D8%B1%D8%A9-led/c251106295'}, 
    {'cat1': 'الإنارة المخفية', 'cat2': 'مجرى ألمنيوم لطش', 'cat3': '', 'url': 'https://fanos.com.sa/%D9%85%D8%AC%D8%B1%D9%89-%D8%A3%D9%84%D9%85%D9%86%D9%8A%D9%88%D9%85-%D9%84%D8%B7%D8%B4/c1946968871'}, 
    {'cat1': 'الإنارة المخفية', 'cat2': 'المجرى الألمنيوم الأرضي', 'cat3': '', 'url': 'https://fanos.com.sa/%D8%A7%D9%84%D9%85%D8%AC%D8%B1%D9%89-%D8%A7%D9%84%D8%A3%D9%84%D9%85%D9%86%D9%8A%D9%88%D9%85-%D8%A7%D9%84%D8%A3%D8%B1%D8%B6%D9%8A/c716820977'}, 
    {'cat1': 'الإنارة المخفية', 'cat2': 'المجرى الألمنيوم داخل السقف أو الحائط', 'cat3': '', 'url': 'https://fanos.com.sa/%D8%A7%D9%84%D9%85%D8%AC%D8%B1%D9%89-%D8%A7%D9%84%D8%A3%D9%84%D9%85%D9%86%D9%8A%D9%88%D9%85-%D8%AF%D8%A7%D8%AE%D9%84-%D8%A7%D9%84%D8%B3%D9%82%D9%81-%D8%A3%D9%88-%D8%A7%D9%84%D8%AD%D8%A7%D8%A6%D8%B7/c1806023416'}, 
    {'cat1': 'الإنارة المخفية', 'cat2': 'مجرى الألمنيوم الزاوية', 'cat3': '', 'url': 'https://fanos.com.sa/%D9%85%D8%AC%D8%B1%D9%89-%D8%A7%D9%84%D8%A3%D9%84%D9%85%D9%86%D9%8A%D9%88%D9%85-%D8%A7%D9%84%D8%B2%D8%A7%D9%88%D9%8A%D8%A9/c217990597'}, 
    {'cat1': 'الإنارة المخفية', 'cat2': 'مجرى الألمنيوم كورنيش', 'cat3': '', 'url': 'https://fanos.com.sa/%D9%85%D8%AC%D8%B1%D9%89-%D8%A7%D9%84%D8%A3%D9%84%D9%85%D9%86%D9%8A%D9%88%D9%85-%D9%83%D9%88%D8%B1%D9%86%D9%8A%D8%B4/c1880952771'}, 
    {'cat1': 'الإنارة المخفية', 'cat2': 'ملحقات شريط الإنارة', 'cat3': '', 'url': 'https://fanos.com.sa/%D9%85%D9%84%D8%AD%D9%82%D8%A7%D8%AA-%D8%B4%D8%B1%D9%8A%D8%B7-%D8%A7%D9%84%D8%A5%D9%86%D8%A7%D8%B1%D8%A9/c75952370'}, 
    
    {'cat1': 'اضاءة مسابح', 'cat2': 'كشافات مسابح', 'cat3': '', 'url': 'https://fanos.com.sa/%D9%83%D8%B4%D8%A7%D9%81%D8%A7%D8%AA-%D9%85%D8%B3%D8%A7%D8%A8%D8%AD/c1337736269'}, 
]

options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')
#opti#     driver = webdriver.Firefox()ons.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)

def get_data(url, next_page):
    if not next_page:
        driver.get(url)
    r = driver.find_element_by_tag_name('body').get_attribute('innerHTML')
    soup = BeautifulSoup(r, 'html.parser')
    time.sleep(1)
    products = soup.find_all('div', {'class': 'product-block contain'})
    len(products)
    liens = [toto.find('a')['href']  for toto in products]
    print('Len products', len(liens))
    list_liens = []
    
    for t in liens:
        list_liens.append(t)
    return soup, list_liens


def getnextpage(soup):

    shoesize = ui.WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/section[3]/div/div/div/div[3]')))
    shoesize.click()



list_urls = []


def scrap_url_product(url1):
    
    cat1 = url1['cat1']
    cat2 = url1['cat2']
    cat3 = url1['cat3']
    url = url1['url']
    data = []
    print(cat1, cat2, cat3)
    next_page = False
    while True:
        soup, urls_list = get_data(url, next_page)
        for toto in urls_list:
            # print(f'URL:', toto)
            data.append({
            'url':toto,
            'cat1': cat1,
            'cat2': cat2,
            'cat3': cat3,
            })

        try:
            shoesize = ui.WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/section[3]/div/div/div/div[3]')))
            shoesize.click()
            next_page = True
#            
        except:
            break
    print( f'Scrape done .')
    return data

df = pd.read_excel('fanos_url_model.xlsx')

for i, url in enumerate(urls):
    print('Count: ', i)
    data = scrap_url_product(url)
    df1 = pd.DataFrame(data)
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('fanos_url_update.xlsx')