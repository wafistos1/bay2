

from bs4 import BeautifulSoup
import requests
import time
import pandas as pd



def get_data(url):
    print('Url:', url)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    cookies = {'session': '134-8225175-0355220'}
    r = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(r.content, "html.parser")
    time.sleep(1)
    products = soup.find_all('a', {'class': 'a-link-normal s-no-outline'})
    len(products)
    list_products = ['https://www.amazon.sa' + pro['href'] for pro in products]
    print('Len products', len(list_products))
    list_liens = []
    
    for t in list_products:
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

    page = soup.find('a', {'class': 's-pagination-item s-pagination-next s-pagination-button s-pagination-separator'})
    # print('Page', page)
    
    try:
        # if next url exist 
        url2 = str('https://www.amazon.sa' + page['href'])
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
    print(cat1, cat2, cat3)
    while True:
        soup, urls_list = get_data(url)
        
        for toto in urls_list:

            # print(f'URL:', toto)
            data.append({
            'url':toto,
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

urls_list = [
    {'url': 'https://www.amazon.sa/s?k=%D8%A8%D9%8A%D9%88%D8%AA%D9%8A+%D9%84%D8%A7%D9%86%D8%AF+%D8%AC%D8%A7%D8%B1%D8%AF%D9%86%D8%B2&ref=bl_dp_s_web_0','cat1': '', 'cat2': '', 'cat3': ''},
]
df = pd.read_excel('amz_url_model.xlsx')

data = scrap_url_product(urls_list[0])

df1 = pd.DataFrame(data)
df = pd.concat([df, df1], ignore_index=True)
df.to_excel('amz_update_url.xlsx')

