import string
from datetime import datetime
from datetime import timedelta
import pandas as pd


two_month = datetime.now() + timedelta(days=60)
two_month = two_month.strftime("%m/%d/%Y")
today = datetime.today().strftime("%d/%m/%Y")
today1 = datetime.today().strftime("%d_%m_%Y")

df1 = pd.read_excel('/home/wafistos/Documents/Projects/scaping_wafi/Midas1/midas_update_23-08-2022-1.xlsx')
df2 = pd.read_excel('/home/wafistos/Documents/Projects/scaping_wafi/Midas1/midas_update_23-08-2022-2.xlsx')
df3 = pd.read_excel('/home/wafistos/Documents/Projects/scaping_wafi/Midas1/midas_update_23-08-2022-3.xlsx')
df4 = pd.read_excel('/home/wafistos/Documents/Projects/scaping_wafi/Midas1/midas_update_23-08-2022-4.xlsx')
df5 = pd.read_excel('/home/wafistos/Documents/Projects/scaping_wafi/Midas1/midas_update_23-08-2022-5.xlsx')
df6 = pd.read_excel('/home/wafistos/Documents/Projects/scaping_wafi/Midas1/midas_update_23-08-2022-6.xlsx')
df7 = pd.read_excel('/home/wafistos/Documents/Projects/scaping_wafi/Midas1/midas_update_23-08-2022-7.xlsx')



df = pd.concat([df1, df2, df3, df4, df5, df6, df7], ignore_index=True)
df.to_excel('brut.xlsx')
df.drop_duplicates(subset=['sku'], inplace=True)

# Clean functions
def clean_punct(name):
    for c in string.punctuation:
        df[name] = df[name].str.replace(c, '-', regex=False)

def toto_clean(name):
    df[name] = df[name].str.replace('\\xa', '-', regex=False)
    df[name] = df[name].str.replace(']', '', regex=False)
    df[name] = df[name].str.replace('[', '', regex=False)
    df[name] = df[name].str.replace('•', '-')
    df[name] = df[name].str.replace(':', '-')
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
    df[name] = df[name].str.replace('#', '-')
    df[name] = df[name].str.replace('”', '-')
    df[name] = df[name].str.replace('!', '-')
    df[name] = df[name].str.replace('♦', '-')
    df[name] = df[name].str.replace('♦', '-')
    df[name] = df[name].str.replace('♦', '-')
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
# Clean Columns
toto_clean('name')
toto_clean('url_key')
clean_punct('name')
clean_punct('description')
toto_clean('description')
#toto_clean('short_description')
#clean_punct('short_description')
toto_clean('free_colors')
clean_punct('free_colors')
toto_clean('products_size')
toto_clean('product_size1')

# Colors Columns
df[['color','sec_color']] = df['free_colors'].str.split("-",expand=True,n = 1)
df.loc[df['sec_color']== 'شفاف', 'raw_materials'] = 'شفاف'
df.loc[df['color']== 'مراية', 'raw_materials'] = 'مراية'
df.loc[df['sec_color']== 'مراية', 'raw_materials'] = 'مراية'
df.loc[df['color']== 'شفاف', 'raw_materials'] = 'شفاف'
df.loc[df['color']== 'لون زجاجى', 'raw_materials'] = 'لون زجاجى'
df.loc[df['sec_color']== 'لون زجاجى', 'raw_materials'] = 'لون زجاجى'
df.loc[df['color']== ' زجاجى', 'raw_materials'] = ' زجاجى'
df.loc[df['sec_color']== ' زجاجى', 'raw_materials'] = ' زجاجى'
df.loc[df['color']== 'شفاف', 'color'] = '__EMPTY__VALUE__'
df.loc[df['color']== 'مراية', 'color'] = '__EMPTY__VALUE__'
df.loc[df['color']== 'لون زجاجى', 'color'] = '__EMPTY__VALUE__'
df.loc[df['color']== 'زجاجى', 'color'] = '__EMPTY__VALUE__'
df.loc[df['sec_color']== 'شفاف', 'sec_color'] = '__EMPTY__VALUE__'
df.loc[df['sec_color']== 'مراية', 'sec_color'] = '__EMPTY__VALUE__'
df.loc[df['sec_color']== 'لون زجاجى', 'sec_color'] = '__EMPTY__VALUE__'
df.loc[df['sec_color']== 'زجاجى', 'sec_color'] = '__EMPTY__VALUE__'
df.loc[df['color'].str.len() >= 30, 'color' ] = '__EMPTY__VALUE__'
df.loc[(df['free_colors'].str.contains('نظرة عامة')) | (df['free_colors'].isnull()) , 'color'] = '__EMPTY__VALUE__'
df.loc[df['color'] == '', 'color'] = '__EMPTY__VALUE__'
df.loc[df['color'].isnull(), 'color'] = '__EMPTY__VALUE__'
df.loc[df['sec_color'].isnull(), 'sec_color'] = '__EMPTY__VALUE__'
df.loc[df['sec_color'] == '', 'sec_color'] = '__EMPTY__VALUE__'
clean_punct('url_key')
df['description'] = df['description'].str.replace('♦', '', regex=False)
df['short_description'] = df['description']
df['ts_dimensions_width'] = df['width']
df['ts_dimensions_height'] = df['height']
df['ts_dimensions_length'] = df['length']
# Clean Prices:
df['price'] = pd.to_numeric(df['price'])
df['cost'] = df['price'] * 0.7
df['price1'] = df['price'] * 1.15

