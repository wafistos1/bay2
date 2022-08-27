

from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

urls = [
    'https://www.virginmegastore.sa/ar/House/Smart-Home/Cameras-Monitors/c/K030201',
    'https://www.virginmegastore.sa/ar/House/Smart-Home/Lighting-Power/c/K030202',
    'https://www.virginmegastore.sa/ar/House/Smart-Home/Remotes-Controllers/c/K030203',
    'https://www.virginmegastore.sa/ar/House/Smart-Home/Alarms-Sensors/c/K030205',
    'https://www.virginmegastore.sa/ar/House/Smart-Home/Smart-Home-Accessories/c/K030209',
    
    
    'https://www.virginmegastore.sa/ar/House/Lifestyle/Home-Decor-Accessories/c/K030302',
    'https://www.virginmegastore.sa/ar/House/Lifestyle/Home-Kitchen-Care/c/K030306',
    'https://www.virginmegastore.sa/ar/House/Lifestyle/Health-Fitness/c/K030307',
    'https://www.virginmegastore.sa/ar/House/Lifestyle/Candles-Fragrances/c/K030303',
    'https://www.virginmegastore.sa/ar/House/Lifestyle/Personal-Care/c/K030305',
    
    
    'https://www.virginmegastore.sa/ar/House/Kitchen-Dining/Appliances/c/K030101',
    'https://www.virginmegastore.sa/ar/House/Kitchen-Dining/Bottles-Mugs/c/K030103',
    'https://www.virginmegastore.sa/ar/House/Kitchen-Dining/Coffee-Tea/c/K030105',
    'https://www.virginmegastore.sa/ar/House/Kitchen-Dining/Tableware/c/K030104',
    'https://www.virginmegastore.sa/ar/House/Kitchen-Dining/Kitchen-Accessories/c/K030109',
    
    
]



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
    products = soup.find_all('a', {'class': 'product-list__thumb position-relative d-flex'})
    
    liens = ['https://www.virginmegastore.sa' + t['href'] for t in products]
    print('Len products', len(liens))

    return soup, liens


def getnextpage(soup):
   
    #Check if next url exist else send None objects
    # Return URL or None
    
    next_page = soup.find('span', text='التالي')

    url  = next_page.parent['href']
    # print('Page', page)
    
    try:
        # if next url exist 
        url2 = next_page.parent['href']
        return url2
        # print('', url2)
    except:
        print('No Next')
        pass
    return url2 


# Extract new urls of Rugaib site from url categories

# url = 'https://rawae.com/search?subsubcategory=Accessories-box-Q3HaJ&page=1'
list_urls = []


def scrap_url_product(url):
    
    
    

    
    data = []
    while True:
        soup, urls_list = get_data(url)
        cats = soup.find('div', {'class': 'breadcrumb-list'}).find_all('div')
        cat1 = cats[1].find('a').text.strip()
        cat2 = cats[2].find('a').text.strip()
        cat3 = cats[3].text.strip()
        for toto in urls_list:

            # print(f'URL:', toto)
            data.append({
            'url':toto,
            'cat1': cat1,
            'cat2': cat2,
            'cat3': cat3,
            })

        try:
            url = url.split('?')[0]  + getnextpage(soup)
#             print('Url dans le while', url)
        except:
            break
    # print(data)
    print( f'Scrape done .')
    return data

df = pd.read_excel('/home/wafistos/Documents/Projects/scaping_wafi/virginmegastore/Virgin_model.xlsx')
for i, url in enumerate(urls):
    print('Count: ', i)
    data = scrap_url_product(url)
    df1 = pd.DataFrame(data)
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('Virgin_urls.xlsx')

