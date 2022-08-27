

from cgitb import enable
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
    
        
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    cookies = {'session': '134-8225175-0355220'}
    r = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(r.content, "html.parser")
    time.sleep(1)
    products = soup.find_all('div', {'class': 'product-item'})
    
    liens = ['https://hometimeksa.com' + p.find('a')['href'] for p in products]
    print('Len products', len(liens))
    cats = soup.find('ol', {'class': 'breadcrumb'}).find_all('li')
    len(cats)
    cat1 = cats[1].text.strip()
    list_liens = []
    
    for t in liens:
        list_liens.append(t)
#     print('list_cat1', list_cat1)

    return soup, list_liens


def getnextpage(soup):
   
    #Check if next url exist else send None objects
    # Return URL or None
    next_page = soup.find_all('li', 'page-item disabled')
    if next_page != []:
        next_page = soup.find('a', text='التالي')
        url2 = str(next_page['href'])
        return url2
    else:
        return None


# Extract new urls of Rugaib site from url categories

# url = 'https://rawae.com/search?subsubcategory=Accessories-box-Q3HaJ&page=1'
list_urls = []


def scrap_url_product(urls):
    
    
    url = urls['url']
    cat1 = urls['cat1']
    cat2 = urls['cat2']
    cat3 = urls['cat3']

    data = []
    
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

        
        url = getnextpage(soup)
        if url == None:
            break
    # print(data)
    print( f'Scrape done .')
    return data

urls = [
    {  'cat1': 'فازات', 'cat2': '', 'cat3': '', 'url': 'https://hometimeksa.com/categories/349798/%D9%81%D8%A7%D8%B2%D8%A7%D8%AA'},
    {  'cat1': 'كوسترات', 'cat2': '', 'cat3': '', 'url': 'https://hometimeksa.com/categories/349572/%D9%83%D9%88%D8%B3%D8%AA%D8%B1%D8%A7%D8%AA'},
    {  'cat1': 'المنتجات المخفضة', 'cat2': '', 'cat3': '', 'url': 'https://hometimeksa.com/categories/335852/%D8%A7%D9%84%D9%85%D9%86%D8%AA%D8%AC%D8%A7%D8%AA-%D8%A7%D9%84%D9%85%D8%AE%D9%81%D8%B6%D8%A9'},
    {  'cat1': 'إنارات', 'cat2': '', 'cat3': '', 'url': 'https://hometimeksa.com/categories/323100/%D8%A5%D9%86%D8%A7%D8%B1%D8%A7%D8%AA'},
    {  'cat1': 'مباخر', 'cat2': '', 'cat3': '', 'url': 'https://hometimeksa.com/categories/314711/%D9%85%D8%A8%D8%A7%D8%AE%D8%B1'},
    {  'cat1': 'شمعدان', 'cat2': '', 'cat3': '', 'url': 'https://hometimeksa.com/categories/314736/%D8%B4%D9%85%D8%B9%D8%AF%D8%A7%D9%86'},
    {  'cat1': 'أكواب-فناجيل-بيالات', 'cat2': '', 'cat3': '', 'url': 'https://hometimeksa.com/categories/314713/%D8%A3%D9%83%D9%88%D8%A7%D8%A8-%D9%82%D9%87%D9%88%D8%A9-%D9%88%D8%B4%D8%A7%D9%8A'},
]

df = pd.read_excel('/home/wafistos/Documents/Projects/scaping_wafi/hometimeksa/Hometimeksa.url_model.xlsx')

for i, url in enumerate(urls):
    print('Count: ', i)
    print('URL: ', url['url'])
    data = scrap_url_product(url)
    df1 = pd.DataFrame(data)
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('Home_urls.xlsx')