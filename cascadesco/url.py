from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
import time
import re
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


def get_data(url):

    # Fonction to scrape all urls from itch categories
    # Return Data

    #     s = HTMLSession()
    #     r = s.get(url)
    #     r.html.render(timeout= 30, sleep=1)
    print('Url:', url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    cookies = {'session': '134-8225175-0355220'}

    
    r = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(r.content, "html.parser")
    time.sleep(0.5)
    products = soup.find('div', {'class': 'new-grid product-grid collection-grid'}).find_all('a', {'class': 'grid-item__link'})

    liens = ['https://cascadesco.com' + toto['href'] for toto in products]
    print('Len products', len(liens))
    list_liens = []

    for t in liens:
        list_liens.append(t)

    return soup, list_liens


def getnextpage(soup):

    # Check if next url exist else send None objects
    # Return URL or None

    page = soup.find('a', {'title': 'Next'})
    # print('Page', page)

    try:
        # if next url exist
        url2 = str('https://cascadesco.com' + page['href'])
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
    print('Scrap:', url['url'])
    data = []
    url1 = url['url']
    while True:
        categories = url['categories']
        categories1 = url['cat1']
        soup, urls_list = get_data(url1)

        for toto in urls_list:

            # print(f'URL:', toto)
            data.append({
                'url': toto,
                'categories1': categories1,
                'categories': categories,
            })

        try:
            url1 = getnextpage(soup)
            print('Url dans le while', url1)
        except:
            break
    # print(data)
    print(f'Scrape done .')
    return data


urls = [
    { 'cat1': 'المنتجات الصدف', 'categories': '', 'url': 'https://cascadesco.com/collections/mother-of-pearl'},
    { 'cat1': 'السخانات والمناقل','categories': '44282', 'url': 'https://cascadesco.com/collections/heatrs-dua'},
    { 'cat1': 'المباخر', 'categories': '42800','url': 'https://cascadesco.com/collections/mabkhars'},
    { 'cat1': 'الإستاندات','categories': '42915,42916,42922,113', 'url': 'https://cascadesco.com/collections/stands'},
    { 'cat1': 'الصواني','categories': '42915,42916,42921,113', 'url': 'https://cascadesco.com/collections/trays'},
    { 'cat1': 'البوكسات والجارات','categories': '', 'url': 'https://cascadesco.com/collections/boxes-jars'},
    { 'cat1': 'الاطباق والصحون','categories': '42915,42916,42931', 'url': 'https://cascadesco.com/collections/bowels-plates'},
    { 'cat1': ' الورد الصناعي ','categories': '42,44,113', 'url': 'https://cascadesco.com/collections/artificial-flowers'},
    { 'cat1': 'الإكسسوارات المنزليه','categories': '37,43777,43779', 'url': 'https://cascadesco.com/collections/home-accesores'},
    { 'cat1': 'الشمعدانات','categories': '43816,43,113', 'url': 'https://cascadesco.com/collections/candle-holders'},
    { 'cat1': 'الفازات','categories': '42,43741,113', 'url': 'https://cascadesco.com/collections/vases'},
    { 'cat1': 'الخزف الصيني','categories': '42,43741,113', 'url': 'https://cascadesco.com/collections/china-blue'},


]

df = pd.read_excel('/home/wafistos/Documents/Projects/scaping_wafi/cascadesco/cascadesco_url_model.xlsx')
for i, url in enumerate(urls):
    print('Count: ', i)
    data = scrap_url_product(url)
    df1 = pd.DataFrame(data)
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('cascadosco.updating.url_products.xlsx')
