

from cgitb import enable
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import re



def get_data(url):
    
    # Fonction to scrape all urls from itch categories
    # Return Data
    
#     s = HTMLSession()
#     r = s.get(url)
#     r.html.render(timeout= 30, sleep=1)
    print('Url:', url)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    cookies = {'session': '134-8225175-0355220'}
    r = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(r.content, "html.parser")
    time.sleep(1)
    products = soup.find_all('form', {'card oe_product_cart'})
    
    liens = [toto.find('a')['href']  for toto in products]
    print('Len products', len(liens))
    list_liens = []
    
    for t in liens:
        list_liens.append(t)
#     print('list_cat1', list_cat1)
    data = {
        'url':list_liens,
        }
    # df = pd.DataFrame(data)
#     print(df)
#         print('Href: ', t['href'])
#     print("Soup get_data")
    return soup, list_liens


def getnextpage(soup):
   
    #Check if next url exist else send None objects
    # Return URL or None
    
    page = soup.find('a', text=re.compile('التالي'))
    # print('Page', page)
    
    try:
        # if next url exist 
        url2 = str('https://www.otantiksaudi.com' + page['href'])
        return url2
        # print('', url2)
    except:
        print('No Next')
        pass
    return url2 


# Extract new urls of Rugaib site from url categories

# url = 'https://rawae.com/search?subsubcategory=Accessories-box-Q3HaJ&page=1'
list_urls = []


def scrap_url_product(url1):
    
    cat1 = url1['cat1']
    cat2 = url1['cat2']
    cat3 = url1['cat3']
    url = url1['url']
    data = []
    while True:
        soup, urls_list = get_data(url)
        
        for toto in urls_list:

            # print(f'URL:', toto)
            data.append({
            'url':'https://www.otantiksaudi.com' + toto,
            'cat1': cat1,
            'cat2': cat2,
            'cat3': cat3,
            })

        try:
            url = getnextpage(soup)
#             print('Url dans le while', url)
        except:
            break
    # print(data)
    print( f'Scrape done .')
    return data


