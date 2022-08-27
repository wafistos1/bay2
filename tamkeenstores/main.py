import pandas as pd
import numpy as np
import re
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup
from pandas.core.frame import DataFrame
import requests
from packeges.scrape_cat import scrape_all_categories
from packeges.scrape_product import scrape_product
from packeges.list_cat import urls_categories
import logging


logging.basicConfig(filename='scraper.log', level=logging.DEBUG, format='%(asctime)s- %(message)s', datefmt='%d-%b-%y %H:%M:%S')






# proxy = '64.124.38.140:8080'
# r = requests.get('https://tamkeenstores.com.sa/product-category/refrigerators/', proxies={'http': proxy, 'https': proxy}, timeout=10 )
# print(r.status_code)

# papi = scrape_all_categories(urls_categories)
# df = pd.DataFrame(papi)
# df.to_excel('tamkeenstores.xlsx')

df = pd.read_excel('model_tamkeenstores.xlsx')

papi_list = []
df_toto = pd.read_excel('/home/wafistos/Documents/Projects/scaping_wafi/tamkeenstores/packeges/tamkeenstores.xlsx')
for index, row in df_toto.iterrows():
    papi_list.append({
        'url': row['url'],
        'cat1': row['cat1'],
        'cat2': row['cat2'],
        'cat3': row['cat3'],
    })

for i, tt in enumerate(papi_list[465:]):
    print('Count:', i)
    df_dic = scrape_product(tt)
    df1 = pd.DataFrame()
    df1 = df1.append(df_dic, ignore_index=True)
    df = pd.concat([df, df1], ignore_index=False)
    df.to_excel('TamkeenUpdate_all1.xlsx')