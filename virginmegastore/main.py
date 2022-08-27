
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import requests, re, cssutils, time
import pandas as pd

def scrap_products(url1):
    time.sleep(0.3)
    url = url1['url']
    cat1 = url1['cat1']
    cat2 = url1['cat2']
    cat3 = url1['cat3']
    print('URL: ', url)
    
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    name = soup.find('h1', {'class': 'name'}).text.strip()
    try:
        price = soup.find('span', {'class': 'price__number price__number--strike-through'}).text.strip()
        special_price = soup.find('span', {'class': 'price__number'}).text.strip()
    except:
        price = soup.find('span', {'class': 'price__number'}).text.strip()
        special_price = ''
        
    try:
        mgs_brans = soup.find('p', {'class': 'brand'}).find('a').text.strip()
    except:
        mgs_brans = ''
    try:
        description = soup.find('div', {'id': 'details'}).text.strip()
    except:
        description = ''
    images = soup.find_all('div', {'class': 'pdp_image-carousel-image js-zoomImage c-pointer'})
    list_images = []
    for img in images:
        style = cssutils.parseStyle(img['style'])
        imgs = style['background']
        imgs = imgs.replace('url(', '').replace(')', '')
        list_images.append('https://www.virginmegastore.sa' + imgs)
    base_image = list_images[0]
    additionnel_images = ','.join(list_images[1:])
    sku = url.split('/')[-1]
    try:
        video = soup.find('iframe', {'allow': 'autoplay'})['src']
    except:
        video = ''
    data = {
        'sku': sku,
        'url_link': url,
        'name': name,
        'price': price,
        'special_price': special_price,
        'base_image':base_image,
        'additionnel_images':additionnel_images,
        'mgs_brands': mgs_brans,
        'description': description,
        'list_images': list_images,
        'video': video,
        'categories1': cat1, 
        'categories2': cat2, 
        'categories3': cat3, 
        
    }
    
    return data


urls = pd.read_excel('/home/wafistos/Documents/Projects/scaping_wafi/virginmegastore/Virgin_urls1.xlsx')
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

df = pd.read_excel('/home/wafistos/Documents/Projects/scaping_wafi/virginmegastore/Virgin_model_products.xlsx')

for i, url in enumerate(list_urls):
    print('Count: ', i)
    data = scrap_products(url)
    df1 = pd.DataFrame([data])
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('Vergin_product_update.xlsx')