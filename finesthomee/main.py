
from email.mime import base
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
import time
import re
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

def extraire_ele(name, soup):
    try:
        toto = soup.find('li', text=re.compile(f'^{name}')).text.replace(name, '').strip()
    except:
        toto = ''
    if toto == '':
        try:
            toto = soup.find('p', text=re.compile(f'^{name}')).text.replace(name, '').strip()
            
        except:
            try:
                toto = soup.find('li', text=re.compile(f'{name}')).text.replace(name, '').strip()
            except:
                toto = ''
    return toto


def extract_colors(detail):
    details = detail.split(' ')
    for i, color in enumerate(details):
        if 'لون' in color:
            return (details[i+1])
options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')
#opti#     driver = webdriver.Firefox()ons.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)
df = pd.read_excel('Fines_model.xlsx')
list_urls = []
urls = pd.read_excel('Fines_list_urls.xlsx')
for index, row in urls.iterrows():
    list_urls.append({'url': row['url'],  'categories': row['categories'], 'categories1': row['categories1']})

count_sku = 2000
for i, url in enumerate(list_urls):
    print('Count: ', i)
    print('URL: ', url['url'])
    driver.get(url['url'])
    name = driver.find_element_by_class_name('product-title').text.strip()
    try:
        free_colors =  extract_colors(name)
    except:
        free_colors = ''
    price = driver.find_element_by_id('product-old-price').text.replace('ر.س', '').strip()
    special_price = driver.find_element_by_id('product-price').text.replace('ر.س', '').strip()
    qty = len(driver.find_elements_by_tag_name('option'))
    weight = driver.find_element_by_class_name('product-meta').get_attribute('innerHTMl')
    description = driver.find_element_by_id('description-tab').text
    details = driver.find_element_by_id('description-tab').get_attribute('innerHTML')
    soup = BeautifulSoup(details, 'html.parser')
    height = extraire_ele('الارتفاع', soup)
    diameter = extraire_ele('القطر', soup)
    if diameter == '':
        diameter = extraire_ele('قطر', soup)
    lenght = extraire_ele('الطول', soup)
    
    amper = extraire_ele('سعة البطارية', soup)
    power = extraire_ele('الطاقة المقدرة', soup)
    rechargeable = extraire_ele('مدة الشحن', soup)
    no_of_lamps = extraire_ele('عدد لمبات المصباح', soup)
    try:
        with_controller = soup.find('span', text=re.compile('ريموت لتحكم ')).text.strip()
        with_controller  ='Yes'
    except:
        with_controller = 'No'
    
    images_thmbs = driver.find_element_by_class_name('image-thumbs').find_elements_by_tag_name('img')
    print(len(images_thmbs))
    list_images = []
    try:
        for img in images_thmbs:
            img.click()
            list_images.append(driver.find_element_by_id('main-img').get_attribute('src'))
            time.sleep(0.3)
    except:
           list_images.append(driver.find_element_by_id('main-img').get_attribute('src'))
    base_image = list_images[0]
    additionnel_images = ','.join(list_images[1:])
    sku1 = driver.find_element_by_xpath('//div[@class="product-sku"]/span')
    sku = sku1.get_attribute('innerHTML')
    print('sku: ', sku)
    
    data = {
        'sku': sku,
        'name': name,
        'price': price,
        'special_price': special_price,
        'qty': qty,
        'free_colors': free_colors,
        'weight': weight,
        'ts_dimensions_height': height,
        'ts_dimensions_length': lenght,
        'categories1': url['categories1'],
        'categories': url['categories'],
        'amper': amper, 
        'power': power, 
        'rechargeable': rechargeable, 
        'no_of_lamps': no_of_lamps, 
        'with_controller': with_controller, 
        
        'diameter': diameter,
        'description': description,
        'link_url': url['url'],
        'base_image': base_image,
        'additionnel_images': additionnel_images,
        
    }
    df1 = pd.DataFrame([data])
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('Fineshomee_update.xlsx')