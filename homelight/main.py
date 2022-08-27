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
import re, logging
# import pandas as pd
# import numpy as np
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

options = Options()
ua = UserAgent()
userAgent = ua.random
logging.info(userAgent)
options.add_argument(f'user-agent={userAgent}')
#opti#     driver = webdriver.Firefox()ons.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)

def return_ele(name, soup):
    try:
        return soup.find('li', text=re.compile(name)).text.replace(name, '').strip()
    except:
        return ''



urls = pd.read_excel('homelight_url_update.xlsx')
list_urls = []
for index, row in urls.iterrows():
    list_urls.append(
        {
            'url': row['url'],
            'cat1': row['cat1'],
            'cat2': row['cat2'],
            'cat3': row['cat3'],
        }
    )


def scrape_data(url1):
    url = url1['url']
    cat1 = url1['cat1']
    cat2 = url1['cat2']
    cat3 = url1['cat3']
    logging.info('URL %s', url)
    driver.get(url)
    body=WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.TAG_NAME,'body')))
    time.sleep(3)
    r = body.get_attribute('innerHTML')
    soup = BeautifulSoup(r, "html.parser")
    name = soup.find('h1', {'class': 'title'}).text.strip()
    sku = soup.find('div', {'class': 'list--table-view__cell value text-unicode'}).text.strip()
    price = soup.find('div', {'class': 'price-wrapper-info'}).text.replace('ر.س', '').strip()
    description = soup.find('article', {'class':'article'}).text
    images = soup.find_all('a', {'data-fancybox':'product-details'})
    list_images = [img.find('img')['data-splide-lazy'] for img in images]
    base_image = list_images[0]
    add_images = ','.join(list_images[1: ])
    raws_materials = return_ele('خامة المنتج :', soup)
    power_lights = return_ele('اضاءة ليد بقدرة :', soup)
    lights_color = return_ele('لون الاضاءة :', soup)
    technics_description = return_ele('معيار مقاومة الماء و الغبار :', soup)
    elec_power = return_ele('الجهد الكهربائي :', soup)
    guarante = return_ele('ضمان', soup)
    power = return_ele('القدرة :', soup)
    lights_color1 = return_ele('اضاءة ليد', soup)
    free_colors = return_ele('لون المنتج :', soup)
    lumen = return_ele('اللومن :', soup)
    tmp = return_ele('درجة حرارة اللون', soup)

    data = {
        'sku': sku,
        'Link_url': url,
        'name': name,
        'price': price,
        'description': description,
        'raws_materials': raws_materials,
        'power_lights': power_lights,
        'lights_color': lights_color,
        'technics_description': technics_description,
        'elec_power': elec_power,
        'power': power,
        'lights_color1': lights_color1,
        'free_colors': free_colors,
        'lumen': lumen,
        'tmp': tmp,
        'guarante': guarante,
        'base_image': base_image,
        'add_images': add_images,
        'cat1': cat1,
        'cat2': cat2,
        'cat3': cat3,
    }
    return data

df = pd.read_excel('homelight_product_model.xlsx')

for i, url in enumerate(list_urls):
    logging.info('--Count: %s', i)
    data = scrape_data(url)
    df1 = pd.DataFrame([data])
    df = pd.concat([df, df1], ignore_index=True)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df.to_excel('homelight_product_update1.xlsx')
