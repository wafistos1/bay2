

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
    products = soup.find_all('a', {'class': 'product-image-link'})
    len(products)

    list_products = [pro['href'] for pro in products]
    cats = soup.find('nav', {'class': 'woocommerce-breadcrumb'}).find_all('a')
    
    if len(cats) == 1:
        cat1 = soup.find('nav', {'class': 'woocommerce-breadcrumb'}).find('span').text.strip()
        cat2 = ''
    else:
        cat1 = cats[1].text.strip()
        cat2 = soup.find('nav', {'class': 'woocommerce-breadcrumb'}).find('span').text.strip()
        
    data = []
    for product in list_products:
        data.append(
            {
                'url': product,
                'cat1': cat1,
                'cat2': cat2,
                }
        )
        
        
    
        

    return soup, data


def getnextpage(soup):
   
    #Check if next url exist else send None objects
    # Return URL or None
    
    page = soup.find('a', {'class': 'next page-numbers'})
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
list_urls = [
    'https://ansaaj.com/product-category/kitchen/',
    
    'https://ansaaj.com/product-category/baby-room/childrens-detachment/',
    'https://ansaaj.com/product-category/baby-room/blanket-children/',
    'https://ansaaj.com/product-category/baby-room/bag-mother/',
    'https://ansaaj.com/product-category/baby-room/cheers-for-breastfeeding/',
    'https://ansaaj.com/product-category/baby-room/pedals/',
    
    'https://ansaaj.com/product-category/living-room/carpets/',
    'https://ansaaj.com/product-category/living-room/creative/',
    
    'https://ansaaj.com/product-category/bedroom/%d8%a3%d8%b3%d8%a7%d8%b3%d9%8a%d8%a7%d8%aa-%d8%a7%d9%84%d8%b3%d8%b1%d9%8a%d8%b1/',
    'https://ansaaj.com/product-category/bedroom/blankets/',
    'https://ansaaj.com/product-category/bedroom/bed-cover/',
    'https://ansaaj.com/product-category/bedroom/quilts/',
    
    'https://ansaaj.com/product-category/towels-and-robes/robes/',
    'https://ansaaj.com/product-category/towels-and-robes/propaganda/',
    'https://ansaaj.com/product-category/towels-and-robes/towels/',
]


def scrap_url_product(url):
    
    
    
    
    data = []
    
    while True:
        soup, urls_list = get_data(url)
        
        for toto in urls_list:

            # print(f'URL:', toto)
            data.append({
            'url':toto['url'],
            'cat1': toto['cat1'],
            'cat2': toto['cat2'],
            })

        try:
            url = getnextpage(soup)
#             print('Url dans le while', url)
        except:
            break
    # print(data)
    print( f'Scrape done .')
    return data



df = pd.read_excel('anssaj_url_model.xlsx')

for i, url in enumerate(list_urls):

    data = scrap_url_product(url)
    df1 = pd.DataFrame(data)
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('ansaaj_url1.xlsx')


