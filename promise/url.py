

from bs4 import BeautifulSoup
import requests
import time
import pandas as pd



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
    liens = soup.find('div', {'class': 'product-sorted'}).find_all('div', {'class':'col-xs-6 col-md-4 col-lg-3 product-box'})
    len(liens)
    list_products = [p.find('a')['href'] for p in liens]
    print('Len products', len(list_products))

#     print('list_cat1', list_cat1)

    # df = pd.DataFrame(data)
#     print(df)
#         print('Href: ', t['href'])
#     print("Soup get_data")
    return list_products


def getnextpage(soup):
   
    #Check if next url exist else send None objects
    # Return URL or None
    
    page = soup.find('a', {'class': 'next i-next'})
    # print('Page', page)
    
    try:
        # if next url exist 
        url2 = str(page['href'])
        return url2
        # print('', url2)
    except:
        print('No Next')
        pass
    return url2 


# Extract new urls of Rugaib site from url categories

# url = 'https://rawae.com/search?subsubcategory=Accessories-box-Q3HaJ&page=1'
list_urls = []


def scrap_url_product(urls):
    
    
    url = urls['url']
    cat1 = urls['cat1']
    cat2 = urls['cat2']
    cat3 = urls['cat3']
    pg = urls['page']
    data = []

    
    urls_list = get_data(url + f'?page={pg}')
    
    for toto in urls_list:

        # print(f'URL:', toto)
        data.append({
        'url':toto,
        'categories1': cat1,
        'categories2': cat2,
        'categories3': cat3,
        })
    
    print( f'Scrape done .')
    return data

list_urls = [
    {'cat1':'مفارش', 'cat2':'مفارش شتوية', 'cat3':'مزدوج', 'url' : 'https://promise-ksa.com/category/lEgDg', 'page': 1},
    {'cat1':'مفارش', 'cat2':'مفارش شتوية', 'cat3':'مزدوج', 'url' : 'https://promise-ksa.com/category/lEgDg', 'page': 2},
    {'cat1':'مفارش', 'cat2':'مفارش شتوية', 'cat3':'مفرد ونص', 'url' : 'https://promise-ksa.com/category/AGory', 'page': 1},
    {'cat1':'مفارش', 'cat2':'مفارش شتوية', 'cat3':'مفرد ونص', 'url' : 'https://promise-ksa.com/category/AGory', 'page': 2},
    {'cat1':'مفارش', 'cat2':'مفارش صيفية', 'cat3':'مزدوج', 'url' : 'https://promise-ksa.com/category/orWDl', 'page': 1},
    {'cat1':'مفارش', 'cat2':'مفارش صيفية', 'cat3':'مفرد ونص', 'url' : 'https://promise-ksa.com/category/rdEDw', 'page': 1},
    {'cat1':'مفارش', 'cat2':'مفارش فاخرة', 'cat3':'مزدوج', 'url' : 'https://promise-ksa.com/category/Qanox', 'page': 1},
    {'cat1':'مفارش', 'cat2':'مفارش فندقية', 'cat3':'مزدوج', 'url' : 'https://promise-ksa.com/category/EmBer', 'page': 1},
    {'cat1':'مفارش', 'cat2':'مفارش فندقية', 'cat3':'مفرد ونص', 'url' : 'https://promise-ksa.com/category/EmBrr', 'page': 1},
    {'cat1':'مفارش', 'cat2':'أطقم بيت لحاف', 'cat3':'مزدوج', 'url' : 'https://promise-ksa.com/category/ebGaO', 'page': 1},
    {'cat1':'مفارش', 'cat2':'أطقم غطاء سرير', 'cat3':'مزدوج', 'url' : 'https://promise-ksa.com/category/ZEzZB', 'page': 1},
    {'cat1':'مفارش', 'cat2':'أطقم غطاء سرير', 'cat3':'مفرد ونص', 'url' : 'https://promise-ksa.com/category/mjRwa', 'page': 1},
    {'cat1':'مفارش', 'cat2':'مفارش أطفال', 'cat3':'', 'url' : 'https://promise-ksa.com/category/WWjwz', 'page': 1},
    {'cat1':'مفارش', 'cat2':'مفارش نفاس', 'cat3':'', 'url' : 'https://promise-ksa.com/category/DmKRY', 'page': 1},
    {'cat1':'لباد و حشوات', 'cat2':'لباد', 'cat3':'', 'url' : 'https://promise-ksa.com/category/Emanq', 'page': 1 },
    {'cat1':'لباد و حشوات', 'cat2':'واقي سرير', 'cat3':'', 'url' : 'https://promise-ksa.com/category/QaXNw', 'page': 1},
    {'cat1':'لباد و حشوات', 'cat2':'واقي مخدة', 'cat3':'', 'url' : 'https://promise-ksa.com/category/ebWED', 'page': 1},
    {'cat1':'لباد و حشوات', 'cat2':'حشوة لحاف', 'cat3':'', 'url' : 'https://promise-ksa.com/category/XDByR', 'page': 1},
    {'cat1':'مخدات', 'cat2':'مخدات فندقية', 'cat3':'', 'url' : 'https://promise-ksa.com/category/zGOPr', 'page': 1},
    {'cat1':'مخدات', 'cat2':'مخدات طبية', 'cat3':'', 'url' : 'https://promise-ksa.com/category/ZEwvx', 'page': 1},
    {'cat1':'العرائس', 'cat2':'مفارش عرائس', 'cat3':'', 'url' : 'https://promise-ksa.com/category/Yxrdo', 'page': 1},
    {'cat1':'الشراشف', 'cat2':'شراشف مزدوج', 'cat3':'', 'url' : 'https://promise-ksa.com/category/rdBGy', 'page': 1},
    {'cat1':'الشراشف', 'cat2':'شراشف مفرد ونص', 'cat3':'', 'url' : 'https://promise-ksa.com/category/yRaPl', 'page': 1},
    {'cat1':'بطانيات', 'cat2':'بطانيات مزدوج', 'cat3':'', 'url' : 'https://promise-ksa.com/category/bKgWx', 'page': 1},
    {'cat1':'بطانيات', 'cat2':'بطاانيات مفرد ونص', 'cat3':'', 'url' : 'https://promise-ksa.com/category/gRxej', 'page': 1},
    {'cat1':'بطانيات', 'cat2':'شالات', 'cat3':'', 'url' : 'https://promise-ksa.com/category/ROqow', 'page': 1},
    {'cat1':'بطانيات', 'cat2':'بلوفر الدفى', 'cat3':'', 'url' : 'https://promise-ksa.com/category/WlAYYN', 'page': 1},
    {'cat1':'الحمام', 'cat2':'دعاسات', 'cat3':'', 'url' : 'https://promise-ksa.com/category/EmaBY', 'page': 1},
    {'cat1':'الحمام', 'cat2':'إكسسوار الحمام', 'cat3':'', 'url' : 'https://promise-ksa.com/category/QaXnv', 'page': 1},
    {'cat1':'إكسسوارات المنزل', 'cat2':'معطرات', 'cat3':'', 'url' : 'https://promise-ksa.com/category/XDBXA', 'page': 1},

]


df = pd.read_excel('urls_models.xlsx')
for i, url in enumerate(list_urls):
    print('Count: ', i)
    
    print('Range: ', url['page'])
    
    data = scrap_url_product(url)
    df1 = pd.DataFrame(data)
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('Promise_url.xlsx')