list_urls = [
    # {'cat1': 'Coffee Sets', 'cat2': 'Turkish coffee sets', 'cat3': '',  'url': 'https://www.otantiksaudi.com/en/shop/category/coffee-sets-turkish-coffee-sets-64'}, 
    # {'cat1': 'Coffee Sets', 'cat2': 'Arabic coffee sets', 'cat3': '',  'url': 'https://www.otantiksaudi.com/en/shop/category/coffee-sets-arabic-coffee-sets-65'}, 
    # {'cat1': 'Coffee Sets', 'cat2': 'Turkish coffee pot', 'cat3': '',  'url': 'https://www.otantiksaudi.com/en/shop/category/coffee-sets-turkish-coffee-pot-66'}, 
    # {'cat1': 'Coffee Sets', 'cat2': 'you & me COFFEE', 'cat3': '',  'url': 'https://www.otantiksaudi.com/en/shop/category/coffee-sets-you-me-coffee-67'}, 
    
    # {'cat1': 'Home Accessories', 'cat2': 'Under Plate', 'cat3': '',  'url': 'https://www.otantiksaudi.com/en/shop/category/home-accessories-under-plate-83'}, 
    # {'cat1': 'Home Accessories', 'cat2': 'Tissue box', 'cat3': '',  'url': 'https://www.otantiksaudi.com/en/shop/category/home-accessories-tissue-box-84'}, 
    # {'cat1': 'Home Accessories', 'cat2': 'Trash can', 'cat3': '',  'url': 'https://www.otantiksaudi.com/en/shop/category/home-accessories-trash-can-85'}, 
    # {'cat1': 'Home Accessories', 'cat2': 'Porcelain INCENSE BURNER', 'cat3': '',  'url': 'https://www.otantiksaudi.com/en/shop/category/home-accessories-trash-can-85'}, 
    
    
    # {'cat1': 'Serving Sets', 'cat2': 'Nuts serving sets', 'cat3': '',  'url': 'https://www.otantiksaudi.com/en/shop/category/serving-sets-nuts-serving-sets-68'}, 
    # {'cat1': 'Serving Sets', 'cat2': 'Cake serving sets', 'cat3': '',  'url': 'https://www.otantiksaudi.com/en/shop/category/serving-sets-cake-serving-sets-69'}, 
    # {'cat1': 'Serving Sets', 'cat2': 'Bowl serving sets', 'cat3': '',  'url': 'https://www.otantiksaudi.com/en/shop/category/serving-sets-bowl-serving-sets-70'}, 
    # {'cat1': 'Serving Sets', 'cat2': 'Two Layers with zinc handle', 'cat3': '',  'url': 'https://www.otantiksaudi.com/en/shop/category/serving-sets-two-layers-with-zinc-handle-71'}, 
    # {'cat1': 'Serving Sets', 'cat2': 'Dinner serving sets', 'cat3': '',  'url': 'https://www.otantiksaudi.com/en/shop/category/serving-sets-dinner-serving-sets-72'}, 
    # {'cat1': 'Serving Sets', 'cat2': 'Dessert Serving Set', 'cat3': '',  'url': 'https://www.otantiksaudi.com/en/shop/category/serving-sets-dessert-serving-set-73'}, 
    # {'cat1': 'Serving Sets', 'cat2': 'Juice cup sets', 'cat3': '',  'url': 'https://www.otantiksaudi.com/en/shop/category/serving-sets-juice-cup-sets-74'}, 
    # {'cat1': 'Serving Sets', 'cat2': 'Juice Dispenser', 'cat3': '',  'url': 'https://www.otantiksaudi.com/en/shop/category/serving-sets-juice-dispenser-75'}, 
    # {'cat1': 'Serving Sets', 'cat2': 'Spices sets', 'cat3': '',  'url': 'https://www.otantiksaudi.com/en/shop/category/serving-sets-spices-sets-76'}, 
    # {'cat1': 'Serving Sets', 'cat2': 'Buffet Sets', 'cat3': '',  'url': 'https://www.otantiksaudi.com/en/shop/category/serving-sets-buffet-sets-91'}, 
    
    # {'cat1': 'Serving Trays', 'cat2': 'Acrylic Serving Trays', 'cat3': '',  'url': 'https://www.otantiksaudi.com/en/shop/category/serving-trays-acrylic-serving-trays-87'},
    # {'cat1': 'Serving Trays', 'cat2': 'Porcelain Serving Trays', 'cat3': '',  'url': 'https://www.otantiksaudi.com/en/shop/category/serving-trays-porcelain-serving-trays-88'},
    # {'cat1': 'Serving Trays', 'cat2': 'Wooden Serving Trays', 'cat3': '',  'url': 'https://www.otantiksaudi.com/en/shop/category/serving-trays-wooden-serving-trays-89'},
    # {'cat1': 'Serving Trays', 'cat2': 'Metal Serving Trays', 'cat3': '',  'url': 'https://www.otantiksaudi.com/en/shop/category/serving-trays-metal-serving-trays-90'},
    # {'cat1': 'Serving Trays', 'cat2': 'Leather Tray', 'cat3': '',  'url': 'https://www.otantiksaudi.com/en/shop/category/serving-trays-leather-tray-92'},
    
    # {'cat1': 'Tea sets', 'cat2': 'Porcelain tea sets', 'cat3': '',  'url': 'https://www.otantiksaudi.com/en/shop/category/tea-sets-porcelain-tea-sets-77'}, 
    # {'cat1': 'Tea sets', 'cat2': 'you & me TEA', 'cat3': '',  'url': 'https://www.otantiksaudi.com/en/shop/category/tea-sets-you-me-tea-78'}, 
    # {'cat1': 'Tea sets', 'cat2': 'Tea glass and coffee sets Dantel Cup', 'cat3': '',  'url': 'https://www.otantiksaudi.com/en/shop/category/tea-sets-porcelain-tea-sets-77'}, 
    # {'cat1': 'Tea sets', 'cat2': 'Tea glass and coffee sets Heybeli Cup', 'cat3': '',  'url': 'https://www.otantiksaudi.com/en/shop/category/tea-sets-tea-glass-and-coffee-sets-heybeli-cup-80'}, 
    # {'cat1': 'Tea sets', 'cat2': 'Tea glass sets', 'cat3': '',  'url': 'https://www.otantiksaudi.com/en/shop/category/tea-sets-tea-glass-sets-81'}, 
    # {'cat1': 'Tea sets', 'cat2': 'Tea Pot', 'cat3': '',  'url': 'https://www.otantiksaudi.com/en/shop/category/tea-sets-tea-pot-82'}, 
    
    # {'cat1': 'Vacuum Flask', 'cat2': 'Porcelain Vacuum Flask', 'cat3': '',  'url': 'https://www.otantiksaudi.com/en/shop/category/vacuum-flask-porcelain-vacuum-flask-60'}, 
    # {'cat1': 'Vacuum Flask', 'cat2': 'Plastic Vacuum Flask', 'cat3': '',  'url': 'https://www.otantiksaudi.com/en/shop/category/vacuum-flask-plastic-vacuum-flask-61'}, 
    # {'cat1': 'Vacuum Flask', 'cat2': 'Vacuum Flasks Set', 'cat3': '',  'url': 'https://www.otantiksaudi.com/en/shop/category/vacuum-flask-vacuum-flasks-set-62'}, 
    # {'cat1': 'Vacuum Flask', 'cat2': 'Steel Vacuum Flask', 'cat3': '',  'url': 'https://www.otantiksaudi.com/en/shop/category/vacuum-flask-vacuum-flasks-set-62'}, 

    {'cat1':'', 'cat2': '', 'cat3': '', 'url': 'https://www.otantiksaudi.com/ar/shop?attrib=0-55'},
   
    {'cat1':'', 'cat2': '', 'cat3': '', 'url': 'https://www.otantiksaudi.com/ar/shop?attrib=0-56'}
]


df = pd.read_excel('otantiksaudi_model_url.xlsx')

for i, url in enumerate(list_urls):
    print('Count: ', i)
    data = scrap_url_product(url)
    df1 = pd.DataFrame(data)
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('otantiksaudi_update_url.xlsx')