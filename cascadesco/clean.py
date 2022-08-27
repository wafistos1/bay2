from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options

import pandas as pd
import numpy as np
import re
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup

df = pd.read_excel('/home/wafistos/Documents/Projects/scaping_wafi/cascadesco/Cascadesco.updating.test3.xlsx')
toto = pd.read_excel('/home/wafistos/Documents/Projects/scaping_wafi/cascadesco/categories/categories كاسكيدز.xlsx')


list_cats = []
for index, row in toto.iterrows():
    list_cats.append({'id': row['ID'], 'description': row['description'], 'categories1': row['categories']})
    
for cat in list_cats:
    df.loc[df['categories1']== cat['categories1'], 'description'] = cat['description']
    df.loc[df['categories1']== cat['categories1'], 'categories'] = cat['id']
    

two_month = datetime.now() + timedelta(days=60)
two_month = two_month.strftime("%m/%d/%Y")
today = datetime.today().strftime("%m/%d/%Y")



df['news_from_date'] = today
df['news_to_date'] = two_month
df['product_websites'] = 'base'
df['attribute_set_code'] = 'Default'
df['product_type'] = 'simple'
df['store_view_code'] = ''
df.drop_duplicates(subset=['sku'], inplace=True)
df['supplier'] = 'CAS'
df['sku'] = 'CAS--' + df['sku']
df['sku number only'] = df['sku'].str.replace('CAS--', '')
#df['manufacturer'] = 'مستوردة'
df['product_websites'] = 'base'
df['is_in_stock']=1
df['allow_backorders'] = df['is_in_stock']
df['visibility'] = 'Catalog, Search'
df['tax_class_name'] = 'Taxable Goods'

df['qty'] = 0
df['out_of_stock_qty'] = -5


df['product_online'] = df['is_in_stock']



df['price'] = pd.to_numeric(df['price'])
df['special_price'] = ''
df['cost'] = df['price'] * 0.8
#df['price'] = df['price'] * 1.3



def toto_clean(name):
    df[name] = df[name].str.replace(',', '-')
    df[name] = df[name].str.replace('/', '-')
    df[name] = df[name].str.replace('"', '-')
    df[name] = df[name].str.replace('%', '-')
    df[name] = df[name].str.replace('&', '-')
    df[name] = df[name].str.replace('?', '-', regex=False)
    df[name] = df[name].str.replace('(', '-', regex=False)
    df[name] = df[name].str.replace(')', '-', regex=False)
    df[name] = df[name].str.replace('{', '-', regex=False)
    df[name] = df[name].str.replace('}', '-', regex=False)
    df[name] = df[name].str.replace("'", '-', regex=False)
    df[name] = df[name].str.replace('*', 'X', regex=False)
    df[name] = df[name].str.replace('!', '-')
    df[name] = df[name].str.replace('=', '-')
    df[name] = df[name].str.replace('+', '-', regex=False)
    df[name] = df[name].str.replace('،', '-', regex=False)
    
def ampty_value(name):
    df.loc[df[name].isnull(), name] = '__EMPTY__VALUE__'
    
    
def price_num(name):
    try:
        df[name] = df[name].str.replace('-', '')
        df[name] = df[name].str.replace(',', '')
    except:
        pass
    df.loc[df[name] == '__EMPTY__VALUE__', name] = 0
    
    df[name] = pd.to_numeric(df[name])
    df.loc[df[name] == 0, name] = '__EMPTY__VALUE__'
toto_clean('name')
toto_clean('description')
toto_clean('free_colors')



df['small_image'] =  df['base_image']
df['swatch_image'] =  df['base_image']
df['thumbnail_image'] =  df['base_image']


df['estimated_delivery_enable'] = 'Static Text'
df['estimated_delivery_text'] = ''
df['url_key'] = df['sku'] + '-' + df['name'] 
df['categories3'] = ''
df['categories2'] = ''

df = df[['sku number only', 'sku', 'store_view_code', 'attribute_set_code', 'product_type',  'product_websites',
         'name',  'estimated_delivery_enable', 'estimated_delivery_text',  'url_key',  'description'
, 'link_url', 'categories1', 'categories2', 'categories3', 'categories',
         
            'free_colors',
    'product_size',
    'raw_materials',
         
    'cost', 'price',  'special_price',  'visibility', 'tax_class_name', 'manufacturer',
         'news_from_date', 'news_to_date','pricipal_img', 'base_image', 'small_image', 'swatch_image' 
    , 'thumbnail_image', 'additionnel_images', 'product_online', 'qty', 'out_of_stock_qty', 'allow_backorders'
    , 'is_in_stock',  'supplier'
        ]]

list_columns = [
    'special_price',
    'free_colors',
    'product_size',
    'raw_materials',
    'manufacturer',
    'pricipal_img',    
]
for column in list_columns:
    df.loc[(df[column] == '') | (df[column].isnull()), column] = '__EMPTY__VALUE__'

df.to_excel(f'Cascadesco-update.xlsx')