# df['categories1'] = df['category1']
# df['categories2'] = df['category2']
# df['categories3'] = df['category3']
# Add Categories Columns
cats = pd.read_excel("/home/wafistos/Documents/Projects/scaping_wafi/Scraping_Midas/Categories/Midas category(1).xlsx")
list_cats = []
for index, row in cats.iterrows():
    list_cats.append([row['Name of category '], row['Num of category '], row['description']]) 
for tt in list_cats:
    df.loc[df['categories2'] == tt[0], 'categories'] =  tt[1]
for tt in list_cats:
    df.loc[df['categories3'] == tt[0], 'categories'] = tt[1]
for tt in list_cats:
    df.loc[(df['categories'] == tt[1]) & (df['description'].isnull()), 'description'] =  tt[2]

#Clean data

df['free_colors'] = df['free_colors'].str.replace('،', '-')
df['free_colors'] = df['free_colors'].str.replace(' لا', '__EMPTY__VALUE__')
df['raw_materials'] = df['raw_materials'].str.replace('/', '-')
df['free_colors'] = df['free_colors'].str.replace('/', '-', regex=False) 
df['sku'] = df['sku'].str.replace('المنتج', '')
df['url_key'] = df['name']+ '-' + df['sku']
df.loc[~df['estimated_delivery_text'].isnull(), 'is_in_stock'] = 0

# Extract  estimated_delivery_text
df.loc[df['estimated_delivery_text'].isnull(), 'estimated_delivery_text'] =  'الوقت المقدر لشحن هذا المنتج أسبوعين'

df['estimated_delivery_enable'] = 'Static Text'
df.loc[df['is_in_stock'] == 'متوفر', 'is_in_stock'] = 1
df.loc[df['is_in_stock'] == 'غير متوفر', 'is_in_stock'] = 0
df['allow_backorders'] = df['is_in_stock']
df['product_online'] = df['is_in_stock']
df['qty'] = df['is_in_stock']  
df['product_online'] = df['is_in_stock']
df['qty'] = df['is_in_stock']  
df.loc[df['product_online'] == 2, 'out_of_stock_qty'] = 0
df.loc[df['product_online'] == 2, 'qty'] = 0
df.loc[df['product_online'] == 2, 'allow_backorders'] = 0
df.loc[df['product_online'] == 2, 'out_of_stock_qty'] = 0

# Check if special price is correct
for index, row in df.iterrows():
    if row['special_price'] != '__EMPTY__VALUE__':
        if row['special_price'] < row['price'] * 0.5 :
            print('ALERT----in', index, ': ', row['price'],'-' , row['special_price'], '-', row['Link_url'])

# extract name
df['name'] = df['name'].str.replace('\n', '')
df['sku number only'] = df['sku'].str.replace('DAS-', '')
df['product_type'] = 'simple'
df['special_price'] = '__EMPTY__VALUE__'
# Clean and empty value in emplty rows

# clean description
df['description'] = df['description'].str.replace('-xa0', '')
df['short_description'] = df['description']

list_columns = [
    'special_price',
    'free_colors',
    'free_color1',
    'raw_materials',
    'raw_material',
    'Weight',
    'ts_dimensions_width',
    'ts_dimensions_length',
    'ts_dimensions_height',
    'style',
    'style1',
    'no_of_peices',
]
for column in list_columns:
    df.loc[(df[column] == '') | (df[column].isnull()), column] = '__EMPTY__VALUE__'

df = df[['sku number only', 'sku', 'store_view_code', 'attribute_set_code', 
         'product_type',  'product_websites',
         'name',  'estimated_delivery_enable', 'estimated_delivery_text',  
         'url_key',  'description', 'short_description', 'products_size',
 'Link_url', 'categories1', 'categories2', 'categories3', 'categories',
         'set_include', 'color', 'sec_color',  'raw_materials','ts_dimensions_width', 
         'ts_dimensions_height', 'ts_dimensions_length',
             'raw_material',
            'free_color1',
            'style1',
            'no_of_peices',
            'product_size1',
    'cost',    
         'price1','price', 'special_price' , 'visibility', 'tax_class_name', 'manufacturer',
         'news_from_date', 'news_to_date', 'base_image', 'small_image', 'swatch_image' 
    , 'thumbnail_image', 'additional_images', 'product_online', 'qty', 'out_of_stock_qty', 'allow_backorders'
    , 'is_in_stock', 'style', 'supplier'
        ]]

df.to_excel(f'Midas_update_all_{today1}.xlsx')
