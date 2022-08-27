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
import time, logging, re
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

options = Options()
ua = UserAgent()
userAgent = ua.random
logging.info(userAgent)
options.add_argument(f'user-agent={userAgent}')
#opti#     driver = webdriver.Firefox()ons.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)


def extract_product_size():
    r = driver.find_element_by_tag_name('body').get_attribute('innerHTML')
    soup = BeautifulSoup(r, "html.parser")
    regex_product_size = [
        
    {'find': ["p", "span"], 'regex': "^الأبعاد:"} ,
    {'find': ["p", "span"], 'regex': "الأبعاد :"} ,
    {'find': ["p", "span"], 'regex': "الابعاد :"} ,
    {'find': ["p", "span"], 'regex': "الابعاد"} ,
    ]
    for i, regex in enumerate(regex_product_size):
        regex1 = re.compile(regex['regex'])
        find = regex['find']
        try:
            product_size = soup.find(find, text=regex1).text.strip()
            
            return product_size
        except:
            continue


def extract_ele(list_name):
    r = driver.find_element_by_tag_name('body').get_attribute('innerHTML')
    soup = BeautifulSoup(r, "html.parser")
    for name in list_name:
        
        elements = soup.find('div', {'class': 'richText-root-2t-'})
        for ele in elements:
            try:
                if name in ele.text:
                    if len(ele.text.strip()) >= 20:
                        return None
                    return ele.text.replace(name, '').replace('•', '').strip()
            except:
                pass


def retrun_totoch(name):
    r = driver.find_element_by_tag_name('body').get_attribute('innerHTML')
    soup = BeautifulSoup(r, "html.parser")
    try:
        
        return soup.find('strong', text=name).next_sibling
    except:
        pass  
    
    
def extract_data(driver, url1):
    url = url1['url']
    cat1 = url1['categories1']
    cat2 = url1['categories2']
    cat3 = url1['categories3']
    driver.get(url)
    time.sleep(5)
    body=WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.TAG_NAME,'body')))
    r = body.get_attribute('innerHTML')
    soup = BeautifulSoup(r, "html.parser")
    sku = soup.find('strong', text=re.compile(r'رقم المنتج')).next_sibling   
    name = soup.find('h1', {'class': 'productFullDetail-productName-BbW'}).text.strip()
    price = soup.find_all('p', {'class': 'productFullDetail-productPrice-1Js'})[1].text.strip()
    special_price = soup.find_all('p', {'class': 'productFullDetail-productPrice-1Js'} )[0].text.strip()
    description = soup.find('div', {'id': 'collapseOne'}).text.strip()
    images = soup.find('div', {'class': 'image-gallery-content bottom'}).find_all('img')
    list_images = [img['src'] for img in images if 'width=700' not in img['src'] ]
    guarantee = soup.find('strong', {'class': 'productFullDetail-three_col_text_img-28a'}, text='ضمان').next_element.next_element.text.strip()
    base_image = list_images[0]
    aditionnel_images = ','.join(list_images[1:])
    logging.info('extract data')
    manufacturer =  extract_ele(['صنع في'])
    
    ts_dimensions_width = extract_ele(['العرض بالسم', 'Width'])
    ts_dimensions_length = extract_ele(['•الارتفاع بالسم', ''])

    ts_dimensions_height = extract_ele(['•العمق بالسم', '•العمق'])
    raw_materials =  extract_ele(['الخامة'],)
    free_colors =  extract_ele(['اللون'])
    guarantee = extract_ele(['الضمان'])
    
    if ts_dimensions_height == None:
        ts_dimensions_height = retrun_totoch('Height : ')

    if ts_dimensions_width == None:
        ts_dimensions_width = retrun_totoch('Width : ')

    if ts_dimensions_length == None:
        ts_dimensions_length = retrun_totoch('Depth : ')
    product_size = extract_product_size()
    data = {
        'sku': sku,
        'Link_url': url,
        'name': name,
        'price': price,
        'special_price': special_price,
        'description': description,
        'manufacturer': manufacturer,
        'depth': '',
        'ts_dimensions_width': ts_dimensions_width,
        'ts_dimensions_length': ts_dimensions_length,
        'ts_dimensions_height': ts_dimensions_height,
        'product_size': product_size,
        'raw_materials': raw_materials,
        'categories1': cat1,
        'categories2': cat2,
        'categories3': cat3,
        'free_colors':free_colors,
        'guarantee': guarantee,
        'base_image': base_image,
        'aditionnel_images': aditionnel_images
    }
    return data

urls = pd.read_excel('/home/wafistos/Documents/Projects/scaping_wafi/almutlaqfurniture/Almut_update_url1.xlsx')
list_urls = []
for index, row in urls.iterrows():
    list_urls.append({
        'url': row['url'], 
        'categories1': row['categories1' ], 
        'categories2': row['categories2' ],  
        'categories3': row['categories3' ],  
        })

df = pd.read_excel('/home/wafistos/Documents/Projects/scaping_wafi/almutlaqfurniture/Almutlaq_product_model.xlsx')

for i, url in enumerate(list_urls):
    logging.info(f'Count: {i}')
    logging.info(f"URL: {url['url']}")
    try:
        data = extract_data(driver, url)
    except:
        logging.warning(f' Error in {url["url"]}')
        continue
    df1 = pd.DataFrame([data])
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('almutlaqfurniture-Update1.xlsx')
