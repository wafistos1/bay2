import time
import os
import requests
import re, logging
import pandas as pd
from dataclasses import dataclass
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
from fake_useragent import UserAgent
from random import randint
import pandas as pd
import numpy as np
from twocaptcha import TwoCaptcha
from selenium.webdriver.chrome.options import Options


mobile_emulation = {
    "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },
    "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" }
chrome_options = Options()
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
driver = webdriver.Chrome(chrome_options = chrome_options, executable_path='./chromedriver')#, desired_capabilities=capabilities)

driver.get('https://rendezvousparis.hermes.com/client/register')


surname = driver.find_element_by_name('surname').send_keys('wafi')
name = driver.find_element_by_name('name').send_keys('mameri')
phone_country =  driver.find_element_by_xpath('//input[@id="phone_number"]').send_keys('6452147854')
# phone_country =  driver.find_element_by_class_name('phone_country').send_keys('06452147854')
email =  driver.find_element_by_xpath('//input[@type="email"]').send_keys('mameri.ouafi@gmail.com')
passport_id =  driver.find_element_by_xpath('//input[@id="passport_id"]').send_keys('12541254785412')
accept = driver.find_element_by_xpath('//input[@id="cgu"]').click()
conent = driver.find_element_by_xpath('//input[@id="processing"]').click()
#favorite store
prefer = driver.find_element(By.XPATH, '//select[@id="prefer"]').click()
option = driver.find_element(By.XPATH, '//option[@value="faubourg"]').click()
# Id phoe
phone_country = driver.find_element(By.XPATH, '//select[@id="phone_country"]').click()
option_phone = driver.find_element(By.XPATH, '//option[@value="FR"]').click()



sitekey = driver.find_element(By.XPATH, '//div[@class="g-recaptcha"]').get_attribute('data-sitekey')
csrf = driver.find_element(By.XPATH, '//input[@name="_csrf"]').get_attribute('value')





#pip install requests pandas openpyxl selenium=3.14 fake_useragent bs4
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
# sitekey = '6LdUViwUAAAAAOBJjtMsmKc9C7200Djd31w2mCs7'

solver = TwoCaptcha('24c7bf9600400be2acf271955dc27384')
url = 'https://rendezvousparis.hermes.com/client/register'

def solve(url, sitekey):
    # try:
    result = solver.solve_captcha(
        site_key=sitekey,
        page_url=url,
        # version='v2',
        # score
        )     

    return result



result = solve(url, sitekey)
print(result.split('|')[1])
# ADD response
time.sleep(1)
driver.execute_script('var element=document.getElementById("g-recaptcha-response"); element.style.display="";')
driver.execute_script("""document.getElementById("g-recaptcha-response").innerHTML = arguments[0] """, result.split('|')[1] )

driver.execute_script('var element=document.getElementById("g-recaptcha-response"); element.style.display="none";')
driver.find_element(By.XPATH, '//button[@type="submit"]').click()