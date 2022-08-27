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
import re
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup
import requests
import string
from requests_html import HTMLSession, HTML


session = HTMLSession()


urls_categories = [
    'https://redsea.com/ar/air-conditioning/ac-s/split-ac',
    'https://redsea.com/ar/air-conditioning/ac-s/window-ac',
    'https://redsea.com/ar/small-appliances/home-living/water-dispensers',
    
]

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0', 
    'Accept-Encoding': 'gzip, deflate', 
    'Accept': 'text/html', 
    'Connection': 'keep-alive', 
    'Accept-Language': 'en-US,en;q=0.5',  
    'Pragma': 'no-cache', 
    'Cache-Control': 'no-cache',
    'Referer': 'https://www.google.com/'
        }


r = requests.get(urls_categories[0], headers=headers)
html_text = ''
if r.status_code == 200:
        html_text = r.text
soup = BeautifulSoup(html_text, 'html.parser')
# r_html = HTML(html=html_text)
print(soup)




