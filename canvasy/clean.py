

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

df1 = pd.read_excel('cancasy_product_update.xlsx')
df2 = pd.read_excel('cancasy_product_update1.xlsx')
df3 = pd.read_excel('cancasy_product_update2.xlsx')

df = pd.concat([df1, df2, df3], ignore_index=True)
df['categories'] = ''
# list_cats = []
# for index, row in toto.iterrows():
#     list_cats.append({'id': row['id'],  'categories1': row['categories1'], 'categories2': row['categories2'], 'categories3': row['categories3'], })
    
# for cat in list_cats:
#     df.loc[(df['categories2']== cat['categories2']) & (df['categories3']== cat['categories3']), 'categories'] = cat['id']

df[['ts_dimensions_length', 'ts_dimensions_width']] = df['size'].str.replace('سنتيمتر', '').str.replace('x', '×').str.split('×', 1, expand=True)

two_month = datetime.now() + timedelta(days=60)
two_month = two_month.strftime("%m/%d/%Y")
today = datetime.today().strftime("%m/%d/%Y")



df['news_from_date'] = today
df['news_to_date'] = two_month
df['product_websites'] = 'base'

df['store_view_code'] = ''
#df.drop_duplicates(subset=['sku'], inplace=True)
df['supplier'] = ''
df['sku'] = 'can-' + df['sku']
df['sku number only'] = df['sku'].str.replace('-', '')
# df['sku number only'] = ''

df['NEW SKU'] = 'can-' + df['NEW SKU']
df['manufacturer'] = 'مستوردة'
df['product_websites'] = 'base'
df['is_in_stock'] = 1
df['allow_backorders'] = 1
df['tax_class_name'] = 'Taxable Goods'
df['allow_bakcorder'] = 1

df['out_of_stock_qty'] = -50


df['product_online'] = 1

# df['price'] = df['price'].str.replace(',', '').str.strip()
# df['special_price'] = df['special_price'].str.replace(',', '').str.strip()

df['special_price'] = pd.to_numeric(df['special_price'])
df['price'] = pd.to_numeric(df['price'])
df['cost'] = df['price'] * 0.75
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
df['size1'] = df['size'].str.replace(' ', '-').str.replace('×', '*').str.strip()
df['brozes1'] = df['prozes'].str.replace(' ', '-').str.strip()

# df['base_image'] = df['base_images']

df['small_image'] =  df['base_image']
df['swatch_image'] =  df['base_image']
df['thumbnail_image'] =  df['base_image']
df['additional_images'] = df['add_images']


df['estimated_delivery_enable'] = 'Static Text'
df['estimated_delivery_text'] = ''
df['url_key'] =  df['name']   + df['size1'] + ',' + df['brozes1']
# df['additionnel_images'] = ''
df['categories3'] = ''
df['categories'] = '55'
df['meta_title'] = df['name'] + '-' + df['size'] + ',' + df['prozes']
df['short_description'] = df['description']
df['raw_materials'] = 'كانفاس'
df['manage_stock'] = 1
df['no_of_peices'] = 1
df['special_price'] = ''
list_columns = [
    'special_price',
]
for column in list_columns:
    df.loc[(df[column] == '') | (df[column].isnull()), column] = '__EMPTY__VALUE__'

df = df[['NEW SKU', 'sku', 'weight', 'configurable_variations', 'attribute_set_code','product_type',  
         'visibility', 'cost', 'price', 'special_price',  'additional_attributes', 'categories',
         'product_websites', 'name', 'meta_title', 'meta_description', 'description', 'short_description',
         'url_key', 'product_online', 'qty', 'is_in_stock', 'allow_bakcorder', 'out_of_stock_qty',  
          
         'manufacturer', 'raw_materials',  'no_of_peices', 
         'ts_dimensions_length', 'ts_dimensions_width', 
         'base_image', 'small_image', 'swatch_image', 'thumbnail_image', 'additional_images',
         'manage_stock', 'store_view_code', 'supplier'
         
        ]]


df.to_excel(f'canvasy-update_product_clean_data3.xlsx')

