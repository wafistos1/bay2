
from unicodedata import name
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



def find_text(list_name, details):
    for name in list_name:
        if name['text1'] in details:
            return name['text2']
    return ''
        

regex_list = [
    
   {'find': 'p', 'regex': "^المقاس:"} ,
   {'find': 'b', 'regex': "المقاس الاول:"} ,
   {'find': 'p', 'regex': "المقاس الاول"} ,
   {'find': 'b', 'regex': "مقاس الاستاند:"} ,
   {'find': 'p', 'regex': "المقاس الاول:"} ,
   {'find': 'p', 'regex': "القطر :"} ,
   {'find': 'p', 'regex': "الطول"} ,
   {'find': 'strong', 'regex': "Size :"} ,
   {'find': 'strong', 'regex': "بحجم"} ,
]

list_country = [
    {'text1': 'صنع في الصين', 'text2': 'الصين'},
    {'text1': 'صنع بالصين', 'text2': 'الصين'},
    {'text1': '(made in India)', 'text2': 'الهند'},
    {'text1': 'صناعة هندية', 'text2': 'الهند'},
    {'text1': 'صنع في فيتنام', 'text2': 'فيتنام'},
    {'text1': 'MAde In China', 'text2': 'الصين'},
    {'text1': 'Made In China', 'text2': 'الصين'},
    
]

list_color = [
    {'text1': 'ذهبي', 'text2': 'ذهبي'},
    {'text1': 'Golden color', 'text2': 'ذهبي'},
    {'text1': 'Silver color', 'text2': 'فضي'},
    {'text1': 'فضي', 'text2': 'فضي'},
]

list_raw_materials = [
    {'text1': 'مصنوع من الزجاج والمعدن', 'text2': 'زجاجي ومعدني'},
    {'text1': 'مصنوع من المعدن', 'text2': 'معدني'},
    {'text1': 'Made Of Metal', 'text2': 'معدني'},
    {'text1': 'معدني', 'text2': 'معدني'},
    {'text1': 'made from metal', 'text2': 'معدني'},
    {'text1': 'جلد بوتيغا', 'text2': 'جلد بوتيغا'},
    {'text1': 'زجاجي', 'text2': 'زجاجي'},
]

def scrape_urls(soup, url1, color=None, pricipal_img=None):
    
    print('URL: ', url1['url'])
    url = url1['url']
    categories1 = url1['categories1']
    categories = url1['categories']
    # headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    # cookies = {'session': '134-8225175-0355220'}
    # r = requests.get(url, headers=headers, cookies=cookies)
    # soup = BeautifulSoup(r.content, "html.parser")
    time.sleep(0.5)

    sku  = soup.find('div', {'class': 'product-single__vendor-sku'}).find('span').find('span').text.strip()

    product_size = ''
    list_colors = ''
    for gex in regex_list:
        regex = re.compile(gex['regex'])
        find = gex['find']
        try:
            product_size = soup.find(find, text=regex).text.strip()
            break
        except:
            pass
        try:
            colors = soup.find('fieldset', {'name': 'Color'}).find_all('input')
            list_colors = [color['value'] for color in colors]
        except:
            pass
    name = soup.find('h1', {'class': 'h2 product-single__title'}).text.strip()
    price = soup.find('span', {'class': 'firstPriceValue'}).text.replace('SR', '').strip()
    print('Price:', price)
    images = soup.find_all('img', {'class': 'photoswipe__image lazyautosizes lazyloaded'})

    print('len images', len(images))
    list_img = []
    for i, img in enumerate(images):

        list_img.append('https:' + img['data-photoswipe-src'].split('?')[0])
        # list_img.append('https:' + (img.find('img')['data-srcset'].replace('{width}', '720').split('?')[0]))
    if list_img == []:
        text = driver.find_element_by_tag_name('body').get_attribute('innerHTML')
        soup = BeautifulSoup(text, 'html.parser')
        tootch = soup.find('div', {'class': 'product__thumbs--scroller'}).find_all('div', {'class': 'product__thumb-item'})
        print('len',len(tootch))
        for t in tootch:
            list_img.append('https:' + t.find('a')['href'])

    

    list_img = list(dict.fromkeys(list_img))
    try:
        base_image = list_img[0]
    except:
        base_image = ''
    additionnel_images = ','.join(list_img[1:])
    descriptions = soup.find_all('div', {'class': 'product-block'})
    
    description = descriptions[3].text.strip()
    manufacturer = find_text(list_country, description)
    if color:
        free_colors = color
    else:
        free_colors = find_text(list_color, description)
    raw_materials = find_text(list_raw_materials, description)
    data = {
        'sku': sku,
        'name': name,
        'price': price,
        'product_size': product_size,
        'categories1': categories1,
        'categories': categories,
        'free_colors': free_colors,
        'raw_materials': raw_materials,
        'manufacturer': manufacturer, 
        'list_colors': list_colors,
        'link_url': url,
        
        'description': description,
        'pricipal_img': pricipal_img,
        'base_image': base_image,
        'additionnel_images': additionnel_images,
    }
    return data

options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')
#opti#     driver = webdriver.Firefox()ons.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)

toto = pd.read_excel('/home/wafistos/Documents/Projects/scaping_wafi/cascadesco/cascadosco.updating.url_products.xlsx')
urls = []
for index , row in toto.iterrows():
    urls.append({'url': row['url'], 'categories1': row['categories1'], 'categories': row['categories']})
    

df = pd.read_excel('/home/wafistos/Documents/Projects/scaping_wafi/cascadesco/cascadesco_product_model.xlsx')

name_excel = 'Cascadesco.updating.test3.xlsx'

for i, url1 in enumerate(urls):
    print('Count: ', i)
    driver.get(url1['url'])
    colors = driver.find_elements_by_xpath('//div[@class="variant-input"]')
    len(colors)
    if len(colors) >=1:
        
        for color in colors:
            c = color.get_attribute('data-value')
            print('colors: ', c)
            color.click()
            time.sleep(0.5)
            text = driver.find_element_by_tag_name('body').get_attribute('innerHTML')
            soup = BeautifulSoup(text, 'html.parser')
            try:
                pricipal_img = soup.find('div', {'class': 'product-main-slide secondary-slide is-selected'}).find('img')['data-photoswipe-src']
            except:
                pricipal_img = soup.find('div', {'class': 'product-main-slide secondary-slide'}).find('img')['data-photoswipe-src']
            pricipal_img = 'https:' +  pricipal_img.split('?')[0]

            data = scrape_urls(soup, url1, color=c, pricipal_img=pricipal_img)
            df1 = pd.DataFrame([data])
            df = pd.concat([df, df1], ignore_index=True)
            df.to_excel(name_excel)
            time.sleep(1)
    else:
        text = driver.find_element_by_tag_name('body').get_attribute('innerHTML')
        soup = BeautifulSoup(text, 'html.parser')
        try:
            data = scrape_urls(soup, url1)
        except:
            continue
        df1 = pd.DataFrame([data])
        df = pd.concat([df, df1], ignore_index=True)
        df.to_excel(name_excel)