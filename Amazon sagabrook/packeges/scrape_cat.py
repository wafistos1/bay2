import pandas as pd
import numpy as np
import re
from requests_html import HTMLSession
from bs4 import BeautifulSoup
# from packeges.scrape_cat import PROXY_LIST
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
import time
import os
from fake_useragent import UserAgent

# create selenium driver
options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')
# options.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)
 
HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64)AppleWebKit/537.36 (KHTML, like Gecko)Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
    
# toto  = 'https://www.amazon.com/stores/page/672D8BB4-D558-45CA-91B7-C71DB374E41B' 
# r = requests.get(toto, headers=headers)
# soup = BeautifulSoup(r.text, 'html.parser')

urls = [
    'https://www.amazon.com/stores/page/672D8BB4-D558-45CA-91B7-C71DB374E41B',
    'https://www.amazon.com/stores/page/6175307D-F540-4718-B226-763DF2677D0A',
    'https://www.amazon.com/stores/page/D700D9F0-5891-45D8-BA52-2B0B96D43EF7',
    'https://www.amazon.com/stores/page/1138F7DF-0F4A-450B-B250-9B91818796EE',
    'https://www.amazon.com/stores/page/4B487A21-7703-4DD8-9292-FF312DDBF830',
    
    'https://www.amazon.com/stores/page/68DB4254-09D8-4602-80EA-920D6EFC2E7C',
    'https://www.amazon.com/stores/page/B4F2EBAF-4FE1-47D6-8115-62EC6712738C',
    'https://www.amazon.com/stores/page/B6EFED1A-24B3-4CA9-B966-7742ABA27C69',
    'https://www.amazon.com/stores/page/0E4ECBA5-B1C8-4483-AD2C-2E5204E11679',
    'https://www.amazon.com/stores/page/3902F47A-1281-437D-8C48-FCA9CF8BAE3C',
    'https://www.amazon.com/stores/page/6175307D-F540-4718-B226-763DF2677D0A',
    'https://www.amazon.com/stores/page/BB4276ED-D0A5-4104-91B0-1386753F20D2',
    'https://www.amazon.com/stores/page/6E430BD1-B340-4D4D-8A67-14B425CB8F4A',
    'https://www.amazon.com/stores/page/9C397C17-5082-45C2-A4D2-F14997F1F744',
    'https://www.amazon.com/stores/page/807D5A55-E7D3-446C-934E-CE79496FCAC8',
    'https://www.amazon.com/stores/page/A05B7ADA-83A5-4939-B80B-37D9BB9A63C1',
    'https://www.amazon.com/stores/page/7CFFF63C-408D-4DEA-91CF-A94DA8DBDF0B',
    
    'https://www.amazon.com/stores/page/807D5A55-E7D3-446C-934E-CE79496FCAC8',
    # 'https://www.amazon.com/stores/page/B6EFED1A-24B3-4CA9-B966-7742ABA27C69',
    'https://www.amazon.com/stores/page/EEDE149E-40AA-4B0F-8767-C242437816D2',
    'https://www.amazon.com/stores/page/672D8BB4-D558-45CA-91B7-C71DB374E41B',
    'https://www.amazon.com/stores/page/5FEB4802-8E97-4D54-830A-D918DAFD9AAE',
    'https://www.amazon.com/stores/page/81C1A6F9-B8C8-479D-A369-D7677D07A2BC',
    'https://www.amazon.com/stores/page/EEDE149E-40AA-4B0F-8767-C242437816D2',
    'https://www.amazon.com/stores/page/3C56334D-BD63-4912-964F-766E2E374BBB',
    'https://www.amazon.com/stores/page/BFC1689F-EAEF-4D21-8FE9-C4375A07BFAE',
    'https://www.amazon.com/stores/page/0A2954D7-41D0-4400-A444-DC57E96AB909',
    'https://www.amazon.com/stores/page/574C9CC0-E2A7-4E89-9CA0-594BFCAEE528',
   
    'https://www.amazon.com/stores/page/A05B7ADA-83A5-4939-B80B-37D9BB9A63C1',
    'https://www.amazon.com/stores/page/64E9A5CD-31C4-4767-A97C-74C236FBC217',
    'https://www.amazon.com/stores/page/B9CE05B6-7D49-44AE-96FF-008FBF513F2B',
    'https://www.amazon.com/stores/page/1E9D9BD2-1802-463C-BC03-93E13A0F98D1',
    'https://www.amazon.com/stores/page/E4B2A1E4-A943-460C-845D-627E42CA824F',
    'https://www.amazon.com/stores/page/D700D9F0-5891-45D8-BA52-2B0B96D43EF7',

]
product_link = []
for i, url in enumerate(urls):
    print('Count:', i)
    print('URL:', url)
    s = HTMLSession()
    
    description = ''
    manufacturer = ''   
    driver.get(url)
    time.sleep(0.5)
    try:
        btn_show_more = driver.find_element_by_xpath('//span[text()="Show more"]')
    except:
        pass
    n_scrolls = 10
    for j in range(0, n_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.3)
        try:
            btn_show_more = driver.find_element_by_xpath('//span[text()="Show more"]')
        except:
            pass
    soup = BeautifulSoup(driver.find_element_by_id('a-page').get_attribute('innerHTML'), 'html.parser')
    cats = soup.find('div', {'class': 'Header__navigationArea__2avdk Header__hasLogo__3osQs'}).find_all('span', {'class': 'style__breadcrumb__3KWWY'})
    print(len(cats))
    cat1 = cats[0].text
    cat2 = cats[1].text
    print( 'CAt1:',cat1)
    print( 'CAt2:', cat2)
    list_products = soup.find('div', {'class': 'ProductGrid__gridContainer__3889x'})
    products = list_products.find_all('li')

    print('len products', len(products))

    
    for product in products:
        try:
            link = product.find('a', href=True)['href']
        
            product_link.append({
                'url':'https://www.amazon.com/'+ product.find('a', href=True)['href'],
                'cat1': cat1,
                'cat2': cat2,
            })
        except:
            continue
df = pd.DataFrame(product_link)
df.to_excel('Segabrook_urls_product.xlsx')
print(f'Scrap url product done with {len(product_link)} products')
   