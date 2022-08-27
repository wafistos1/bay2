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
import re
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup
import requests


name_cat = 'finesthomee_update_12_04.xlsx'
list_cate = [
('6723,6724,113',	'اضاءات'),
('42,42800'	'مباخر'),
('43816,43,113',	'شمعدان'),
('42915,42918',	'اكواب'),
('44100,44101,44104',	'فناجيل'),
('44100,44101,44103',	'بيالات'),
('42915,42916,42922,113','حامل'),
('42,48,113',	'وردة زجاجية'),
('42915,42916',	'أطقم منزلية وتقديمات'),
('42927',	'كوستر'),
]

df = pd.read_excel('/home/wafistos/Documents/Projects/scaping_wafi/finesthomee/Fineshomee_update.xlsx')
two_month = datetime.now() + timedelta(days=60)
two_month = two_month.strftime("%m/%d/%Y")
today = datetime.today().strftime("%m/%d/%Y")



df['news_from_date'] = today
df['news_to_date'] = two_month
df['product_websites'] = 'base'
df['attribute_set_code'] = 'Default'
df['product_type'] = 'simple'
df['store_view_code'] = ''

df['supplier'] = 'FIN'
df['sku'] = 'FIN-' +   df['sku']
df['sku number only'] = df['sku'].str.replace('FIN-', '')
df['manufacturer'] = 'مستوردة'
df['product_websites'] = 'base'
df.loc[df['qty'] !=0, 'is_in_stock'] = 1
df.loc[df['is_in_stock'] != 1, 'is_in_stock'] = 0
df['allow_backorders'] = df['is_in_stock']
df['visibility'] = 'Catalog, Search'
df['tax_class_name'] = 'Taxable Goods'


df['out_of_stock_qty'] = -5
df['product_online'] = df['is_in_stock']
df.loc[df['product_online'] == 0, 'product_online'] = 2

df['product_online'] = df['is_in_stock']

df.loc[df['price'].isnull(), 'price'] = df['special_price']
df.loc[df['price'] == df['special_price'], 'special_price'] = '__EMPTY__VALUE__'
try:
    df['price'] = df['price'].str.replace(',', '')
except:
    pass



df['price'] = pd.to_numeric(df['price'])
df['cost'] = df['price'] * 0.7
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



df['small_image'] =  df['base_image']
df['swatch_image'] =  df['base_image']
df['thumbnail_image'] =  df['base_image']


df['estimated_delivery_enable'] = 'Static Text'
df['estimated_delivery_text'] = ''
df['url_key'] = df['sku'] + '-' + df['name'] 


df['categories2']  = ''
df['categories3']  = ''


df = df[['sku number only', 'sku', 'store_view_code', 'attribute_set_code', 'product_type',  'product_websites',
         'name',  'estimated_delivery_enable', 'estimated_delivery_text',  'url_key',  'description'
, 'link_url', 'categories1', 'categories2', 'categories3', 'categories', 
         'ts_dimensions_height', 'ts_dimensions_length',
         
          'amper', 'power', 'rechargeable', 'no_of_lamps',   'with_controller',
         
    'cost', 'price',  'special_price',   'visibility', 'tax_class_name', 'manufacturer',
         'news_from_date', 'news_to_date', 'base_image', 'small_image', 'swatch_image' 
    , 'thumbnail_image', 'additionnel_images', 'product_online', 'qty', 'out_of_stock_qty', 'allow_backorders'
    , 'is_in_stock',  'supplier'
        ]]

list_columns = [
    
    'ts_dimensions_length',
    'ts_dimensions_height',
    'amper',
    'power',
    'rechargeable',
    'no_of_lamps',
    'with_controller',
    
    

    
]
for column in list_columns:
    df.loc[(df[column] == '') | (df[column].isnull()), column] = '__EMPTY__VALUE__'

df.to_excel(f'-{name_cat}.xlsx')