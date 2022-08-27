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

df = pd.read_csv('Aynbma_product1.csv')
#df1 = pd.read_excel('')
# toto = pd.read_excel('/home/wafistos/Documents/Projects/scaping_wafi/promise/categories/Promise_cats.xlsx')

df['categories'] = ''
# list_cats = []
# for index, row in toto.iterrows():
#     list_cats.append({'id': row['id'],  'categories1': row['categories1'], 'categories2': row['categories2'], 'categories3': row['categories3'], })
    
# for cat in list_cats:
#     df.loc[(df['categories2']== cat['categories2']) & (df['categories3']== cat['categories3']), 'categories'] = cat['id']
    
    

two_month = datetime.now() + timedelta(days=60)
two_month = two_month.strftime("%m/%d/%Y")
today = datetime.today().strftime("%m/%d/%Y")



df['news_from_date'] = today
df['news_to_date'] = two_month
df['product_websites'] = 'base'
df['attribute_set_code'] = 'Default'
df['product_type'] = 'simple'
df['store_view_code'] = ''
#df.drop_duplicates(subset=['sku'], inplace=True)
df['supplier'] = ''
# df['sku'] = '-' + df['sku']
df['sku number only'] = df['sku'].str.replace('-', '')
# df['sku number only'] = ''
df['sku'] = '-' + df['sku']
df['manufacturer'] = 'مستوردة'
df['product_websites'] = 'base'
df.loc[df['is_in_stock']=='نفدت الكمية', 'is_in_stock'] = 0
df['allow_backorders'] = df['is_in_stock']
df['visibility'] = 'Catalog, Search'
df['tax_class_name'] = 'Taxable Goods'

#df['qty'] = 0
df['qty'] = 0
df['out_of_stock_qty'] = -5


df['product_online'] = df['is_in_stock']
df['price'] = df['price'].astype(str).str.replace('ر.س', '')
df['price'] = df['price'].astype(str).str.replace(',', '').astype(float)
df['special_price'] = df['price'].astype(str).str.replace('ر.س', '')
df['special_price'] = df['price'].astype(str).str.replace(',', '').astype(float)
df['cost'] = df['price']

# df['price'] = df['price'].str.replace('.', '').str.replace(',', '.').str.replace('رس', '').str.replace('ر.س', '').str.strip()
# df['special_price'] = df['special_price'].str.replace('.', '').str.replace('رس', '').str.replace(',', '.').str.replace('ر.س', '').str.replace('ر.س', '').str.strip()

# df['special_price'] = pd.to_numeric(df['special_price'])
# df['price'] = pd.to_numeric(df['price'])
# df['cost'] = df['price'] * 0.75
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

# df['cost'] = df['base_images']
df['small_image'] =  df['base_image']
df['swatch_image'] =  df['base_image']
df['thumbnail_image'] =  df['base_image']
df['estimated_delivery_enable'] = 'Static Text'
df['estimated_delivery_text'] = ''
df['url_key'] = df['sku'] + '-' + df['name'] 
# df['additionnel_images'] = ''
df['categories1'] = df['cat1']
df['categories2'] = df['cat2']
df['categories3'] = df['cat3']
df['categories'] = ''

df['special_price'] = ''
list_columns = [
    'special_price',
]
for column in list_columns:
    df.loc[(df[column] == '') | (df[column].isnull()), column] = '__EMPTY__VALUE__'

df = df[['sku number only', 'sku', 'store_view_code', 'attribute_set_code', 'product_type',  'product_websites',
         'name',  'estimated_delivery_enable', 'estimated_delivery_text',  'url_key',  'description'
, 'link_url', 'categories1', 'categories2', 'categories3', 'categories',
         
    'cost', 'price',  'special_price',  'visibility', 'tax_class_name', 'manufacturer',
         'news_from_date', 'news_to_date', 'base_image', 'small_image', 'swatch_image' 
    , 'thumbnail_image', 'add_images', 'product_online', 'qty', 'out_of_stock_qty', 'allow_backorders'
    , 'is_in_stock',  'supplier'
        ]]
list_columns = [
    'special_price'
]
for column in list_columns:
    df.loc[(df[column] == '') | (df[column].isnull()), column] = '__EMPTY__VALUE__'


df.to_excel(f'Aynma-update_product3.xlsx')