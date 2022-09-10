
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
    products = soup.find_all('div', {'class': 'collection__item'})
    liens =  [ 'https://knothome.com' + toto.find('a')['href']  for toto in products]
    
    print('Len products', len(liens))
    return len(liens), liens


def getnextpage(soup):
    page = soup.find('a', {'class': 'next i-next'})
    
    try:
        url2 = str(page['href'])
        return url2
    except:
        print('No Next')
        pass
    return url2 


list_urls = [
    # {'cat1': 'الإكسسوارات', 'cat2': 'المزهريات والعبوات والجرات', 'cat3': '', 'url': 'https://knothome.com/collections/vases-canisters-jars'},
    # {'cat1': 'الإكسسوارات', 'cat2': 'صناديق للديكور', 'cat3': '', 'url': 'https://knothome.com/collections/box'},
    # {'cat1': 'الإكسسوارات', 'cat2': 'الصواني-لوحات-وحاملات الشموع', 'cat3': '', 'url': 'https://knothome.com/collections/trays-plates-candle-holders'},
    # {'cat1': 'الإكسسوارات', 'cat2': 'كراسي للديكور', 'cat3': '', 'url': 'https://knothome.com/collections/stools'},
    # {'cat1': 'الإكسسوارات', 'cat2': 'تماثيل ومنحوتات', 'cat3': '', 'url': 'https://knothome.com/collections/statues-and-sculptures'},
    {'cat1': 'وسائد', 'cat2': 'حزم وسائد مصممة', 'cat3': '', 'url': 'https://knothome.com/collections/designer-bundles'},
    {'cat1': 'وسائد', 'cat2': 'وسائد مفردة', 'cat3': '', 'url': 'https://knothome.com/collections/single-cushions'},
    # {'cat1': 'السجاد', 'cat2': '', 'cat3': '', 'url': 'https://knothome.com/collections/carpets-rugs'},
    # {'cat1': 'اضواء', 'cat2': 'مصابيح الطاولة', 'cat3': '', 'url': 'https://knothome.com/collections/table-lamps'},
    # {'cat1': 'اضواء', 'cat2': 'مصابيح أرضية', 'cat3': '', 'url': 'https://knothome.com/collections/floor-lamps'},
    
    # {'cat1': '', 'cat2': '', 'cat3': '', 'url': ''},
]


def scrap_url_product(url1):
    
    cat1 = url1['cat1']
    cat2 = url1['cat2']
    cat3 = url1['cat3']
    url = url1['url']
    data = []
    count = 1
    while True:
        len_list, urls_list = get_data(url)
        
        for toto in urls_list:
            data.append({
            'url':toto,
            'cat1': cat1,
            'cat2': cat2,
            'cat3': cat3,
            })
        if len_list != 0:
            count += 1
            url = url.split('?')[0] + f'page={count}'
            
        else:
            logging.info('Next URL')
            break
    logging.info( 'Scrape Categories Done --> Next .')
    return data
df = pd.read_csv('knothhome_url_model.csv')
for i, url in enumerate(list_urls):
    logging.info('Count: %s', i)
    data = scrap_url_product(url)
    df1 = pd.DataFrame(data)
    df = pd.concat([df, df1], ignore_index=True)
    df.to_csv('knothhome_url_mupdate.csv')
logging.info('Scraping URL Done.')

