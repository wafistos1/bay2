

from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

list_urls = [
    
    {'url': 'https://jerm.online/collections/area-rugs/Area-Rug', 'cat1': 'Medium and Large Rugs', 'cat2': 'Area Rug', 'cat3': ''},
    {'url': 'https://jerm.online/collections/kilim-runners/Runner', 'cat1': 'Runners', 'cat2': 'runner', 'cat3': ''},
    {'url': 'https://jerm.online/collections/runners', 'cat1': 'Small Rugs', 'cat2': 'Small Rugs', 'cat3': ''},
    {'url': 'https://jerm.online/collections/artworks/Artwork', 'cat1': 'Handpicked Artworks and Accessories', 'cat2': 'artwork', 'cat3': ''},


]


def get_data(url):

    print('Url:', url)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    cookies = {'session': '134-8225175-0355220'}
    r = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(r.content, "html.parser")
    time.sleep(1)
    products = soup.find_all('a', {'class': 'grid-link text-center'})
    
    liens = [toto['href']  for toto in products]
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
    
    page = soup.find('a', {'title': 'Next »'})
    # print('Page', page)
    
    try:
        # if next url exist 
        url2 = 'https://jerm.online' + str(page['href'])
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


list_urls = [
    
    {'url': 'https://jerm.online/collections/area-rugs/Area-Rug', 'cat1': 'Medium and Large Rugs', 'cat2': 'Area Rug', 'cat3': ''},
    {'url': 'https://jerm.online/collections/kilim-runners/Runner', 'cat1': 'Runners', 'cat2': 'runner', 'cat3': ''},
    {'url': 'https://jerm.online/collections/runners', 'cat1': 'Small Rugs', 'cat2': 'Small Rugs', 'cat3': ''},
    {'url': 'https://jerm.online/collections/artworks/Artwork', 'cat1': 'Handpicked Artworks and Accessories', 'cat2': 'artwork', 'cat3': ''},


]


df = pd.read_excel('jerm_url_model.xlsx')
print('toto')
for i, url2 in enumerate(list_urls):
    print('Count: ', i)
    data = scrap_url_product(url2)

    df1 = pd.DataFrame(data)
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('jerm_update_url.xlsx')


