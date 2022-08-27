import pandas as pd
import numpy as np
import re
from requests_html import HTMLSession
from bs4 import BeautifulSoup

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
import random
# PROXY_LIST = [
#     # '78.154.167.68:8080'
#     # '18.220.20.81:8080'
#     # '64.124.38.142:8080'
#     # '158.177.253.24:80',
#     # '3.213.139.74:8888',
#     '64.124.38.140:8080',
#     '64.124.38.125:8080',
#     '64.124.38.141:8080',
#     '64.124.38.142:8080',
#     '45.152.188.39:3128',
#     '45.152.188.48:3128',
#     '45.152.188.16:3128',
#     '207.244.227.169:443',
#     '91.149.203.12:3128',
#     '3.20.236.208:49205',
#     '104.149.140.174:443',
#     '149.28.91.128:1088'
#     '168.91.234.183:80',
#     '207.244.170.103:8118',
#     '108.170.12.14:80',
#     '64.124.38.141:8080',
#     '158.177.253.24:80',
#     '64.124.38.138:8080',

# ]

# create selenium driver
# options = Options()
# ua = UserAgent()
# userAgent = ua.random
# print(userAgent)
# options.add_argument(f'user-agent={userAgent}')
# options.add_argument("--headless")
# driver = webdriver.Firefox(firefox_options=options)

# user_agent = 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/80.0.3987.132 Safari/537.36'
# accept ="text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
# accept_en = "gzip, deflate, br"
# accept_lan = "en-US,en;q=0.9"
# cache_con = "max-age=0"
# cokies = ""
# down_link = "0.35"
# headers = {'accept': accept,
#            'accept-encoding': accept_en,
#            'accept-language': accept_lan,
#            'cache-control': cache_con,
#            'cache': cokies,
#            'user-agent': user_agent,}
# HEADERS = ({'User-Agent':
#             'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
#             AppleWebKit/537.36 (KHTML, like Gecko) \
#             Chrome/90.0.4430.212 Safari/537.36',
#             'Accept-Language': 'en-US, en;q=0.5'})

user_agent_list = [
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]


# HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64)AppleWebKit/537.36 (KHTML, like Gecko)Chrome/44.0.2403.157 Safari/537.36',
#             'Accept-Language': 'en-US, en;q=0.5'})
# print(user_agent)

product_link = []
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "DNT": "1",
    "Connection": "close",
    "Upgrade-Insecure-Requests": "1",
}


# cookies = {'session': '134-8225175-0355220'}   
# driver.get('https://www.amazon.com//Sagebrook-Home-12495-02-Metal-Accent/dp/B079DRDS3J?ref_=ast_sto_dp')
# time.sleep(0.5)
# r = requests.get('https://www.amazon.com//Sagebrook-Home-12495-02-Metal-Accent/dp/B079DRDS3J?ref_=ast_sto_dp', headers=headers, cookies=cookies)
cookies = {'session': '134-8225175-0355220'}
r = requests.get("https://www.amazon.com/Life-Concept-desighed-Couch-Tables/dp/B0828NK51M/ref=pd_pb_ss_no_hpb_3/147-1776137-4121237",
        headers=headers,
        cookies=cookies
    )
soup = BeautifulSoup(r.content, "lxml")

details = soup.find('div', {'id': 'productDetails_feature_div'})
# details = driver.find_element_by_id('productDetails_detailBullets_sections1').text
# print(details)
sku = details.find(text=re.compile('Item model number')).parent.parent.find('td').text.strip()
print('sku', sku)