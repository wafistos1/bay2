import pandas as pd
import numpy as np
import re
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup
from .list_cat import urls_categories

import requests

PROXY_LIST = [
    '158.177.253.24:80',
    '3.213.139.74:8888',
    '64.124.38.140:8080',
    '64.124.38.125:8080',
    '64.124.38.141:8080',
    '64.124.38.142:8080',
    '45.152.188.39:3128',
    '45.152.188.48:3128',
    '45.152.188.16:3128',
    '207.244.227.169:443',
    '91.149.203.12:3128',
    '3.20.236.208:49205',
    '104.149.140.174:443',
    '149.28.91.128:1088'
    '168.91.234.183:80',
    '207.244.170.103:8118',
    '108.170.12.14:80',
    '64.124.38.141:8080',
    '158.177.253.24:80',
    '64.124.38.138:8080',

]


def scrape_all_categories(toto):
    list_urls_categories = []
    for i, pat in enumerate(toto):
        print('Count:', i)
        print('URL:', pat['url'])
        # proxy = '64.124.38.140:8080'
        for tt in PROXY_LIST:
            
            try:
                r = requests.get(pat['url'], proxies={'http': tt, 'https': tt}, timeout=10 )
                if r.status_code == 200:
                    print(r.status_code)
                    break
            except:
                pass
            
            

        soup  = BeautifulSoup(r.text, 'html.parser')
        
        urls = soup.find_all('div', {'class': 'mf-product-thumbnail'})
        len(urls)
        cat1 = pat['cat1']
        cat2 = pat['cat2']
        cat3 = pat['cat3']
        for url in urls:
            list_urls_categories.append({ 'url': url.find('a')['href'],
                                            'cat1': cat1,
                                            'cat2': cat2,
                                            'cat3': cat3,
                                     })
    return list_urls_categories
        

# papi = scrape_all_categories(urls_categories)
# df = pd.DataFrame(papi)
# df.to_excel('tamkeenstores.xlsx')

