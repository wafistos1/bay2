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

options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')
#opti#     driver = webdriver.Firefox()ons.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)


def extract_ele(name, soup):
    elements = soup.find_all('td')
    for ele in elements:
        if name in ele.text:
            return ele.next_element.next_element.text.strip()
        
urls = pd.read_excel('/home/wafistos/Downloads/Noon-update1 (1) (1).xlsx')

list_products = urls['link_url'].to_list()
      
df = pd.read_excel('/home/wafistos/Documents/Projects/scaping_wafi/Noon/Noon_model_product.xlsx')
for i, url in enumerate(list_products[1351: ]):
    print('Count: ', i)
    print('URL: ', url)
    driver.get( url)
    r = driver.find_element_by_tag_name('body').get_attribute('innerHTML')
    soup = BeautifulSoup(r, "html.parser")
    time.sleep(0.5)
    
    try:
        sku = driver.find_element_by_class_name('modelNumber').text.replace('رقم الموديل', '').replace(':', '').strip()
        print('SKU: ', sku)
    except:
        continue
    name = soup.find('h1', {'class': 'sc-ebb3cc52-12 kVfnLm'}).text.strip()
    try:
        price = soup.find('div', {'class': 'priceWas'}).text.replace('ر.س', '').strip()
        special_price = soup.find('div', {'class': 'priceNow'}).text.replace('شاملاً ضريبة القيمة المضافة', '').replace('(', '').replace(')', '').replace('ر.س', '').replace('', '').strip()
    except:
        price = soup.find('div', {'class': 'priceNow'}).text.replace('شاملاً ضريبة القيمة المضافة', '').replace('ر.س', '').replace('(', '').replace(')', '').strip()
        special_price = ''
    try:
        description = soup.find('div', {'class': 'sc-b21e051a-4 cwboMX'}).text
    except:
        description = soup.find('div', {'class': 'sc-b21e051a-1 hUYYrw'}).text
        
    try:
        click_btn = driver.find_element_by_xpath('//div[contains(text(),"عرض الموصفات بالكامل")]')
        click_btn.click()
        r = driver.find_element_by_tag_name('body').get_attribute('innerHTML')
        soup = BeautifulSoup(r, "html.parser")
    except:
        pass
    raw_materials = extract_ele('المادة', soup)
    free_colors = extract_ele('اسم اللون', soup)
    products_size = extract_ele('الحجم', soup)
    manufacturer = extract_ele('بلد المنشأ', soup)
    number_pieces = extract_ele('عدد القطع', soup)
    ts_dimensions_width = extract_ele('عرض/عمق المنتج', soup)
    ts_dimensions_length = extract_ele('طول المنتج', soup)
    ts_dimensions_height = extract_ele('ارتفاع المنتج', soup)
    set_include = extract_ele('الطقم يتضمن', soup)
    weight = extract_ele('وزن المنتج', soup)
    images = soup.find('div', {'class': 'sc-5b0fbc26-2 cAxeFA'}).find_all('img')
    len(images)
    cats = soup.find('div', {'class': 'sc-f019e14d-2 ekDKTS'}).find_all('a')
    len(cats)
    cat1 = cats[0].text
    cat2 = cats[1].text
    try:
        cat3 = cats[-1].text
    except:
        cat3 = ''
    
    list_images = [img['src'] for img in images]
    base_images = list_images[0]
    additionnel_images = ','.join(list_images[1:])

    data = {
        
        'sku': sku,
        'name': name,
        'link_url': url,
        'price': price,
        'special_price': special_price,
        'description': description,
        'free_colors': free_colors,
        'ts_dimensions_width':ts_dimensions_width,
        'ts_dimensions_length':ts_dimensions_length,
        'ts_dimensions_height':ts_dimensions_height,
        'weight': weight,
        'products_size': products_size,
        'set_include': set_include,
        'number_pieces': number_pieces, 
        'categories1': cat1,
        'categories2': cat2,
        'categories3': cat3,
        'raw_materials': raw_materials,
        'manufacturer': manufacturer,
        'base_images': base_images,
        'additionnel_images': additionnel_images,
    }
    df1 = pd.DataFrame([data])
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('Noon-wafi-products3.xlsx')

