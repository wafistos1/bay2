
import time
import os
import requests
import re, logging
import pandas as pd
from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.firefox.options import Options
from fake_useragent import UserAgent
from random import randint
import pandas as pd
# import numpy as np
from twocaptcha import TwoCaptcha


#pip install requests pandas openpyxl selenium=3.14 fake_useragent bs4
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
# sitekey = '6LdUViwUAAAAAOBJjtMsmKc9C7200Djd31w2mCs7'

solver = TwoCaptcha('24c7bf9600400be2acf271955dc27384')


def solve(url, sitekey):
    # try:
    result = solver.solve_captcha(
        site_key=sitekey,
        page_url=url,
        # version='v2',
        # score
        )     
    # except:
    #     logging.info('Failed to solve Capcha')
    #     exit()
    
    return result
        

heades = {
    'Accept': '*/*', 
    'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.3',
    'Set-Cookie': 'lang=en-US; Path=/; Expires=Wed, 23 Aug 2023 10:27:56 GMT; SameSite=Strict',
    'Accept-CH': 'Sec-CH-UA,Sec-CH-UA-Mobile,Sec-CH-UA-Platform,Sec-CH-UA-Arch,Sec-CH-UA-Full-Version-List,Sec-CH-UA-Model,Sec-CH-Device-Memory',
}



url = 'https://rendezvousparis.hermes.com/client/register'

def get_crsf_cookie(url):
    r = requests.get(url, headers=heades)
    soup = BeautifulSoup(r.text, 'lxml')
    csrf = soup.select_one('[name=_csrf]')
    sitekey = soup.select_one('[class=g-recaptcha]')
    csrf_token = csrf['value']
    sitekey_id = sitekey['data-sitekey']
    coockies = r.cookies
    
    return csrf_token, coockies, sitekey_id

def main():
    csrf, cookie, sitekey_id = get_crsf_cookie(url)
    result = solve(url, sitekey_id)
    print(result.split('|')[0])
    payload = {
    '_csrf': csrf,
    'prefer': 'Hermès Faubourg Saint-Honoré',
    'surname' :'wafi',
    'name' :'mameri',
    'phone_country' :'06694323221',
    'email' :'mameri.ouafi@gmail.com',
    'passport_id' :'1234567889',
    'g-recaptcha-response': result.split('|')[1],
    }
    
    r = requests.post(url, headers=heades, cookies=cookie, data=payload)
    print(r.text)
if __name__ == '__main__':
    main()