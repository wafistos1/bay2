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

df1 = pd.read_excel('/home/wafistos/Documents/Projects/scaping_wafi/Noon/Noon-wafi-products1.xlsx')
df2 = pd.read_excel('/home/wafistos/Documents/Projects/scaping_wafi/Noon/Noon-wafi-products2.xlsx')
df3 = pd.read_excel('/home/wafistos/Documents/Projects/scaping_wafi/Noon/Noon-wafi-products3.xlsx')


print('df1', df1.shape)
print('df2', df2.shape)
print('df3', df3.shape)
df = pd.read_excel('/home/wafistos/Documents/Projects/scaping_wafi/Noon/Noon_model_product.xlsx')
df = pd.concat([df, df1], ignore_index=True)
df = pd.concat([df, df2], ignore_index=True)
df = pd.concat([df, df3], ignore_index=True)
df.to_excel('toto.xlsx')
# df.drop_duplicates(subset=['sku'], inplace=True)
df.drop(df.loc[df['categories3'].str.contains('https:')].index, inplace=True)
df.drop(df.loc[df['categories2'].str.contains('https:')].index, inplace=True)
df.drop(df.loc[df['categories1'].str.contains('https:')].index, inplace=True)
print('Len products: ' ,df.shape)
toto = pd.read_excel('/home/wafistos/Downloads/Noon-categories-1 (1)(2).xlsx')
df['categories'] = ''

list_cats = []
for index, row in toto.iterrows():
    list_cats.append({'categories3': row['categories3'], 'id': row['id']})
    
for cat in list_cats:
    df.loc[df['categories3']== cat['categories3'], 'categories'] = cat['id']
    

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
df['supplier'] = 'STR'
df['sku'] = 'STR-' + df['sku']
df['sku number only'] = df['sku'].str.replace('STR-', '')
df['manufacturer'] = 'مستوردة'
df['product_websites'] = 'base'
df['is_in_stock']=1
df['allow_backorders'] = df['is_in_stock']
df['visibility'] = 'Catalog, Search'
df['tax_class_name'] = 'Taxable Goods'

df['qty'] = 0
df['out_of_stock_qty'] = -5


df['product_online'] = df['is_in_stock']
df.loc[df['raw_materials'].isnull(), 'raw_materials'] =  '__EMPTY__VALUE__'

df['price'] = df['price'].str.rstrip(' .').str.strip()
df['special_price'] = df['special_price'].str.rstrip(' .').str.strip()
df['price'] = df['price'].str.rstrip('.‏()').str.strip()
df['special_price'] = df['special_price'].str.rstrip('.‏()').str.strip()

df['price'] = pd.to_numeric(df['price'])
df['special_price'] = pd.to_numeric(df['special_price'])
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



df['small_image'] =  df['base_images']
df['swatch_image'] =  df['base_images']
df['thumbnail_image'] =  df['base_images']


df['estimated_delivery_enable'] = 'Static Text'
df['estimated_delivery_text'] = ''
df['url_key'] = df['sku'] + '-' + df['name'] 


df = df[['sku number only', 'sku', 'store_view_code', 'attribute_set_code', 'product_type',  'product_websites',
         'name',  'estimated_delivery_enable', 'estimated_delivery_text',  'url_key',  'description'
, 'link_url', 'categories1', 'categories2', 'categories3', 'categories',
         
            'free_colors',
    'ts_dimensions_width',
    'ts_dimensions_length',
    'ts_dimensions_height',
    'weight',
    'products_size',
    'set_include',
    'raw_meterials',
         
    'cost', 'price',  'special_price',  'visibility', 'tax_class_name', 'manufacturer',
         'news_from_date', 'news_to_date', 'base_images', 'small_image', 'swatch_image' 
    , 'thumbnail_image', 'additionnel_images', 'product_online', 'qty', 'out_of_stock_qty', 'allow_backorders'
    , 'is_in_stock',  'supplier'
        ]]

list_columns = [
    'special_price',
    'free_colors',
    'ts_dimensions_width',
    'ts_dimensions_length',
    'ts_dimensions_height',
    'weight',
    'products_size',
    'set_include',
    'raw_meterials',
    'manufacturer',    
]
for column in list_columns:
    df.loc[(df[column] == '') | (df[column].isnull()), column] = '__EMPTY__VALUE__'

df.to_excel(f'Noon-new-update4.xlsx')