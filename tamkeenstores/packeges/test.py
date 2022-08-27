import pandas as pd
import numpy as np
import re

from bs4 import BeautifulSoup
from scrape_cat import PROXY_LIST
import requests
import time



urls = [
    'https://tamkeenstores.com.sa/product/gib_mff3026rs/',
    'https://tamkeenstores.com.sa/product/gshf224/',
    'https://tamkeenstores.com.sa/product/dfb512fw/',
]

for i, url in enumerate(urls):
    print('Count:', i)
    print('URL:', url)
    for tt in PROXY_LIST:
        description = ''
        manufacturer = ''   
        try:
            r = requests.get(url, proxies={'http': tt, 'https': tt}, timeout=10 )
            if r.status_code == 200:
                print(r.status_code)
                break
        except:
            pass
    soup  = BeautifulSoup(r.text, 'html.parser')

    try:
        short_description = soup.find('div', {'id': 'tab-description'}).text
    except:
        short_description = description
    print('len dimension',short_description )
   
