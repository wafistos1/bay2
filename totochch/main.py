
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

cookies1 = {
    "domain": ".facebook.com",
    "hostOnly": False,
    "httpOnly": False,
    "name": "act",
    "path": "/",
    "sameSite": "strict",
    "secure": True,
    "session": True,
    "storeId": "0",
    "value": "0000....000", #the value here is changed
    "id": 1
}

chrome_options = webdriver.ChromeOptions()
experimentalFlags = ['same-site-by-default-cookies@1','cookies-without-same-site-must-be-secure@1']
chromeLocalStatePrefs = { 'browser.enabled_labs_experiments' : experimentalFlags}
chrome_options.add_experimental_option('localState',chromeLocalStatePrefs)
driver = webdriver.Chrome(options=chrome_options, executable_path='/home/wafistos/Documents/Projects/scaping_wafi/totochch/chromedriver')
driver.add_cookie = cookies1
driver.get("https://visa-fr.tlscontact.com/dz/orn/register.php")

